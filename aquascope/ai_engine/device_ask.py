"""Ask on the reader's device (#590): what a small model is shown of a tool result, and the lock on its answer.

The Explorer's on-device Ask runs Chrome's built-in model (or WebLLM) through a short loop: the model picks a
tool, the worker runs it, the model writes two or three sentences. Two things went wrong on the device:

* the tool result was cut at its first 3,000 characters, which ended inside the annual maxima, so the trend
  and the flood frequency never reached the model and it guessed them ("an increasing trend" where the test
  gives Sen's slope +0.059 m3/s per year, p = 0.82);
* nothing checked the answer, so numbers from an earlier question, a trend never computed and gauge ids
  swapped between sites reached the page.

:func:`compact_result` is what the model is shown instead: the record, the statistics, the flow-duration
points, the return levels and the trend with its reading in words, and no series. :func:`lock_answer` holds
the answer to this question's compact results, the way the map roles' locks hold theirs: every number, date
and gauge id must be in them (rounding allowed), every trend or significance word must agree with the test.
When it refuses, :func:`facts` is what the page shows instead, with a short line saying why.

Internal: only the Explorer's worker imports this module.
"""

from __future__ import annotations

import json
import re
from typing import Any

from aquascope.ai_engine.verify import (
    _COMPASS,
    _CONVENTIONS,
    _DATE,
    _EXPONENT_UNIT,
    _SQUARED_UNIT,
    _close,
    _numbers,
    normalise,
)

#: Tools whose result is one station's (or one model cell's) analysis.
_ANALYSIS_TOOLS = ("analyze_station", "flood_frequency")

#: Keys that never help a small model answer: citations, licences, hashes.
_DROP_KEYS = frozenset({"methods", "citation", "license", "attribution", "url", "data_snapshot", "archive_revision",
                        "software_revision", "eligibility", "sampling", "series", "series_downsampled",
                        "annual_max", "annual_max_excluded", "requested", "params"})

#: The most a compact result may weigh, as JSON; past it, lists are cut harder.
MAX_CHARS = 4000

_P_SIGNIFICANT = 0.05


def _round(x: Any, digits: int = 4) -> Any:
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        return x
    if x != x or x in (float("inf"), float("-inf")):
        return None
    return round(float(x), digits) if isinstance(x, float) else x


def _short(text: Any, limit: int) -> str | None:
    if not isinstance(text, str) or not text.strip():
        return None
    s = re.sub(r"\s+", " ", text).strip()
    return s if len(s) <= limit else s[: limit - 3].rstrip() + "..."


def _shrink(value: Any, *, depth: int = 0, list_limit: int = 8) -> Any:
    """A generic compact copy: no citations, no long numeric series, short strings, a few levels deep."""
    if depth > 4:
        return None
    if isinstance(value, dict):
        out = {}
        for k, v in value.items():
            if k in _DROP_KEYS:
                continue
            small = _shrink(v, depth=depth + 1, list_limit=list_limit)
            if small is not None and small != {} and small != []:
                out[k] = small
        return out
    if isinstance(value, (list, tuple)):
        if len(value) > list_limit and all(isinstance(v, (int, float)) or v is None for v in value):
            return None   # a series: the statistics carry what the answer needs
        return [s for s in (_shrink(v, depth=depth + 1, list_limit=list_limit) for v in value[:list_limit])
                if s is not None]
    if isinstance(value, str):
        return _short(value, 200)
    return _round(value)


def _trend(block: Any, unit: str | None) -> dict[str, Any] | None:
    """A Mann-Kendall block with its reading in words, which the model is asked to copy."""
    if not isinstance(block, dict) or block.get("p_value") is None:
        return None
    p = float(block["p_value"])
    slope = block.get("sens_slope_per_year")
    out: dict[str, Any] = {k: _round(block[k]) for k in ("on", "p_value", "sens_slope_per_year", "n_years")
                           if block.get(k) is not None}
    out["significant"] = p < _P_SIGNIFICANT
    on = block.get("on") or "the series"
    slope_txt = ""
    if isinstance(slope, (int, float)):
        slope_txt = f"; Sen's slope {slope:+.4g}{' ' + unit if unit else ''} per year"
    if p < _P_SIGNIFICANT:
        direction = block.get("trend") if block.get("trend") in ("increasing", "decreasing") else (
            "increasing" if isinstance(slope, (int, float)) and slope > 0 else "decreasing")
        out["direction"] = direction
        out["reading"] = f"a significant {direction} trend in the {on} (Mann-Kendall p = {p:.3g}{slope_txt})"
    else:
        out["reading"] = f"no significant trend in the {on} (Mann-Kendall p = {p:.3g}{slope_txt})"
    return out


def _return_levels(ffa: Any) -> dict[str, Any] | None:
    if not isinstance(ffa, dict):
        return None
    fits = ffa.get("fits") if isinstance(ffa.get("fits"), dict) else {}
    gev = (fits.get("gev_lmoments") or {}).get("q_by_T") or {}
    lp3 = fits.get("lp3") or {}
    lp3_q = lp3.get("q_by_T") or {}
    periods = ffa.get("return_periods") or sorted({int(float(t)) for t in [*gev, *lp3_q]})
    ci = lp3.get("ci") if isinstance(lp3.get("ci"), list) else []
    rows = []
    for i, t in enumerate(periods):
        key = str(int(t)) if float(t).is_integer() else str(t)
        row: dict[str, Any] = {"T_years": _round(t)}
        if gev.get(key) is not None:
            row["gev"] = _round(gev[key], 2)
        if lp3_q.get(key) is not None:
            row["lp3"] = _round(lp3_q[key], 2)
        if i < len(ci) and isinstance(ci[i], (list, tuple)) and len(ci[i]) == 2:
            row["lp3_90ci"] = [_round(ci[i][0], 2), _round(ci[i][1], 2)]
        if len(row) > 1:
            rows.append(row)
    out: dict[str, Any] = {}
    if ffa.get("n_years") is not None:
        out["n_years"] = ffa["n_years"]
    if rows:
        out["return_levels"] = rows
    rec = ffa.get("record_max")
    if isinstance(rec, dict) and rec.get("value") is not None:
        out["record_max"] = {k: _round(rec[k], 2) for k in ("value", "year") if rec.get(k) is not None}
    return out or None


