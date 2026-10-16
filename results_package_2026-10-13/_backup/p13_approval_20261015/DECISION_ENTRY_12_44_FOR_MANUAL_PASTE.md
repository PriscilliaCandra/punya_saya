# Draft decision entry 12.44: ratification of exception classes for resume (FOR THE OWNER TO REVIEW; NOT ENTERED; NO CLASS IS RATIFIED)

This file is a draft in the style of `DECISION_ENTRY_12_38_FOR_MANUAL_PASTE.md`. It is not part of the decision record. The "Recommended" column is the assistant's evaluation (see `MD08_OWNER_DECISION_PACKAGE_2026-10-15.md` section 2 and `MD08_EXCEPTION_AUDIT_2026-10-15.md`); the "Owner decision" column is blank on purpose. Until the owner fills it in and the entry is recorded in `research_design/STEP3_OWNER_DECISIONS_RECORD_DRAFT.md`, `RATIFIED_TRANSPORT_ERROR_CLASSES` stays empty and no resume is available. Applying a recorded ratification is a separate step: set the constant in `s10_resume.py` to the ratified names (backup first), update the tests, rerun the Step 10 suite and the full check, and re-record the 31 hashes.

### 12.44 Ratification of exception classes for resume, <date written by the owner> (records the owner's decisions; no advisor approval)

Scope of a ratification: a class listed as ratified makes (a) a halt whose SF1 records carry only ratified classes resumable and (b) a trailing failure of that class a valid basis for the process-death contract, in both cases only with no HTTP status, SF1 alone, no response text, the whole run clean (option A1, entry 12.43) and the owner's written authorization. The HTTP status allow-list stays empty. A recorded `URLError.reason` category (entry 12.43) gives no eligibility. Ratification does not say that the provider did not process the lost request, and does not say that the cause of the failure is gone.

| # | Class | Recommended (assistant, not binding) | Owner decision (ratified / not ratified / deferred) | Reason (owner) |
|---|---|---|---|---|
| 1 | `TimeoutError` | RATIFY | | |
| 2 | `timeout` | REJECT | | |
| 3 | `URLError` | DEFER | | |
| 4 | `ConnectionError` | REJECT | | |
| 5 | `ConnectionResetError` | RATIFY | | |
| 6 | `ConnectionAbortedError` | DEFER | | |
| 7 | `ConnectionRefusedError` | REJECT | | |
| 8 | `BrokenPipeError` | DEFER | | |
| 9 | `RemoteDisconnected` | RATIFY | | |
| 10 | `IncompleteRead` | RATIFY | | |
| 11 | `gaierror` | REJECT | | |
| 12 | `SSLError` | REJECT | | |
| 13 | `SSLEOFError` | DEFER | | |
| 14 | `SSLZeroReturnError` | DEFER | | |

Classes not marked "ratified" by the owner are not ratified. Not authorized by this entry: a resume of any run, the pilot, the main run, any provider call, the code-freeze declaration, the final freeze manifest.
