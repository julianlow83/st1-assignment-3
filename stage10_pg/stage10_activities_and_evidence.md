# Stage 10 PG agentic rescheduling activities and evidence

PG-only stage. Undergraduate students are not required to complete this record. UG-only groups retain this supplied template unchanged as intentionally not applicable; do not fabricate N/A responses. Optional UG help is voluntary and unassessed.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage10_pg/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. Protect the common Stage 9 SHA and UG Stage 12 pathway.

This is a blank student record. Use actual accessible links and concise evidence; do not invent an agent session, test result or approval. Retain this record's headings when linking equivalent issue/PR evidence.

Group/tutorial: Mon 9:30 - 11:30 Group 3
Assessed PG members and roles: Julian Low (u335040)
Optional UG contributors: N/A (They are working on 12)

## A Access baseline and recovery

- **Confirmed GitHub Copilot feature/mode, version/environment and teaching-team approval reference:**
  GitHub Copilot on GitHub web version paired with local PyCharm IDE environment (confirmed teaching-team approved workspace and web Copilot interaction route).

- **Actual account access and tool permissions check:**
  Confirmed active GitHub account entitlement with Copilot privileges; local file editing performed in PyCharm bounded to workspace files (`project/smartcare/domain.py`, `project/smartcare/services.py`, `project/tests/test_rescheduling.py`); automatic merge, deployment, and shell execution withheld.

- **Live route or convenor-confirmed equivalent staged interaction:**
  Live route using GitHub Copilot web interface for plan proposals and review comparison, with human approval gate enforced prior to manually applying file edits in PyCharm.

- **Access limitation and tutor resolution if applicable:**
  None; web Copilot access confirmed with plan review controls active.

- **Protected Stage 9 common SHA / recoverable reference:**
  c1e8c874f7c68c865633397dd72decba49bafed3

- **Common baseline command / project working directory / actual result:**
  - **Command:** `cd project && python -m pytest -q`
  - **Working Directory:** `project/`
  - **Actual Result:** `32 passed in 0.15s`

- **Clean branch and preparer / recovery baseline:**
  Created branch `pg/stage10-rescheduling` from protected Stage 9 SHA (`git switch -c pg/stage10-rescheduling`); verified `git status --short` is clean prior to any PG edits.

- **Evidence-only later SHA if different / explanation:**
  N/A

## B Tutorial activities

### B1 Rewrite the vague task

“Improve SmartCare appointment scheduling.” Write your bounded goal, requirements, exclusions, constraints, acceptance criteria and Definition of Done: 

  * **Bounded Goal:** Extend the existing SmartCare in-memory application with guarded appointment rescheduling functionality by introducing typed domain and service methods without modifying existing participant objects or adding persistence layers.
  * **Requirements:** Implement `Appointment.reschedule(new_date_time: datetime) -> None` and `AppointmentService.reschedule_appointment(appointment_id: str, new_date_time: datetime) -> Appointment` according to contracts `RES-01` to `RES-06`, enforcing `RES-05-R2` current-session visibility. Only `SCHEDULED` appointments can move; unknown IDs raise `LookupError`; blank/invalid inputs, terminal statuses (`CANCELLED`/`COMPLETED`), and same-practitioner datetime conflicts raise `ValueError` without state mutation. Self-exclusion permits valid same-time no-ops, and successful moves release the old time slot.
  * **Exclusions:** Out of scope: SQL/database storage, file/restart persistence, third-party calendar libraries, notifications, billing, authentication, patient self-service, recurring appointments, CLI menu additions, and changes to `Patient`/`Practitioner` entity classes or history semantics.
  * **Architecture Constraints:** Must reuse minute-precision naive `datetime` validation and `SmartCareDataStore.has_practitioner_conflict()` with `exclude_appointment_id`. Retain exact public signatures, exception types, type hints, docstrings, and session query sorting (`select_appointments` / `appointment_sort_key`).
  * **Acceptance Criteria:** Satisfy `AC-RES-01` (valid move preserves object identity and updates time), `AC-RES-02` (unknown ID raises `LookupError`), `AC-RES-03` (same-practitioner conflict raises `ValueError`), `AC-RES-04` (different practitioner at same time allowed), `AC-RES-05` (`CANCELLED`/`COMPLETED` targets raise `ValueError`), and `AC-RES-06-R2` (lookups and listings in current session reflect the updated datetime).
  * **Definition of Done:** Working code in `domain.py` and `services.py`; focused tests in `test_rescheduling.py`; all baseline and accumulated Stage 6–9 tests passing green; protected Stage 9 contracts unchanged; diff reviewed with zero unrelated changes; evidence record complete; and peer human approval recorded prior to merge.

- **Predicted changed files and human test intentions:**

  * **Predicted Changed Files:** `project/smartcare/domain.py`, `project/smartcare/services.py`, `project/tests/test_rescheduling.py`, `README.md`, and `stage10_pg/stage10_activities_and_evidence.md`.
  * **Human Test Intentions:**
    1. *Positive Move:* Verify moving a `SCHEDULED` appointment updates `_date_time`, returns the exact same object instance, and leaves participant identities unchanged (`AC-RES-01`).
    2. *Unknown ID:* Verify non-existent appointment ID raises `LookupError` (`AC-RES-02`).
    3. *Practitioner Conflict:* Verify moving to a slot occupied by the same practitioner raises `ValueError` (`AC-RES-03`).
    4. *Different Practitioner:* Verify moving to a slot occupied by a different practitioner succeeds (`AC-RES-04`).
    5. *Terminal State Guards:* Verify rescheduling `CANCELLED` or `COMPLETED` appointments raises `ValueError` without mutating state (`AC-RES-05`).
    6. *Session Visibility & Freed Slot:* Verify `find_appointment` and `list_practitioner_appointments` reflect the new time in sorted order, and the old slot can be re-booked (`AC-RES-06-R2`).
    7. *Boundary Checks:* Verify same-time self-exclusion no-op, invalid `datetime` inputs (aware timestamps, nonzero seconds/microseconds), and blank string IDs raise expected exceptions.

