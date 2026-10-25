"""The worker's on-device Ask Python (#590), run in CPython with a fake ``js`` module.

It is the exact code string worker.js hands to Pyodide: op "tool" runs one analyst tool and returns only the
compact result the small model is shown, op "lock" holds the model's answer to this question's results. The
map's reply check gets the request's words, so a box the model made up can be refused.
"""

from __future__ import annotations

import json
import re
import sys
import types
from pathlib import Path

import pytest

from aquascope.ai_engine import analyst

ROOT = Path(__file__).resolve().parents[2]
WORKER = ROOT / "explorer" / "worker.js"


def _block(fn: str) -> str:
    text = WORKER.read_text(encoding="utf-8")
    m = re.search(r"async function " + fn + r"\(.*?const code = `(.*?)`;", text, re.S)
    assert m, f"{fn}'s Python block is missing from worker.js"
    return m.group(1)


def _runner(monkeypatch, fn: str, var: str):
    code = _block(fn)

    def call(payload: dict):
        fake = types.ModuleType("js")
        setattr(fake, var, json.dumps(payload))
        monkeypatch.setitem(sys.modules, "js", fake)
        ns: dict = {}
        lines = code.strip().splitlines()
        exec("\n".join(lines[:-1]), ns)  # noqa: S102 - the worker's own code, under test
        return json.loads(eval(lines[-1], ns))  # noqa: S307 - the block's last expression, as Pyodide returns it

    return call


@pytest.fixture
def device(monkeypatch):
    return _runner(monkeypatch, "deviceAsk", "__aqDev")


def test_the_tool_op_returns_the_compact_result_not_the_payload(device, monkeypatch):
    payload = {"source": "usgs", "station_id": "01646500", "unit": "m3/s", "start": "1930-03-01",
               "end": "2026-10-24", "stats": {"mean": 320.7738, "min": 3.43, "max": 12100.0},
               "annual_max": {"year": list(range(1930, 2026)), "v": [1.0] * 96},
               "methods": [{"name": "x", "text": "y" * 500, "citation": "z"}],
               "trend": {"on": "annual mean", "p_value": 0.82, "trend": "no trend", "sens_slope_per_year": 0.059}}
    spec = analyst.ToolSpec("analyze_station", "d", {"type": "object"}, lambda **kw: payload)
    monkeypatch.setattr(analyst, "_tool_specs", lambda: [spec])
    out = device({"op": "tool", "name": "analyze_station", "args": {"source": "usgs", "station_id": "01646500"}})
    assert out["ok"] is True
    assert "annual_max" not in out["compact"] and "methods" not in out["compact"]
    assert out["compact"]["trend_annual_mean"]["p_value"] == 0.82


def test_a_failing_tool_comes_back_as_data(device, monkeypatch):
    def boom(**kw):
        raise ValueError("no such station")

    monkeypatch.setattr(analyst, "_tool_specs", lambda: [analyst.ToolSpec("find_stations", "d", {}, boom)])
    out = device({"op": "tool", "name": "find_stations", "args": {}})
    assert out["ok"] is False and "no such station" in out["compact"]["error"]
    assert device({"op": "tool", "name": "nope", "args": {}})["ok"] is False


def test_the_lock_op_refuses_the_recorded_trend_with_no_test(device):
    out = device({"op": "lock", "answer": "The Mann-Kendall test indicates an upward trend.", "results": [],
                  "words": "Is the Potomac at Little Falls getting drier? Use the annual-mean trend."})
    assert out["ok"] is False and out["refused"]


def test_the_map_reply_op_hands_the_words_to_the_check(monkeypatch):
    run = _runner(monkeypatch, "mapCommand", "__aqMap")
    reply = json.dumps({"actions": [{"type": "fly_to", "bbox": [15, 20, 30, 40]}]})
    out = run({"op": "reply", "reply": reply, "text": "where is it driest in Africa right now? zoom there",
               "today": "2026-10-25", "context": "", "actions": [], "llm": {}})
    assert out["actions"][0]["region"] == "africa"
    assert out["actions"][0]["bbox"] == [-18.0, -35.0, 52.0, 37.5]


def test_the_page_sends_what_the_worker_reads():
    ask = (ROOT / "explorer" / "src" / "ask.js").read_text(encoding="utf-8")
    cmd = (ROOT / "explorer" / "src" / "map-command.js").read_text(encoding="utf-8")
    studio = (ROOT / "explorer" / "src" / "studio.js").read_text(encoding="utf-8")
    assert 'call("device_ask", { op: "tool", name, arguments: args })' in ask
    assert 'call("device_ask", { op: "lock", answer, results, words })' in ask
    assert '{ op: "reply", reply, text, today: todayIso() }' in cmd
    assert "parseBriefReply(reply, text)" in studio
    worker = WORKER.read_text(encoding="utf-8")
    assert 'if (m.type === "device_ask") return await deviceAsk(m);' in worker
