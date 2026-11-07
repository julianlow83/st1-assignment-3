# Stage 9 activities and evidence

Common UG and PG record. All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage09/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. Use the Stage 9 handout and Overview/revision 2 baseline. Keep responses concise and link accessible artefacts; do not paste entire logs or private peer ratings.

Group: <!-- complete -->
Members and responsibilities: <!-- complete -->
Stage 8 integrated SHA, command, working directory and actual result: <!-- complete -->

## A. Tutorial activities

### A1 Session state classification

| Information | Required session/domain or transient state? | Requirement or reason                                                                                      |
|---|---------------------------------------------|------------------------------------------------------------------------------------------------------------|
| Patient identity | Required session/domain state               | FR-01: Must persist during the active session to link patients to bookings across menu operations.         |
| Appointment history | Required session/domain state               | FR-07, FR-08, BR-06: Completed and cancelled appointments must remain retrievable in session memory.       |
| Temporary menu choice | Transient interaction/debug state           | NFR-03, NFR-04: User CLI inputs exist only during command parsing and dispatching; lost on menu iteration. |
| Practitioner specialty | Required session/domain state               | FR-03: Domain attribute needed to identify practitioner profiles during active session lookups.                                                                                                           |
| Debug print output | Transient interaction/debug state           | Standard terminal output generated during runtime; has zero bearing on application session state.                                                                                                           |
| Appointment status | Required session/domain state                                            | FR-06, BR-08: Required state machine attribute (SCHEDULED, CANCELLED, COMPLETED) controlling lifecycles.                                                                                                           |

What is intentionally lost on exit? 

**ANSWER:** All in-memory object instances stored in SmartCareDataStore (patients, practitioners, appointments, and histories) are intentionally lost when the console application exits. FR-10 between-session persistence (SQL databases, files, JSON/CSV, pickles) is retired.

### A2 Interface and domain data plan

Plan before AI. This replaces schema/key design; no database tables are required.

| Function or component | Explicit inputs and types | Outputs | Responsibility and validation                                                                            | Domain source / existing constraint |
|---|---------------------------|---------|----------------------------------------------------------------------------------------------------------|-------------------------------------|
| appointment_sort_key | appointment: Appointment                          | tuple[datetime, str]        | Pure sorting key extractor. Extracts (date_time, appointment_id) key without side effects or mutations.  | Domain invariant: Appointment attributes (_date_time, _appointment_id).                                    |
| select_appointments | appointments: list[Appointment], practitioner_id: str, `status: AppointmentStatus                          | None = None`        | list[Appointment]                                                                                                         | Pure query. Filters by practitioner ID and optional status enum; returns a new list sorted ascending by date/time and tie-broken by ID.                                    |
| Service listing | practitioner_id: str, `status: AppointmentStatus                          | None = None`        | list[Appointment]                                                                                                         | Validates practitioner exists in data store, validates optional enum status, fetches fresh list, delegates to pure query.                                    |
| Console | Interactive string prompts (input())                          | Terminal output (print())        | Parses CLI text, converts inputs/enums, invokes service methods, handles expected errors gracefully.                                                                                                         | UI-01, UI-02, NFR-04.                                    |

Relate patient ID/name, practitioner ID/name/specialty, and appointment ID/actual participants/date_time/status to the existing contracts:

1. **Patient** (patient_id, name): Validated on registration (FR-01). patient_id must be trimmed and non-blank; duplicate IDs are rejected.
2. **Practitioner** (practitioner_id, name, specialty): Validated on registration (FR-03). practitioner_id must be trimmed and non-blank; duplicate IDs are rejected.
3. **Appointment** (appointment_id, patient_id, practitioner_id, date_time, status): Validated on booking (FR-04). Stores string references to registered participant IDs. date_time follows strict YYYY-MM-DD HH:MM format. status defaults to AppointmentStatus.SCHEDULED and transitions to CANCELLED via domain guard (FR-06).

### A3 Responsibility violations

