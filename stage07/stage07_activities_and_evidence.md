# Stage 7 Testing and Verification Record

Group/tutorial: [complete]  Members/cohorts: [complete]
Requirements baseline: SmartCare A3 Requirements Baseline 2026, revision 2.
Use the same project/. Link actual evidence; keep responses concise. Blank fields are for your group. Copy rows only as needed.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage07/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions.

## A Tutorial Activities

### Activity 1 Requirement to test

For each requirement, propose one positive test, one negative test and the key assertion.

| Requirement | Positive test                                                                                                        | Negative test | Key assertion                                                                                                                                                                                                                                                                                                                                                                            |
|---|----------------------------------------------------------------------------------------------------------------------|---|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| FR-01 Register patient | Register a patient with a valid, non-blank, unused ID (e.g., 'P101') and a required full name (e.g., 'Alice Smith') via PatientService.register_patient('P101', 'Alice Smith'). | Attempt to register a patient with an existing, previously registered patient ID (e.g., 'P101') or a blank/invalid ID (e.g., '' or '   ') via PatientService.register_patient(). | **Positive:** Assert that the returned Patient object is stored in the data store, has patient_id == 'P101', and name == 'Alice Smith'.<br/>**Negative:** Assert that pytest.raises(ValueError) is raised for duplicate or blank IDs and that the original stored patient record remains unmutated.                                                                                      |
| FR-05 Prevent practitioner conflict | Book an appointment for Practitioner 'D201' at datetime 2026-11-01 10:00, then book a second appointment for a different Practitioner (e.g., 'D202') at the exact same datetime 2026-11-01 10:00.                                                                                                           | Attempt to book a second appointment for the same Practitioner 'D201' at the exact same datetime 2026-11-01 10:00 while the first appointment is in SCHEDULED status. | **Positive:** Assert that the second appointment for Practitioner 'D202' is successfully created with status AppointmentStatus.SCHEDULED.<br/>**Negative:** Assert that pytest.raises(ValueError) is raised when booking Practitioner 'D201' at the occupied time slot, and that the existing booking remains unchanged.                                                                 |
| FR-06 Cancel appointment | Call AppointmentService.cancel_appointment('A301') on an existing appointment 'A301' that currently has status AppointmentStatus.SCHEDULED.                                                                                                          | Attempt to cancel an appointment 'A301' that is already in CANCELLED status (repeated cancellation) or COMPLETED status, or attempt cancellation with an unknown/blank appointment ID. | **Positive:** Assert that cancel_appointment('A301') returns the exact same Appointment object instance (retrieved is original) and that its status property equals AppointmentStatus.CANCELLED.<br/>**Negative:** Assert that pytest.raises(ValueError) (for repeated/illegal cancellation) or pytest.raises(LookupError) (for unknown ID) is raised without altering the stored state. |
| FR-07 Retain cancelled history | After successfully cancelling appointment 'A301', perform a session lookup via AppointmentService.find_appointment('A301') or query practitioner/patient appointment listings.                                                                                                          | Verify that cancelling appointment 'A301' does not remove, delete, or return None when searching for 'A301' in SmartCareDataStore. | **Positive:** Assert that find_appointment('A301') returns the target Appointment object and its status remains AppointmentStatus.CANCELLED within current-session memory.<br/>**Negative:** Assert that data_store.find_appointment('A301') is not None (proving the record was retained in the store rather than hard-deleted).                                                        |

### Activity 2 Strong or weak assertion

For each, select Strong for stated behaviour or Weak/unclear and explain why. State the behaviour and limits.

`assert True`
Judgement: **Classification:** Weak/unclear
<br>**Reason:** Establishes only that execution reached the assertion without throwing an uncaught exception; proves zero product or requirement behavior.

`assert appointment is not None`
Judgement: **Classification:** Weak/unclear 
<br>**Reason:** Establishes only that a non-null reference exists; does not prove the object has correct attributes, valid types, or required status.

`assert appointment.status == AppointmentStatus.CANCELLED`
Judgement: **Classification:** Strong
<br>**Reason:** Explicitly establishes that the appointment's observable domain status transitioned to `AppointmentStatus.CANCELLED` as required by FR-06 / AC-05.1.

`assert len(results) > 0`
Judgement: **Classification:** Weak/unclear
<br>**Reason:** Establishes only that a collection is non-empty; fails to verify result count, filtering correctness, sorting order, or element identity.

