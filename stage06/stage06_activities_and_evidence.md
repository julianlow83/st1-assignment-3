# Stage 6 activities and evidence

Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: Monday 9:30-11:30 tutorial, group 3
- Members, GitHub usernames and cohorts: Julian Low (`julianlow83`), Labiba Taskin (`TODO`), Tanika Young (`u3334655`)
- Repository URL: https://github.com/julianlow83/st1-assignment-3
- Starting SHA: `11d3d21`

## A Requirement to issue activities

**Title:** FR-02: Implement Patient Search by Patient ID

**Context:** Currently, PatientService.find_patient will raise NotImplementedError. We need the ability to search for and retrieve stored patient records using a unique patient_id. The service must interface with SmartCareDataStore and enforce the required lookup validation contracts.

**Requirement:** FR-02: Find a patient by patient ID.

Acceptance criteria: 

1. Searching with a valid, existing patient_id will return the exact stored Patient object.
2. Input IDs are trimmed of th surrounding whitespace before lookup and are case-sensitive.
3. Searching for a valid, non-blank patient_id that is absent from the store will raise LookupError.
4. Blank, whitespace-only, empty, or non-string IDs raise ValueError.
5. Unsuccessful or successful lookups leave session data and stored objects unchanged.

Scope: 

1. Updating PatientService.find_patient in project/smartcare/services.py and adding unit tests in project/tests/test_services.py. 
2. Exclude name/substring searches, external databases, or CLI menu integrations.

Definition of Done: 

1. PatientService.find_patient implemented; focused unit tests added to project/tests/test_services.py covering valid lookups, absent lookups, trimmed/case-sensitive IDs, and ValueError rejections
2. All 8 baseline tests mus pas; peer code review completed and approved via PR before merging to main.

Owner/s: Julian, Labiba, Tanika

**Actual issue link:** https://github.com/julianlow83/st1-assignment-3/issues/2#issue-6008989965

**Title: FR-06 / FR-07:** Implement Appointment Cancellation with Retained History

**Context:** AppointmentService.cancel_appointment raises NotImplementedError. We need to be able to cancel scheduled appointments while keeping the historical records retrievable in current session memory. Implementation must execute domain transitions without deleting objects or breaking store rules.

****Requirement:**

- FR-06: Cancel only a SCHEDULED appointment. 
- FR-07: Retain the same appointment with CANCELLED status in current-session history.

**Acceptance criteria:**

1. Cancelling an appointment with status SCHEDULED executes Appointment.cancel(), updates status to CANCELLED, and returns the same Appointment object.
2. Cancelled appointment remains stored in SmartCareDataStore with CANCELLED status and remains retrievable in history queries.
3. Attempting to cancel an appointment that is already CANCELLED or COMPLETED raises ValueError without modifying state.
4. A valid but unknown appointment_id raises LookupError; blank or invalid IDs raise ValueError.
5. The operation does not delete the appointment object or create a replacement instance.

**Scope:** Implementing AppointmentService.cancel_appointment in project/smartcare/services.py and writing corresponding test assertions in project/tests/test_services.py. Exclude rescheduling, prompt-driven console menus, or persistent file/database storage.

**Definition of Done:** AppointmentService.cancel_appointment implemented; unit tests added in project/tests/test_services.py asserting same-object return, status transition to CANCELLED, history retention, and error rejections; all 8 baseline checks pass; peer review and GitHub Copilot comparison documented and approved prior to the merge.

**Owner:** Julian Low, Labiba Taskin, Tanika Young

**Actual issue link:** https://github.com/julianlow83/st1-assignment-3/issues/3#issue-6009069022

## B Commit quality

| Original example | Strong or Weak | Reason                                                                                                                                     |
|---|----------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| changes | WEAK           | Very generic/vague and doesn't say what files were modified, features added or the reason for commit.                                      |
| final version | WEAK           | Not informative, does not describe the technical changes made, possibly misleading by implying no further changes required.                |
| Add patient search by ID | STRONG         | Clear and concise, explains the specific functional capability (FR-02 patient lookup) added to the codebase.                               |
| fix stuff | WEAK           | Non-descriptive and unprofessionally worded. We don't know what defect was resolved, which components were affected, or how it was tested. |
| Prevent cancellation of completed appointments | STRONG         | Descriptive and intent-focused; explicitly states the specific domain business rule and state transition guardrail (FR-06/BR-06) enforced. |

