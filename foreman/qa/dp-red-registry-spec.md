# Design-Phase RED (DP-RED) Registry Specification

**Version**: 1.0.0  
**Status**: Active  
**Authority**: BUILD_PHILOSOPHY.md + QA Governance  
**Last Updated**: 2025-12-16

---

## I. Purpose and Authority

### Purpose

The DP-RED Registry provides a **controlled mechanism** for managing intentionally RED (failing) tests during the design phase, without weakening QA standards.

**Objective**: Allow design-phase work to proceed while RED tests exist, while ensuring RED cannot leak into production builds.

### Constitutional Authority

This mechanism is authorized by and extends:
- **BUILD_PHILOSOPHY.md** Phase 2: RED QA (Failing Tests)
- **QA Governance** - Zero Test Debt + 100% Pass Requirements
- **Build-to-Green Enforcement** - Strict QA validation

### Core Principle

**Intentional RED is acceptable ONLY during design phase, and ONLY when explicitly registered.**

- Not "skip tests to make green"
- Not "defer QA forever"  
- Not "ignore failures"
- **Explicit registration** of intentional failures during architecture design

---

## II. What is DP-RED?

### Design-Phase RED (DP-RED)

**Definition**: Tests that are intentionally RED (failing) because the implementation does not yet exist, registered during the design phase.

**Valid Use Cases**:
1. **Wave 0 Minimum RED Suite** - Architecture validation tests before implementation exists
2. **New Module Design** - Tests written as part of architecture before building
3. **Integration Contracts** - Tests for interfaces not yet implemented

**INVALID Use Cases** (will be blocked):
1. Failing tests in already-built modules
2. Tests failing due to bugs in existing code
3. Skipped tests or test debt
4. Tests marked TODO/FIXME
5. Production failures disguised as DP-RED

### How DP-RED Differs from Test Debt

| Aspect | DP-RED (ALLOWED in design phase) | Test Debt (NEVER ALLOWED) |
|--------|-----------------------------------|---------------------------|
| **Intent** | Intentional RED before build | Skipped/incomplete tests |
| **Registration** | Explicitly registered | Hidden or informal |
| **Phase** | Design phase only | Any phase (always blocked) |
| **Exit Criteria** | Implementation completes | Must be fixed immediately |
| **Enforcement** | Registry + phase gate | CI hard block |

---

## III. DP-RED Registry Schema

### Registry File Location

```
foreman/qa/dp-red-registry.json
```

### Schema Structure

```json
{
  "schema_version": "1.0.0",
  "phase": "QA_DESIGN",
  "entries": [
    {
      "test_id": "string (required)",
      "test_path": "string (required)",
      "phase": "string (required, must be QA_DESIGN)",
      "reason": "string (required, min 20 chars)",
      "registered_by": "string (required)",
      "registered_date": "ISO-8601 timestamp (required)",
      "expiry_date": "ISO-8601 timestamp (optional)",
      "module": "string (required)",
      "category": "string (required)",
      "architecture_ref": "string (required)",
      "build_blocker": "boolean (required)"
    }
  ]
}
```

### Field Definitions

#### test_id (required)
- **Type**: string
- **Description**: Unique identifier for the test
- **Format**: `module.category.test_name`
- **Example**: `foreman.liveness.test_heartbeat_generation`

#### test_path (required)
- **Type**: string
- **Description**: Full file path to the test
- **Example**: `tests/wave0_minimum_red/test_liveness.py::test_heartbeat_generation`

#### phase (required)
- **Type**: string (enum)
- **Values**: `QA_DESIGN` only
- **Description**: Current QA phase - MUST be QA_DESIGN for entry to be valid

#### reason (required)
- **Type**: string
- **Min Length**: 20 characters
- **Description**: Clear explanation why this test is intentionally RED
- **Example**: "Implementation module foreman.runtime.liveness does not exist yet. Test validates architecture contract before build."

