# Wave 1.0 Build-to-Green Specification

**Version:** 1.0  
**Date:** 2026-01-02  
**Owner:** Foreman (FM)  
**Phase:** Wave 1.0 Build-to-Green  
**Status:** READY_TO_EXECUTE  
**Authority:** FM Agent Contract v3.0.0, BUILD_PHILOSOPHY.md

---

## Executive Summary

Wave 1.0 QA-to-Red phase is **COMPLETE** (72.9%, 153/210 QA components).

**118 QA components remain RED** and require Build-to-Green implementation:
- **ui-builder:** 39 QA components (QA-019 to QA-057)
- **qa-builder:** 79 QA components (QA-132 to QA-210)

This document specifies the Build-to-Green phase requirements, sequencing, and gate criteria.

---

## Part 1: Build-to-Green Context

### 1.1 What is Build-to-Green?

**Build-to-Green** is the implementation phase where builders take **existing RED tests** and implement production code to make them **GREEN**.

**Key Principles:**
- Tests already exist (QA-to-Red phase complete)
- Architecture is frozen (V2.0, frozen 2025-12-31)
- Implementation must match test expectations exactly
- One-Time Build Correctness: GREEN achieved on first attempt
- Zero test debt: no skips, no TODOs, no placeholders

### 1.2 Wave 1.0 Build-to-Green Status

**QA-to-Red Complete:** 153/210 (72.9%)  
**Already GREEN:** 92/210 (43.8%)  
**Awaiting Build-to-Green:** 118/210 (56.2%)

**Builders Awaiting Build-to-Green:**

| Builder | QA Range | QA Count | Tests | Current State |
|---------|----------|----------|-------|---------------|
| ui-builder | QA-019 to QA-057 | 39 | 39 tests RED | Tests exist, implementation pending |
| qa-builder | QA-132 to QA-210 | 79 | 79 tests RED | Tests exist, implementation pending |

### 1.3 Why Two Builders Remain RED

**ui-builder** was executed as **QA-to-Red only** (Wave 1.0.3):
- 39 tests created
- All tests RED (correct QA-to-Red state)
- No implementation code written
- Purpose: Establish test blueprint before implementation

**qa-builder** was executed as **QA-to-Red only** (Wave 1.0.2):
- 79 tests created (43 test files covering 79 QA components)
- All tests RED (correct QA-to-Red state)
- No implementation code written
- Purpose: Establish test blueprint before implementation

---

## Part 2: Build-to-Green Scope

### 2.1 Wave 1.0.6 — ui-builder Build-to-Green

**QA Range:** QA-019 to QA-057 (39 QA components)  
**Builder:** ui-builder  
**Dependencies:** schema-builder ✅, api-builder ✅ (both complete)

**Subsystems:**
1. **CONV-05:** Conversation UI (QA-019 to QA-022) — 4 QA
2. **DASH-01:** Domain Status Manager UI (QA-023 to QA-027) — 5 QA
3. **DASH-02:** Drill-Down Navigator UI (QA-028 to QA-032) — 5 QA
4. **DASH-03:** Executive View Controller (QA-033 to QA-035) — 3 QA
5. **DASH-04:** Dashboard UI Renderer (QA-036 to QA-042) — 7 QA
6. **PARK-04:** Parking Station UI (QA-043 to QA-046) — 4 QA
7. **BUILD-04:** Build Visibility UI (QA-047 to QA-050) — 4 QA
8. **ESC-04:** Escalation UI (QA-051 to QA-057) — 7 QA

**Test Suite:**
- 39 tests exist in `tests/wave1_ui/`
- All tests currently RED
- Tests validate UI components, props, rendering, interactions

**Implementation Requirements:**
- Create `foreman/ui/` module structure
- Implement 8 UI component modules
- Make all 39 tests GREEN
- Zero test debt
- Architecture alignment (100% from frozen spec)

