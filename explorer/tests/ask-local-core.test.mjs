// On-device Ask (#590): a fresh conversation per question, the compact result the model sees, the lock's verdict
// on the page, and the sampling options Chrome 155 accepts. The model replies are the ones Gemini Nano wrote on
// 2026-10-25 (docs/assessments/ai-on-the-map.md); the lock is a stub here (its rules are tested in pytest).
import { test } from "node:test";
import assert from "node:assert/strict";

import {
  askLoop, createSession, deviceAnswerHtml, deviceAnswerMarkdown, parseReply, samplingNote, samplingOptions, sessionPool, stepPrompt,
  inView, selectedGaugeContext, withCatalogueName,
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
  // One conversation per step: two for the first question (tool, answer), one for the second.
  assert.equal(eng.convs.length, 3);
  assert.ok(eng.convs.every((c) => c.closed), "every conversation is closed after its step");
  assert.ok(eng.convs.every((c) => c.prompts.length === 1), "no conversation takes a second prompt");
  assert.ok(!eng.convs[2].prompts.join(" ").includes("320.7738"), "the second question never saw the first result");
  assert.equal(first.lock.ok, true);
  assert.equal(second.results.length, 0);
  assert.equal(second.lock.ok, false);
});

test("the model is shown the whole compact result, trend included, never a 3,000-character cut", async () => {
  const eng = recordingEngine(['{"tool": "analyze_station", "arguments": {}}', '{"answer": "ok"}']);
  const big = { ...POTOMAC, notes: ["x".repeat(3500)] };
  await askLoop("Summarise", { open: () => eng.open(), callTool: async () => ({ ok: true, compact: big }),
    lock: async () => ({ ok: true }) });
  const second = eng.convs[1].prompts[0];
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

// ── one prompt per session (recheck, 2026-10-26) ─────────────────────────────
// In Chrome 155 a second prompt in a session failed with "kErrorUnknown" in 11 of 13 trials after a first prompt
// with a responseConstraint; the same text as the only prompt of a fresh clone ran 4 of 4. This engine fails the
// same way: a conversation's second prompt throws.
function chromeLikeEngine(replies, { failFirst = 0 } = {}) {
  const convs = [];
  let failures = failFirst;
  return {
    convs,
    open() {
      const conv = { prompts: [], closed: false };
      convs.push(conv);
      return {
        async generate(prompt) {
          conv.prompts.push(prompt);
          if (conv.prompts.length > 1) throw new Error("kErrorUnknown");
          if (failures > 0) { failures -= 1; throw new Error("kErrorUnknown"); }
          return replies.shift();
        },
        close() { conv.closed = true; },
      };
    },
  };
}

const SUMMARY = "Summarise the record at this gauge: period, mean, trend, and the flood frequency";

test("the summary question reaches its answer: each step is the only prompt of its own session", async () => {
  const eng = chromeLikeEngine([
    '{"tool": "analyze_station", "arguments": {"source": "usgs", "station_id": "01646500"}}',
    '{"answer": "USGS 01646500, 1930-03-01 to 2026-10-24: mean 320.7738 m3/s, no significant trend."}',
  ]);
  const res = await askLoop(SUMMARY, { open: () => eng.open(), callTool: async () => ({ ok: true, compact: POTOMAC }),
    lock: async () => ({ ok: true, refused: [], facts: [], notes: [] }), context: "The user is looking at the gauge USGS 01646500." });
  assert.equal(res.canned, false);
  assert.match(res.answer, /320\.7738/);
  assert.equal(eng.convs.length, 2);
  assert.ok(eng.convs.every((c) => c.prompts.length === 1 && c.closed));
  // Step 2 carries the question and the result, as one prompt.
  assert.ok(eng.convs[1].prompts[0].startsWith(SUMMARY));
  assert.match(eng.convs[1].prompts[0], /Result of analyze_station\({"source":"usgs","station_id":"01646500"}\): {"source":"usgs"/);
});

test("a step that fails is tried once more in a fresh session", async () => {
  const eng = chromeLikeEngine([
    '{"tool": "analyze_station", "arguments": {"source": "usgs", "station_id": "01646500"}}',
    '{"answer": "Mean 320.7738 m3/s."}',
  ], { failFirst: 1 });
  const events = [];
  const res = await askLoop(SUMMARY, { open: () => eng.open(), callTool: async () => ({ ok: true, compact: POTOMAC }),
    lock: async () => ({ ok: true }), onEvent: (m) => events.push(m) });
  assert.equal(res.answer, "Mean 320.7738 m3/s.");
  assert.equal(eng.convs.length, 3);
  assert.ok(eng.convs.every((c) => c.closed));
  assert.ok(events.some((e) => /Step 1 failed \(kErrorUnknown\); trying it once more/.test(e)));
});

test("a step that fails twice after a tool ran shows the tools' facts and the reason, not an error", async () => {
  const eng = chromeLikeEngine(['{"tool": "analyze_station", "arguments": {}}'], { failFirst: 0 });
  // Steps after the first all fail.
  let calls = 0;
  const open = () => {
    calls += 1;
    if (calls === 1) return eng.open();
    return { async generate() { throw new Error("kErrorUnknown"); }, close() {} };
  };
  const res = await askLoop(SUMMARY, { open, callTool: async () => ({ ok: true, compact: POTOMAC }),
    lock: async (answer) => ({ ok: !answer, refused: [], facts: ["usgs 01646500: discharge 1930-03-01 to 2026-10-24."], notes: [] }) });
  assert.equal(calls, 3);
  assert.equal(res.lock.ok, false);
  assert.match(res.stopped, /stopped at step 2, twice \(kErrorUnknown\)/);
  const html = deviceAnswerHtml({ ...res, model: "Chrome built-in (Gemini Nano)" });
  assert.match(html, /No answer: the on-device model stopped at step 2, twice \(kErrorUnknown\)\. What the tools returned:/);
  assert.match(html, /<li>usgs 01646500: discharge 1930-03-01 to 2026-10-24\.<\/li>/);
  assert.match(deviceAnswerMarkdown(SUMMARY, res), /No answer: the on-device model stopped at step 2/);
});

test("a first step that fails twice is an error the page reports, as before", async () => {
  const open = () => ({ async generate() { throw new Error("kErrorUnknown"); }, close() {} });
  await assert.rejects(askLoop(SUMMARY, { open, callTool: async () => ({}), lock: async () => ({ ok: true }) }), /kErrorUnknown/);
});

test("the step prompt carries every result so far, not only the last", () => {
  const p = stepPrompt("q\n\nContext: c", "q", [
    { name: "find_stations", arguments: { query: "Kingston" }, compact: { stations: [{ station_id: "E1" }] } },
    { name: "analyze_station", arguments: { station_id: "E1" }, compact: { mean: 1 } },
  ]);
  assert.match(p, /Result of find_stations/);
  assert.match(p, /Result of analyze_station/);
  assert.equal(stepPrompt("q\n\nContext: c", "q", []), "q\n\nContext: c");
});

// ── warm sessions for the one-off calls (recheck item 5) ─────────────────────
// A stub LanguageModel that counts creates, clones and destroys. This checks only that the pool is correct;
// whether a clone of a warm base is quicker than a create needs Chrome's model on a device.
function stubLM({ cloneFails = false } = {}) {
  const log = { create: [], clone: 0, destroyed: [] };
  let n = 0;
  const make = (system, kind) => {
    const id = `${kind}${++n}`;
    return {
      id, system,
      async clone() { if (cloneFails) throw new Error("clone failed"); log.clone += 1; return make(system, "clone"); },
      async prompt() { return "{}"; },
      destroy() { log.destroyed.push(id); },
    };
  };
  return { log, async create(options) { const sys = options.initialPrompts[0].content; log.create.push(sys); return make(sys, "base"); } };
}

test("one warm base per system prompt: later calls clone it rather than create a session", async () => {
  const LM = stubLM();
  const pool = sessionPool(LM);
  const a = await pool.open("map system", { samplingMode: "most-predictable" });
  const b = await pool.open("map system", { samplingMode: "most-predictable" });
  assert.equal(LM.log.create.length, 1, "the base is created once");
  assert.equal(LM.log.clone, 2);
  assert.ok(a.id.startsWith("clone") && b.id.startsWith("clone") && a !== b, "each call gets its own clone");
  await pool.open("explain system");
  assert.equal(LM.log.create.length, 2, "another system prompt gets its own base");
  assert.equal(pool.size(), 2);
  a.destroy();
  assert.deepEqual(LM.log.destroyed, [a.id], "destroying a clone leaves the base warm");
});

test("the pool keeps at most a few bases, destroying the least recently used", async () => {
  const LM = stubLM();
  const pool = sessionPool(LM, { max: 2 });
  await pool.open("one");
  await pool.open("two");
  await pool.open("one");      // touch "one"
  await pool.open("three");    // evicts "two"
  await new Promise((r) => setTimeout(r, 0));
  assert.equal(pool.size(), 2);
  assert.equal(LM.log.destroyed.length, 1);
  await pool.open("one");
  assert.equal(LM.log.create.filter((s) => s === "one").length, 1, "the used base stayed warm");
  await pool.open("two");
  assert.equal(LM.log.create.filter((s) => s === "two").length, 2, "the evicted base is created again");
});

test("a clone that fails falls back to a fresh session", async () => {
  const LM = stubLM({ cloneFails: true });
  const pool = sessionPool(LM);
  const s = await pool.open("sys");
  assert.ok(s.id.startsWith("base"));
  assert.equal(LM.log.create.length, 2, "the base, then a fresh session for this call");
});

// ── the context line (recheck item 9) ─────────────────────────────────────────
const POTOMAC_ROW = { source: "usgs", station_id: "01646500", name: "POTOMAC RIVER NEAR WASH, DC LITTLE FALLS PUMP STA",
  lat: 38.9497, lon: -77.1275 };
const EUROPE = { west: -12, south: 35, east: 32, north: 62 };
const VIRGINIA = { west: -78, south: 38.5, east: -76.5, north: 39.3 };

test("a selected gauge off screen is left out for the map's roles and said as off screen for Ask", () => {
  assert.match(selectedGaugeContext(POTOMAC_ROW, VIRGINIA), /^the gauge POTOMAC RIVER .* id 01646500, 38\.950, -77\.127\)$/);
  // Recorded: Scout in Europe ordered USGS-01646500, from the context line, which named it though it was off screen.
  assert.equal(selectedGaugeContext(POTOMAC_ROW, EUROPE), "");
  assert.match(selectedGaugeContext(POTOMAC_ROW, EUROPE, { offScreen: "say" }), /, selected earlier and now off screen$/);
  assert.match(selectedGaugeContext(POTOMAC_ROW, null), /^the gauge POTOMAC/, "no map yet: said as before");
});

test("inView wraps across the antimeridian and takes a whole-world view", () => {
  assert.ok(inView({ west: 170, south: -50, east: 190, north: -30 }, -41, -175));
  assert.ok(!inView({ west: 170, south: -50, east: 190, north: -30 }, -41, 160));
  assert.ok(inView({ west: -540, south: -85, east: 540, north: 85 }, 10, 100));
  assert.ok(!inView(EUROPE, 70, 10));
});

test("an analysis carries the catalogue's name and river, so two gauges can be told apart", () => {
  const byKey = new Map([["usgs/01646500", { ...POTOMAC_ROW, river: "Potomac River" }]]);
  const out = withCatalogueName({ ok: true, compact: { source: "usgs", station_id: "01646500", unit: "m3/s" } },
    { source: "usgs", station_id: "01646500" }, byKey);
  assert.equal(out.compact.name, POTOMAC_ROW.name);
  assert.equal(out.compact.river, "Potomac River");
  const err = { ok: false, compact: { error: "no data" } };
  assert.equal(withCatalogueName(err, {}, byKey), err);
  const named = { ok: true, compact: { source: "usgs", station_id: "01646500", name: "Little Falls" } };
  assert.equal(withCatalogueName(named, {}, byKey).compact.name, "Little Falls");
});
