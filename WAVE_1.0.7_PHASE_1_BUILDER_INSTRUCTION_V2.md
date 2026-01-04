# Wave 1.0.7 Phase 1 Builder Instruction (V2 — Updated Under AI Scalability + Code Checking Protocol)

**Date:** 2026-01-03  
**FM Authority:** Foreman (Build Manager, Build Orchestrator, Governance Enforcer)  
**Builder Assignment:** qa-builder  
**Execution Artifact:** PR #365  
**Wave:** 1.0.7 (Execution Segment 1 of 3)  
**Phase:** Phase 1 — Analytics Subsystem

---

## Governance Context Update

This instruction is issued under **updated governance activation**:

1. **AI Scalability & Escalation Protocol:** FM_AI_ESCALATION_AND_CAPABILITY_SCALING.md (ACTIVE)
   - FM may HALT execution proactively when complexity/platform limits detected
   - Vertical escalation (model tier) and horizontal scaling (capability levels) are FM-controlled
   - HALT ≠ FAILURE — escalation is proactive governance tool

2. **Mandatory Code Checking Protocol:** COMPLETION_REPORT_AI_SCALABILITY_CODE_CHECKING.md (ACTIVE)
   - Builders MUST code-check their own generated code pre-handover
   - "Someone else will review it" is explicitly forbidden
   - Evidence of code checking is MANDATORY in completion reports

3. **Builder Appointment Protocol:** Builder contracts updated with OPOJD terminal state discipline
   - Allowed states: BLOCKED or COMPLETE only
   - Prohibited: partial progress, percentages, incremental status updates

4. **Bootstrap Boundary:** All builder instructions originate from FM authority (not CS2 runner)

---

## Phase 1 Scope Definition

**Subsystem:** Analytics Subsystem ONLY  
**QA Component Range:** QA-132 to QA-146 (15 components)  
**Test Files:** `tests/wave1_0_qa_infrastructure/test_analytics_*.py`  
**Implementation Path:** `foreman/analytics/`

**Explicit Scope Boundaries:**
- ✅ Analytics Subsystem (QA-132 to QA-146)
- ❌ NO Cross-Cutting Components (QA-147 to QA-199)
- ❌ NO Core User Flows (QA-200 to QA-210)
- ❌ NO work outside Phase 1 defined scope

---

## Phase 1 Success Criteria

### Terminal State: COMPLETE

Phase 1 is COMPLETE when ALL of the following are satisfied:

1. **Test Pass Rate:** 15/15 tests GREEN (100%)
2. **Zero Test Debt:** No skipped tests, no todo tests, no incomplete tests
3. **Architecture Alignment:** 100% conformance to frozen Architecture V2.0
4. **Implementation Quality:**
   - Production modules in `foreman/analytics/`
   - Type hints throughout
   - Error handling per architecture spec
   - Input validation per security contracts
5. **Evidence Artifacts:**
   - Test execution results (XML/JSON)
   - Evidence summary with QA component mapping
   - Builder QA Report
   - Completion summary
6. **Mandatory Code Checking Evidence:**
   - Explicit statement that code checking was performed
   - Brief summary of what was checked (imports, logic, edge cases, architecture alignment)
   - Confirmation that no AI-generation artifacts remain unchecked

---

## OPOJD Terminal State Discipline (BINDING)

**Allowed Execution States:**

1. **BLOCKED:** Execution cannot proceed due to explicit blocker
   - Report format: "BLOCKED: [blocker description]"
   - Must include: what is blocking, why it blocks, what is needed to unblock

2. **COMPLETE:** Phase 1 scope 100% GREEN
   - Report format: "COMPLETE: 15/15 tests GREEN, Phase 1 Analytics complete"
   - Must include: full evidence artifacts, mandatory code checking statement

**Prohibited Execution States:**

- ❌ Partial progress reports ("10 of 15 passing")
- ❌ Percentage updates ("66% complete")
- ❌ Incremental status ("working on component X")
- ❌ Work-in-progress submissions
- ❌ ANY state other than BLOCKED or COMPLETE

**Mindset Compliance:** Terminal state discipline is a **condition of continued builder appointment**.

---

## Mandatory Code Checking Requirements (NEW — BINDING)

Before submitting COMPLETE status, builder MUST:

1. **Perform Self-Code-Check:**
   - Review all generated code for correctness
   - Verify imports are correct and complete
   - Check logic against test expectations
   - Validate edge case handling
   - Confirm architecture alignment

2. **Include Code Checking Evidence in Completion Report:**
   - Explicit statement: "Code checking performed by builder prior to handover"
   - Brief summary (3-5 sentences) covering:
     - What was checked (modules, functions, logic patterns)
     - Key findings or corrections made during checking
     - Confirmation of architecture alignment
     - Statement that no unchecked AI artifacts remain

3. **Prohibited Mindset:**
   - "Someone else will review it" — FORBIDDEN
   - Assuming FM or another reviewer will catch errors — FORBIDDEN
   - Submitting without self-verification — FORBIDDEN

