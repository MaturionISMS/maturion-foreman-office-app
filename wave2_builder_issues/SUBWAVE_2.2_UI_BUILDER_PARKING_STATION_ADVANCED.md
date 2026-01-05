# Subwave 2.2: Parking Station Advanced — ui-builder Build-to-Green

**Wave:** 2.0  
**Subwave:** 2.2  
**Builder:** ui-builder  
**QA Range:** QA-376 to QA-385 (10 QA components)  
**Complexity:** LOW  
**Duration Estimate:** 3-4 days  
**Dependencies:** GATE-SUBWAVE-2.1 PASS  
**Status:** READY FOR AUTHORIZATION (pending Subwave 2.1 completion)

---

## Executive Summary

Implement **Parking Station Advanced** features for the Foreman Office App to make **10 RED tests GREEN**.

**Mission:** Add advanced features to the Parking Station including prioritization, bulk operations, and enhanced issue management.

**Context:**
- Builds on Wave 1.0 Parking Station foundation (QA-043 to QA-046)
- Adds prioritization features (5 QA)
- Adds bulk operations (5 QA)

**Critical Boundaries:**
- This is Subwave 2.2 of Wave 2.0 (14 total subwaves)
- Sequential to Subwave 2.1 (same builder)
- Must complete before Subwave 2.3 can start

---

## Scope Definition

### QA Components to Implement

**Total Test Count:** 10 tests  
**Test Location:** `tests/wave2_0_qa_infrastructure/test_parking_station_advanced_*.py`

**Advanced Parking Station Features:**
- **Prioritization Features** (QA-376 to QA-380): 5 tests
  - QA-376: Priority UI component rendering
  - QA-377: Priority assignment logic
  - QA-378: Priority-based sorting
  - QA-379: Priority escalation handling
  - QA-380: Priority visualization

- **Bulk Operations** (QA-381 to QA-385): 5 tests
  - QA-381: Bulk selection UI
  - QA-382: Bulk action handlers
  - QA-383: Bulk move operations
  - QA-384: Bulk status updates
  - QA-385: Bulk operation validation

### Out of Scope
- ❌ Enhanced Dashboard features — Subwave 2.1, do not modify
- ❌ System optimizations — Subwaves 2.3+, do not modify
- ❌ Any API, Schema, or Integration components — other builders
- ❌ Extended parking QA beyond QA-376 to QA-385

---

## Input Artifacts

### Architecture (Frozen)
- **Wave 2 Architecture Specification** (frozen before Wave 2.0)
- Section: Parking Station Advanced (expansion of Wave 1 Parking Station)
- All component contracts defined and frozen

### References
- **WAVE_2_ROLLOUT_PLAN.md** — Section II, Subwave 2.2 specification
- **WAVE_2_IMPLEMENTATION_PLAN.md** — Wave 2 scope and objectives
- **FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md** — Wave 1 Parking Station foundation

### QA Catalog
- **QA_CATALOG.md** (updated for Wave 2)
- QA-376 to QA-385 specifications

### Test Suite (RED)
- **Location:** `tests/wave2_0_qa_infrastructure/`
- **Status:** All 10 tests RED (awaiting implementation)

---

## Task

### Primary Objective
**Implement Parking Station Advanced features to make all 10 RED tests GREEN.**

### Implementation Requirements

1. **Enhance Parking Station Module**
   - Extend existing `ui/src/components/parking-station/` structure
   - Create prioritization components
   - Create bulk operation components
   - All enhancements integrate with Wave 1 Parking Station

2. **Implement Advanced Features**
   - Implement prioritization per frozen architecture
   - Implement bulk operations per frozen architecture
   - Follow architecture contracts exactly
   - Ensure tenant isolation via `organisation_id`

3. **Achieve Build-to-Green**
   - Make all 10 tests GREEN
   - Achieve GREEN on **first attempt**
   - Zero test debt

4. **Code Checking (Mandatory)**
   - Perform self-code-checking
   - Verify logical correctness
   - Document code checking evidence

---

## Execution Instructions

### Step 1: Review Input Artifacts
- Read frozen Wave 2 architecture (Parking Station Advanced section)
- Review QA catalog (QA-376 to QA-385)
- Inspect RED test suite