| Conceptual case | Violation | Correct boundary and reason |
|---|-----------|-----------------------------|
| Appointment.cancel reads input | UI/Presentation leakage into Domain model          | Domain Boundary Violation: Domain entities must be pure and UI-agnostic. Interaction (input('Confirm?')) belongs strictly in console.py before invoking service workflows.                            |
| Service prints/reads the menu | Presentation leakage into Service Layer          | Application Service Boundary Violation: Services coordinate use cases and return values/exceptions. Prompts and print() calls belong in console.py.                            |
| Query sorts its source in place | Side-effect mutation in Pure Query          | Functional Purity Violation: A pure query must not modify argument collections in-place (appointments.sort()). It must construct and return a sorted() new list.                            |
| Store prints Appointment saved | UI output inside Data Access component          | Data Layer Violation: Stores manage in-memory lookup and storage silently. Output rendering is the exclusive responsibility of console.py.                            |

### A4 Sorting comparison

For `appointments.sort(key=appointment_sort_key)` and `result = sorted(appointments, key=appointment_sort_key)`, predict source order, return value and result identity. Give a meaningful mutation check: <!-- response -->

Score-example prediction and explanation of passing the named key: 
1. For appointments.sort(key=appointment_sort_key): In-place mutation. Modifies the order of appointments in place, returns None, and mutates the source list reference.
2. For result = sorted(appointments, key=appointment_sort_key): Non-mutating pure operation. Source list appointments retains its original order, returns a new list container result, where result is not appointments while contained object references are preserved (result[0] is appointments[x]).

**Meaningful Mutation Check:**  
original_order = list(appointments)
result = select_appointments(appointments, "D1")
assert appointments == original_order, "Source collection was mutated!"
assert result is not appointments, "Returned list identity must be distinct!"

**Score-example prediction and explanation of passing the named key:**
1. Predicted Output: [('Chen', 5), ('Ali', 8), ('Bea', 8)].
2. Source vs. Result Identity: scores remains [('Bea', 8), ('Ali', 8), ('Chen', 5)] (distinct container return).
3. Explanation: Passing the named function score_key as key=score_key passes a first-class function reference that sorted() calls lazily for each element during execution. Calling score_key(...) immediately would evaluate the function once with a missing argument and fail with a TypeError.


### A5 Exit question

Explain cancellation versus deletion, and checks for same-session lookup, all-status listing and SCHEDULED-only exclusion: <!-- response -->

**Cancellation vs. Deletion:** Cancellation updates the existing Appointment object's internal status property to AppointmentStatus.CANCELLED while retaining its reference in SmartCareDataStore. Deletion purges the record entirely from memory. Deletion is retired and prohibited because historical visit records and audit integrity must be maintained.

**Session Lookup & Listing Checks:**
1. data_store.find_appointment('A1') returns the exact same object reference after cancellation (status == AppointmentStatus.CANCELLED).
2. list_practitioner_appointments('D1', status=None) returns all appointments, including A1 (CANCELLED).
3. list_practitioner_appointments('D1', status=AppointmentStatus.SCHEDULED) # excludes A1 because its status does not match SCHEDULED.

## B. Human design and contracts

Complete before GitHub Copilot. Record any interface/integrity decision and its reasoning: <!-- response -->