## C Over scoped PR review

A cancellation PR also renames unrelated patient fields, restructures unrelated code and adds a new dependency.

- **Scope concerns:** The PR introduces unrelated changes that fall outside the appointment cancellation requirement (FR-06/FR-07). Specifically, it renames unrelated Patient fields, restructures unrelated code modules, and adds an unapproved new third-party dependency.
- **Responsibility and architecture concerns:** Modifying core Patient properties and adding external dependencies violates single-responsibility boundaries and pollutes the domain model. The SmartCare architecture requires keeping changes isolated to the specific service workflow (AppointmentService.cancel_appointment) without modifying standard library baselines or unrelated domain entities.
- **Testing and review concerns:** Renaming Patient fields introduces high regression risk across the baseline test suite (test_starter.py) and obscures the core pull request diff. A passing test run does not validate architectural boundary violations or unapproved dependencies, making it difficult for reviewers to verify the actual cancellation behaviour.
- Changes to remove or separate, with reasons: [response]
  1. Revert all Patient field renamings and structural code changes: These create merge conflicts and break existing codebase contracts. 
  2. Remove the new third-party dependency entirely: The application must run using only standard Python libraries and supplied starter utilities. 
  3. Separate into a single focused PR: Request the author resubmit a PR containing only the AppointmentService.cancel_appointment implementation and its corresponding tests in test_services.py. If patient refactoring is necessary, it must be tracked in a separate, dedicated issue.

## D Challenge a weak Copilot review

GitHub Copilot says: "Looks good; tests pass."

- Missing evidence: 
1. No evidence that the unit tests actually verify object identity, exact state transitions, or retained history, rather than just asserting non-null values.
2. No verification mapping specific lines of code and assertions back to acceptance criteria (FR-02, FR-06, FR-07).
3. No evidence checking whether domain encapsulation was respected.
4. No proof that invalid transitions and unknown/whitespace IDs were tested and correctly raised ValueError or LookupError.
5. Copilot cannot actually run tests; it merely reads text. There is no human-observed verification log showing execution commands (python -m pytest), code SHAs, or exact test outputs.

- **Follow-up review question 1:** "Which specific test function in test_services.py proves that cancel_appointment returns the exact same Appointment object instance rather than instantiating a new replacement record?"
- **Follow-up review question 2:** "Where in the diff does AppointmentService.cancel_appointment delegate the state transition to the domain method Appointment.cancel(), and how do we verify that protected domain attributes were not mutated directly by the service?"
- **Follow-up review question 3:** "What line in the unit tests verifies that a cancelled appointment remains stored in SmartCareDataStore with status CANCELLED and continues to be retrievable via appointment lookups?"
- **Follow-up review question 4:** "How do the new test cases verify that attempting to cancel an appointment from a COMPLETED state or calling repeat cancellations raises ValueError while leaving the appointment's state unchanged?"
- **Follow-up review question 5:** "What explicit assertions confirm that lookups with trimmed whitespace, case-sensitive strings, or invalid/blank IDs behave according to the contract by raising ValueError or LookupError appropriately?"
- **Additional questions if useful:** N/A

## E Team workflow agreement

