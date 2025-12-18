# Design-Phase RED (DP-RED) Policy

**Version**: 1.0.0  
**Status**: Active  
**Authority**: BUILD_PHILOSOPHY.md + QA Governance  
**Last Updated**: 2025-12-16

---

## I. Policy Statement

### Purpose

This policy establishes the rules and procedures for managing intentionally RED (failing) tests during the QA design phase.

**Core Principle**: Intentional RED during design phase is acceptable ONLY when explicitly registered and controlled.

### Authority

This policy is mandated by:
- BUILD_PHILOSOPHY.md Phase 2: RED QA (Failing Tests)
- Governance Supremacy Rule
- Zero Test Debt Constitutional Rule
- QA Governance Framework

---

## II. What is DP-RED?

### Definition

**Design-Phase RED (DP-RED)**: Tests that are intentionally failing because the implementation does not yet exist, registered during the QA design phase.

### Distinguished from Test Debt

| DP-RED (CONTROLLED) | Test Debt (FORBIDDEN) |
|---------------------|----------------------|
| Tests for unimplemented features | Skipped or incomplete tests |
| Explicitly registered | Hidden or informal |
| Design phase only | Any phase (always blocked) |
| Clear exit criteria | No clear resolution |
| Architectural validation | Development shortcuts |

---

## III. When DP-RED is Allowed

### VALID Use Cases

1. **Wave 0 Minimum RED Suite**
   - Architecture validation tests written before implementation
   - Tests verify contracts and interfaces that will be built
   - Example: foreman.runtime.liveness tests before liveness module exists

2. **New Module Design**
   - Tests written as part of architectural design
   - Tests define the expected behavior of new modules
   - Tests serve as executable specifications

3. **Integration Contract Validation**
   - Tests for interfaces not yet implemented by other teams/modules
   - Cross-module integration tests during design phase

### INVALID Use Cases (Will be BLOCKED)

1. ❌ Failing tests in already-implemented modules
2. ❌ Tests failing due to bugs in existing code
3. ❌ Skipped tests or tests marked with .skip()
4. ❌ Tests with TODO/FIXME markers
5. ❌ Production failures disguised as "design phase"
6. ❌ Test debt hidden in DP-RED registry

---

## IV. Registration Requirements

### Mandatory Registration

ALL intentionally RED tests during design phase MUST be registered in:
```
foreman/qa/dp-red-registry.json
```

### Registration Fields

**Required for every entry**:
- `test_id`: Unique identifier
- `test_path`: Full path to test
- `phase`: Must be "QA_DESIGN"
- `reason`: Clear explanation (min 20 chars)
- `registered_by`: Who registered
- `registered_date`: ISO-8601 timestamp
- `module`: Which module
- `category`: Test category
- `architecture_ref`: Link to architecture document
- `build_blocker`: true (all DP-RED blocks build)

**Optional**:
- `expiry_date`: When this registration expires

### Registration Process

**Who can register**:
- Foreman (primary)
- Repository Owner (Johan)

**How to register**:
1. Create entry in dp-red-registry.json with all required fields
2. Commit and push to repository
3. CI validates registration automatically
4. Merge proceeds if validation passes

---

## V. Phase Rules

### QA_DESIGN Phase

**DP-RED Status**: ✅ ALLOWED

**Rules**:
- RED tests MUST be in DP-RED registry
- Unregistered RED tests → BLOCKED
- Test debt still forbidden
- Merge allowed if all RED tests registered

### QA_BUILD Phase

**DP-RED Status**: ❌ BLOCKED

**Rules**:
- DP-RED registry MUST be empty
- Any DP-RED entries → HARD BLOCK
- Cannot transition from QA_DESIGN with DP-RED entries
- All tests must be GREEN

### QA_GREEN Phase

**DP-RED Status**: ❌ BLOCKED

**Rules**:
- DP-RED registry MUST be empty (enforced in QA_BUILD)
- 100% pass rate required
- No exceptions

### QA_VALIDATE Phase

**DP-RED Status**: ❌ BLOCKED

**Rules**:
- DP-RED registry MUST be empty
- Full validation suite GREEN
- Ready for production

---

## VI. Merge Gate Logic

### Design Phase Merge