| Requirement | Input / session data | Operation and responsible component | Expected result or error | Test / evidence |
|---|---|---|---|---|
| QRY-01 | `appointments: list[Appointment]`, `practitioner_id: str` | `queries.select_appointments` | Returns new list containing only appointments for specified practitioner | `test_queries.py::test_select_appointments_practitioner_isolation` |
| QRY-02 | `appointments`, `practitioner_id`, `status: AppointmentStatus` | `queries.select_appointments` | Filters by status; default `None` includes all statuses (`SCHEDULED`, `CANCELLED`, `COMPLETED`); no-match returns `[]` | `test_queries.py::test_select_appointments_status_filtering` |
| QRY-03 | `appointments`, `practitioner_id` | `queries.select_appointments` / `appointment_sort_key` | Ascending sort by `date_time`, tie-broken by `appointment_id`; source list/objects unmutated | `test_queries.py::test_select_appointments_ordering_and_tie_break` |
| QRY-04 | `practitioner_id: str`, `status: AppointmentStatus | None` | `AppointmentService.list_practitioner_appointments` | Validates practitioner ID; calls pure query on store snapshot; preserves cancelled history | `test_workflows.py::test_list_practitioner_appointments_service` |
| FP-01 | Unchanged inputs | `queries.select_appointments` | Pure execution with identical return outputs; no I/O, no side effects, no global state mutation | `test_queries.py::test_query_purity_repeatability` |
| FP-02 | Unsorted/sorted/empty list inputs | `queries.select_appointments` | Returns a distinct list instance (`result is not source`); contained element references remain identical | `test_queries.py::test_query_non_mutation_and_identity` |
| FP-03 | `appointment: Appointment` | `queries.appointment_sort_key` | Returns tuple key `(date_time, appointment_id)` directly; verified explicitly in key tests | `test_queries.py::test_appointment_sort_key_direct` |
| UI-01 | Interactive menu commands 1–8, 0 | `console.py` (`run_menu`) / `main.py` | Full interactive demo: register, book, reject conflict, book different practitioner, cancel, list all/scheduled, reuse freed slot | `test_workflows.py::test_ui_01_full_menu_workflow` |
| UI-02 | Malformed text, unknown IDs, invalid status, invalid choice | `console.py` (`run_menu`) | Catches `ValueError` / `LookupError`, displays clear diagnostic prompt, returns to menu without corrupting state | `test_workflows.py::test_ui_02_invalid_input_recovery` |
| FR-01–03 | `patient_id`, `name`, `practitioner_id`, `specialty` | `PatientService`, `PractitionerService` | Registers valid entities; duplicate/blank IDs raise `ValueError` without overwriting stored objects | `test_workflows.py::test_participant_registration` |
| FR-04–05 | `appointment_id`, `patient_id`, `practitioner_id`, `date_time` | `AppointmentService.book_appointment` | Validates participants and time format; rejects same-practitioner `SCHEDULED` conflict at exact time | `test_workflows.py::test_booking_conflict_rejection` |
| FR-06–08 | `appointment_id` | `AppointmentService.cancel_appointment` | Updates status to `CANCELLED`; object remains retrievable in session memory (deletion prohibited) | `test_workflows.py::test_cancellation_and_history_retention` |

Cover QRY-01–04, FP-01–03, UI-01–02 and relevant FR-01–09. Explain empty versus unknown versus invalid, enum conversion, actual object identity, error handling and unchanged state on rejection: 

### Detailed Contract and Integration Explanations

* **Empty vs. Unknown vs. Invalid Distinction:**
  * **Known practitioner with no appointments / no matching status:** Returns a **new empty list `[]`** with no error.
  * **Valid format but unregistered/unknown practitioner ID:** `AppointmentService.list_practitioner_appointments` raises a **`LookupError`** after failing data store lookup.
  * **Blank/malformed ID or non-enum status string:** Raises a **`ValueError`** at the validation boundary. Strings such as `'scheduled'` are rejected as `ValueError` rather than treated as no matches.
* **Enum Conversion at Interaction Boundary:**
  `console.py` receives raw string text from CLI input. It trims input and explicitly parses status strings using `AppointmentStatus[status_str.upper()]` or maps blank input to `None` before delegating to `AppointmentService`. Direct service callers must supply valid `AppointmentStatus` enums or `None`.
* **Actual Object Identity:**
  Pure queries return a **new list container** (`result is not appointments`). However, elements within the list retain exact object references (`result[0] is appointments[x]`). Domain entities are shared read-only references across store collections and query outputs.
* **Error Handling & State Preservation on Rejection:**
  Validation checks in services and domain guards occur **before** state modification. If an invalid input (e.g., malformed date, unknown participant ID, duplicate registration, or scheduling conflict) occurs, an exception is raised, and `SmartCareDataStore` remains completely unmutated. `console.py` catches `ValueError` and `LookupError` gracefully, displays a clear message to the user, and re-renders the menu without exiting or corrupting session data.

## C. Implementation and query verification

