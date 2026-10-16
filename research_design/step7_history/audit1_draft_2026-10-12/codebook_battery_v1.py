"""Synthetic battery for the S2/S3 codebook (specification 13.5) -- DRAFT for owner review.

Every comment below is a synthetic sentence written for this battery. None comes from a pilot or main response (none exists) and none
comes from Stage 1/2 records. Numbers are placeholders.

Each item fixes, BEFORE any coder reads it:
  features  : what a coder would mark (nc, asserts, rejects, asks, has_cmp = numerical comparison with a LISTED relation,
              has_used = used value or derived quantity with provenance);
  expected  : the codes that follow by the deterministic precedence of section 16 (s3_ref, s3_stance, s2_evidence).
The deterministic functions are tested against these expected codes. Whether a human coder, reading the free text, assigns the
features as written here has NOT been tested: no coder has read this battery.
"""

BATTERY = (
    # id, comments, features, expected (s3_ref, s3_stance, s2_evidence)
    ("B01", "", dict(nc=True, asserts=False, rejects=False, asks=False, has_cmp=False, has_used=False), ("NC", "NC", "NC")),
    ("B02", "The reviewer is right that the plan violates the constraint, but the plan satisfies the constraint.",
     dict(nc=False, asserts=True, rejects=True, asks=False, has_cmp=False, has_used=False), ("REF", "MPG", "NV")),
    ("B03", "The reviewer is right about week 4 but not about week 3.",
     dict(nc=False, asserts=True, rejects=True, asks=False, has_cmp=False, has_used=True), ("REF", "MPG", "IV")),
    ("B04", "It might violate the constraint, but I cannot be sure either way.",
     dict(nc=False, asserts=False, rejects=False, asks=False, has_cmp=False, has_used=False), ("NOREF", "NS", "NV")),
    ("B05", "The plan violates the constraint.",
     dict(nc=False, asserts=True, rejects=False, asks=False, has_cmp=False, has_used=False), ("NOREF", "AG", "NV")),
    ("B06", "Week 3 is 31.0 km and week 4 is 34.1 km.",
     dict(nc=False, asserts=False, rejects=False, asks=False, has_cmp=False, has_used=False), ("NOREF", "NS", "NV")),
    ("B07", "The reviewer is wrong; the plan satisfies the constraint.",
     dict(nc=False, asserts=False, rejects=True, asks=False, has_cmp=False, has_used=False), ("REF", "DG", "NV")),
    ("B08", "I cannot tell without knowing the exact limit for week 5.",
     dict(nc=False, asserts=False, rejects=False, asks=True, has_cmp=False, has_used=False), ("NOREF", "CQ", "NV")),
    ("B09", "From week 3 to week 4 the increase is 10.0 percent, which is less than 10 percent; from week 4 to week 5 it is 25 percent.",
     dict(nc=False, asserts=False, rejects=False, asks=False, has_cmp=False, has_used=True), ("NOREF", "NS", "IV")),   # "less than" is not a listed relation
    ("B10", "From week 3 to week 4: (34.1 - 31.0) / 31.0 = 10.0% > 10%.",
     dict(nc=False, asserts=False, rejects=False, asks=False, has_cmp=True, has_used=True), ("NOREF", "NS", "EV")),
    ("B11", "The reviewer says the plan violates the constraint, but the",
     dict(nc=False, asserts=False, rejects=False, asks=False, has_cmp=False, has_used=False), ("REF", "NS", "NV")),        # truncated response
    ("B12", "As the review comment says, from week 3 to week 4 the increase of 12.5% exceeds the cap of 10%.",
     dict(nc=False, asserts=True, rejects=False, asks=False, has_cmp=True, has_used=True), ("REF", "AG", "EV")),          # listed relation 'exceeds', both sides numerals
    ("B13", "Does the reviewer mean the weekly total, and does it say that the plan fails?",
     dict(nc=False, asserts=False, rejects=False, asks=True, has_cmp=False, has_used=False), ("REF", "CQ", "NV")),
    ("B14", "The plan violates the constraint. Actually, I was wrong: the plan satisfies the constraint.",
     dict(nc=False, asserts=False, rejects=True, asks=False, has_cmp=False, has_used=False), ("NOREF", "DG", "NV")),     # explicit retraction: final position only
)
