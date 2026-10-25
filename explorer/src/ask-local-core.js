// On-device Ask (#590), the parts with no browser in them, so node can run them with the model's recorded replies:
// the loop over one fresh conversation per question, the sampling options Chrome accepts, and the answer as
// the page shows it once the package's lock (aquascope.ai_engine.device_ask.lock_answer) has read it.
//
// What went wrong on the device: one Prompt API session served every question, so a later answer quoted an
// earlier question's tool result; the tool result was cut at 3,000 characters, so the trend never reached the
// model; and nothing checked the answer. Now each question opens its own conversation and closes it, the
// model sees the package's compact result (stats, trend, return levels, no series), and the answer is shown
// only when every number, id and trend word in it is in this question's results.

/** The model's reply as an object: a tool call, or {answer}. Prose around the JSON is tolerated. */
export function parseReply(text) {
  const raw = String(text || "").trim();
  const start = raw.indexOf("{");
  const end = raw.lastIndexOf("}");
  if (start < 0 || end <= start) return { answer: raw };
  try {
    return JSON.parse(raw.slice(start, end + 1));
  } catch {
    return { answer: raw };
  }
}

/**
 * The sampling options `LanguageModel.create()` takes, feature-detected (checked against
 * developer.chrome.com/docs/ai/prompt-api on 2026-10-25).
 *
 * In a Chrome extension, `LanguageModel.params()` gives the default topK and the temperature range, and a
 * session takes `topK` and `temperature`, both or neither. On the web there is no `params()` (it is
 * undefined in Chrome 155, which is why the 0.1 asked for was never set) and no raw numbers: the sampling
 * origin trial adds `samplingMode`, one of seven words, "most-predictable" through "most-creative". Without the trial
 * the member is ignored and Chrome keeps its own sampling; `samplingNote()` says which happened.
 */
export async function samplingOptions(LM, temperature) {
  if (LM && typeof LM.params === "function") {
    try {
      const p = await LM.params();
      if (p && Number.isFinite(p.defaultTopK)) {
        return { temperature: Math.min(temperature, Number.isFinite(p.maxTemperature) ? p.maxTemperature : temperature),
          topK: p.defaultTopK };
      }
    } catch { /* fall through to the web's option */ }
    return {};
  }
  const mode = temperature <= 0.2 ? "most-predictable" : temperature <= 0.5 ? "predictable" : "balanced";
  return { samplingMode: mode };
}

/** `LanguageModel.create(options)`, retried without the sampling option if this Chrome refuses it. */
export async function createSession(LM, options) {
  try {
    return await LM.create(options);
  } catch (err) {
    if (!("samplingMode" in options) && !("temperature" in options)) throw err;
    const rest = { ...options };
    for (const k of ["samplingMode", "temperature", "topK"]) delete rest[k];
    return LM.create(rest);
  }
}

/** What sampling a session actually runs with, in words: what was set, never what was only asked for. */
export function samplingNote(session) {
  if (session && typeof session.samplingMode === "string" && session.samplingMode) return `sampling ${session.samplingMode}`;
  if (session && Number.isFinite(session.temperature)) return `temperature ${session.temperature}`;
  return "Chrome's default sampling";
}

const STEPS_USED = "The local model used its steps without reaching an answer. A larger model (bring your own key) will do better on this question.";
const NO_ANSWER = "The local model did not produce an answer.";

/**
 * One question on the device. `open()` gives a fresh conversation `{generate(prompt), close()}`, closed when
 * the question is done; `callTool(name, args)` runs a tool in the worker and returns `{ok, compact}` (the
 * package's compact result, which is all the model sees); `lock(answer, results, words)` is the package's
 * check. Returns `{answer, toolCalls, results, lock, canned}`; `canned` marks the page's own text.
 */