| Requirement / test ID | Code location | Case and meaningful assertion | Actual result | Evidence link |
|---|---|---|---|---|
| QRY-01 | `project/tests/test_queries.py` | `test_select_appointments_practitioner_isolation`: Asserts only requested practitioner `D1` is selected; `D2` control appointment excluded | `PASSED` | `test_queries.py::test_select_appointments_practitioner_isolation` |
| QRY-02 | `project/tests/test_queries.py` | `test_select_appointments_status_filtering`: Asserts `status=None` includes all, explicit `SCHEDULED`/`CANCELLED` enums filter strictly, no-match produces `[]` | `PASSED` | `test_queries.py::test_select_appointments_status_filtering` |
| QRY-03 | `project/tests/test_queries.py` | `test_appointment_sort_key_and_tie_break`: Asserts ascending sort by `date_time`, equal-time tie-break by `appointment_id` ("A1" before "A2"), source order unmutated | `PASSED` | `test_queries.py::test_appointment_sort_key_and_tie_break` |
| QRY-04 | `project/tests/test_workflows.py` | `test_service_list_practitioner_appointments_cases`: Asserts known practitioner gives list, matching status filters, valid unknown ID raises `LookupError`, blank ID or string status raises `ValueError` | `PASSED` | `test_workflows.py::test_service_list_practitioner_appointments_cases` |
| FP-01 | `project/tests/test_queries.py` | Purity verification: Repeated calls with unchanged inputs return identical outputs without reading/writing I/O or modifying global state | `PASSED` | `test_queries.py::test_query_non_mutation_and_identity` |
| FP-02 | `project/tests/test_queries.py` | `test_query_non_mutation_and_identity`: Asserts returned list is a distinct container instance (`res is not source`), while contained objects maintain exact reference identity (`res[0] is a1`) | `PASSED` | `test_queries.py::test_query_non_mutation_and_identity` |
| FP-03 | `project/tests/test_queries.py` | Named sorting key evaluation: Directly verifies `appointment_sort_key(appt)` returns tuple `(date_time, appointment_id)` and that `sorted(..., key=appointment_sort_key)` uses it | `PASSED` | `test_queries.py::test_appointment_sort_key_and_tie_break` |

Purity explanation from code inspection, including absence of hidden state and I/O:   
Code inspection of `smartcare/queries.py` confirms that `select_appointments` and `appointment_sort_key` depend strictly on explicit argument inputs (`appointments`, `practitioner_id`, `status`). The functions contain zero global variables, perform no interactive I/O (`input()`, `print()`), make no service or store lookup calls, and do not mutate arguments or contained objects in-place (`appointments.sort()`). Selection is performed via list comprehension, and ordering is executed using standard `sorted(..., key=appointment_sort_key)`, which instantiates and returns a brand-new list container instance.

What the tests do and do not establish:
* **What the tests establish:** Automated unit tests establish that the query logic is deterministic, handles status filtering/tie-breaking correctly, preserves source list ordering and contained object identity, and that service listing correctly handles ID trimming, unknown practitioner lookups, and input validation bounds.
* **What the tests do not establish:** Passing tests alone do not prove absolute functional purity. A test cannot catch hidden side-effects if the side-effect (e.g., mutating an internal global log or printing to standard output) is not explicitly asserted against in the test suite. Purity must be established by combining passing tests with direct code inspection of `smartcare/queries.py`.

## D. Integrated console and workflow evidence

| Scenario / acceptance ID | Reproducible inputs / artefact | Expected result | Observed result and state check | Evidence link |
|---|---|---|---|---|
| UI-01 full menu workflow | Interactive CLI session inputs (Commands: 1, 3, 3, 2, 4, 5, 5, 5, 6, 7, 8, 8, 5, 8, 0) | Complete happy-path execution: Register P1, D1, D2; book A1 (P1/D1 2026-10-01 09:00); reject same-time D1 conflict; book A2 for D2 at same time; cancel A1; verify A1 status CANCELLED; list D1 all vs SCHEDULED; re-book A3 in freed slot; exit session cleanly. | Exited cleanly (Status 0). `SmartCareDataStore` retained history correctly; allowed same-time booking for different practitioner D2; excluded cancelled A1 from SCHEDULED-only listing but retained it in all-status listing. | `tests/test_workflows.py::test_ui_01_full_menu_workflow` |
| UI-02 invalid-input recovery | Interactive CLI session inputs (Commands: 99, 1, 3, 5, 5, 6, 8, 0) | Graceful error recovery: Catch `ValueError` / `LookupError` / invalid choices, print diagnostic message, maintain menu loop without crashing or partial state changes. | Recovered gracefully on all invalid inputs. Rejected invalid choice (99), duplicate registration, missing participant, malformed date string ('invalid-date'), non-existent appointment ID, and invalid status string ('invalid_status'). Checked state was completely preserved before/after each rejection. | `tests/test_workflows.py::test_ui_02_invalid_input_recovery` |
| Automated service workflow | `pytest tests/test_workflows.py` | Automated integration suite executing participant registration, conflict prevention, guarded cancellation, freed-slot rebooking, and error handling. | `PASSED` (All workflow tests executed cleanly in 0.08s). Verified state preservation on rejected calls. | `tests/test_workflows.py` |

