"""Explain what is on screen (#562): facts read from the map by code, the template notes, and the claim lock."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

np = pytest.importorskip("numpy")

from aquascope import cli  # noqa: E402
from aquascope import map_commands as mc  # noqa: E402
from aquascope import map_explain as me  # noqa: E402
from aquascope.map_layers import STATUS_CLASSES  # noqa: E402
from tests.test_map_layers import _tiff  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DEG = 0.5
RED = {c["id"]: c["rgb"][0] for c in STATUS_CLASSES}


def _box(grid, west, south, east, north, value):
    rows = slice(int((90 - north) / DEG), int((90 - south) / DEG))
    grid[rows, slice(int((west + 180) / DEG), int((east + 180) / DEG))] = value


def _status_file():
    """A half-degree world: normal land from 0 to 40 E and 0 to 30 N, with a much above normal block in its
    west, a smaller below normal block in its east, and sea (no data) everywhere else."""
    red = np.zeros((int(180 / DEG), int(360 / DEG)), dtype=np.uint8)
    _box(red, 0, 0, 40, 30, RED["normal"])
    _box(red, 2, 8, 18, 24, RED["much_above"])      # 16 x 16 degrees
    _box(red, 28, 4, 36, 10, RED["below"])          # 8 x 6 degrees
    return _tiff([red, red, red], tile=64)


VIEW = {"bbox": [0, 0, 40, 30], "date": "2026-10-12", "layers": list(me.LAYERS), "zoom": 4.5}

WARNINGS = {"issue_date": "2026-10-09", "features": [
    # Peaks on the 4th day at its 25-year flow; on the map's day (the 4th, 12 Oct) it is at its 10-year flow.
    {"type": "Feature", "geometry": {"type": "Point", "coordinates": [20.0, 15.0]},
     "properties": {"river_id": 1, "rp": 25, "peak": 2400.0, "q2": 800.0, "day": "2026-10-13",
                    "daily": "1233344321000000"}},
    {"type": "Feature", "geometry": {"type": "Point", "coordinates": [24.0, 20.0]},
     "properties": {"river_id": 2, "rp": 2, "peak": 120.0, "q2": 100.0, "day": "2026-10-10",
                    "daily": "011100000000000"}},
    # Outside the view.
    {"type": "Feature", "geometry": {"type": "Point", "coordinates": [-60.0, 15.0]},
     "properties": {"river_id": 3, "rp": 100, "peak": 9000.0, "q2": 1000.0, "day": "2026-10-10", "daily": "6"}},
]}

FLOODS = {"months": ["2025-10", "2025-11"], "deg": 0.5, "cells": [
    [int((25.25 + 90) / 0.5), int((30.25 + 180) / 0.5), 40, 0],    # centred 25.25 N, 30.25 E: the busiest cell
    [int((25.25 + 90) / 0.5), int((30.25 + 180) / 0.5), 8, 3],     # the same cell, the other month
    [int((5.25 + 90) / 0.5), int((8.25 + 180) / 0.5), 11, 900],    # 5.25 N, 8.25 E
    [int((40.25 + 90) / 0.5), int((8.25 + 180) / 0.5), 500, 0],    # outside the view
]}

GAUGES = [
    {"source": "usgs", "station_id": "01", "name": "VALATIE KILL NEAR NASSAU NY", "agency": "USGS (US)",
     "lat": 18.0, "lon": 10.0, "cls": "much_above", "pct": 97.4, "date": "2026-10-09", "value": 12.34, "n_years": 36},
    {"source": "usgs", "station_id": "02", "name": "Dry Creek", "agency": "USGS (US)",
     "lat": 7.0, "lon": 32.0, "cls": "much_below", "pct": 3, "date": "2026-10-09", "value": 0.5, "n_years": 41},
    {"source": "usgs", "station_id": "03", "name": "Plain", "agency": "USGS (US)",
     "lat": 22.0, "lon": 24.0, "cls": "normal", "pct": 50, "date": "2026-10-09", "value": 3.0, "n_years": 20},
]


@pytest.fixture(scope="module")
def status():
    return {"month": "2026-09", "data": _status_file()}


@pytest.fixture(scope="module")
def facts(status):
    return me.view_facts(VIEW, status=status, warnings=WARNINGS, floods_past=FLOODS, gauges=GAUGES)


def ph(fid, part=""):
    """A fact's placeholder as a model writes it: {f3}, {f3.when}."""
    return "{" + fid + (f".{part}" if part else "") + "}"


