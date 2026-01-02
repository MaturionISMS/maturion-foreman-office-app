# Issue — Wave 1.0.6: ui-builder Build-to-Green

**Builder:** ui-builder  
**Wave:** 1.0.6  
**Phase:** Build-to-Green  
**QA Range:** QA-019 to QA-057 (39 QA components)  
**Dependencies:** schema-builder ✅, api-builder ✅ (all satisfied)  
**Issue Type:** Build-to-Green Implementation  
**Priority:** HIGH  
**Status:** READY TO EXECUTE

---

## Objective

Implement UI components for Foreman Office to make **39 RED tests GREEN**.

**Context:**
- Wave 1.0.3 (ui-builder QA-to-Red) completed successfully
- 39 tests created and currently RED (correct QA-to-Red state)
- Tests prove UI components don't exist yet
- This wave implements production code to make all tests GREEN

---

## Scope

### QA Components to Implement

**Total:** 39 QA components (QA-019 to QA-057)

#### 1. CONV-05: Conversation UI (QA-019 to QA-022) — 4 QA
- Conversational interface components
- Message display, input handling, conversation flow

#### 2. DASH-01: Domain Status Manager UI (QA-023 to QA-027) — 5 QA
- Domain-level status visualization
- Status cards, indicators, navigation

#### 3. DASH-02: Drill-Down Navigator UI (QA-028 to QA-032) — 5 QA
- Hierarchical drill-down interface
- Navigation, breadcrumbs, level transitions

#### 4. DASH-03: Executive View Controller (QA-033 to QA-035) — 3 QA
- Executive-level dashboard controller
- View switching, filters, aggregations

#### 5. DASH-04: Dashboard UI Renderer (QA-036 to QA-042) — 7 QA
- Dashboard rendering engine
- Widget layout, responsive design, data binding

#### 6. PARK-04: Parking Station UI (QA-043 to QA-046) — 4 QA
- Parking station interface
- Intent parking, retrieval, management

#### 7. BUILD-04: Build Visibility UI (QA-047 to QA-050) — 4 QA
- Build progress visualization
- Build state display, progress indicators

#### 8. ESC-04: Escalation UI (QA-051 to QA-057) — 7 QA
- Escalation management interface
- Escalation display, routing, decision handling

---

## Input Artifacts

### Architecture (Frozen)
- **FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md** (frozen 2025-12-31)
- Sections: CONV-05, DASH-01 to DASH-04, PARK-04, BUILD-04, ESC-04
- All UI component contracts defined and frozen

### QA Catalog
- **QA_CATALOG.md**
- QA-019 to QA-057 specifications

### Test Suite (RED)
- **Location:** `tests/wave1_ui/`
- **Files:**
  - `tests/wave1_ui/conftest.py`
  - `tests/wave1_ui/test_conversation_ui.py`
  - `tests/wave1_ui/test_dashboard_ui.py`
  - `tests/wave1_ui/test_dashboard_renderer.py`
  - `tests/wave1_ui/test_parking_station_ui.py`
  - `tests/wave1_ui/test_build_visibility_and_escalation_ui.py`
- **Status:** All 39 tests RED (awaiting implementation)

### Evidence Artifacts
- **QA-to-Red Evidence:** `evidence/wave-1.0/ui-builder/`
- **QA Test Results:** `evidence/wave-1.0/ui-builder/qa_test_results.xml`
- **QA Evidence Summary:** `evidence/wave-1.0/ui-builder/qa_evidence_summary.json`

---

## Task

### Primary Objective
**Implement UI components to make all 39 RED tests GREEN.**

### Implementation Requirements

1. **Create Module Structure**
   - Create `foreman/ui/` module directory
   - Organize components by subsystem

2. **Implement UI Components**
   - Implement all 8 UI component modules per frozen architecture
   - Follow architecture contracts exactly
   - Implement all props, state, rendering, interactions per tests

3. **Achieve Build-to-Green**
   - Make all 39 tests GREEN
   - Achieve GREEN on **first attempt** (One-Time Build Correctness)
   - Zero test debt (no skips, no TODOs, no incomplete tests)

4. **Generate Evidence**
   - Update evidence artifacts
   - Generate Builder QA Report
   - Generate completion summary

---

## Constraints

### MUST NOT
- ❌ Modify frozen architecture
- ❌ Modify test suite (unless correcting obvious test bugs)
- ❌ Modify governance documents
- ❌ Skip, comment out, or mark tests as TODO
- ❌ Add test debt
- ❌ Deviate from frozen architecture specifications