`assert data_store.find_appointment('A1') is appointment`
Judgement: **Classification:** Strong
<br>**Reason:** Establishes object identity and memory persistence in `SmartCareDataStore` (FR-07 / AC-05.2), confirming the store returns the exact original instance rather than a newly constructed copy.

### Activity 3 Boundary thinking

Design boundary or edge cases for blank identifiers, whitespace-only names, same-time practitioner bookings, cancelled appointments and invalid status transitions.

- **Blank identifiers:**
  - **Input/State:** Empty string `""`, whitespace string `"   "`, or non-string `None` passed as patient_id, practitioner_id, or appointment_id.
  - **Expected Result:** Raises `ValueError` without mutating store state or performing lookup.
  - **Contract:** Revision 2 Validation Contract: IDs must be trimmed non-blank strings; invalid inputs raise `ValueError`.

- **Whitespace-only names:**
  - **Input/State:** Name or specialty field containing only whitespace (e.g., `'   '`).
  - **Expected Result:** Raises `ValueError` on construction or registration.
  - **Contract:** Revision 2 Validation Contract: Required names and specialty are non-blank.

- **Same-time practitioner bookings:**
  - **Input/State:** Booking Practitioner 'D201' at exact datetime '2026-11-01 10:00' when an existing SCHEDULED booking exists for 'D201' at that exact time. Boundary checks: different practitioner at same time or booking after cancellation.
  - **Expected Result:** Same practitioner + exact time raises `ValueError`; different practitioner or post-cancellation time slot succeeds.
  - **Contract:** FR-05 / BR-05 / AC-04.1 & AC-04.2: Same practitioner/exact time/SCHEDULED conflicts; another practitioner at the same time is allowed.

- **Cancelled appointments:**
  - **Input/State:** Invoking cancellation on a SCHEDULED appointment 'A301', followed by a store lookup.
  - **Expected Result:** Status transitions to `CANCELLED`; exact object is retained and retrievable in session store; time slot is freed for future bookings.
  - **Contract:** FR-06 / FR-07 / AC-05.1 & AC-05.2: Cancel SCHEDULED appointment and retain same instance in current-session history.

- **Invalid status transitions:**
  - **Input/State:** Attempting `cancel_appointment()` on an appointment that is already in `CANCELLED` or `COMPLETED` status.
  - **Expected Result:** Raises `ValueError` and leaves appointment status unmutated.
  - **Contract:** FR-06 / AC-05.3 / BR-06: Cancel only a SCHEDULED appointment; repeated cancellation is rejected.

### Activity 4 Critique GitHub Copilot tests

GitHub Copilot generates five tests, all of which pass. Two only assert that objects are not None, one asserts True, and two assume SMS notifications exist. Identify what is wrong and rewrite the test intentions.

| Candidate | What is wrong | Rewritten test intention |
|---|---|---|
| 1 | Asserts only `assert result is not None`, which fails to verify object type, attribute values, or correct initialization data. | Assert that the registered patient object's attributes match the input parameters (`patient_id == 'P101'`, `name == 'Alice Smith'`). |
| 2 | Asserts `assert True` at the end of execution, verifying zero business logic or domain requirements. | Assert that calling `cancel_appointment()` updates the appointment status explicitly to `AppointmentStatus.CANCELLED`. |
| 3 | Asserts only non-null presence on a search result collection without verifying item counts, sorting, or correct matching ID. | Assert that searching for a valid patient ID returns an exact collection containing the correct matching `Patient` instance. |
| 4 | Assumes an external SMS notification subsystem exists, which violates the architectural specification and scope limits. | Verify that booking an appointment successfully returns a valid `Appointment` object with `AppointmentStatus.SCHEDULED` in the data store. |
| 5 | Asserts that an exception happens globally using a broad base `Exception` catch, which can swallow test errors or unintended exceptions. | Use `with pytest.raises(ValueError):` narrowly around the specific conflicting booking call to enforce the exact rejection contract. |

### Tutorial exit question

Why can 100% code coverage coexist with poor software verification?

**Answer:** Code coverage is a quantitative metric measuring which lines of code executed during test execution; it does not measure requirement correctness, state accuracy, or assertion strength. 100% coverage coexists with poor verification when tests utilize weak assertions (e.g., `assert True` or non-null checks), omit negative/boundary error conditions, or allow invalid inputs to bypass domain contracts without verifying expected outcomes. A test suite can touch every executable line of code while completely failing to catch broken business logic or missing functional rules.


## B Requirement to Test Traceability Matrix

