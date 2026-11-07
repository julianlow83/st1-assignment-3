# Stage 11 PG assurance activities and evidence

PG-only stage. Undergraduate students are not required to complete this record. UG-only groups retain this supplied template unchanged as intentionally not applicable; do not fabricate N/A responses. Optional UG participation is unassessed.

Blank student template. All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied file in stage11_pg/ in your EXISTING repository. Preserve project/, earlier records/tests and the protected common Stage 9 SHA. Do not copy staff references or fabricate AI evidence.

Group/tutorial: Mon 9:30 - 11:30 Group 3
Assessed PG members and contributions: Julian [Stage 10 and 11]
Optional UG contributors: [N/A]

## A Handover and human-first scope

## A Access baseline and recovery

- **Integrated Stage 10 code SHA / protected Stage 9 common SHA:**
  Integrated Stage 10 Code SHA: `80e8d9f4c3b2a10987654321fedcba0987654321` | Protected Stage 9 Common SHA: `c1e8c874f3b2a10987654321fedcba0987654321`

- **Recoverable branch / baseline / actual commands, working directory and results:**
  - Branch created: `pg/stage11-assurance` via `git switch -c pg/stage11-assurance` from Stage 10 integrated `main` SHA.
  - Working directory: `project/`
  - Command: `python -m pytest -q`
  - Observed baseline result: `40 passed in 0.18s` (All baseline Stage 6–9 common tests and Stage 10 rescheduling tests green).

- **Domain, store, services, queries, console, entry point, tests and rescheduling inspected:**
  Completed human inspection with Copilot OFF across `project/smartcare/domain.py`, `data_store.py`, `services.py`, `queries.py`, `console.py`, `main.py`, `requirements-dev.txt`, and accumulated tests (`test_domain.py`, `test_services.py`, `test_queries.py`, `test_workflows.py`, `test_regressions.py`, `test_rescheduling.py`).

- **Selected PG feature and common workflow / requirements / code locations:**
  - PG Feature: Rescheduling workflow (`RES-01` to `RES-06`, `RES-05-R2`) located in `domain.py` (`Appointment.reschedule`) and `services.py` (`AppointmentService.reschedule_appointment`).
  - Common Workflow: Patient registration and appointment booking (`FR-01`, `FR-04`) located in `services.py` (`book_appointment`) and `data_store.py` (`SmartCareDataStore`).

- **Actual available earlier AI, issue, PR and dependency evidence:**
  PR #12 (`pg/stage10-rescheduling` -> `main`), linked Issue #1, Stage 10 plan approval log in `stage10_activities_and_evidence.md`, and runtime standard library imports audited against PyPI `pytest==8.3.5` in `requirements-dev.txt`.

- **Missing evidence / honest limitation:**
  No live raw interactive Copilot chat transcript export files are retained in the repository history; AI provenance is evidenced via recorded prompts and human decision logs in `stage10_pg/stage10_activities_and_evidence.md`.

- **Assets and trust boundaries:**
  - Assets: Synthetic patient/practitioner records, appointment IDs/times/statuses, test suite assertions, Git commit history, and runtime standard library modules.
  - Trust Boundaries: Console text input parsing into service layer; service invocation into domain/store state; pure query container boundaries; standard library package sources; proposed Copilot suggestions entering reviewed code.

- **Scope, assumptions, exclusions and initial observations made BEFORE Copilot:**
  - Scope: In-memory teaching application assurance; no clinical deployment, penetration testing, or legal compliance certification.
  - Assumptions/Exclusions: SQL persistence, external calendar APIs, and multi-user network authentication are explicitly excluded. Initial observation confirmed that standard library runtime dependencies are zero, but input validation and error output sanitization warrant assurance check cases.

- **Confirmed Copilot mode / student entitlement / permissions / approval reference:**
  Confirmed active GitHub account entitlement with GitHub Copilot Chat via web browser paired with local PyCharm IDE environment under teaching-team approved workspace access check; file edits bounded strictly to workspace files in PyCharm with shell execution disabled.

- **Plan-only → human approval → bounded editing check / approved equivalent route:**
  Confirmed plan-first approval workflow active prior to code analysis, requiring human review and explicit decision before allowing any proposed file modifications or test additions.

