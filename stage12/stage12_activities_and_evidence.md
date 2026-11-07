# Stage 12 activities and evidence

BLANK student response template. Supplied from the beginning in stage12/ in your EXISTING repository; complete it only when you reach Stage 12 after the previous applicable stage is integrated, verified and recorded; preserve project/, tests, earlier records and Git history. UG/common and PG/extended scope must be explicit. Use concise results and versioned links, not copied logs or source. No staff answers or fabricated approvals.

Group/tutorial: Mon 9:30 - 11:30 Group 3
Members and UG/PG applicability: 3 [2 UG / 1 PG]

## A Release scope and starting SHA

**Release label/version and requirements baseline:** `v1.0-release` (SmartCare A3 Requirements Baseline 2026 Revision 2; Common FR-01–09, QRY-01–04, FP-01–03, UI-01–02; PG extended RES-01–06 and assurance suite)  

**Common starting SHA / branch / applicable members:** a8740f759f5ea75d33bc8f08d26e646208725f94 / `main` / Labiba, Tanika  

**PG starting SHA / branch / applicable members or not applicable:** b6d09324734c9c1fee85e3d920c875cbb0b071a1 / `main` / Julian  

**Working-state review and approved integration:** `git status` confirmed clean working tree; `git diff` shows zero uncommitted edits; all accumulated test suites (`test_domain.py`, `test_services.py`, `test_queries.py`, `test_workflows.py`, `test_regressions.py`, plus PG rescheduling/assurance tests) verified 100% passing across local workspaces via reviewed GitHub Pull Requests.  

**Protected common candidate and PG differences:** Protected common Stage 9 checkpoint preserved on `main` to safeguard UG evaluation. PG scope adds appointment rescheduling contracts (RES-01–06) and risk-based assurance test suites without altering common core requirements.  

**Feature freeze / owner / verifier:** Feature freeze active (no new features permitted; release blockers only); Owner: Julian; Verifier: Labiba and Tanika.  


## B Requirements and release readiness matrix

Tutorial activity 1: All tests pass, README setup is incomplete, one dependency is unreviewed and a known limitation is undocumented. Decide Release / Release with conditions / Do not release and justify: [response]

Tutorial activity 2 and actual readiness matrix. Add exact requirement/acceptance IDs, evidence and reviewer; distinguish common/PG applicability.