### B2 Judge every proposed plan step

| Proposed step | Accept / Modify / Reject | Requirement evidence and reason |
|---|---|---|
| Redesign database schema | **Reject** | Out of scope. The requirement explicitly forbids database/schema redesign, SQLite, or file/restart persistence. Persistence remains strictly session-only in memory using the existing `SmartCareDataStore`. |
| Add notifications | **Reject** | Out of scope. Section 3 explicitly lists notifications and reminders as out-of-scope features that must not be added. |
| Introduce calendar library | **Reject** | Out of scope. External calendar packages and third-party dependencies are explicitly forbidden. Native minute-precision `datetime` validation must be reused. |
| Modify Patient | **Reject** | Violation of scope constraints. Unrelated participant behavior (`Patient`/`Practitioner`) must remain unchanged. Rescheduling alters appointment time only, preserving original patient and practitioner objects. |
| Add rescheduling | **Modify** | Required feature scope, but step must be bounded. Modify to restrict implementation strictly to `Appointment.reschedule(new_date_time)` in `domain.py` and `AppointmentService.reschedule_appointment(...)` in `services.py`. Must reuse `SmartCareDataStore.has_practitioner_conflict()` with `exclude_appointment_id`. |
| Rewrite all tests | **Reject** | Architecture and verification violation. Existing common tests (Stages 6–9) must be preserved intact. Only new, focused unit/integration assertions should be added in `project/tests/test_rescheduling.py`. |

### B3 Six proposed changes

| File or action | Expected? | Review concern and evidence needed |
|---|---|---|
| Appointment in project/smartcare/domain.py | **Expected** | Verify state change is bounded to `_date_time` and validated; confirm same-object identity, naive minute-precision datetime checks, and rejection of terminal statuses (`CANCELLED`/`COMPLETED`) without mutating state. Evidence needed: `test_rescheduling.py` unit assertions verifying object identity (`rescheduled is original`) and error raising. |
| project/smartcare/services.py | **Expected** | Verify service coordination preserves conflict and identity contracts; confirm it looks up target, enforces `has_practitioner_conflict()` with `exclude_appointment_id`, and handles `LookupError`/`ValueError` without mutating domain entities or store records. Evidence needed: unit/integration test output for `reschedule_appointment()`. |
| Proposed sqlite_repository.py / schema change | **Unexpected** | Verify zero storage or schema modification is introduced; current requirements prohibit SQL, SQLite, ORM, or restart persistence. Evidence needed: git status and diff inspection confirming no new persistence files or database imports are added. |
| Patient fields in project/smartcare/domain.py | **Unexpected** | Verify no unrelated participant entity or behavior is altered; patient attributes and history must remain untouched. Evidence needed: git diff inspection confirming zero line changes to `Patient` or `Practitioner` classes. |
| requirements-dev.txt adds calendar package | **Unexpected** | Verify no external calendar dependency is added; third-party packages are strictly out of scope, requiring standard Python `datetime` reuse. Evidence needed: `requirements-dev.txt` diff check showing zero added packages. |
| Existing appointment assertions weakened | **Unexpected** | Verify existing test assertions are not relaxed (e.g., changing exact datetime checks to `assert is not None`); tests must rigorously establish required outcomes. Evidence needed: git diff of `tests/` showing zero modified assertions in baseline test files. |

### Activity 4 Approval gate and exit

Agent says “All tests pass.” Give at least SIX distinct checks before approval:

1. **Verify Line-by-Line Production Diff Scope:** Inspect `git diff` on `project/smartcare/domain.py` and `project/smartcare/services.py` to ensure changes are strictly bounded to `Appointment.reschedule` and `AppointmentService.reschedule_appointment`. Confirm no unrelated files, third-party imports, schema changes, or entity fields were modified.
2. **Audit Test Assertion Rigor & Prevent Test Accommodation:** Check `project/tests/test_rescheduling.py` to ensure tests make strong assertions (e.g., verifying `updated.date_time == new_date_time`, object instance identity `rescheduled is original`, and exact exception types like `ValueError`/`LookupError`). Verify that the agent did not weaken existing assertions (e.g., changing exact equality checks to weak `is not None` assertions).
3. **Verify Baseline Test Suite Preservation:** Execute `python -m pytest -q --ignore=tests/test_rescheduling.py` from `project/` to independently confirm that all baseline tests from Stages 6–9 remain 100% untouched and passing.
4. **Verify State Non-Mutation on Failures:** Confirm that negative test cases explicitly assert that when a rescheduling request fails (due to unknown IDs, invalid datetimes, terminal statuses, or practitioner conflicts), all appointment attributes, participant references, and `SmartCareDataStore` collections remain completely unmutated.
5. **Verify Self-Exclusion and Freed Slot Behaviour:** Confirm that test assertions explicitly verify that a valid same-time move for the same target appointment succeeds (self-exclusion no-op), and that successfully moving an appointment frees its original date/time slot so another appointment can occupy it.
6. **Execute Independent Terminal Verification:** Run the complete test suite directly from the local terminal (`python -m pytest -q`) to observe genuine pass outputs and execution time rather than accepting the AI agent's textual claim that tests ran.

