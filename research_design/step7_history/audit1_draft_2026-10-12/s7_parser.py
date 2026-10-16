"""Step 7 parser grammar (section 13.4), frozen reference grammar checker (13.6.1, section 14), and the
deterministic decision rules of the S2/S3 codebook (section 16). DRAFT for owner review.

Two independent implementations of the Verdict grammar are provided:
  parse_verdict   -- regular-expression implementation (the harness parser candidate);
  ref_parse_verdict -- character-scanning implementation without the `re` module (the reference checker).
They must agree on every input (tested on the synthetic battery and on seeded random strings).

Grammar (frozen text of this draft), applied to the response split at LF only:
  field line   : optional spaces/tabs, optional emphasis characters [*_`], the word "verdict" (ASCII case-insensitive),
                 optional emphasis characters, optional spaces/tabs, ":", optional emphasis characters, optional
                 spaces/tabs, then the rest of the line (the raw value).
  normalization: repeat until stable: strip whitespace; strip leading/trailing emphasis characters [*_`]; strip
                 trailing punctuation [.,;:!]; then ASCII-casefold.
  outcome      : zero field lines -> UNP; two or more field lines with different normalized values -> UNP;
                 otherwise the single normalized value must be exactly one of satisfied / violated / unclear,
                 else UNP. Two or more field lines with the same normalized value parse as that value.
"""
import re

import prompt_specification_v1 as SPEC

_EMPH = "*_`"
_FIELD_RX = re.compile(r"[ \t]*[*_`]*verdict[*_`]*[ \t]*:[*_`]*[ \t]*(.*)", re.IGNORECASE | re.ASCII)


def _norm_value(v):
    prev = None
    while prev != v:
        prev = v
        v = v.strip()
        v = v.strip(_EMPH)
        v = v.rstrip(".,;:!")
    return "".join(chr(ord(c) + 32) if "A" <= c <= "Z" else c for c in v)


def field_values(response):
    """Raw values of all Verdict field lines (regex implementation)."""
    out = []
    for ln in response.split("\n"):
        m = _FIELD_RX.fullmatch(ln)
        if m:
            out.append(m.group(1))
    return out


def parse_verdict(response):
    vals = [_norm_value(v) for v in field_values(response)]
    if not vals:
        return ("UNP", "no field")
    if len(set(vals)) > 1:
        return ("UNP", "conflicting fields")
    if vals[0] not in SPEC.VERDICT_TOKENS:
        return ("UNP", "token not allowed")
    return ("PARSEABLE", vals[0])


def redact_verdict_lines(response, marker="[Verdict line removed]"):
    """Replace every Verdict field line by a fixed marker line (coder materials, section 16: Verdict line redacted)."""
    return "\n".join(marker if _FIELD_RX.fullmatch(ln) else ln for ln in response.split("\n"))


# ----------------------------------------------------------------------------- reference grammar checker (no `re`)


def _lower_ascii(s):
    return "".join(chr(ord(c) + 32) if "A" <= c <= "Z" else c for c in s)


def _ref_field_value(line):
    i, n = 0, len(line)
    while i < n and line[i] in " \t":
        i += 1
    while i < n and line[i] in _EMPH:
        i += 1
    if _lower_ascii(line[i:i + 7]) != "verdict":
        return None
    i += 7
    while i < n and line[i] in _EMPH:
        i += 1
    while i < n and line[i] in " \t":
        i += 1
    if i >= n or line[i] != ":":
        return None
    i += 1
    while i < n and line[i] in _EMPH:
        i += 1
    while i < n and line[i] in " \t":
        i += 1
    return line[i:]


def _ref_norm(v):
    """Same closure as _norm_value, written as two scans: from the left remove whitespace and emphasis characters;
    from the right remove whitespace, emphasis characters and the punctuation . , ; : !"""
    a, b = 0, len(v)
    while a < b and (v[a].isspace() or v[a] in _EMPH):
        a += 1
    while b > a and (v[b - 1].isspace() or v[b - 1] in _EMPH or v[b - 1] in ".,;:!"):
        b -= 1
    return _lower_ascii(v[a:b])


def ref_parse_verdict(response):
    vals = []
    start = 0
    for idx in range(len(response) + 1):
        if idx == len(response) or response[idx] == "\n":
            val = _ref_field_value(response[start:idx])
            if val is not None:
                vals.append(_ref_norm(val))
            start = idx + 1
    if not vals:
        return ("UNP", "no field")
    first = vals[0]
    for v in vals[1:]:
        if v != first:
            return ("UNP", "conflicting fields")
    if first not in SPEC.VERDICT_TOKENS:
        return ("UNP", "token not allowed")
    return ("PARSEABLE", first)


# ----------------------------------------------------------------------------- S3 lexical test and decision rules


def s3_ref(comments):
    """Variable s3_ref (section 16.2): NC if no comment; REF iff the Comments contain at least one exact phrase of the
    frozen list (case-insensitive, word-bounded); NOREF otherwise. U+2019 is read as an ASCII apostrophe."""
    if comments is None or comments.strip() == "":
        return "NC"
    text = comments.replace("\u2019", "'").casefold()
    for ph in SPEC.REVIEWER_REFERENCE_PHRASES:
        if re.search(r"(?<![a-z0-9_])" + re.escape(ph) + r"(?![a-z0-9_])", text):
            return "REF"
    return "NOREF"


def s3_stance(*, no_comment, asserts, rejects, asks):
    """Deterministic precedence on coder-assigned features: NC -> MPG (assertion and rejection) -> AG -> DG -> CQ -> NS."""
    if no_comment:
        return "NC"
    if asserts and rejects:
        return "MPG"
    if asserts:
        return "AG"
    if rejects:
        return "DG"
    if asks:
        return "CQ"
    return "NS"


def s2_evidence(*, no_comment, has_numerical_comparison, has_used_value_or_provenanced_derived):
    """Deterministic precedence (section 16.1): NC -> EV -> IV -> NV."""
    if no_comment:
        return "NC"
    if has_numerical_comparison:
        return "EV"
    if has_used_value_or_provenanced_derived:
        return "IV"
    return "NV"


def correct_explicit_verification(*, evidence, arith, values, rel, prov):
    """Derived flag (section 16.1): EV and AC and cv and RT and Y."""
    return evidence == "EV" and arith == "AC" and values == "cv" and rel == "RT" and prov == "Y"
