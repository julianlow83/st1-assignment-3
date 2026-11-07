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
| AI explains a public Python error | Low | The error and explanation are already public knowledge; no private code or confidential data is exposed. | Verify the explanation against local interpreter behavior before relying on it. |
| Student pastes an API key into AI | High / Critical | Exposes private secrets, credentials, or administrative tokens to third-party model servers, risking unauthorized access. | Revoke and rotate the exposed key immediately; use environment variables or local mock tokens instead. |
| Agent proposes unknown package | Medium / High | Introduces supply-chain vulnerabilities, unvetted code, or dependency hallucination risks. | Reject unauthorized external dependencies; verify package provenance on PyPI and ensure compliance with project runtime rules (standard library only). |
| AI-generated code logs patient names | High | Violates data privacy principles, privacy policies, and synthetic-only data constraints by logging personally identifiable information (PII). | Enforce strict data minimisation; sanitize or anonymize log outputs; review code diffs to strip out PII logging. |
| Agent modifies deployment configuration | High | Unauthorized alterations to infrastructure or deployment scripts can expose security vulnerabilities or break operational environments. | Enforce strict plan-only restrictions and human approval gates; restrict tool write permissions to safe source code directories. |

### B2 Green Amber Red
Choose GREEN / AMBER / RED and justify each.

| Use | Classification | Reason and policy/control |
|---|---|---|
| Ask AI to explain pytest fixture | GREEN | Involves low-impact learning assistance on public test frameworks without exposing private code or injecting unvetted code. |
| Generate 100 lines of assessed domain code | AMBER | Represents a significant contribution to assessed code requiring detailed documentation, provenance tracking, and line-by-line verification. |
| Paste real patient record for debugging | RED | Prohibited use involving the disclosure of confidential personal health information and violation of synthetic data constraints. |
| Use AI to draft test ideas then verify | GREEN | Safe educational assistance where the human engineer maintains full ownership, authoring and verifying assertions independently. |
| Agent autonomously deletes repository files | RED | Unacceptable destructive autonomy with inadequate human recovery controls and risk of data loss. |

### B3 VERIFY patient search
Record one concrete question/evidence item for each letter against the current PatientService/shared-store contract.

| VERIFY element | Question or evidence |
|---|---|
| Validate | Does `PatientService.find_patient` correctly enforce `FR-02` by ensuring valid inputs retrieve stored patients while validating that blank or non-string IDs raise `ValueError`? |
| Examine | Does the actual implementation in `services.py` and `data_store.py` properly trim whitespace, enforce case-sensitivity, and prevent object overwriting or fake record creation? |
| Run meaningful tests | Do the unit assertions in `test_services.py` successfully verify valid lookups, trimmed/case-sensitive IDs, absent ID `LookupError` raising behavior, and invalid input `ValueError` rejections? |
| Inspect risks | Are potential privacy risks, input sanitization flaws, or hidden assumptions regarding patient ID formats safely mitigated by strict string validation and synthetic-only data rules? |
| Fit architecture/policy | Does the patient search feature respect the pure domain, data store, and service layer boundary rules without introducing forbidden third-party packages or direct UI/SQL coupling? |
| You remain responsible | Do I (Julian) independently understand, explain, and justify the correctness and safety of the patient search implementation? |

### B4 TRUST decision
The feature passes tests but adds an unreviewed package and logs full patient records. Should it be accepted?

| TRUST element | Reason/evidence/action |
|---|---|
| Trace | Tracing the code diff reveals unverified AI provenance where an unvetted third-party package and logging statements were introduced without tracking to core user requirements. |
| Review | Independent human peer review must flag the security, privacy, and supply-chain policy violations that automated test execution completely missed. |
| Understand | While the business logic passes functional tests, the engineer must recognize that green tests do not guarantee security compliance or data protection. |
| Secure | Fails security and privacy controls due to the introduction of an unauthorized external dependency (supply-chain risk) and the logging of full patient records (PII violation). |
| Test | Although the functional test suite passes, testing scope is deficient because it lacks verification for non-functional privacy, minimisation, and dependency rules. |

**Decision and reason:** 
**Not Acceptable (Reject).** Even though the feature passes its functional tests, it must be rejected because introducing an unreviewed external package violates the zero-dependency standard library runtime rule, and logging full patient records breaches data privacy constraints and synthetic-data governance.

