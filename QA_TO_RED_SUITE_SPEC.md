# QA-to-Red Suite Specification — RED/GREEN Scope Semantics

**Version:** 2.0  
**Status:** Phase 4.4 Deliverable (Re-derived from Architecture V2)  
**Date:** 2025-12-31  
**Owner:** Foreman (FM)  
**Authority:** Derived from FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md  
**Canonical Location:** `/QA_TO_RED_SUITE_SPEC.md`

---

## Purpose

This document defines the **deterministic semantics** of RED and GREEN states in the QA-to-Red suite:
- What "RED" means in bootstrap (QA-to-Red phase)
- What "GREEN scope" means per builder assignment
- How partial green is measured and gated
- How "allowed red" sets enable progressive build

This enables **bounded builder assignment** where:
- Builder A: build-to-green for QA-001 to QA-010
- Builder B: build-to-green for QA-011 to QA-020
- All other QA remain RED without blocking unrelated work

---

## Constitutional Hierarchy

```
FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md (Architecture Contract)
    ↓
QA_CATALOG.md (QA Index)
    ↓
QA_TO_RED_SUITE_SPEC.md (THIS DOCUMENT - RED/GREEN Semantics)
    ↓
QA_TRACEABILITY_MATRIX.md (Bidirectional Traceability)
    ↓
BUILDER_GREEN_SCOPE_RULES.md (Assignment Rules)
```

---

## 1. RED State Definition (QA-to-Red Phase)

### 1.1 What RED Means

In the **QA-to-Red phase** (Phase 4.4 - design only):

**RED means:**
- The QA component is **defined** (numbered, named, mapped to architecture)
- The QA component is **NOT implemented** (no test code exists)
- The QA component is **NOT executable** (cannot run)
- The QA component **proves functionality does not exist**

**RED is expected and correct during QA-to-Red:**
- All 400+ QA components START as RED
- RED proves the system is hollow (not yet built)
- RED enables deterministic Build-to-Green

### 1.2 RED State Verification

**How to verify a QA component is RED:**

1. **Check Implementation:**
   - Test file does NOT exist
   - Test function does NOT exist
   - Test code is NOT written

2. **Check Executability:**
   - Running the QA component fails (test not found)
   - No test output generated
   - No evidence artifacts produced

3. **Check Evidence Store:**
   - No evidence for QA-XXX in evidence store
   - No QA execution results
   - No GREEN status recorded

**RED State Properties:**
- Initial state: RED by default
- Cannot accidentally become GREEN (no code to pass)
- Deterministic (RED until implemented)
- Auditable (absence of code is provable)

### 1.3 RED State Documentation

For each QA component in RED state, the following is documented in QA_CATALOG.md:

- **QA ID:** QA-XXX
- **Name:** Human-readable name
- **Architectural Element:** Component/Flow/State/Failure mapped to
- **Expected Initial State:** RED (not yet implemented)
- **Expected Evidence (when GREEN):** What artifacts prove the QA passes

**Example:**
```
QA-042: Dashboard UI error handling
- Architectural Element: DASH-04 Dashboard UI Renderer
- Initial State: RED (not implemented)
- Expected Evidence (GREEN): 
  - Test execution log showing error scenario triggered
  - Screenshot of error UI displayed correctly
  - Audit log entry for error handling
```

---

## 2. GREEN State Definition (Build-to-Green Phase)

### 2.1 What GREEN Means

In the **Build-to-Green phase** (Wave 1.0+ - implementation):

**GREEN means:**
- The QA component is **implemented** (test code exists)
- The QA component is **executable** (can run)
- The QA component **passes** (all assertions succeed)
- The QA component **produces evidence** (artifacts prove functionality exists)

**GREEN is the goal of Build-to-Green:**
- Builder implements code to make assigned QA components GREEN
- GREEN proves functionality exists and works
- GREEN enables progressive build (partial system functional)

### 2.2 GREEN State Verification

**How to verify a QA component is GREEN:**