#### registered_by (required)
- **Type**: string
- **Description**: Who registered this DP-RED entry
- **Example**: "Foreman" or "Johan"

#### registered_date (required)
- **Type**: ISO-8601 timestamp
- **Description**: When this entry was registered
- **Example**: "2025-12-16T10:30:00Z"

#### expiry_date (optional)
- **Type**: ISO-8601 timestamp
- **Description**: When this DP-RED expires (if known)
- **Example**: "2025-12-20T00:00:00Z"
- **Note**: If not set, entry is valid until manually removed

#### module (required)
- **Type**: string
- **Description**: Which module this test belongs to
- **Example**: "foreman", "wrac", "pit"

#### category (required)
- **Type**: string
- **Description**: Test category
- **Values**: "liveness", "governance", "decision", "evidence", "integration", etc.

#### architecture_ref (required)
- **Type**: string
- **Description**: Reference to architecture document that defines this test's contract
- **Example**: "foreman/architecture/FOREMAN_ARCHITECTURE_v1.0.md#liveness-system"

#### build_blocker (required)
- **Type**: boolean
- **Description**: Whether this test blocks build progression
- **Value**: true (all DP-RED tests block build until implemented)

---

## IV. Phase Model

### QA Phases

```
1. QA_DESIGN    → DP-RED allowed ✅
2. QA_BUILD     → DP-RED BLOCKED ❌
3. QA_GREEN     → DP-RED BLOCKED ❌
4. QA_VALIDATE  → DP-RED BLOCKED ❌
```

### Phase Transition Rules

#### From QA_DESIGN → QA_BUILD

**Preconditions**:
- ✅ Architecture is frozen
- ✅ All DP-RED entries documented in registry
- ✅ Build plan created

**No Precondition**: Registry must be empty (RED tests still allowed)

#### From QA_BUILD → QA_GREEN

**Hard Block**: DP-RED registry MUST be empty

**Validation**:
- ❌ If any DP-RED entries exist → BUILD BLOCKED
- ❌ If any tests are RED → BUILD BLOCKED  
- ✅ All tests GREEN + Registry empty → Proceed

#### From QA_GREEN → QA_VALIDATE

**Hard Block**: DP-RED registry MUST be empty (already enforced)

### Current Phase Storage

**File**: `foreman/qa/current-phase.json`

```json
{
  "phase": "QA_DESIGN",
  "updated_at": "2025-12-16T10:30:00Z",
  "updated_by": "Foreman"
}
```

---

## V. Merge Gate Logic

### Design Phase Merge Rules

**When phase == QA_DESIGN**:

```python
def can_merge_in_design_phase(test_results, registry):
    """
    Allow merge during design phase if:
    1. All RED tests are registered in DP-RED registry
    2. Current phase is QA_DESIGN
    3. No test debt exists
    4. All DP-RED entries are valid
    """
    failing_tests = get_failing_tests(test_results)
    registered_tests = get_registered_dp_red_tests(registry)
    
    # Check all RED tests are registered
    unregistered_red = failing_tests - registered_tests
    if unregistered_red:
        return False, f"RED tests not in DP-RED registry: {unregistered_red}"
    
    # Check phase
    if registry['phase'] != 'QA_DESIGN':
        return False, f"Phase is {registry['phase']}, DP-RED only valid in QA_DESIGN"
    
    # Check no test debt
    if has_test_debt():
        return False, "Test debt detected - fix before merge"
    
    # Check all entries valid
    if not validate_registry_entries(registry):
        return False, "Invalid DP-RED registry entries"
    
    return True, "Merge allowed - all RED tests registered as DP-RED"
```

### Build Phase Merge Rules

**When phase == QA_BUILD or later**:

