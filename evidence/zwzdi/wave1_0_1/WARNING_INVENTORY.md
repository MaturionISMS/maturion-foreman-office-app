# Wave 1.0.1 Warning Inventory

**Campaign**: ZWZDI-2026-001  
**Wave**: 1.0.1  
**Builder**: Schema Builder  
**Date**: 2026-01-08  
**Status**: COMPLETE

---

## Baseline State

**Test Directory**: `tests/wave1_schema_foundation/`  
**Test Count**: 36 tests  
**Passing Tests**: 36  
**Failing Tests**: 0  
**Total Warnings**: 9

---

## Warning Breakdown

### Category 1: SQLAlchemy Deprecation Warning (1 warning)

**Type**: MovedIn20Warning  
**Source**: `fm/data/models/base.py:15`  
**Message**: 
```
The declarative_base() function is now available as sqlalchemy.orm.declarative_base(). 
(deprecated since: 2.0)
```

**Root Cause**: Using deprecated import path `sqlalchemy.ext.declarative.declarative_base`

**Fix Applied**: 
- Updated import from `from sqlalchemy.ext.declarative import declarative_base` 
- To: `from sqlalchemy.orm import declarative_base`
- File: `fm/data/models/base.py` lines 8-11

**Verification**: Warning eliminated after fix

---

### Category 2: Pytest Unknown Mark Warnings (8 warnings)

**Type**: PytestUnknownMarkWarning  
**Sources**: All schema foundation test files  
**Messages**: 
```
Unknown pytest.mark.wave1 - is this a typo?
Unknown pytest.mark.schema - is this a typo?
```

**Affected Files**:
1. `tests/wave1_schema_foundation/test_qa001_qa005_conversation_manager.py:25` - `@pytest.mark.wave1`
2. `tests/wave1_schema_foundation/test_qa001_qa005_conversation_manager.py:26` - `@pytest.mark.schema`
3. `tests/wave1_schema_foundation/test_qa006_qa010_message_handler.py:28` - `@pytest.mark.wave1`
4. `tests/wave1_schema_foundation/test_qa006_qa010_message_handler.py:29` - `@pytest.mark.schema`
5. `tests/wave1_schema_foundation/test_qa011_qa013_fm_conversation_initiator.py:28` - `@pytest.mark.wave1`
6. `tests/wave1_schema_foundation/test_qa011_qa013_fm_conversation_initiator.py:29` - `@pytest.mark.schema`
7. `tests/wave1_schema_foundation/test_qa014_qa018_clarification_engine.py:24` - `@pytest.mark.wave1`
8. `tests/wave1_schema_foundation/test_qa014_qa018_clarification_engine.py:25` - `@pytest.mark.schema`

**Root Cause**: Custom pytest marks `wave1` and `schema` were not registered in `pytest.ini`

**Fix Applied**: 
- Added `wave1` and `schema` markers to `pytest.ini` markers section
- File: `pytest.ini` lines 22-49
- Added definitions:
  - `wave1: Wave 1.0 tests (all Wave 1 components)`
  - `schema: Schema and database model tests`

**Verification**: All 8 warnings eliminated after fix

---

## Test Debt Analysis

**Failing Tests**: 0  
**Skipped Tests**: 0  
**Incomplete Tests**: 0  

**Conclusion**: No test debt found in Wave 1.0.1 scope

---

## Summary

| Metric | Baseline | After Fixes | Target | Status |
|--------|----------|-------------|--------|--------|
| **Total Warnings** | 9 | 0 | 0 | ✅ ACHIEVED |
| **SQLAlchemy Warnings** | 1 | 0 | 0 | ✅ ACHIEVED |
| **Pytest Mark Warnings** | 8 | 0 | 0 | ✅ ACHIEVED |
| **Failing Tests** | 0 | 0 | 0 | ✅ ACHIEVED |
| **Test Pass Rate** | 100% | 100% | 100% | ✅ ACHIEVED |

---

## Files Modified

1. `fm/data/models/base.py` - Updated SQLAlchemy import to use non-deprecated API
2. `pytest.ini` - Registered `wave1` and `schema` custom marks

---

## Verification Command

```bash
pytest tests/wave1_schema_foundation/ -v -W default --tb=short
```

**Result**: 36 passed, 0 warnings in 0.42s

---

**Status**: ✅ ALL WARNINGS ELIMINATED  
**Completion Date**: 2026-01-08  
**Builder**: Schema Builder
