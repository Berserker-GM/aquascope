# The AI roles on the device (#590)

**Question.** With no key, do the Explorer's AI roles (Ask the map, Explain this view,
Scout, Review my model results, What if, the Ask panel and the Studio brief) give answers a
reader can trust when Chrome's built-in model writes them?

**Answer: mostly, where a claim lock exists.** The locks in `map_explain.claim_lock`,
`map_scout.check_wording` and `whatif_map.parse_scenario_reply` held: no number outside the
facts reached a pin, a note or a scenario. The Ask panel had no lock, and it is where the
worst answers came from: numbers from an earlier question, a trend never computed, gauge
ids swapped between sites. Seventeen defects were found; the table at the end says where
each one was fixed. A recheck on the device after those fixes, and the second round of fixes it
led to, follow it.

The other half of #590, the same roles with a real key (the reader's own model through
Ask's provider list), is **still to be run by the maintainer**. Nothing on this page covers it.

## How it was run

- Date: 2026-10-25.
- Browser: the maintainer's Chrome 155 on a Mac, window 865 x 447 CSS px.
- Model: Gemini Nano through Chrome's Prompt API (`LanguageModel.availability()` was
  "available"). No key stored.
- Explorer: the live build at <https://rekin226-aquascope-explorer.static.hf.space/>
  (repo `main` at 49b00c1).
- WebLLM: not tested. When the Prompt API is present `loadLocalModel` uses it and the UI
  offers no WebLLM choice.

Every request went through the page's own UI (the box, the buttons, the panels). To see
what the model was sent and what it replied, `LanguageModel.create` was wrapped in the page
to log each prompt, reply and time. Map moves between requests and "Undo all" were done
from the console. One What-if line was submitted with `requestSubmit()` because the panel's
input was clipped at this window height. Three extra Studio brief checks called the Prompt
API directly with the page's own system prompt and schema (marked below).

Times are from submit to the final line on screen; "model" is the Prompt API call alone.

## Ask the map

| Request | Engine | Reply | Time (model) | Numbers in the facts? |
|---|---|---|---|---|
| show floods ahead in Bangladesh | device | fly to Bangladesh, Floods ahead on | 19.8 s (1.3 s) | yes (no numbers) |
| fly to the Rhine and show river status | device | fly to Rhine (bbox of the river), status on | 2.7 s (1.0 s) | yes |
| take me to the Mekong delta and turn on groundwater | rules | fly to Mekong Delta, groundwater on | 0.2 s | yes |
| where is it driest in Africa right now? zoom there | device | fly to bbox [15, 20, 30, 40] the model made up; status, surface water and land cover on; 2 actions refused and said | 4.3 s (2.7 s) | no: the bbox is the model's own |
| what did the Indus look like during the big Pakistan floods? | device | Floods past on, fly to "Indus, Sindh" (a town) at zoom 8; date left at 2026-09-15 | 2.2 s (1.2 s) | yes, but the question (the 2022 floods) was not answered |

## Explain this view

| View | Engine | Notes | Time (model) | Numbers in the facts? |
|---|---|---|---|---|
| Bangladesh, zoom 4 | rules (device tried) | 3 rules notes. The device's one note was refused, but the line says "Rules, no model" | 5.0 s (1.2 s) | the lock caught 20 and 75/90 under the wrong fact |
| Europe, zoom 4 | device | 2 device notes and 1 rules; 3 refused (no place) | 8.1 s (5.9 s) | yes. Wording: "96% ... significantly below normal" (the fact is "below or much below"); values said twice |
| US mid-Atlantic, zoom 6.5 | device | 1 device note and 1 rules; 1 refused | 5.8 s (3.8 s) | the lock caught "59" (from another fact). A passing note reads "54% (54%) ... 41,000 km² (41,000 km²)" |
| Africa, zoom 3 | device | 2 device and 1 rules; 1 refused | 8.5 s (4.2 s) | yes. "6,000,000 km² km²", values repeated in brackets |
| Australia, zoom 4 | device | 3 device notes; 2 refused | 9.1 s (6.0 s) | yes. Each note ends "This is located at a point on the map." (copied from the prompt) |

## Scout

| View | Engine | Result | Time (model) | Numbers in the facts? |
|---|---|---|---|---|
| world, zoom 1.2 | device | 7 pins; 3 device wordings, 4 refused | 21.8 s (13.9 s) | yes |
| Europe, zoom 4 | device | 2 pins from 4 findings: the model mangled two ids ("2026-09-1" for "2026-09:1") and those findings were dropped | 17.9 s (8.0 s) | yes; one reason adds advice ("worth validating") |
| US, zoom 4 | rules (device tried) | 4 pins, all 4 wordings refused: each wrote "January 2026" or "September 2026" outside the slots | 13.8 s (6.5 s) | the lock refused correct years |
| South Asia, zoom 4 | rules (device tried) | 1 pin, wording refused (a literal "January 2026") | 8.8 s (2.2 s) | the lock refused a correct year |
| South America, zoom 3 | rules (device tried) | 1 pin, wording refused (a literal "September 2026") | 2.7 s (1.9 s) | the lock refused a correct year |

