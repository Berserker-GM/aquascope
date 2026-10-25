"""On-device Ask (#590): the compact tool result a small model is shown, and the lock on its answer.

The replies quoted here are the ones Gemini Nano wrote in Chrome 155 on 2026-10-25 (docs/assessments/
ai-on-the-map.md); the results they are held to are fixtures shaped like the tools' real payloads.
"""

from __future__ import annotations

import json

import numpy as np
import pandas as pd
import pytest

from aquascope.ai_engine.device_ask import MAX_CHARS, compact_result, facts, lock_answer
from aquascope.explore import analyze_series

POTOMAC_WORDS = "Summarise the record at this gauge: period, mean, trend, and the flood frequency."


def _potomac_payload() -> dict:
    """An analyze_station payload as the MCP face returns it, with the Potomac's recorded figures."""
    rng = np.random.default_rng(1)
    idx = pd.date_range("1990-01-01", "2020-12-31", freq="D")
    res = analyze_series(pd.Series(np.exp(rng.normal(5, 1, len(idx))), index=idx), "discharge", "m3/s")
    res.pop("series", None)
    res["fdc"] = {k: res["fdc"][k] for k in ("q95", "q50", "q10")}
    res.update(source="usgs", station_id="01646500", start="1930-03-01", end="2026-10-24",
               stats={"mean": 320.7738, "median": 182.0, "min": 3.43, "max": 12100.0})
    res["trend"] = {"on": "annual mean", "p_value": 0.82, "tau": 0.016, "trend": "no trend",
                    "sens_slope_per_year": 0.059, "n_years": 96}
    return res


def _result(name: str, payload: dict, arguments: dict | None = None) -> dict:
    return {"name": name, "arguments": arguments or {}, "compact": compact_result(name, payload), "ok": True}


# ── the compact result ─────────────────────────────────────────────────────────


def test_the_compact_result_keeps_the_trend_and_floods_the_3000_character_cut_lost() -> None:
    payload = _potomac_payload()
    full = json.dumps(payload, default=str)
    assert "p_value" not in full[:3000], "the fixture reproduces the cut: the trend lies past 3,000 characters"
    c = compact_result("analyze_station", payload)
    text = json.dumps(c)
    assert len(text) <= MAX_CHARS
    assert c["trend_annual_mean"]["p_value"] == 0.82 and c["trend_annual_mean"]["significant"] is False
    assert "no significant trend" in c["trend_annual_mean"]["reading"] and "+0.059" in c["trend_annual_mean"]["reading"]
    assert {r["T_years"] for r in c["flood_frequency"]["return_levels"]} >= {2, 10, 100}
    assert set(c["flow_duration"]) >= {"q95", "q50", "q10"}
    assert c["daily_values"]["max"] == 12100.0          # the key says these are daily values, not annual ones
    assert "annual_max" not in c and "methods" not in c  # the series and the citations stay out


def test_find_stations_and_anywhere_compact_to_what_an_answer_needs() -> None:
    stations = {"n_catalog": 60000, "n_returned": 12, "limit": 12, "stations": [
        {"source": "uk_ea", "station_id": f"E{i:05d}A", "name": f"SITE {i}", "latitude": 51.4, "longitude": -0.3,
         "license": "OGL", "url": "https://x", "variables": ["discharge"]} for i in range(12)]}
    c = compact_result("find_stations", stations)
    assert len(c["stations"]) == 10 and "license" not in c["stations"][0]
    here = {"latitude": 25.05, "longitude": 121.55, "climate": {
        "precipitation_mm_per_year": 1733.4111, "temperature_mean_c": 22.7201, "aridity_index": 1.4838,
        "aridity_class": "humid", "monthly_precipitation_mm": list(range(12)),
        "annual_precipitation": {"year": list(range(2006, 2026)), "mm": list(range(20))}},
        "glofas": {"unit": "m3/s", "start": "2006-01-01", "end": "2026-10-24",
                   "stats": {"mean": 5.6336, "min": 1.35, "max": 214.28}, "modelled": True}}
    c = compact_result("anywhere", here)
    assert "monthly_precipitation_mm" not in c["climate"]
    assert c["glofas"]["daily_values"] == {"mean": 5.6336, "min": 1.35, "max": 214.28}
    assert any("1733" in line or "1,733" in line for line in facts("anywhere", c))


def test_a_huge_unknown_result_is_shrunk_never_cut_mid_value() -> None:
    payload = {"rows": [{"id": i, "note": "x" * 300, "values": list(range(50))} for i in range(200)]}
    c = compact_result("describe_catchment", payload)
    assert len(json.dumps(c)) <= MAX_CHARS
    assert isinstance(c, dict)


# ── the lock: recorded device answers ─────────────────────────────────────────


def test_the_recorded_increasing_trend_claim_is_refused_against_p_082() -> None:
    res = [_result("analyze_station", _potomac_payload(), {"source": "usgs", "station_id": "01646500"})]
    answer = ("The Potomac at Little Falls (USGS 01646500) has a record from 1930 to 2026 with a mean of "
              "320.7738 m3/s, a minimum of 3.43 and a maximum of 12100. The trend in annual mean flow is increasing.")
    out = lock_answer(answer, res, POTOMAC_WORDS)
    assert not out["ok"]
    assert any("trend wording" in r and "p = 0.82" in r for r in out["refused"])
    assert any("no significant trend" in line for line in out["facts"])


