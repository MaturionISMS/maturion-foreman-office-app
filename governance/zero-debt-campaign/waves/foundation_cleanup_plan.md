# Foundation Cleanup Plan

**Campaign**: ZWZDI-2026-001  
**Wave**: Foundation (Cross-Cutting Infrastructure)  
**Builders**: Schema Builder + API Builder (joint ownership)  
**Status**: BLOCKED (awaiting all specific waves completion)  
**Created**: 2026-01-08

---

## Wave Overview

### Original Foundation Work

**Implemented**: Cross-cutting infrastructure spanning multiple waves  
**Deliverables**:
- Foundation layer architecture
- Shared infrastructure components
- Startup requirements system
- Build intervention system
- Cross-wave integration points

**Test Infrastructure**:
- Foundation/infrastructure tests
- Startup requirements tests
- Build control tests
- Cross-cutting integration tests

---

## Cleanup Scope

### Test Directories and Files

Primary scope:
- `tests/test_startup_requirement_loader.py` (14 failing tests)
- `tests/test_startup_guard_spec.py`
- `tests/test_build_intervention.py`
- `tests/test_build_node_inspector.py`
- Cross-cutting tests in `tests/wave1_0_qa_infrastructure/`

---

## Current State (Baseline)

**Status**: PENDING INVENTORY

### Known Issues

**14 Failing Tests** (FileNotFoundError - missing startup requirements files):

In `test_startup_requirement_loader.py`:
1. `test_requirements_exist` - startup-requirements.json not found
2. `test_requirements_structure` - startup-requirements.json not found
3. `test_requirements_include_memory_checks` - startup-requirements.json not found
4. `test_loader_exports_required_methods` - RequirementLoader.ts not found
5. `test_loader_defines_types` - RequirementLoader.ts not found
6. `test_assessment_includes_status` - RequirementLoader.ts not found
7. `test_no_execution_in_loader` - RequirementLoader.ts not found
8. `test_readme_states_no_execution` - README.md not found
9. `test_critical_statement_present` - README.md not found
10. `test_integration_with_commissioning_documented` - README.md not found
11. `test_validators_are_read_only` - RequirementLoader.ts not found
12. `test_ac_requirements_loadable` - startup-requirements.json not found
13. `test_ac_validation_results_surfaced` - RequirementLoader.ts not found
14. `test_ac_read_only_assessment_only` - README.md not found
15. `test_ac_no_execution_triggers` - README.md not found

**Missing Files**:
- `lib/startup/startup-requirements.json`
- `lib/startup/RequirementLoader.ts`
- `lib/startup/README.md`

### Metrics (To Be Determined)
- **Warnings**: TBD
- **Failing Tests**: 14 (known) + TBD
- **Passing Tests**: TBD
- **Test Pass Rate**: TBD

---

## Target State

**Warnings**: 0 (ZERO)  
**Failing Tests**: 0 (ZERO)  
**Test Pass Rate**: 100%

**Required**: All missing startup requirements files created OR tests properly removed with documentation.

---

## Cleanup Strategy

### Phase 1: Inventory (1 hour)

Run tests:
```bash
pytest tests/test_startup_requirement_loader.py tests/test_startup_guard_spec.py tests/test_build_intervention.py tests/test_build_node_inspector.py -v -W default
```

Document:
1. All warnings by category
2. All failures by type
3. Assessment of startup requirements system status

---

### Phase 2: Resolve Startup Requirements Files (4-6 hours)

**Critical Decision**: Are startup requirements still needed?

#### Option A: Implement Missing Files (if functionality needed)

1. **Create `lib/startup/` directory**
2. **Create `startup-requirements.json`**:
   - Define startup requirements structure
   - Include memory checks
   - Define validation criteria

3. **Create `RequirementLoader.ts`**:
   - Implement loader exports
   - Define required types
   - Implement read-only assessment (NO execution)
   - Include status reporting

4. **Create `README.md`**:
   - Document no-execution policy
   - Document integration with commissioning
   - Include critical statements per tests
   - Document read-only assessment

#### Option B: Remove Tests (if functionality obsolete)

1. **Verify with CS2/FM**: Are startup requirements still in architecture?
2. **If obsolete**:
   - Remove all 14 tests
   - Create `STARTUP_REQUIREMENTS_REMOVAL.md` documenting:
     - Why removed
     - What was the original intent
     - Why no longer needed
     - Any replacement functionality
   - Update architecture docs if needed

**Recommended**: Check architecture specs first, then decide.

---

### Phase 3: Eliminate Warnings (0.5-1 day)

Common foundation warning patterns:
- Infrastructure component warnings
- Import warnings
- Type warnings in shared code
- Test fixture warnings
- Build control warnings

**Strategy**:
1. Fix infrastructure component patterns
2. Clean up imports in shared code
3. Add type hints to foundation components
4. Fix shared test fixtures
5. Update build control patterns

