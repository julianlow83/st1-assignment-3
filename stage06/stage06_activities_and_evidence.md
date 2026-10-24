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
| Branch naming | [response] |
| Commit message convention | [response] |
| PR size | [response] |
| Another-member review requirement | [response] |
| Merge rule | [response] |
| Significant Copilot disclosure rule | [response] |

## F Issue and backlog index

Create at least two focused issues. Add a linked practitioner-lookup issue or an explicit supporting criterion with the tutor if needed to cover all three service targets.

| Issue link | Requirement | Owner                  | Acceptance criteria or precise link                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Status |
|---|---|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---|
| https://github.com/julianlow83/st1-assignment-3/issues/2#issue-6008989965 | FR-02: Patient Search | Julian, Labiba, Tanika | 1. Searching with a valid, non-blank patient_id returns the exact stored Patient object. <br/> 2. Inputs are trimmed of surrounding whitespace prior to lookup and are strictly case-sensitive.<br/>3. Valid but absent patient_id raises LookupError.<br/>4. Blank, empty, or non-string IDs raise ValueError.<br/>5. Operations preserve stored entity state.                                                                                                                                       | In Progress |
| https://github.com/julianlow83/st1-assignment-3/issues/2#issue-6008989965 | FR-06 / FR-07: Appointment Cancellation with Retained History | Julian, Labiba, Tanika | 1. Cancelling a SCHEDULED appointment executes Appointment.cancel(), updates status to CANCELLED, and returns the same object.<br/>2. The cancelled appointment remains stored in session history and retrievable via lookups (FR-07).<br/>3. Cancelling an already CANCELLED or COMPLETED appointment raises ValueError without altering state.<br/>4. Valid unknown ID raises LookupError; blank or invalid ID raises ValueError.<br/>5. Does not delete the object or create a replacement record. | In Progress |

## G Pull request evidence

Repeat this block per PR. Record actual events, not planned approvals.

- PR link and title: [response]
- Linked issue and requirement: [response]
- Feature branch: [response]
- Changed behaviour: [response]
- Meaningful commits: [links]
- Test command, directory and observed result: [response]
- Another-member reviewer: [response]
- Human observations recorded before Copilot: [link and time]
- Requirement, responsibilities, test assertions and unrelated-scope checks: [response]
- Key feedback: [response]
- Author response/change and verification: [response]
- Reviewer recheck and approval: [link]
- Merge outcome and SHA: [response]
- Significant Copilot assistance: [summary or none]
- Linked issue closure: [response]
- Each member updated main: [member and confirmation]
- Integrated verification after merge: [command, directory, result and code SHA]

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

- Member and task: [response]
- Prompt/purpose and relevant issue/diff: [response]
- Summary of output: [response]
- Human check against actual code, requirements and tests: [response]
- Decision — Accept / Modify / Reject: [select]
- Reason: [response]
- Verification/evidence: [link and result]

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: [response]
- Copilot noticed: [response]
- Overlap: [response]
- What did the human reviewer notice that Copilot did not: [response]
- What did Copilot identify that the human reviewer initially missed: [response]
- Unsupported or incorrect Copilot suggestion: [response or none identified with explanation]
- Human judgement accepted, modified or rejected, and why: [response]
- Which evidence justified merge approval: [response]

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: [response]
- Implementation: [work and evidence]
- Testing: [work and evidence]
- Review: [work and evidence]
- Issue refinement: [work and evidence]
- Design and responsibility discussion: [work and evidence]
- Debugging or integration: [work and evidence]
- Documentation or team support: [work and evidence]

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

[response]

## L Stage 6 formative questions

1. What is version control?

[response]

2. Why is a feature branch useful?

[response]

3. What makes a commit a good engineering commit?

[response]

4. What is a pull request?

[response]

5. What is the purpose of code review?

[response]

6. What does a Git diff show?

[response]

7. What is a Definition of Done?

[response]

8. What is the appropriate role of GitHub Copilot in pull-request review?

[response]

9. Why should individual contribution not be judged only by commit count?

[response]

10. What is the Stage 6 engineering rule?

[response]

## M Completion and handover

- Starting SHA: [response]
- Final Stage 6 code SHA: [response]
- Test command: [response]
- Working directory: [response]
- Observed result: [response]
- PR and another-member reviewer: [links]
- Unresolved issue or none: [response]
- Stage 7 handover status: [ready for tutor checkpoint / unresolved work]
- Final submitted SHA if later than tested SHA: [response and evidence-only difference]

- [ ] Three Stage 6 service targets completed and checked.
- [ ] Original supplied tests retained and passing.
- [ ] At least two focused issues link requirements and acceptance criteria.
- [ ] Feature work reviewed by another member using the actual diff.
- [ ] Human-first review and required Copilot comparison recorded.
- [ ] Feedback resolved and approval recorded before merge.
- [ ] Everyone pulled main and integrated checks passed.
- [ ] Required activities, quiz responses and contribution notes completed.
- [ ] Only synthetic data included; confidential peer material kept out.
- [ ] Tutor can trace a requirement through issue, code, tests, PR and checkpoint.

Do not write a file's own future commit SHA into that file. Record the tested code SHA first, then commit the evidence; explain the difference when submitting.