Assign TEST IDs before implementation or generation. Use canonical AC IDs with their actual meaning; quote supporting revision 2 contracts when no canonical AC is assigned. Blank-ID validation is not AC-01.2. Identify supplied versus student-authored evidence.

| Requirement | Acceptance criterion | Test ID | Test type | Test name / location | Expected behaviour | Result / observed status | Supplied or student-authored |
|---|---|---|---|---|---|---|---|
| FR-01 | AC-01.1 | TEST-FR01-01 | Positive Domain/Service | `tests/test_services.py::test_register_and_find_patient` | Valid patient data is stored and retrievable via service. | PASSED | Student-authored |
| FR-01 | Revision 2 Validation | TEST-FR01-02 | Negative Boundary | `tests/test_domain.py::test_blank_patient_id_rejected` | Blank or whitespace patient IDs raise `ValueError`. | PASSED | Student-authored |
| FR-02 | AC-02.1 / AC-02.2 | TEST-FR02-01 | Positive/Negative Service | `tests/test_services.py::test_find_patient_by_id` | Known patient lookup succeeds; absent ID raises `LookupError`. | PASSED | Student-authored |
| FR-04 | AC-03.1 | TEST-FR04-01 | Positive Service | `tests/test_services.py::test_book_appointment_success` | Valid participants and free time produce a `SCHEDULED` appointment. | PASSED | Student-authored |
| FR-05 | AC-04.1 / AC-04.2 | TEST-FR05-01 | Negative/Positive Service | `tests/test_services.py::test_prevent_practitioner_conflict` | Same practitioner/time conflict raises `ValueError`; different practitioner succeeds. | PASSED | Student-authored |
| FR-06 | AC-05.1 / AC-05.3 | TEST-FR06-01 | Positive/Negative Service | `tests/test_services.py::test_cancel_appointment_transitions` | Scheduling cancellation updates status to `CANCELLED`; repeat cancellation raises `ValueError`. | PASSED | Student-authored |
| FR-07 | AC-05.2 | TEST-FR07-01 | Positive Service | `tests/test_services.py::test_retained_cancelled_history` | Cancelled appointment remains queryable in current session store. | PASSED | Student-authored |


## C Test Design

Use descriptive test names such as test_cancel_changes_status() or test_blank_patient_id_is_rejected(). Explain what new evidence each case adds.

| Test ID | Requirement | Acceptance criterion | Positive / Negative / Boundary | Test intention | Observable result expected | Added evidence beyond supplied tests |
|---|---|---|---|---|---|---|
| TEST-FR01-01 | FR-01 | AC-01.1 | Positive | Verify patient registration stores and exposes attributes correctly. | Returns stored `Patient` with matching ID and name. | Proves end-to-end service registration workflow. |
| TEST-FR02-01 | FR-02 | AC-02.1 | Positive | Verify ID lookup retrieves exact original instance. | Returns exact target object instance. | Proves memory reference persistence. |
| TEST-FR05-01 | FR-05 | AC-04.1 | Negative | Prevent double-booking a practitioner at an occupied time slot. | Raises `ValueError` and leaves prior appointment intact. | Proves state protection during conflicts. |
| TEST-FR06-01 | FR-06 | AC-05.1 | Positive | Transition appointment status upon cancellation. | Status becomes `CANCELLED` and returns original reference. | Proves exact state mutation logic. |
| TEST-FR07-07 | FR-07 | AC-05.2 | Positive | Retain cancelled history in session memory. | Store query successfully returns the cancelled appointment. | Proves non-destructive cancellation storage retention. |

## D Arrange Act Assert Record

Arrange test data; act on one meaningful behaviour; assert the required observable outcome. Use the specific current exception with pytest.raises where needed.

| Test ID | Arrange | Act | Assert | Why meaningful / why assertion proves criterion |
|---|---|---|---|---|
| TEST-FR06-01 | Create store, register patient and practitioner, book appointment 'A301' (status SCHEDULED). | Call `AppointmentService.cancel_appointment('A301')`. | Assert return value is original instance, status is `AppointmentStatus.CANCELLED`, and store contains updated status. | Proves that cancellation mutates the domain object correctly without breaking object identity or creating unwanted copies. |
| TEST-FR05-01 | Create store, register practitioner 'D201', book first appointment at 10:00. | Attempt second booking for 'D201' at 10:00. | Assert `ValueError` is raised and existing booking slot remains untouched. | Proves conflict guardrails block double-booking while protecting existing records. |