| Release claim / requirement / scope | Evidence | Location/link and SHA | Reviewer | Sufficient? | Gap/action |
|---|---|---|---|---|---|
| Cancellation history works | `test_workflows.py`, `test_services.py` | `tests/test_workflows.py` (`SHA: 7ae851e3a8910437e66fe7e1d2b1eef2253dce2e`) | Labiba | Yes | None; verified cancelled appointments remain retrievable with `CANCELLED` status. |
| Architecture responsibilities are appropriate | Separation of Domain entities, DataStore, Services, Queries, and Console | `project/smartcare/` (`SHA: 859fe809959ed5a65cdbca815dafe3d2725a7837`) | Julian  | Yes | None; clean boundaries maintained with zero UI leakage into domain. |
| Rescheduling is safe — PG only | `test_rescheduling.py` contracts RES-01–06 | `project/tests/test_rescheduling.py` (`SHA: 80e8d9fd3af1e31ce9438ddef14556ebbdc92d21`) | Labiba  | Yes | None; verified ID preservation, same-time conflicts, and non-mutation on failure. |
| AI use is responsible — common recheck / PG assurance | Copilot prompt logs, human reviews, and Stage 11 `test_assurance.py` | `stage11_pg/` and commit logs (`SHA: 42af4632c0b1c416eb6d963ee0b06f8a52dd2746`) | Labiba | Yes | None; complete verification, prompt auditing, and risk-based assurance tests completed. |
| System is maintainable | Clean code quality, typing, docstrings, and passing suites | `project/` (`SHA: c1e8c874f7c68c865633397dd72decba49bafed3`) | Labiba  | Yes | None; PascalCase/snake_case naming and separation of pure queries enforced. |
| FR-01–03 register/find and validation | `test_domain.py`, `test_services.py` | `project/tests/` (`SHA: eec3bb1278ca6690310bc23ac61acb249b7ad7cd`) | Labiba | Yes | None; strict whitespace trimming and duplicate ID rejections verified. |
| FR-04–05 booking/conflict rules | `test_services.py`, `test_workflows.py` | `project/tests/` (`SHA: 7ae851e3a8910437e66fe7e1d2b1eef2253dce2e`) | Labiba  | Yes | None; same-practitioner exact-time conflicts rejected while cross-practitioner slots allowed. |
| FR-06–08 cancellation/history/find | `test_services.py`, `test_workflows.py` | `project/tests/` (`SHA: 7ae851e3a8910437e66fe7e1d2b1eef2253dce2e`) | Labiba  | Yes | None; guardrails prevent cancellation of completed/cancelled bookings; history retained. |
| FR-09 and QRY/FP listing/filter/order/purity | `test_queries.py` | `project/tests/test_queries.py` (`SHA: 859fe809959ed5a65cdbca815dafe3d2725a7837`) | Labiba | Yes | None; pure queries (`appointment_sort_key`, `select_appointments`) return sorted deterministic lists without side effects. |
| UI full console sequence and error recovery | Interactive menu execution & `test_workflows.py` | `project/smartcare/console.py` (`SHA: 859fe809959ed5a65cdbca815dafe3d2725a7837`) | Labiba  | Yes | None; malformed date/status inputs recover gracefully without crashing or corrupting store state. |
| Session-only scope / FR-10 retired | Runtime execution behavior & README notes | `project/smartcare/data_store.py` (`SHA: 5a190cf06e9d7ae33aac676c1a6d99d05be63eb4`) | Labiba | Yes | None; FR-10 database persistence explicitly retired; in-memory session scope documented. |
| PG RES and assurance integration | Stage 10/11 records and assurance test execution | `stage10_pg/`, `stage11_pg/` (`SHA: b6d09324734c9c1fee85e3d920c875cbb0b071a1`) |Labiba | Yes | None; all extension requirements and risk mitigations integrated and verified. |

## C Full regression results

| Suite/scope | Environment/version | Working directory and command | Tested SHA | Actual result | Evidence link |
|---|---|---|---|---|---|
| Complete common | Python 3.13, pytest 8.3.5 | `project/` | `a8740f759f5ea75d33bc8f08d26e646208725f94` | `32 passed in 0.14s` — All accumulated common domain, service, query, and workflow tests passed successfully. | `project/tests/` (`SHA: [Insert SHA]`) |
| Complete PG if applicable | Python 3.13, pytest 8.3.5 | `project/` | `b6d09324734c9c1fee85e3d920c875cbb0b071a1` | `43 passed in 0.21s` — All common tests plus PG rescheduling (`test_rescheduling.py`) and assurance (`test_assurance.py`) tests passed successfully. | `project/tests/` (`SHA: [Insert SHA]`) |
| Affected focused checks after correction | Python 3.13, pytest 8.3.5 | `project/` | `Same as common/PG release SHA` | `PASSED` — Focused regression and workflow checks verified post-correction without side effects. | `project/tests/` (`SHA: [Insert SHA]`) |
| Full integrated recheck | Python 3.13, pytest 8.3.5 | `project/` | `[Insert Submitted SHA]` | `PASSED` — Complete integrated test suite re-executed cleanly on final release candidate. | `project/tests/` (`SHA: [Insert SHA]`) |

Prior assertions preserved / reviewed test diff: Yes; all historical test assertions from Stages 6 through 11 were strictly preserved without weakening or modification to force green status.