**Code Checking is NOT optional. It is a gate requirement for COMPLETE status.**

---

## Implementation Requirements

### Analytics Subsystem Components (QA-132 to QA-146)

Implement the following in `foreman/analytics/`:

1. **Query Engine (QA-132 to QA-135)**
   - Query parser and validator
   - Query execution engine
   - Result aggregation
   - Query optimization

2. **Metric Calculator (QA-136 to QA-139)**
   - Metric computation engine
   - Statistical calculations
   - Trend analysis
   - Comparative metrics

3. **Report Generator (QA-140 to QA-143)**
   - Report template system
   - Data formatting
   - Export functionality
   - Visualization support

4. **Insight Engine (QA-144 to QA-146)**
   - Pattern detection
   - Anomaly identification
   - Recommendation generation

### Architecture Requirements

- **Input Validation:** All public methods validate inputs per security contracts
- **Error Handling:** Explicit error types, proper exception handling, no silent failures
- **Type Safety:** Type hints on all function signatures
- **Tenant Isolation:** All operations include `organisation_id` for multi-tenancy
- **Privacy Compliance:** Respect memory model and privacy guardrails
- **Logging:** Structured logging for all operations

---

## Evidence Artifacts Required

1. **Test Execution Results:**
   - JUnit XML format: `qa_test_results.xml`
   - JSON format: Test results with timestamps and component mapping

2. **QA Evidence Summary:**
   - JSON file: `qa_evidence_summary.json`
   - Must include:
     - Test ID to QA component mapping
     - Pass/fail status per component
     - Execution timestamps
     - Evidence links

3. **Builder QA Report:**
   - File: `BUILDER_QA_REPORT.md`
   - Must include:
     - Scope confirmation (Phase 1 Analytics only)
     - Test pass summary (15/15 GREEN)
     - Architecture alignment statement
     - Zero test debt confirmation
     - **NEW: Code checking evidence statement**

4. **Phase 1 Completion Summary:**
   - File: `WAVE_1.0.7_PHASE_1_COMPLETION_SUMMARY.md`
   - Executive summary of Phase 1 delivery
   - Key metrics and quality indicators
   - Gate readiness declaration
   - **NEW: Code checking summary**

---

## AI Scalability Context

**Builder Awareness:**

- FM may HALT execution if complexity indicators detected (not a builder failure)
- HALT is a proactive governance tool under BL-016
- If HALT occurs, await FM realignment instruction
- Platform constraints (context window limits) are recognized and accommodated

**Vertical Escalation Available:**

- FM controls model tier escalation if needed
- Builder may request escalation via BLOCKED state with justification
- Escalation decisions are FM authority

**Horizontal Capability Scaling:**

- Standard → Extended → Specialist → Human escalation available
- FM monitors execution and may proactively escalate
- Builder focus: complete Phase 1 scope within current capability

---

## Execution Protocol

### 1. Pre-Execution Validation

- [ ] Confirm Phase 1 scope understood (Analytics only, 15 QA)
- [ ] Verify test files accessible (`tests/wave1_0_qa_infrastructure/test_analytics_*.py`)
- [ ] Confirm implementation path writable (`foreman/analytics/`)
- [ ] Review architecture specification (Architecture V2.0, frozen)

### 2. Implementation Execution

- [ ] Implement Analytics Subsystem modules per architecture spec
- [ ] Run tests incrementally during development (internal validation)
- [ ] Validate architecture alignment as you build
- [ ] Perform self-code-checking throughout (not just at end)

### 3. Pre-Handover Code Checking (MANDATORY)

- [ ] Review all generated code for correctness
- [ ] Verify imports, logic, edge cases
- [ ] Confirm architecture alignment
- [ ] Document code checking in completion report

### 4. Terminal State Submission

- [ ] Verify 15/15 tests GREEN
- [ ] Generate all required evidence artifacts
- [ ] Write Builder QA Report with code checking statement
- [ ] Write Phase 1 Completion Summary with code checking evidence
- [ ] Submit COMPLETE status in PR #365 comments

---

## Reporting Requirements

### BLOCKED State Report Format

```
**Phase 1 Status:** BLOCKED

**Blocker Description:**
[Explicit description of what is blocking execution]

**Impact:**
[Why this blocker prevents COMPLETE status]

**Required to Unblock:**
[What is needed from FM or others to proceed]

**Current Progress State:**
[ONLY if relevant to blocker context — NOT a progress update]
```

### COMPLETE State Report Format