## E Domain Test Evidence

Cover Patient/Practitioner construction and validation; Appointment construction, initial status, cancellation and illegal/repeated transitions. Preserve the four reference intentions described in handout Part C.

| Behaviour | Test file/function | Result |
|---|---|---|
| Patient construction & validation | `tests/test_domain.py::test_patient_construction_and_validation` | PASSED |
| Practitioner construction & validation | `tests/test_domain.py::test_practitioner_construction_and_validation` | PASSED |
| Appointment initial status `SCHEDULED` | `tests/test_domain.py::test_appointment_initial_status` | PASSED |
| Guarded cancellation & repeat rejection | `tests/test_domain.py::test_appointment_cancellation_guards` | PASSED |

## F Service Test Evidence

Use fresh shared SmartCareDataStore state, registered objects and completed Stage 6 services.

| Test ID | Behaviour | Requirement / criterion | Test file/function | Result |
|---|---|---|---|---|
| TEST-FR01-01 | Patient registration & lookup | FR-01 / AC-01.1 | `tests/test_services.py::test_register_patient` | PASSED |
| TEST-FR02-01 | Patient lookup by ID | FR-02 / AC-02.1 | `tests/test_services.py::test_find_patient` | PASSED |
| TEST-FR04-01 | Appointment booking | FR-04 / AC-03.1 | `tests/test_services.py::test_book_appointment` | PASSED |
| TEST-FR05-01 | Practitioner conflict prevention | FR-05 / AC-04.1 | `tests/test_services.py::test_practitioner_conflict` | PASSED |
| TEST-FR06-01 | Appointment cancellation & history | FR-06 / FR-07 / AC-05.1 | `tests/test_services.py::test_cancel_appointment` | PASSED |

## G Negative and Boundary Cases

Connect cases to actual contracts and verify unchanged state after rejection.

| Behaviour | Boundary/invalid input | Expected result | Test ID |
|---|---|---|---|
| Blank ID handling | Empty string `""` or whitespace `"   "` | Raises `ValueError` | TEST-BOUND-01 |
| Duplicate ID rejection | Registering existing ID `'P101'` twice | Raises `ValueError` | TEST-BOUND-02 |
| Unknown record lookup | Querying non-existent ID `'P999'` | Raises `LookupError` (service) / returns `None` (store) | TEST-BOUND-03 |
| Double cancellation | Cancelling an already `CANCELLED` appointment | Raises `ValueError`, leaves state unchanged | TEST-BOUND-04 |

## H GitHub Copilot Test Design

Select ONE real acceptance criterion. Complete human-first fields before using Copilot. Do not require an accepted generated test.

Requirement: FR-06 Cancel appointment
Acceptance criterion: AC-05.1 Cancelling an appointment with status SCHEDULED updates status to CANCELLED.
Behaviour to test: Successful transition of a scheduled appointment to cancelled state via service workflow.
Human-first test idea/categories: Positive test verifying status transition and object return consistency.
Prompt and purpose: Used prompt guidelines to generate candidate service tests for cancellation verification.

- Copilot test idea/candidate: `test_copilot_cancel_appointment_status`
- What it claims to verify: Service cancels a scheduled appointment.
- Requirement trace: FR-06 / AC-05.1
- Assertion quality: Strong (`assert appointment.status == AppointmentStatus.CANCELLED`)
- Human critique: Valid test candidate, adheres to project public interface contracts.
- Decision: Accept
- Reason: Accurately checks required domain behavior without private implementation dependencies.
- Final test reference if accepted/modified: `tests/test_services.py::test_copilot_cancel_appointment_status`
- Actual verification result: PASSED

Before accepting: traces to a requirement/criterion; can fail for the right reason; assertion checks required behaviour; no invented business rule; no unnecessary private implementation dependence. Reject/modify weak assertions, invented requirements, excessive mocking, duplicates, wrong exceptions, obsolete architecture and unnecessary dependencies.

## I Weak Copilot Test Reflection

Which Copilot-generated test looked convincing but was weak? A candidate asserting `assert result is not None` for appointment cancellation.
Why was it weak? It checked only for the existence of a return reference rather than verifying that the appointment's status field had actually transitioned to `CANCELLED`.
How did you strengthen it? Replaced the non-null check with an explicit assertion verifying `assert result.status == AppointmentStatus.CANCELLED` and checking that the store retains the instance.
Accepted / modified / rejected test decisions and evidence: Accepted modified assertion model in `tests/test_services.py`.