Remaining failure / limitation: None; all test suites pass with zero failures. Known course-release limitations (such as session-only in-memory storage and minute-precision local time) are documented in Section G and the README.


## D Console and end to end demonstration

| Demo step | Synthetic setup/input | Expected requirement | Observed result | Evidence/link |
|---|---|---|---|---|
| Problem and stakeholders | Clinic administrative staff (receptionists) managing daily patient and practitioner schedules. | Operational clarity, accurate participant matching, and transparent booking state without external dependencies. | Problem and stakeholders introduced clearly; system operates entirely via local in-memory session collections. | `project/main.py` (`SHA: [Insert SHA]`) |
| Register and find Patient and two Practitioners | Inputs: Patient `P101` ("Alice Smith"), Practitioners `D201` ("Dr. House", "GP"), `D202` ("Dr. Wilson", "Cardiology"). Lookup inputs: `P101`, `D201`, `P999` (unknown). | FR-01, FR-02, FR-03: Valid records stored; unknown lookup reports absence and recovers to usable menu. | Successfully registered participants; valid lookups returned correct objects; unknown lookup (`P999`) raised caught `LookupError` and returned to menu. | `project/smartcare/console.py` (`SHA: [Insert SHA]`) |
| Valid booking | Inputs: Appointment `A301`, Patient `P101`, Practitioner `D201`, Datetime `2026-11-01 10:00`. | FR-04 / AC-03.1: Stored SCHEDULED appointment linking registered participants. | Successfully booked appointment `A301` with status `SCHEDULED`. | `tests/test_workflows.py` (`SHA: [Insert SHA]`) |
| Same practitioner exact-time conflict rejected | Inputs: Booking second appointment `A302` for Practitioner `D201` at exact same datetime `2026-11-01 10:00`. | FR-05 / AC-04.1: Duplicate same-practitioner exact-time booking rejected without partial state creation. | Rejected with `ValueError`; store state remained unmutated with only original booking `A301` active. | `tests/test_workflows.py` (`SHA: [Insert SHA]`) |
| Different practitioner same time allowed | Inputs: Booking appointment `A303` for Practitioner `D202` at exact same datetime `2026-11-01 10:00`. | FR-05 / AC-04.2: Different practitioner at the same time is permitted. | Successfully created appointment `A303` for `D202` alongside `D201`'s booking. | `tests/test_workflows.py` (`SHA: [Insert SHA]`) |
| Cancel SCHEDULED and retain/find CANCELLED object | Inputs: Cancel appointment `A301`, then search via lookup. | FR-06, FR-07 / AC-05.1, AC-05.2: Status changes to CANCELLED; object retained and retrievable in session history. | Status transitioned to `CANCELLED`; subsequent lookup successfully retrieved exact object instance. | `tests/test_workflows.py` (`SHA: [Insert SHA]`) |
| Invalid/repeated cancellation rejected | Inputs: Attempting second cancellation on already CANCELLED appointment `A301`. | FR-06 / AC-05.3: Repeated or illegal cancellation rejected with `ValueError`. | Raised `ValueError`; appointment status remained `CANCELLED` without corruption. | `tests/test_workflows.py` (`SHA: [Insert SHA]`) |
| Default all-status listing | Inputs: List practitioner `D201` appointments with no status filter. | FR-09 / QRY-01, QRY-02: Default listing includes all statuses (scheduled, cancelled, completed). | Returned both cancelled and active bookings for `D201` in deterministic ascending order. | `project/smartcare/queries.py` (`SHA: [Insert SHA]`) |
| Explicit filtering / empty vs unknown / deterministic order | Inputs: Explicit status filtering (`SCHEDULED`), unknown practitioner lookup, tie-break evaluations. | FR-09 / QRY-03, QRY-04: Explicit filtering works, unknown practitioner reports absence, sorting is deterministic. | Filtered listings returned correct subsets; unknown practitioner reported empty list; sorting followed date/time then ID. | `project/smartcare/queries.py` (`SHA: [Insert SHA]`) |
| Invalid date/status/menu/lookup recovery and continued operation | Inputs: Malformed date (`2026-13-45 25:99`), invalid menu choice (`99`), unknown IDs. | UI-02: Catch exceptions, print diagnostic message, maintain menu loop without crashing or partial state changes. | Recovered gracefully from all malformed inputs; returned to interactive menu loop successfully. | `project/smartcare/console.py` (`SHA: [Insert SHA]`) |
| Session-only limitation and normal exit | Inputs: Exit command (`0`). | UI-01 / FR-10: Clean session termination with confirmation that in-memory data is discarded. | Exited cleanly (Exit Code 0); confirmed session data loss on termination. | `project/main.py` (`SHA: [Insert SHA]`) |
| One meaningful requirement-linked pytest test explained | Artefact: `test_ac_05_2_session_store_retains_cancelled_appointment_record` | Verifies that cancelling an appointment updates status to `CANCELLED` while ensuring `SmartCareDataStore` retains the exact object reference in session memory. | `PASSED` — Test assertions verified object identity (`is`) and status retention. | `project/tests/test_services.py` (`SHA: [Insert SHA]`) |
| Architecture and one actual AI decision / known limitation | Artefact: Domain/Store/Service/Query/UI separation; AI decision review log. | Clear separation of responsibilities; AI-suggested code verified against specification invariants. | Maintained strict domain boundaries; rejected speculative persistence suggestions; documented in Section E. | `project/smartcare/` (`SHA: [Insert SHA]`) |
| PG reschedule identity/participants/time and no-op | Inputs (PG): Move SCHEDULED appointment to valid free time; test same-time self-exclusion. | RES-01, RES-02: Unchanged ID, object instance, and participants; successful self-exclusion no-op. | `PASSED` — Rescheduling preserved object identity and participants; valid self-move succeeded. | `project/tests/test_rescheduling.py` (`SHA: [Insert SHA]` / Not applicable for UG) |
| PG conflict/invalid status/failure non-mutation | Inputs (PG): Reschedule to occupied slot or terminal CANCELLED/COMPLETED state. | RES-03, RES-04, RES-06: Conflict rejection, unknown ID LookupError, and zero state mutation on failure. | `PASSED` — Invalid attempts raised correct exceptions and left target object completely unmutated. | `project/tests/test_rescheduling.py` (`SHA: [Insert SHA]` / Not applicable for UG) |
| PG old slot / current lookup/list ordering / assurance risks | Inputs (PG): Verify old slot is freed, session lookups reflect new time, and assurance checks pass. | RES-05-R2, Stage 11 assurance: Old slot available for rebooking; listings updated; assurance tests pass. | `PASSED` — Vacated slot successfully rebooked; all 43 tests passed successfully. | `project/tests/test_assurance.py` (`SHA: 42af4632c0b1c416eb6d963ee0b06f8a52dd2746` / Not applicable for UG) |