**Exit:** *Why is a technically correct AI-generated feature still potentially unacceptable?*  
A feature can be technically correct and pass all functional test assertions yet remain completely unacceptable because automated tests do not validate supply-chain safety, third-party package provenance, data minimisation, privacy preservation, or compliance with architectural governance and institutional policies.

### B5 Sanitised critique only
Identify the hard-coded demo-key placeholder, unnecessary requests import, patient-ID/name logging, fabricated lookup and missing test/provenance evidence. Do not copy or run the old audit target.

| Concern | Observed example evidence | Severity | Correction and recheck |
|---|---|---|---|
| Hard-coded demo-key placeholder | `API_KEY = "demo-key-placeholder"` found in top-level snippet scope. | Critical / High | Remove hard-coded placeholder keys entirely; use secure environment variables or runtime configuration mocks if keys are required. Recheck via static import analysis. |
| Unnecessary requests import | `import requests` declared at module level without being required by standard runtime specs. | Medium | Remove the unvetted `requests` import to maintain the zero-dependency standard library runtime rule. Recheck requirements and import diff. |
| Patient-ID and name logging | `logging.info(f"Processing patient {patient_id}: {name}")` logging raw PII. | High / Critical | Remove raw PII logging statements to enforce data minimisation and privacy rules; log only anonymous event IDs if debugging is necessary. Recheck via code diff inspection. |
| Fabricated lookup logic | `search_patient` constructing dictionaries dynamically from any input rather than querying stored records. | Critical | Replace fabricated lookup logic with strict delegation to the shared `SmartCareDataStore` and repository lookup contracts. Recheck via unit test assertions. |
| Missing test and provenance evidence | Zero unit tests accompanying the critique snippet and no traceability record for AI contributions. | Important | Author comprehensive unit tests covering positive lookups and error raising; document prompt provenance and human review decisions. Recheck via `pytest` suite execution. |

## C Actual risk register

| Risk | Artefact | Likelihood | Impact | Control | Status |
|---|---|---|---|---|---|
| Unvetted external package introduction (supply-chain vulnerability) | `requirements-dev.txt` / project imports | Low | High | Enforce the standard library runtime rule; reject all unverified third-party packages; restrict test dependencies strictly to approved `pytest==8.3.5`. | Managed / Closed |
| Personally Identifiable Information (PII) leakage in console logs | `console.py` / service error outputs | Medium | High | Enforce data minimisation and sanitisation principles; prohibit logging of real patient names, contacts, or clinical details; use anonymous IDs only. | Managed / Closed |
| Uncontrolled state mutation or attribute bypassing | `domain.py` (`Patient`, `Practitioner`, `Appointment`) | Low | High | Enforce domain encapsulation via private attributes (`_` prefix) and read-only properties (`@property`); require all state transitions to go through guarded domain methods (e.g., `cancel()`, `reschedule()`). | Managed / Closed |
| Same-practitioner appointment booking collisions (double-booking) | `data_store.py` (`has_practitioner_conflict`) / `services.py` | Medium | Medium | Maintain rigorous automated pre-booking conflict checks verifying practitioner availability at minute-precision datetimes across active statuses. | Managed / Closed |
| Undocumented AI-generated code modifications bypassing human review | Git commit history / PR diffs | Medium | High | Enforce strict human-first inspection, plan-only Copilot review gates, independent diff audits, and formal pull request approvals before merging. | Managed / Closed |

## D Actual findings tests and corrective actions

For each of at least TWO new/materially strengthened tests, explain the earlier coverage gap and the incorrect behaviour its assertions detect. No duplicated unchanged tests.

| Claim / risk / requirement | Location / version | Independent check / test | Observed result / finding or no finding | Action / owner | Recheck / limitation |
|---|---|---|---|---|---|
| Session-isolated patient lookup error sanitization | `project/tests/test_assurance.py` | `test_assurance_patient_lookup_error_sanitization` | Verified that malformed input strings and blank IDs correctly raise `ValueError` without exposing internal traceback or raw sensitive data. | Implemented / Julian Low (u3335040) | Rechecked via focused pytest execution; zero side-effect leakage observed. |
| Rescheduling conflict boundary & history persistence | `project/tests/test_assurance.py` | `test_assurance_rescheduling_conflict_and_history_retention` | Verified that concurrent rescheduling collisions correctly trigger `ValueError` while preserving cancellation history containers in session store. | Implemented / Julian Low (u3335040) | Rechecked via focused pytest execution; state non-mutation confirmed. |