1. **Check Implementation:**
   - Test file exists
   - Test function exists and is complete
   - Test code is executable

2. **Check Executability:**
   - Running the QA component succeeds (test found and runs)
   - Test output shows PASS
   - All assertions succeed

3. **Check Evidence Store:**
   - Evidence for QA-XXX exists in evidence store
   - QA execution result shows GREEN status
   - Evidence artifacts match expected format

**GREEN State Properties:**
- Achieved only through implementation
- Cannot be GREEN without passing test
- Deterministic (GREEN means code works)
- Auditable (evidence proves GREEN)

### 2.3 GREEN State Documentation

For each QA component in GREEN state, the following is documented:

- **QA ID:** QA-XXX
- **Status:** GREEN
- **Test Execution Timestamp:** When the test passed
- **Evidence Location:** Path to evidence artifacts
- **Requirements Covered:** FR IDs validated
- **Components Covered:** Architecture components validated

**Example:**
```
QA-042: Dashboard UI error handling
- Status: GREEN
- Execution Timestamp: 2025-12-31T12:00:00Z
- Test File: tests/dashboard/test_ui_error_handling.py
- Test Function: test_dashboard_error_display
- Evidence: foreman/evidence/qa/DASH/QA-042/result.json
- Assertions: 5 passed, 0 failed
- Requirements: FR-DASH-2 (Drill-Down)
- Components: DASH-04 (Dashboard UI Renderer)
```

---

## 3. GREEN Scope Definition (Bounded Builder Assignment)

### 3.1 What is GREEN Scope?

**GREEN scope** is the **bounded set of QA components** that a builder is assigned to make GREEN.

**Properties of GREEN Scope:**
- Explicitly bounded (e.g., QA-001 to QA-010, or QA-023, QA-025, QA-030)
- Builder-specific (each builder has own scope)
- Gate-evaluated (only assigned QA checked for GREEN)
- Non-blocking for unassigned QA (other QA can remain RED)

**Example:**
```
Builder A assigned GREEN scope: QA-001 to QA-022
- Builder A must make QA-001 through QA-022 GREEN
- All other QA (QA-023 to QA-400+) can remain RED
- Gate checks only QA-001 to QA-022 for Builder A
- Builder A is NOT blocked by QA-023 being RED
```

### 3.2 GREEN Scope Notation

**Notation Format:**

1. **Range Notation:** `QA-XXX to QA-YYY`
   - Example: `QA-001 to QA-010` means QA-001, QA-002, ..., QA-010 (inclusive)

2. **List Notation:** `QA-XXX, QA-YYY, QA-ZZZ`
   - Example: `QA-001, QA-005, QA-010` means exactly those three QA components

3. **Wildcard Notation:** `QA-DOMAIN-*`
   - Example: `QA-CONV-*` means all Conversational Interface QA (but QA Catalog uses sequential numbers, so this would be `QA-001 to QA-022`)

4. **Mixed Notation:** `QA-XXX to QA-YYY, QA-ZZZ`
   - Example: `QA-001 to QA-010, QA-015` means range plus one specific QA

### 3.3 GREEN Scope Assignment

**Assignment Process:**

1. **FM determines GREEN scope** for each builder based on:
   - Architectural subsystem assignment (e.g., Builder A gets Conversational Interface)
   - QA range mapping (subsystem → QA range via QA_CATALOG.md)
   - Builder capability (some builders specialize in certain QA types)

2. **GREEN scope is explicit in builder task:**
   - Builder receives: "Make QA-001 to QA-022 GREEN"
   - Builder knows exact QA numbers
   - Builder focuses only on assigned QA
   - Builder is NOT responsible for unassigned QA

3. **GREEN scope is immutable during wave:**
   - Scope does not change mid-wave
   - If scope expansion needed, new wave initiated
   - Audit trail of scope assignments