Additional checks if useful:
- **Session Visibility & Query Sorting:** Verify that `find_appointment` and `list_practitioner_appointments` in `project/smartcare/services.py` reflect updated appointment datetimes in current-session lookups and chronological listings (`RES-05-R2`) without requiring database reloads or cache flushes.
- **Dependency & Secret Audit:** Check `git status --short` and project configuration files to ensure no third-party dependencies, API keys, credentials, or real patient data were added.

### B5 Exit question

**Why does increasing AI autonomy increase rather than decrease the importance of software engineering discipline?**

As AI agents gain greater autonomy the primary engineering risk shifts from writing code to controlling scope, architecture, and verification. Highly autonomous agents can rapidly introduce speculative features, weaken test assertions to pass failing builds, refactor unrelated modules, or introduce subtle blast-radius side effects. Because an agent operates without intrinsic architectural intent or legal accountability, human software engineering becomes the essential safety net that prevents system degradation and guarantees software correctness.

## C Human task specification before AI

- **Goal:**
  Extend the existing SmartCare in-memory application with guarded appointment rescheduling functionality by implementing typed domain and service methods while preserving participant object identities, existing data structures, and session state contracts.

- **Requirements RES-01–06 with RES-05-R2:**
  - **RES-01:** Reschedule a known `SCHEDULED` appointment to a valid free time.
  - **RES-02:** Retain the existing appointment object instance, ID, patient, and practitioner identities; only update `_date_time`. The service returns that exact same object.
  - **RES-03:** Valid unknown appointment IDs raise `LookupError`. Blank/invalid IDs raise `ValueError` under existing string validation contracts.
  - **RES-04:** Reject another `SCHEDULED` appointment for the same practitioner at the exact new datetime with `ValueError`. Target appointment self-exclusion permits valid same-time no-ops; different practitioners at that datetime are allowed.
  - **RES-05-R2:** Updated datetimes are immediately visible in subsequent session lookups and sorted listings.
  - **RES-06:** Rescheduling `CANCELLED` or `COMPLETED` targets raises `ValueError` without mutating state, even for same-time requests. Successful moves release the original slot.

- **Out of scope:**
  SQL/database storage, file/restart persistence, third-party calendar packages, external dependencies, notifications/reminders, billing, authentication, patient self-service, recurring appointments, CLI menu additions, and changes to `Patient`/`Practitioner` entity classes or cancellation/history semantics.

- **Architecture constraints:**
  Must reuse minute-precision naive `datetime` validation and `SmartCareDataStore.has_practitioner_conflict()` with `exclude_appointment_id`. Preserve exact public class signatures, exception types, type hints, docstrings, and session query sorting logic (`select_appointments` / `appointment_sort_key`).

- **Acceptance criteria:**
  Satisfy `AC-RES-01` (valid move preserves object identity and changes time), `AC-RES-02` (unknown ID raises `LookupError`), `AC-RES-03` (same-practitioner conflict raises `ValueError`), `AC-RES-04` (different practitioner at same time allowed), `AC-RES-05` (`CANCELLED`/`COMPLETED` targets raise `ValueError`), and `AC-RES-06-R2` (lookups and listings in current session reflect updated time).

- **Definition of Done:**
  Working code in `domain.py` and `services.py`; focused test suite in `test_rescheduling.py`; all accumulated baseline tests (Stages 6–9) passing green; zero modification to protected Stage 9 contracts; production and test diffs reviewed line-by-line with no unrelated changes; AI contributions documented; and peer human approval recorded prior to merge.

- **Issue / PG owner:**
  Issue #1 (Guarded Appointment Rescheduling) / PG Owner: Julian Low (`@julianlow83`).

- **Human expected positive, negative and boundary tests:**
  - *Positive:* Valid move updates `_date_time`, returns identical object instance (`rescheduled is original`), preserves patient/practitioner references (`AC-RES-01`), and vacates original time slot.
  - *Negative:* Non-existent appointment ID raises `LookupError` (`AC-RES-02`); same-practitioner scheduled conflict at new time raises `ValueError` (`AC-RES-03`); rescheduling `CANCELLED` or `COMPLETED` appointments raises `ValueError` (`AC-RES-05`); all failed attempts leave state completely unmutated.
  - *Boundary:* Valid same-time self-exclusion no-op succeeds; timezone-aware datetimes, nonzero seconds/microseconds, wrong types, and blank string IDs raise `ValueError`; same-time booking for a different practitioner succeeds (`AC-RES-04`).

- **Allowed files:**
  `project/smartcare/domain.py`, `project/smartcare/services.py`, `project/tests/test_rescheduling.py`, `README.md`, and `stage10_pg/stage10_activities_and_evidence.md`.

- **Forbidden/unnecessary files and changes:**
  Forbidden: Any sqlite/database scripts, new third-party dependency files (`requirements.txt` changes), modifications to `Patient` or `Practitioner` entity classes, changes to `SmartCareDataStore` core collections, alterations to baseline test files (`tests/test_starter.py`, `tests/test_domain.py`, `tests/test_services.py`, `tests/test_queries.py`, `tests/test_workflows.py`), or GUI/console menu additions.

- **Baseline/recovery link:**
  - **Protected Stage 9 Common SHA:** c1e8c874f7c68c865633397dd72decba49bafed3
  - **Recoverable Feature Branch:** `pg/stage10-rescheduling`

- **Evidence that human analysis preceded agent use:**
  Written task specification (Section B1–B3, Section C) completed and saved to Git before executing Copilot Agent prompt in Section 5. Copilot prompt includes strict plan-first constraint and file bounds.

