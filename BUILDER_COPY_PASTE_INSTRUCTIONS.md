# Builder Instructions — Ready to Copy & Paste

**TO:** Builder (ui-builder)  
**FROM:** Maturion Foreman (FM)  
**RE:** Subwave 2.1: Enhanced Dashboard — Corrected Instructions  
**DATE:** 2026-01-05

---

## 📋 Copy-Paste Instructions for Builder

Dear Builder,

The test suite for Subwave 2.1 is now available. Below are the corrected instructions you can copy and paste.

**⚠️ IMPORTANT:** Do NOT start execution yet. Wave 2 prerequisites are still pending (architecture freeze, complete QA-to-Red suite, platform readiness, CS2 authorization). Wait for FM's explicit authorization before proceeding.

---

## STEP 1: Pull Latest Changes

```bash
git pull origin main
```

---

## STEP 2: Verify Test Suite Exists

```bash
ls -la tests/wave2_0_qa_infrastructure/test_dashboard_enhanced_*.py
```

**You should see:**
```
test_dashboard_enhanced_drilldown.py
test_dashboard_enhanced_filtering.py
test_dashboard_enhanced_realtime.py
```

---

## STEP 3: Review Test Suite

```bash
# Read drill-down tests (QA-361 to QA-365)
cat tests/wave2_0_qa_infrastructure/test_dashboard_enhanced_drilldown.py

# Read filtering tests (QA-366 to QA-370)
cat tests/wave2_0_qa_infrastructure/test_dashboard_enhanced_filtering.py

# Read real-time tests (QA-371 to QA-375)
cat tests/wave2_0_qa_infrastructure/test_dashboard_enhanced_realtime.py
```

**Understand:**
- What features need to be implemented
- Expected behavior for each feature
- Test fixtures and context
- Integration points with Wave 1 Dashboard

---

## STEP 4: Wait for FM Authorization

**⚠️ DO NOT PROCEED PAST THIS STEP UNTIL FM EXPLICITLY AUTHORIZES**

FM will authorize Subwave 2.1 execution only after:
- ✅ Wave 2 Architecture is frozen
- ✅ Complete Wave 2 QA-to-Red suite is generated (190 tests)
- ✅ Platform readiness is GREEN
- ✅ CS2 (Johan) grants authorization

**Current Status:** ⏸️ BLOCKED — Prerequisites pending

---

## STEP 5: When Authorized — Create Branch

**Only execute after FM authorization:**

```bash
git checkout -b ui-builder/subwave-2.1-enhanced-dashboard
```

---

## STEP 6: When Authorized — Implement Features

**Only execute after FM authorization:**

Implement Enhanced Dashboard features per `wave2_builder_issues/SUBWAVE_2.1_UI_BUILDER_ENHANCED_DASHBOARD.md` with the correction that test suite is now available at:

```
tests/wave2_0_qa_infrastructure/test_dashboard_enhanced_*.py
```

**Implement:**
1. Drill-down navigation (QA-361 to QA-365)
2. Advanced filtering (QA-366 to QA-370)
3. Real-time updates (QA-371 to QA-375)

**Follow:**
- Frozen Wave 2 architecture (when available)
- BUILD_PHILOSOPHY.md (One-Time Build Correctness)
- Terminal state discipline (BLOCKED or COMPLETE only)
- Checkpoint reporting at 50% (7-8 QA)
- Mandatory code checking

---

## STEP 7: When Authorized — Run Tests

**Only execute after FM authorization and implementation:**

```bash
pytest tests/wave2_0_qa_infrastructure/test_dashboard_enhanced_*.py -v
```

**Target:** 15/15 tests GREEN, zero failures

---

## STEP 8: When Authorized — Submit

**Only execute after FM authorization and 15/15 GREEN:**

Generate evidence and completion report per sub-issue instructions.

Report COMPLETE state to FM.

---

## Test Suite Details

**Location:**
```
tests/wave2_0_qa_infrastructure/
├── __init__.py
├── conftest.py
├── test_dashboard_enhanced_drilldown.py    (QA-361 to QA-365)
├── test_dashboard_enhanced_filtering.py    (QA-366 to QA-370)
└── test_dashboard_enhanced_realtime.py     (QA-371 to QA-375)
```

**Test Breakdown:**

**Drill-Down Navigation (5 tests):**
- QA-361: Drill-down UI component rendering
- QA-362: Drill-down state management
- QA-363: Drill-down navigation handlers
- QA-364: Breadcrumb navigation
- QA-365: Drill-down data flow

**Advanced Filtering (5 tests):**
- QA-366: Filter UI component rendering
- QA-367: Filter state management
- QA-368: Multi-criteria filtering
- QA-369: Filter persistence
- QA-370: Filter reset handling

**Real-Time Updates (5 tests):**
- QA-371: WebSocket connection setup
- QA-372: Real-time data update handlers
- QA-373: Dashboard auto-refresh logic
- QA-374: Update notification UI
- QA-375: Real-time data consistency

**Current State:** All 15 tests are RED (proper QA-to-Red state)

---

## Fixtures Available

From `tests/wave2_0_qa_infrastructure/conftest.py`:

- `ui_test_context` — Base UI test context with `organisation_id` for tenant isolation
- `dashboard_enhanced_context` — Dashboard-specific test context

---

## Governance Reminders

1. **100% = 100%** — 14/15 = FAIL. Only 15/15 = PASS.
2. **Checkpoint Mandatory** — Report at 50% (7-8 QA complete).
3. **No Test Dodging** — Flaky tests are blockers.
4. **Terminal States Only** — BLOCKED or COMPLETE. No percentages.
5. **Code Checking Mandatory** — Self-review with evidence.
6. **Scope Discipline** — Enhanced Dashboard ONLY (QA-361 to QA-375).

---

## If Issues Arise

**IF you encounter:**
- Test suite unclear
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

✅ **Test suite is NOW AVAILABLE** and ready  
✅ **All 15 tests exist and are RED**  
✅ **Tests follow quality standards**  
⏸️ **Execution BLOCKED** until FM authorization  
⚠️ **DO NOT START** until FM explicitly authorizes

---

## Contact

- **Escalations:** Report BLOCKED state to FM
- **Clarifications:** Use BLOCKED state, don't assume

---

**From:** Maturion Foreman (FM)  
**Date:** 2026-01-05  
**Status:** Instructions Ready, Awaiting FM Authorization

---

**END OF BUILDER COPY-PASTE INSTRUCTIONS**