**Example Assignment:**
```
Wave 1.0 - Conversational Interface Implementation
- Builder: ui-builder
- GREEN Scope: QA-019 to QA-022 (CONV-05 UI Renderer)
- Required GREEN: QA-019, QA-020, QA-021, QA-022 (4 QA components)
- Allowed RED: All other QA (QA-001 to QA-018, QA-023 to QA-400+)
- Gate Evaluation: Check only QA-019 to QA-022
- Success Criteria: All 4 assigned QA must be GREEN
```

---

## 4. Partial Green Measurement

### 4.1 What is Partial Green?

**Partial green** means:
- SOME QA components are GREEN
- SOME QA components are RED
- System is **partially functional**
- Progressive build is in progress

**Partial green is normal and expected:**
- During progressive build, not all QA is GREEN at once
- Builders work on different subsystems in parallel
- Each builder makes their assigned QA GREEN incrementally

### 4.2 How Partial Green is Measured

**Measurement Formula:**

```
Green Percentage = (Number of GREEN QA) / (Total QA in Scope) × 100%
```

**Example:**
```
Builder A assigned QA-001 to QA-022 (22 QA components)
- Currently GREEN: QA-001, QA-002, QA-003, QA-004, QA-005 (5 QA)
- Currently RED: QA-006 to QA-022 (17 QA)
- Green Percentage: 5 / 22 × 100% = 22.7% GREEN
- Builder A progress: 22.7% complete
```

**System-Wide Green Percentage:**

```
System Green % = (Total GREEN QA) / (Total QA) × 100%
```

**Example:**
```
Total QA: 400 components
GREEN: 50 QA components
RED: 350 QA components
System Green %: 50 / 400 × 100% = 12.5% GREEN
```

### 4.3 Progress Tracking

**Progress Metrics:**

1. **Per-Builder Progress:**
   - GREEN count for assigned QA
   - RED count for assigned QA
   - Percentage complete
   - Estimated completion time

2. **Per-Wave Progress:**
   - GREEN count for all QA in wave
   - RED count for all QA in wave
   - Percentage complete
   - Gate readiness status

3. **System-Wide Progress:**
   - Total GREEN QA
   - Total RED QA
   - Overall system completeness
   - Remaining work estimation

**Dashboard Display:**
```
Builder A: QA-001 to QA-022
├─ GREEN: 5 / 22 (22.7%)
├─ RED: 17 / 22 (77.3%)
└─ Status: IN_PROGRESS

Builder B: QA-023 to QA-042
├─ GREEN: 2 / 20 (10%)
├─ RED: 18 / 20 (90%)
└─ Status: IN_PROGRESS

System Overall: 400 QA components
├─ GREEN: 7 / 400 (1.75%)
├─ RED: 393 / 400 (98.25%)
└─ Status: EARLY_BUILD
```

---

## 5. Allowed RED Set (Progressive Build Enabler)

### 5.1 What is Allowed RED Set?

**Allowed RED set** is the **explicit list of QA components** that are **permitted to remain RED** without blocking the current wave or builder.

**Purpose:**
- Enable progressive build (not all features at once)
- Prevent false blocking (unassigned QA being RED is OK)
- Focus gating on assigned QA only

**Example:**
```
Wave 1.0 Gate:
- Required GREEN: QA-001 to QA-022 (Conversational Interface)
- Allowed RED: QA-023 to QA-400+ (all other subsystems)
- Gate Logic: Check if QA-001 to QA-022 are all GREEN
- Gate ignores RED state of QA-023 to QA-400+
```

### 5.2 Allowed RED Set Notation

**Notation Format:**

1. **Range Notation:** `QA-XXX to QA-YYY`
   - Example: `QA-023 to QA-400` means QA-023, QA-024, ..., QA-400 can be RED

2. **Wildcard Notation:** `QA-DOMAIN-*` (conceptual, maps to ranges)
   - Example: `QA-DASH-*` means Dashboard QA can be RED (translates to QA-023 to QA-042)

3. **All Except Notation:** `ALL EXCEPT QA-XXX to QA-YYY`
   - Example: `ALL EXCEPT QA-001 to QA-022` means everything but Conversational Interface can be RED