def by_kind(res, kind, **match):
    return [f for f in res["facts"] if f["kind"] == kind and all(f.get(k) == v for k, v in match.items())]


# ── the facts ────────────────────────────────────────────────────────────────


def test_the_status_sample_reads_only_the_view_and_samples_big_views():
    data = _status_file()
    s = me.status_sample(data, [0, 0, 40, 30])
    assert s["classes"].shape == (60, 80) and s["deg"] == DEG
    assert s["lats"][0] == pytest.approx(29.75) and s["lons"][0] == pytest.approx(0.25)
    coarse = me.status_sample(data, [-180, -90, 180, 90], max_cells=90)
    assert coarse["classes"].shape[1] <= 90 and coarse["deg"] == pytest.approx(DEG * 8)
    # Across the antimeridian: the columns run on from 170 E to 170 W.
    wrap = me.status_sample(data, [170, 0, -170, 10])
    assert wrap["classes"].shape == (20, 40) and wrap["lons"][0] == pytest.approx(170.25)
    assert wrap["lons"][-1] == pytest.approx(-170.25)
    # A view narrower than one cell is that cell.
    assert me.status_sample(data, [10.01, 10.01, 10.02, 10.02])["classes"].shape == (1, 1)


def test_status_facts_share_the_mapped_land_and_find_the_largest_areas(facts):
    above = by_kind(facts, "status_share", side="above")[0]
    below = by_kind(facts, "status_share", side="below")[0]
    # Area-weighted shares of the mapped land (sea is not counted): 16 x (sin 24 - sin 8) of 40 x sin 30.
    assert 21 < above["value"] < 22 and above["shown"] == f"{round(above['value'])}%"
    assert 3 < below["value"] < 5
    area = by_kind(facts, "status_area", **{"class": "much_above"})[0]
    lat, lon = area["place"]["lat"], area["place"]["lon"]
    assert 8 < lat < 24 and 2 < lon < 18                             # on the colour it describes
    assert area["value"] == above["value"]                           # the one much above area is all of it
    assert area["when"] == "September 2026" and area["colour_words"] == "dark teal"
    size = by_kind(facts, "status_size", **{"class": "much_above"})[0]
    assert size["unit"] == "km²" and 2.9e6 < size["value"] < 3.1e6    # 16 x 16 degrees near 16 N
    bound = by_kind(facts, "status_class", **{"class": "much_above"})[0]
    assert bound["shown"] == "above the 90th percentile"
    assert by_kind(facts, "status_class", **{"class": "below"})[0]["shown"] == "in the 10th to 25th percentile"
    assert not by_kind(facts, "status_area", **{"class": "normal"})


def test_a_globe_view_keeps_to_the_side_facing_the_reader(status):
    view = {**VIEW, "bbox": [-180, -85, 180, 85], "disc": {"lat": 15, "lon": 30, "deg": 10}}
    res = me.view_facts(view, status=status)
    # The much above block (2 to 18 E) is more than 10 degrees of arc from 15 N, 30 E: left out.
    assert not by_kind(res, "status_area", **{"class": "much_above"})
    assert by_kind(res, "status_area", **{"class": "below"})
    with pytest.raises(ValueError):
        me.view_facts({**view, "disc": {"lat": 0, "lon": 0, "deg": 120}})