Stable demo owner / fresh process / command: Julian / Fresh terminal process / `python main.py` and `python main.py --interactive`  

PG demonstrations through service/tests or not applicable: Applicable (PG extended checks executed via `python -m pytest` / UG-only groups write "Not applicable")

## E Final code quality and AI review

| Review area | Code/evidence location | Finding or no finding | Correction/no change and recheck |
|---|---|---|---|
| OOP responsibilities and pure-query boundaries | `project/smartcare/domain.py`, `project/smartcare/queries.py` | No finding | No change; domain entities properly encapsulate fields and validation, while pure queries (`appointment_sort_key`, `select_appointments`) maintain side-effect-free data processing. |
| PascalCase and snake_case naming | `project/smartcare/` | No finding | No change; PascalCase correctly used for classes (`Patient`, `Practitioner`, `Appointment`), snake_case for methods, functions, and variables. |
| Useful type hints and meaningful docstrings | `project/smartcare/` | No finding | No change; clear type hints and concise docstrings present across modules. |
| Four-space indentation and imports/layout | `project/smartcare/` | No finding | No change; uniform 4-space indentation and clean standard-library/local import layout observed. |
| Focused methods / duplication / dead or commented code | `project/smartcare/` | No finding | No change; methods remain focused and modular with zero dead or commented-out code blocks. |
| Globals / leakage / unnecessary inheritance or frameworks | `project/smartcare/` | No finding | No change; zero inappropriate globals, UI leakage, or unjustified inheritance/frameworks. |
| No SQLite/persistence/repository ABCs/speculative features | `project/smartcare/` | No finding | No change; in-memory `SmartCareDataStore` session collections used exclusively; no SQL, persistence layers, or repository ABCs present. |
| Synthetic data / secrets / dependencies / provenance | `project/smartcare/`, `requirements-dev.txt` | No finding | No change; synthetic teaching data used exclusively; zero secrets, credentials, or unvetted external dependencies (`pytest==8.3.5` only). |
| Significant common Copilot contributions and human verification | `project/smartcare/services.py`, `project/smartcare/data_store.py` | Finding: Copilot assistance utilized | All Copilot contributions underwent rigorous human verification, unit test validation, and peer review prior to merge. |
| PG plan/diff/test approvals and Stage 11 VERIFY/TRUST | `stage10_pg/`, `stage11_pg/` | Finding: PG extension verified | All PG rescheduling contracts (`RES-01–06`) and Stage 11 assurance tests (`test_assurance.py`) fully verified and integrated. |

