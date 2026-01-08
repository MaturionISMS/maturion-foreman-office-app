# Wave 1.0 Warning Inventory

**Date**: 2026-01-08  
**Wave**: 1.0 (UI Builder)  
**Total Warnings**: 14

---

## Warning Category Breakdown

### PytestUnknownMarkWarning: 14 warnings

**Description**: Unknown pytest marks used without registration in pytest.ini

**Severity**: Low (configuration issue, not code defect)

**Impact**: None on functionality, only produces warning noise

---

## Detailed Warning List

### Group 1: @pytest.mark.ui (9 warnings)

**File**: `tests/test_commissioning_wizard_spec.py`

1. Line 32: `@pytest.mark.ui` on TestCommissioningWizardSpec
2. Line 69: `@pytest.mark.ui` on TestUXPrinciples
3. Line 137: `@pytest.mark.ui` on TestStepDefinitions
4. Line 207: `@pytest.mark.ui` on TestUIComponents
5. Line 251: `@pytest.mark.ui` on TestNavigationRules
6. Line 289: `@pytest.mark.ui` on TestBatch2Constraints
7. Line 349: `@pytest.mark.ui` on TestIntegrationPoints
8. Line 381: `@pytest.mark.ui` on TestAccessibility
9. Line 413: `@pytest.mark.ui` on TestAcceptanceCriteria

**Warning Message**:
```
PytestUnknownMarkWarning: Unknown pytest.mark.ui - is this a typo?  
You can register custom marks to avoid this warning - 
for details, see https://docs.pytest.org/en/stable/how-to/mark.html
```

---

### Group 2: @pytest.mark.commissioning (5 warnings)

**File**: `tests/test_commissioning_controller.py`

1. Line 29: `@pytest.mark.commissioning` on TestCommissioningControllerStructure
2. Line 90: `@pytest.mark.commissioning` on TestCommissioningControllerImplementation
3. Line 207: `@pytest.mark.commissioning` on TestCommissioningControllerDocumentation
4. Line 263: `@pytest.mark.commissioning` on TestCommissioningControllerCompliance
5. Line 355: `@pytest.mark.commissioning` on TestCommissioningControllerIntegration

**Warning Message**:
```
PytestUnknownMarkWarning: Unknown pytest.mark.commissioning - is this a typo?  
You can register custom marks to avoid this warning - 
for details, see https://docs.pytest.org/en/stable/how-to/mark.html
```

---

## Root Cause Analysis

**Why did these warnings occur?**

The test files used custom pytest markers (`@pytest.mark.ui` and `@pytest.mark.commissioning`) for test categorization and selective execution. However, these markers were never registered in the pytest configuration file (`pytest.ini`).

When pytest's `--strict-markers` flag is enabled (which it is in this project's pytest.ini), any unregistered marker produces a warning.

**Why is marker registration important?**

1. **Prevents typos**: Catches accidental misspellings of marker names
2. **Documents intent**: Makes markers discoverable and self-documenting
3. **Enables filtering**: Allows selective test execution (e.g., `pytest -m ui`)
4. **Governance compliance**: Enforces configuration discipline

---

## Fix Summary

**Solution**: Register both markers in pytest.ini

**Change**:
```ini
# Added to markers section in pytest.ini:
ui: UI component and interface tests
commissioning: Commissioning wizard and controller tests
```

**Result**: All 14 warnings eliminated

---

**Status**: ✅ **RESOLVED** — Zero warnings remaining
