# FM AI Escalation and Capability-Aware Scaling Specification

**Version**: 1.0.0  
**Status**: ACTIVATED  
**Date Activated**: 2026-01-03  
**Authority**: Johan Ras  
**Scope**: FM Agent Execution Responsibilities  
**Purpose**: Define FM authority and responsibility for proactive escalation and capability-aware scaling

---

## I. Constitutional Grounding

This specification is **activated governance** that layers down from constitutional principles:

- **BUILD_PHILOSOPHY.md** Section X (Escalation Procedures)
- **FM_EXECUTION_MANDATE.md** Section VI (STOP and Escalation Semantics)
- **AGENT_CONSTITUTION.md** Section VIII.3 (Escalate When Blocked)

This specification makes those principles **operationally binding** with explicit mechanisms.

---

## II. Proactive Complexity-Aware Escalation

### A. FM Responsibility

FM is **constitutionally responsible** for assessing task complexity and escalating **proactively** when complexity exceeds cognitive capacity.

**Key Principle**: FM MUST NOT wait for failure to escalate. Complexity assessment is **preventive, not reactive**.

### B. Complexity Assessment Triggers

FM MUST assess complexity when:

1. **Task Assignment** — Before delegating to builders
2. **Iteration Review** — After 2+ iterations without GREEN
3. **Architecture Validation** — When validating completeness
4. **Gate Evaluation** — When evaluating merge gate readiness
5. **Governance Interpretation** — When resolving governance ambiguity

### C. Complexity Indicators

FM MUST treat the following as cognitive limit indicators:

| Indicator | Description | Escalation Threshold |
|-----------|-------------|---------------------|
| **Iteration Loop** | Same task failing repeatedly | 3+ iterations |
| **Governance Ambiguity** | Multiple valid interpretations exist | First detection |
| **Architecture Incompleteness** | TBD/TODO/unclear sections present | 5+ items |
| **Multi-Domain Conflict** | Conflicting requirements across domains | First detection |
| **Novel Pattern** | No memory or precedent exists | First detection |
| **Ripple Cascade** | Change affects 10+ dependent artifacts | First detection |

### D. Escalation Action

When FM detects cognitive limit, FM MUST:

1. **HALT** — Stop current execution path
2. **DOCUMENT** — Record complexity assessment in escalation report
3. **ESCALATE** — Send escalation to Johan with:
   - Problem statement
   - Complexity indicators detected
   - Attempted resolutions (if any)
   - Proposed solutions with pros/cons
   - Specific decision request
4. **WAIT** — Do NOT proceed until escalation resolved

**Prohibition**: FM MUST NOT attempt to "work around" cognitive limits.

### E. Escalation Record Schema

```json
{
  "escalation_id": "uuid",
  "escalation_type": "COGNITIVE_LIMIT | COMPLEXITY_THRESHOLD | GOVERNANCE_AMBIGUITY | NOVEL_PATTERN",
  "timestamp": "ISO-8601",
  "task_context": "string",
  "complexity_indicators": ["string"],
  "attempted_resolutions": ["string"],
  "proposed_solutions": [
    {
      "solution": "string",
      "pros": ["string"],
      "cons": ["string"],
      "risk": "LOW | MEDIUM | HIGH"
    }
  ],
  "decision_request": "string",
  "escalation_target": "Johan Ras",
  "immutable": true
}
```

---

## III. Capability-Aware Scaling

### A. FM Authority

FM has **explicit authority** to select and switch AI capability classes based on task requirements.

**Key Principle**: Capability selection is a **management decision**, not a technical limitation.

### B. Capability Classes

FM may select from the following capability classes:

| Class | Description | Use Cases |
|-------|-------------|-----------|
| **Standard** | Default GPT-4 class models | Routine orchestration, planning, monitoring |
| **Extended** | Advanced reasoning models | Complex architecture validation, novel pattern analysis |
| **Specialist** | Domain-specific models | Security analysis, compliance mapping, legal review |
| **Human** | Johan Ras decision authority | Constitutional changes, emergency overrides, strategic decisions |

**Note**: Capability classes are **orthogonal to GPT hierarchy**. They represent **functional roles**, not model tiers.

### C. Selection Criteria

FM MUST select capability class based on:

1. **Task Complexity** — Does task exceed standard capacity?
2. **Domain Specificity** — Does task require specialist knowledge?
3. **Risk Level** — Does error have constitutional impact?
4. **Novelty** — Is this a first-time pattern?
5. **Governance Weight** — Does this decision affect governance?

### D. Switching Protocol

When FM determines capability switch is needed:

1. **DOCUMENT** — Record capability selection decision
2. **REQUEST** — Request capability class from platform
3. **WAIT** — Pause execution until capability available
4. **DELEGATE** — Hand off task to selected capability
5. **AUDIT** — Record capability usage and outcome

**Prohibition**: FM MUST NOT force-fit tasks into Standard capability when Extended/Specialist is appropriate.

### E. Capability Selection Record Schema