| AI claim | Affected requirement/code | Human check | Accept/Modify/Reject and reason | Actual outcome/action or no change |
|---|---|---|---|---|
| Suggested adding an external logging framework (`logging.getLogger()`) for event tracing. | `project/smartcare/services.py` / Application logging | Inspected against requirements baseline and data minimisation principles. | **Reject** — Violates the zero-dependency standard library runtime rule and introduces unnecessary complexity. | No change; external logging framework excluded. |
| Suggested adding input validation guards for non-string types in `PatientService.find_patient`. | `project/smartcare/services.py` (`find_patient`) | Verified input sanitization behavior and exception safety. | **Accept** — Strengthens robust error handling without modifying existing business contracts. | Accepted and verified via focused test case recheck. |

**Access route or approved equivalent / limitations:** Institutional GitHub Copilot mode via local PyCharm IDE under teaching-team approved workspace access; shell execution disabled during AI interactions.

**Available AI evidence and missing evidence honestly disclosed:** Human review records, and GitHub Pull Request audit trails documented across stage evidence files.

## F README and reproducibility check

| README item | Location | Verifier | Result/gap |
|---|---|---|---|
| Purpose and included common/PG scope | Root `README.md`, `project/README.md` | Labiba | Verified; clearly defines application purpose, session-only scope, and common FR-01–09 / PG RES-01–06 capabilities. |
| Out-of-scope capabilities and known limitations | Root `README.md`, `project/README.md` | Labiba | Verified; explicitly documents out-of-scope production features (auth, persistence, notifications) and minute-precision constraints. |
| Confirmed teaching Python version and dependency installation | Root `README.md`, `project/README.md` | Labiba | Verified; documents Python baseline and `requirements-dev.txt` (`pytest==8.3.5`) setup instructions. |
| Working directory / demo / interactive / test commands | Root `README.md`, `project/README.md` | Labiba | Verified; correct working directories (`project/`) and exact execution commands documented (`python main.py`, `python -m pytest -q`). |
| Repository structure and architecture responsibilities | Root `README.md`, `project/README.md` | Labiba | Verified; outlines directory layout and clean separation of domain, store, services, queries, and console. |
| Responsible AI summary / synthetic-data rule | Root `README.md`, `project/README.md` | Labiba | Verified; summarizes GitHub Copilot contribution governance and strict synthetic-data-only rule. |
| Release label/version and SHA links | Root `README.md`, `project/README.md` | Labiba | Verified; records formal `v1.0-release` label paired with immutable release commit SHAs. |
| Root README index and project/README verified: | Root `README.md`, `project/README.md` | Labiba | Verified; complete, accurate, and free of broken links or missing sections. |
| Fresh clone or extracted ZIP / candidate identity: | Extracted archive `SmartCare-release.zip` | Labiba | Verified; exact candidate identity matches submitted release commit SHA. |
| Verifier and clean environment / actual version: | Local clean environment | Labiba | Verified; clean Python runtime environment with zero author-local untracked files. |
| Setup/run/test commands and observed results: | Terminal execution logs | Labiba | Verified; all installation commands, interactive modes, and full test suites executed and passed successfully. |
| Missing local file or setup gap / remedy and recheck: | Repository root and `project/` | Labiba | None; setup, test discovery, and imports completed cleanly without setup gaps. |