### 5.3 Allowed RED Set in Gates

**Gate Configuration Example:**

```yaml
gate:
  name: "Conversational Interface Gate"
  id: "GATE-CONV"
  required_green:
    - QA-001 to QA-022
  allowed_red:
    - QA-023 to QA-400+
  enforcement: "BLOCKING"
  description: "Conversational Interface must be fully functional before proceeding"
```

**Gate Evaluation Logic:**

1. **Check Required GREEN:**
   - Are QA-001 to QA-022 all GREEN?
   - If YES: gate PASS (proceed)
   - If NO: gate FAIL (identify which QA are still RED)

2. **Ignore Allowed RED:**
   - QA-023 to QA-400+ can be RED
   - Their RED status does NOT block the gate
   - No evaluation needed for allowed RED set

3. **Report Gate Status:**
   - PASS: All required QA are GREEN
   - FAIL: List which required QA are still RED
   - Allowed RED status: informational only (not blocking)

**Example Gate Report:**
```
Gate: GATE-CONV
Status: FAIL
Required GREEN (22 QA):
  ✅ QA-001 to QA-005 (GREEN)
  ❌ QA-006 to QA-022 (RED) ← BLOCKING
Allowed RED (378 QA):
  ❌ QA-023 to QA-400 (RED) ← OK, not blocking
Decision: Gate BLOCKED until QA-006 to QA-022 are GREEN
```

---

## 6. Gate Semantics (Progressive Build Control)

### 6.1 Gate Purpose

**Gates** control progressive build by:
- Enforcing required QA GREEN before progression
- Allowing unassigned QA to remain RED
- Preventing premature advancement
- Providing clear blocking/unblocking criteria

### 6.2 Gate Types

**1. Wave Gates:**
- Control progression between build waves
- Example: "Wave 1 Gate" checks all Wave 1 QA are GREEN before Wave 2 starts

**2. Builder Gates:**
- Control individual builder completion
- Example: "Builder A Gate" checks Builder A's assigned QA are GREEN before handover

**3. Milestone Gates:**
- Control major milestones (e.g., "Foundation Complete", "Core Features Complete")
- Example: "Foundation Gate" checks all foundation subsystems are GREEN

**4. Final Gate:**
- Control overall system completion
- Example: "System Complete Gate" checks ALL 400+ QA are GREEN before delivery

### 6.3 Gate Configuration Format

**Standard Gate Configuration:**

```yaml
gate:
  name: "Human-readable gate name"
  id: "GATE-XXX"
  type: "wave" | "builder" | "milestone" | "final"
  required_green:
    - QA-XXX to QA-YYY
    - QA-ZZZ
  allowed_red:
    - QA-AAA to QA-BBB
    - ALL EXCEPT required_green (alternative notation)
  enforcement: "BLOCKING" | "WARNING"
  escalation_on_failure: true | false
  description: "Gate purpose and criteria"
```

### 6.4 Gate Evaluation Algorithm

**Step-by-Step Gate Evaluation:**

1. **Load Gate Configuration:**
   - Identify gate ID and type
   - Parse required_green set
   - Parse allowed_red set

2. **Query QA Status:**
   - For each QA in required_green: check if GREEN
   - For each QA in allowed_red: informational only (not blocking)

3. **Evaluate Pass/Fail:**
   - IF all required_green QA are GREEN: gate PASS
   - ELSE: gate FAIL (identify RED QA in required_green)

4. **Generate Report:**
   - List GREEN QA in required_green
   - List RED QA in required_green (blockers)
   - List RED QA in allowed_red (informational)
   - Provide gate decision (PASS/FAIL)

5. **Execute Enforcement:**
   - If enforcement = "BLOCKING" and gate FAIL: block progression
   - If enforcement = "WARNING" and gate FAIL: warn but allow progression
   - If escalation_on_failure = true and gate FAIL: create escalation

**Example Evaluation:**