def test_floods_ahead_classes_each_reach_on_the_map_day(facts):
    count = by_kind(facts, "fa_count")[0]
    assert count["value"] == 2 and count["when"] == "on Mon 12 Oct"
    top = by_kind(facts, "fa_class", rank=0)[0]
    assert top["value"] == 10 and top["shown"] == "10-year flow"      # the 4th day's class, not the peak's
    assert (top["place"]["lat"], top["place"]["lon"]) == (15.0, 20.0)
    peak = by_kind(facts, "fa_peak", rank=0)[0]
    assert peak["shown"] == "2,400 m³/s" and peak["when"] == "on Tue 13 Oct"
    assert by_kind(facts, "fa_ratio", rank=0)[0]["shown"] == "3.0 times"
    assert all(f.get("river_id") != 3 for f in facts["facts"])        # outside the view


def test_a_cut_issue_gives_its_count_as_a_floor():
    res = me.view_facts(VIEW, warnings={**WARNINGS, "truncated": True})
    count = by_kind(res, "fa_count")[0]
    assert count["value"] == 2 and count["shown"] == "at least 2"
    notes = me.template_notes(res["facts"], VIEW["bbox"])
    assert "at least 2 reaches in view pass theirs" in notes[0]["text"]


def test_outside_the_fifteen_days_the_peak_class_is_shown(status):
    res = me.view_facts({**VIEW, "date": "2026-11-30"}, warnings=WARNINGS)
    top = by_kind(res, "fa_class", rank=0)[0]
    assert top["value"] == 25 and top["when"] == "in the 15 days from 9 Oct"


def test_floods_past_sums_the_months_inside_the_view(facts):
    total = by_kind(facts, "fp_news_total")[0]
    assert total["value"] == 59 and total["when"] == "Oct 2025 to Nov 2025"
    top = by_kind(facts, "fp_news_cell", rank=0)[0]
    assert top["value"] == 48 and (top["place"]["lat"], top["place"]["lon"]) == (25.25, 30.25)
    radar = by_kind(facts, "fp_radar_cell", rank=0)[0]
    assert radar["value"] == 900 and radar["unit"] == "detections"


def test_gauges_furthest_from_normal_with_their_record(facts):
    high = by_kind(facts, "gauge_pct", side="above")[0]
    assert high["shown"] == "97th percentile" and high["when"] == "on 9 Oct"
    assert high["place"]["name"] == "Valatie Kill near Nassau NY"    # capitals tidied
    assert high["source"] == "gauges:usgs"
    assert me._credit(high["source"])["short"] == "USGS Water Data gauge record, US-PD"   # the registry's terms
    assert by_kind(facts, "gauge_years", side="above")[0]["shown"] == "36 years"
    assert by_kind(facts, "gauge_flow", side="above")[0]["shown"] == "12 m³/s"      # two figures under 100
    assert by_kind(facts, "gauge_pct", side="below")[0]["shown"] == "3rd percentile"
    assert by_kind(facts, "gauge_count", side="above")[0]["value"] == 1


def test_layers_that_are_off_give_no_facts_and_say_why(status):
    res = me.view_facts({**VIEW, "layers": ["status"]}, status=status, warnings=WARNINGS, floods_past=FLOODS,
                        gauges=GAUGES)
    assert {f["layer"] for f in res["facts"]} == {"status"}
    empty = me.view_facts({**VIEW, "bbox": [-150, -60, -140, -50]}, status=status, warnings=WARNINGS,
                          floods_past=FLOODS, gauges=GAUGES)
    assert empty["facts"] == [] and len(empty["skipped"]) == 4
    assert me.template_notes(empty["facts"], VIEW["bbox"]) == []


def test_every_fact_names_its_value_unit_and_source(facts):
    ids = [f["id"] for f in facts["facts"]]
    assert ids == [f"f{i}" for i in range(1, len(ids) + 1)]
    for f in facts["facts"]:
        assert f["shown"] and f["source"] and f["layer"] in me.LAYERS and "value" in f and "unit" in f
    assert any("CC BY 4.0" in c for c in facts["credits"])


# ── the template notes ──────────────────────────────────────────────────────