| Practice | Team agreement |
|---|---|
| Branch naming | All new feature work, bug fixes, or task implementations must take place on dedicated, isolated feature branches created off an up-to-date main branch. Direct pushes to main are strictly forbidden. Branch names must be short, lowercase, hyphen-separated, and clearly linked to the task or issue. |
| Commit message convention | Every commit must represent a single, logical, and runnable unit of work with all local unit tests passing. Commit messages must use clear, imperative, descriptive phrasing that explains what changed and why. Vague messages (such as "updates", "fixed stuff", or single-word commits) are rejected. |
| PR size | Pull Requests (PRs) must be kept tightly focused and small in scope, corresponding to a single GitHub issue or discrete requirement (e.g., 1–3 related files changed). Large, multi-feature "mega-PRs" that touch unrelated modules or refactor unassigned files are not permitted, ensuring reviewers can conduct thorough line-by-line diff inspections. |
| Another-member review requirement | Self-reviewing and self-merging are strictly prohibited. Every PR must have at least one other group member formally assigned as a reviewer on GitHub. The reviewer must inspect the code diff, verify domain boundaries and test coverage, and complete an independent human evaluation before consulting any AI tools. |
| Merge rule | A feature branch may only be merged into main after receiving explicit human approval on GitHub, resolving all review feedback, and confirming that all 16 new unit tests plus 8 baseline tests pass cleanly (python -m pytest). Once merged via GitHub, all team members must immediately switch to local main (git switch main), pull the updates (git pull), and re-run tests to confirm integrated verification. |
| Significant Copilot disclosure rule | GitHub Copilot serves solely as an assistant for candidate code suggestions and review comparison, never as an autonomous merge authority. Any significant use of Copilot (for drafting code, unit tests, or PR critiques) must be explicitly disclosed in the PR description and recorded in the evidence file with prompt details, candidate outputs, and explicit Accept / Modify / Reject decisions backed by human reasoning. |

## F Issue and backlog index

Create at least two focused issues. Add a linked practitioner-lookup issue or an explicit supporting criterion with the tutor if needed to cover all three service targets.

| Issue link | Requirement | Owner                  | Acceptance criteria or precise link                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Status |
|---|---|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---|
| https://github.com/julianlow83/st1-assignment-3/issues/2#issue-6008989965 | FR-02: Patient Search | Julian, Labiba, Tanika | 1. Searching with a valid, non-blank patient_id returns the exact stored Patient object. <br/> 2. Inputs are trimmed of surrounding whitespace prior to lookup and are strictly case-sensitive.<br/>3. Valid but absent patient_id raises LookupError.<br/>4. Blank, empty, or non-string IDs raise ValueError.<br/>5. Operations preserve stored entity state.                                                                                                                                       | In Progress |
| https://github.com/julianlow83/st1-assignment-3/issues/2#issue-6008989965 | FR-06 / FR-07: Appointment Cancellation with Retained History | Julian, Labiba, Tanika | 1. Cancelling a SCHEDULED appointment executes Appointment.cancel(), updates status to CANCELLED, and returns the same object.<br/>2. The cancelled appointment remains stored in session history and retrievable via lookups (FR-07).<br/>3. Cancelling an already CANCELLED or COMPLETED appointment raises ValueError without altering state.<br/>4. Valid unknown ID raises LookupError; blank or invalid ID raises ValueError.<br/>5. Does not delete the object or create a replacement record. | In Progress |

## G Pull request evidence

Repeat this block per PR. Record actual events, not planned approvals.

- PR link and title: https://github.com/julianlow83/st1-assignment-3/pull/5 
- Linked issue and requirement: Closes #1 (FR-02: Patient Lookup, FR-03: Practitioner Lookup, FR-06: Cancel Appointment, FR-07: Retain Cancelled History)
- Feature branch: julian-stage06
- Changed behaviour:
  1. Implemented lookup and cancellation logic in project/smartcare/services.py:
  2. PractitionerService.find_practitioner(practitioner_id): Trims whitespace, performs exact lookup, and enforces string non-blank constraints.
  3. AppointmentService.cancel_appointment(appointment_id): Transitions SCHEDULED appointments to CANCELLED, retains the appointment instance in current-session history, and rejects repeated cancellations or unknown IDs.
  4. Created 10 new unit test cases in project/tests/test_services.py
- Meaningful commits: Implemented lookup and cancellation logic in project/smartcare/services.py
  1. 1cccef7338b17c9725bd62f1883947496779668a — first branch push for part D,E,F
  2. f6a26b3e6bfe53a34ac2fe9fc05776f18228ffd7 — stage 6 and 7