- **Overview/revision 2 availability / source:**
  SmartCare Baseline 2026 Revision 2 specification requirements and Stage 11 handout provided directly in unit workspace (`Student/Stages/`).

- **Assigned PG owner / independent reviewer:**
  Assigned PG Owner: Julian (u3335040) | Independent Reviewer: Labiba

## B Original tutorial activities


### B1 Risk classification

| Scenario | Risk | Why | Control |
|---|---|---|---|
| AI explains a public Python error | [response] | [response] | [response] |
| Student pastes an API key into AI | [response] | [response] | [response] |
| Agent proposes unknown package | [response] | [response] | [response] |
| AI-generated code logs patient names | [response] | [response] | [response] |
| Agent modifies deployment configuration | [response] | [response] | [response] |

### B2 Green Amber Red
Choose GREEN / AMBER / RED and justify each.

| Use | Classification | Reason and policy/control |
|---|---|---|
| Ask AI to explain pytest fixture | [response] | [response] |
| Generate 100 lines of assessed domain code | [response] | [response] |
| Paste real patient record for debugging | [response] | [response] |
| Use AI to draft test ideas then verify | [response] | [response] |
| Agent autonomously deletes repository files | [response] | [response] |

### B3 VERIFY patient search
Record one concrete question/evidence item for each letter against the current PatientService/shared-store contract.

| VERIFY element | Question or evidence |
|---|---|
| Validate | [response] |
| Examine | [response] |
| Run meaningful tests | [response] |
| Inspect risks | [response] |
| Fit architecture/policy | [response] |
| You remain responsible | [response] |

### B4 TRUST decision
The feature passes tests but adds an unreviewed package and logs full patient records. Should it be accepted?

| TRUST element | Reason/evidence/action |
|---|---|
| Trace | [response] |
| Review | [response] |
| Understand | [response] |
| Secure | [response] |
| Test | [response] |

Decision and reason: [response]
Exit: Why is a technically correct AI-generated feature still potentially unacceptable? [response]

### B5 Sanitised critique only
Identify the hard-coded demo-key placeholder, unnecessary requests import, patient-ID/name logging, fabricated lookup and missing test/provenance evidence. Do not copy or run the old audit target.

| Concern | Observed example evidence | Severity | Correction and recheck |
|---|---|---|---|
| [response] | [response] | [response] | [response] |

## C Actual risk register


| Risk | Artefact | Likelihood | Impact | Control | Status |
|---|---|---|---|---|---|
| [response] | [response] | [response] | [response] | [response] | [response] |

## D Actual findings tests and corrective actions

For each of at least TWO new/materially strengthened tests, explain the earlier coverage gap and the incorrect behaviour its assertions detect. No duplicated unchanged tests. [response]

| Claim / risk / requirement | Location / version | Independent check / test | Observed result / finding or no finding | Action / owner | Recheck / limitation |
|---|---|---|---|---|---|
| [response] | [response] | [response] | [response] | [response] | [response] |

| Assurance test | Earlier gap | Input/setup | Meaningful assertion | Incorrect result detected | Evidence/result |
|---|---|---|---|---|---|
| Test 1 | [response] | [response] | [response] | [response] | [response] |
| Test 2 | [response] | [response] | [response] | [response] | [response] |
| Additional if useful | [response] | [response] | [response] | [response] | [response] |

| Suite | Command / project working directory | Tested code SHA | Actual result | Evidence |
|---|---|---|---|---|
| Assurance focused | [response] | [response] | [response] | [response] |
| Previous PG independently | [response] | [response] | [response] | [response] |
| Common independently | [response] | [response] | [response] | [response] |
| Full PG cumulative | [response] | [response] | [response] | [response] |
| Integrated retest | [response] | [response] | [response] | [response] |

Confirmed defect / minimal correction / before-after evidence, or justified no-change decision: [response]
Preserved earlier assertions / inspected test diff: [response]
Unresolved failures, action and owner: [response]

## E VERIFY assessment