**Success Criteria:**
- All 39 tests GREEN (100% pass rate)
- Build-to-Green achieved on first attempt
- Zero test debt
- Evidence artifacts generated
- Gate PASS

---

### 2.2 Wave 1.0.7 — qa-builder Build-to-Green

**QA Range:** QA-132 to QA-210 (79 QA components)  
**Builder:** qa-builder  
**Dependencies:** schema-builder ✅, api-builder ✅, integration-builder ✅ (all complete)

**Subsystems:**
1. **Analytics Subsystem** (QA-132 to QA-146) — 15 QA
   - Token tracker, cost calculator, metrics collector

2. **Cross-Cutting Components** (QA-147 to QA-199) — 53 QA
   - **MEM-01:** Memory Fabric (QA-147 to QA-152) — 6 QA
   - **AUTH-01:** Authority Engine (QA-153 to QA-160) — 8 QA
   - **AUDIT-01:** Audit Trail System (QA-161 to QA-166) — 6 QA
   - **EVID-01:** Evidence Manager (QA-167 to QA-173) — 7 QA
   - **NOTIF-01:** Notification Router (QA-174 to QA-179) — 6 QA
   - **WATCH-01:** Watchdog System (QA-180 to QA-185) — 6 QA
   - **Remaining Cross-Cutting:** QA-186 to QA-199 — 14 QA

3. **Core User Flows** (QA-200 to QA-210) — 11 QA
   - Intent-to-Execution flow (foundational steps)
   - Build lifecycle flow
   - Escalation flow

**Test Suite:**
- 79 tests exist in `tests/wave1_0_qa_infrastructure/` (43 test files)
- All tests currently RED
- Tests validate analytics, cross-cutting components, core flows

**Implementation Requirements:**
- Create `foreman/analytics/`, `foreman/cross_cutting/`, `foreman/flows/` modules
- Implement all subsystem components
- Make all 79 tests GREEN
- Zero test debt
- Architecture alignment (100% from frozen spec)

**Success Criteria:**
- All 79 tests GREEN (100% pass rate)
- Build-to-Green achieved on first attempt
- Zero test debt
- Evidence artifacts generated
- Gate PASS

---

## Part 3: Execution Sequencing

### 3.1 Concurrent Execution (RECOMMENDED)

**ui-builder** and **qa-builder** Build-to-Green **CAN** proceed concurrently:
- ✅ No dependencies between them
- ✅ Both have all prerequisites satisfied
- ✅ No shared implementation targets
- ✅ Parallel execution safe

**Sequencing:**
```
Wave 1.0.6 (ui-builder) ━━━━━━━━━━━━━━┓
                                       ┣━━ Wave 1.0 COMPLETE
Wave 1.0.7 (qa-builder) ━━━━━━━━━━━━━┛
```

### 3.2 Sequential Execution (ALTERNATIVE)

If concurrent execution is not desired, either order is valid:

**Option A:**
1. Wave 1.0.6 (ui-builder) → 39 QA GREEN
2. Wave 1.0.7 (qa-builder) → 79 QA GREEN

**Option B:**
1. Wave 1.0.7 (qa-builder) → 79 QA GREEN
2. Wave 1.0.6 (ui-builder) → 39 QA GREEN

**FM Recommendation:** Concurrent execution for fastest completion.

---

## Part 4: Builder Instructions

### 4.1 Common Requirements (Both Builders)

**Input:**
- Frozen architecture (FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md)
- QA catalog (QA_CATALOG.md)
- Existing RED test suite
- QA-to-Red evidence artifacts

**Constraints:**
- ❌ No architecture changes
- ❌ No test modifications (unless correcting obvious test bugs)
- ❌ No governance modifications
- ❌ No changes to frozen specs
- ✅ Implement exactly as specified in frozen architecture

**Output:**
- Production code implementing all assigned QA components
- All tests GREEN (100% pass rate)
- Zero test debt
- Builder QA Report
- Completion summary
- Evidence artifacts

