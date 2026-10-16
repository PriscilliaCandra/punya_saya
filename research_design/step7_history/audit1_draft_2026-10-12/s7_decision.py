"""Step 7 decision script (specification sections 10, 13.6, 14) -- DRAFT for owner review.

It computes, from counts only, the pilot round outcome (13.6), builds the canonical call list (10), derives the seed from the
script-stamped UTC date (10), shuffles the canonical order once with random.Random(seed).shuffle (10), and builds the
decision record (10). It never reads response content: its inputs are integers.

Nothing runs at import. The clock is injectable so that tests are deterministic; in real use the clock is the system UTC clock
(the seed is script-stamped, never typed). write_decision_record() refuses to overwrite.

Open points marked in the code are specification gaps, not choices made here:
  GAP-1  the denominator of the "UNP share" is not defined by the specification text; `round_outcome` takes it as an explicit
         argument (`n_calls`) and the report states it; the draft convention is "all calls of the round" (UNP stays in
         every denominator, section 13.4).
  GAP-2  the specification does not say which outcome applies when a round meets both the FAIL-S and the FAIL-U condition;
         `round_outcome` returns the label "FAIL-S+FAIL-U" and decides nothing.
"""
import datetime
import hashlib
import json
import os
import platform
import random
from fractions import Fraction

CONDITION_TOKENS = ("A", "B", "C", "D")
STRUCTURAL = ("SF1", "SF2", "SF3", "SF4", "SF5")


def round_outcome(counts, n_calls, f_S, theta_unp):
    """Round outcome by counts only (13.6). counts: dict with SF1..SF5 and UNP (non-negative ints);
    f_S int; theta_unp Fraction/str/int. Returns a dict with the outcome and the quantities used."""
    for k in STRUCTURAL + ("UNP",):
        if not isinstance(counts.get(k), int) or counts[k] < 0:
            raise ValueError(f"count {k} missing or invalid")
    if not isinstance(n_calls, int) or n_calls <= 0:
        raise ValueError("n_calls must be a positive int")
    theta = Fraction(theta_unp)
    hard = counts["SF2"] + counts["SF3"] + counts["SF5"]
    soft = counts["SF1"] + counts["SF4"]
    unp_share = Fraction(counts["UNP"], n_calls)
    fail_s = hard > 0 or soft > f_S
    fail_u = unp_share > theta
    if fail_s and fail_u:
        label = "FAIL-S+FAIL-U"          # GAP-2: precedence not defined by the specification
    elif fail_s:
        label = "FAIL-S"
    elif fail_u:
        label = "FAIL-U"
    else:
        label = "PASS"
    return {"outcome": label, "fail_s": fail_s, "fail_u": fail_u, "hard_SF2_SF3_SF5": hard, "soft_SF1_SF4": soft,
            "unp_share": str(unp_share), "unp_share_denominator": n_calls, "f_S": f_S, "theta_unp": str(theta)}


def main_run_halt(consecutive_structural_failures, completed_calls, structural_failures, c_stop, calls_min_main, theta_main):
    """Main-run monitor rule (13.8): halt if the consecutive structural failures reach c_stop, or if, after at least
    calls_min_main completed calls, the cumulative share of SF1-SF5 exceeds theta_main."""
    if consecutive_structural_failures >= c_stop:
        return True
    if completed_calls >= calls_min_main and completed_calls > 0:
        return Fraction(structural_failures, completed_calls) > Fraction(theta_main)
    return False


def call_list(template_ids, R):
    """Canonical call list (10): (template, condition, repetition) triples, templates in the given canonical order,
    condition tokens A<B<C<D, repetition 1..R; one line '<template_id>,<token>,<repetition>' per triple, LF-joined, final LF."""
    if not isinstance(R, int) or R < 1:
        raise ValueError("R must be a positive int")
    lines = [f"{t},{c},{r}" for t in template_ids for c in CONDITION_TOKENS for r in range(1, R + 1)]
    return "\n".join(lines) + "\n"


def seed_from_clock(now_utc):
    """YYYYMMDD of the script-stamped UTC date as an integer (10)."""
    if now_utc.tzinfo is None or now_utc.utcoffset() != datetime.timedelta(0):
        raise ValueError("the clock value must be timezone-aware UTC")
    return int(now_utc.strftime("%Y%m%d"))


def shuffled_order(call_list_text, seed):
    """The one shuffle (10): random.Random(seed).shuffle over the canonical lines."""
    lines = call_list_text.rstrip("\n").split("\n")
    random.Random(seed).shuffle(lines)
    return lines


def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()


def build_decision_record(*, pilot_counts, round_result, fz_hash, script_path, call_list_text, clock=None):
    """Decision record (10): pilot structural counts and UNP share, FZ hash, decision-script hash, script-stamped UTC
    timestamp, computed seed, interpreter version, SHA-256 and length of the canonical call list."""
    now = clock() if clock else datetime.datetime.now(datetime.timezone.utc)
    seed = seed_from_clock(now)
    with open(script_path, "rb") as fh:
        script_hash = sha256_hex(fh.read())
    data = call_list_text.encode("ascii")
    return {
        "pilot_structural_counts": dict(pilot_counts),
        "round_result": round_result,
        "fz_hash": fz_hash,
        "decision_script_sha256": script_hash,
        "utc_timestamp": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "seed": seed,
        "interpreter_version": platform.python_version(),
        "call_list_sha256": sha256_hex(data),
        "call_list_length_bytes": len(data),
        "call_list_lines": call_list_text.count("\n"),
    }


def write_decision_record(record, path):
    if os.path.exists(path):
        raise FileExistsError("decision record exists; nothing is overwritten")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(json.dumps(record, indent=2, sort_keys=True) + "\n")