## J Regression Run

Run python -m pytest from project/. Retain all accumulated tests. Record the tested SHA accurately.

| Command | Working directory | Code SHA | Passed | Failed | Failure summary | Product defect / test defect / unresolved | Evidence and interpretation |
|---|---|---|---|---|---|---|---|
| `python -m pytest` | `project/` | `d6e8139` | 24 | 0 | None | None | All accumulated domain, service, and starter tests pass successfully. |

**Individual test runs and changed-order independence evidence:** 
- `python -m pytest tests/test_domain.py` (Result: PASSED)
- `python -m pytest tests/test_services.py` (Result: PASSED)
- `python -m pytest tests/test_services.py tests/test_domain.py` (Result: 24 passed, order independent)

**Requirement → test → verification chain:** 
- FR-06 (Cancel appointment) → `test_cancel_appointment` → Verified status transition to `CANCELLED` via AC-05.1 contract → Maintained in full regression suite. [PR #4 link](https://github.com/julianlow83/st1-assignment-3/pull/4)

## K What the Suite Still Does Not Prove

What does your test suite still not prove? The test suite does not prove multi-threaded concurrency safety, persistence across application restarts (as storage is in-memory), or compliance with external regulatory health standards.
Coverage if used: Not used.
Which uncovered areas matter, and why does coverage percentage alone not establish correctness? Uncovered areas include extreme edge conditions in CLI console input loops and date parser boundary limits. Coverage percentage alone does not establish correctness because lines can execute under weak assertions without verifying logical outcomes.

## L Git and Review Evidence

Use links rather than copying GitHub history. Continue the Stage 6 workflow; no commit/PR count, conflict or individual test quota is imposed.

| Issue/task | Branch | PR | Reviewer | Key feedback | Outcome |
|---|---|---|---|---|---|
| FR-02 & FR-06 Verification | `feature/stage7-tests` | PR #4 | Labiba Taskin | Ensure strict exception matching on blank ID inputs. | Approved and Merged |

## M Contribution Evidence

Record actual work in test design, implementation, review, traceability, diagnosis, necessary fixes and integration. Do not include confidential peer ratings.

| Member | Actual contribution | Evidence link |
|---|---|---|
| Julian Low | Developed domain and service test cases for appointment cancellation and status guards. | [PR #4 link](https://github.com/julianlow83/st1-assignment-3/pull/4) |
| Labiba Taskin | Authored traceability matrix mappings, boundary test validations, and peer PR code reviews. | [PR #4 link](https://github.com/julianlow83/st1-assignment-3/pull/4) |
| Tanika Young | Implemented regression suite test executions, integration verification, and documentation. | [PR #4 link](https://github.com/julianlow83/st1-assignment-3/pull/4) |

## N Formative Questions

1. What question does verification answer?

Does the system match its specified requirements and design contracts?

2. What question does validation answer?

Does the system satisfy the user's actual needs and expectations in real-world use?

3. What is a unit test?
 
An automated test that isolates and verifies the behavior of a single component or small unit of code (like a method or class) independently.

4. What is a pytest fixture?

A reusable setup function decorated with `@pytest.fixture` that provides clean, consistent test data or environment states to test functions.

5. What is parametrisation in pytest?

A feature (`@pytest.mark.parametrize`) that runs a single test function multiple times with different input and expected-result parameters.

6. What is regression testing?

Re-running tests after code changes to ensure existing functionality remains intact and no new defects were introduced.

7. What does code coverage tell us, and what does it not prove?

It tells us which lines of code executed during testing; it does not prove code correctness, logical completeness, or assertion strength.

8. What makes an assertion weak?

An assertion that checks trivial conditions (like `assert True` or `assert x is not None`) without verifying exact values, types, or state transitions.

9. What is the appropriate role of GitHub Copilot as a test assistant?

To propose candidate scenarios and test drafts that must be critically evaluated, verified, and refined by human engineers.

10. What is the Stage 7 engineering rule?

Every test must trace to a documented requirement contract, establish its own independent state, use strong observable assertions, and be fully verified via pytest execution.

## O Stage Completion

Tested Stage 7 main SHA: `d6e8139`
Full-suite result: 24 passed, 0 failed
Unresolved defects and effect on baseline: None
Clean working tree and integration evidence: Verified clean working tree via git status.
Stage 8 handover status: Complete; ready for subsequent assignment phases.
All tutorial/formative responses and traceability/Copilot decisions complete: Confirmed.