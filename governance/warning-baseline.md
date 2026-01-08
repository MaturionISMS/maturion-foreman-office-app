# Warning Baseline

**Established**: 2026-01-08  
**Context**: Emergency remediation of test dodging incident (INCIDENT-2026-01-08-WARNING-SUPPRESSION)  
**Status**: ACTIVE DEBT (tracked in DEBT-004)

---

## Summary

After removing `--disable-warnings` from pytest.ini (which was suppressing quality signals), this baseline documents all warnings that appeared. These warnings represent **existing technical debt** that must be remediated.

---

## Warning Inventory

### Total Warnings: 64

**Category**: PytestUnknownMarkWarning (unknown pytest markers)

---

## Detailed Breakdown

### Unknown Pytest Markers

The following custom markers are used in tests but not registered in pytest.ini:

1. **chp** (7 occurrences)
   - Files: `tests/test_chp_memory_integration.py`
   - Context: CHP (Conversation History Persistence) memory integration tests

2. **commissioning** (5 occurrences)
   - Files: `tests/test_commissioning_controller.py`
   - Context: Commissioning controller tests

3. **governance_sync** (12 occurrences)
   - Files: `tests/test_governance_memory_sync.py`
   - Context: Governance memory synchronization tests

4. **guard** (unknown count)
   - Context: Guard/validation tests

5. **lifecycle** (9 occurrences)
   - Files: `tests/test_memory_lifecycle_runtime.py`
   - Context: Memory lifecycle runtime tests

6. **memory** (multiple occurrences)
   - Files: `tests/test_global_memory_runtime.py`, `tests/test_memory_proposals.py`
   - Context: Global memory runtime tests

7. **startup** (unknown count)
   - Context: Startup/initialization tests

8. **ui** (9 occurrences)
   - Files: `tests/test_commissioning_wizard_spec.py`
   - Context: UI component and wizard tests

---

## Root Cause

**These warnings exist because**:
- Custom pytest markers used in tests
- Markers not registered in pytest.ini `markers` section
- Tests written before marker registration process established

**Why this is problematic**:
- Pytest doesn't know these are intentional markers
- Could mask typos in marker names
- Reduces test categorization reliability
- Creates noise in test output

---

## Remediation Strategy

**Tracked in**: DEBT-004 (Warning Debt Remediation)

### Option 1: Register Markers (Recommended)

Add missing markers to `pytest.ini`:

```ini
markers =
    # ... existing markers ...
    chp: CHP memory integration tests
    commissioning: Commissioning controller tests
    governance_sync: Governance memory synchronization tests
    guard: Guard and validation tests
    lifecycle: Memory lifecycle runtime tests
    memory: Memory subsystem tests
    startup: Startup and initialization tests
    ui: UI component and wizard tests
```

### Option 2: Remove Unused Markers

If any markers are legacy/unused:
- Remove marker decorators from tests
- Use existing markers instead (e.g., `integration`, `wave2`, etc.)

### Option 3: Consolidate Markers

If markers overlap with existing ones:
- Map custom markers to standard markers
- Update tests to use standard markers
- Document mapping in test README

---

## Priority Assessment

**Severity**: LOW to MEDIUM  
**Impact**: Quality (noise in test output, potential typo masking)  
**Urgency**: DEFER (not blocking current work)

**Rationale**:
- Tests still run correctly
- No functional impact
- No security/compliance risk
- Primarily organizational/quality issue

**Recommendation**: Fix in dedicated debt remediation sprint, not inline with feature work.

---

## Acceptance Criteria for Resolution

- [ ] All markers either registered in pytest.ini OR removed from tests
- [ ] Test run produces zero `PytestUnknownMarkWarning` warnings
- [ ] Marker usage documented in test suite README
- [ ] Marker registration reflects actual usage patterns

---

## Historical Context

**Before**: `--disable-warnings` in pytest.ini suppressed these warnings  
**Incident**: INCIDENT-2026-01-08-WARNING-SUPPRESSION documented test dodging  
**Corrective Action**: Removed `--disable-warnings`, established this baseline  
**Future**: Systematic remediation via DEBT-004

---

## Related Documents

- `governance/incidents/INCIDENT-2026-01-08-WARNING-SUPPRESSION.md`
- `governance/incidents/DEBT_REGISTER.md` (DEBT-004 entry)
- `governance/policies/ZERO_WARNING_TEST_DEBT_IMMEDIATE_REMEDY_DOCTRINE.md`

---

**Baseline Owner**: Foreman (FM)  
**Review Date**: 2026-02-08  
**Status**: DOCUMENTED (remediation deferred to DEBT-004)