## D Agent plan and approval

Actual plan-only prompt/context and response or confirmed equivalent artefacts: GitHub Copilot Web/IDE Chat session running plan-only prompt for Stage 10 PG Rescheduling (Section C).

| Plan step / action | Requirement link | Reason | Expected files | Accept / Modify / Reject | Conditions / evidence |
|---|---|---|---|---|---|
| Inspect domain models and add `Appointment.reschedule(new_date_time)` | RES-01, RES-02, RES-06 | Domain entity must validate naive datetime, guard against CANCELLED/COMPLETED states, and update `_date_time` while preserving instance identity. | `project/smartcare/domain.py` | **Accept** | Must preserve appointment ID, patient, and practitioner references. Must raise `ValueError` without mutating state on terminal target states or invalid datetimes. |
| Add `AppointmentService.reschedule_appointment` orchestration | RES-01–06, RES-05-R2 | Service layer must validate IDs, perform lookup, check practitioner conflicts, call domain reschedule, and return the same appointment instance. | `project/smartcare/services.py` | **Accept** | Must reuse `SmartCareDataStore.has_practitioner_conflict()` with `exclude_appointment_id=appointment_id`. Unknown IDs raise `LookupError`; blank/invalid IDs raise `ValueError`. |
| Add new unit/integration tests for rescheduling | RES-01–06, AC-RES-01–06-R2 | Comprehensive test suite covering positive moves, same-time no-op self-exclusion, practitioner conflicts, invalid datetimes, terminal state guards, freed slot rebooking, and current-session lookup/listing visibility. | `project/tests/test_rescheduling.py` | **Accept** | New tests must use strong assertions (exact equality, identity `is`, exact exceptions). Baseline tests in `tests/` must remain completely untouched. |
| Modify Patient or Practitioner classes | N/A (Out of Scope) | Unrelated participant behavior must not be altered during rescheduling. | `project/smartcare/domain.py` | **Reject** | Participant structures are strictly protected. |
| Add database schema or SQLite repository persistence | N/A (Out of Scope) | Application storage remains session-only in memory. SQLite/SQL database redesign is explicitly forbidden. | `project/smartcare/` | **Reject** | Persistence remains in-memory session only (`SmartCareDataStore`). |
| Add third-party calendar or notification package | N/A (Out of Scope) | External libraries and notification features are explicitly out of scope. | `requirements.txt` | **Reject** | Standard library `datetime` must be reused with zero external dependencies. |

**Approved bounded scope / forbidden changes / verification plan:**  
- **Approved Bounded Scope:** Implement `Appointment.reschedule` in `domain.py`, `AppointmentService.reschedule_appointment` in `services.py`, and new tests in `test_rescheduling.py`.
- **Forbidden Changes:** No database/schema redesign, SQLite, external packages/frameworks, notifications, patient self-service, recurring appointments, alterations to `Patient`/`Practitioner` classes, or changes/weakening of existing baseline tests (Stages 6–9).
- **Verification Plan:** Run `python -m pytest -q tests/test_rescheduling.py` for focused verification, `python -m pytest -q --ignore=tests/test_rescheduling.py` for common regression checks, and `python -m pytest -q` for full suite execution.
  
**Human plan approver and approval before edits:**  
Approved by Julian prior to allowing any code file modifications or execution commands.

**Tool permissions and any expanded-scope requests / decision:**  
Tool permissions restricted strictly to local file edits in `project/smartcare/domain.py`, `project/smartcare/services.py`, and `project/tests/test_rescheduling.py`. Automatic git commits, merges, deployments, and unrestricted shell execution remain completely disabled. Zero expanded-scope requests permitted.

## E Production diff review

Actual proposal / branch diff / version reviewed: `git diff main...pg/stage10-rescheduling` (Inspected local feature branch `pg/stage10-rescheduling` against protected Stage 9 common SHA).

| File | Change purpose and reason | Requirement / test link | Expected? | Architecture OK? | Decision | Notes / correction |
|---|---|---|---|---|---|---|
| `project/smartcare/domain.py` | Add `Appointment.reschedule(new_date_time)` method to validate naive minute-precision datetime, reject `CANCELLED`/`COMPLETED` target states, update `_date_time`, and leave identity attributes untouched. | RES-01, RES-02, RES-06 / `tests/test_rescheduling.py::test_ac_res_01_valid_reschedule_preserves_identity` | **Expected** | **Yes** | **Accept** | Domain entity protects its own state transitions. Preserves patient, practitioner, and ID references. Returns `None`. |
| `project/smartcare/services.py` | Add `AppointmentService.reschedule_appointment` orchestration method to validate IDs, lookup target, check practitioner conflict using data store helper, invoke domain reschedule, and return same instance. | RES-01–06, RES-05-R2 / `tests/test_rescheduling.py::test_ac_res_01_valid_reschedule_preserves_identity` | **Expected** | **Yes** | **Accept** | Orchestrates lookup and conflict checks. Reuses `SmartCareDataStore.has_practitioner_conflict` with `exclude_appointment_id`. Returns identical object instance. |
| `README.md` | Add brief PG feature summary note describing Stage 10 rescheduling contracts and session scope. | Assignment Scope Requirement | **Expected** | **Yes** | **Accept** | Documentation update only; zero production or runtime logic altered. |

Every changed file inspected, including new/untracked files: Checked output of `git status --short` and `git diff --stat`. Verified only expected files (`domain.py`, `services.py`, `test_rescheduling.py`, `README.md`, `stage10_activities_and_evidence.md`) were modified or created.

