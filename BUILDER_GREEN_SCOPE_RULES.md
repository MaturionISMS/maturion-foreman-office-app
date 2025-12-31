# Builder Green Scope Rules — Bounded QA Assignment

**Version:** 2.0  
**Status:** Phase 4.4 Deliverable (Re-derived from Architecture V2)  
**Date:** 2025-12-31  
**Owner:** Foreman (FM)  
**Authority:** Derived from FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md  
**Canonical Location:** `/BUILDER_GREEN_SCOPE_RULES.md`

---

## Purpose

This document defines the **rules for bounded QA assignment** to builders:
- How GREEN scope is determined for each builder
- How gates evaluate only assigned QA (not all QA)
- How builders work in parallel without blocking each other
- How progressive build proceeds with partial GREEN

---

## Core Principle: Bounded Assignment

**Bounded assignment means:**
- Each builder is assigned a **specific, explicit set of QA components**
- Builder's gate checks **only their assigned QA** (not all QA)
- Other QA remaining RED does **NOT block** the builder
- Multiple builders can work in parallel on different QA sets

**Example:**
```
Builder A assigned: QA-001 to QA-022 (Conversational Interface)
Builder B assigned: QA-023 to QA-042 (Dashboard)

Builder A's gate checks: QA-001 to QA-022 only
- If all GREEN → Builder A's gate PASS
- QA-023 to QA-042 being RED does NOT block Builder A

Builder B's gate checks: QA-023 to QA-042 only
- If all GREEN → Builder B's gate PASS
- QA-001 to QA-022 being RED does NOT block Builder B
```

---

## Rule 1: GREEN Scope Assignment

### 1.1 Assignment Process

**FM determines GREEN scope based on:**

1. **Architectural Subsystem:**
   - Builder A → Conversational Interface Subsystem
   - Builder B → Dashboard Subsystem
   - QA range = subsystem's component QA range

2. **Builder Capability:**
   - ui-builder → UI-focused QA (QA-019 to QA-022, QA-036 to QA-042, etc.)
   - api-builder → API-focused QA
   - schema-builder → Data model QA

3. **Progressive Build Wave:**
   - Wave 1: Foundation QA (QA-001 to QA-100)
   - Wave 2: Application QA (QA-101 to QA-200)
   - Wave 3: Integration QA (QA-201 to QA-300)

### 1.2 Assignment Notation

**Standard Assignment Format:**
```
Builder: <builder_name>
GREEN Scope: <QA_range>
Gate: <gate_id>
```

**Example:**
```
Builder: ui-builder
GREEN Scope: QA-019 to QA-022
Gate: GATE-CONV-UI
Required GREEN: QA-019, QA-020, QA-021, QA-022
Allowed RED: All except QA-019 to QA-022
```

### 1.3 Assignment Documentation

**Assignment recorded in:**
- Builder task specification
- Build orchestration metadata
- Gate configuration
- Audit log

---

## Rule 2: Gate Evaluation (Bounded Scope Only)

### 2.1 Gate Evaluation Rule

**Gates evaluate ONLY the builder's assigned QA:**
- Check if assigned QA are GREEN
- Ignore all other QA (allowed to be RED)
- PASS if all assigned QA are GREEN
- FAIL if any assigned QA are RED

### 2.2 Gate Configuration

**Standard Gate Configuration for Bounded Scope:**
```yaml
gate:
  id: "GATE-<BUILDER>-<WAVE>"
  builder: "<builder_name>"
  required_green:
    - <assigned_QA_range>
  allowed_red:
    - ALL EXCEPT <assigned_QA_range>
  enforcement: "BLOCKING"
```

**Example:**
```yaml
gate:
  id: "GATE-UI-BUILDER-WAVE-1"
  builder: "ui-builder"
  required_green:
    - QA-019 to QA-022
  allowed_red:
    - ALL EXCEPT QA-019 to QA-022
  enforcement: "BLOCKING"
```

### 2.3 Gate Evaluation Algorithm

**Step-by-Step:**

1. Load gate configuration
2. Identify builder's assigned QA range
3. Query status of assigned QA only
4. IF all assigned QA are GREEN: gate PASS
5. ELSE: gate FAIL (list which assigned QA are RED)
6. Ignore all non-assigned QA (their status irrelevant)

---

## Rule 3: Parallel Builder Execution

### 3.1 Parallel Work Principle

**Multiple builders can work simultaneously:**
- Builder A: QA-001 to QA-022 (Conversational Interface)
- Builder B: QA-023 to QA-042 (Dashboard)
- Builder C: QA-043 to QA-057 (Parking Station)

**All work in parallel:**
- No dependency between Builder A, B, C
- Each makes their assigned QA GREEN
- Each evaluated by their own gate
- None blocked by others' RED QA

### 3.2 Parallel Execution Example

**Initial State:**
- All 400+ QA are RED

**Wave 1 Assignments:**
- Builder A: QA-001 to QA-022
- Builder B: QA-023 to QA-042
- Builder C: QA-043 to QA-057

**After 1 hour:**
- Builder A: QA-001 to QA-010 GREEN (45% done)
- Builder B: QA-023 to QA-030 GREEN (40% done)
- Builder C: QA-043 to QA-050 GREEN (53% done)

