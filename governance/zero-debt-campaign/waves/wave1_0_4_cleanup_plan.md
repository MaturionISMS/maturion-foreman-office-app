# Wave 1.0.4 Cleanup Plan

**Campaign**: ZWZDI-2026-001  
**Wave**: 1.0.4  
**Builder**: API Builder  
**Status**: BLOCKED (awaiting Wave 1.0.3 completion)  
**Created**: 2026-01-08

---

## Wave Overview

### Original Wave 1.0.4 Work

**Implemented**: Additional API features and enhancements  
**Deliverables**:
- Extended API functionality
- Additional endpoints
- Enhanced API features
- API optimization and refinements

**Test Infrastructure**:
- Feature-specific API tests
- Enhanced endpoint tests
- Additional integration tests

---

## Cleanup Scope

### Test Directories

Primary scope:
- Additional tests in `tests/wave1_api_builder/` (Wave 1.0.4 specific)

Related scope (Wave 1.0.4 specific tests):
- Feature-specific tests in `tests/wave1_0_qa_infrastructure/`

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
pytest tests/wave1_api_builder/ -v -W default -k "wave_1_0_4"
```

Document warnings by category and failures by type specific to Wave 1.0.4.

---

### Phase 2: Eliminate Warnings (0.5 day)

Similar to Wave 1.0.3, common API warning patterns:
- Flask/API deprecation warnings
- Type warnings in new endpoints
- Import warnings
- JSON handling warnings
- Feature-specific warnings

**Strategy**:
1. Apply lessons from Wave 1.0.3
2. Fix API-specific warnings
3. Update type hints
4. Clean up imports
5. Fix feature-specific issues

---

### Phase 3: Resolve Test Debt (0.5 day)

For each failing test:
1. Investigate feature implementation
2. Fix endpoint logic
3. Resolve validation issues
4. Verify tests properly configured

---

### Phase 4: Verification (1 hour)

Run full Wave 1.0.4 scope and verify:
- Zero warnings
- Zero failures
- 100% pass rate
- Collect evidence

---

## Estimated Effort

**Total**: 1 day

| Phase | Estimated Time |
|-------|----------------|
| Inventory | 0.5 hours |
| Eliminate Warnings | 0.5 day |
| Resolve Test Debt | 0.5 day |
| Verification & Evidence | 2 hours |

**Note**: Should be faster than Wave 1.0.3 due to lessons learned and similar patterns.

---

## Success Criteria

- ✅ Zero warnings in all Wave 1.0.4 scope tests
- ✅ Zero failing tests in Wave 1.0.4 scope
- ✅ 100% test pass rate
- ✅ All fixes documented
- ✅ Completion evidence provided
- ✅ FM verification PASS

---

## Dependencies

**Depends On**: Wave 1.0.3 cleanup COMPLETE  
**Blocks**: Foundation cleanup

**Can Start**: After Wave 1.0.3 FM verification PASS

---

## Completion Evidence Requirements

Create in `evidence/zwzdi/wave1_0_4/`:

1. **COMPLETION_SUMMARY.md**
2. **test_output.txt**
3. **fixes_detailed.md** (if needed)

---

## Common API Warning Patterns

### Expected Warning Types

Same as Wave 1.0.3:
1. **Flask/API deprecation warnings**
2. **Type warnings in route handlers**
3. **Import warnings**
4. **JSON serialization warnings**
5. **Feature-specific warnings**

### Common Fixes

Apply patterns from Wave 1.0.3:
- Update API patterns consistently
- Add type hints to new endpoints
- Fix JSON handling for new features
- Clean up imports

---

## Synergy with Wave 1.0.3

**Leverage learning from Wave 1.0.3**:
- Same builder (API Builder)
- Similar warning patterns expected
- Can apply same fixes to similar issues
- Faster execution due to familiarity

**Reuse from Wave 1.0.3**:
- Fix patterns for Flask warnings
- Type hint strategies
- JSON serialization solutions
- Test fixture patterns

---

## Risk Assessment

### Low Risk
- Most patterns already addressed in Wave 1.0.3
- Same builder, same domain

### Medium Risk
- Feature-specific warnings (new to this wave)
- New endpoint logic

### High Risk
- Minimal (most risks mitigated in Wave 1.0.3)

**Mitigation**: Apply proven patterns from Wave 1.0.3.

---

## Builder Checklist

Before starting:
- [ ] Read GOVERNANCE_LEARNING_BRIEF.md (if not done for Wave 1.0.3)
- [ ] Reviewed this cleanup plan
- [ ] Reviewed Wave 1.0.3 fixes for reusable patterns
- [ ] Wave 1.0.3 verified COMPLETE

During execution:
- [ ] Inventory complete
- [ ] Warnings categorized
- [ ] Applied Wave 1.0.3 patterns where applicable
- [ ] All warnings eliminated
- [ ] All test debt resolved
- [ ] Verification passed locally
- [ ] Evidence collected

Before submission:
- [ ] Zero warnings confirmed
- [ ] Zero failures confirmed
- [ ] 100% pass rate confirmed
- [ ] New API features still functional
- [ ] Evidence files created
- [ ] FM verification requested

---

**Plan Status**: READY (blocked by Wave 1.0.3)  
**Awaiting**: Wave 1.0.3 completion  
**Owner**: API Builder (same as Wave 1.0.3)  
**Created By**: Foreman (FM)