Include registration/find, booking, conflict rejection, different-practitioner booking, cancellation, retrieval, listing/filtering, freed slot and exit; duplicate/unknown/blank IDs, malformed/impossible date, invalid status, unknown choice and repeated cancellation. Identify before/after state and subsequent successful action.

## E. GitHub Copilot review and human decisions

Human design completed before AI: Completed Section E pre-Copilot Human Hypotheses for F8-01 and F8-02  
Actual prompt/context supplied: Full handout diagnostic prompt with observed/expected behavior, minimal reproduction, failing test path, human hypothesis, and source snippet from `smartcare/data_store.py`  
Actual response: Copilot generated 3 ranked diagnostic candidates assessing practitioner conflict filtering and lookup status guards  

| AI finding | Code/test evidence | Severity | Accept/Modify/Reject and reason | Change or no change | Actual verification |
|---|---|---|---|---|---|
| **Finding 1:** Missing practitioner ID predicate in `has_practitioner_conflict()` | Inspected `smartcare/data_store.py` line 112 against baseline diff; line reads `if appt.date_time == date_time...` without checking `practitioner_id` | Critical | **Accept** — Re-adding `appt.practitioner.practitioner_id == practitioner_id` restores compliance with AC-04.2 | Change | Executed `python -m pytest tests/test_regressions.py::test_f8_01_different_practitioners_same_time_permitted`; test passed in 0.04s |
| **Finding 2:** Service layer (`AppointmentService.book_appointment`) passing incorrect arguments | Inspected call site in `smartcare/services.py`; service correctly passes `practitioner_id` and `date_time` | Important | **Reject** — Service call signature and arguments are clean; fault belongs strictly to store boundary | No change | Code diff inspection confirmed `services.py` remained untouched and correct |
| **Finding 3:** Injected status guard filtering `CANCELLED` appointments in `find_appointment()` | Inspected `smartcare/data_store.py` line 92; method contains `if appointment is not None and appointment.status == AppointmentStatus.CANCELLED: return None` | Critical | **Accept** — Removing the status conditional restores retention and retrieval of cancelled appointments per FR-07 / AC-05.2 | Change | Executed `python -m pytest tests/test_regressions.py::test_f8_02_find_cancelled_appointment_retained`; test passed in 0.03s |

Responsibility check: explain how domain invariants, shared-store collections, service coordination, pure queries and console effects remain separate:  
Domain entities (`Appointment`, `Patient`, `Practitioner`) own internal state validation and state machine transitions without depending on external infrastructure or UI packages. `SmartCareDataStore` manages in-memory collection storage silently without printing terminal output or executing business rules. Application services (`services.py`) orchestrate workflows, coordinate store lookups, and delegate filtering to pure queries (`queries.py`) without performing interactive I/O. Pure query functions operate on explicit arguments and return new sorted containers without mutating source collections or store state. Terminal presentation (`console.py`) parses raw CLI text, converts status strings to enums, handles exceptions gracefully, and renders display output without embedding domain rules or direct storage manipulations.

## F. Required reflections

1. Which integration concern was architectural rather than a filtering/sorting detail? <!-- response -->
2. Which Copilot suggestion did you reject as over-engineering, and why? <!-- response -->
3. How did you prove cancelled appointments remain retrievable and listable in the same session? <!-- response -->

## G. Ten formative answers

1. **What makes select_appointments pure, and what side effect breaks purity?**
   `select_appointments` is pure because it depends strictly on its explicit arguments (`appointments`, `practitioner_id`, `status`), performs deterministic filtering/sorting without mutating the input arguments or contained objects, and returns a new list. Any side effect—such as reading CLI input (`input()`), printing output (`print()`), mutating global or store state, calling non-pure services, or modifying the input list in-place (`appointments.sort()`)—breaks functional purity.

2. **Which explicit inputs are needed, and why avoid a global store?**
   The query requires three explicit arguments: `appointments: list[Appointment]`, `practitioner_id: str`, and `status: AppointmentStatus | None = None`. Avoiding a global data store ensures the function remains deterministic, isolated, easily unit-tested without mock databases, and completely free of hidden side effects or hidden persistent dependencies.