def test_the_correct_reading_passes() -> None:
    res = [_result("analyze_station", _potomac_payload())]
    for answer in (
        "USGS 01646500 runs from 1930-03-01 to 2026-10-24, mean 320.77 m3/s. There is no significant trend in the "
        "annual mean (Mann-Kendall p = 0.82; Sen's slope +0.059 m3/s per year).",
        "No, the Potomac at Little Falls is not getting drier: the annual-mean trend is not significant (p = 0.82).",
        "The annual means rise slightly (Sen's slope 0.059 m3/s per year), but the trend is not significant.",
    ):
        out = lock_answer(answer, res, POTOMAC_WORDS)
        assert out["ok"], (answer, out["refused"])


def test_numbers_from_an_earlier_question_are_refused_when_no_tool_ran() -> None:
    # Recorded: no tool call, the figures came from the previous question's result still in the session.
    answer = ("The 100-year flood (Q10) is not directly available from the data, which covers a record from "
              "1930-03-01.")
    out = lock_answer(answer, [], "What is the 100-year flood at this gauge?")
    assert not out["ok"]
    joined = " ".join(out["refused"])
    assert "1930-03-01" in joined and "Q10" in joined
    assert "100" not in joined.replace("1930", "")  # the 100 is the reader's own


def test_a_trend_with_no_test_behind_it_is_refused() -> None:
    answer = ("The Potomac at Little Falls shows an increasing trend in annual mean flow. The Mann-Kendall test "
              "indicates an upward trend.")
    out = lock_answer(answer, [], "Is the Potomac at Little Falls getting drier? Use the annual-mean trend.")
    assert not out["ok"]
    assert any("no trend was computed" in r for r in out["refused"])


KINGSTON = {"n_catalog": 60000, "n_returned": 3, "limit": 5, "stations": [
    {"source": "uk_ea", "station_id": "E02102A", "name": "KINGSTON VALE", "latitude": 51.43, "longitude": -0.26},
    {"source": "uk_ea", "station_id": "3400TH", "name": "HOGSMILL AT EWELL", "latitude": 51.35, "longitude": -0.25},
    {"source": "uk_ea", "station_id": "3990TH", "name": "KINGSTON BRIDGE", "latitude": 51.41, "longitude": -0.31},
]}


def test_gauge_ids_swapped_between_sites_are_refused() -> None:
    res = [_result("find_stations", KINGSTON, {"near": [51.1, 0.0], "limit": 5})]
    words = "Find the five gauges nearest to Kingston upon Thames"
    swapped = "KINGSTON VALE (3400TH), HOGSMILL AT EWELL (E02102A) and KINGSTON BRIDGE (3990TH)."
    out = lock_answer(swapped, res, words)
    assert not out["ok"]
    assert any("3400TH is the id of HOGSMILL AT EWELL" in r for r in out["refused"])
    right = "KINGSTON VALE (E02102A), HOGSMILL AT EWELL (3400TH) and KINGSTON BRIDGE (3990TH)."
    ok = lock_answer(right, res, words)
    assert ok["ok"], ok["refused"]
    # The search point was the model's own (about 35 km from Kingston): said, not hidden.
    assert ok["notes"] and "51.1" in ok["notes"][0]


def test_an_id_that_no_result_holds_is_refused() -> None:
    res = [_result("find_stations", KINGSTON)]
    out = lock_answer("The nearest is KINGSTON VALE (E02103B).", res, "nearest gauge to Kingston")
    assert not out["ok"] and any("E02103B" in r for r in out["refused"])


def test_the_recorded_anywhere_answer_passes_on_its_numbers() -> None:
    here = {"latitude": 25.05, "longitude": 121.55, "start": "2016-10-24", "end": "2026-10-24",
            "climate": {"precipitation_mm_per_year": 1733.4111, "temperature_mean_c": 22.7201,
                        "aridity_index": 1.4838, "aridity_class": "humid"},
            "glofas": {"unit": "m3/s", "start": "2006-01-01", "end": "2026-10-24",
                       "stats": {"mean": 5.6336, "min": 1.35, "max": 214.28}, "modelled": True}}
    res = [_result("anywhere", here, {"lat": 25.05, "lon": 121.55})]
    answer = ("At 25.05, 121.55 the climate is humid: 1733.4111 mm of rain a year, 22.7201 °C, aridity 1.4838. "
              "GloFAS gives a mean discharge of 5.6336 m3/s from 2006 to 2026, with a minimum of 1.35 and a "
              "maximum of 214.28 m3/s.")
    out = lock_answer(answer, res, "What is the climate and modelled discharge at 25.05, 121.55?")
    assert out["ok"], out["refused"]


@pytest.mark.parametrize("answer", [
    "The mean flow is 999 m3/s.",
    "The 100-year flood is 4,500 m3/s.",
    "The record starts in 1950.",
])
def test_an_invented_number_is_refused(answer: str) -> None:
    res = [_result("analyze_station", _potomac_payload())]
    assert not lock_answer(answer, res, POTOMAC_WORDS)["ok"]


def test_rounding_and_list_markers_are_not_refused() -> None:
    res = [_result("analyze_station", _potomac_payload())]
    answer = "1. Mean flow: 320.8 m3/s.\n2. Lowest day: 3.4 m3/s.\n3. Highest day: 12,100 m3/s."
    out = lock_answer(answer, res, POTOMAC_WORDS)
    assert out["ok"], out["refused"]