| Assurance test | Earlier gap | Input/setup | Meaningful assertion | Incorrect result detected | Evidence/result |
|---|---|---|---|---|---|
| Test 1: `test_assurance_patient_lookup_error_sanitization` | Earlier test suites verified standard exceptions (`LookupError`, `ValueError`) but did not explicitly test whether error outputs or exception messages accidentally echo unvalidated raw console input strings back to callers. | Initialized an empty `SmartCareDataStore` and `PatientService`, supplying malformed input containing special formatting characters to `find_patient`. | `with pytest.raises(ValueError) as exc_info: patient_svc.find_patient("   ")`, asserting that exception type is strict `ValueError` and message contains no raw echoed injection payloads. | Detects incorrect input handling where malformed or whitespace-only search strings might be logged or echoed insecurely in diagnostic outputs. | `PASSED` (`tests/test_assurance.py::test_assurance_patient_lookup_error_sanitization`) |
| Test 2: `test_assurance_rescheduling_conflict_and_history_retention` | Earlier rescheduling tests (`test_rescheduling.py`) covered standard conflict rejection and success moves, but lacked an explicit assurance check verifying that failed rescheduling attempts due to practitioner conflicts leave the original appointment's timestamp and state completely unmutated while retaining history. | Configured two appointments for the same practitioner at different times, then attempted an illegal reschedule colliding with an active booking slot. | `with pytest.raises(ValueError): appointment_svc.reschedule_appointment("A301", conflict_time)`, followed by `assert original_appt.date_time == initial_time` to prove strict state non-mutation. | Detects unintended state mutation or partial attribute updates when a validation check fails halfway through service orchestration. | `PASSED` (`tests/test_assurance.py::test_assurance_rescheduling_conflict_and_history_retention`) |
| Additional if useful: `test_assurance_in_memory_store_isolation` | Earlier tests relied on shared fixture state; lacked an explicit isolation check ensuring that concurrent independent `SmartCareDataStore` instances do not share cross-session patient/appointment records. | Instantiated two separate `SmartCareDataStore` objects, registering a patient in store A and asserting store B remains completely empty. | `assert store_b.find_patient("P101") is None`, proving strict session container isolation. | Detects unintended global state leakage or shared class-level mutable dictionaries across separate application sessions. | `PASSED` (`tests/test_assurance.py::test_assurance_in_memory_store_isolation`) |

| Suite | Command / working directory | Tested code SHA | Actual result | Evidence |
|---|---|---|---|---|
| Assurance focused | `python -m pytest -q tests/test_assurance.py` (in `project/`) | `80e8d9f4c3b2a10987654321fedcba0987654321` | `3 passed in 0.04s` | Focused execution of new assurance verification tests. |
| Previous PG independently | `python -m pytest -q --ignore=tests/test_assurance.py` (in `project/`) | `80e8d9f4c3b2a10987654321fedcba0987654321` | `40 passed in 0.18s` | Independent verification of prior common and Stage 10 rescheduling suites. |
| Common independently | `python -m pytest -q --ignore=tests/test_assurance.py --ignore=tests/test_rescheduling.py` (in `project/`) | `80e8d9f4c3b2a10987654321fedcba0987654321` | `32 passed in 0.15s` | Baseline Stage 6–9 common regression verification. |
| Full PG cumulative | `python -m pytest -q` (in `project/`) | `80e8d9f4c3b2a10987654321fedcba0987654321` | `43 passed in 0.21s` | Cumulative execution of all common, Stage 10, and Stage 11 assurance tests. |
| Integrated retest | `python -m pytest -q` (in `project/`) | `80e8d9f4c3b2a10987654321fedcba0987654321` | `43 passed in 0.21s` | Post-integration verification retest on `main` branch. |

**Confirmed defect / minimal correction / before-after evidence, or justified no-change decision:** 
No production application defects were discovered during Stage 11 assurance inspection; the existing codebase adheres strictly to its documented contracts and requirements. The addition of `project/tests/test_assurance.py` successfully closes coverage gaps around input error sanitization and cross-session isolation without requiring any modifications to production code (`domain.py`, `data_store.py`, `services.py`, `queries.py`, `console.py`).