---

### Phase 4: Resolve Other Test Debt (if any)

Address any additional failing tests discovered during inventory.

---

### Phase 5: Verification (2 hours)

Run full Foundation scope and verify:
- Zero warnings
- Zero failures (including all 14 startup tests)
- 100% pass rate
- Collect evidence

---

## Estimated Effort

**Total**: 2 days

| Phase | Estimated Time |
|-------|----------------|
| Inventory | 1 hour |
| Startup Requirements Resolution | 4-6 hours |
| Eliminate Warnings | 0.5-1 day |
| Resolve Other Debt | 0-2 hours |
| Verification & Evidence | 2 hours |

**Note**: Time heavily depends on Option A vs B for startup requirements.

---

## Success Criteria

- ✅ Zero warnings in all Foundation scope tests
- ✅ Zero failing tests (including all 14 startup tests)
- ✅ 100% test pass rate
- ✅ Startup requirements either implemented OR properly removed with documentation
- ✅ All fixes documented
- ✅ Completion evidence provided
- ✅ FM verification PASS

---

## Dependencies

**Depends On**: ALL specific waves (1.0 - 1.0.4) COMPLETE  
**Blocks**: Phase 3 (Verification)

**Can Start**: After Wave 1.0.4 FM verification PASS

---

## Joint Ownership

**Schema Builder responsibilities**:
- Database-related foundation components
- Schema infrastructure warnings
- Shared model/data warnings

**API Builder responsibilities**:
- API-related foundation components
- Build control infrastructure
- Shared API/endpoint warnings

**Joint responsibilities**:
- Startup requirements resolution (decide together with FM guidance)
- Cross-cutting integration tests
- Shared fixtures

**Coordination**: Both builders must coordinate, especially on startup requirements decision.

---

## Completion Evidence Requirements

Create in `evidence/zwzdi/foundation/`:

1. **COMPLETION_SUMMARY.md**:
   - Include detailed explanation of startup requirements resolution
   - Document Option A or B chosen and rationale
   - List fixes by builder (Schema vs API)

2. **test_output.txt**

3. **STARTUP_REQUIREMENTS_DECISION.md**:
   - Document decision process for missing files
   - Rationale for implementation or removal
   - CS2/FM approval reference

4. **fixes_detailed.md** (if needed)

---

## Common Foundation Warning Patterns

### Expected Warning Types

1. **Import warnings** (cross-module imports)
2. **Type warnings** (shared types)
3. **Test fixture warnings** (shared fixtures)
4. **Build system warnings**
5. **Infrastructure component warnings**

### Common Fixes

- Clean up cross-module imports
- Add type hints to shared components
- Fix shared test fixtures
- Update build system patterns
- Modernize infrastructure components

---

## Risk Assessment

### Low Risk
- Import warnings
- Simple type warnings

### Medium Risk
- Shared fixture updates (may affect multiple test suites)
- Infrastructure component changes

### High Risk
- **Startup requirements decision** (affects system architecture)
- Cross-cutting changes (may have ripple effects)

**Mitigation for High Risk**:
- Get FM/CS2 guidance on startup requirements
- Test thoroughly after cross-cutting changes
- Coordinate carefully between Schema and API builders

---

## Special Notes

### Startup Requirements Decision Process

**Before implementing OR removing**:

1. **Review architecture specs** in `architecture/` folder
2. **Search for "startup requirements"** in docs
3. **Check git history** for context
4. **Escalate to FM** for guidance
5. **Get CS2 approval** for removal if that's the decision

**DO NOT**:
- Guess whether to implement or remove
- Implement without understanding requirements
- Remove without proper documentation and approval

---

## Builder Checklist

Before starting:
- [ ] Read GOVERNANCE_LEARNING_BRIEF.md
- [ ] Reviewed this cleanup plan
- [ ] Acknowledged joint accountability
- [ ] ALL waves (1.0-1.0.4) verified COMPLETE
- [ ] Coordinated with other builder (Schema ↔ API)

During execution:
- [ ] Inventory complete
- [ ] Startup requirements decision made with FM guidance
- [ ] Startup requirements resolved (implemented or removed)
- [ ] Warnings categorized and assigned
- [ ] All warnings eliminated
- [ ] All test debt resolved
- [ ] Verification passed locally
- [ ] Evidence collected

Before submission:
- [ ] Zero warnings confirmed
- [ ] Zero failures confirmed (all 14 startup tests addressed)
- [ ] 100% pass rate confirmed
- [ ] Startup requirements properly handled
- [ ] Evidence files created
- [ ] Both builders sign off
- [ ] FM verification requested

---

**Plan Status**: READY (blocked by all specific waves)  
**Awaiting**: Waves 1.0-1.0.4 completion  
**Owners**: Schema Builder + API Builder (joint)  
**Created By**: Foreman (FM)