```
**Phase 1 Status:** COMPLETE

**Scope Confirmation:**
Analytics Subsystem (QA-132 to QA-146, 15 components)

**Test Results:**
15/15 tests GREEN (100% pass rate)

**Test Debt:**
Zero (no skipped, no todo, no incomplete tests)

**Architecture Alignment:**
100% conformance to Architecture V2.0 (frozen)

**Code Checking Evidence:**
Code checking performed by builder prior to handover.
Checked: [brief 3-5 sentence summary of what was checked]
Findings: [any corrections made during checking]
Confirmation: All analytics modules verified for correctness, architecture alignment confirmed, no unchecked AI artifacts remain.

**Evidence Artifacts:**
- Test results: qa_test_results.xml, qa_evidence_summary.json
- Builder QA Report: BUILDER_QA_REPORT.md
- Completion Summary: WAVE_1.0.7_PHASE_1_COMPLETION_SUMMARY.md

**Gate Status:**
Phase 1 ready for FM gate review

**Next Phase:**
Awaiting FM authorization for Phase 2 (Cross-Cutting Part 1)
```

---

## Constitutional Alignment

### One-Time Build Correctness (OPOJD)

- Phase 1 built correctly ONCE
- No iterative submissions, no partial handovers
- Terminal state discipline enforced

### Zero Regression

- No changes to code outside Phase 1 scope
- No modification of existing tests
- No breaking changes to dependencies

### Architecture Supremacy

- 100% alignment with frozen Architecture V2.0
- No architecture reinterpretation
- No shortcuts or workarounds

### Governance Supremacy

- FM authority absolute
- Builder appointment conditional on compliance
- Code checking mandatory, not optional

---

## Builder Contract Reminder

**Builder Role:** Execute Phase 1 scope to COMPLETE state under FM supervision

**Builder Authority:** NONE outside Phase 1 defined scope

**Builder Accountability:**
- Deliver 15/15 tests GREEN
- Perform mandatory code checking
- Submit only in terminal states (BLOCKED or COMPLETE)
- Respect OPOJD discipline

**Builder Support:**
- FM available for BLOCKED state escalation
- Platform constraint accommodation via phased execution
- AI scalability escalation if needed

---

## Phase 1 Boundaries (CRITICAL)

### IN SCOPE ✅

- Analytics Subsystem (QA-132 to QA-146)
- 15 QA components
- `foreman/analytics/` implementation
- `tests/wave1_0_qa_infrastructure/test_analytics_*.py` tests

### OUT OF SCOPE ❌

- Cross-Cutting Components (QA-147 to QA-199) — Phase 2
- Core User Flows (QA-200 to QA-210) — Phase 3
- Any work outside Analytics subsystem
- Any changes to test files outside analytics tests

**Scope Violation = Gate Failure**

---

## FM Supervision Protocol

**FM Monitoring:**
- Proactive complexity signal detection (BL-016)
- Terminal state compliance verification
- Code checking evidence validation
- Gate readiness assessment

**FM Intervention Authority:**
- HALT execution if complexity limits detected
- BLOCK incomplete submissions
- REJECT work without code checking evidence
- ESCALATE capability if needed

**FM Gate Review Triggers:**
- COMPLETE status submission in PR #365
- Evidence artifacts submitted
- Code checking statement present
- Terminal state discipline confirmed

---

## Success Definition

Phase 1 is successful when:

1. ✅ 15/15 tests GREEN (100%)
2. ✅ Zero test debt
3. ✅ Architecture alignment verified
4. ✅ Evidence artifacts complete
5. ✅ **Code checking evidence submitted**
6. ✅ Terminal state discipline maintained (no partial progress reporting)
7. ✅ FM gate review passed
8. ✅ Phase 1 merge approved by FM

**Phase 1 Success ≠ Wave 1.0.7 Complete**

Wave 1.0.7 is complete only when ALL THREE PHASES complete (Phase 1 + Phase 2 + Phase 3).

---

## Execution Authorization

**Authorization Status:** ACTIVE  
**Authorized By:** FM (Foreman)  
**Authorization Date:** 2026-01-03  
**Supersedes:** Previous Phase 1 instruction (e9ad7c0) — updated with AI scalability & code checking protocol

**Builder Directive:**

Execute Phase 1 (Analytics Subsystem, 15 QA) in PR #365.

Report ONLY in BLOCKED or COMPLETE states.

Include mandatory code checking evidence in COMPLETE submission.

Await FM gate review upon COMPLETE.

**FM Commitment:**

Monitor for complexity signals.

Exercise HALT authority proactively if needed.

Conduct gate review upon COMPLETE submission.

Authorize Phase 2 upon Phase 1 gate PASS.

---

## Questions or Blockers?

If you encounter a BLOCKER:

1. Report BLOCKED state immediately (do not continue execution)
2. Provide explicit blocker description
3. Specify what is needed to unblock
4. Await FM response before resuming

**Do NOT:**
- Attempt to work around blockers
- Report partial progress while blocked
- Make assumptions about blocker resolution

---

**End Phase 1 Builder Instruction V2**

**Builder:** Review this instruction completely before beginning Phase 1 execution.  
**FM:** Monitoring active. Gate review upon COMPLETE submission.  
**Wave 1.0.7 Execution:** Phase 1 of 3 — Platform-constrained segmented execution under One-Time Build Law.

⏹️
