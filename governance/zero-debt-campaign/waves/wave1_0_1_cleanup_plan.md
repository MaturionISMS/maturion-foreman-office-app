# Wave 1.0.1 Cleanup Plan

**Campaign**: ZWZDI-2026-001  
**Wave**: 1.0.1  
**Builder**: Schema Builder  
**Status**: BLOCKED (awaiting Wave 1.0 completion)  
**Created**: 2026-01-08

---

## Wave Overview

### Original Wave 1.0.1 Work

**Implemented**: Database schema foundation and models  
**Deliverables**:
- Database schema design
- SQLAlchemy models
- Model relationships
- Schema migrations (if applicable)

**Test Infrastructure**:
- Schema validation tests
- Model tests
- Migration tests
- Database integration tests

---

## Cleanup Scope

### Test Directories

Primary scope:
- `tests/wave1_schema_foundation/`

Related scope (Wave 1.0.1 specific tests):
- Schema-related tests in `tests/wave1_0_qa_infrastructure/`

---

## Current State (Baseline)

**Status**: PENDING INVENTORY

### Metrics (To Be Determined)
- **Warnings**: TBD
- **Failing Tests**: TBD
- **Passing Tests**: TBD
- **Test Pass Rate**: TBD

### Known Issues
*(To be populated during warning inventory)*

---

## Target State

**Warnings**: 0 (ZERO)  
**Failing Tests**: 0 (ZERO)  
**Test Pass Rate**: 100%

---

## Cleanup Strategy

### Phase 1: Inventory (30 minutes)

Run tests:
```bash
pytest tests/wave1_schema_foundation/ -v -W default
```

Document warnings by category and failures by type.

---

### Phase 2: Eliminate Warnings (1-1.5 days)

Common schema/database warning patterns:
- SQLAlchemy deprecation warnings
- Type annotation warnings in models
- Import warnings
- Database connection warnings
- ORM relationship warnings

**Strategy**:
1. Fix SQLAlchemy API deprecations
2. Add proper type hints to models
3. Clean up imports
4. Fix database connection patterns
5. Update ORM relationships if needed

---

### Phase 3: Resolve Test Debt (0.5 day)

For each failing test:
1. Investigate database setup/teardown issues
2. Fix model validation logic
3. Resolve schema migration issues
4. Verify test fixtures properly configured

---

### Phase 4: Verification (2 hours)

Run full Wave 1.0.1 scope and verify:
- Zero warnings
- Zero failures
- 100% pass rate
- Collect evidence

---

## Estimated Effort

**Total**: 2 days

| Phase | Estimated Time |
|-------|----------------|
| Inventory | 0.5 hours |
| Eliminate Warnings | 1-1.5 days |
| Resolve Test Debt | 0.5 day |
| Verification & Evidence | 3 hours |

---

## Success Criteria

- ✅ Zero warnings in all Wave 1.0.1 scope tests
- ✅ Zero failing tests in Wave 1.0.1 scope
- ✅ 100% test pass rate
- ✅ All fixes documented
- ✅ Completion evidence provided
- ✅ FM verification PASS

---

## Dependencies

**Depends On**: Wave 1.0 cleanup COMPLETE  
**Blocks**: Wave 1.0.2 cleanup

**Can Start**: After Wave 1.0 FM verification PASS

---

## Completion Evidence Requirements

Create in `evidence/zwzdi/wave1_0_1/`:

1. **COMPLETION_SUMMARY.md**
2. **test_output.txt**
3. **fixes_detailed.md** (if needed)

---

## Common Schema Warning Patterns

### Expected Warning Types

1. **SQLAlchemy deprecation warnings**
2. **Model type annotation warnings**
3. **Database connection warnings**
4. **ORM relationship warnings**
5. **Migration warnings**

### Common Fixes

- Update to SQLAlchemy 2.0 patterns
- Add proper type hints to model fields
- Fix deprecated query patterns
- Update relationship configurations

---

## Risk Assessment

### Low Risk
- Import warnings
- Simple type warnings

### Medium Risk
- SQLAlchemy API migrations
- ORM relationship updates

### High Risk
- Database connection patterns (may affect multiple tests)
- Schema migration issues (may affect data integrity)

**Mitigation**: Test each fix thoroughly against database.

---

## Builder Checklist

Before starting:
- [ ] Read GOVERNANCE_LEARNING_BRIEF.md
- [ ] Reviewed this cleanup plan
- [ ] Acknowledged accountability
- [ ] Wave 1.0 verified COMPLETE

During execution:
- [ ] Inventory complete
- [ ] Warnings categorized
- [ ] All warnings eliminated
- [ ] All test debt resolved
- [ ] Verification passed locally
- [ ] Evidence collected

Before submission:
- [ ] Zero warnings confirmed
- [ ] Zero failures confirmed
- [ ] 100% pass rate confirmed
- [ ] Evidence files created
- [ ] FM verification requested

---

**Plan Status**: READY (blocked by Wave 1.0)  
**Awaiting**: Wave 1.0 completion  
**Owner**: Schema Builder (to be assigned)  
**Created By**: Foreman (FM)