```
Gate: GATE-FOUNDATION
Type: milestone
Required GREEN: QA-001 to QA-100 (foundation subsystems)
Allowed RED: QA-101 to QA-400+ (application subsystems)

Query Results:
- QA-001 to QA-080: GREEN (80 QA)
- QA-081 to QA-100: RED (20 QA) ← BLOCKING
- QA-101 to QA-400: RED (300 QA) ← OK, allowed

Gate Decision: FAIL
Blockers: QA-081 to QA-100 must be made GREEN
Enforcement: BLOCKING (build cannot proceed to Wave 2)
Escalation: Created (Builder assigned QA-081 to QA-100 notified)
```

---

## 7. RED-to-GREEN Transition Rules

### 7.1 Transition Trigger

**A QA component transitions RED → GREEN when:**

1. **Test Code is Implemented:**
   - Test file created
   - Test function written
   - All assertions implemented

2. **Test Execution Passes:**
   - Test runs without errors
   - All assertions succeed
   - No test failures

3. **Evidence is Generated:**
   - Evidence artifacts produced
   - Evidence stored in evidence store
   - Evidence matches expected format

**Transition is Atomic:**
- QA is either RED or GREEN (no partial state)
- Transition happens when test passes (not when code is written)
- Once GREEN, QA should remain GREEN (regression prevention)

### 7.2 Transition Verification

**How to verify RED → GREEN transition:**

1. **Before Transition (RED):**
   - QA status: RED
   - Test execution: FAIL or NOT_FOUND
   - Evidence: NONE

2. **After Transition (GREEN):**
   - QA status: GREEN
   - Test execution: PASS
   - Evidence: EXISTS and VALID

3. **Transition Event:**
   - Timestamp recorded
   - Actor recorded (which builder)
   - Evidence location recorded
   - Audit log entry created

### 7.3 Transition Audit Trail

**Audit Log Entry Format:**

```json
{
  "event": "QA_TRANSITION",
  "qa_id": "QA-042",
  "from_state": "RED",
  "to_state": "GREEN",
  "timestamp": "2025-12-31T12:00:00Z",
  "actor": "ui-builder",
  "test_execution_id": "exec-12345",
  "evidence_location": "foreman/evidence/qa/DASH/QA-042/result.json",
  "requirements_validated": ["FR-DASH-2"],
  "components_validated": ["DASH-04"]
}
```

---

## 8. Regression Prevention (GREEN-to-RED Prevention)

### 8.1 GREEN Must Stay GREEN

**Once a QA component is GREEN, it MUST remain GREEN:**

- No regressions allowed
- Any GREEN → RED transition is a **build failure**
- Regression triggers immediate escalation

### 8.2 Regression Detection

**How to detect GREEN → RED regression:**

1. **Continuous QA Execution:**
   - All GREEN QA re-executed periodically
   - Any GREEN QA that fails → regression detected

2. **Pre-Commit QA Execution:**
   - Before code commit, run all GREEN QA
   - If any GREEN QA fails, commit blocked

3. **Regression Alert:**
   - Regression detected → alert created
   - Alert includes: which QA regressed, when, which code change caused it
   - Alert routed to builder who caused regression

### 8.3 Regression Handling

**When regression detected:**

1. **Block Build:**
   - Build state: BLOCKED
   - No further progression until regression fixed

2. **Create Escalation:**
   - Escalation type: REGRESSION
   - Escalation priority: HIGH or CRITICAL
   - Escalation context: which QA, which code change, which builder

3. **Fix Regression:**
   - Builder identifies root cause
   - Builder fixes code
   - Builder re-runs QA to confirm GREEN
   - Regression escalation closed

4. **Audit Regression:**
   - Regression logged in audit trail
   - Root cause documented
   - Prevention measures identified

---

## 9. QA Execution Order

### 9.1 Why Order Matters

**QA execution order is deterministic:**

- Some QA depend on others (e.g., QA-002 requires QA-001 to pass first)
- Execution order affects efficiency (run foundation QA before application QA)
- Execution order affects failure diagnosis (early failure = no need to run later QA)