Pin counts are low partly because this window is short and Scout leaves out pins that would
sit under a bar.

## Review my model results

Sample: HEC-RAS 2D, Portsmouth, Virginia (6,272 cells, 109 steps). 9 of 9 checks ran each time.

| Request | Engine | Result | Time (model) | Numbers in the facts? |
|---|---|---|---|---|
| review my model results | device | 8 pins; 6 device wordings, 2 refused | 29.0 s (7.6 s) | yes. Meaning flipped: the rules say "worth a look if it is not a channel or a pit you expect", the device "investigate if it's expected for the area" |
| is anything wrong with my flood model? | device (Ask the map) | not routed to the review: the model turned Floods past on | 1.5 s (0.8 s) | n/a |
| check my model | device | 1 device wording, 7 refused (reasons not shown) | 7.5 s (7.1 s) | numbers yes, claim no: "8 cells ... (< 0.0269 m)"; the rules say 8 cells are under 0.03 m and 0.0269 m is one cell's maximum |
| review my model results (MODFLOW Freyberg sample now on screen in Texas) | device | reviewed the older HEC-RAS mesh, pins off screen in Virginia; the final line does not name the file | 31.3 s (11.2 s) | yes |
| legend "Review these results" | device | 8 pins, 1 refused | 8.1 s (7.4 s) | yes |

## What if

Reach: a stream east of Siegburg (reach 230428063, 1,379 km²). The Rhine at Cologne
(143,851 km²) offered "What if..." but could not run: it is above the 100,000 km² limit.

| Line | Engine | Read as | Time (model) | Numbers in the words? |
|---|---|---|---|---|
| a hotter and drier climate | device, refused | model said rain -10 %, +1 °C; both refused; the line suggests Chrome's model, which was just used | about 21.5 s, model called after 20.3 s (1.2 s) | the lock caught invented numbers |
| what if the town pumps 300 litres per second out of the river | device, refused | model said demand 0.3 m³/s (correct); refused | model called after 20.6 s (1.2 s) | false refusal: "litres per second" is not read as l/s |
| summers get much hotter, maybe three degrees | device, refused | model said +3 °C (correct); refused | model called after 0.4 s (0.8 s) | false refusal: "three" is not counted as a number |
| rain falls by a fifth and evaporation goes up 10 percent | rules | "20% less rain"; the evaporation clause dropped without a word | 33.8 s (GR4J calibration) | yes, but half the line ignored |
| drought: precipitation down by a quarter with 1.5 C of warming | device | "25% less rain, 1.5 °C warmer"; mean flow -47 % (-48 to -46 %) | 23.0 s, model called after 20.6 s (1.2 s) | yes |

The result numbers (flow change, KGE) are the code's; the model only fills the four parameters.

## The Ask panel on the device

Gauge: USGS 01646500, Potomac at Little Falls. "Tell it what I am looking at" on.

| Question | Engine | Reply (short) | Time (model steps) | Numbers in the tool results? |
|---|---|---|---|---|
| Summarise the record ... period, mean, trend, and the flood frequency | device + analyze_station | mean 320.7738 m3/s, 1930 to 2026, min 3.43, max 12100, "trend ... is increasing", flood frequency "from the flow-duration curve" | 30.4 s (1.2 s, 3.8 s) | numbers yes. The trend and the GEV never reached the model: the payload was cut at 3,000 characters, inside a series |
| What is the 100-year flood at this gauge? | device, no tool call | "The 100-year flood (Q10) ... not directly available ... record from 1930-03-01" | 2.2 s (2.1 s) | no: Q10 and 1930-03-01 come from the previous question's tool result, still in the session; Q10 is not the 100-year flood |
| Find the five gauges nearest to Kingston upon Thames | device + find_stations | failed at step 2: "kErrorUnknown" | 2.9 s | n/a; the model passed near = [51.1, 0.0], about 35 km from Kingston |
| What is the climate and modelled discharge at 25.05, 121.55? | device + anywhere | 1733.4111 mm, 22.7201 °C, aridity 1.4838 (humid), GloFAS mean 5.6336 m3/s 2006 to 2026, "annual" min 1.35 and max 214.28 | 31.4 s (22.8 s, 4.4 s) | numbers yes; the min and max are daily, not annual |
| Is the Potomac at Little Falls getting drier? Use the annual-mean trend. | device, no tool call | "an increasing trend ... Mann-Kendall ... indicates an upward trend" | 1.6 s (1.4 s) | no trend result was ever seen. The recorded key answer gives Sen's slope +0.059 m³/s per year, p = 0.82: no trend |
| (retry) Find the gauges nearest to Kingston upon Thames | device + find_stations | five Kingston gauges with ids | 6.0 s (1.0 s, 4.5 s) | ids in the payload but swapped between sites; "nearest" is not what the tool returned |