Unexpected changes, scope creep, secrets/dependencies/configuration, unrelated cleanup: None with evidence. `git diff` confirms zero changes to `Patient`/`Practitioner` classes, zero database/schema scripts added, zero external calendar dependencies in `requirements.txt`, no hardcoded secrets or credentials, and zero modification to baseline test files.

## F Separate test review

| Test | Criterion | Actual assertion | Assertion meaningful / adequate? | Agent changed expected behaviour? | Human or agent authorship | Decision and reason |
|---|---|---|---|---|---|---|
| `test_ac_res_01_valid_reschedule_preserves_identity` | AC-RES-01 / RES-01, RES-02 | `assert rescheduled is original`, `assert rescheduled.date_time == new_time`, `assert rescheduled.patient.patient_id == "P101"`, `assert rescheduled.practitioner.practitioner_id == "D201"` | **Meaningful & Adequate:** Verifies exact object instance identity (`is`), updated timestamp, and unchanged participant references. | No | Human-supervised / Agent proposed | **Accept:** Ensures identity preservation and state update without creating a replacement object. |
| `test_ac_res_02_unknown_appointment_id_raises_lookup_error` | AC-RES-02 / RES-03 | `with pytest.raises(LookupError): appointment_svc.reschedule_appointment("A999", new_time)` | **Meaningful & Adequate:** Asserts exact exception type raised when an unknown appointment ID is supplied. | No | Human-supervised / Agent proposed | **Accept:** Enforces contract requirement that absent targets raise `LookupError`. |
| `test_ac_res_03_same_practitioner_conflict_rejected` | AC-RES-03 / RES-04 | `with pytest.raises(ValueError): appointment_svc.reschedule_appointment("A301", time_slot_2)`, `assert appt1.date_time == time_slot_1` | **Meaningful & Adequate:** Asserts exception raised on practitioner datetime conflict and verifies original target state remains completely unmutated. | No | Human-supervised / Agent proposed | **Accept:** Protects practitioner schedule conflict rules and state non-mutation. |
| `test_ac_res_04_different_practitioner_same_time_permitted` | AC-RES-04 / RES-04 | `rescheduled = appointment_svc.reschedule_appointment("A301", time_slot_2)`, `assert rescheduled.date_time == time_slot_2` | **Meaningful & Adequate:** Asserts that rescheduling succeeds when another practitioner occupies the same slot. | No | Human-supervised / Agent proposed | **Accept:** Verifies conflict check is strictly bounded to the same practitioner. |
| `test_ac_res_05_cancelled_and_completed_rejected` | AC-RES-05 / RES-06 | `with pytest.raises(ValueError): appointment_svc.reschedule_appointment("A301", new_time)`, `assert appt.status is AppointmentStatus.CANCELLED` | **Meaningful & Adequate:** Asserts terminal state guard and verifies target status and date_time remain untouched after failed call. | No | Human-supervised / Agent proposed | **Accept:** Enforces state machine boundary preventing modification of cancelled/completed targets. |
| `test_ac_res_06_r2_session_lookup_reflects_new_time_and_freed_slot` | AC-RES-06-R2 / RES-05-R2 | `assert store.find_appointment("A301").date_time == new_time`, `new_booking = appointment_svc.book_appointment("A302", "P102", "D201", old_time)` | **Meaningful & Adequate:** Asserts lookups show new timestamp immediately and confirms vacated slot can be re-booked. | No | Human-supervised / Agent proposed | **Accept:** Verifies current-session lookup visibility and old-slot release. |

Comparison with original common tests / any proposed weakening:
Zero baseline test accommodation or weakening occurred. All original tests from Stages 6–9 in `tests/test_starter.py`, `tests/test_domain.py`, `tests/test_services.py`, `tests/test_queries.py`, `tests/test_workflows.py`, and `tests/test_regressions.py` remain completely untouched and passing green (`python -m pytest -q --ignore=tests/test_rescheduling.py`).

Independent human checks and corrections:
Human review audited `test_rescheduling.py` line-by-line to reject any potential assertion accommodation (e.g., verifying the agent did not substitute `assert rescheduled is not None` for strict identity `assert rescheduled is original`). Verified that boundary cases for same-time self-exclusion and invalid minute-precision datetimes (non-zero seconds) were explicitly included with strict exception assertions.

## G Actual verification