def test_template_notes_are_three_to_five_spaced_and_every_number_traces_to_a_fact(facts):
    notes = me.template_notes(facts["facts"], VIEW["bbox"])
    assert me.MIN_NOTES <= len(notes) <= me.MAX_NOTES
    by_id = {f["id"]: f for f in facts["facts"]}
    for n in notes:
        cited = [by_id[i] for i in n["fact_ids"]]
        assert me.claim_lock(n["title"] + " " + n["text"], cited) == [], n
        assert n["source"] and n["credit"] and n["tone"].startswith("#")
        assert 0 + 40 * me.PIN_MARGIN <= n["lon"] <= 40 - 40 * me.PIN_MARGIN
    for a in notes:
        for b in notes:
            if a is not b:
                assert abs(a["lat"] - b["lat"]) / 30 + abs(a["lon"] - b["lon"]) / 40 > 0.1
    titles = [n["title"] for n in notes]
    assert titles[0] == "Much above normal"          # what the strongest colour means comes first
    assert "Valatie Kill near Nassau NY" in titles
    first = notes[0]
    assert first["text"].startswith("Dark teal: flow above the 90th percentile for September, on ")


def test_a_note_moves_inside_a_large_area_when_its_first_spot_is_taken(status):
    # A gauge sits right on the much above block's best spot: the status note moves to another spot inside it.
    res = me.view_facts(VIEW, status=status)
    area = by_kind(res, "status_area", **{"class": "much_above"})[0]
    assert area["spots"], "a large area offers more than one spot"
    spot = area["place"]
    gauge = {**GAUGES[0], "lat": spot["lat"], "lon": spot["lon"], "pct": 100}
    res = me.view_facts(VIEW, status=status, gauges=[gauge])
    notes = me.template_notes(res["facts"], VIEW["bbox"])
    status_note = next(n for n in notes if n["layer"] == "status" and n["title"] == "Much above normal")
    assert (status_note["lat"], status_note["lon"]) != (spot["lat"], spot["lon"])
    assert 8 < status_note["lat"] < 24 and 2 < status_note["lon"] < 18


def test_explain_names_the_places_of_the_notes_only(status):
    calls = []

    def fake(lat, lon):
        calls.append((lat, lon))
        return [{"properties": {"state": "Somewhere State", "country": "Testland", "postcode": "12345"}}]

    me._NAMES.clear()
    res = me.explain(VIEW, status=status, warnings=WARNINGS, floods_past=FLOODS, gauges=GAUGES, fetch=fake)
    gauge_notes = [n for n in res["notes"] if n["layer"] == "gauges"]
    assert gauge_notes and all(n["place"] == "USGS (US) 01" or n["place"] == "USGS (US) 02" for n in gauge_notes)
    named = [n for n in res["notes"] if n["layer"] != "gauges"]
    assert named and all(n["place"] == "Somewhere State, Testland" for n in named)
    assert len(calls) == len(named) <= me.MAX_NOTES
    assert me.PLACE_CREDIT in res["credits"] and res["prompt"]["system"]


def test_place_names_leave_out_digits_and_fail_quietly():
    def postcode(lat, lon):
        return [{"properties": {"name": "222145", "city": "Patti", "county": "Pratapgarh", "state": "Uttar Pradesh",
                                "country": "India"}}]

    assert me.place_name(26, 82, 5, postcode) == "Uttar Pradesh, India"
    assert me.place_name(26, 82, 9, postcode) == "Patti, Uttar Pradesh"

    def broken(lat, lon):
        raise OSError("offline")

    assert me.place_name(26, 82, 5, broken) == ""
    assert me.place_name(26, 82, 5, lambda lat, lon: []) == ""
    # A gazetteer that fails is asked once per explanation, not once per note.
    calls = []

    def down(lat, lon):
        calls.append(1)
        raise OSError("connection refused")

    me._NAMES.clear()
    notes = [{"lat": float(i), "lon": float(i), "place": ""} for i in range(4)]
    assert [n["place"] for n in me.name_notes(notes, 5, down)] == ["", "", "", ""] and len(calls) == 1


# ── the claim lock ──────────────────────────────────────────────────────────