```
IF phase == QA_DESIGN:
    IF all RED tests in registry:
        IF no test debt:
            IF all entries valid:
                ✅ MERGE ALLOWED
            ELSE:
                ❌ MERGE BLOCKED (invalid entries)
        ELSE:
            ❌ MERGE BLOCKED (test debt)
    ELSE:
        ❌ MERGE BLOCKED (unregistered RED)
ELSE:
    # Build phase or later
    IF registry has entries:
        ❌ MERGE BLOCKED (DP-RED not cleared)
    IF any RED tests:
        ❌ MERGE BLOCKED (tests not GREEN)
    ELSE:
        ✅ MERGE ALLOWED
```

### Build Phase Transition

**Preconditions for QA_DESIGN → QA_BUILD**:
- ✅ Architecture frozen
- ✅ Build plan created
- ✅ All dependencies resolved

**NOT Required**:
- ❌ DP-RED registry empty (RED tests still OK in design)

**Required for QA_BUILD → QA_GREEN**:
- ✅ DP-RED registry MUST be empty
- ✅ All tests GREEN (100%)

---

## VII. Enforcement Mechanisms

### Automated Enforcement

**CI/CD Validation** (every commit):
1. Test debt detection
2. **DP-RED compliance validation** ← NEW
3. 100% pass enforcement
4. Suppressed failure detection
5. Constitutional compliance

**Script**: `foreman/scripts/validate-dp-red-compliance.py`

**Workflow**: `.github/workflows/build-to-green-enforcement.yml`

### Validation Checks

1. **Schema Validation**
   - All required fields present
   - Correct data types
   - Valid enum values

2. **Phase Validation**
   - Registry phase matches current phase
   - DP-RED only in QA_DESIGN

3. **Entry Validation**
   - Unique test IDs
   - Valid test paths
   - Sufficient reason length
   - Architecture references exist

4. **Test Mapping**
   - All RED tests registered
   - All entries map to actual tests
   - No orphaned entries

5. **Build Gate**
   - Empty registry in build phases

### Abuse Prevention

**Mechanically prevented**:
1. ❌ Cannot fake phase (version-controlled phase file)
2. ❌ Cannot hide failures (validation maps registry to tests)
3. ❌ Cannot skip registration (unregistered RED blocked)
4. ❌ Cannot carry into build (registry must be empty)
5. ❌ Cannot use for test debt (debt detection still runs)

---

## VIII. Exit Criteria

### How to Clear DP-RED

**For each registered test**:
1. Implement the missing functionality
2. Make the test pass (GREEN)
3. Remove entry from dp-red-registry.json
4. Verify removal with validation script

**Bulk clearing**:
```bash
# After implementation wave completes
# Verify all tests GREEN
python -m pytest tests/

# Clear registry
echo '{"schema_version": "1.0.0", "phase": "QA_BUILD", "entries": []}' > foreman/qa/dp-red-registry.json

# Update phase
echo '{"phase": "QA_BUILD", "updated_at": "2025-12-16T12:00:00Z", "updated_by": "Foreman"}' > foreman/qa/current-phase.json

# Validate
python foreman/scripts/validate-dp-red-compliance.py

# Commit
git add foreman/qa/dp-red-registry.json foreman/qa/current-phase.json
git commit -m "Transition to QA_BUILD - all tests GREEN"
```

---

## IX. Relationship to Enhancement Parking Lot

### DP-RED vs Parking Lot

| Aspect | DP-RED | Enhancement Parking Lot |
|--------|--------|-------------------------|
| Purpose | Design-phase validation | Long-term deferral |
| Duration | Days to weeks | Weeks to months |
| Phase | QA_DESIGN only | Any phase |
| Tests | RED tests exist | Tests removed or GREEN |
| Commitment | Must implement soon | Roadmap item |

### When to Move from DP-RED to Parking Lot

**Scenario**: Feature needs to be deferred beyond design phase

**Process**:
1. Remove test from codebase OR make it pass with minimal stub
2. Remove entry from dp-red-registry.json
3. Add to Enhancement Parking Lot with:
   - Feature description
   - Rationale for deferral
   - Target timeline
   - Link to removed test (if applicable)

**Example**:
```markdown
# Enhancement Parking Lot Entry

## Feature: Advanced Liveness Monitoring
**Status**: Deferred to Q2 2026  
**Reason**: Core liveness sufficient for MVP  
**Original Tests**: Removed from tests/wave0_minimum_red/test_liveness.py  
**Architecture**: foreman/architecture/FOREMAN_ARCHITECTURE_v1.0.md#advanced-liveness
```

---

## X. Monitoring and Reporting

### Dashboards

**QA Dashboard** shows:
- Current phase
- DP-RED entry count
- Entries by category
- Expiring entries
- Validation status

