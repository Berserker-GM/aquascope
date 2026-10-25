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
        "source", "station_id", "name", "agency", "variable", "unit", "start", "end", "years", "n", "modelled",
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
_Q_LABEL = re.compile(r"\bQ(\d{1,2})\b")
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


def lock_answer(answer: str, results: list[dict[str, Any]], words: str = "") -> dict[str, Any]:
    """Hold an on-device answer to this question's tool results.

    ``results`` are ``{"name", "arguments", "compact", "ok"}``, one per tool call made for this question (and
    only this one: a fresh session per question means nothing else could have been seen). ``words`` is the
    question with the context line the page added.

    Every number, date, flow-duration label (Q95, Q10) and gauge id in the answer must be in the results or in
    the words, allowing for rounding; a gauge id must sit next to its own gauge's name; every trend or
    significance word must agree with the Mann-Kendall result. Returns ``{"ok", "refused", "facts", "notes"}``:
    ``refused`` says why in short phrases, ``facts`` are lines built from the results (what the page shows when
    the answer is refused), ``notes`` say what the reader should know either way.
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