def test_the_claim_lock_lets_only_the_numbers_of_the_cited_facts_through(facts):
    by_id = {f["id"]: f for f in facts["facts"]}
    high = by_kind(facts, "gauge_pct", side="above")[0]
    assert me.claim_lock(f"At the {ph(high['id'])} today.", [high]) == []
    assert me.claim_lock("At the 97th percentile today.", [high]) == []          # its own number, copied right
    assert me.claim_lock("At the 99th percentile today.", [high]) == ["99"]
    assert me.claim_lock("Up 40% since 2019.", [high]) == ["2019", "40"]
    peak = by_kind(facts, "fa_peak", rank=0)[0]
    assert me.claim_lock("Peaks at 2400 m³/s on 13 Oct.", [peak]) == []         # thousands with or without a comma
    assert by_id  # the facts are there to cite


def test_model_notes_are_filled_in_by_code_and_held_to_their_facts(facts):
    fid = {f["kind"] + str(f.get("rank", f.get("side", f.get("class", "")))): f["id"] for f in facts["facts"]}
    reply = json.dumps({"notes": [
        {"facts": [fid["fa_class0"], fid["fa_peak0"]], "title": "A big flow coming",
         "text": f"This reach reaches its {ph(fid['fa_class0'])} {ph(fid['fa_class0'], 'when')}, "
                 f"peaking at {ph(fid['fa_peak0'])}."},
        {"facts": [fid["gauge_pctabove"]], "title": "A gauge running high",
         "text": f"At the {ph(fid['gauge_pctabove'])}, the highest in 120 years."},          # 120 is made up
        {"facts": ["f999"], "title": "Ghost", "text": "Nothing."},
        {"facts": [fid["fp_news_total"]], "title": "Many reports", "text": f"{ph(fid['fp_news_total'])} reports."},
        {"facts": [fid["fp_news_cell0"]], "title": "Reports here",
         "text": f"{ph(fid['fp_news_cell0'])} reports, {ph(fid['fp_news_total'])} in the whole view."},
    ]})
    out = me.check_model_notes(reply, facts["facts"], VIEW["bbox"])
    titles = [n["title"] for n in out["notes"]]
    # Two passed; a template note on a fact the model left alone makes the third.
    assert titles[:2] == ["A big flow coming", "Reports here"] and len(titles) == me.MIN_NOTES
    assert out["notes"][2]["by"] == "rules" and "by" not in out["notes"][0]
    first = out["notes"][0]
    assert first["text"] == "This reach reaches its 10-year flow on Mon 12 Oct, peaking at 2,400 m³/s."
    assert (first["lat"], first["lon"]) == (15.0, 20.0)
    # A placeholder of a fact the note did not list still counts as cited, with its source.
    assert fid["fp_news_total"] in out["notes"][1]["fact_ids"]
    assert out["notes"][1]["text"] == "48 reports, 59 in the whole view."
    reasons = " | ".join(out["refused"])
    assert "a number not in its facts (120)" in reasons
    assert "no known fact" in reasons and "none of its facts has a place" in reasons


def test_a_reply_that_is_not_notes_is_refused_whole(facts):
    assert me.check_model_notes("Sorry, I cannot help.", facts["facts"])["notes"] == []
    assert me.check_model_notes({"actions": []}, facts["facts"])["refused"] == ["the model did not reply with notes"]
    note = {"facts": ["f1", "f4"], "title": "Wet", "text": "Mostly {f4}."}
    fenced = "```json\n" + json.dumps({"notes": [note]}) + "\n```"
    out = me.check_model_notes(fenced, facts["facts"])
    assert out["notes"][0]["text"].startswith("Mostly ") and out["notes"][0]["title"] == "Wet"


def test_the_prompt_lists_each_fact_with_its_placeholder(facts):
    p = me.notes_prompt(facts["facts"], context="a map of somewhere")
    for f in facts["facts"]:
        assert ph(f["id"]) in p["system"]
    assert "a map of somewhere" in p["system"] and p["schema"]["required"] == ["notes"]