```python
def can_merge_in_build_phase(test_results, registry):
    """
    Hard block if:
    1. Any DP-RED entries exist
    2. Any tests are RED
    """
    if registry['entries']:
        return False, "DP-RED registry not empty - must be cleared before build phase"
    
    if has_red_tests(test_results):
        return False, "RED tests detected - 100% pass required"
    
    return True, "Merge allowed - all tests GREEN and no DP-RED entries"
```

---

## VI. Validation Rules

### Registry Validation

**validate-dp-red-compliance.py** checks:

1. **Schema Validation**
   - All required fields present
   - Field types correct
   - Enum values valid

2. **Phase Validation**
   - Current phase from current-phase.json
   - Registry phase matches current phase
   - Phase is QA_DESIGN (if DP-RED entries exist)

3. **Entry Validation**
   - test_id unique
   - test_path exists and is valid
   - reason >= 20 characters
   - architecture_ref exists
   - registered_date not in future

4. **Test Mapping Validation**
   - Every failing test is in registry
   - Every registry entry maps to a failing test
   - No orphaned entries

5. **Expiry Validation**
   - If expiry_date set, not already expired
   - Warning if expiry approaching

### Abuse Prevention

**Mechanical blocks for abuse attempts**:

1. **Can't fake phase**
   - Phase stored in version-controlled current-phase.json
   - Can only be changed by Foreman or Owner

2. **Can't hide failures**
   - Validation maps registry to actual test results
   - Unmapped RED tests block merge

3. **Can't skip registration**
   - All RED tests must be registered
   - Unregistered RED → hard block

4. **Can't carry into build**
   - Registry must be empty in QA_BUILD phase
   - Enforced by CI

5. **Can't use for test debt**
   - Test debt detection still runs
   - Skipped tests still blocked
   - TODO/FIXME still blocked

---

## VII. CI/CD Integration

### Workflow: build-to-green-enforcement.yml

**New Job**: `validate-dp-red-compliance`

```yaml
validate-dp-red-compliance:
  name: "Validate DP-RED Compliance"
  runs-on: ubuntu-latest
  
  steps:
    - name: Validate DP-RED Registry
      run: |
        python foreman/scripts/validate-dp-red-compliance.py \
          --registry foreman/qa/dp-red-registry.json \
          --phase-file foreman/qa/current-phase.json \
          --test-dir tests \
          --json > dp-red-compliance-report.json
        
        if [ $? -ne 0 ]; then
          echo "::error::DP-RED validation failed"
          exit 1
        fi
```

**Job Dependencies**:
```
enforce-zero-test-debt
    ↓
validate-dp-red-compliance (NEW)
    ↓
enforce-100-percent-pass
    ↓
...
```

### Artifacts Generated

1. **dp-red-compliance-report.json** - Full validation report
2. **dp-red-summary.md** - Human-readable summary

---

## VIII. Dashboard Integration

### QA Dashboard Updates

**New Section**: DP-RED Status

```
┌─────────────────────────────────────────┐
│ DP-RED Status                           │
├─────────────────────────────────────────┤
│ Phase: QA_DESIGN                        │
│ Registered: 58 tests                    │
│ Expiring Soon: 0                        │
│ Invalid Entries: 0                      │
│                                         │
│ Categories:                             │
│   Liveness: 9 tests                     │
│   Governance: 11 tests                  │
│   Decision: 11 tests                    │
│   Evidence: 14 tests                    │
│   Integration: 13 tests                 │
│                                         │
│ Status: ✅ All RED tests registered     │
└─────────────────────────────────────────┘
```

### Distinction from Failures

```
Test Results:
  Total: 58
  Passing: 0
  Failing: 58
    ├─ DP-RED (Registered): 58 ✅
    └─ Actual Failures: 0 ❌
  
Status: ✅ GREEN for design phase
```

---

## IX. Governance & Compliance

### Authority Chain

```
BUILD_PHILOSOPHY.md (Supreme Authority)
    ↓
Phase 2: RED QA (Failing Tests)
    ↓
DP-RED Policy (This Spec)
    ↓
validate-dp-red-compliance.py (Enforcement)
    ↓
CI/CD (Automated Blocking)
```