**Governance Dashboard** shows:
- Phase transition history
- DP-RED duration metrics
- Abuse attempt logs (if any)

### Metrics Tracked

1. **DP-RED Count Over Time**
   - Target: Decreasing over build phase
   - Alert: Increasing or flat

2. **Time in DP-RED**
   - Target: < 2 weeks per test
   - Alert: > 4 weeks

3. **Phase Transition Blocks**
   - Track attempts to transition with non-empty registry
   - Expected: 0 in healthy workflow

4. **Validation Failures**
   - By type: schema, phase, mapping, etc.
   - Target: 0

---

## XI. Escalation Procedures

### When to Escalate

**Immediate escalation to Foreman**:
1. DP-RED entries older than 4 weeks
2. Multiple failed transition attempts
3. Suspected abuse
4. Invalid entries that cannot be fixed

**Escalation to Owner (Johan)**:
1. Policy exception requests
2. Phase override requirements
3. Emergency production issues

### Resolution Process

1. Investigate root cause
2. Document findings in governance memory
3. Implement corrective action
4. Update registry or policy as needed
5. Re-validate

---

## XII. Compliance and Audit

### Audit Trail

**Tracked in version control**:
- All registry changes (who, when, what)
- Phase transitions
- Validation results
- Policy modifications

**Stored in CI artifacts**:
- dp-red-compliance-report.json
- Validation logs
- Enforcement summaries

### Compliance Requirements

1. ✅ All RED tests registered during design
2. ✅ Registry empty in build phases
3. ✅ Valid entries only
4. ✅ Test debt = 0 always
5. ✅ 100% pass in build phases

**Violation = Build BLOCKED**

---

## XIII. Examples

### Example 1: Valid DP-RED Entry

```json
{
  "test_id": "foreman.governance.test_architecture_freeze",
  "test_path": "tests/wave0_minimum_red/test_governance_supremacy.py::test_architecture_cannot_be_modified_during_build",
  "phase": "QA_DESIGN",
  "reason": "Governance enforcement module foreman.governance.architecture_freeze does not exist yet. Test validates that architecture is frozen during build execution per BUILD_PHILOSOPHY.md.",
  "registered_by": "Foreman",
  "registered_date": "2025-12-16T08:00:00Z",
  "module": "foreman",
  "category": "governance",
  "architecture_ref": "foreman/architecture/FOREMAN_ARCHITECTURE_v1.0.md#governance-enforcement",
  "build_blocker": true
}
```

**Status**: ✅ Valid - Will allow merge in QA_DESIGN

### Example 2: Invalid Entry (Blocked)

```json
{
  "test_id": "mymodule.test_broken",
  "test_path": "tests/test_mymodule.py::test_broken",
  "phase": "QA_DESIGN",
  "reason": "Broken",
  "registered_by": "Developer",
  "registered_date": "2025-12-16T08:00:00Z"
}
```

**Violations**:
- ❌ Reason too short (< 20 chars)
- ❌ Missing required fields (module, category, architecture_ref, build_blocker)
- ❌ Suspicious reason ("Broken" suggests bug, not design-phase validation)

**Status**: ❌ Blocked

---

## XIV. Version and Authority

**Version**: 1.0.0  
**Status**: Active  
**Authority**: BUILD_PHILOSOPHY.md + QA Governance  
**Precedence**: Extends Build-to-Green Enforcement  
**Last Updated**: 2025-12-16  
**Owner**: Johan (MaturionISMS)  
**Enforcer**: CI/CD + Foreman

**Changelog**:
- 1.0.0 (2025-12-16): Initial DP-RED Policy

---

## XV. Summary

### Policy Commitments

1. ✅ **Controlled RED** - Only in design phase, only when registered
2. ✅ **Zero Leakage** - Cannot enter build phase
3. ✅ **Mechanical Enforcement** - Abuse impossible
4. ✅ **Zero Weakening** - QA standards unchanged
5. ✅ **Full Auditability** - Complete evidence trail

### Key Messages

**For Developers**:
- DP-RED allows design-phase work without blocking merges
- All RED tests must be registered
- Registry must be cleared before build phase

**For QA**:
- DP-RED does not weaken QA standards
- 100% pass still required in build phases
- Test debt still forbidden always

**For Governance**:
- Abuse is mechanically prevented
- Full audit trail maintained
- Phase gates enforced automatically

**Intentional RED is not test debt. It's architectural validation.**

---

*END OF DP-RED POLICY*