**Gate Status:**
- Builder A gate: FAIL (QA-011 to QA-022 still RED)
- Builder B gate: FAIL (QA-031 to QA-042 still RED)
- Builder C gate: FAIL (QA-051 to QA-057 still RED)

**No blocking between builders:** Each progresses independently

**After 2 hours:**
- Builder A: QA-001 to QA-022 ALL GREEN → Builder A gate PASS ✅
- Builder B: QA-023 to QA-040 GREEN (still working on QA-041, QA-042)
- Builder C: QA-043 to QA-057 ALL GREEN → Builder C gate PASS ✅

**Result:** Builder A and C complete, Builder B continues (no blocking)

---

## Rule 4: Progressive Build Waves

### 4.1 Wave Structure

**Build progresses in waves:**
- Wave 1: Foundation (QA-001 to QA-100)
- Wave 2: Application (QA-101 to QA-200)
- Wave 3: Integration (QA-201 to QA-300)
- Wave 4: Failure Modes (QA-301 to QA-400+)

**Wave Gate:**
- Checks ALL QA assigned in that wave
- Must ALL be GREEN before next wave starts
- Ensures foundation is solid before building on top

### 4.2 Wave Transition Rule

**Transition from Wave N to Wave N+1:**

1. **All builders in Wave N complete:**
   - All assigned QA in Wave N are GREEN
   - All builder gates in Wave N PASS

2. **Wave N Gate evaluation:**
   - Check ALL Wave N QA are GREEN
   - If PASS: proceed to Wave N+1
   - If FAIL: identify blockers, wait for resolution

3. **Wave N+1 initiation:**
   - Assign builders to Wave N+1 QA
   - Wave N+1 gates configured
   - Builders start making Wave N+1 QA GREEN

### 4.3 Wave Gate Configuration

**Example Wave 1 Gate:**
```yaml
gate:
  id: "GATE-WAVE-1"
  type: "wave"
  required_green:
    - QA-001 to QA-100
  allowed_red:
    - QA-101 to QA-400+
  enforcement: "BLOCKING"
  description: "Foundation complete before application build"
```

---

## Rule 5: Dependency Handling

### 5.1 QA Dependencies

**Some QA depend on others:**
- QA-002 (Retrieve conversation) depends on QA-001 (Create conversation)
- QA-007 (Deliver message) depends on QA-006 (Send message)

**Dependency Rule:**
- If QA-B depends on QA-A, then QA-A must be GREEN before QA-B can be tested
- Builder assigned QA-B cannot make it GREEN until QA-A is GREEN

### 5.2 Cross-Builder Dependencies

**If dependency spans builders:**

**Example:**
- Builder A assigned: QA-001 to QA-022
- Builder B assigned: QA-058 to QA-077
- QA-060 (Intent Intake) depends on QA-006 (Message Handler)

**Resolution:**
- Builder B waits for Builder A to make QA-006 GREEN
- Once QA-006 is GREEN, Builder B can proceed with QA-060
- No blocking: Builder B works on non-dependent QA while waiting

### 5.3 Dependency Documentation

**Dependencies documented in QA_CATALOG.md:**
```
QA-060: Intent intake
- Dependencies: QA-006 (Message Handler must be functional)
- Cannot be GREEN until QA-006 is GREEN
```

---

## Rule 6: Failure Escalation

### 6.1 Builder-Specific Escalation

**If builder cannot make assigned QA GREEN:**
- Builder escalates with 5-element escalation (what/why/blocked/decision/consequence)
- Escalation routed to FM
- FM investigates: architecture issue? builder capability? dependency?

### 6.2 Cross-Builder Escalation

**If dependency blocks builder:**
- Builder B waiting on Builder A to finish QA-006
- If Builder A stalls: Builder B escalates dependency delay
- FM intervenes: expedite Builder A, reassign QA, or adjust scope

---

## Rule 7: Complete System Gate (Final Gate)

### 7.1 Final Gate Rule

**System Complete Gate:**
- Checks ALL 400+ QA are GREEN
- No allowed RED (all must be GREEN)
- Enforces complete system functionality
- Only gate that checks all QA

**Final Gate Configuration:**
```yaml
gate:
  id: "GATE-SYSTEM-COMPLETE"
  type: "final"
  required_green:
    - QA-001 to QA-400+
  allowed_red: []
  enforcement: "BLOCKING"
  description: "All QA must be GREEN before system delivery"
```

### 7.2 Handover Criteria

**System ready for handover when:**
- Final gate PASS (all 400+ QA GREEN)
- Evidence for all QA exists
- Audit trail complete
- Architecture traceability verified

---

## FM Acceptance Declaration

I, Foreman (FM), confirm that these Builder Green Scope Rules:

- Define bounded QA assignment (explicit QA range per builder)
- Define gate evaluation rules (check only assigned QA)
- Enable parallel builder execution (no cross-blocking)
- Define progressive build waves (foundation → application → integration → failure modes)
- Handle QA dependencies (wait for dependencies, escalate if blocked)
- Define final system gate (all 400+ QA must be GREEN)
- Align with FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md
- Align with QA_CATALOG.md
- Align with QA_TO_RED_SUITE_SPEC.md
- Enable deterministic build orchestration

**Accepted By:** Foreman (FM)  
**Date:** 2025-12-31  
**Derivation:** Re-derived from Architecture V2 (Wiring-Complete)

---

**End of Builder Green Scope Rules**