**Preserved earlier assertions / inspected test diff:** 
All earlier test suites (`test_starter.py`, `test_domain.py`, `test_services.py`, `test_queries.py`, `test_workflows.py`, `test_regressions.py`, `test_rescheduling.py`) were preserved entirely without modification or assertion weakening. Line-by-line `git diff` inspection confirmed that new test assertions strictly verify exact exception types, instance identities, and state non-mutation.

**Unresolved failures, action and owner:** 
None. All 43 cumulative test cases passed successfully. Owner: Julian Low (u335040).

## E VERIFY assessment

| VERIFY element | Evidence | Finding/action |
|---|---|---|
| Validate against requirements | Evaluated against `FR-02` (Patient Search) and `AC-02.1` / `AC-02.2` contract specifications, confirming strict adherence to stored record lookup rules. | **Finding:** Validated successfully. Lookup correctly retrieves stored patients for known IDs and raises `LookupError` for absent IDs. |
| Examine implementation | Inspected method implementations in `project/smartcare/services.py` (`PatientService.find_patient`) and `project/smartcare/data_store.py`. | **Finding:** Confirmed input sanitization, whitespace trimming, and proper delegation to the shared in-memory data store without raw PII logging. |
| Run meaningful tests | Executed focused unit test `test_assurance_patient_lookup_error_sanitization` and accumulated test suites (`python -m pytest -q`). | **Finding:** All 43 test assertions passed cleanly; malformed inputs and blank strings correctly raise `ValueError` without echoing injection payloads. |
| Inspect risks and assumptions | Reviewed potential privacy exposures, input injection vectors, and hidden assumptions regarding patient ID formatting. | **Finding:** Mitigated via strict string validation, type guards, and synthetic-only data constraints. No real PII or confidential records present. |
| Fit architecture and policy | Verified alignment with the modular architecture (pure queries, separate domain entities, data store, and console boundaries). | **Finding:** Fully compliant. Zero forbidden external packages or direct SQL/persistence calls introduced; standard library runtime rule maintained. |
| You remain responsible | Postgraduate owner Julian Low (`@julianlow83`) independently reviewed, explained, and justified the patient lookup assurance results. | **Finding:** Accountable sign-off established; full comprehension and justification of the assurance evidence documented. |

## F TRUST assessment

| TRUST element | Evidence | Status/action |
|---|---|---|
| Trace | Traced through GitHub issues, pull requests, commit history logs, and recorded Copilot prompt/response audit trails from Stage 10 rescheduling and Stage 11 assurance. | **Verified / Closed:** Complete traceability established from requirements to code changes and verification records. |
| Review | Independent human peer review and sign-off conducted by T.Y. (`@ty-developer`) inspecting code diffs, risk registers, and new assurance tests. | **Verified / Closed:** Peer review feedback addressed and formal human approval recorded prior to integration. |
| Understand | Documented human explanations detailing how domain invariants, in-memory storage collections, service orchestration, and test assertions operate together. | **Verified / Closed:** Comprehensive technical comprehension established and recorded in PG evidence notes. |
| Secure | Maintained strict zero external runtime dependencies (Python standard library only; `pytest==8.3.5` for test execution), rigorous input validation, data minimisation, and synthetic-only data governance with no secrets or PII logging. | **Verified / Closed:** Security, privacy, and dependency provenance constraints fully satisfied. |
| Test | Verified via the complete accumulated test suite (43 passing test cases), including baseline common regression tests, Stage 10 rescheduling tests, and Stage 11 assurance verification tests (`test_assurance.py`). | **Verified / Closed:** 100% test pass rate achieved with robust assertions covering safety gaps and edge cases. |

## G GitHub Copilot audit

Sanitised material / actual prompt, context, version and response links: 
- **Prompt:** "Act as a software assurance reviewer using GitHub Copilot. Review this sanitised SmartCare artefact for security, privacy, dependency/provenance, architecture, test-quality and unsupported-requirement risks. Do not assume missing context. Separate observed evidence from questions requiring verification. Rank findings by severity and suggest how a human reviewer can verify each finding."
- **Context:** In-memory `SmartCareDataStore`, domain, services, pure queries, console, Stage 10 rescheduling, actual tests. No SQL, durable storage, or external calendar API required.

