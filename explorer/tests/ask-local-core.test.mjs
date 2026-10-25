// On-device Ask (#590): a fresh conversation per question, the compact result the model sees, the lock's verdict
// on the page, and the sampling options Chrome 155 accepts. The model replies are the ones Gemini Nano wrote on
// 2026-10-25 (docs/assessments/ai-on-the-map.md); the lock is a stub here (its rules are tested in pytest).
import { test } from "node:test";
import assert from "node:assert/strict";

import {
  askLoop, createSession, deviceAnswerHtml, deviceAnswerMarkdown, parseReply, samplingNote, samplingOptions,
} from "../src/ask-local-core.js";
import { numbersIn, parseBriefReply } from "../src/intake.js";

// An engine whose conversations remember what they were told, as a Prompt API session does.
function recordingEngine(replies) {
  const convs = [];
  return {
    convs,
    open() {
      const conv = { prompts: [], closed: false };
      convs.push(conv);
      return {
        async generate(prompt) {
          conv.prompts.push(prompt);
          return replies.shift();
        },
        close() { conv.closed = true; },
      };
    },
  };
}

const POTOMAC = {
  source: "usgs", station_id: "01646500", unit: "m3/s", start: "1930-03-01", end: "2026-10-24",
  daily_values: { mean: 320.7738, min: 3.43, max: 12100 },
  trend_annual_mean: { on: "annual mean", p_value: 0.82, sens_slope_per_year: 0.059, significant: false,
    reading: "no significant trend in the annual mean (Mann-Kendall p = 0.82; Sen's slope +0.059 m3/s per year)" },
};

test("each question opens its own conversation and closes it, so an earlier result cannot answer a later one", async () => {
  const eng = recordingEngine([
    '{"tool": "analyze_station", "arguments": {"source": "usgs", "station_id": "01646500"}}',
    '{"answer": "Mean 320.7738 m3/s from 1930 to 2026."}',
    // Recorded second question: no tool call, numbers from the first question's result.
    '{"answer": "The 100-year flood (Q10) is not directly available; the record is from 1930-03-01."}',
  ]);
  const callTool = async () => ({ ok: true, compact: POTOMAC });
  const lock = async (answer, results) => ({ ok: results.length > 0, refused: results.length ? [] : ["Q10 is in no result for this question"], facts: [], notes: [] });
  const first = await askLoop("Summarise the record", { open: () => eng.open(), callTool, lock });
  const second = await askLoop("What is the 100-year flood at this gauge?", { open: () => eng.open(), callTool, lock });
  assert.equal(eng.convs.length, 2);
  assert.ok(eng.convs.every((c) => c.closed), "every conversation is closed after its question");
  assert.ok(!eng.convs[1].prompts.join(" ").includes("320.7738"), "the second conversation never saw the first result");
  assert.equal(first.lock.ok, true);
  assert.equal(second.results.length, 0);
  assert.equal(second.lock.ok, false);
});

test("the model is shown the whole compact result, trend included, never a 3,000-character cut", async () => {
  const eng = recordingEngine(['{"tool": "analyze_station", "arguments": {}}', '{"answer": "ok"}']);
  const big = { ...POTOMAC, notes: ["x".repeat(3500)] };
  await askLoop("Summarise", { open: () => eng.open(), callTool: async () => ({ ok: true, compact: big }),
    lock: async () => ({ ok: true }) });
  const second = eng.convs[0].prompts[1];
  assert.ok(second.includes('"p_value":0.82') && second.includes("no significant trend"));
  assert.ok(second.length > 3500);
});