3. **How can a new list reuse Appointment objects safely?**
   A new list instance (`result is not appointments`) acts as a fresh container holding references to the existing `Appointment` objects. Because `Appointment` objects strictly guard their internal state transitions (e.g., via `cancel()`) and pure queries perform no field modifications on them, reusing object references is memory-efficient and thread-safe without triggering unintended mutations.

4. **Why use a named key, and what breaks equal-time ties?**
   A named key function (`appointment_sort_key`) extracts the tuple `(date_time, appointment_id)`. Passing a named key reference allows `sorted()` to evaluate keys lazily per element without immediate evaluation errors. Including `appointment_id` as the second element of the key tuple acts as a deterministic tie-breaker for appointments scheduled at the exact same date and time.

5. **How do default and explicit status filters differ?**
   When `status=None` (the default), the filter includes appointments of **every** status, preserving historical records like `CANCELLED` and `COMPLETED`. When an explicit status enum is supplied (e.g., `AppointmentStatus.SCHEDULED`), the query restricts results strictly to matching objects and excludes all other lifecycle statuses.

6. **How do empty results, an unknown practitioner and an invalid filter cases differ?**
   * **Known practitioner with no matching appointments:** Returns a valid **new empty list `[]`** with no error.
   * **Valid format but unknown practitioner ID:** `AppointmentService.list_practitioner_appointments` fails store lookup and raises **`LookupError`**.
   * **Invalid/blank ID or non-enum status string:** Fails validation bounds and raises **`ValueError`** (e.g., raw string `'scheduled'` raises `ValueError` rather than matching nothing).

7. **Which console errors should be recoverable, and how is unchanged state checked?**
   Expected interaction errors—such as `ValueError` (malformed input, unknown choice, duplicate registration, conflict) and `LookupError` (unregistered participant/appointment)—must be caught by `console.py`, displayed as user-friendly diagnostics, and recovered from by re-rendering the menu. State preservation is verified by asserting that `SmartCareDataStore` contents (e.g., record counts, existing object attributes) remain identical before and after the rejected call.

8. **What does data integrity mean for registered participants, conflicts and history?**
   Data integrity requires that:
   1. Appointments link only to valid, registered `Patient` and `Practitioner` entities.
   2. Practitioner time collisions for `SCHEDULED` bookings are strictly blocked.
   3. Cancelled and completed visit records are retained in session memory for lookup/audit rather than deleted.

9. **What is GitHub Copilot's appropriate review role, and who verifies findings?**
   GitHub Copilot serves as an **assistant for candidate critique and secondary analysis**, not an autonomous reviewer or code authority. Human team members must establish human designs and tests first, evaluate Copilot findings critically (Accepting, Modifying, or Rejecting each), and verify all claims through concrete test execution.

10. **How do pure functions and OOP responsibilities work together?**
    Object-Oriented domain entities (`Appointment`, `SmartCareDataStore`) own state representation, invariant validation, and guarded state transitions. Pure functional queries (`queries.py`) operate on top of domain object snapshots to perform side-effect-free selection, filtering, and sorting. Application services (`services.py`) orchestrate state retrieval and delegate processing to pure queries without mixing interaction logic into domain models.
## H. Review, completion and common handover

Issues and bounded branches: <!-- links -->
PR/diff and another-member human reviewer: <!-- actual links/name -->
Review responses and Copilot comparison: <!-- links -->
Integrated common Stage 9 SHA: <!-- complete -->
Full regression command, working directory, actual count/result and evidence: <!-- complete -->
README run instructions and scope/limitations: <!-- link -->
Unresolved issues and support/action: <!-- complete -->
UG common candidate / PG future branch plan: <!-- complete -->

- [ ] Query contracts, purity, new lists and named-key ordering verified.
- [ ] Service empty/unknown/invalid cases and cancellation history verified.
- [ ] Every console command and invalid-input recovery demonstrated.
- [ ] Query and workflow tests plus all previous tests pass; actual evidence linked.
- [ ] Human design, Copilot critique, review and integration recorded honestly.
- [ ] Reflections and ten formative responses completed.
- [ ] README updated; earlier code/tests/records preserved.
- [ ] Common SHA protected for UG Stage 12; PG Stage 10/11 work deferred until approved.

No persistence, rescheduling or assurance implementation is part of Stage 9. UG: 6→7→8→9→12. PG: 6→7→8→9→10→11→12. Mixed groups keep one repository and protect the common candidate.
