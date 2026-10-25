# The AI roles on the device (#590)

**Question.** With no key, do the Explorer's AI roles (Ask the map, Explain this view,
Scout, Review my model results, What if, the Ask panel and the Studio brief) give answers a
reader can trust when Chrome's built-in model writes them?

**Answer: mostly, where a claim lock exists.** The locks in `map_explain.claim_lock`,
`map_scout.check_wording` and `whatif_map.parse_scenario_reply` held: no number outside the
facts reached a pin, a note or a scenario. The Ask panel had no lock, and it is where the
worst answers came from: numbers from an earlier question, a trend never computed, gauge
ids swapped between sites. Seventeen defects were found; the table at the end says where
each one was fixed.

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

Two pull requests fix them: **A** is `fix/ondevice-ask-590` (the Ask panel, Ask the map,
the sampling and the Studio brief), **B** is `fix/ondevice-roles-590` (Scout, Explain, What
if, the review and the map card). Neither was checked on a real on-device model after the
fix: headless Chrome has none, so each fix is covered by tests that use the recorded model
replies above.

| # | Where | Defect | Fixed |
|---|---|---|---|
| 1 | `explorer/src/local-model.js` `loadLocalModel`, `askLocally` | one Prompt API session served every question, so earlier tool results answered later questions | A: one base session, never prompted; each question gets a clone of it (or a new session) and destroys it after |
| 2 | `local-model.js` `askLocally` | the tool result was cut at 3,000 characters, so the trend and flood frequency never reached the model | A: `aquascope.ai_engine.device_ask.compact_result` keeps the record, daily statistics, FDC points, return levels with their interval and the trend with its reading in words, and drops series and citations |
| 3 | `explorer/src/ask.js` `runLocally`, `local-model.js` `localAnswerHtml` | no claim lock on the on-device answer | A: `device_ask.lock_answer` holds every number, date, Q label and gauge id to this question's results (rounding allowed), checks that an id sits next to its own gauge's name and that trend words agree with the Mann-Kendall result; a refused answer is replaced by the tools' facts and one line saying why |
| 4 | `aquascope/map_scout.py` `apply_wording` | findings the model left out of its order were dropped | B |
| 5 | `map_scout.py` `check_wording` | a correct year written out ("September 2026") was refused | B |
| 6 | `explorer/src/map-explain.js` `explainView` | when every device note was refused, the line said "Rules, no model" | B |
| 7 | `aquascope/map_explain.py` | values said twice, prompt text copied into notes | B |
| 8 | `aquascope/whatif_map.py` | "litres per second" and number words not read | B |
| 9 | `explorer/src/whatif-map.js` `readLine` | the device's refusal not shown; the hint suggests the model just used | B |
| 10 | `whatif-map.js`, `whatif_map.parse_scenario` | a partial rules match dropped a clause in silence | B |
| 11 | `whatif-map.js` `readLine` | about 20 s before the device is called | B |
| 12 | `aquascope/map_commands.py` | "is anything wrong with my flood model?" did not reach the review | A: the review and explain phrases are wider, and a model may answer with `{"control": "review"}` or `{"control": "explain"}` |
| 13 | `explorer/src/map-command.js` `byDevice`, `map_commands` reply check | a bbox the model made up was applied as the answer | A: `map_commands.ground_places` keeps a box or point only when the words hold its numbers; otherwise the place the model named, the extent of a region the words name ("Africa"), or the model's label as a place the words say; failing those, refused with "name a place or a region" |
| 14 | `local-model.js` `promptOptions` | `LanguageModel.params` is undefined in Chrome 155, so the 0.1 temperature was never set | A: feature-detected. An extension (with `params()`) gets `topK` and `temperature`; a web page gets `samplingMode`, which only the sampling origin trial honours (checked against the Prompt API docs on 2026-10-25), else Chrome's own sampling; a Chrome that refuses the option gets a session without it |
| 15 | `explorer/src/intake.js` `parseBriefReply` | a return period not in the sentence was kept when in range | A: a return period or timescale is kept only when the sentence states it, in digits or words ("50-year", "hundred-year", "twelve months") |
| 16 | `explorer/src/mesh-review.js` `reviewModel` | the review did not name its file, and reviewed an older mesh off screen | B |
| 17 | `explorer/src/map-card.js` | "What if..." offered on reaches above the 100,000 km² limit | B |

Not fixed by either: "right numbers, wrong claim" (escape 2) is not one of the seventeen,
and a presence check cannot catch it. The real-key run of #590 is still to be done by the
maintainer.
