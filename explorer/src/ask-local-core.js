// On-device Ask (#590), the parts with no browser in them, so node can run them with the model's recorded replies:
// the loop over one fresh conversation per step, the sampling options Chrome accepts, and the answer as
// the page shows it once the package's lock (aquascope.ai_engine.device_ask.lock_answer) has read it.
//
// What went wrong on the device: one Prompt API session served every question, so a later answer quoted an
// earlier question's tool result; the tool result was cut at 3,000 characters, so the trend never reached the
// model; and nothing checked the answer. Now each step of a question opens its own conversation and closes it
// (a second prompt in a session failed with "kErrorUnknown" in the recheck), the model sees the package's
// compact result (stats, trend, return levels, no series), and the answer is shown only when every number, id,
// label and trend word in it holds against this question's results.

/** Is a point inside a view {west, south, east, north} (degrees)? A view across the antimeridian wraps. */
export function inView(view, lat, lon) {
  if (!view || !Number.isFinite(lat) || !Number.isFinite(lon)) return false;
  const { west, south, east, north } = view;
  if (!(lat >= south && lat <= north)) return false;
  if (east - west >= 360) return true;
  const wrap = (x) => ((((x + 180) % 360) + 360) % 360) - 180;
  const w = wrap(west), e = wrap(east), x = wrap(lon);
  return w <= e ? x >= w && x <= e : x >= w || x <= e;
}

/**
 * The selected gauge as the context line says it. In view, as it was. Off screen (the recheck found Scout in
 * Europe ordering the Potomac gauge, selected earlier, because the line named it): `offScreen: "say"` keeps it
 * and says so (Ask, where "this gauge" still means it), `"omit"` leaves it out (the map's roles, which are
 * about the view).
 */
export function selectedGaugeContext(r, view, { offScreen = "omit" } = {}) {
  if (!r) return "";
  const what = `the gauge ${r.name || r.station_id} (source ${r.source}, id ${r.station_id}, ` +
    `${Number(r.lat).toFixed(3)}, ${Number(r.lon).toFixed(3)})`;
  if (!view || inView(view, r.lat, r.lon)) return what;
  return offScreen === "say" ? `${what}, selected earlier and now off screen` : "";
}

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

/**
 * Warm sessions for one-off structured calls (Ask the map, Explain, Scout, What-if, the review): one base
 * session per system prompt, created once and never prompted, and a clone of it for each call, which the
 * caller destroys. `LanguageModel.create` took 20.6 to 21.1 s on 7 of 21 calls in the recheck (2026-10-26);
 * a call that clones a warm base does not create one. Whether a clone is quicker than a create on the device
 * is not measured here (Ask's clones also stalled now and then): that needs Chrome's model. At most `max`
 * bases are kept, the least recently used destroyed first. A base or a clone that fails falls back to a
 * fresh session, as before.
 */