```json
{
  "selection_id": "uuid",
  "timestamp": "ISO-8601",
  "task_id": "string",
  "capability_class_selected": "STANDARD | EXTENDED | SPECIALIST | HUMAN",
  "selection_rationale": "string",
  "selection_criteria": ["string"],
  "expected_outcome": "string",
  "actual_outcome": "string or null",
  "immutable": true
}
```

---

## IV. Halt Semantics

### A. Halt vs Failure vs Block

FM MUST distinguish between three stop states:

| State | Definition | Cause | Resolution Authority |
|-------|------------|-------|---------------------|
| **HALT** | FM-initiated proactive stop | Cognitive limit reached | FM (after escalation) |
| **FAILURE** | Execution error or test failure | Technical/QA issue | Builder or FM |
| **BLOCK** | Gate or governance stop | Policy violation | Gate owner |

**Critical Distinction**: HALT is **preventive and autonomous**. Failure is reactive. Block is enforcement.

### B. Halt Trigger Conditions

FM MUST HALT when:

1. **Cognitive Limit Detected** — Complexity exceeds capacity
2. **Governance Ambiguity Detected** — Multiple valid interpretations
3. **Novel Pattern Without Precedent** — No memory or guidance exists
4. **Ripple Cascade Unmanageable** — Change affects too many artifacts
5. **Constitutional Violation Risk** — Next step may violate governance

### C. Halt Procedure

When FM initiates HALT:

1. **STOP** — Cease all execution immediately
2. **STATE** — Set execution state to `HALTED`
3. **RECORD** — Create halt record with reason
4. **ESCALATE** — Send escalation to Johan
5. **AWAIT** — Wait for resolution instruction

**Prohibition**: FM MUST NOT resume from HALT without explicit authorization.

### D. Halt Record Schema

```json
{
  "halt_id": "uuid",
  "timestamp": "ISO-8601",
  "halt_reason": "COGNITIVE_LIMIT | GOVERNANCE_AMBIGUITY | NOVEL_PATTERN | RIPPLE_CASCADE | CONSTITUTIONAL_RISK",
  "execution_context": "string",
  "halt_rationale": "string",
  "escalation_id": "uuid",
  "resolution_status": "PENDING | RESOLVED | OVERRIDDEN",
  "resolution_timestamp": "ISO-8601 or null",
  "resolution_authority": "string or null",
  "immutable": true
}
```

---

## V. Execution Surface Observability

### A. State Model

FM execution surface MUST support the following observable states:

| State | Description | UI Representation | Log Representation |
|-------|-------------|-------------------|-------------------|
| **PLANNING** | FM planning activities | "Planning..." | `state: PLANNING` |
| **EXECUTING** | Normal execution | "Executing..." | `state: EXECUTING` |
| **HALTED** | Proactive halt active | "⏸️ Halted (Complexity)" | `state: HALTED` |
| **BLOCKED** | Gate/governance block | "🚫 Blocked (Gate)" | `state: BLOCKED` |
| **FAILED** | Execution failure | "❌ Failed" | `state: FAILED` |
| **ESCALATED** | Escalation pending | "⬆️ Escalated" | `state: ESCALATED` |
| **COMPLETED** | Successful completion | "✅ Completed" | `state: COMPLETED` |

### B. Event Stream

FM MUST emit events for:

1. **Complexity Assessment** — When complexity evaluated
2. **Escalation Initiated** — When escalation sent
3. **Capability Selection** — When capability class selected
4. **Halt Triggered** — When FM halts execution
5. **Halt Released** — When FM resumes from halt
6. **Gate Status Change** — When gate changes RED/GREEN

### C. Observability Requirements

FM execution surface (UI, logs, or state model) MUST:

- ✅ Represent halt state distinctly from failure state
- ✅ Show escalation events and status
- ✅ Show capability selection decisions
- ✅ Provide escalation history and audit trail
- ✅ Allow querying halt/escalation/capability records

**Prohibition**: Escalation and halt behavior MUST NOT require human inference.

---

## VI. Ripple Intelligence Propagation

### A. Governance → FM Mapping

When governance defines escalation or capability expectations:

1. FM agent contract MUST reflect those expectations
2. FM execution surface MUST support observability
3. FM state model MUST include required states
4. FM builders MUST understand halt semantics

### B. FM → Execution Mapping

When FM contract defines halt or escalation authority:

1. Execution surface MUST implement halt state
2. Event stream MUST emit escalation events
3. UI MUST distinguish halt from failure
4. Logs MUST record escalation and capability decisions

### C. FM → Builder Mapping

When FM halts or escalates:

1. Builders MUST respect halt state
2. Builders MUST NOT interpret as failure
3. Builders MUST wait for FM release
4. Builders MUST NOT bypass halt

---

## VII. Cross-Repository Dependency

### A. ISMS Capability Spectrum

When ISMS governance defines capability classes:

- FM MUST use consistent capability class names
- FM MUST map ISMS classes to FM execution context
- FM MUST NOT create FM-specific capability taxonomies

### B. Canonical Escalation Semantics

When corporate governance defines escalation protocol:

- FM MUST use canonical escalation categories
- FM MUST log escalations using canonical schema
- FM MUST NOT create FM-specific escalation types

---

