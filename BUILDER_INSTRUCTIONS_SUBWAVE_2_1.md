# Builder Instructions — Subwave 2.1: Enhanced Dashboard

**Builder:** ui-builder  
**Issue:** #388 (Subwave 2.1: Enhanced Dashboard — ui-builder Build-to-Green)  
**Status:** READY TO PROCEED (test suite now available)  
**Date:** 2026-01-05

---

## ⚠️ CRITICAL UPDATE: Test Suite Now Available

The test suite for Subwave 2.1 (QA-361 to QA-375) has been generated and is now available in the repository.

**Previous Issue:** Test suite was missing when sub-issue was initially created.  
**Resolution:** Test suite generated as part of escalation corrective action.  
**Status:** Test suite now baselined to repository and ready for use.

---

## Quick Start Instructions (Copy-Paste Ready)

**STEP 1: Pull Latest Changes**

```bash
git pull origin main
```

**STEP 2: Verify Test Suite Exists**

```bash
ls -la tests/wave2_0_qa_infrastructure/test_dashboard_enhanced_*.py
```

**Expected Output:**
```
tests/wave2_0_qa_infrastructure/test_dashboard_enhanced_drilldown.py
tests/wave2_0_qa_infrastructure/test_dashboard_enhanced_filtering.py
tests/wave2_0_qa_infrastructure/test_dashboard_enhanced_realtime.py
```

**STEP 3: Verify Tests Are RED** (if pytest installed)

```bash
pytest tests/wave2_0_qa_infrastructure/test_dashboard_enhanced_*.py -v
```

**Expected Result:** All 15 tests should FAIL (RED state) with clear messages indicating features not yet implemented.

**STEP 4: Review Test Suite**

Read through all 15 tests to understand:
- What Enhanced Dashboard features need to be implemented
- Expected behavior for each feature
- Integration points with existing Wave 1 Dashboard
- Test fixtures and test context

**Test Files:**
- `test_dashboard_enhanced_drilldown.py` — QA-361 to QA-365 (Drill-Down Navigation)
- `test_dashboard_enhanced_filtering.py` — QA-366 to QA-370 (Advanced Filtering)
- `test_dashboard_enhanced_realtime.py` — QA-371 to QA-375 (Real-Time Updates)

**STEP 5: Create New Branch for Implementation**

```bash
git checkout -b ui-builder/subwave-2.1-enhanced-dashboard
```

**STEP 6: Implement Enhanced Dashboard Features**

Follow the original sub-issue instructions (`wave2_builder_issues/SUBWAVE_2.1_UI_BUILDER_ENHANCED_DASHBOARD.md`) with ONE CRITICAL CHANGE:

✅ **Test suite is NOW AVAILABLE** at `tests/wave2_0_qa_infrastructure/`

All other instructions remain the same:
- Implement drill-down navigation (QA-361 to QA-365)
- Implement advanced filtering (QA-366 to QA-370)
- Implement real-time updates (QA-371 to QA-375)
- Follow frozen architecture (when available)
- Achieve build-to-green on first attempt
- Report checkpoint at 50% (7-8 QA complete)
- Perform mandatory code checking
- Terminal states only (BLOCKED or COMPLETE)

**STEP 7: Run Tests to Verify GREEN**

```bash
pytest tests/wave2_0_qa_infrastructure/test_dashboard_enhanced_*.py -v
```

**Target:** 15/15 tests GREEN, zero failures

**STEP 8: Generate Evidence & Submit**

Create completion report and evidence artifacts per sub-issue instructions.

---

## Test Suite Details

### Location

```
tests/wave2_0_qa_infrastructure/
├── __init__.py                                    # Module init
├── conftest.py                                    # Pytest fixtures
├── test_dashboard_enhanced_drilldown.py           # QA-361 to QA-365
├── test_dashboard_enhanced_filtering.py           # QA-366 to QA-370
└── test_dashboard_enhanced_realtime.py            # QA-371 to QA-375
```

### Test Breakdown

**Drill-Down Navigation (QA-361 to QA-365):**
- QA-361: Drill-down UI component rendering
- QA-362: Drill-down state management
- QA-363: Drill-down navigation handlers
- QA-364: Breadcrumb navigation
- QA-365: Drill-down data flow

**Advanced Filtering (QA-366 to QA-370):**
- QA-366: Filter UI component rendering
- QA-367: Filter state management
- QA-368: Multi-criteria filtering
- QA-369: Filter persistence
- QA-370: Filter reset handling

**Real-Time Updates (QA-371 to QA-375):**
- QA-371: WebSocket connection setup
- QA-372: Real-time data update handlers
- QA-373: Dashboard auto-refresh logic
- QA-374: Update notification UI
- QA-375: Real-time data consistency

### Test Fixtures Available

**From `conftest.py`:**
- `ui_test_context` — Base UI test context with organisation_id for tenant isolation
- `dashboard_enhanced_context` — Dashboard-specific test context

### Current Test State

**All 15 tests are in RED state** using `pytest.fail()` with descriptive messages:
- Tests clearly indicate what needs to be implemented
- Tests reference Wave 2 architecture requirements
- Tests follow Wave 1 QA infrastructure patterns
- Tests use proper fixtures for context

---

## Important Reminders

### ⚠️ Prerequisites Still Pending

**IMPORTANT:** While the test suite is now available, the following Wave 2 prerequisites are STILL PENDING:

- ⏳ Wave 2 Architecture Freeze — NOT YET COMPLETE
- ⏳ Complete Wave 2 QA-to-Red Suite — PARTIALLY COMPLETE (15/190 tests)
- ⏳ Platform Readiness Verification — NOT YET CONFIRMED
- ⏳ CS2 Authorization — NOT YET GRANTED

**DO NOT START IMPLEMENTATION** until FM explicitly authorizes execution after all prerequisites are satisfied.

### Governance Reminders

1. **100% = 100%** — 14/15 = FAIL. Only 15/15 = PASS.
2. **Checkpoint Mandatory** — Report at 50% (7-8 QA complete).
3. **No Test Dodging** — Flaky tests are blockers, not acceptable debt.
4. **Terminal States Only** — Report BLOCKED or COMPLETE. No percentages.
5. **Code Checking Mandatory** — Self-review required with evidence.
6. **Scope Discipline** — Enhanced Dashboard ONLY (QA-361 to QA-375).

### If Issues Arise

**IF you encounter ANY of the following:**
- Test suite unclear or ambiguous
- Architecture reference missing
- Test expectations not understandable
- Any blocker or uncertainty

**THEN:**
- STOP immediately
- Report BLOCKED state to FM
- Describe specific issue clearly
- Wait for FM clarification
- DO NOT proceed with assumptions

---

## Summary

✅ **Test suite is NOW AVAILABLE** and ready for use  
✅ **All 15 tests exist and are in RED state**  
✅ **Tests follow Wave 1 patterns and quality standards**  
⏳ **Wave 2 prerequisites still pending** (architecture, full QA-to-Red, authorization)  
⚠️ **DO NOT START** until FM explicitly authorizes execution

**Next Step:** Wait for FM authorization after all Wave 2 prerequisites complete.

---

## Contact

- **Escalations:** Report BLOCKED state to FM
- **Clarifications:** Use BLOCKED state, don't assume
- **Questions:** Reference governance docs (BUILD_PHILOSOPHY.md, learnings)

---

**Created By:** Maturion Foreman (FM)  
**Date:** 2026-01-05  
**Status:** Builder Instructions Ready  
**Awaiting:** FM authorization after Wave 2 prerequisites complete

---

**END OF BUILDER INSTRUCTIONS**