## The Studio brief on the device

| Sentence | Engine | Brief read | Time | Numbers in the sentence? |
|---|---|---|---|---|
| I need the design flood for a footbridge here, something like the 50-year peak, using data since 1980 | device | return_period 50, "Design flood calculation"; the Consultant: 2 known, 0 to ask | 0.8 s | yes ("since 1980" not captured) |
| Will the road by the pump station flood this winter? | device | return_period 1 (not in the sentence; dropped by the 2 to 100,000 range), quantities ["this winter"] | 0.7 s | no, caught by the range only |
| Is this site safe from a big flood for a new school? (direct call, same prompt) | device | return_period 0 (dropped) | 0.7 s | no, caught by the range only |
| How low does the river get in a dry summer? We plan a water intake. (direct call) | device | return_period 0 (dropped) | 0.8 s | no, caught by the range only |
| Has the river been getting more extreme since the dam was built? (direct call) | device | return_period 0 (dropped), quantities ["none"] kept | 0.7 s | no, caught by the range only |

The on-device plan (at review) and prose (after the run) were not reached in this session.

## What got past the locks

1. **The Ask panel had no lock.** Numbers from a previous question ("Q10", "1930-03-01"),
   a trend direction never computed, gauge ids swapped between sites, invented search
   coordinates.
2. **Right numbers, wrong claim.** The review note "8 cells ... (< 0.0269 m)" and the
   Explain note "96% ... significantly below normal". Each number is in the cited facts,
   but they are put together wrongly. A presence check cannot catch this.
3. **Ask the map: a bounding box the model made up** for "where is it driest in Africa",
   applied as the answer.
4. **Studio brief: no check that a return period or timescale is in the sentence;** only
   the range check stopped the invented 1 and 0.

Console: no errors from the AI roles; two MapLibre missing-sprite warnings.

## The defects and where they were fixed

Two pull requests fix them: **A** is #639 on `fix/ondevice-ask-590` (the Ask panel, Ask the map,
the sampling and the Studio brief), **B** is #640 on `fix/ondevice-roles-590` (Scout, Explain, What
if and the review). Neither was checked on a real on-device model after the
fix: headless Chrome has none, so each fix is covered by tests that use the recorded model
replies above.

