# Wave 1.0 Cleanup Plan

**Campaign**: ZWZDI-2026-001  
**Wave**: 1.0  
**Builder**: UI Builder  
**Status**: PENDING (awaiting CS2 approval to begin)  
**Created**: 2026-01-08

---

## Wave Overview

### Original Wave 1.0 Work

**Implemented**: Initial UI components and dashboard infrastructure  
**Deliverables**:
- UI component library foundation
- Dashboard layout and structure
- Commissioning wizard
- Commissioning controller

**Test Infrastructure**:
- UI component tests
- Dashboard integration tests
- Commissioning flow tests

---

## Cleanup Scope

### Test Directories

Primary scope:
- `tests/wave1_ui/`
- `tests/test_commissioning_wizard_spec.py`
- `tests/test_commissioning_controller.py`

Related scope (Wave 1.0 specific tests):
- UI-related tests in `tests/wave1_0_qa_infrastructure/`

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

All tests in Wave 1.0 scope:
- Execute without warnings
- Pass completely (GREEN)
- Have proper assertions
- Test actual functionality

---

## Cleanup Strategy

### Phase 1: Inventory (30 minutes)

1. **Run tests in scope**:
   ```bash
   pytest tests/wave1_ui/ -v -W default
   pytest tests/test_commissioning_wizard_spec.py -v -W default
   pytest tests/test_commissioning_controller.py -v -W default
   ```

2. **Document**:
   - Total warnings by category
   - Total failures by type
   - Current pass rate
   - Specific files with issues

3. **Categorize warnings**:
   - Deprecation warnings
   - Import warnings
   - Type warnings
   - Test framework warnings
   - Runtime warnings

---

### Phase 2: Eliminate Warnings (1-1.5 days)

#### Strategy by Warning Type

**Deprecation Warnings**:
1. Identify deprecated API
2. Find replacement API in documentation
3. Update code to use new API
4. Test to verify functionality unchanged
5. Verify warning eliminated

**Import Warnings**:
1. Identify unused imports
2. Remove unused imports
3. Make wildcard imports explicit
4. Verify tests still pass

**Type Warnings**:
1. Add missing type hints
2. Fix type mismatches
3. Update type annotations
4. Run type checker to verify

**Test Framework Warnings**:
1. Update test fixtures if needed
2. Fix assertion patterns
3. Update pytest usage
4. Verify tests still meaningful

**Runtime Warnings**:
1. Fix resource leaks (unclosed files, etc.)
2. Address performance warnings
3. Fix security warnings immediately

#### Execution
- Fix ONE warning at a time
- Run tests after each fix to verify
- Document non-obvious fixes
- Commit incrementally (if possible)

---

### Phase 3: Resolve Test Debt (0.5 day)

For each failing test:

1. **Investigate failure**:
   - Read error message carefully
   - Identify root cause
   - Determine if implementation missing or test broken

2. **Take action**:
   - **If missing implementation**: IMPLEMENT the feature
   - **If broken test**: FIX the test
   - **If obsolete test**: REMOVE with documented rationale

3. **Verify GREEN**:
   - Test passes
   - Test actually tests something meaningful
   - No false positives

---

### Phase 4: Verification (2 hours)

1. **Run full Wave 1.0 scope**:
   ```bash
   pytest tests/wave1_ui/ tests/test_commissioning_wizard_spec.py tests/test_commissioning_controller.py -v -W default
   ```

2. **Verify**:
   - Zero warnings
   - Zero failures
   - 100% pass rate

3. **Collect evidence**:
   - Save test output
   - Create completion summary
   - Document fixes made

---

## Estimated Effort

**Total**: 2 days

| Phase | Estimated Time |
|-------|----------------|
| Inventory | 0.5 hours |
| Eliminate Warnings | 1-1.5 days |
| Resolve Test Debt | 0.5 day |
| Verification | 2 hours |
| Evidence Collection | 1 hour |

**Note**: Estimate may need adjustment based on actual warning count and complexity.

---

## Success Criteria

Wave 1.0 cleanup is COMPLETE when:

- ✅ Zero warnings in all Wave 1.0 scope tests
- ✅ Zero failing tests in Wave 1.0 scope
- ✅ 100% test pass rate
- ✅ All fixes documented
- ✅ Completion evidence provided
- ✅ FM verification PASS

---

## Dependencies

**Depends On**: None (Wave 1.0 is first wave)  
**Blocks**: Wave 1.0.1 cleanup

**Can Start**: After CS2 approves campaign plan

---

## Completion Evidence Requirements

Create in `evidence/zwzdi/wave1_0/`:

1. **COMPLETION_SUMMARY.md**:
   - Baseline metrics (before)
   - Final metrics (after)
   - List of warnings eliminated
   - List of tests fixed
   - List of tests removed (if any)
   - Time spent
   - Lessons learned

2. **test_output.txt**:
   - Full pytest output showing 0 warnings, 0 failures
   - Run date and time
   - Python and pytest versions

3. **fixes_detailed.md** (if needed):
   - Detailed explanations for complex fixes
   - Root causes identified
   - Solutions implemented
   - Rationale for removed tests (if any)

---

## Common UI Warning Patterns

*(To be populated during execution and used as reference for future waves)*

### Expected Warning Types

1. **React-related warnings** (if applicable)
2. **Component lifecycle warnings**
3. **Prop validation warnings**
4. **Test fixture warnings**
5. **Async/await warnings in tests**

### Common Fixes

- Update deprecated component APIs
- Fix async test patterns
- Properly cleanup test fixtures
- Add missing prop types

---

## Risk Assessment

### Low Risk
- Import warnings: Easy to fix, low complexity
- Simple type warnings: Straightforward fixes

### Medium Risk
- Deprecation warnings: Require API migration, testing needed
- Test framework warnings: May require test refactoring

### High Risk
- Runtime warnings: May indicate actual bugs requiring investigation
- Security warnings: Must be fixed immediately and carefully

**Mitigation**: For high-risk items, investigate thoroughly before fixing. Escalate to FM if uncertain.

---

## Support and Escalation

**Questions**: Comment on cleanup issue or escalate to FM  
**Blockers**: Escalate immediately to FM  
**Systemic Issues**: If you find 3+ similar warnings, escalate to FM (may indicate systemic problem)

**Do NOT proceed if blocked.**

---

## Builder Checklist

Before starting:
- [ ] Read GOVERNANCE_LEARNING_BRIEF.md
- [ ] Reviewed this cleanup plan
- [ ] Acknowledged accountability
- [ ] Have necessary tools and access

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
- [ ] Completion summary written
- [ ] FM verification requested

---

## Next Steps

1. **Wait for CS2 approval** of campaign plan
2. **FM creates cleanup issue** and assigns UI Builder
3. **UI Builder reads** GOVERNANCE_LEARNING_BRIEF.md
4. **UI Builder executes** this cleanup plan
5. **UI Builder provides** completion evidence
6. **FM verifies** cleanup (PASS/FAIL)
7. **If PASS**: Wave 1.0.1 authorized
8. **If FAIL**: Continue cleanup until PASS

---

**Plan Status**: READY  
**Awaiting**: CS2 campaign approval  
**Owner**: UI Builder (to be assigned)  
**Created By**: Foreman (FM)