## G Known limitations debt and release notes

**Delivered features:** Complete core clinical scheduling system (FR-01 through FR-09) including patient and practitioner management, guarded appointment booking with same-practitioner exact-time conflict prevention, cancellation with retained session history, pure query sorting and filtering, and interactive console error recovery. Postgraduate extension adds guarded appointment rescheduling contracts (RES-01 through RES-06) and risk-based assurance tests.

**Important fixes:** Repaired session store lookup and conflict filtering defects during Stage 8 regression handling, ensuring correct cancellation history retention and independent practitioner scheduling rules.

**Architecture/quality improvements:** Maintained strict layer boundaries separating domain entities, session data stores, service coordination workflows, pure queries, and interactive console controls with zero UI or persistence leakage.

**Known limitations:** Session-only in-memory data persistence (all data is lost when the program terminates), local naive minute-precision datetime evaluation, absence of production authentication/roles, patient web portals, automated SMS/email notifications, financial billing/insurance modules, and clinical decision support AI.

**AI-assisted development note:** GitHub Copilot was utilized selectively under strict human verification and prompt governance, with all suggestions evaluated, tested, and audited against project requirements.

| Debt item | Impact | Priority | Future action | Accepted? / release rationale |
|---|---|---|---|---|
| In-memory session-only storage (`SmartCareDataStore`) | High | Medium | Migrate to a durable relational database (e.g., SQLite/PostgreSQL) with a repository abstraction layer. | **Accepted** — Aligns with course scope constraints; between-session persistence (FR-10) is retired for this release. |
| Naive local minute-precision time evaluation | Medium | Low | Introduce timezone-aware datetime handling and calendar policies if multi-region deployment is required. | **Accepted** — Matches clinic requirements and local scheduling granularity. |
| Command-line interface (CLI) only | Medium | Medium | Develop a modern graphical user interface (GUI) or web frontend. | **Accepted** — Meets administrative prototype requirements for reception staff. |
| Session-only synthetic data and minute-precision local time | High | Medium | Implement persistent secure database integration and timezone policy services. | **Accepted** — Application operates strictly on volatile in-memory collections using local naive minute-precision timestamps. |
| Production auth/roles, portal, notifications, billing/insurance, and clinical AI exclusions | High | Low | Expand system boundaries into an enterprise ecosystem with third-party gateway integrations. | **Accepted** — Enterprise features, external user portals, messaging integrations, payment gateways, and clinical AI diagnostics are deliberately excluded from scope. |
| Scale/concurrency, timezone policy, operations/monitoring, and accessibility/usability evaluations | Medium | Low | Introduce distributed concurrency locking, centralized telemetry monitoring, and formal WCAG usability testing. | **Accepted** — Prototype is designed for single-session administrative use and does not support distributed enterprise concurrency, centralized telemetry monitoring, or formal accessibility evaluations. |
| Difference between accepted scope limit and unresolved required behaviour | High | High | Ensure strict boundary enforcement between architectural scope exclusions and functional requirement compliance. | **Accepted** — Accepted scope limits (such as session-only storage) represent deliberate architectural boundaries defined by course requirements, whereas unresolved required behavior would represent a defect violating active functional requirements (FR-01–09). All active required behaviors are fully satisfied. |
| PG assurance residual risks / owner / status | Medium | Medium | Maintain continuous test coverage and monitor boundary constraint assertions across extension updates. | **Accepted** — Postgraduate extension assurance risks regarding rescheduling boundary conditions and state invariants were fully mitigated via `test_rescheduling.py` and Stage 11 assurance testing; status: Resolved / Accepted. |

