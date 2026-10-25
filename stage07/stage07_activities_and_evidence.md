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
Judgement: 
<br>**Classification:** Weak/unclear
<br>**Reason:** Establishes only that execution reached the assertion without throwing an uncaught exception; proves zero product or requirement behavior.

`assert appointment is not None`
Judgement: 
<br>**Classification:** Weak/unclear 
<br>**Reason:** Establishes only that a non-null reference exists; does not prove the object has correct attributes, valid types, or required status.

`assert appointment.status == AppointmentStatus.CANCELLED`
Judgement: 
<br>**Classification:** Strong
<br>**Reason:** Explicitly establishes that the appointment's observable domain status transitioned to `AppointmentStatus.CANCELLED` as required by FR-06 / AC-05.1.

`assert len(results) > 0`
Judgement: 
<br>**Classification:** Weak/unclear
<br>**Reason:** Establishes only that a collection is non-empty; fails to verify result count, filtering correctness, sorting order, or element identity.

`assert data_store.find_appointment('A1') is appointment`
Judgement:
<br>* **Classification:** Strong
<br>**Reason:** Establishes object identity and memory persistence in `SmartCareDataStore` (FR-07 / AC-05.2), confirming the store returns the exact original instance rather than a newly constructed copy.


### Activity 3 Boundary thinking

Design boundary or edge cases for blank identifiers, whitespace-only names, same-time practitioner bookings, cancelled appointments and invalid status transitions.
For each input/state, expected result and supporting contract:

* **Blank identifiers:**
  * **Input/State:** Empty string `""`, whitespace string `"   "`, or non-string `None` passed as patient_id, practitioner_id, or appointment_id.
  * **Expected Result:** Raises `ValueError` without mutating store state or performing lookup.
  * **Contract:** Revision 2 Validation Contract: IDs must be trimmed non-blank strings; invalid inputs raise `ValueError`.

* **Whitespace-only names:**
  * **Input/State:** Name or specialty field containing only whitespace (e.g., `'   '`).
  * **Expected Result:** Raises `ValueError` on construction or registration.
  * **Contract:** Revision 2 Validation Contract: Required names and specialty are non-blank.

* **Same-time practitioner bookings:**
  * **Input/State:** Booking Practitioner 'D201' at exact datetime '2026-11-01 10:00' when an existing SCHEDULED booking exists for 'D201' at that exact time. Boundary checks: different practitioner at same time or booking after cancellation.
  * **Expected Result:** Same practitioner + exact time raises `ValueError`; different practitioner or post-cancellation time slot succeeds.
  * **Contract:** FR-05 / BR-05 / AC-04.1 & AC-04.2: Same practitioner/exact time/SCHEDULED conflicts; another practitioner at the same time is allowed.

* **Cancelled appointments:**
  * **Input/State:** Invoking cancellation on a SCHEDULED appointment 'A301', followed by a store lookup.
  * **Expected Result:** Status transitions to `CANCELLED`; exact object is retained and retrievable in session store; time slot is freed for future bookings.
  * **Contract:** FR-06 / FR-07 / AC-05.1 & AC-05.2: Cancel SCHEDULED appointment and retain same instance in current-session history.

* **Invalid status transitions:**
  * **Input/State:** Attempting `cancel_appointment()` on an appointment that is already in `CANCELLED` or `COMPLETED` status.
  * **Expected Result:** Raises `ValueError` and leaves appointment status unmutated.
  * **Contract:** FR-06 / AC-05.3 / BR-06: Cancel only a SCHEDULED appointment; repeated cancellation is rejected.

### Activity 4 Critique GitHub Copilot tests

GitHub Copilot generates five tests, all of which pass. Two only assert that objects are not None, one asserts True, and two assume SMS notifications exist. Identify what is wrong and rewrite the test intentions.

| Candidate | What is wrong | Rewritten test intention |
|---|---|---|
| 1 | [response] | [response] |
| 2 | [response] | [response] |
| 3 | [response] | [response] |
| 4 | [response] | [response] |
| 5 | [response] | [response] |

### Tutorial exit question

Why can 100% code coverage coexist with poor software verification?

**Answer:** Code coverage is a quantitative metric that measures which lines of code executed during a test run; it does not measure requirement correctness, state accuracy, or assertion strength. 100% coverage can coexist with poor verification because tests may use weak assertions (e.g., `assert True` or checking non-null references), omit critical negative/boundary scenarios, or pass invalid inputs without verifying domain contracts. A test suite can touch every line of code while completely failing to catch broken business logic or missing specification requirements.

## B Requirement to Test Traceability Matrix

Assign TEST IDs before implementation or generation. Use canonical AC IDs with their actual meaning; quote supporting revision 2 contracts when no canonical AC is assigned. Blank-ID validation is not AC-01.2. Identify supplied versus student-authored evidence.