test("a refused answer shows the tools' facts and one line why, never the model's text", async () => {
  // Recorded: "Is the Potomac at Little Falls getting drier? Use the annual-mean trend." with no tool call.
  const bad = "The Potomac at Little Falls shows an increasing trend. The Mann-Kendall test indicates an upward trend.";
  const eng = recordingEngine([JSON.stringify({ answer: bad })]);
  const res = await askLoop("Is the Potomac at Little Falls getting drier?", {
    open: () => eng.open(), callTool: async () => ({ ok: true, compact: {} }),
    lock: async () => ({ ok: false, refused: ["the answer states a trend, but no trend was computed for this question"], facts: [], notes: [] }),
  });
  const html = deviceAnswerHtml({ ...res, model: "Chrome built-in (Gemini Nano)" });
  assert.ok(!html.includes("upward trend"));
  assert.match(html, /The model's wording was refused: the answer states a trend, but no trend was computed/);
  assert.match(html, /No tool ran for this question/);
  const facts = deviceAnswerHtml({ answer: bad, lock: { ok: false, refused: ["x"], facts: ["Trend: no significant trend (p = 0.82)."], notes: [] } });
  assert.match(facts, /<li>Trend: no significant trend \(p = 0\.82\)\.<\/li>/);
  assert.match(deviceAnswerMarkdown("Q", { answer: bad, lock: { ok: false, refused: ["x"], facts: ["F"] } }), /refused: x\. .*\n\n- F/);
});

test("a passing answer is shown with the lock's notes, and a broken lock fails closed", async () => {
  const ok = deviceAnswerHtml({ answer: "KINGSTON VALE (E02102A).", lock: { ok: true, refused: [], facts: [],
    notes: ["The search was near 51.1, 0.0, a point the model chose."] } });
  assert.match(ok, /KINGSTON VALE \(E02102A\)\./);
  assert.match(ok, /a point the model chose/);
  const eng = recordingEngine(['{"answer": "Mean 999 m3/s."}']);
  const res = await askLoop("q", { open: () => eng.open(), callTool: async () => ({}), lock: async () => { throw new Error("worker gone"); } });
  assert.equal(res.lock.ok, false);
  assert.match(res.lock.refused[0], /the check could not run \(worker gone\)/);
});

test("the page's own lines are not sent to the lock", async () => {
  const eng = recordingEngine(["", '{"tool": "find_stations", "arguments": {}}', '{"tool": "find_stations", "arguments": {}}']);
  const lock = async () => { throw new Error("must not be called"); };
  const none = await askLoop("q", { open: () => eng.open(), callTool: async () => ({ ok: true, compact: {} }), lock });
  assert.equal(none.canned, true);
  const used = await askLoop("q", { open: () => eng.open(), callTool: async () => ({ ok: true, compact: {} }), lock, maxSteps: 2 });
  assert.equal(used.canned, true);
  assert.match(used.answer, /used its steps/);
});

test("parseReply tolerates prose around the JSON", () => {
  assert.deepEqual(parseReply('Sure: {"answer": "x"} done'), { answer: "x" });
  assert.deepEqual(parseReply("no json"), { answer: "no json" });
});

test("sampling: Chrome 155 on the web has no params(), so the page asks for samplingMode and says what it got", async () => {
  // Chrome 155 on a web page: LanguageModel.params is undefined (recorded on 2026-10-25).
  const web = { create: async (o) => ({ samplingMode: o.samplingMode }) };
  assert.deepEqual(await samplingOptions(web, 0.1), { samplingMode: "most-predictable" });
  assert.equal(samplingNote(await createSession(web, await samplingOptions(web, 0.1))), "sampling most-predictable");
  // Without the origin trial the member is ignored: the note says Chrome's own sampling, not 0.1.
  assert.equal(samplingNote({}), "Chrome's default sampling");
  // An extension still has params(): topK and temperature together.
  const ext = { params: async () => ({ defaultTopK: 3, maxTemperature: 2, defaultTemperature: 1 }) };
  assert.deepEqual(await samplingOptions(ext, 0.1), { temperature: 0.1, topK: 3 });
  // A Chrome that refuses the option still gets a session, without it.
  const seen = [];
  const strict = { create: async (o) => { seen.push(o); if ("samplingMode" in o) throw new TypeError("no"); return {}; } };
  await createSession(strict, { initialPrompts: [], samplingMode: "most-predictable" });
  assert.equal(seen.length, 2);
  assert.ok(!("samplingMode" in seen[1]) && "initialPrompts" in seen[1]);
});

test("Studio brief: a return period or timescale the sentence does not hold is dropped (recorded replies)", () => {
  const winter = "Will the road by the pump station flood this winter?";
  assert.deepEqual(parseBriefReply('{"return_period": 1, "quantities": ["this winter"]}', winter),
    { brief: { quantities: ["this winter"] }, intake: {} });
  const school = "Is this site safe from a big flood for a new school?";
  assert.equal(parseBriefReply('{"return_period": 100}', school), null);   // a guess, even in range
  const bridge = "I need the design flood for a footbridge here, something like the 50-year peak, using data since 1980";
  assert.deepEqual(parseBriefReply('{"return_period": 50, "decision": "Design flood calculation"}', bridge),
    { brief: { decision: "Design flood calculation" }, intake: { return_period: 50 } });
  assert.deepEqual(parseBriefReply('{"return_period": 100}', "what is the hundred-year flood here?").intake, { return_period: 100 });
  assert.deepEqual(parseBriefReply('{"timescales": [3, 12, 6]}', "drought at 3 and twelve months").intake, { timescales: [3, 12] });
  assert.deepEqual(parseBriefReply('{"return_period": 200}').intake, { return_period: 200 }, "no sentence, no check");
  assert.deepEqual([...numbersIn("a 1 in 10,000 year event, two hundred years, twenty-five")].sort((a, b) => a - b),
    [1, 25, 200, 10000]);
});