def compact_analysis(payload: dict[str, Any]) -> dict[str, Any]:
    """One analysis (analyze_station, flood_frequency, a GloFAS cell): record, statistics, FDC, floods, trend."""
    if not isinstance(payload, dict):
        return {}
    if payload.get("error"):
        return {"error": _short(str(payload["error"]), 300)}
    unit = payload.get("unit")
    out: dict[str, Any] = {k: _round(payload[k]) for k in (
        "source", "station_id", "name", "river", "agency", "variable", "unit", "start", "end", "years", "n", "modelled",
        "comparable") if payload.get(k) is not None}
    stats = payload.get("stats")
    if isinstance(stats, dict):
        # min and max are of the daily values, not of annual ones; the key says so.
        out["daily_values"] = {k: _round(v) for k, v in stats.items() if isinstance(v, (int, float))}
    fdc = payload.get("fdc")
    if isinstance(fdc, dict):
        pts = {k: _round(fdc[k]) for k in ("q95", "q50", "q10") if fdc.get(k) is not None}
        if pts:
            out["flow_duration"] = {**pts, "note": "q95 is exceeded 95 % of the time, q10 10 % of the time"}
    floods = _return_levels(payload.get("ffa"))
    if floods:
        # Two fits, two numbers per period: the model is told which is which, and that the page's own figures
        # are the GEV (#590: a 100-year answer gave the LP3 value and named no method).
        floods["method"] = ("gev: GEV fitted by L-moments, the method the page's figures use; lp3: Log-Pearson III, "
                            "with lp3_90ci its 90 % interval. Name the method with the number.")
        out["flood_frequency"] = floods
    trend = _trend(payload.get("trend"), unit)
    if trend:
        out["trend_annual_mean"] = trend
    ffa = payload.get("ffa") if isinstance(payload.get("ffa"), dict) else {}
    amax = _trend(ffa.get("amax_trend"), unit)
    if amax:
        out["trend_annual_max"] = amax
    for key in ("fetch_note", "note"):
        if _short(payload.get(key), 200):
            out[key] = _short(payload.get(key), 200)
    notes = [_short(n, 160) for n in (payload.get("notes") or []) if isinstance(n, str)]
    if any(notes):
        out["notes"] = [n for n in notes if n][:3]
    return out


def _compact_stations(payload: dict[str, Any]) -> dict[str, Any]:
    fields = ("source", "station_id", "name", "river", "country", "latitude", "longitude", "period_start",
              "period_end")
    rows = []
    for st in (payload.get("stations") or [])[:10]:
        if isinstance(st, dict):
            rows.append({k: _round(st[k]) for k in fields if st.get(k) not in (None, "")})
    return {"n_returned": payload.get("n_returned", len(rows)), "stations": rows}