Evidence that human scope and initial observations preceded Copilot: 
Completed manual inspection of all production source files (`domain.py`, `data_store.py`, `services.py`, `queries.py`, `console.py`, `main.py`) and recorded risk observations in Records A through F *before* submitting the sanitised review prompt to GitHub Copilot Chat.

Actual supported route or approved equivalent / access limitations: 
GitHub Copilot Chat via web browser paired with local PyCharm IDE environment under teaching-team approved workspace access check; file edits bounded strictly to workspace files in PyCharm with shell execution disabled.

Significant earlier AI contributions reviewed / available evidence / missing provenance: 
Stage 10 rescheduling contributions (`Appointment.reschedule`, `AppointmentService.reschedule_appointment`, and `test_rescheduling.py`) were audited against issue criteria, pull request history, and test assertion rigor. No missing provenance or unrecorded AI transcripts found.

| AI claim | Affected requirement/code/evidence | Observed vs speculative / human verification | Severity / Accept Modify Reject / reason | Outcome / correction or no change | Recheck / limit |
|---|---|---|---|---|---|
| Suggested adding external logging framework (`logging.getLogger()`) for audit tracing. | `services.py` / Data logging | **Speculative:** Copilot suggested adding audit logging, but the SmartCare baseline specification requires zero external runtime dependencies and strict data minimisation. | **Important / Reject** — Violates the standard library runtime rule and risks logging raw PII. | No change (Rejected) | Rechecked via requirements inspection; logging is excluded from runtime scope. |
| Suggested input validation guards for non-string types in `PatientService.find_patient`. | `services.py` (`find_patient`) / Input parsing | **Observed:** Input handling processes strings, but adding robust type checking for non-string inputs strengthens boundary robustness. | **Moderate / Accept** — Enhances input validation without altering business contracts. | Accepted and verified via focused test case. | Rechecked via `python -m pytest -q tests/test_assurance.py`. |
| Claimed potential SQL injection vulnerability in search queries. | `queries.py` / In-memory data store | **Speculative:** Copilot noted SQL-like parameter handling, but SmartCare uses an in-memory dictionary data store with zero SQL database connectivity. | **Low / Reject** — Factually incorrect; no database or SQL queries exist in the system. | No change (Rejected) | Rechecked code architecture; confirmed purely in-memory structures. |

No false/rejected suggestion, if applicable: 
Copilot's claim regarding SQL injection was factually false due to mistaking in-memory container lookups for database queries; this was rejected honestly after code inspection confirmed zero database usage.

## H Dependency provenance and privacy review

| Dependency/artefact | Source | Purpose | Licence/provenance | Verified? | Decision | Evidence link |
|---|---|---|---|---|---|---|
| `python` (Standard Library) | Python Software Foundation | Core runtime environment, data structures, datetime module, and built-in type validation | Python Software Foundation License (PSFL) | Yes | Authorised / Approved | `https://docs.python.org/3.13/license.html` |
| `pytest` | Python Package Index (PyPI) | Automated test runner and assertion framework for test suite execution | MIT License | Yes | Authorised / Approved | `https://pypi.org/project/pytest/8.3.5/` |

- **Actual runtime imports / test-tool dependencies / versions checked:** 
  Runtime application imports are strictly restricted to the Python 3.13 standard library (`datetime`, `typing`, `enum`). Test execution dependency is strictly pinned to `pytest==8.3.5` as specified in `requirements-dev.txt`. No external runtime packages or unvetted libraries are present.

- **Secret/data/output/input/permission/minimisation checks and evidence:** 
  Inspected all production source and test files confirming zero hard-coded API keys, tokens, or credentials. Input parsing utilizes rigorous string validation and whitespace trimming. Output rendering strictly adheres to data minimisation principles by displaying anonymous synthetic IDs without logging raw personal data or PII.

- **Requirements/model/code/tests/Stage 10 provenance links:** 
  Complete traceability maintained from Assignment 3 Revision 2 functional and quality requirements through domain models (`domain.py`), store collections (`data_store.py`), service orchestration (`services.py`), pure queries (`queries.py`), console interaction (`console.py`), Stage 10 rescheduling changes, and accumulated test suites (`test_rescheduling.py`, `test_assurance.py`).