**Gate Requirements:**
- All assigned tests GREEN
- Zero test debt
- Architecture alignment verified
- Governance compliance confirmed
- Evidence artifacts complete

### 4.2 ui-builder Build-to-Green Instructions

**Task:** Implement UI components to make 39 RED tests GREEN

**Architecture Reference:**
- FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md
- Section: Conversational Interface, Dashboard, Parking Station, Build Visibility, Escalation UI components

**Test Suite Location:** `tests/wave1_ui/`

**Implementation Target:** `foreman/ui/` (create module structure)

**Test Execution:**
```bash
pytest tests/wave1_ui/ -v
```

**Expected Outcome:** 39/39 tests GREEN, zero failures

**Components to Implement:**
1. Conversation UI components (CONV-05)
2. Dashboard UI components (DASH-01, DASH-02, DASH-03, DASH-04)
3. Parking Station UI (PARK-04)
4. Build Visibility UI (BUILD-04)
5. Escalation UI (ESC-04)

**Deliverables:**
- `foreman/ui/conversation.py` (or equivalent React/Vue components)
- `foreman/ui/dashboard.py`
- `foreman/ui/parking.py`
- `foreman/ui/build_visibility.py`
- `foreman/ui/escalation.py`
- All tests GREEN
- Builder QA Report
- Completion summary

### 4.3 qa-builder Build-to-Green Instructions

**Task:** Implement analytics, cross-cutting components, and core flows to make 79 RED tests GREEN

**Architecture Reference:**
- FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md
- Sections: Analytics, Memory Fabric, Authority Engine, Audit Trail, Evidence Manager, Notification Router, Watchdog, Core Flows

**Test Suite Location:** `tests/wave1_0_qa_infrastructure/`

**Implementation Target:** `foreman/analytics/`, `foreman/cross_cutting/`, `foreman/flows/` (create module structures)

**Test Execution:**
```bash
pytest tests/wave1_0_qa_infrastructure/ -v
```

**Expected Outcome:** 79/79 tests GREEN (via 43 test files), zero failures

**Components to Implement:**
1. Analytics subsystem (token tracker, cost calculator, metrics collector)
2. Memory Fabric (MEM-01)
3. Authority Engine (AUTH-01)
4. Audit Trail System (AUDIT-01)
5. Evidence Manager (EVID-01)
6. Notification Router (NOTIF-01)
7. Watchdog System (WATCH-01)
8. Remaining cross-cutting components
9. Core user flows (Intent-to-Execution, Build lifecycle, Escalation)

**Deliverables:**
- `foreman/analytics/` module with all analytics components
- `foreman/cross_cutting/` module with all cross-cutting components
- `foreman/flows/` module with all core flows
- All tests GREEN
- Builder QA Report
- Completion summary

---

## Part 5: Gate Criteria

### 5.1 Wave 1.0.6 Gate (ui-builder)

**Gate ID:** GATE-UI-BUILDER-BUILD-TO-GREEN-WAVE-1.0

**Requirements:**
- ✅ All 39 tests GREEN (100% pass rate)
- ✅ Zero test debt (no skips, no TODOs, no incomplete tests)
- ✅ Architecture alignment verified (100% from frozen spec)
- ✅ Build-to-Green achieved on first attempt
- ✅ Evidence artifacts complete
- ✅ Builder QA Report submitted

**Gate Pass Condition:** ALL requirements satisfied  
**Gate Fail Condition:** ANY requirement not satisfied

### 5.2 Wave 1.0.7 Gate (qa-builder)

**Gate ID:** GATE-QA-BUILDER-BUILD-TO-GREEN-WAVE-1.0

**Requirements:**
- ✅ All 79 tests GREEN (100% pass rate)
- ✅ Zero test debt (no skips, no TODOs, no incomplete tests)
- ✅ Architecture alignment verified (100% from frozen spec)
- ✅ Build-to-Green achieved on first attempt
- ✅ Evidence artifacts complete
- ✅ Builder QA Report submitted