def _compact_anywhere(payload: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {k: _round(payload[k]) for k in ("latitude", "longitude", "start", "end", "years")
                           if payload.get(k) is not None}
    climate = payload.get("climate")
    if isinstance(climate, dict):
        out["climate"] = {k: _round(climate[k]) for k in (
            "source", "precipitation_mm_per_year", "et0_mm_per_year", "temperature_mean_c", "aridity_index",
            "aridity_class", "wettest_day_mm") if climate.get(k) is not None}
    glofas = payload.get("glofas")
    if isinstance(glofas, dict):
        out["glofas"] = compact_analysis(glofas)
    notes = [_short(n, 160) for n in (payload.get("notes") or []) if isinstance(n, str)]
    if any(notes):
        out["notes"] = [n for n in notes if n][:3]
    return out


def compact_result(name: str, payload: Any) -> dict[str, Any]:
    """What the on-device model is shown of a tool result: the facts an answer needs, no series, no citations.

    Small enough for a small model's context (:data:`MAX_CHARS` as JSON) and never cut in the middle: a
    result that is still too big loses list items, not its trend.
    """
    if not isinstance(payload, dict):
        return {"value": _shrink(payload)}
    if payload.get("error"):
        return {"error": _short(str(payload["error"]), 300)}
    if name in _ANALYSIS_TOOLS:
        out = compact_analysis(payload)
    elif name == "find_stations":
        out = _compact_stations(payload)
    elif name == "anywhere":
        out = _compact_anywhere(payload)
    else:
        out = _shrink(payload) or {}
    limit = 8
    while len(json.dumps(out, default=str)) > MAX_CHARS and limit > 1:
        limit = max(1, limit // 2)
        out = _shrink(out, list_limit=limit) or {}
    return out


# ── the facts the page shows when the model's wording is refused ──────────────


def _fmt(x: Any) -> str:
    if isinstance(x, float):
        return f"{x:,.4g}" if abs(x) < 1e5 else f"{x:,.0f}"
    return str(x)


def _analysis_lines(c: dict[str, Any], label: str = "") -> list[str]:
    unit = c.get("unit") or ""
    who = label or " ".join(str(c[k]) for k in ("name", "source", "station_id") if c.get(k)) or "The record"
    lines = []
    if c.get("error"):
        return [f"{who}: {c['error']}"]
    span = f"{c['start']} to {c['end']}" if c.get("start") and c.get("end") else ""
    daily = c.get("daily_values") or {}
    bits = [f"{k} {_fmt(daily[k])} {unit}".strip() for k in ("mean", "min", "max") if daily.get(k) is not None]
    lines.append(f"{who}: {c.get('variable') or 'record'} {span}".strip()
                 + (f"; daily values {', '.join(bits)}" if bits else "") + ".")
    fd = c.get("flow_duration") or {}
    if fd:
        pts = [f"{k.upper()} {_fmt(fd[k])} {unit}".strip() for k in ("q95", "q50", "q10") if k in fd]
        lines.append(f"Flow duration: {', '.join(pts)}.")
    ff = c.get("flood_frequency") or {}
    rows = {r.get("T_years"): r for r in ff.get("return_levels") or []}
    for t in (100, 10, 2):
        r = rows.get(t)
        if r and r.get("gev") is not None:
            ci = r.get("lp3_90ci")
            ci_txt = f" (LP3 90 % interval {_fmt(ci[0])} to {_fmt(ci[1])})" if ci else ""
            lines.append(f"{t}-year flood (GEV): {_fmt(r['gev'])} {unit}{ci_txt}.")
            break
    for key in ("trend_annual_mean", "trend_annual_max"):
        t = c.get(key)
        if isinstance(t, dict) and t.get("reading"):
            lines.append(f"Trend: {t['reading']}.")
    return lines


def facts(name: str, compact: Any) -> list[str]:
    """Plain lines from one compact result, built by code: what the page shows instead of a refused answer."""
    if not isinstance(compact, dict):
        return []
    if compact.get("error"):
        return [f"{name} failed: {compact['error']}"]
    if name in _ANALYSIS_TOOLS:
        return _analysis_lines(compact)
    if name == "find_stations":
        rows = compact.get("stations") or []
        if not rows:
            return ["The catalogue search found no gauges."]
        return [f"{r.get('name') or r.get('station_id')} ({r.get('source')} {r.get('station_id')})"
                + (f", {r['river']}" if r.get("river") else "")
                + (f", {_fmt(r['latitude'])}, {_fmt(r['longitude'])}" if r.get("latitude") is not None else "")
                for r in rows[:6]]
    if name == "anywhere":
        lines = []
        cl = compact.get("climate") or {}
        if cl:
            bits = []
            if cl.get("precipitation_mm_per_year") is not None:
                bits.append(f"rainfall {_fmt(cl['precipitation_mm_per_year'])} mm a year")
            if cl.get("temperature_mean_c") is not None:
                bits.append(f"mean temperature {_fmt(cl['temperature_mean_c'])} °C")
            if cl.get("aridity_index") is not None:
                bits.append(f"aridity index {_fmt(cl['aridity_index'])}"
                            + (f" ({cl['aridity_class']})" if cl.get("aridity_class") else ""))
            lines.append(f"Climate at {compact.get('latitude')}, {compact.get('longitude')} "
                         f"({cl.get('source', 'ERA5')}): {', '.join(bits)}.")
        if isinstance(compact.get("glofas"), dict):
            lines += _analysis_lines(compact["glofas"], label="GloFAS (modelled)")
        return lines
    flat = []
    for k, v in compact.items():
        if isinstance(v, (str, int, float)) and not isinstance(v, bool):
            flat.append(f"{k.replace('_', ' ')}: {_fmt(v)}")
    return flat[:6]


# ── the lock ───────────────────────────────────────────────────────────────────

#: A gauge id with letters and digits ("E02102A", "3400TH"); pure digit ids are numbers and checked as numbers.
_ALNUM_ID = re.compile(r"\b(?=[A-Za-z0-9_-]*[A-Za-z])(?=(?:[A-Za-z_-]*\d){3})[A-Za-z0-9][A-Za-z0-9_-]{4,}\b")
_Q_LABEL = re.compile(r"\bQ ?(\d{1,2})\b", re.I)
_LIST_MARK = re.compile(r"(?m)^\s*(?:\d{1,2}[.)]|[-*•])\s+")

_TREND_TOPIC = re.compile(r"\btrend|mann|kendall|sen'?s|over (?:the )?(?:time|years|record|decades)|getting|becoming|"
                          r"per year|/yr\b|a year\b", re.I)
_UP = re.compile(r"\b(?:increas\w*|upward|rising|wetter)\b", re.I)
_DOWN = re.compile(r"\b(?:decreas\w*|downward|falling|declin\w*|drier|dryer)\b", re.I)
_NOT_SIG = re.compile(r"\b(?:not|no|non|isn'?t|aren'?t|wasn'?t)[- ](?:statistically )?significant|\binsignificant|"
                      r"\bno (?:clear |real |detectable |meaningful |statistically significant |significant )?trend|"
                      r"\bno evidence of (?:a )?trend|\bnot a (?:significant |real )?trend", re.I)
_NOT_DIR = re.compile(r"\b(?:not|isn'?t|aren'?t|no longer) (?:getting |becoming |really )?"
                      r"(?P<w>increas\w*|decreas\w*|drier|dryer|wetter|rising|falling|declin\w*)", re.I)
_SIG = re.compile(r"\bsignificant", re.I)
_MAXIMA = re.compile(r"\b(?:peak|maxim|flood|annual max|amax)\w*", re.I)
_SENTENCE = re.compile(r"(?<=[.!?])\s+|\n")


def _strings(payload: Any) -> list[str]:
    found: list[str] = []
    stack = [payload]
    while stack:
        item = stack.pop()
        if isinstance(item, dict):
            stack.extend(item.values())
        elif isinstance(item, (list, tuple)):
            stack.extend(item)
        elif isinstance(item, str):
            found.append(item)
    return found


def _pool(payloads: list[Any], words: str) -> list[float]:
    """Every number in the results and in the reader's own words."""
    pool: list[float] = []
    stack = list(payloads)
    while stack:
        item = stack.pop()
        if isinstance(item, bool):
            continue
        if isinstance(item, (int, float)):
            pool.append(float(item))
        elif isinstance(item, dict):
            stack.extend(item.values())
        elif isinstance(item, (list, tuple)):
            stack.extend(item)
        elif isinstance(item, str):
            pool.extend(_numbers(item))
    pool.extend(_numbers(words))
    return pool


def _stations(compacts: list[tuple[str, dict[str, Any]]]) -> list[tuple[str, str]]:
    """(station_id, name) for every gauge in the results."""
    out = []
    for name, c in compacts:
        rows = c.get("stations") if name == "find_stations" else [c]
        for r in rows or []:
            if isinstance(r, dict) and r.get("station_id"):
                out.append((str(r["station_id"]), str(r.get("name") or "")))
    return out


def _swapped_ids(answer: str, stations: list[tuple[str, str]]) -> list[str]:
    """Ids written next to another gauge's name: the nearest name before an id (else after it) must be its own."""
    names = sorted({n for _, n in stations if len(n) >= 4}, key=len, reverse=True)
    if len({sid for sid, _ in stations}) < 2 or not names:
        return []
    own: dict[str, set[str]] = {}
    for sid, n in stations:
        own.setdefault(sid.lower(), set()).add(n.lower())
    wrong = []
    for line in re.split(r"\n|;|(?<=[.!?])\s+", answer):
        low = line.lower()
        spans: list[tuple[int, int, str]] = []
        for n in names:
            for m in re.finditer(re.escape(n.lower()), low):
                if not any(a <= m.start() < b for a, b, _ in spans):
                    spans.append((m.start(), m.end(), n.lower()))
        if not spans:
            continue
        for sid in own:
            for m in re.finditer(r"(?<![\w-])" + re.escape(sid) + r"(?![\w-])", low):
                before = [s for s in spans if s[1] <= m.start()]
                after = [s for s in spans if s[0] >= m.end()]
                if before:
                    near = max(before, key=lambda s: s[1])
                elif after:
                    near = min(after, key=lambda s: s[0])
                else:
                    continue
                if near[2] not in own[sid]:
                    their = next(iter(own[sid]), "").upper() or "another gauge"
                    wrong.append(f"{sid.upper()} is the id of {their}, not {near[2].upper()}")
    return wrong


def _trend_check(answer: str, compacts: list[tuple[str, dict[str, Any]]]) -> list[str]:
    tests: dict[str, dict[str, Any]] = {}
    for _, c in compacts:
        for holder in (c, c.get("glofas") if isinstance(c.get("glofas"), dict) else None):
            if not isinstance(holder, dict):
                continue
            for key in ("trend_annual_mean", "trend_annual_max"):
                if isinstance(holder.get(key), dict) and key not in tests:
                    tests[key] = holder[key]
    refused = []
    for sentence in _SENTENCE.split(answer):
        if not _TREND_TOPIC.search(sentence):
            continue
        not_sig = bool(_NOT_SIG.search(sentence))
        not_dir = _NOT_DIR.search(sentence)
        rest = _NOT_DIR.sub(" ", sentence)
        up, down = bool(_UP.search(rest)), bool(_DOWN.search(rest))
        says_sig = bool(_SIG.search(sentence)) and not not_sig
        if not (not_sig or not_dir or up or down or says_sig):
            continue
        key = "trend_annual_max" if _MAXIMA.search(sentence) and "trend_annual_max" in tests else "trend_annual_mean"
        test = tests.get(key) or next(iter(tests.values()), None)
        if test is None:
            refused.append("the answer states a trend, but no trend was computed for this question")
            continue
        sig = bool(test.get("significant"))
        slope = test.get("sens_slope_per_year")
        actual = test.get("direction") or ("increasing" if isinstance(slope, (int, float)) and slope > 0 else
                                           "decreasing" if isinstance(slope, (int, float)) and slope < 0 else None)
        said = "increasing" if up and not down else "decreasing" if down and not up else None
        p = test.get("p_value")
        if not_sig:
            ok = not sig and (said is None or actual is None or said == actual)
        elif not_dir:
            w = not_dir.group("w").lower()
            denied = "increasing" if _UP.match(w) else "decreasing"
            ok = not (sig and actual == denied)
        else:
            ok = sig and (said is None or said == actual)
        if not ok:
            refused.append(f"its trend wording does not match the test ({test.get('reading') or f'p = {p}'})")
    return refused


# ── labelled numbers: each label held to its own value (#590) ─────────────────
#
# The number check above asks only whether a number is somewhere in the results. On the device that let a right
# number through under a wrong label: "the Potomac's q95 of 3.43 m3/s" (3.43 is its daily minimum; its Q95 is
# 35.7) and "the return period for a flood of magnitude 2 m3/s is 2 years" (2 is a return period, not a flow).
# Here a number that a label claims (Q95, a mean, a minimum, an N-year flood, a record's dates) must be that
# label's value for the gauge the sentence is about, and a number written as a flow must be a flow.

#: A flow written after a number: m3/s and its spellings (NFKC has already turned m³ into m3).
_FLOW_UNIT = re.compile(r"\s*(?:m3/s(?:ec)?|m3 ?s-1|m\^3/s|cumecs|cubic met(?:re|er)s? (?:per|a) second)", re.I)
#: Any other unit after a number: rain, temperature, shares, areas, periods. Such a number is not a flow statistic.
_OTHER_UNIT = re.compile(r"\s*(?:mm\b|°|deg|%|percent|km|kilomet|years?\b|yrs?\b|days?\b|people|inhabitants)",
                         re.I)
#: A number as the prose writes it, with its place in the text: not a label's digits (Q95, m3) nor an id's.
_NUM_AT = re.compile(r"(?<![\w.])-?\d[\d,]*(?:\.\d+)?(?![\w])")
#: Where one claim ends and the next begins: sentence ends, semicolons, and "while", "whereas", "but", "and".
_CLAUSE_BREAK = re.compile(r"[.!?](?=\s|$)|;|\n|,?\s+(?:while|whereas|but|and)\s+", re.I)
#: The labels a statistic is claimed under, and what each may be.
_STAT_LABELS = (
    ("q", re.compile(r"\bq ?(95|50|10)\b", re.I)),
    ("mean", re.compile(r"\b(?:mean|average)\b", re.I)),
    ("median", re.compile(r"\bmedian\b", re.I)),
    ("min", re.compile(r"\b(?:minimum|min|lowest)\b", re.I)),
    ("max", re.compile(r"\b(?:maximum|max|highest)\b", re.I)),
)
_LABEL_WORDS = {"mean": "mean", "median": "median", "min": "minimum", "max": "maximum"}
#: What may stand between a label and its number: "a minimum of 3.43", "mean flow: 320.8", "maximum recorded
#: value is 12100". Anything else ("the annual mean (Mann-Kendall p = 0.82") does not tie the two.
_CONNECTIVE = re.compile(r"[\s:=(,]*(?:(?:daily|recorded|flow|discharge|value|values|is|was|of|about|around|"
                         r"approximately|roughly|at|day|on record|ever|a|an|the)[\s:=(,]+)*", re.I)
#: An N-year flood, said four ways.
_PERIODS = (
    re.compile(r"\b(\d{1,4})[- ](?:year|yr)\b(?=[- ](?:flood|return|event|peak|design|flow|discharge|level|"
               r"storm|high|max))", re.I),
    re.compile(r"\b1[- ]in[- ](\d{1,4})\b", re.I),
    re.compile(r"\breturn period (?:of |is |= ?)?(?:about |around )?(\d{1,4}) ?(?:years?|yrs?)\b", re.I),
    re.compile(r"\breturn period\b[^.;\n]*?\bis (\d{1,4}) ?(?:years?|yrs?)\b", re.I),
)
_LP3 = re.compile(r"\b(?:lp3|lp-3|lp ?iii|log[- ]?pearson)", re.I)
_GEV = re.compile(r"\bgev\b|generali[sz]ed extreme", re.I)
_DATE_RANGE = re.compile(r"(\d{4}-\d{2}-\d{2})\s*(?:to|until|through|-|and)\s*(\d{4}-\d{2}-\d{2})", re.I)
#: Words in a gauge's name too common to say which gauge a sentence is about.
_GENERIC = frozenset({"river", "near", "above", "below", "creek", "brook", "station", "stream", "gauge", "pump",
                      "with", "from", "upon", "lake", "canal", "water", "little", "great", "north", "south", "east",
                      "west", "upper", "lower", "the", "and", "at"})
#: Numbers in a result that are never flows: periods, counts, tests, places, climate.
_NOT_FLOW = frozenset({"T_years", "n_years", "years", "n", "p_value", "tau", "latitude", "longitude", "year",
                       "n_returned", "n_catalog", "limit", "aridity_index", "precipitation_mm_per_year",
                       "et0_mm_per_year", "temperature_mean_c", "wettest_day_mm"})


def _flow_pool(payloads: list[Any]) -> list[float]:
    """The numbers in the results that are flows (or rates of flow), not periods, counts or test statistics."""
    pool: list[float] = []
    stack: list[tuple[str, Any]] = [("", p) for p in payloads]
    while stack:
        key, item = stack.pop()
        if key in _NOT_FLOW or isinstance(item, bool):
            continue
        if isinstance(item, (int, float)):
            pool.append(float(item))
        elif isinstance(item, dict):
            stack.extend((str(k), v) for k, v in item.items())
        elif isinstance(item, (list, tuple)):
            stack.extend((key, v) for v in item)
    return pool


def _gauges(compacts: list[tuple[str, dict[str, Any]]]) -> list[dict[str, Any]]:
    """Every analysed record in the results, with what names it in prose and its labelled values."""
    out = []
    for name, c in compacts:
        if name in _ANALYSIS_TOOLS:
            g, whole = c, c
        elif name == "anywhere" and isinstance(c.get("glofas"), dict):
            g, whole = c["glofas"], c
        else:
            continue
        if g.get("error"):
            continue
        label = " ".join(str(g[k]) for k in ("name", "station_id") if g.get(k)) or (
            "the GloFAS cell" if name == "anywhere" else "the record")
        tokens = {str(g["station_id"]).lower()} if g.get("station_id") else set()
        for field in ("name", "river"):
            tokens |= {w for w in re.findall(r"[a-z]{4,}", str(g.get(field) or "").lower()) if w not in _GENERIC}
        if name == "anywhere":
            tokens.add("glofas")
        daily = g.get("daily_values") or {}
        fd = g.get("flow_duration") or {}
        ff = g.get("flood_frequency") or {}
        rec = (ff.get("record_max") or {}).get("value")
        values = {
            "q95": [fd.get("q95")], "q50": [fd.get("q50"), daily.get("median")], "q10": [fd.get("q10")],
            "mean": [daily.get("mean")], "median": [daily.get("median"), fd.get("q50")],
            "min": [daily.get("min")], "max": [daily.get("max"), rec],
        }
        levels = {}
        for r in ff.get("return_levels") or []:
            if isinstance(r, dict) and r.get("T_years") is not None:
                ci = r.get("lp3_90ci") if isinstance(r.get("lp3_90ci"), list) else []
                levels[float(r["T_years"])] = {"gev": r.get("gev"), "lp3": r.get("lp3"), "ci": ci}
        pairs = set()
        for d in [whole, g]:
            stack = [d]
            while stack:
                item = stack.pop()
                if isinstance(item, dict):
                    if isinstance(item.get("start"), str) and isinstance(item.get("end"), str):
                        pairs.add((item["start"][:10], item["end"][:10]))
                    stack.extend(item.values())
        out.append({"label": label, "tokens": tokens, "unit": g.get("unit") or "",
                    "values": {k: [float(v) for v in vs if isinstance(v, (int, float)) and not isinstance(v, bool)]
                               for k, vs in values.items()},
                    "levels": levels, "pairs": pairs,
                    "strings": " ".join(s.lower() for s in _strings(whole))})
    # A word two gauges share ("thames" for two gauges on it) names neither.
    for g in out:
        g["tokens"] = {t for t in g["tokens"] if not any(t in h["tokens"] for h in out if h is not g)}
    return out


def _clauses(text: str) -> list[tuple[int, int]]:
    bounds, start = [], 0
    for m in _CLAUSE_BREAK.finditer(text):
        bounds.append((start, m.start()))
        start = m.end()
    bounds.append((start, len(text)))
    return [b for b in bounds if b[1] > b[0]]


class _Who:
    """Which gauge a place in the answer is about: the one its clause names, else the last one named before."""

    def __init__(self, text: str, gauges: list[dict[str, Any]]):
        low = text.lower()
        self.gauges = gauges
        self.mentions: list[tuple[int, int]] = []
        for i, g in enumerate(gauges):
            for t in g["tokens"]:
                for m in re.finditer(r"(?<![\w-])" + re.escape(t) + r"(?![\w-])", low):
                    self.mentions.append((m.start(), i))
        self.mentions.sort()
        self.clauses = _clauses(text)

    def at(self, pos: int) -> int | None:
        if len(self.gauges) == 1:
            return 0
        a, b = next(((a, b) for a, b in self.clauses if a <= pos < b), (pos, pos + 1))
        inside = {i for p, i in self.mentions if a <= p < b}
        if len(inside) == 1:
            return inside.pop()
        if inside:
            return None    # two gauges in one clause: either may be meant
        before = [i for p, i in self.mentions if p < a]
        return before[-1] if before else None

    def clause(self, pos: int) -> tuple[int, int]:
        return next(((a, b) for a, b in self.clauses if a <= pos < b), (pos, pos + 1))


def _num(token: str) -> float | None:
    try:
        return float(token.replace(",", ""))
    except ValueError:
        return None


def _fmt_vals(vals: list[float], unit: str) -> str:
    return " or ".join(f"{_fmt(v)}" for v in vals) + (f" {unit}" if unit else "")


def _label_check(text: str, compacts: list[tuple[str, dict[str, Any]]], words: str) -> list[str]:
    """Each labelled number against its own value, for the gauge its sentence is about (see the section note)."""
    gauges = _gauges(compacts)
    refused: list[str] = []
    blank = _DATE.sub(lambda m: " " * len(m.group(0)), text)
    numbers = [(m.start(), m.end(), _num(m.group(0))) for m in _NUM_AT.finditer(blank)]
    # A gauge id of digits ("USGS-01646500") is a name here, not a number a label could claim.
    low = blank.lower()
    ids = {sid.lower() for sid, _ in _stations(compacts)}
    id_spans = [(m.start(), m.end()) for sid in ids
                for m in re.finditer(r"(?<![\w])" + re.escape(sid) + r"(?![\w])", low)]
    numbers = [(a, b, v) for a, b, v in numbers
               if v is not None and not any(x <= a < y for x, y in id_spans)]
    flows = {a for a, b, _ in numbers if _FLOW_UNIT.match(blank, b)}

    # A number written as a flow must be a flow in the results (or the reader's own): "2 m3/s" where 2 is a
    # return period is refused.
    flow_pool = _flow_pool([c for _, c in compacts]) + _numbers(words)
    if compacts:
        for a, b, v in numbers:
            if a in flows and abs(v) > 1e-9 and not _close(v, flow_pool):
                refused.append(f"{v:g} m3/s is not a flow in the results")
    if not gauges:
        return refused
    who = _Who(text, gauges)

    def name(i: int | None) -> str:
        return gauges[i]["label"] if i is not None else "any gauge in the results"

    def next_number(pos: int, end: int) -> tuple[int, int, float] | None:
        return next(((a, b, v) for a, b, v in numbers if pos <= a < end), None)

    # Statistics under a label: Q95, mean, median, minimum, maximum.
    labels = []
    for kind, rx in _STAT_LABELS:
        for m in rx.finditer(blank):
            labels.append((m.start(), m.end(), f"q{m.group(1)}" if kind == "q" else kind))
    labels.sort()
    for j, (ls, le, kind) in enumerate(labels):
        _, cend = who.clause(ls)
        nxt = next_number(le, cend)
        if nxt is None:
            continue
        a, b, v = nxt
        if any(le <= o[0] < a for o in labels[j + 1:]) or a - le > 80:
            continue   # another label sits between (the number is that one's), or the two are far apart
        filler = blank[le:a]
        if a not in flows and (_OTHER_UNIT.match(blank, b) or not _CONNECTIVE.fullmatch(filler)):
            continue
        i = who.at(a)
        cands = [i] if i is not None else list(range(len(gauges)))
        have = [k for k in cands if gauges[k]["values"].get(kind)]
        if not have:
            continue
        if any(_close(v, gauges[k]["values"][kind]) for k in have):
            continue
        said = kind.upper() if kind.startswith("q") else f"daily {_LABEL_WORDS[kind]}"
        others = [k for k, g in enumerate(gauges) if k not in cands and _close(v, g["values"].get(kind) or [])]
        if i is not None and others:
            refused.append(f"{v:g} is the {said} of {name(others[0])}, not of {name(i)}")
        elif i is not None:
            refused.append(f"{v:g} is not the {said} of {name(i)} "
                           f"({_fmt_vals(gauges[i]['values'][kind][:1], gauges[i]['unit'])})")
        else:
            refused.append(f"{v:g} is not the {said} of any gauge in the results")

    # N-year floods: the flow tied to a period must be that period's return level, by the method named.
    for rx in _PERIODS:
        for m in rx.finditer(blank):
            t = float(m.group(1))
            cstart, cend = who.clause(m.start())
            after = [n for n in numbers if m.end() <= n[0] < cend and n[0] in flows]
            before = [n for n in numbers if cstart <= n[0] < m.start() and n[0] in flows]
            bound = after[0] if after else (before[-1] if before else None)
            if bound is None:
                continue
            a, b, v = bound
            i = who.at(a)
            cands = [i] if i is not None else list(range(len(gauges)))
            rows = [(k, gauges[k]["levels"].get(t)) for k in cands]
            rows = [(k, r) for k, r in rows if r]
            if not rows:
                if not any(gauges[k]["levels"] for k in cands):
                    continue
                refused.append(f"there is no {t:g}-year flood in the results for {name(i)}")
                continue
            sentence = next((s for s in _SENTENCE.split(text) if text.find(s) <= a < text.find(s) + len(s)), text)
            says_lp3, says_gev = bool(_LP3.search(sentence)), bool(_GEV.search(sentence))
            fits = []
            for k, r in rows:
                if r.get("gev") is not None and _close(v, [r["gev"]]):
                    fits.append("gev")
                if r.get("lp3") is not None and _close(v, [r["lp3"]]):
                    fits.append("lp3")
                if any(_close(v, [x]) for x in r.get("ci") or [] if isinstance(x, (int, float))):
                    fits.append("ci")
            k0, r0 = rows[0]
            unit = gauges[k0]["unit"]
            if not fits:
                elsewhere = [f"{tt:g}" for tt, rr in gauges[k0]["levels"].items()
                             if any(isinstance(x, (int, float)) and _close(v, [x])
                                    for x in (rr.get("gev"), rr.get("lp3")))]
                if elsewhere:
                    refused.append(f"{v:g} is the {elsewhere[0]}-year flood, not the {t:g}-year")
                else:
                    gev = f"GEV {_fmt(r0['gev'])}" if r0.get("gev") is not None else ""
                    lp3 = f"LP3 {_fmt(r0['lp3'])}" if r0.get("lp3") is not None else ""
                    refused.append(f"{v:g} is not the {t:g}-year flood of {name(k0)} "
                                   f"({', '.join(x for x in (gev, lp3) if x)} {unit})".replace(" )", ")"))
            elif "gev" not in fits and "lp3" in fits and not says_lp3:
                refused.append(f"{v:g} is the LP3 {t:g}-year flood, and the answer does not say LP3 (the page's "
                               f"figure is the GEV, {_fmt(r0['gev'])} {unit})" if r0.get("gev") is not None else
                               f"{v:g} is the LP3 {t:g}-year flood, and the answer does not say LP3")
            elif "lp3" not in fits and "gev" in fits and says_lp3 and not says_gev:
                refused.append(f"{v:g} is the GEV {t:g}-year flood, not the LP3")

    # Record dates: a date said of one gauge must be that gauge's, and "from A to B" its start and end.
    for m in _DATE_RANGE.finditer(text):
        i = who.at(m.start())
        pair = (m.group(1), m.group(2))
        cands = [i] if i is not None else list(range(len(gauges)))
        if any(pair in gauges[k]["pairs"] for k in cands):
            continue
        others = [k for k, g in enumerate(gauges) if k not in cands and pair in g["pairs"]]
        if i is not None and others:
            refused.append(f"{pair[0]} to {pair[1]} is the record of {name(others[0])}, not of {name(i)}")
        elif i is not None and all(d in gauges[i]["strings"] for d in pair) and gauges[i]["pairs"]:
            s0, e0 = sorted(gauges[i]["pairs"])[0]
            refused.append(f"the record of {name(i)} runs from {s0} to {e0}, not {pair[0]} to {pair[1]}")
    for m in _DATE.finditer(text):
        i = who.at(m.start())
        d = m.group(0)
        if i is None or d in gauges[i]["strings"]:
            continue
        others = [k for k, g in enumerate(gauges) if k != i and d in g["strings"]]
        if others:
            refused.append(f"{d} is in the record of {name(others[0])}, not of {name(i)}")
    return refused


_LIST_COUNT = re.compile(r"\b(?P<n>two|three|four|five|six|seven|eight|nine|ten|\d{1,2})\s+(?:[a-z]+\s+){0,2}"
                         r"(?:gauges|stations|sites)\b", re.I)
_LIST_WORDS = re.compile(r"\b(?:list|which|all)\b[^.?]*\b(?:gauges|stations)\b", re.I)
_COUNT_WORDS = {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}


def wanted_list(question: str) -> int:
    """How many gauges a question asks to be listed ("the five gauges nearest Kingston" is 5); 0 for none."""
    m = _LIST_COUNT.search(question or "")
    if m:
        n = m.group("n").lower()
        return _COUNT_WORDS.get(n) or int(n)
    return 2 if _LIST_WORDS.search(question or "") else 0


def _list_check(text: str, compacts: list[tuple[str, dict[str, Any]]], words: str) -> list[str]:
    """A question that asks for several gauges is answered with several: "five gauges nearest Kingston" with one
    analysed gauge is refused, and the page shows the search's list instead."""
    question = (words or "").split("\n\nContext:")[0]
    want = wanted_list(question)
    rows = [r for name, c in compacts if name == "find_stations" for r in c.get("stations") or []
            if isinstance(r, dict)]
    if want < 2 or not rows:
        return []
    low = text.lower()
    named = sum(1 for r in rows if (r.get("station_id") and str(r["station_id"]).lower() in low)
                or (len(str(r.get("name") or "")) >= 4 and str(r["name"]).lower() in low))
    need = min(want, len(rows))
    if named < need:
        return [f"the question asks for {want} gauges and the answer names {named} of those the search found"]
    return []


def lock_answer(answer: str, results: list[dict[str, Any]], words: str = "") -> dict[str, Any]:
    """Hold an on-device answer to this question's tool results.

    ``results`` are ``{"name", "arguments", "compact", "ok"}``, one per tool call made for this question (and
    only this one: a fresh session per question means nothing else could have been seen). ``words`` is the
    question with the context line the page added.

    Every number, date, flow-duration label (Q95, Q10) and gauge id in the answer must be in the results or in
    the words, allowing for rounding; a gauge id must sit next to its own gauge's name; every trend or
    significance word must agree with the Mann-Kendall result. A labelled number must be that label's value for
    the gauge its clause is about (:func:`_label_check`: Q95 its flow-duration Q95, an N-year flood its return
    level for N by the method named, a mean or a record date its own field), and a number written in m3/s a
    flow. A question asking for several gauges must be answered with several (:func:`_list_check`).

    Returns ``{"ok", "refused", "facts", "notes"}``: ``refused`` says why in short phrases, ``facts`` are lines
    built from the results (what the page shows when the answer is refused), ``notes`` say what the reader
    should know either way.
    """
    text = normalise(answer or "")
    words_n = normalise(words or "")
    ok_results = [r for r in results or [] if r.get("ok") and isinstance(r.get("compact"), dict)]
    compacts = [(str(r.get("name")), r["compact"]) for r in ok_results]
    refused: list[str] = []

    # Dates, whole: "1930-03-01" must be a date one of the results (or the reader) wrote.
    strings = [s.lower() for _, c in compacts for s in _strings(c)] + [words_n.lower()]
    for d in dict.fromkeys(_DATE.findall(text)):
        if not any(d in s for s in strings):
            refused.append(f"the date {d} is in no result for this question")
    body = _LIST_MARK.sub(" ", _DATE.sub(" ", text))

    # Flow-duration labels: Q10 is a point of the flow-duration curve, and only one the results hold.
    fdc_keys = {k for _, c in compacts for holder in (c, c.get("glofas") or {}) if isinstance(holder, dict)
                for k in (holder.get("flow_duration") or {})}
    for m in dict.fromkeys(_Q_LABEL.findall(body)):
        if f"q{m}" not in fdc_keys and f"q{m}" not in words_n.lower():
            refused.append(f"Q{m} is in no result for this question")

    # Gauge ids with letters in them, which the number check cannot see.
    for token in dict.fromkeys(_ALNUM_ID.findall(body)):
        if not any(token.lower() in s for s in strings):
            refused.append(f"the id {token} is in no result for this question")
    refused += _swapped_ids(text, _stations(compacts))

    # Numbers: the results and the reader's words, with rounding; a percentage may be a fraction in the result.
    pool = _pool([c for _, c in compacts], words_n)
    plain = _SQUARED_UNIT.sub(" ", _EXPONENT_UNIT.sub(" ", body))
    percents = {float(m.replace(",", "")) for m in re.findall(r"(-?\d[\d,]*\.?\d*)\s*%", plain)}
    # "68.6 W" is the longitude -68.6: the compass letter carries the sign.
    compass = {float(m.group(1)) for m in _COMPASS.finditer(plain) if m.group(2) in "SW"}
    unsupported = []
    for n in _numbers(plain):
        if n in _CONVENTIONS or abs(n) < 1e-9 or (n in percents and n / 100 in _CONVENTIONS):
            continue   # p < 0.05, a 90 % interval: conventions, not claims about the data
        if float(n).is_integer() and 1800 <= n <= 2100:
            ok = n in pool
        else:
            ok = (_close(n, pool) or (n in compass and _close(-n, pool))
                  or (n in percents and _close(n / 100, pool)))
        if not ok and n not in unsupported:
            unsupported.append(n)
    if unsupported:
        listed = ", ".join(f"{n:g}" for n in unsupported[:5])
        refused.append(f"{listed} {'is' if len(unsupported) == 1 else 'are'} in no result for this question"
                       if compacts else f"no tool ran for this question, so {listed} cannot come from data")

    refused += _trend_check(text, compacts)
    refused += _label_check(text, compacts, words_n)
    refused += _list_check(text, compacts, words_n)

    notes = []
    for r in ok_results:
        near = (r.get("arguments") or {}).get("near")
        if r.get("name") == "find_stations" and isinstance(near, (list, tuple)) and len(near) == 2:
            given = _numbers(words_n)
            if not all(isinstance(v, (int, float)) and _close(float(v), given) for v in near):
                notes.append(f"The search was near {near[0]}, {near[1]}, a point the model chose; your words did "
                             "not give it, so 'nearest' is nearest to that point.")
    lines = [line for name, c in compacts for line in facts(name, c)]
    return {"ok": not refused, "refused": list(dict.fromkeys(refused))[:6], "facts": lines[:12], "notes": notes}