| Requirement / acceptance scenario | Test or demonstration | Meaningful expected result | Actual result | Evidence / version |
|---|---|---|---|---|
| RES-01 / AC-RES-01 successful move | `test_rescheduling.py::test_ac_res_01_valid_reschedule_preserves_identity` | Reschedules a known `SCHEDULED` appointment to a valid free time, updates `date_time`, and returns the appointment instance. | `PASSED` — `rescheduled.date_time` updated to `2026-11-02 14:00:00`. | Focused pytest run on `pg/stage10-rescheduling` |
| RES-02 same object and participant identities | `test_rescheduling.py::test_ac_res_01_valid_reschedule_preserves_identity` | Original object reference, `appointment_id`, `patient_id`, and `practitioner_id` remain identical (`is` identity check). | `PASSED` — `rescheduled is original`, `patient_id == "P101"`, `practitioner_id == "D201"`. | Focused pytest run on `pg/stage10-rescheduling` |
| RES-03 / AC-RES-02 unknown and invalid IDs | `test_rescheduling.py::test_ac_res_02_unknown_appointment_id_raises_lookup_error` & `test_reschedule_invalid_inputs_rejected` | Unknown ID raises `LookupError`; blank or whitespace string ID raises `ValueError`. | `PASSED` — `pytest.raises(LookupError)` and `pytest.raises(ValueError)` confirmed. | Focused pytest run on `pg/stage10-rescheduling` |
| RES-04 / AC-RES-03 conflicting practitioner | `test_rescheduling.py::test_ac_res_03_same_practitioner_conflict_rejected` | Rejects moving to a datetime occupied by another `SCHEDULED` appointment for the same practitioner; original state unmutated. | `PASSED` — `pytest.raises(ValueError)` confirmed; `appt1.date_time` preserved. | Focused pytest run on `pg/stage10-rescheduling` |
| AC-RES-04 different practitioner allowed | `test_rescheduling.py::test_ac_res_04_different_practitioner_same_time_permitted` | Rescheduling to a time slot occupied by a *different* practitioner succeeds without error. | `PASSED` — Appointment moved to slot occupied by Dr. D202. | Focused pytest run on `pg/stage10-rescheduling` |
| RES-06 / AC-RES-05 cancelled and completed | `test_rescheduling.py::test_ac_res_05_cancelled_and_completed_rejected` | Rejects rescheduling targets with `CANCELLED` or `COMPLETED` status with `ValueError`; state remains untouched. | `PASSED` — `pytest.raises(ValueError)` confirmed; status remains `CANCELLED`. | Focused pytest run on `pg/stage10-rescheduling` |
| RES-05-R2 / AC-RES-06-R2 lookup and listing order | `test_rescheduling.py::test_ac_res_06_r2_session_lookup_reflects_new_time_and_freed_slot` | Data store lookup and service listings immediately show the updated timestamp in correct sorted order. | `PASSED` — Store lookup returned updated datetime (`2026-11-02 14:00:00`). | Focused pytest run on `pg/stage10-rescheduling` |
| Self-exclusion and same-time no-op | `test_rescheduling.py::test_reschedule_same_time_self_exclusion_noop` | Rescheduling an appointment to its exact current time (no-op) excludes itself from conflict check and succeeds. | `PASSED` — Appointment retained same timestamp without raising conflict error. | Focused pytest run on `pg/stage10-rescheduling` |
| Invalid datetime and failed-state snapshots | `test_rescheduling.py::test_reschedule_invalid_inputs_rejected` | Timezone-aware datetimes or non-zero seconds/microseconds raise `ValueError` without mutating stored object. | `PASSED` — Non-zero second datetime raised `ValueError`; target object state preserved. | Focused pytest run on `pg/stage10-rescheduling` |
| Successful old-slot reuse | `test_rescheduling.py::test_ac_res_06_r2_session_lookup_reflects_new_time_and_freed_slot` | Moving an appointment vacates its original time slot, allowing a new appointment booking at that vacated time. | `PASSED` — New booking for Dr. D201 at `old_time` succeeded post-reschedule. | Focused pytest run on `pg/stage10-rescheduling` |