export function sessionPool(LM, { max = 4 } = {}) {
  const bases = new Map();   // key -> Promise<session>
  const drop = (p) => { p.then((b) => { try { b.destroy(); } catch { /* fine */ } }, () => {}); };
  function base(key, options) {
    if (bases.has(key)) {
      const p = bases.get(key);
      bases.delete(key);
      bases.set(key, p);     // most recently used last
      return p;
    }
    const p = createSession(LM, options);
    bases.set(key, p);
    p.catch(() => { if (bases.get(key) === p) bases.delete(key); });
    while (bases.size > max) {
      const [oldest, old] = bases.entries().next().value;
      bases.delete(oldest);
      drop(old);
    }
    return p;
  }
  return {
    async open(system, sampling = {}) {
      const options = { initialPrompts: [{ role: "system", content: system }], ...sampling };
      const key = JSON.stringify([system, sampling]);
      let session = null;
      try {
        const b = await base(key, options);
        session = typeof b.clone === "function" ? await b.clone() : null;
      } catch {
        session = null;
      }
      return session || createSession(LM, options);
    },
    size: () => bases.size,
    clear() { for (const p of bases.values()) drop(p); bases.clear(); },
  };
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
 * A tool's `{ok, compact}` with the catalogue row's name and river added to an analysis (analyze_station
 * carries the id and no name). `byKey` is the page's catalogue map, keyed "source/station_id".
 */
export function withCatalogueName(out, args, byKey) {
  const c = out && out.compact;
  if (!c || typeof c !== "object" || c.error || !byKey || typeof byKey.get !== "function") return out;
  const source = c.source || (args && args.source);
  const id = c.station_id || (args && args.station_id);
  const row = source && id ? byKey.get(`${source}/${id}`) : null;
  if (!row) return out;
  const extra = {};
  if (!c.name && row.name) extra.name = row.name;
  if (!c.river && row.river) extra.river = row.river;
  return Object.keys(extra).length ? { ...out, compact: { ...c, ...extra } } : out;
}

/** The prompt for one step: the question, then every tool result so far, so a step needs no earlier turn. */
export function stepPrompt(words, question, results) {
  if (!results.length) return words;
  const seen = results.map((r) => `Result of ${r.name}(${JSON.stringify(r.arguments || {})}): ${JSON.stringify(r.compact)}`);
  return `${question}\n\n${seen.join("\n\n")}\n\n` +
    "Now reply with either another tool call or the final answer, as one JSON object.";
}

/**
 * One question on the device. `open()` gives a fresh conversation `{generate(prompt), close()}`; `callTool(name,
 * args)` runs a tool in the worker and returns `{ok, compact}` (the package's compact result, which is all the
 * model sees); `lock(answer, results, words)` is the package's check. Returns `{answer, toolCalls, results, lock,
 * canned, stopped}`; `canned` marks the page's own text, `stopped` the step the model failed at twice.
 *
 * Each step runs in a conversation of its own, opened for that one prompt and closed after it. In Chrome 155 a
 * second prompt in a session failed with "kErrorUnknown" in 11 of 13 trials after a first prompt with a
 * `responseConstraint`, and the same text as the only prompt of a fresh clone ran 4 of 4 (recheck, 2026-10-26).
 * So a step's prompt carries the question and every tool result so far, and a step that fails is tried once
 * more in another fresh conversation. A second failure after tools ran shows what they returned.
 */
export async function askLoop(question, { open, callTool, lock, onEvent = () => {}, maxSteps = 3, context = "" } = {}) {
  const words = context ? `${question}\n\nContext: ${context}` : question;
  const toolCalls = [];
  const results = [];
  let answer = null;
  const once = async (prompt) => {
    const conv = await open();
    try {
      return await conv.generate(prompt);
    } finally {
      try { conv.close(); } catch { /* fine */ }
    }
  };
  for (let step = 1; step <= maxSteps; step++) {
    // A small model takes twenty seconds or so over a couple of tool calls.
    // Without a running commentary that is indistinguishable from a hang.
    onEvent(`Thinking… (step ${step} of ${maxSteps})`);
    const prompt = stepPrompt(words, question, results);
    let text;
    try {
      text = await once(prompt);
    } catch (first) {
      onEvent(`Step ${step} failed (${first.message}); trying it once more in a fresh session…`);
      try {
        text = await once(prompt);
      } catch (err) {
        if (!results.length) throw err;
        return stoppedResult(step, err, { toolCalls, results, lock, words });
      }
    }
    const reply = parseReply(text);
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

// The model failed the same step twice after tools ran: the page shows what they returned, with the reason.
async function stoppedResult(step, err, { toolCalls, results, lock, words }) {
  let facts = [];
  let notes = [];
  try {
    const v = await lock("", results, words);
    facts = (v && v.facts) || [];
    notes = (v && v.notes) || [];
  } catch { /* the reason alone */ }
  const why = `the on-device model stopped at step ${step}, twice (${err.message})`;
  return { answer: "", toolCalls, results, canned: true, stopped: why,
    lock: { ok: false, refused: [why], facts, notes } };
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
  const lead = result.stopped ? `No answer: ${esc(result.stopped)}` : `The model's wording was refused: ${esc(why)}`;
  return `${head}<p class="ask-refused">${lead}. What the tools returned:</p>` + facts + notes;
}

/** The same, as Markdown for Copy and Download. */
export function deviceAnswerMarkdown(question, result) {
  const lock = result.lock;
  const notes = lock && Array.isArray(lock.notes) && lock.notes.length ? `\n${lock.notes.join(" ")}\n` : "";
  if (!lock || lock.ok) return `# ${question}\n\n${result.answer}\n${notes}`;
  const why = (lock.refused || []).join("; ") || "it did not match the tool results";
  const facts = (lock.facts || []).map((f) => `- ${f}`).join("\n") || "No tool ran for this question.";
  const lead = result.stopped ? `No answer: ${result.stopped}` : `The model's wording was refused: ${why}`;
  return `# ${question}\n\n${lead}. What the tools returned:\n\n${facts}\n${notes}`;
}