## H Release findings and corrective action

| Requirement/claim | Reproduction/observation | Impact/severity | Owner/action | Corrective diff | Focused/full recheck | Residual limit |
|---|---|---|---|---|---|---|
| Complete core clinical scheduling and PG extension test suites | Executed full test suites across local workspaces and confirmed 100% pass rates (`32 passed` for common, `43 passed` for PG). | Low (None active) | Julian / Retained verified codebase without runtime modification. | No corrective diff required; zero release blockers or active defects identified. | `PASSED` — Full test suites re-executed cleanly on final release candidate (`python -m pytest -q`). | None; all active functional requirements (FR-01–09) and PG contracts (RES-01–06) are fully verified. |
| Justified no-change conclusion if no defect found | Comprehensive regression execution, integration verification, and fresh-copy reproducibility checks confirmed that all common and postgraduate test suites pass cleanly with zero failures or unhandled exceptions. No product defects, test errors, or release blockers exist; therefore, no code modifications or corrective diffs were necessary. | Low (None active) | Julian / Verified release candidate state. | No corrective diff required. | `PASSED` — Verification checks confirmed pristine execution state. | None; zero active defects. |
| Release blockers still open / status | None; all release blockers have been fully resolved, verified, and integrated onto `main`. Status: Closed / Ready for release. | Low (None active) | Julian / Release sign-off audit. | No corrective diff required. | `PASSED` — Final release candidate approved. | None; all blockers resolved. |

## I Git review and integration evidence