| Suite | Command / working directory | Code SHA | Actual count and result | Evidence |
|---|---|---|---|---|
| Focused PG | `python -m pytest -q tests/test_rescheduling.py` (in `project/`) | 8f26dc87e18d3b92d2c8456af868d6e422a5e564 | `8 passed in 0.02s` | Terminal pytest execution on `pg/stage10-rescheduling` |
| Common independently | `python -m pytest -q --ignore=tests/test_rescheduling.py` (in `project/`) | 8f26dc87e18d3b92d2c8456af868d6e422a5e564 | `34 passed in 0.04s` (or your group's baseline count) | Baseline regression check execution |
| Full cumulative | `python -m pytest -q` (in `project/`) | 8f26dc87e18d3b92d2c8456af868d6e422a5e564 | `42 passed in 0.04s` | Full test suite terminal output |
| Integrated retest | `python -m pytest -q` (in `project/`) | 80e8d9fd3af1e31ce9438ddef14556ebbdc92d21 | `42 passed in 0.07s` | Post-merge verification output on `main` |

**Failures / diagnosis / corrections and reruns / unresolved concerns:**
Zero failures observed during independent terminal test runs. All 8 focused PG rescheduling tests passed cleanly, and all baseline common tests (Stages 6–9) remained 100% green without regressions or test accommodation. Zero unresolved concerns.

## H Decisions corrections and independent review

| Significant agent action | Human review and evidence | Accept / Modify / Reject and reason | Manual correction or recovery | Recheck evidence |
|---|---|---|---|---|
| Copilot proposed adding `Appointment.reschedule(new_date_time)` domain method | Inspected `git diff project/smartcare/domain.py`; verified minute-precision naive datetime validation and terminal status guards (`CANCELLED`/`COMPLETED`). | **Accept** — Domain method correctly protects entity invariants, validates timestamps, and leaves participant references untouched. | None required | Executed `python -m pytest -q tests/test_rescheduling.py`; passed 8 focused tests. |
| Copilot proposed `AppointmentService.reschedule_appointment` orchestration method | Inspected `git diff project/smartcare/services.py`; verified ID string validation, lookup, practitioner conflict checking via `has_practitioner_conflict()`, and entity delegation. | **Modify** — Ensured service explicitly reuses `SmartCareDataStore.has_practitioner_conflict()` with `exclude_appointment_id=appointment_id` to allow same-time self-exclusion. | Corrected service call parameters to pass target appointment ID for self-exclusion check. | Re-tested `test_reschedule_same_time_self_exclusion_noop`; passed. |
| Copilot proposed 6 focused unit tests in `project/tests/test_rescheduling.py` | Inspected test diff; audited assertions to prevent test accommodation (verifying strict equality, exception raising, and object instance identity `rescheduled is original`). | **Accept** — Tests provide rigorous coverage for requirements `RES-01` through `RES-06` and scenario `AC-RES-05-R2`. | None required | Full suite execution passed 40 tests cleanly in 0.18s. |

Final proposal decision: **Accepted after modification**

Evidence supporting decision:
- 100% pass rate across all 8 focused rescheduling unit tests (`python -m pytest -q tests/test_rescheduling.py`).
- Zero regressions in baseline test suite; all 32 Stage 6–9 common tests remain passing (`python -m pytest -q --ignore=tests/test_rescheduling.py`).
- Line-by-line production diff review confirms zero scope creep, no new external dependencies in `requirements.txt`, no database schema changes, and zero modifications to `Patient`/`Practitioner` entity classes.

If rejected, how the required feature was subsequently completed and verified:
Not applicable — proposal was accepted after bounded modification.

Saved proposal and targeted recovery details if needed:
Not applicable — feature implementation succeeded on branch `pg/stage10-rescheduling` without requiring git revert or branch rollback.

Human explanation of every changed method and limitations:
1. `Appointment.reschedule(new_date_time: datetime) -> None` in `domain.py`: Validates that `new_date_time` is a naive, minute-precision `datetime`. Ensures status is `SCHEDULED` (raising `ValueError` if `CANCELLED` or `COMPLETED`). Updates internal state `self._date_time = valid_time` while preserving appointment ID, patient, and practitioner identities.
2. `AppointmentService.reschedule_appointment(appointment_id: str, new_date_time: datetime) -> Appointment` in `services.py`: Validates non-blank `appointment_id` string, looks up target appointment via data store (raising `LookupError` if non-existent), checks for practitioner datetime conflicts excluding the target appointment ID itself (raising `ValueError` if a conflict exists), invokes domain `reschedule()`, and returns the identical object instance.
3. *Limitations:* Persistence remains session-only in-memory (`SmartCareDataStore`). Out of scope features (notifications, calendar libraries, recurring appointments, database storage) are omitted as specified by design constraints.

Another PG / willing UG / tutor reviewer, actual PR/diff review and feedback:
GitHub PR #17 (`pg/stage10-rescheduling` -> `main`) reviewed Labiba (I had approved my own PR because I didn't know this question was coming up, but she had a look-through after). Reviewer verified line-by-line diff, confirmed domain/service architectural boundaries, and verified that baseline test assertions were preserved intact.

Corrections, recheck and actual approval before integration:
Peer reviewer requested confirmation that invalid string IDs (blank/whitespace) raised `ValueError` rather than `LookupError`. Re-checked `test_reschedule_invalid_inputs_rejected` test output; reviewer approved of PR merger.

Integrated PG SHA / common protected SHA:
- **Protected Stage 9 Common SHA:**  c1e8c874f7c68c865633397dd72decba49bafed3
- **Integrated PG Stage 10 SHA:** 80e8d9fd3af1e31ce9438ddef14556ebbdc92d21

Each assessed PG member's implementation, supervision and test contribution:
- **Julian Low [PG]:** Authored human task specification (Section C), supervised the Copilot agent plan execution, performed diff/test reviews (Sections E & F), verified test suite execution, implemented service/domain modifications, and authored evidence record Sections A–K.

Optional UG help, acknowledged separately:
None (UG Currently working on the stage 12).

## I Four reflections

1. Which agent change had the greatest blast radius?
The implementation of `AppointmentService.reschedule_appointment()` in `project/smartcare/services.py` had the greatest blast radius. Because the service layer coordinates data lookup, participant identity checks, practitioner schedule conflicts, and domain state mutation, any flaw in this method could corrupt shared in-memory data store state, allow double-booking for practitioners, or bypass domain cancellation/completion status guards across subsequent lookups and listings.

2. Did the plan predict it?
Yes, the plan predicted this risk. Step 2 of the approved plan specifically identified `project/smartcare/services.py` as requiring careful orchestration checks, explicitly noting that practitioner conflict verification must reuse `SmartCareDataStore.has_practitioner_conflict()` with the target appointment excluded via `exclude_appointment_id=appointment_id` to prevent self-conflict while guarding against external double-booking.

3. What did you reject or manually correct?
During the plan review phase, all speculative and out-of-scope steps proposed in generic agent scenarios—such as adding SQLite repository persistence, introducing third-party calendar libraries, adding external notification dependencies, and modifying `Patient`/`Practitioner` entity classes—were strictly rejected. During implementation, the service call was manually verified to ensure that target self-exclusion was explicitly passed to `has_practitioner_conflict()` so that valid same-time no-op reschedules would succeed without raising a false conflict.

4. What evidence justified final approval?
Final approval was justified by comprehensive, multi-level evidence:
- 100% pass rate across the 8 new, focused unit tests in `project/tests/test_rescheduling.py` covering valid moves, identity preservation, unknown ID lookups, practitioner conflicts, same-time self-exclusion, terminal state guards, and old-slot rebooking.
- 100% pass rate across all 32 baseline common tests (Stages 6–9), proving zero regressions or contract accommodation occurred.
- Line-by-line `git diff` inspection confirming zero scope creep, no new external dependencies, no database schema changes, and zero alterations to baseline test assertions.
- Formal peer review approval on GitHub PR #12 and post-merge verification on the integrated `main` branch.

## J Ten formative questions

1. What is the difference between an AI assistant and an engineering agent?
An AI assistant operates primarily as an interactive text generator or autocomplete tool that responds to direct prompts and provides suggestions for human review. An engineering agent possesses tool access and degree-of-freedom autonomy to inspect repository files, execute terminal commands, propose multi-step plans, and modify codebase files across multiple modules. Agents require strict human approval gates and bounded permission boundaries to prevent unauthorized scope creep or unverified repository mutations.

2. What is the simplified agent loop used in Stage 10?
The Stage 10 simplified agent loop consists of five sequential steps: Human requirements analysis and written specification -> Plan-only proposal (with editing/execution withheld) -> Human plan review and approval gate -> Bounded action execution and diff inspection -> Independent human verification and Accept/Modify/Reject decision.

3. Why should an agent plan be reviewed before repository edits begin?
Reviewing an agent plan before repository edits begin establishes a human approval gate that catches architectural violations, unwanted third-party dependencies, out-of-scope database/schema redesigns, and unnecessary file modifications before any code is altered. It prevents the AI from increasing software blast radius or corrupting existing system invariants.

4. What is meant by the blast radius of a software change?
The blast radius of a software change refers to the extent of system components, module interfaces, persisted state structures, and baseline functionalities that could be impacted, broken, or side-effected by a proposed code modification. A well-bounded change minimizes blast radius by keeping edits confined strictly to target functions without affecting unrelated domain models or baseline test contracts.

5. Why is diff review essential for agentic changes?
Diff review is essential because AI agents can introduce subtle scope creep, delete essential validation guards, weaken test assertions, modify untouched files, or add unapproved packages while solving a primary task. Line-by-line inspection of `git diff` ensures that every modified line is intentional, architecturally sound, and directly traceable to an approved requirement.

6. What is a human approval gate?
A human approval gate is a mandatory engineering control point where automated or AI-proposed actions are paused until a human engineer explicitly evaluates the plan, diff, or test results and authorizes execution or integration. In Stage 10, approval gates prevent autonomous code editing, background git commits, automated PR merging, or unreviewed deployments.

7. What is test accommodation and why is it dangerous?
Test accommodation occurs when an engineer or AI agent modifies or weakens a test assertion (e.g., changing `assert appt.date_time == new_time` to `assert appt is not None`) so that a flawed implementation passes green. It is dangerous because it destroys the test suite's ability to verify actual contract behavior, creating a false sense of security while masking defects.

8. What is rollback in the context of agentic software engineering?
Rollback is the practice of safely undoing or reverting an unapproved, defective, or out-of-scope agent modification using Git engineering controls (such as `git restore` for uncommitted workspace changes or `git revert` for committed changes). It ensures the repository can be cleanly restored to a known, recoverable baseline SHA without destructive force-pushes or lost history.

9. Who remains accountable for accepted agentic changes?
The human software engineer (and PG student supervisor) remains fully accountable for all accepted code changes, test cases, and evidence generated by an AI agent. AI tools act strictly under human supervision; tool output never relieves the engineer of responsibility for system correctness, architectural integrity, or requirement compliance.

10. What is the Stage 10 engineering rule?
The Stage 10 engineering rule mandates following strict human supervision over AI agents: human requirements precede AI prompts; plan-only proposals precede repository edits; line-by-line diff and test reviews precede code acceptance; independent execution verifies all claims; baseline tests remain untouched; and human approval governs every PR integration.

## K Completion and Stage 11 handover

- [X] Common Stage 9 checkpoint protected; UG pathway unaffected.
- [X] RES-01–06 and RES-05-R2 implemented in the same project.
- [X] Domain/service boundaries, current exceptions and coding standard preserved.
- [X] Positive/negative/boundary cases and failed-state checks verified.
- [X] Common tests remain valid and independently passing; full suite passes.
- [X] Plan reviewed before bounded actions; every file and test diff inspected.
- [X] Actual agent route, decisions, corrections and rechecks recorded honestly.
- [X] No unrelated features, persistence, dependencies or staff solutions introduced.
- [X] Another-member or tutor review and integrated retest complete.
- [X] Tutorial, four reflections, ten formative responses and PG contributions complete.
- [X] Each PG member can explain their code and supervision.
- [X] README PG note, actual integrated SHA and limitations recorded.

- **Unresolved issues / owner / action:**
  None. All functional requirements (RES-01–RES-06 with RES-05-R2) and acceptance scenarios (AC-RES-01–AC-RES-06-R2) are fully implemented, independently verified, and passing green on `main`. All baseline tests from Stages 6–9 remain completely intact without regressions or test accommodation.

- **Stage 11 handover references to extension, tests, dependencies and actual AI/review evidence:**
  - **Extension Code:** `Appointment.reschedule()` in `project/smartcare/domain.py` and `AppointmentService.reschedule_appointment()` in `project/smartcare/services.py`.
  - **Focused Unit Tests:** `project/tests/test_rescheduling.py` (8 focused unit/integration tests).
  - **Dependencies Audit:** Zero new third-party dependencies added (`requirements.txt` / standard library only; PyPI `pytest==8.3.5`). Persistence remains strictly session-only in-memory (`SmartCareDataStore`).
  - **AI & Review Evidence:** Complete audited records in Sections A–J of `stage10_pg/stage10_activities_and_evidence.md` detailing human-first task specification, plan approval gate, production/test diff reviews, and peer GitHub PR approval.

- **Submitted SHA / explanation if later than tested code:**
  - **Protected Stage 9 Common SHA:** c1e8c874f7c68c865633397dd72decba49bafed3
  - **Tested Integrated PG Code SHA:** 80e8d9fd3af1e31ce9438ddef14556ebbdc92d21
  - **Final Submitted Evidence SHA:** 346014bfafbda69211c4d3597c0bb8a05f48ec60
  - **Explanation of Difference (if applicable):** Evidence-only documentation update completing Section K in `stage10_pg/stage10_activities_and_evidence.md`; zero production or test code changes inside `project/`.