### MUST
- ✅ Implement exactly as specified in frozen architecture
- ✅ Make all 39 tests GREEN
- ✅ Achieve Build-to-Green on first attempt
- ✅ Maintain zero test debt
- ✅ Follow BUILD_PHILOSOPHY.md principles
- ✅ Generate complete evidence artifacts

---

## Success Criteria

### Gate Requirements (GATE-UI-BUILDER-BUILD-TO-GREEN-WAVE-1.0)

- ✅ All 39 tests GREEN (100% pass rate)
- ✅ Zero test debt (no skips, no TODOs, no incomplete tests)
- ✅ Architecture alignment verified (100% from frozen spec)
- ✅ Build-to-Green achieved on first attempt
- ✅ Evidence artifacts complete
- ✅ Builder QA Report submitted

**Gate Pass:** ALL requirements satisfied  
**Gate Fail:** ANY requirement not satisfied

---

## Deliverables

1. **Production Code**
   - `foreman/ui/conversation.py` (or React/Vue equivalent)
   - `foreman/ui/dashboard.py`
   - `foreman/ui/parking.py`
   - `foreman/ui/build_visibility.py`
   - `foreman/ui/escalation.py`
   - All supporting modules

2. **Test Results**
   - All 39 tests GREEN
   - Updated test results XML
   - Updated evidence summary JSON

3. **Documentation**
   - Builder QA Report (BUILDER_QA_REPORT.md)
   - Completion summary (WAVE_1.0.6_COMPLETION_SUMMARY.md)
   - Updated evidence artifacts

---

## Execution Instructions

### 1. Review Input Artifacts
- Read frozen architecture (FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md)
- Review QA catalog (QA_CATALOG.md, QA-019 to QA-057)
- Inspect RED test suite (`tests/wave1_ui/`)
- Review QA-to-Red evidence artifacts

### 2. Create Module Structure
```bash
mkdir -p foreman/ui
touch foreman/ui/__init__.py
```

### 3. Implement UI Components
- Implement each UI component module per architecture
- Follow frozen contracts exactly
- Implement all required functionality per tests

### 4. Validate Tests
```bash
pytest tests/wave1_ui/ -v
```

**Expected:** 39/39 tests GREEN, zero failures

### 5. Generate Evidence
- Update evidence artifacts
- Generate Builder QA Report
- Generate completion summary

### 6. Submit for Gate Validation
- Commit all changes
- Push to PR
- Request FM gate validation

---

## Dependencies

### Prerequisite Builders (All Satisfied ✅)
- **schema-builder:** QA-001 to QA-018 (18 QA) — ✅ COMPLETE, MERGED
- **api-builder:** QA-058 to QA-092 (35 QA) — ✅ COMPLETE, MERGED

### Parallel Execution
- **qa-builder (Wave 1.0.7):** Can execute concurrently (no conflicts)

---

## FM Support

**Architecture Questions:**
- Refer to frozen architecture (FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md)
- Escalate if architecture ambiguities discovered

**Test Questions:**
- Refer to test suite (`tests/wave1_ui/`)
- Tests define expected behavior precisely

**Governance Questions:**
- Refer to BUILD_PHILOSOPHY.md
- Escalate if governance clarification needed

---

## Gate Validation

**Gate Owner:** Foreman (FM)

**Gate Process:**
1. Builder submits PR with all deliverables
2. FM reviews submission against gate requirements
3. FM validates all 39 tests GREEN
4. FM verifies zero test debt
5. FM confirms architecture alignment
6. FM confirms Build-to-Green achieved on first attempt
7. FM declares gate PASS or FAIL
8. If PASS: FM approves merge
9. If FAIL: FM provides corrective instructions

---

## Timeline Expectation

**Phase:** Build-to-Green implementation  
**Estimated Duration:** ~1-2 hours (based on previous builder performance)  
**Critical Path:** Yes (required for Wave 1.0 completion)

---

## Notes

- This is a **Build-to-Green** task (tests exist, implementation needed)
- Architecture is **frozen** (no design changes allowed)
- One-Time Build Correctness: GREEN must be achieved on **first attempt**
- Zero test debt is **absolute requirement**
- All 39 tests must be GREEN for gate PASS

---

**Issue Created By:** Maturion Foreman (FM)  
**Authority:** FM Agent Contract v3.0.0  
**Date:** 2026-01-02 15:54 UTC

---

**END OF ISSUE SPECIFICATION**
