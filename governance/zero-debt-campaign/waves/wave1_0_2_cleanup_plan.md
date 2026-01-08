# Wave 1.0.2 Cleanup Plan

**Campaign**: ZWZDI-2026-001  
**Wave**: 1.0.2  
**Builder**: Integration Builder  
**Status**: BLOCKED (awaiting Wave 1.0.1 completion)  
**Created**: 2026-01-08

---

## Wave Overview

### Original Wave 1.0.2 Work

**Implemented**: Integration subsystem and escalation management  
**Deliverables**:
- Integration layer architecture
- Escalation subsystem
- Event handling infrastructure
- Cross-subsystem communication

**Test Infrastructure**:
- Integration tests
- Escalation flow tests
- Event handling tests
- Cross-subsystem tests

---

## Cleanup Scope

### Test Directories

Primary scope:
- `tests/wave1_integration_builder/`

Related scope (Wave 1.0.2 specific tests):
- Integration-related tests in `tests/wave1_0_qa_infrastructure/`

---

## Current State (Baseline)

**Status**: PENDING INVENTORY

### Known Issues

**7 Failing Tests** (AttributeError in escalation subsystem):
1. `test_qa_097_create_escalation_with_5_elements` - AttributeError: 'dict' object has no attribute 'what'
2. `test_qa_098_route_escalation_to_johan` - AttributeError: 'dict' object has no attribute 'escalation_id'
3. `test_qa_099_present_escalation_in_ui` - AttributeError: 'dict' object has no attribute 'escalation_id'
4. `test_qa_100_handle_escalation_decision` - AttributeError: 'dict' object has no attribute 'escalation_id'
5. `test_qa_101_track_escalation_lifecycle` - AttributeError: 'dict' object has no attribute 'escalation_id'
6. `test_qa_102_escalation_priority_handling` - AttributeError: 'dict' object has no attribute 'escalation_id'
7. `test_qa_103_escalation_context_linking` - AttributeError: 'dict' object has no attribute 'escalation_id'

**Root Cause**: Tests expect object with attributes, but receiving dictionary

### Metrics (To Be Determined)
- **Warnings**: TBD
- **Failing Tests**: 7 (known) + TBD (from warnings)
- **Passing Tests**: TBD
- **Test Pass Rate**: TBD

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
pytest tests/wave1_integration_builder/ -v -W default
```

Document warnings by category and all failure types.

---

### Phase 2: Fix Known AttributeErrors (2-4 hours)

**Strategy**:
1. Review escalation manager implementation
2. Identify where dict is returned instead of object
3. Options:
   - Convert dict to proper object/dataclass
   - Update tests to access dict keys instead of attributes
   - Create proper escalation model/class

**Recommended**: Create proper escalation class with attributes (better design)

**Steps**:
1. Create `Escalation` class/dataclass with required attributes
2. Update escalation manager to return `Escalation` objects
3. Verify all 7 tests now pass
4. Ensure no regression in other tests

---

### Phase 3: Eliminate Warnings (0.5-1 day)

Common integration/event warning patterns:
- Async/await warnings
- Event handler deprecations
- Import warnings
- Type warnings in event payloads
- Integration test fixture warnings

**Strategy**:
1. Fix async patterns and event handlers
2. Update integration APIs if deprecated
3. Clean up imports
4. Add type hints to event payloads
5. Fix test fixtures

---

### Phase 4: Resolve Remaining Test Debt (if any)

Address any additional failing tests discovered during inventory.

---

### Phase 5: Verification (1 hour)

Run full Wave 1.0.2 scope and verify:
- Zero warnings
- Zero failures (all 7 AttributeError tests fixed)
- 100% pass rate
- Collect evidence

---

## Estimated Effort

**Total**: 1 day

| Phase | Estimated Time |
|-------|----------------|
| Inventory | 0.5 hours |
| Fix AttributeErrors | 2-4 hours |
| Eliminate Warnings | 0.5-1 day |
| Resolve Other Debt | 0-2 hours |
| Verification & Evidence | 2 hours |

---

## Success Criteria

- ✅ Zero warnings in all Wave 1.0.2 scope tests
- ✅ Zero failing tests (including 7 known AttributeError tests)
- ✅ 100% test pass rate
- ✅ Escalation subsystem properly returns objects (not dicts)
- ✅ All fixes documented
- ✅ Completion evidence provided
- ✅ FM verification PASS

---

## Dependencies

**Depends On**: Wave 1.0.1 cleanup COMPLETE  
**Blocks**: Wave 1.0.3 cleanup

**Can Start**: After Wave 1.0.1 FM verification PASS

---

## Completion Evidence Requirements

Create in `evidence/zwzdi/wave1_0_2/`:

1. **COMPLETION_SUMMARY.md** (include details on AttributeError fixes)
2. **test_output.txt**
3. **fixes_detailed.md** (document escalation subsystem fix)

---

## Common Integration Warning Patterns

### Expected Warning Types

1. **Async/await warnings**
2. **Event handler deprecations**
3. **Integration test fixture warnings**
4. **Type warnings in event payloads**
5. **Import warnings**

### Common Fixes

- Update async patterns to modern syntax
- Fix event handler registrations
- Properly cleanup integration test fixtures
- Add type hints to events and handlers

---

## Risk Assessment

### Low Risk
- Import warnings
- Simple type warnings

### Medium Risk
- Event handler updates
- Integration fixture cleanup

### High Risk
- **AttributeError fixes** (affects escalation subsystem core functionality)
- Async pattern changes (may affect multiple tests)

**Mitigation for High Risk**:
- Test escalation subsystem thoroughly after AttributeError fix
- Verify no regression in escalation flows
- Escalate to FM if unsure about escalation design approach

---

## Special Notes

### AttributeError Fix Guidance

**Current behavior**: Escalation manager returns dict  
**Expected behavior**: Should return object with attributes

**Recommended approach**:
```python
from dataclasses import dataclass

@dataclass
class Escalation:
    escalation_id: str
    what: str
    why: str
    when: str
    context: dict
    # ... other fields
```

Then update escalation manager to return `Escalation` instances.

**Do NOT** just change tests to access dict keys - that's fixing the symptom, not the root cause.

---

## Builder Checklist

Before starting:
- [ ] Read GOVERNANCE_LEARNING_BRIEF.md
- [ ] Reviewed this cleanup plan
- [ ] Acknowledged accountability
- [ ] Wave 1.0.1 verified COMPLETE

During execution:
- [ ] Inventory complete
- [ ] AttributeError tests identified and understood
- [ ] Escalation subsystem fix implemented
- [ ] All 7 AttributeError tests passing
- [ ] All warnings eliminated
- [ ] All other test debt resolved
- [ ] Verification passed locally
- [ ] Evidence collected

Before submission:
- [ ] Zero warnings confirmed
- [ ] Zero failures confirmed (all 7 fixed)
- [ ] 100% pass rate confirmed
- [ ] Escalation subsystem design improved
- [ ] Evidence files created
- [ ] FM verification requested

---

**Plan Status**: READY (blocked by Wave 1.0.1)  
**Awaiting**: Wave 1.0.1 completion  
**Owner**: Integration Builder (to be assigned)  
**Created By**: Foreman (FM)