def test_model_notes_go_through_the_readers_client(facts):
    class Fake:
        def __init__(self):
            self.chat = self
            self.completions = self
            self.sent = None

        def create(self, **kw):
            self.sent = kw
            msg = type("M", (), {"content": json.dumps({"notes": [
                {"facts": ["f4"], "title": "Wet west", "text": "{f4} of the mapped land, in 2099."}]})})
            return type("R", (), {"choices": [type("C", (), {"message": msg})]})

    fake = Fake()
    out = me.model_notes(facts["facts"], provider="openai", model="m", client=fake, bbox=VIEW["bbox"])
    assert out["model"] == "m via openai" and out["notes"] == [] and "2099" in out["refused"][0]
    assert fake.sent["temperature"] == 0 and "{f4}" in fake.sent["messages"][0]["content"]


# ── the faces and the page ──────────────────────────────────────────────────


@pytest.mark.parametrize("text", ["What am I seeing?", "what's on the screen", "Explain this view", "explain",
                                  "what do the colours mean here", "Whats going on here"])
def test_what_am_i_seeing_is_the_explain_control(text):
    res = mc.parse_command(text, today="2026-10-10")
    assert res["matched"] and res["control"] == "explain" and res["actions"] == []


def test_the_rules_still_read_other_requests_as_actions():
    assert mc.parse_command("what is the rhine", today="2026-10-10")["control"] is None


def test_the_cli_prints_the_notes(monkeypatch, capsys, facts):
    notes = me.template_notes(facts["facts"], VIEW["bbox"])
    seen = {}

    def fake(bbox, day, layers, name_places=True, llm=None):
        seen.update(bbox=bbox, day=day, layers=layers, llm=llm)
        return {**facts, "notes": notes, "by": "rules"}

    monkeypatch.setattr(me, "explain_view", fake)
    monkeypatch.setattr(sys, "argv", ["aquascope", "layers", "explain", "0", "0", "40", "30", "--date", "2026-10-12",
                                      "--layers", "status", "gauges", "--facts"])
    cli.main()
    out = capsys.readouterr().out
    assert seen == {"bbox": [0.0, 0.0, 40.0, 30.0], "day": "2026-10-12", "layers": ["status", "gauges"], "llm": None}
    assert "1. Much above normal" in out and "Facts:" in out and "f1" in out


def test_the_cli_refuses_an_unknown_layer(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["aquascope", "layers", "explain", "0", "0", "1", "1", "--layers", "lava"])
    with pytest.raises(SystemExit):
        cli.main()
    assert "Unknown layer lava" in capsys.readouterr().out


def test_the_mcp_tool_is_registered():
    from aquascope import mcp_server

    assert callable(mcp_server.explain_view)
    src = (ROOT / "aquascope" / "mcp_server.py").read_text()
    assert "server.tool()(explain_view)" in src


def test_the_note_colours_are_the_pages():
    now_core = (ROOT / "explorer" / "src" / "now-core.js").read_text()
    for cid, (hex_, _words) in me.CLASS_COLOURS.items():
        assert re.search(f'id: "{cid}",[^}}]*color: "{hex_}"', now_core), cid
    floods = (ROOT / "explorer" / "src" / "floods-ahead-core.js").read_text()
    for rp, hex_ in me.FLOOD_COLOURS.items():
        assert f'{{ rp: {rp}, label: "{rp}-year", color: "{hex_}" }}' in floods
    past = (ROOT / "explorer" / "src" / "floods-past-core.js").read_text()
    assert f'NEWS_COLOR = "{me.NEWS_COLOUR}"' in past and f'RADAR_COLOR = "{me.RADAR_COLOUR}"' in past


def test_the_worker_runs_the_same_functions():
    worker = (ROOT / "explorer" / "worker.js").read_text()
    assert '"map_explain"' in worker.split("LITE_TYPES", 1)[1].split("\n", 1)[0]
    for fn in ("explain", "check_model_notes", "model_notes", "name_notes"):
        assert f"_me.{fn}(" in worker and hasattr(me, fn)