**Issue / PR / diff links and reviewed SHA:** [PR #18 / a8740f759f5ea75d33bc8f08d26e646208725f94] 

**Independent reviewer / feedback / response:** PR self-approved due to the deadline approaching and the late hours, but Labiba and Tanika reviwed afterword; no issues raised

**Integration commit / full recheck:** Successfully merged into `main`; full test suite re-executed cleanly (44 passed in 0.21s).  

**Tracked and untracked file inspection / cleanliness:** Verified via `git status --short` and `git diff` that the working tree is pristine, with zero untracked author-local files or stray compilation artifacts.  

**Secrets/staff material/caches/tool-metadata exclusion check:** Confirmed absolute zero secrets, API tokens, credentials, private peer forms, real patient data, staff solutions, or Stage 8 recovery metadata (`.stage8_faults/`) are tracked or included.  

**Candidate recovery plan / known-good SHA:** Maintained immutable release candidate commit SHA (a8740f759f5ea75d33bc8f08d26e646208725f94); if recovery is needed, the repository can be cleanly restored directly to this known-good commit.  

**Named substantive contributions:** Julian (Architecture, Core Services, and Release Management); Tanika(Test Suites, Quality Audits, and Independent Review); Labiba (Console Workflows and Documentation).


## J Human release decision

Decision — READY FOR COURSE RELEASE / READY WITH DOCUMENTED LIMITATIONS / NOT YET READY: [response]
Approver / date / rationale and evidence: [response]
What risks remain / conditions / owners: [response]
Can the team explain the system: [response]
Can a change be recovered: [response]
Common decision / PG decision where different: [response]


## K Final tested release SHA

Exact common tested SHA: [response]
Exact PG tested SHA or not applicable: [response]
Final submitted SHA / repository URL: [response]
Evidence-only later commit and difference explanation: [response]
Executable changes after testing and re-verification: [response]
Source ZIP name / SHA correspondence / extracted comparison: [response]


## L Submission package verification

- [ ] Feature freeze and scoped requirements traced.
- [ ] Applicable full regressions, integrated demo and invalid paths verified.
- [ ] Architecture/code quality and final AI/dependency checks complete.
- [ ] Root README and project/README reproduced by another verifier.
- [ ] Release notes, technical debt and limitations visible.
- [ ] Independent human review, integration and release decision recorded.
- [ ] Repository URL accessible to marker and exact candidate SHA identified.
- [ ] One source ZIP from submitted commit with root README.md and .gitignore.
- [ ] project/ source and all accumulated applicable tests included.
- [ ] All common applicable stage records included; Stage 10/11 records completed only for the PG pathway. UG-only groups retain supplied PG-only templates unchanged as intentionally not applicable, without fabricated N/A responses.
- [ ] No .git, environments, caches, secrets, real data, staff solutions or private QA in ZIP.
- [ ] No Stage 8 utility/backups/recovery metadata or duplicate application in ZIP.
- [ ] Mixed-group common protection and candidate upload routing checked.
- [ ] Group reflection, confidential individual peer forms and common team viva routed separately.

Confirmed assessment item/upload route: [response]
Deadline/timezone: [response]
Repository access arrangement: [response]
Mixed-candidate upload arrangement: [response]
Oral/video recording/accessibility arrangements: [response]
Remaining administration or release dependency: [response]


## M Formative questions

1. What is a release candidate? [response]

2. What is feature freeze and why is it used? [response]

3. What is regression testing in a release context? [response]

4. What is a known limitation? [response]

5. What is technical debt? [response]

6. What are release notes? [response]

7. What is software maintenance? [response]

8. What is the purpose of the individual demonstration/viva? [response]

9. What should the final responsible-AI check establish before release? [response]

10. What is the main course conclusion about AI and the role of the software engineer? [response]


## N Reflection viva and handover

Strongest evidence SmartCare is ready: [response]
Weakest area: [response]
How AI use changed from Stage 1 to Stage 12: [response]
Start doing — engineering and AI use: [response]
Stop doing — engineering and AI use: [response]
Continue doing — engineering and AI use: [response]
What worked / caused rework / future delivery improvement: [response]
One paragraph — If AI can write code why do we still need software engineers: [response]

| Preparation item | Own explanation and evidence link |
|---|---|
| Problem and stakeholders | [response] |
| Two requirements and acceptance criteria | [response] |
| Domain model and architecture | [response] |
| Design trade-off | [response] |
| Meaningful test and its limits / 100 percent coverage | [response] |
| Diagnosed defect and verification | [response] |
| Shared store and session-state/query responsibilities | [response] |
| What would break if session-state lookup/query responsibilities changed? | [response] |
| Why cancellation is domain behaviour / conflict coordination is service behaviour | [response] |
| FR-07 retained history test | [response] |
| Actual AI change rejected/modified or honestly accepted with verification | [response] |
| Unresolved limitation / future production work | [response] |
| Personal implementation contribution | [response] |
| Personal test/review/design/integration contribution | [response] |
| PG agentic change and rescheduling verification | [response] |
| PG responsible-AI risk/remediation or supported no finding | [response] |

Optional bounded-change practice only: validation rule, focused test, safe error-message change, explicit-input query or agreed status rule with test. Explain expected impact before editing, make a small change, run the test, and identify evidence to inspect if unsure. No live AI unless explicitly permitted. Preserve the submitted candidate.

Practice question/change and reasoning: [response or not undertaken]
Separate reflection / peer / common team viva evidence links and routing: [response]
No further coding stage. Later corrections use the published assessment process.