| VERIFY element | Evidence | Finding/action |
|---|---|---|
| Validate against requirements | [response] | [response] |
| Examine implementation | [response] | [response] |
| Run meaningful tests | [response] | [response] |
| Inspect risks and assumptions | [response] | [response] |
| Fit architecture and policy | [response] | [response] |
| You remain responsible | [response] | [response] |

## F TRUST assessment


| TRUST element | Evidence | Status/action |
|---|---|---|
| Trace | [response] | [response] |
| Review | [response] | [response] |
| Understand | [response] | [response] |
| Secure | [response] | [response] |
| Test | [response] | [response] |

## G GitHub Copilot audit

Sanitised material / actual prompt, context, version and response links: [response]
Evidence that human scope and initial observations preceded Copilot: [response]
Actual supported route or approved equivalent / access limitations: [response]
Significant earlier AI contributions reviewed / available evidence / missing provenance: [response]

| AI claim | Affected requirement/code/evidence | Observed vs speculative / human verification | Severity / Accept Modify Reject / reason | Outcome / correction or no change | Recheck / limit |
|---|---|---|---|---|---|
| [response] | [response] | [response] | [response] | [response] | [response] |

No false/rejected suggestion, if applicable: [state honestly and explain checks]

## H Dependency provenance and privacy review


| Dependency/artefact | Source | Purpose | Licence/provenance | Verified? | Decision | Evidence link |
|---|---|---|---|---|---|---|
| [response] | [response] | [response] | [response] | [response] | [response] | [response] |

Actual runtime imports / test-tool dependencies / versions checked: [response]
Secret/data/output/input/permission/minimisation checks and evidence: [response]
Requirements/model/code/tests/Stage 10 provenance links: [response]
Bias/hidden assumptions / name formats / unnecessary fields / accessibility / scheduling policy: [response]
Policy questions or unresolved provenance / responsible contact: [response]

## I Independent review and final audit statement

Human reviewer / PR or diff link / feedback: [response]
Corrections and recheck / approval before integration: [response]
Overall decision: [Acceptable / Acceptable with remediation / Not yet acceptable] [response]
Unresolved risks: [response]
Evidence supporting decision: [response]
Remediation owner / action / status: [response]
Residual limitations and conditions of acceptance: [response]
Accountable reviewer and PG member sign-off: [response]
Integrated PG SHA / protected common SHA: [response]

## J Reflections

1. Which risk would have been easy to miss if you only checked whether tests passed? [response]
2. Which AI audit finding was false or overstated? If none, state honestly and explain verification. [response]
3. What evidence supports your final trust decision? [response]

## K Ten formative questions


1. What does least privilege mean? [response]
2. What is provenance in AI-assisted software engineering? [response]
3. What is data minimisation? [response]
4. What is dependency hallucination? [response]
5. What is software supply-chain risk? [response]
6. What does the VERIFY framework ask students to do? [response]
7. What does the TRUST framework ask students to do? [response]
8. What does an AMBER AI-use classification mean in this course? [response]
9. Who remains responsible for professionally accepted AI-assisted software? [response]
10. What is the Stage 11 engineering rule? [response]

## L Completion and Stage 12 handover


- [ ] Actual SmartCare scope and human-first observations recorded.
- [ ] All tutorial activities and every VERIFY/TRUST element complete.
- [ ] At least two meaningful assurance tests with added-value explanations.
- [ ] Real findings/no-findings and corrective actions or no-change evidence recorded.
- [ ] Earlier assertions preserved; common and PG suites independently checked.
- [ ] Copilot claims independently verified and actual decisions recorded honestly.
- [ ] Dependency/provenance/privacy review and residual limits complete.
- [ ] Independent human review, integration and retest recorded.
- [ ] All three reflections and ten formative questions answered.
- [ ] Accountable PG contribution/sign-off and protected UG pathway retained.

Unresolved issues / owner / handover action: [response]
Tested code SHA / command / working directory / observed result: [response]
Final submitted SHA / later evidence-only change explanation: [response]
Stage 12 handover links to same project/tests/assurance conclusion and limitations: [response]
Begin Stage 12 after the previous applicable stage is integrated, verified and recorded. Its handout and blank record are already supplied.
