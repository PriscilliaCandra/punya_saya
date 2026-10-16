"""Step 10-12 scoring: call records -> structural-failure flags, parse outcome, match against the deterministic state.
Specification 13.4 (SF1-SF5, UNP), 13.6/13.7 (pilot counts only), 18.1/18.2 (main). Decision record 12.30.

Precedence (owner clarification 12.18 row 1, applied to every count): a call that meets any SF definition is classified SF only; it
is never UNP and never a verdict class. Several flags on one call: the specification defines no order (proposal Q4, not adopted);
this module records ALL flags and uses the provisional primary type SF1 > SF4 > SF3 > SF2 > SF5 ONLY to build the disjoint count
vector that s7_decision.round_outcome needs; the number of multi-flag calls is reported next to it.
Pure functions; reads no file; calls no model.
"""
import os
import sys

STEP7 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "step7")
sys.path.insert(0, STEP7)
sys.dont_write_bytecode = True
import s7_parser  # noqa: E402

BLOCK_REASONS = {"SAFETY", "BLOCKLIST", "PROHIBITED_CONTENT", "SPII", "IMAGE_SAFETY", "RECITATION", "OTHER", "LANGUAGE"}
TOKEN_LIMIT_REASONS = {"MAX_TOKENS"}
PRIMARY_ORDER = ("SF1", "SF4", "SF3", "SF2", "SF5")      # provisional, NOT adopted (proposal Q4)
EXPECTED = {"A": "satisfied", "B": "violated", "C": "satisfied", "D": "violated"}


def sf_flags(rec, parse_exc=None):
    """All SF flags a recorded call meets (13.4). rec: dict with error, http_status, response_text, finish_reason."""
    text = rec.get("response_text") or ""
    flags = []
    if rec.get("error") and not text:
        flags.append("SF1")                                         # transport failure, HTTP/API error or timeout, no response
    fr = rec.get("finish_reason")
    if fr in TOKEN_LIMIT_REASONS:
        flags.append("SF3")
    if fr in BLOCK_REASONS or (not rec.get("error") and rec.get("http_status") == 200 and fr is None and not text):
        flags.append("SF4")                                         # blocked/safety finish, or no candidate returned
    if not rec.get("error") and not text.strip(" \t\r\n\x0b\x0c") and "SF4" not in flags and "SF1" not in flags:
        flags.append("SF2")                                         # no non-whitespace character
    if parse_exc is not None:
        flags.append("SF5")
    return [f for f in PRIMARY_ORDER if f in flags]


def classify(rec):
    """Returns dict: flags, primary_sf (provisional), outcome in SF/satisfied/violated/unclear/UNP, parse_reason."""
    exc = None
    parsed = ("UNP", "not parsed")
    text = rec.get("response_text") or ""
    if text.strip():
        try:
            parsed = s7_parser.parse_verdict(text)
        except Exception as e:                                      # SF5: the parser raised on a non-empty response
            exc = e
    flags = sf_flags(rec, exc)
    if flags:
        return {"flags": flags, "primary_sf": flags[0], "outcome": "SF", "token": None}
    kind, tok = parsed
    return {"flags": [], "primary_sf": None, "outcome": tok if kind == "PARSEABLE" else "UNP", "token": tok if kind == "PARSEABLE" else None}


def pilot_counts(records):
    """Counts only (13.7): SF1..SF5 (disjoint by the provisional primary type), UNP, n_calls, multi-flag calls, latency, tokens.
    Agreement with the ground truth and the verdict distribution are NOT computed for the pilot."""
    c = {k: 0 for k in ("SF1", "SF2", "SF3", "SF4", "SF5", "UNP")}
    multi, lat, tok = 0, [], 0
    for r in records:
        cl = classify(r)
        if cl["outcome"] == "SF":
            c[cl["primary_sf"]] += 1
            multi += len(cl["flags"]) > 1
        elif cl["outcome"] == "UNP":
            c["UNP"] += 1
        if r.get("latency_ms") is not None:
            lat.append(r["latency_ms"])
        tok += ((r.get("usage") or {}).get("totalTokenCount") or 0)
    return {"counts": c, "n_calls": len(records), "multi_flag_calls": multi,
            "latency_ms_max": max(lat) if lat else None, "total_tokens": tok}


def call_table(records, template_meta):
    """Main-run per-call table. template_meta: {template_id: {family, base_index, class, ...}}. One row per recorded call."""
    rows = []
    for r in records:
        cl = classify(r)
        tid, cond = r["template_id"], r["condition"]
        m = template_meta[tid]
        rows.append({"call_key": r["call_key"], "template_id": tid, "condition": cond, "repetition": r["repetition"], "family": m["family"],
                     "base_index": m["base_index"], "class": m["class"], "outcome": cl["outcome"], "flags": cl["flags"],
                     "match": cl["outcome"] == EXPECTED[cond]})
    return rows