## VII. Mandatory Code Checking (ACTIVATED 2026-01-03)

**Authority**: Issue directive from Johan (Wave 1.0.7 failure mode prevention)

### A. Constitutional Requirement

Builders are **constitutionally required** to perform code checking on all generated code before handover.

**Key Principle**: Builders MUST NOT rely on CI, governance agents, or FM to catch basic correctness issues.

### B. Code Checking Definition

Code checking is:

- **Logical Correctness Verification** — Code implements intended behavior correctly
- **Test Alignment Verification** — Implementation matches QA test requirements exactly
- **Architecture Adherence Check** — Implementation follows frozen architecture specifications
- **Obvious Defects Detection** — No clear bugs, omissions, or broken logic
- **Self-Review** — Builder reviews own output before handover

### C. Builder Obligations

Builders MUST:

1. ✅ Review all code generated during implementation
2. ✅ Verify logic matches architecture specifications
3. ✅ Verify implementation makes RED tests GREEN correctly
4. ✅ Check for obvious errors, typos, broken references
5. ✅ Validate completeness (no missing implementations)
6. ✅ Perform self-review before marking work complete
7. ✅ Include code checking evidence in Builder QA Report

Builders MUST NOT:

- ❌ Skip code checking to save time
- ❌ Assume "CI will catch it"
- ❌ Assume "FM will review it"
- ❌ Assume "someone else will check it"
- ❌ Delegate code checking responsibility implicitly

### D. FM Verification Authority

FM MUST:

1. ✅ Verify that code checking was performed by builders
2. ✅ Reject work where code checking is absent or superficial
3. ✅ Require evidence of code checking in Builder QA Reports
4. ✅ Require re-execution if obvious defects are detected
5. ✅ Treat missing code checking as governance violation

FM MUST NOT:

- ❌ Perform code checking on behalf of builders
- ❌ Accept work without code checking evidence
- ❌ Allow builders to bypass code checking responsibility

### E. Code Checking vs CI/Review Distinction

**Code checking** is:
- Builder self-review of generated code
- Pre-handover verification of correctness
- Builder obligation, not optional practice
- Performed BEFORE handover

**Code checking is NOT**:
- CI validation (happens after handover)
- FM review (FM verifies process, not code)
- Human code review (happens after merge gate)
- Quality gate (gates validate outputs, not process)

### F. Critical Prohibition

**"Someone else will review it" is NOT a valid execution posture.**

Code checking is a **builder obligation**, not an optional quality practice.

### G. Enforcement

**Violation Handling**:

- Builder skipping code checking → **Constitutional Violation**
- Builder delegating code checking to CI/FM → **Governance Violation**
- FM accepting work without code checking evidence → **FM Non-Compliance**
- Builder claiming "someone will review it" → **Invalid Execution Posture**

---

## VIII. Success Criteria

This specification is successfully implemented when:

1. ✅ FM agent contract explicitly states escalation responsibilities
2. ✅ FM agent contract explicitly states capability selection authority
3. ✅ FM agent contract explicitly defines halt semantics
4. ✅ FM execution surface can represent halt state
5. ✅ FM execution surface can represent escalation events
6. ✅ FM execution surface can represent capability decisions
7. ✅ Builder contracts acknowledge FM halt authority
8. ✅ Escalation and halt are observable without inference
9. ✅ Capability classes are consistently named
10. ✅ Ripple intelligence demonstrates propagation
11. ✅ **NEW**: Builder contracts explicitly require code checking
12. ✅ **NEW**: FM agent contract explicitly states code checking verification authority
13. ✅ **NEW**: "Someone else will review it" is explicitly prohibited
14. ✅ **NEW**: Code checking evidence required in Builder QA Reports

---

## IX. Enforcement

This specification is **MANDATORY** and **ACTIVATED** as of 2026-01-03.

**Violation Handling**:

- FM proceeding without complexity assessment → **Constitutional Violation**
- FM bypassing cognitive limits → **Constitutional Violation**
- FM failing to escalate when required → **Constitutional Violation**
- Execution surface lacking halt state → **Governance Gap**
- Builder ignoring FM halt → **Agent Boundary Violation**
- **NEW**: Builder skipping code checking → **Constitutional Violation**
- **NEW**: Builder delegating code checking to CI/FM → **Governance Violation**
- **NEW**: FM accepting work without code checking evidence → **FM Non-Compliance**
- **NEW**: Builder claiming "someone will review it" → **Invalid Execution Posture**

---

## X. References

- **BUILD_PHILOSOPHY.md** Section X (Escalation Procedures)
- **FM_EXECUTION_MANDATE.md** Section VI (STOP and Escalation Semantics)
- **AGENT_CONSTITUTION.md** Section VIII.3 (Escalate When Blocked)
- **GOVERNANCE_AUTHORITY_MATRIX.md** Section IX (Escalation Authority)
- **PR_GATE_FAILURE_HANDLING_PROTOCOL.md** Section IV (Escalation Protocol)

---

**Escalate proactively. Scale capability intentionally. Halt when needed. Check code always.**

*END OF FM AI ESCALATION AND CAPABILITY-AWARE SCALING SPECIFICATION*