### 9.2 Execution Order Rules

**1. Sequential by Number (Default):**
- Execute QA-001, then QA-002, then QA-003, ...
- Simple and predictable
- May be inefficient if QA are independent

**2. Dependency-Ordered:**
- Execute QA with no dependencies first
- Execute dependent QA only after dependencies pass
- More efficient but requires dependency graph

**3. Parallel Execution:**
- Execute independent QA in parallel
- Significant speed improvement
- Requires careful dependency management

### 9.3 Dependency Notation

**QA Dependency Format:**

```
QA-XXX depends on QA-YYY
```

**Example:**
```
QA-002 depends on QA-001
- QA-002 (Retrieve conversation) requires QA-001 (Create conversation) to pass first
- If QA-001 fails, QA-002 is skipped (cannot test retrieve if create doesn't work)
```

**Dependency Graph (Partial Example):**
```
QA-001 (no dependencies)
  └─> QA-002 (depends on QA-001)
       └─> QA-003 (depends on QA-002)

QA-006 (no dependencies)
  └─> QA-007 (depends on QA-006)

QA-011 (depends on QA-001)
```

---

## 10. QA Evidence Requirements

### 10.1 Evidence Purpose

**Evidence serves to:**
- Prove QA component is GREEN (objective verification)
- Enable non-coder verification (no code review needed)
- Support audit and compliance (permanent record)
- Enable failure diagnosis (what went wrong)

### 10.2 Evidence Artifact Format

**Standard Evidence Format (JSON):**

```json
{
  "qa_id": "QA-042",
  "qa_name": "Dashboard UI error handling",
  "status": "GREEN",
  "execution_timestamp": "2025-12-31T12:00:00Z",
  "execution_time_ms": 250,
  "test_framework": "pytest",
  "test_file": "tests/dashboard/test_ui_error_handling.py",
  "test_function": "test_dashboard_error_display",
  "assertions_passed": 5,
  "assertions_total": 5,
  "coverage_percentage": 100.0,
  "evidence_artifacts": [
    {
      "type": "screenshot",
      "location": "foreman/evidence/qa/DASH/QA-042/error_ui.png",
      "description": "Error UI displayed correctly"
    },
    {
      "type": "audit_log",
      "location": "foreman/evidence/qa/DASH/QA-042/audit_log.json",
      "description": "Error handling logged to audit trail"
    }
  ],
  "requirements_covered": ["FR-DASH-2"],
  "components_covered": ["DASH-04"]
}
```

### 10.3 Evidence Storage

**Evidence Location:**
```
foreman/evidence/qa/<SUBSYSTEM>/<QA_ID>/
  ├─ result.json         # QA execution result
  ├─ artifacts/          # Supporting evidence artifacts
  │   ├─ screenshot.png
  │   ├─ database_dump.json
  │   └─ ...
  └─ logs/               # Execution logs
      └─ execution.log
```

**Evidence Retention:**
- Evidence is permanent (never deleted)
- Evidence is immutable (cannot be modified)
- Evidence is version-controlled
- Evidence is auditable

---

## 11. FM Acceptance Declaration

I, Foreman (FM), confirm that this QA-to-Red Suite Specification:

- Defines deterministic RED state semantics (not yet implemented)
- Defines deterministic GREEN state semantics (implemented and passes)
- Defines GREEN scope for bounded builder assignment
- Defines partial green measurement (percentage complete)
- Defines allowed RED set for progressive build
- Defines gate semantics for build control
- Defines RED-to-GREEN transition rules with audit trail
- Defines regression prevention (GREEN must stay GREEN)
- Defines QA execution order and dependencies
- Defines evidence requirements and format
- Aligns with FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md
- Enables non-coder orchestration (no code review required)

**Accepted By:** Foreman (FM)  
**Date:** 2025-12-31  
**Derivation:** Re-derived from Architecture V2 (Wiring-Complete)

---

**End of QA-to-Red Suite Specification**