### Compliance Requirements

1. **Registration Mandatory**
   - All RED tests during design must be registered
   - Unregistered RED → hard block

2. **Phase Enforcement**
   - DP-RED only in QA_DESIGN phase
   - Auto-blocked in all other phases

3. **Expiry Management**
   - Optional expiry dates
   - Warning when approaching expiry
   - No auto-removal (must be done explicitly)

4. **Audit Trail**
   - All registrations tracked
   - All phase transitions logged
   - Full evidence trail

### Integration with Enhancement Parking Lot

**DP-RED is NOT a parking lot**

- DP-RED: Temporary, design-phase only
- Parking Lot: Long-term deferrals

**If work needs to be deferred beyond design phase**:
1. Remove DP-RED entry
2. Remove incomplete test (or make it pass)
3. Add to Enhancement Parking Lot
4. Link to future roadmap

---

## X. Example Usage

### Example 1: Wave 0 Minimum RED

**Registry Entry**:
```json
{
  "test_id": "foreman.liveness.test_heartbeat_generation",
  "test_path": "tests/wave0_minimum_red/test_liveness.py::test_heartbeat_generation",
  "phase": "QA_DESIGN",
  "reason": "Implementation module foreman.runtime.liveness does not exist yet. Test validates architecture contract before build.",
  "registered_by": "Foreman",
  "registered_date": "2025-12-16T10:00:00Z",
  "module": "foreman",
  "category": "liveness",
  "architecture_ref": "foreman/architecture/FOREMAN_ARCHITECTURE_v1.0.md#liveness-system",
  "build_blocker": true
}
```

**Result**:
- ✅ Merge allowed in QA_DESIGN phase
- ❌ Blocks progression to QA_BUILD phase

### Example 2: Transition to Build Phase

**Before Transition**:
```json
{
  "phase": "QA_DESIGN",
  "entries": [58 DP-RED entries]
}
```

**Attempt Transition**:
```bash
$ python foreman/scripts/transition-qa-phase.py --to QA_BUILD

❌ TRANSITION BLOCKED
DP-RED registry contains 58 entries
All RED tests must be implemented and GREEN before build phase

Recommendation: Run build-to-green to implement:
- foreman.liveness (9 tests)
- foreman.governance (11 tests)
- foreman.decision (11 tests)
- foreman.evidence (14 tests)
- foreman.integration (13 tests)
```

---

## XI. Success Metrics

### Effectiveness Metrics

**Target**:
- ✅ 100% of RED tests registered during design
- ✅ Zero DP-RED leakage into build phase
- ✅ Zero abuse incidents
- ✅ Design phase merges unblocked
- ✅ Build phase quality unchanged

### Monitoring

Track:
- DP-RED entry count over time
- Time in DP-RED before implementation
- Phase transition attempts blocked
- Validation failures by type

---

## XII. Version and Authority

**Version**: 1.0.0  
**Status**: Active  
**Authority**: BUILD_PHILOSOPHY.md + QA Governance  
**Precedence**: Extends Build-to-Green enforcement  
**Last Updated**: 2025-12-16  
**Owner**: Johan (MaturionISMS)  
**Enforcer**: CI/CD + Foreman

**Changelog**:
- 1.0.0 (2025-12-16): Initial DP-RED Registry Specification

---

## XIII. Summary: The Commitment

DP-RED commits to:

1. ✅ **Controlled RED** - Intentional RED only in design phase
2. ✅ **Zero Leakage** - Cannot enter build phase
3. ✅ **Full Registration** - All RED must be registered
4. ✅ **Mechanical Enforcement** - Abuse is impossible
5. ✅ **Zero Weakening** - QA standards unchanged

**Intentional RED is not test debt. It's architecture validation.**

---

*END OF DP-RED REGISTRY SPECIFICATION*