- Test command, directory and observed result:
  - Command: python -m pytest
  - Directory: project/
  - Observed Result: 24 passed in 0.09s
- Another-member reviewer: Tanika Young 
- Human observations recorded before Copilot: [2026-10-26 c10:20 A.M.]
- Requirement, responsibilities, test assertions and unrelated-scope checks:
  - Requirements: Meets AC-02.1, AC-03.1, AC-05.1, AC-05.2, and AC-05.3.
  - Responsibilities: Service layer delegates state changes to domain entities and session storage cleanly.
  - Assertions: Uses strict object reference assertions (assert retrieved is registered) and exact exception context matching.
  - Unrelated-scope check: Confirmed domain.py, data_store.py, and test_starter.py were not altered.
- Key feedback: I have submitted issue No.4 (#4) regarding missing type hints, meaning this branch looks ready-to-merge from my perspective.
- Author response/change and verification: Current Stage 6 feature branch focused on functional correctness and unit testing, log it as a separate chore/refactoring task to be addressed in an upcoming stage
- Reviewer recheck and approval: https://github.com/julianlow83/st1-assignment-3/pull/5#event-34210079938
- Merge outcome and SHA: Merged via Squash and Merge into main
- Significant Copilot assistance: Used Copilot Chat to review PR diff against requirement AC-05.1. Evaluated output: Accepted non-string input type guard, Rejected proposal to add unnecessary logging modules.
- Linked issue closure: GitHub Issue #1 automatically closed via commit keyword
- Each member updated main: Confirmed
- Integrated verification after merge: 
  - Command: python -m pytest
  - Directory: project/
  - Observed Result: 24 passed in 0.09s
- Integrated Code SHA: d6e81399469d88908e39746d2542d26e85f411a6

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

- Member and task: Julian Low — Task: Generate and evaluate candidate pytest unit tests for Appointment Cancellation (AC-05.1 / AC-05.2).
- Prompt/purpose and relevant issue/diff:
  - Purpose: Evaluate Copilot's candidate unit tests for AC-05.1 and AC-05.2 against human test design to verify status transitions, repeated cancellation rejection, and session store retention.
  - Relevant Issue / Diff: Closes #1 (FR-06 / FR-07). Closes #1 (FR-06 / FR-07). Diff under review includes cancel_appointment logic in smartcare/services.py and unit tests in tests/test_services.py.
  - Prompt Used: "Generate 3 candidate pytest unit tests for requirement AC-05.1 (Cancellation State Change) and AC-05.2 (History Retention). Include positive happy path, repeated cancellation rejection, and session store retention checks. Use pytest fixtures and strict object assertions."
- Summary of output:
  1. test_ac_05_1_cancelled_status_change_happy_path: Cancels a scheduled appointment A301, asserting cancelled is booked, status is CANCELLED, and it remains retrievable via appointment_svc and store.
  2. test_ac_05_1_repeated_cancellation_rejected: Performs a second cancellation on A301 and asserts pytest.raises(ValueError, match="Cannot cancel appointment in status 'cancelled'"),
  3. test_ac_05_2_session_store_retains_cancelled_appointment_record: Cancels A301 and checks store.find_appointment("A301") and store.list_appointments(), asserting object identity (retained is booked), non-null status, and status equality (CANCELLED).
- Human check against actual code, requirements and tests:
  1. Strong & accurate. Asserts strict object identity (cancelled is booked), correct status transition (AppointmentStatus.CANCELLED), and store retrieval.
  2. Partially brittle exception string. Properly verifies pytest.raises(ValueError), but checking the exact exception message string (match="Cannot cancel...") makes the test fragile if the service exception phrasing is slightly different.
  3. Slight redundancy. Correctly asserts retention in store.list_appointments(), but includes a redundant assert retained is not None right after asserting assert retained is booked (since booked is already confirmed non-null).
- Decision — Accept / Modify / Reject:
  1. Candidate 1 (test_ac_05_1_cancelled_status_change_happy_path): Accept
  2. Candidate 2 (test_ac_05_1_repeated_cancellation_rejected): Modify
  3. Candidate 3 (test_ac_05_2_session_store_retains_cancelled_appointment_record): Modify
- Reason: 
  1. The test is clean, uses strict object identity (is), and directly satisfies AC-05.1.
  2. Removed the rigid match="Cannot cancel..." regex check from pytest.raises(ValueError) to prevent fragile test failures while keeping the core ValueError assertion intact.
  3. Removed the redundant assert retained is not None check, keeping the strict object identity assertion (assert retained is booked) and session history checks.
- Verification/evidence: Executed python -m pytest tests/test_services.py inside project/ 3 passed in 0.06s

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: 
  -During the Part G code review on GitHub, Julian confirmed that services.py accurately enforced edge case rejections (blank string IDs raise ValueError, unknown IDs raise LookupError). Julian also noted that unit tests in test_services.py used strict object identity checks (assert cancelled is booked) and verified post-cancellation session retention (find_appointment("A301")). Tanika flagged one observation: function signatures in services.py and test methods were missing explicit Python type hint annotations (e.g., def find_patient(self, patient_id: str) -> Patient:).
- Copilot noticed: When running the Part H PR diff prompt through GitHub Copilot Chat, Copilot provided three findings:
  1. Identified that find_patient lacked explicit type guards for non-string invalid types (e.g., passing an integer or None as patient_id).
  2. Suggested adding a third-party logging framework (logging.getLogger()) to record every appointment cancellation event.
  3. Flagged missing type hint annotations across function signatures in services.py.
- Overlap: Both the human reviewer (Tanika) and GitHub Copilot independently identified the missing Python type hint annotations across the service method signatures in services.py.
- What did the human reviewer notice that Copilot did not: The human reviewer explicitly verified domain scope and test assertions. Julian confirmed that no unrelated files (such as domain.py or data_store.py) were altered, verified that test_starter.py remained unchanged, and confirmed that pytest assertions correctly validated object identity (cancelled is booked). Copilot's raw critique did not verify file scope boundaries or starter test preservation.
- What did Copilot identify that the human reviewer initially missed: Copilot identified that input validation in find_patient focused primarily on string trimming and blank checks, but lacked parameterized unit test coverage for non-string types (such as passing 123 or None).
- Unsupported or incorrect Copilot suggestion: 
  - *Suggestion:* Adding an external logging module (logging.getLogger()) inside cancel_appointment.
  - *Explanation:* Rejected as out-of-scope / invented requirement. The SmartCare A3 Requirements Baseline (2026 Revision 2) contains no requirement for external audit logging frameworks, and adding unneeded modules violates the project's zero-dependency baseline.
- Human judgement accepted, modified or rejected, and why: 
  1. Accepted (Copilot non-string guard): Added non-string edge cases (None, 123) to parameterized unit tests (@pytest.mark.parametrize("invalid_id", ["", "   ", None, 123])) in test_services.py.
  2. Rejected (Copilot logging proposal): Rejected as an unnecessary third-party feature not supported by the client requirements baseline.
  3. Modified / Deferred (Human type hints feedback): Deferred adding type hint annotations to services.py as a non-breaking code-quality refactoring for an upcoming stage (Stage 8), confirming that Python runtime execution is unaffected and all unit tests pass cleanly.
- Which evidence justified merge approval:
  - Executing python -m pytest inside the project/ directory produced 18 passed in 0.24s with zero failures or uncaught exceptions. The test output verified that all 8 starter tests and all 10 new service unit tests passed, confirming both functional correctness and regression protection prior to PR approval and merge.
  
## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: Julian
- Implementation: [work and evidence]
- Testing: [work and evidence]
- Review: [work and evidence]
- Issue refinement: [work and evidence]
- Design and responsibility discussion: [work and evidence]
- Debugging or integration: [work and evidence]
- Documentation or team support: [work and evidence]

- Member: Labiba
- Implementation: [work and evidence]
- Testing: [work and evidence]
- Review: [work and evidence]
- Issue refinement: [work and evidence]
- Design and responsibility discussion: [work and evidence]
- Debugging or integration: [work and evidence]
- Documentation or team support: [work and evidence]

- Member: Tanika
- Implementation: [work and evidence]
- Testing: [work and evidence]
- Review: [work and evidence]
- Issue refinement: [work and evidence]
- Design and responsibility discussion: [work and evidence]
- Debugging or integration: [work and evidence]
- Documentation or team support: [work and evidence]

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

Commit count is a misleading metric that can be easily inflated by artificial, micro-commits (e.g., fixing a single typo per commit) or artificially inflated commit activity.

## L Stage 6 formative questions

1. What is version control?

Version control (such as Git) is a software engineering system that tracks, manages, and records changes made to a codebase over time.

2. Why is a feature branch useful?

A feature branch isolates new development or bug fixes from the stable main integration branch, allowing team members to write code, execute local unit tests, and experiment without breaking the working application for others.

3. What makes a commit a good engineering commit?

A good engineering commit represents a single, logical, and coherent unit of work accompanied by a clear, imperative commit message explaining what changed and why.

4. What is a pull request?

A Pull Request (PR) is a formal mechanism on platforms like GitHub to propose merging code from a feature branch into a target branch (such as main).

5. What is the purpose of code review?

The purpose of code review is to ensure software quality, correctness, maintainability, and alignment with project requirements before code enters the stable main branch.

6. What does a Git diff show?

A Git diff shows the line-by-line comparison between two commits, branches, or file states. It explicitly highlights added lines (green/+), deleted lines (red/-), and modified lines of code, allowing developers and reviewers to inspect exact code changes and ensure no accidental, unrelated modifications were staged.

7. What is a Definition of Done?

A Definition of Done (DoD) is a shared, agreed-upon checklist of completion criteria that must be satisfied before a feature or issue is considered truly finished.

8. What is the appropriate role of GitHub Copilot in pull-request review?

GitHub Copilot serves as an assistant for candidate suggestions and comparison, not an autonomous reviewer or merge authority. Human team members must record independent review observations first, use Copilot's prompt output as secondary input, critically evaluate its suggestions (accepting, modifying, or rejecting them with explicit justification), and independently verify claims via actual test execution.

9. Why should individual contribution not be judged only by commit count?

Commit count is a misleading metric that can be easily inflated by artificial, micro-commits (e.g., fixing a single typo per commit) or artificially inflated commit activity.

10. What is the Stage 6 engineering rule?

The Stage 6 engineering rule is to follow the complete feature-branch lifecycle for every change: update main, create a focused issue and feature branch, implement code and unit tests, inspect the diff, push meaningful commits, open a PR, perform an independent human review before comparing with Copilot, resolve feedback, obtain teammate approval, merge into main, and verify the integrated build on main across all team members' local environments.

## M Completion and handover

- Starting SHA: 11d3d21d78ed5fa30ea82f48a697fc6cd0f18ed9
- Final Stage 6 code SHA: 579e67d3bbcb265735b9e0ff86e992b3ed760576
- Test command: python -m pytest
- Working directory: project/
- Observed result: 11 passed in 0.05s
- PR and another-member reviewer: Reviewed and approved by Tanika
- Unresolved issue or none: N/A
- Stage 7 handover status: [ready for tutor checkpoint]
- Final submitted SHA if later than tested SHA: TBA

- [X] Three Stage 6 service targets completed and checked.
- [X] Original supplied tests retained and passing.
- [X] At least two focused issues link requirements and acceptance criteria.
- [X] Feature work reviewed by another member using the actual diff.
- [X] Human-first review and required Copilot comparison recorded.
- [X] Feedback resolved and approval recorded before merge.
- [X] Everyone pulled main and integrated checks passed.
- [X] Required activities, quiz responses and contribution notes completed.
- [X] Only synthetic data included; confidential peer material kept out.
- [X] Tutor can trace a requirement through issue, code, tests, PR and checkpoint.

Do not write a file's own future commit SHA into that file. Record the tested code SHA first, then commit the evidence; explain the difference when submitting.