| # | Where | Defect | Fixed |
|---|---|---|---|
| 1 | `explorer/src/local-model.js` `loadLocalModel`, `askLocally` | one Prompt API session served every question, so earlier tool results answered later questions | A: one base session, never prompted; each question gets a clone of it (or a new session) and destroys it after |
| 2 | `local-model.js` `askLocally` | the tool result was cut at 3,000 characters, so the trend and flood frequency never reached the model | A: `aquascope.ai_engine.device_ask.compact_result` keeps the record, daily statistics, FDC points, return levels with their interval and the trend with its reading in words, and drops series and citations |
| 3 | `explorer/src/ask.js` `runLocally`, `local-model.js` `localAnswerHtml` | no claim lock on the on-device answer | A: `device_ask.lock_answer` holds every number, date, Q label and gauge id to this question's results (rounding allowed), checks that an id sits next to its own gauge's name and that trend words agree with the Mann-Kendall result; a refused answer is replaced by the tools' facts and one line saying why |
| 4 | `aquascope/map_scout.py` `apply_wording` | findings the model left out of its order were dropped | B: they follow in the rules' order up to `max_pins`, and an id written with other punctuation ("2026-09-1" for "2026-09:1") still finds its finding when only one reads that way |
| 5 | `map_scout.py` `check_wording` | a correct year written out ("September 2026") was refused | B: `slots_back` puts a slot's exact value back into its `{slot}` before the checks; another month or year is still refused, and so is a sign against the written value |
| 6 | `explorer/src/map-explain.js` `explainView` | when every device note was refused, the line said "Rules, no model" | B: the line says the model's wording was refused and lists the refusals (`map-actions-core.js` `explainWho`) |
| 7 | `aquascope/map_explain.py` | values said twice, prompt text copied into notes | B: `drop_repeats` writes a value once ("54% (54%)", "km² km²"; Scout and the review fill through it too); the prompt no longer offers "a point on the map", and a sentence that only copies the prompt is dropped |
| 8 | `aquascope/whatif_map.py` | "litres per second" and number words not read | B: litres or liters per second, l/s, L/s, cubic metres per second and number words are read ("one" only before a unit); Nano's 0.3 m³/s and +3 °C pass, and the digit in "m3/s" no longer counts as a number said |
| 9 | `explorer/src/whatif-map.js` `readLine` | the device's refusal not shown; the hint suggests the model just used | B: the line names the model and its reasons, and the hint names only a way not yet tried (`whatif-core.js` `notReadLine`) |
| 10 | `whatif-map.js`, `whatif_map.parse_scenario` | a partial rules match dropped a clause in silence | B: the clause in the run was read by the rules but dropped by the sliders (evaporation has none); it now goes with the run and is said. When the rules read only part of a line and no model reads it, the line names the words not read and nothing runs |
| 11 | `whatif-map.js` `readLine` | about 20 s before the device is called | B, in part: the rules' reading and the device prompt are one worker call, and a quick call goes to the main worker when every light worker is busy reading the network and the main worker is idle. Headless with a stub, the one light worker held by a slow host: 20.6 s before, 4 ms after. With the main worker busy as well the wait remains, and if the live 20 s was Chrome reloading Nano, this does not help; neither could be told apart without the device |
| 12 | `aquascope/map_commands.py` | "is anything wrong with my flood model?" did not reach the review | A: the review and explain phrases are wider, and a model may answer with `{"control": "review"}` or `{"control": "explain"}` |
| 13 | `explorer/src/map-command.js` `byDevice`, `map_commands` reply check | a bbox the model made up was applied as the answer | A: `map_commands.ground_places` keeps a box or point only when the words hold its numbers; otherwise the place the model named, the extent of a region the words name ("Africa"), or the model's label as a place the words say; failing those, refused with "name a place or a region" |
| 14 | `local-model.js` `promptOptions` | `LanguageModel.params` is undefined in Chrome 155, so the 0.1 temperature was never set | A: feature-detected. An extension (with `params()`) gets `topK` and `temperature`; a web page gets `samplingMode`, which only the sampling origin trial honours (checked against the Prompt API docs on 2026-10-25), else Chrome's own sampling; a Chrome that refuses the option gets a session without it |
| 15 | `explorer/src/intake.js` `parseBriefReply` | a return period not in the sentence was kept when in range | A: a return period or timescale is kept only when the sentence states it, in digits or words ("50-year", "hundred-year", "twelve months") |
| 16 | `explorer/src/mesh-review.js` `reviewModel` | the review did not name its file, and reviewed an older mesh off screen | B: from Ask the map the review is of the model on screen; a MODFLOW model there, or the mesh out of view, is said instead (`mesh-review-core.js` `reviewTarget`). The legend row and WebMCP still review the loaded mesh, and the final line names the file |
| 17 | `explorer/src/map-card.js` | "What if..." offered on reaches above the 100,000 km² limit | B, in the What if panel rather than the card: it checks the basin as it opens (`whatif_map._basin_check`, main worker) and says the limit with Run off. The Rhine at Cologne, headless: 143,881 km², said after 16 s. The card still offers the button |

"Right numbers, wrong claim" (escape 2), fixed in B for the two cases seen, by checks that look
past the presence of a number:

- Explain "96% ... significantly below normal": `map_explain.class_claims` refuses a claim of the
  stronger class ("much", "significantly", "well below normal") unless a cited fact is of that
  class, and a side of normal no cited fact is on. It reads a note as a whole, so a note citing
  both the share and a much-below area would pass.
- Review "8 cells ... (< 0.0269 m)": the film check's threshold is a fact of its own ("A film is
  shallower than", 0.03 m) and the count names it; a sentence that puts the count under another
  value is refused. Only the film check's count carries a bound so far.

Other ways to put right numbers together wrongly are not caught. The real-key run of #590 is
still to be done by the maintainer.

## Recheck after #639 and #640