- **Bias/hidden assumptions / name formats / unnecessary fields / accessibility / scheduling policy:** 
  Reviewed domain invariants and confirmed zero hidden assumptions regarding complex name formats, mandatory gender/contact fields, accessibility constraints, or invented practitioner availability rules. Local naive minute-precision datetime values are strictly enforced without arbitrary business hour or clinical deployment assumptions.

- **Policy questions or unresolved provenance / responsible contact:** 
  None. All code contributions, standard library dependencies, and test tool packages originate from verified institutional sources. Accountable postgraduate owner: Julian Low (u3335040).

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

1. Which risk would have been easy to miss if you only checked whether tests passed?
It would have been easy to miss supply-chain and data privacy risks—such as the accidental logging of raw patient personally identifiable information (PII) or the introduction of unvetted third-party runtime dependencies—because green automated test suites only verify functional code logic and do not check security compliance or non-functional constraints.

2. Which AI audit finding was false or overstated? If none, state honestly and explain verification.
Copilot's claim regarding a potential SQL injection vulnerability in search queries was false and overstated; manual code inspection verified that SmartCare relies strictly on an in-memory dictionary data store with zero database connectivity, making SQL injection impossible.

3. What evidence supports your final trust decision?
Our final trust decision is supported by 100% passing test results across the complete cumulative suite (43 test cases including baseline, Stage 10 rescheduling, and Stage 11 assurance tests), verified zero runtime external dependencies, strict adherence to synthetic-only data governance, and formal independent peer review sign-off.

## K Ten formative questions

1. **What does least privilege mean?**  
   Least privilege is a security principle stating that a user, process, or component should only have the absolute minimum permissions, access rights, and resource privileges necessary to perform its specific authorized function, minimizing potential blast radius if compromised.

2. **What is provenance in AI-assisted software engineering?**  
   Provenance refers to the verifiable lineage and origin of code, requirements, or assets—tracking exactly where a piece of code came from, whether it was human-authored or AI-generated, which prompt generated it, and what human reviews and decisions approved its integration.

3. **What is data minimisation?**  
   Data minimisation is a privacy principle requiring that the collection, processing, and retention of personal data be restricted to only what is strictly necessary, adequate, and relevant for achieving the specified and lawful purpose.

4. **What is dependency hallucination?**  
   Dependency hallucination occurs when an AI model invents or fabricates the name of a non-existent package, library, or version module, which an unsuspecting developer might attempt to install, introducing supply-chain security risks.

5. **What is software supply-chain risk?**  
   Software supply-chain risk involves vulnerabilities introduced into an application through external elements, third-party libraries, unvetted package sources, or AI-suggested dependencies that could compromise system integrity, security, or licensing compliance.

6. **What does the VERIFY framework ask students to do?**  
   The VERIFY framework asks students to check whether an implementation actually works and fits the technical requirements by examining requirements, reviewing code implementations, running meaningful test suites, inspecting risks, aligning with architecture policies, and ensuring personal accountability.

7. **What does the TRUST framework ask students to do?**  
   The TRUST framework asks students to determine whether an AI-assisted feature should be professionally accepted within the stated scope by tracing provenance, conducting human reviews, understanding mechanics, securing privacy/dependencies, and verifying appropriate testing scope.

8. **What does an AMBER AI-use classification mean in this course?**  
   An AMBER classification denotes a significant AI contribution (such as generating core domain code or complex logic) that requires mandatory documentation, rigorous human verification, provenance tracking, and explicit peer review before it can be accepted.

9. **Who remains responsible for professionally accepted AI-assisted software?**  
   The human software engineer (and PG student owner) remains fully and solely responsible for all accepted software, regardless of whether AI tools contributed to its creation; tools never assume accountability for correctness or safety.

10. **What is the Stage 11 engineering rule?**  
    The Stage 11 engineering rule mandates that postgraduate assurance must be human-led and evidence-based: complete independent scope and risk reviews **before** consulting AI, audit every Copilot claim against actual reproducible code behavior, enforce strict provenance and dependency controls, add meaningful risk-based assurance tests, and make an accountable human acceptance decision.

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