| Requirement | Acceptance criterion | Test ID | Test type | Test name / location | Expected behaviour | Result / observed status | Supplied or student-authored |
|---|---|---|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

## C Test Design

Use descriptive test names such as test_cancel_changes_status() or test_blank_patient_id_is_rejected(). Explain what new evidence each case adds.

| Test ID | Requirement | Acceptance criterion | Positive / Negative / Boundary | Test intention | Observable result expected | Added evidence beyond supplied tests |
|---|---|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

## D Arrange Act Assert Record

Arrange test data; act on one meaningful behaviour; assert the required observable outcome. Use the specific current exception with pytest.raises where needed.

| Test ID | Arrange | Act | Assert | Why meaningful / why assertion proves criterion |
|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] |

## E Domain Test Evidence

Cover Patient/Practitioner construction and validation; Appointment construction, initial status, cancellation and illegal/repeated transitions. Preserve the four reference intentions described in handout Part C.

| Test ID | Behaviour | Test file/function | Result |
|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] |

## F Service Test Evidence

Use fresh shared SmartCareDataStore state, registered objects and completed Stage 6 services.

| Test ID | Behaviour | Requirement / criterion | Test file/function | Result |
|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] |

## G Negative and Boundary Cases

Connect cases to actual contracts and verify unchanged state after rejection.

| Behaviour | Boundary/invalid input | Expected result | Test ID |
|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] |

## H GitHub Copilot Test Design

Select ONE real acceptance criterion. Complete human-first fields before using Copilot. Do not require an accepted generated test.

Requirement: [complete]
Acceptance criterion: [quote]
Behaviour to test: [complete]
Human-first test idea/categories: [complete]
Prompt and purpose: [complete or link]

For each significant candidate, copy this entry as needed:
- Copilot test idea/candidate: [complete]
- What it claims to verify: [complete]
- Requirement trace: [complete]
- Assertion quality: [complete]
- Human critique: [complete]
- Decision: [Accept / Modify / Reject]
- Reason: [complete]
- Final test reference if accepted/modified: [link or not retained]
- Actual verification result: [complete; do not claim an unrun test passed]

Before accepting: traces to a requirement/criterion; can fail for the right reason; assertion checks required behaviour; no invented business rule; no unnecessary private implementation dependence. Reject/modify weak assertions, invented requirements, excessive mocking, duplicates, wrong exceptions, obsolete architecture and unnecessary dependencies.

## I Weak Copilot Test Reflection

Which Copilot-generated test looked convincing but was weak? [response]
Why was it weak? [response]
How did you strengthen it? [response]
Accepted / modified / rejected test decisions and evidence: [link actual decisions in H]

## J Regression Run

Run python -m pytest from project/. Retain all accumulated tests. Record the tested SHA accurately.

| Command | Working directory | Code SHA | Passed | Failed | Failure summary | Product defect / test defect / unresolved | Evidence and interpretation |
|---|---|---|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

Individual test runs and changed-order independence evidence: [commands, results, links]
Optional tutor-led demonstration notes: [optional; leave blank if not used]
A meaningful test should detect a relevant incorrect result. Students do not have to perform the demonstration or submit failure/restoration evidence for assessment. The tutor restores the example and reruns its tests. This is not a Stage 8 fault activity.
Requirement → test → failure/observation → diagnosis → change → verification: [concise links where applicable]

## K What the Suite Still Does Not Prove

What does your test suite still not prove? [response]
Coverage if used: [result or not used]
Which uncovered areas matter, and why does coverage percentage alone not establish correctness? [response]
Optional fixtures/parametrisation used and why, if any: [response or not used]

## L Git and Review Evidence

Use links rather than copying GitHub history. Continue the Stage 6 workflow; no commit/PR count, conflict or individual test quota is imposed.

| Issue/task | Branch | PR | Reviewer | Key feedback | Outcome |
|---|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

## M Contribution Evidence

Record actual work in test design, implementation, review, traceability, diagnosis, necessary fixes and integration. Do not include confidential peer ratings.

| Member | Actual contribution | Evidence link |
|---|---|---|
| [complete] | [complete] | [complete] |

## N Formative Questions

1. What question does verification answer?
[response]

2. What question does validation answer?
[response]

3. What is a unit test?
[response]

4. What is a pytest fixture?
[response]

5. What is parametrisation in pytest?
[response]

6. What is regression testing?
[response]

7. What does code coverage tell us, and what does it not prove?
[response]

8. What makes an assertion weak?
[response]

9. What is the appropriate role of GitHub Copilot as a test assistant?
[response]

10. What is the Stage 7 engineering rule?
[response]

## O Stage Completion

Tested Stage 7 main SHA: [complete]
Full-suite result: [complete]
Unresolved defects and effect on baseline: [complete or none]
Clean working tree and integration evidence: [complete]
Stage 8 handover status: [complete; no Stage 8 work assigned]
All tutorial/formative responses and traceability/Copilot decisions complete: [confirm]