**Gate Pass Condition:** ALL requirements satisfied  
**Gate Fail Condition:** ANY requirement not satisfied

### 5.3 Wave 1.0 Completion Gate

**Gate ID:** GATE-WAVE-1.0-COMPLETE

**Requirements:**
- ✅ All 5 builder gates PASS
- ✅ All 210 QA components GREEN (100%)
- ✅ Zero test debt across entire Wave 1.0
- ✅ All builders executed successfully
- ✅ All evidence artifacts complete

**Current Status:**
- schema-builder: GATE PASS ✅
- api-builder: GATE PASS ✅
- integration-builder: GATE PASS ✅
- ui-builder (QA-to-Red): GATE PASS ✅
- qa-builder (QA-to-Red): GATE PASS ✅
- ui-builder (Build-to-Green): ⏳ PENDING
- qa-builder (Build-to-Green): ⏳ PENDING
- Overall: 92/210 QA GREEN (43.8%)

**Gate Will PASS When:**
- ui-builder Build-to-Green COMPLETE (39 QA GREEN)
- qa-builder Build-to-Green COMPLETE (79 QA GREEN)
- Total: 210/210 QA GREEN (100%)

---

## Part 6: FM Orchestration

### 6.1 FM Responsibilities

**Before Execution:**
- ✅ Create Build-to-Green specification (this document)
- ✅ Create Wave 1.0.6 issue (ui-builder Build-to-Green)
- ✅ Create Wave 1.0.7 issue (qa-builder Build-to-Green)
- ✅ Provide frozen architecture reference
- ✅ Confirm test suites ready
- ✅ Confirm dependencies satisfied

**During Execution:**
- Monitor builder progress
- Respond to escalations
- Provide clarifications if needed

**After Execution:**
- Review builder submissions
- Validate gate requirements
- Approve or reject merges
- Update progress dashboard
- Declare Wave 1.0 completion when all gates PASS

### 6.2 CS2 Responsibilities

**Execution:**
- Execute Wave 1.0.6 (ui-builder Build-to-Green) via Issue #TBD
- Execute Wave 1.0.7 (qa-builder Build-to-Green) via Issue #TBD
- Merge approved PRs

**Coordination:**
- Confirm concurrent or sequential execution preference
- Coordinate builder execution timing

---

## Part 7: Success Criteria

### 7.1 Wave 1.0.6 Success Criteria

- ✅ All 39 tests GREEN
- ✅ Build-to-Green achieved on first attempt
- ✅ Zero test debt
- ✅ Gate PASS
- ✅ FM merge approval

### 7.2 Wave 1.0.7 Success Criteria

- ✅ All 79 tests GREEN
- ✅ Build-to-Green achieved on first attempt
- ✅ Zero test debt
- ✅ Gate PASS
- ✅ FM merge approval

### 7.3 Wave 1.0 Completion Success Criteria

- ✅ All 210 QA components GREEN (100%)
- ✅ All 5 builder gates PASS
- ✅ Zero test debt across entire Wave 1.0
- ✅ All evidence artifacts complete
- ✅ FM declares Wave 1.0 COMPLETE

---

## Part 8: Next Steps

**FM Actions:**
1. ✅ Create this Build-to-Green specification
2. ⏳ Create Issue for Wave 1.0.6 (ui-builder Build-to-Green)
3. ⏳ Create Issue for Wave 1.0.7 (qa-builder Build-to-Green)

**CS2 Actions:**
1. ⏳ Execute Wave 1.0.6 (ui-builder Build-to-Green)
2. ⏳ Execute Wave 1.0.7 (qa-builder Build-to-Green)
3. ⏳ Merge approved PRs
4. ⏳ Confirm Wave 1.0 completion

---

**Specification Maintained By:** Maturion Foreman (FM)  
**Authority:** FM Agent Contract v3.0.0  
**Date:** 2026-01-02 15:54 UTC

---

**END OF WAVE 1.0 BUILD-TO-GREEN SPECIFICATION**