### Step 2: Enhance Parking Station Module
- Extend existing parking station components
- Create prioritization components
- Create bulk operation handlers

### Step 3: Implement Advanced Features
- Implement per architecture spec
- Follow test-driven approach
- Ensure integration with existing Wave 1 Parking Station

### Step 4: Validate Tests
```bash
pytest tests/wave2_0_qa_infrastructure/test_parking_station_advanced_*.py -v
```

**Expected:** 10/10 tests GREEN, zero failures

**Note:** No intermediate checkpoint required (≤10 QA)

### Step 5: Perform Code Checking
- Review all generated code
- Verify architecture alignment
- Document findings

### Step 6: Generate Evidence
- Generate Builder QA Report
- Evidence artifacts:
  - `evidence/wave-2.0/ui-builder/subwave-2.2/qa_test_results.xml`
  - `evidence/wave-2.0/ui-builder/subwave-2.2/qa_evidence_summary.json`
  - `WAVE_2.2_BUILDER_COMPLETION_REPORT.md`

### Step 7: Submit for Gate Validation
- Commit to new PR
- Report COMPLETE state to FM

---

## Success Criteria

### Gate Requirements (GATE-SUBWAVE-2.2)

- ✅ All 10 QA GREEN (100%)
- ✅ Zero test debt
- ✅ Architecture alignment verified
- ✅ Code checking performed and documented
- ✅ Evidence artifacts complete
- ✅ Builder completion report with COMPLETE terminal state
- ✅ FM gate review PASS

**Gate Pass:** ALL requirements satisfied  
**Gate Fail:** ANY requirement not satisfied

---

## Execution State Discipline (Terminal States Only)

### Allowed States
1. **BLOCKED** — Cannot proceed
2. **COMPLETE** — 10/10 GREEN, all artifacts ready

### Prohibited States
❌ Partial progress, percentages, incremental updates

---

## Builder Appointment Package

### 1. Scope Statement
- **QA Range:** QA-376 to QA-385
- **QA Count:** 10 components
- **Complexity:** LOW
- **Duration:** 3-4 days

### 2. Architecture References
- Wave 2 Architecture Specification (Parking Station Advanced)
- Wave 1 Parking Station (integration points)

### 3. QA-to-Red Confirmation
- All 10 QA in RED state before execution

### 4. Execution State Discipline
- Terminal states: BLOCKED or COMPLETE only
- No checkpoint required (≤10 QA)

### 5. Evidence Requirements
- Test results, evidence summary, completion report

### 6. Governance References
- BUILD_PHILOSOPHY.md, ui-builder contract, BL-016/018/019

---

## Dependencies

### Prerequisites (Blocking)
- ✅ **Wave 1.0 Complete** — SATISFIED
- ⏳ **GATE-SUBWAVE-2.1 PASS** — BLOCKING (must complete before 2.2 starts)

### Downstream Dependencies
- **Subwave 2.3** — BLOCKED until GATE-SUBWAVE-2.2 PASS

### Parallel Execution
- **None** — Sequential to Subwave 2.1 (same builder)

---

## Parallelism and Sequencing

### Blocking Condition
- **BLOCKED** until GATE-SUBWAVE-2.1 PASS

### Sequential Execution
- Follows Subwave 2.1 (ui-builder sequential execution)
- Must complete before Subwave 2.3

---

## Deliverables

1. **Production Code**
   - Enhanced Parking Station components
   - Prioritization components
   - Bulk operation handlers

2. **Test Results**
   - All 10 tests GREEN

3. **Documentation**
   - Builder QA Report (`WAVE_2.2_BUILDER_COMPLETION_REPORT.md`)

---

## Timeline Expectation

**Duration:** 3-4 days  
**No Checkpoint Required** (≤10 QA)

---

## FM Authorization

**Status:** READY FOR AUTHORIZATION (pending Subwave 2.1 completion)  
**Authority:** Maturion Foreman (FM)  
**FM Agent Contract Version:** 3.3.0  
**Rollout Plan Reference:** WAVE_2_ROLLOUT_PLAN.md Section II, Subwave 2.2

---

**END SUBWAVE 2.2 BUILDER SUB-ISSUE SPECIFICATION**