Date: 2026-10-26.
Browser: the maintainer's Chrome 155 on a Mac, window 865 x 447 CSS px, a new tab, hard-reloaded.
Model: Gemini Nano through the Prompt API (`LanguageModel.availability()` = "available"). No key stored (Ask's "forget key" control hidden); no key read or entered.
Explorer: the live build at rekin226-aquascope-explorer.static.hf.space, asset version `c406699`, which loads `src/ask-local-core.js`.

How it was run. As in the first run: every request through the page's own UI or its own entry points (`__aq.mapAsk.run`, `__aq.mapExplain.run`, `__aq.scout.run`, the What-if form), with `LanguageModel.create` wrapped to log prompts, replies and times. Map moves were done from the console. Before the Scout runs the selected gauge was cleared from the console (see Scout). Marked "direct" below: Prompt API calls made from the console with the page's own system prompt and schema, and answers sent to the page's own lock in the worker (`device_ask`, op `lock`).

Times are from submit to the final line; "create" is `LanguageModel.create`, "model" is the prompt call.

### Before and after

| Baseline defect | Now |
|---|---|
| Ask: one session for every question, earlier results answer later questions | Gone. Each question gets a clone, destroyed after. "And what is its 50-year flood?" called the tool itself |
| Ask: tool payload cut at 3,000 characters, trend and GEV never seen | Gone. The step-2 prompt is 1,693 characters with stats, return levels and both trends |
| Ask: no lock | Lock in place. Replayed baseline answers are refused: "Q10 ... 1930-03-01" with no tool run (date and Q10 refused), "an increasing trend" (trend wording refused) |
| Ask: "kErrorUnknown" once | Worse: 7 of 12 UI runs stopped at step 2 with "kErrorUnknown" (see Ask) |
| Ask the map: model's own bbox applied for "driest in Africa" | Gone. "refused the model's own box, replaced by the extent of Africa" |
| Ask the map: "is anything wrong with my flood model?" not routed to the review | Gone. The review ran |
| Explain: "Rules, no model" when every device note was refused | Gone. The line names the model and gives each refusal's reason |
| Explain: "54% (54%)", "km² km²", "This is located at a point on the map" | Not seen. New copies: "is pinned, unnamed", "on on Sat 7 Nov" |
| Scout: findings with mangled ids dropped | Gone. Europe: 3 findings, 3 pins, though Nano again wrote "2026-09-1" and "2026-01-275-407" |
| Scout: written-out years refused | Gone. "September 2026" and "January 2026" pass |
| What-if: "300 litres per second" and "three degrees" refused | Gone. Read as 0.3 m³/s and +3 °C |
| What-if: refusal not shown, hint suggests Chrome's model | Gone. "Chrome's built-in model: refused dp_pct 10: that number is not in the words" |
| What-if: evaporation clause dropped | Gone. Rules read "20% less rain, 10% more evaporation" |
| What-if: about 20 s before the device call | The wait before the call is now 3 to 62 ms, but `LanguageModel.create` itself took 20.6 and 21.1 s in 2 of 4 device reads |
| What-if: Rhine at Cologne offered a run it could not do | Gone. The panel says "143,881 km2 drain to this reach ... the limit here is 100,000 km2" and Run is disabled |
| Review: MODFLOW on screen, older HEC-RAS mesh reviewed off screen | Gone. The line says the MODFLOW file is on screen and not covered, and names the loaded mesh that is out of view |
| Review: "8 cells ... (< 0.0269 m)" | Not seen |
| Review: meaning flipped ("investigate if it's an expected feature") | Still there, on 5 pins |
| Temperature 0.1 never set | samplingMode "most-predictable" is passed and `create` does not throw, but the session reports no `samplingMode`, so the page says "Chrome's default sampling" (samplingNote). It does not claim a setting it cannot see |

### Ask panel

Gauge USGS 01646500 selected, "Tell it what I am looking at" on.

| Question | Result | Steps (model) | Lock |
|---|---|---|---|
| Summarise the record at this gauge: period, mean, trend, and the flood frequency (4 runs) | 4 of 4 "The on-device model could not run: ... kErrorUnknown" after analyze_station | 0.9 to 21.1 s, then error in 0.8 s | not reached |
| What is the 100-year flood at this gauge? (2 runs) | 1 error; 1 answer: 10795.57 m3/s | 0.93 s, 2.6 s; total 9.3 s | passed. The value is the LP3 100-year; the GEV is 11247.39 and the method is not named |
| Is the Potomac at Little Falls getting drier? Use the annual-mean trend. (2 runs) | 2 of 2 kErrorUnknown | 1.3 and 21.9 s, then error | not reached |
| Find the five gauges nearest to Kingston upon Thames | analysed one gauge (Kingston, 8496ce69-..., id right) instead of listing five | 21.7, 1.5, 3.7 s; total 29.7 s | passed |
| What is the climate and modelled discharge at 25.05, 121.55? | 5.63 m3/s, 22.72 °C, 1733.41 mm; min and max no longer called annual | 0.86, 2.95 s; total 8.1 s (was 31.4 s) | passed |
| New: compare the mean flow of the Potomac (USGS-01646500) with the Thames at Kingston | means, periods and maxima right; "the Potomac's ... q95 of 3.43 m3/s" is wrong (3.43 is its daily minimum; its Q95 is 35.7) | 0.96, 1.7, 5.7 s; total 14.6 s | passed: escape |
| New: And what is its 50-year flood? | 9150.06 m3/s with its 90 % interval, from a fresh tool call | 0.92, 1.3, 2.3 s | passed |

Claim-lock pass rate. UI: 5 answers reached the lock, 5 passed. Direct (page's prompt and compact result as a single first prompt, then the page's lock): 9 answers, 9 passed. Of these 14 passing answers, 2 show a wrong number as fact: the q95 above, and "the return period for a flood of magnitude 2 m3/s is 2 years, and ... 10 m3/s is 25 years" (direct). The trend answers were right in 3 of 3 direct runs ("no significant trend ... Sen's slope -0.0365 m3/s per year").

The kErrorUnknown failure, from direct trials on the same prompts:
- a second prompt in one session, after a first prompt with `responseConstraint`, failed in 11 of 13 trials, with and without `samplingMode` and on clones and fresh sessions alike;
- with no constraint on the first prompt, 2 of 2 passed;
- the same step-2 text as the only prompt of a fresh clone passed 4 of 4.

Per-step time with fresh sessions: step 1 took 0.86 to 1.25 s in 9 of 12 runs and 21.1 to 21.9 s in 3; later steps took 1.3 to 5.7 s. The first question also waited 16.5 s for the base session.

### Ask the map

| Request | Engine | Result | Time (create, model) |
|---|---|---|---|
| where is it driest in Africa right now? zoom there | device | bbox refused and said, Africa's extent used; it also started an unasked playback, September to October 2026 by month. "Driest" not answered | 23.7 s (20.9 s, 2.7 s) |
| is anything wrong with my flood model? (HEC-RAS Portsmouth on screen) | rules, then device wording | the review ran: 8 pins, final line names Flood_model.p01_BC12_S6_R6.hdf, 1 wording refused | 32.8 s (20.8 s, 9.2 s) |
| New: does this simulation look plausible to you? | device | `{"actions": []}`, "Not understood"; not routed to the review | 1.8 s (1.2 s, 0.4 s) |
| New: tell me in plain words what this map is showing me | device | flew to the selected gauge and turned river status on; not routed to Explain | 3.2 s (0.8 s, 1.2 s) |
| (review) are the depths in my flood model realistic? | device | flew to and lit up the Nile, the example in the system prompt; 2 actions applied | 10.3 s (0.7 s, 1.1 s) |

### Explain

| View | Result | Time (create, model) | Passing device notes |
|---|---|---|---|
| Bangladesh, zoom 4 (run 1) | 2 device + 1 rules; 3 refused, reasons on the line | 13.1 s (1.2 s, 9.5 s) | readable; one gives the largest area's 20 % as "20% of the mapped land is below normal" (27 % is below or much below) |
| Bangladesh, zoom 4 (run 2) | 1 device + 2 rules; 4 refused | 5.6 s (0.8 s, 4.7 s) | escape: "The river is mapped at 21% above normal". The 21 % is the share of the view covered by the largest above-normal area, not a flow |
| Europe, zoom 4 | 1 device + 2 rules; 0 refused | 24.9 s (21.1 s, 1.8 s) | right: "92% of the view ... much below normal ... 1,400,000 km²" |
| New: Australia, zoom 4 | 1 device + 2 rules; 3 refused (90, 10/25, 2.0 not in cited facts) | 10.3 s (1.0 s, 5.8 s) | right (news counts) |
| New: Africa, zoom 3 | 4 device; 1 refused | 12.4 s (1.1 s, 7.6 s) | escapes: "flow at least 81% below normal" (81 % is the land below or much below normal), "flow above normal at 6%" (6 % of land). Also "is pinned, unnamed" copied from the prompt and "on on Sat 7 Nov" |

Refusal reasons list "²" as a number when a cited fact has no km² ("(760000, ²)").

### Scout

| View | Result | Time (create, model) |
|---|---|---|
| Europe, zoom 4, gauge USGS 01646500 still selected | 3 of 3 pins, all in rules wording: Nano ordered only "USGS-01646500", from the context line, which names the selected gauge though it is off screen. The line still says "worded on this device" and reports no refusal | 45.8 s (20.8 s, 1.9 s) |
| Europe, zoom 4, selection cleared (2 runs) | 3 of 3 pins each time; 3 device wordings, then 2 device + 1 refused. One passing reason reverses the finding: "poor agreement with a gauge's water flow, raising questions about the gauge's measurement" (the rules say the models miss this river) | 22.3 s (0.3 s, 5.2 s); 20.7 s (0.3 s, 5.0 s) |
| South America, zoom 3 | 1 pin, device wording passed ("September 2026" written out) | 3.3 s (0.5 s, 1.8 s) |
| New: US, zoom 4 | 4 pins, 4 wordings refused. Right refusals: Nano wrote a slot that does not exist, `{year}` | 25.5 s (0.3 s, 6.1 s) |
| New: South Asia, zoom 4 | 2 pins, 2 device wordings; both add interpretation ("suggesting substantial water flow") | 21.2 s (0.3 s, 3.8 s) |

No number outside the slots reached a pin. The line still gives a count of refusals, not reasons.

### What if

Reach 230428063, east of Siegburg (1,379 km², validation KGE 0.65, fair, 17 of 24 parameter sets kept).

| Line | Read as | Wait before device call | Create, model | Total |
|---|---|---|---|---|
| what if the town pumps 300 litres per second out of the river | device: 0.3 m³/s taken; mean flow −1 % | 62 ms | 0.6 s, 0.8 s | 96.7 s (95 s cold GR4J calibration) |
| summers get much hotter, maybe three degrees | device: 3 °C warmer, applied to the whole year without saying so; mean flow −6 % | 19 ms | 20.6 s, 1.2 s | 27.1 s |
| rain falls by a fifth and evaporation goes up 10 percent | rules: 20 % less rain, 10 % more evaporation; mean flow −41 % | no device call | | 5.4 s |
| Rhine at Cologne, reach 230515098 | panel says the 100,000 km² limit, Run disabled | | | |
| New: a much wetter future | device said rain +10 %; refused and said, with the model's name | 3 ms | 21.1 s, 1.1 s | 22.4 s |
| New: what if the factory takes twenty litres a second | device: 0.02 m³/s (right), but the status line and the map log say "0 m³/s taken" | 6 ms | 0.4 s, 0.8 s | 2.5 s |

### Review my model results

| Request | Result | Time (create, model) |
|---|---|---|
| review my model results (MODFLOW Freyberg on screen in Texas, HEC-RAS mesh loaded in Virginia) | "freyberg.hds (MODFLOW heads) is the model on screen: the review reads HEC-RAS 2D and UGRID meshes ... Flood_model.p01_BC12_S6_R6.hdf is loaded but not in view" | 0.4 s, no model call |
| is anything wrong with my flood model? (mesh on screen) | 8 pins, 7 device wordings, 1 refused ("Two cells exhibit a wet/dry cycle 5 times"). The 5 deepest-water pins say "investigate if it's an expected feature"; the rules say worth a look if it is not | 32.8 s (20.8 s, 9.2 s) |
| New: check my model (mesh on screen) | 8 pins, 8 device wordings, 0 refused; "check if expected (e.g. channel or pit)"; Nano put the 8.97 m pin before the 17.1 m one under "most severe first" | 29.8 s (21.1 s, 8.5 s) |

### Session start time

Across the 21 calls the page made for Ask the map, Explain, Scout, What-if and the review, `LanguageModel.create` took 20.6 to 21.1 s on 7 and 0.28 to 1.2 s on 14. This is now where the "20 s wait" sits. In Ask, the first prompt on a clone stalled the same way in 3 of 12 runs.

### Console

No errors from the AI roles. Two MapLibre exceptions, "Cannot read properties of undefined (reading 'key')", at one moment during the session.

### Remaining defects

Blocking for 1.0 (a claim-lock escape, or a wrong number shown as fact):

1. Explain: a share of land written as a flow ("mapped at 21% above normal", "flow at least 81% below normal", "flow above normal at 6%") passes. `aquascope/map_explain.py` `class_claims` / `check_model_notes`: refuse a "N% above/below normal" phrase when the cited fact is a share of the view, or fill that fact as "N% of the mapped land in view" and refuse literal values.
2. Ask: right number, wrong label passes ("the Potomac's q95 of 3.43 m3/s"; "a flood of magnitude 2 m3/s ... 2 years"). `aquascope/ai_engine/device_ask.py` `lock_answer`: tie a Q label to that gauge's flow-duration value, and a return period to its own return level.
3. What-if: "0 m³/s taken" for a 0.02 m³/s run, in the status line and the map log. `aquascope/whatif_map.py` `_g` (used by `scenario_label`) and `explorer/src/whatif-core.js` `g`: keep significant figures for small values.

Not blocking:

4. Ask: "kErrorUnknown" on step 2 in 7 of 12 runs, so summary and trend questions do not answer. `explorer/src/ask-local-core.js` `askLoop`: run each step in a fresh clone (the step prompt already restates the question; carry all results so far), or retry a failed step once in a fresh clone.
5. Session start of about 21 s in a third of calls. `explorer/src/local-model.js` `generateJsonLocally` creates a session per call. A warm base session per role might help, but Ask's clones also stalled, so this is not shown to work.
6. Review: the meaning flip persists ("investigate if it's an expected feature"). The wording check that `explorer/src/mesh-review.js` `wordWithModel` calls looks at numbers only; the package function was not opened in this recheck.
7. Scout: a reason that reverses the finding passes ("questions about the gauge's measurement"). `aquascope/map_scout.py` `check_wording` checks numbers and slots only.
8. Scout: the line says "worded on this device" when no device wording was used, and gives counts, not reasons. `explorer/src/scout.js` `runScout`.
9. Context: the selected gauge is named in the context line when it is off screen, and Nano answers about it (Scout in Europe, Ask the map). The page's `currentContext()`.
10. Ask the map: actions on a place the words do not name (the Nile, from the prompt's example); review and Explain requests in other words do not reach those controls. `aquascope/map_commands.py` reply check, `explorer/src/map-command.js` `byDevice`: refuse a place that is not in the words, as #639 does for boxes.
11. Explain: prompt text copied ("is pinned, unnamed"), "on on Sat 7 Nov", and "²" listed as a number in refusal reasons. `aquascope/map_explain.py` `notes_prompt`, `drop_repeats`, `claim_lock`.
12. What-if: "summers ... three degrees" runs as a year-round warming without saying so. `explorer/src/whatif-map.js` `readLine` (`heldWords`).
13. Ask: "five gauges nearest to Kingston" analysed one gauge; the 100-year answer gives the LP3 value without naming it while the page's facts use GEV. `aquascope/ai_engine/device_ask.py` prompt and facts.

### Round 2 fixes

Two more pull requests take the remaining defects: **C** is this one, on `fix/ondevice-ask-labels-590`
(the Ask panel, Ask the map, the context line, the device sessions), **D** is #641 on
`fix/ondevice-roles-round2-590` (Explain, Scout, What if, the review). Each was tested with the
recorded replies above as fixtures, in pytest and node, and C also in headless Chrome with a stubbed
`LanguageModel`; neither was rerun on the device.

| # | Defect | Fixed in |
|---|---|---|
| 1 | Explain: a share of land written as a flow | D |
| 2 | Ask: right number, wrong label ("q95 of 3.43", "2 m3/s ... 2 years") | C: `device_ask.lock_answer` ties each labelled number to its own value for the gauge its clause is about: a Q label to that gauge's flow-duration point, an N-year flood to its return level for N, a mean, minimum, maximum or record dates to their own fields. A number written in m3/s must be a flow, not a return period. The recorded comparison is refused on its Q95 alone; with the Potomac's Q95 it passes. The page adds the catalogue's name and river to an analysis, so the lock can tell two gauges apart |
| 3 | What if: "0 m³/s taken" for 0.02 m³/s | D |
| 4 | Ask: "kErrorUnknown" at step 2 | C: `ask-local-core.js` `askLoop` runs each step as the only prompt of a fresh clone, carrying the question and every tool result so far, and tries a failed step once more in another. A step that fails twice after tools ran shows what they returned, with the reason. A stub that fails a session's second prompt, as Chrome 155 did, now reaches the answer |
| 5 | About 21 s session starts | C, not shown to help: `generateJsonLocally` clones a warm base session kept per system prompt (`ask-local-core.js` `sessionPool`, at most four), and Ask the map sends its context with the words, so its system prompt and warm base stay the same. Tested with a stub for correctness only (one create, then clones); whether a clone avoids the 21 s needs the device, and Ask's clones also stalled |
| 6 | Review: the meaning flip | D |
| 7 | Scout: a reason that reverses the finding | D |
| 8 | Scout: "worded on this device" with no device wording | D |
| 9 | Context: the selected gauge named when off screen | C: `currentContext` leaves an off-screen gauge out for the map's roles and says it is "selected earlier and now off screen" for Ask, where "this gauge" still means it |
| 10 | Ask the map: a place the words do not name; review and Explain in other words | C: `map_commands.ground_places` refuses a place the words do not name ("Nile, a place the words do not name"); the prompt's examples say `<river>`, `<place>` and `<region>` instead of the Nile, the Rhine and South Asia; "realistic", "plausible to you", "are the depths right" reach the review and "what this map is showing me" the notes on the view, by the rules, with no model |
| 11 | Explain: prompt text copied, "on on", "²" as a number | D |
| 12 | What if: "summers" run as a whole year | D |
| 13 | Ask: five gauges asked, one analysed; the 100-year flood without its method | C: a question that asks for several gauges is refused when the answer names fewer than the search found, and the page shows the search's list; the device prompt asks for the list. The compact result says which return level is GEV (the page's figures) and which LP3, and the lock refuses an LP3 value given without saying LP3 |
