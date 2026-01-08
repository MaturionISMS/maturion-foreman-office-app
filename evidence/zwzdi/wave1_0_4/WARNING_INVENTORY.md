# Wave 1.0.4 (QA Builder) Warning Inventory

**Date**: 2026-01-08  
**Wave**: 1.0.4 (QA Builder)  
**Total Warnings**: 58 (PytestUnknownMarkWarning)

---

## Warning Category Breakdown

### PytestUnknownMarkWarning: 58 warnings

**Description**: Unknown pytest marks used without registration in pytest.ini

**Severity**: Medium (configuration issue, prevents proper test categorization)

**Impact**: Warning noise, test filtering disabled, marker typos undetected

---

## Detailed Warning List by Marker

### Group 1: @pytest.mark.memory (14 occurrences)

**Files**: `tests/test_global_memory_runtime.py`

**Warning Message**:
```
PytestUnknownMarkWarning: Unknown pytest.mark.memory - is this a typo?  
You can register custom marks to avoid this warning - 
for details, see https://docs.pytest.org/en/stable/how-to/mark.html
```

---

### Group 2: @pytest.mark.governance_sync (11 occurrences)

**Files**: `tests/test_governance_memory_sync.py`

**Warning Message**:
```
PytestUnknownMarkWarning: Unknown pytest.mark.governance_sync - is this a typo?  
You can register custom marks to avoid this warning - 
for details, see https://docs.pytest.org/en/stable/how-to/mark.html
```

---

### Group 3: @pytest.mark.lifecycle (9 occurrences)

**Files**: Various test files with lifecycle management tests

**Warning Message**:
```
PytestUnknownMarkWarning: Unknown pytest.mark.lifecycle - is this a typo?  
You can register custom marks to avoid this warning - 
for details, see https://docs.pytest.org/en/stable/how-to/mark.html
```

---

### Group 4: @pytest.mark.guard (8 occurrences)

**Files**: Guard and validation test files

**Warning Message**:
```
PytestUnknownMarkWarning: Unknown pytest.mark.guard - is this a typo?  
You can register custom marks to avoid this warning - 
for details, see https://docs.pytest.org/en/stable/how-to/mark.html
```

---

### Group 5: @pytest.mark.chp (7 occurrences)

**Files**: `tests/test_chp_memory_integration.py`

**Warning Message**:
```
PytestUnknownMarkWarning: Unknown pytest.mark.chp - is this a typo?  
You can register custom marks to avoid this warning - 
for details, see https://docs.pytest.org/en/stable/how-to/mark.html
```

---

### Group 6: @pytest.mark.startup (6 occurrences)

**Files**: Startup and initialization test files

**Warning Message**:
```
PytestUnknownMarkWarning: Unknown pytest.mark.startup - is this a typo?  
You can register custom marks to avoid this warning - 
for details, see https://docs.pytest.org/en/stable/how-to/mark.html
```

---

### Group 7: @pytest.mark.analytics (3 occurrences)

**Files**: `tests/wave1_0_qa_infrastructure/analytics/`

**Warning Message**:
```
PytestUnknownMarkWarning: Unknown pytest.mark.analytics - is this a typo?  
You can register custom marks to avoid this warning - 
for details, see https://docs.pytest.org/en/stable/how-to/mark.html
```

---

## Root Cause Analysis

**Why did these warnings occur?**

The test files used custom pytest markers for test categorization and selective execution. However, these markers were never registered in the pytest configuration file (`pytest.ini`).

When pytest's `--strict-markers` flag is enabled (which it is in this project's pytest.ini), any unregistered marker produces a warning.

**Why is marker registration important?**

1. **Prevents typos**: Catches accidental misspellings of marker names
2. **Documents intent**: Makes markers discoverable and self-documenting
3. **Enables filtering**: Allows selective test execution (e.g., `pytest -m memory`)
4. **Governance compliance**: Enforces configuration discipline

---

## Fix Summary

**Solution**: Register all 7 markers in pytest.ini

**Changes**:
```ini
# Added to markers section in pytest.ini:
memory: Memory and persistence tests
governance_sync: Governance synchronization tests
lifecycle: Lifecycle and state management tests
guard: Guard and validation tests
chp: CHP (Copilot Help Protocol) integration tests
startup: Startup and initialization tests
analytics: Analytics and reporting tests
```

**Result**: All 58 PytestUnknownMarkWarning eliminated

---

**Status**: ✅ **RESOLVED** — Zero marker warnings remaining