export async function askLoop(question, { open, callTool, lock, onEvent = () => {}, maxSteps = 3, context = "" } = {}) {
  const words = context ? `${question}\n\nContext: ${context}` : question;
  const toolCalls = [];
  const results = [];
  let answer = null;
  const conv = await open();
  try {
    let prompt = words;
    for (let step = 1; step <= maxSteps; step++) {
      // A small model takes twenty seconds or so over a couple of tool calls.
      // Without a running commentary that is indistinguishable from a hang.
      onEvent(`Thinking… (step ${step} of ${maxSteps})`);
      const reply = parseReply(await conv.generate(prompt));
      if (reply.answer || !reply.tool) {
        answer = typeof reply.answer === "string" && reply.answer.trim() ? reply.answer.trim() : "";
        break;
      }
      const args = reply.arguments && typeof reply.arguments === "object" ? reply.arguments : {};
      onEvent(`tool ${reply.tool}(${JSON.stringify(args).slice(0, 120)})`);
      let out;
      try {
        onEvent(`Running ${reply.tool}…`);
        out = await callTool(reply.tool, args);
      } catch (err) {
        out = { ok: false, compact: { error: err.message } };
      }
      const ok = Boolean(out && out.ok);
      const compact = (out && out.compact) || {};
      results.push({ name: reply.tool, arguments: args, compact, ok });
      toolCalls.push({ name: reply.tool, arguments: args, ok });
      prompt = `${question}\n\nResult of ${reply.tool}: ${JSON.stringify(compact)}\n\n` +
        "Now reply with either another tool call or the final answer, as one JSON object.";
    }
  } finally {
    try { conv.close(); } catch { /* fine */ }
  }
  if (answer === null) return { answer: STEPS_USED, toolCalls, results, lock: null, canned: true };
  if (!answer) return { answer: NO_ANSWER, toolCalls, results, lock: null, canned: true };
  let verdict;
  try {
    verdict = await lock(answer, results, words);
  } catch (err) {
    verdict = { ok: false, refused: [`the check could not run (${err.message})`], facts: [], notes: [] };
  }
  return { answer, toolCalls, results, lock: verdict, canned: false };
}

const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

/** The answer block: the model's words when the lock passed, else the tools' facts and one line why. */
export function deviceAnswerHtml(result) {
  const head = `<div class="showcase-note">Answered on your device by ${esc(result.model || "a local model")}, ` +
    `with a reduced tool set and no key. Small models are weaker at multi-step work: for a hard question, ` +
    `bring a key above.</div>`;
  const lock = result.lock;
  const notes = lock && Array.isArray(lock.notes) && lock.notes.length
    ? `<p class="ask-device-note">${lock.notes.map(esc).join(" ")}</p>` : "";
  if (!lock || lock.ok) return `${head}<p>${esc(result.answer)}</p>${notes}`;
  const why = (lock.refused || []).join("; ") || "it did not match the tool results";
  const facts = Array.isArray(lock.facts) && lock.facts.length
    ? `<ul class="ask-device-facts">${lock.facts.map((f) => `<li>${esc(f)}</li>`).join("")}</ul>`
    : "<p>No tool ran for this question, so there are no results to show. Ask again, naming the gauge or the place.</p>";
  return `${head}<p class="ask-refused">The model's wording was refused: ${esc(why)}. What the tools returned:</p>` +
    facts + notes;
}

/** The same, as Markdown for Copy and Download. */
export function deviceAnswerMarkdown(question, result) {
  const lock = result.lock;
  const notes = lock && Array.isArray(lock.notes) && lock.notes.length ? `\n${lock.notes.join(" ")}\n` : "";
  if (!lock || lock.ok) return `# ${question}\n\n${result.answer}\n${notes}`;
  const why = (lock.refused || []).join("; ") || "it did not match the tool results";
  const facts = (lock.facts || []).map((f) => `- ${f}`).join("\n") || "No tool ran for this question.";
  return `# ${question}\n\nThe model's wording was refused: ${why}. What the tools returned:\n\n${facts}\n${notes}`;
}
