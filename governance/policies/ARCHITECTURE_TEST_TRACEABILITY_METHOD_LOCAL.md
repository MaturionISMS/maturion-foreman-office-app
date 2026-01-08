# ARCHITECTURE_TEST_TRACEABILITY_METHOD_LOCAL

**Policy ID**: ARCHITECTURE_TEST_TRACEABILITY_METHOD_LOCAL  
**Version**: 1.0.0  
**Date**: 2026-01-08  
**Authority**: Governance Canon  
**Status**: ACTIVE (Local Guidance)

---

## Purpose

This document provides **local guidance** on the canonical ARCHITECTURE_TEST_TRACEABILITY_METHODOLOGY for determining whether tests map to architecture requirements. It prevents incorrect test removal by establishing the correct methodology for traceability analysis.

---

## Canonical Reference

**Source**: APGI-cmy/maturion-foreman-governance  
**Canonical Methodology**: `governance/policy/ARCHITECTURE_TEST_TRACEABILITY_METHODOLOGY.md`  
**Layered Down From**: PR #891  
**Incident Context**: BL-021 (60 tests nearly removed due to wrong methodology)

---

## The BL-021 Lesson

**What Happened**: 60 tests nearly removed using **incorrect traceability methodology**.

**Incorrect methodology used**:
```
Test → Class Name → Search Architecture Document → "Not found" → Remove Test
```

**Correct methodology**:
```
Test → Behavior Under Test → Requirement → Architecture Section → Decision
```

**Result**: Evidence tests, governance tests, and heartbeat tests almost lost.

**Lesson**: **Methodology matters.** Using wrong methodology = catastrophic outcomes.

---

## Correct Traceability Methodology

### Step-by-Step Process

#### Step 1: Identify Behavior Under Test

**Question**: What behavior is this test validating?

**NOT**: What class name appears in the test?  
**INSTEAD**: What system capability, requirement, or constraint is being verified?

**Examples**:
- ❌ Wrong: "Tests class `ArchitectureIndex`"
- ✅ Right: "Validates that architecture index exists and is loadable"

#### Step 2: Map Behavior to Requirement

**Question**: What requirement drives this behavior?

**Sources** (in priority order):
1. Functional Requirements Specification (FRS)
2. Architecture document
3. Governance policy
4. Build philosophy
5. Constitutional rule

**Examples**:
- Behavior: "Architecture index exists and is loadable"
- Requirement: "FM must have access to complete architecture for governance enforcement" (FRS or Architecture)

#### Step 3: Map Requirement to Architecture Section

**Question**: Where is this requirement specified in architecture/governance?

**Search targets**:
- Architecture document sections
- Governance policies
- QA requirements
- Build philosophy principles

**Examples**:
- Requirement: "FM must have access to complete architecture"
- Architecture section: "Architecture Indexing" or "Governance Data Model"

#### Step 4: Make Decision

**Decision tree**:

```
Does test map to architecture/governance requirement?
├─ YES → Test is valid, keep it
│   └─ Document mapping in test docstring/comments
│
├─ NO → Is this an evidence, governance, or heartbeat test?
│   ├─ YES → Test is valid, keep it (validates governance artifact)
│   └─ NO → Does this test validate planned functionality?
│       ├─ YES → Test is valid RED QA, keep it
│       └─ NO → Present evidence to CS2 for removal decision
```

**Default**: When in doubt, **keep the test**.

---

## Common Test Categories

### Category 1: Evidence Tests

**Purpose**: Validate existence and correctness of governance artifacts

**Examples**:
- `test_architecture_index_exists()`
- `test_qa_catalog_schema()`
- `test_tier0_manifest_complete()`

**Traceability**:
- Behavior: "Governance artifact X exists"
- Requirement: "Governance requires artifact X" (from governance policy)
- Architecture: "Governance Data Model" or "Evidence Generation"

**Decision**: **Always keep** unless governance artifact deprecated.

### Category 2: Governance Tests

**Purpose**: Validate constitutional rules and governance policies

**Examples**:
- `test_governance_supremacy_enforced()`
- `test_zero_test_debt_rule_active()`
- `test_design_freeze_prevents_changes()`

**Traceability**:
- Behavior: "Constitutional rule X is enforced"
- Requirement: "Rule X must be enforced" (from T0 document)
- Architecture: "Governance Enforcement" or "Constitutional Rules"

**Decision**: **Always keep** unless constitutional rule changed (requires CS2).

### Category 3: Heartbeat Tests

**Purpose**: Validate basic platform liveness and stall prevention

**Examples**:
- `test_platform_responds()`
- `test_builder_heartbeat()`
- `test_no_infinite_loops()`

**Traceability**:
- Behavior: "Platform responds within timeout"
- Requirement: "Platform must not stall" (from Build Philosophy)
- Architecture: "Liveness Monitoring" or "Anti-Stall Mechanisms"

**Decision**: **Always keep** unless functionality removed (requires architecture change).

### Category 4: RED QA Tests

**Purpose**: Define requirements for future implementation (TDD)

**Examples**:
- Tests in `tests/wave0_minimum_red/RED_QA/`
- Tests marked with future wave markers
- Tests for planned but unimplemented features

**Traceability**:
- Behavior: "Future feature X works correctly"
- Requirement: "Feature X planned in Wave N" (from build plan)
- Architecture: Feature section in architecture document

**Decision**: **Always keep** (RED tests are intentional, not failures to fix).

### Category 5: Behavior Validation Tests

**Purpose**: Validate implemented functionality works correctly

**Examples**:
- API endpoint tests
- UI component tests
- Integration flow tests

**Traceability**:
- Behavior: "API endpoint X returns correct response"
- Requirement: "Endpoint X must exist" (from FRS)
- Architecture: "API Routes" section

**Decision**: Keep if behavior is required. Remove only if requirement deprecated.

---

## Decision Tree for Common Scenarios

### Scenario 1: "Test class name not found in architecture"

**Question**: Is the class name the behavior?  
**Answer**: NO. Classes are implementation details.

**Correct analysis**:
1. What behavior does this test validate?
2. Is that behavior required?
3. If yes → Keep test
4. If no → Why was test created? (Likely speculative or deprecated)

**Example**:
- Test: `test_architecture_indexer_loads()`
- Wrong: "Class `ArchitectureIndexer` not in architecture → Remove"
- Right: "Test validates architecture loading (required behavior) → Keep"

### Scenario 2: "Test validates governance artifact"

**Question**: Does this test check if a governance file exists/is correct?  
**Answer**: If YES → This is an **evidence test**.

**Decision**: **Keep** (evidence tests validate governance compliance)

**Example**:
- Test: `test_tier0_manifest_exists()`
- Analysis: Validates governance artifact (T0 manifest)
- Decision: Keep (evidence test)

### Scenario 3: "Test is RED (failing)"

**Question**: Is this test failing because it's not implemented yet?  
**Answer**: Check test location and markers.

**If in RED_QA directory or marked with future wave**:
- Decision: **Keep** (intentional RED QA)
- Action: Document in RED_QA/README.md

**If in regular test suite**:
- Decision: Fix or escalate (should not be RED in implemented suite)

### Scenario 4: "Multiple tests for same behavior"

**Question**: Are these true duplicates or different aspects?

**Analysis**:
1. Compare test assertions (what's being validated?)
2. Compare test scenarios (edge cases vs. happy path?)
3. Compare test context (unit vs. integration?)

**Acceptable duplication**:
- Unit test + integration test (different levels)
- Happy path + edge cases (different scenarios)
- Current implementation + future enhancement (RED QA)

**True duplication**:
- Same assertions, same scenarios, same context
- Decision: Keep more comprehensive test, remove simpler duplicate

---

## Training Examples

### Example 1: Evidence Test (Correct Traceability)

**Test**:
```python
def test_architecture_index_exists():
    """Validate that ARCHITECTURE_INDEX.json exists."""
    assert Path("ARCHITECTURE_INDEX.json").exists()
```

**Incorrect analysis**:
- "Class `ArchitectureIndex` not in architecture → Remove"

**Correct analysis**:
- Behavior: "Architecture index exists"
- Requirement: "FM needs architecture index for governance" (FRS)
- Architecture: "Governance Data Model" section
- Category: Evidence test
- Decision: **Keep**

### Example 2: Governance Test (Correct Traceability)

**Test**:
```python
def test_governance_supremacy_enforced():
    """Validate that governance blocks non-compliant changes."""
    # Test code...
```

**Incorrect analysis**:
- "No class `GovernanceSupremacy` in architecture → Remove"

**Correct analysis**:
- Behavior: "Governance supremacy rule enforced"
- Requirement: "T0-002 Governance Supremacy Rule"
- Architecture: "Governance Enforcement" section
- Category: Governance test
- Decision: **Keep**

### Example 3: RED QA Test (Correct Traceability)

**Test**:
```python
@pytest.mark.wave2
def test_parking_station_advanced_allocation():
    """Validate advanced parking allocation algorithm."""
    # Test code for future feature...
```

**Incorrect analysis**:
- "Test is failing, no implementation → Remove"

**Correct analysis**:
- Behavior: "Advanced parking allocation works"
- Requirement: "Wave 2 feature" (Build Plan)
- Architecture: "Parking Station" section
- Category: RED QA test (intentional)
- Decision: **Keep** (mark as wave2, implement later)

### Example 4: Speculative Test (Requires CS2 Decision)

**Test**:
```python
def test_blockchain_integration():
    """Validate blockchain integration."""
    # Test code...
```

**Analysis**:
- Behavior: "Blockchain integration works"
- Requirement: None found in FRS, Architecture, or Build Plan
- Architecture: No blockchain section
- Category: Unknown/Speculative
- Decision: **Escalate to CS2** with evidence (no requirement found)

---

## Prevention Checklist

Before removing ANY test, verify:

- [ ] Used **correct methodology** (Behavior → Requirement → Architecture)
- [ ] Did NOT use incorrect methodology (Class Name → Search → Not Found)
- [ ] Checked all test categories (Evidence, Governance, Heartbeat, RED QA)
- [ ] Searched FRS, Architecture, Governance policies, Build Philosophy
- [ ] Documented traceability analysis
- [ ] Obtained appropriate approval (per TEST_REMOVAL_GOVERNANCE_GATE_LOCAL.md)

**If any checkbox is unchecked → STOP. Do not remove test.**

---

## Integration with Test Removal Gate

This methodology is **mandatory** for Step 1 of TEST_REMOVAL_GOVERNANCE_GATE_LOCAL.md:

**Traceability Analysis Required Evidence**:
1. Behavior under test (not class name)
2. Requirement source (FRS, Architecture, Governance, Build Philosophy)
3. Architecture section (if mapped)
4. Test category (Evidence, Governance, Heartbeat, RED QA, Behavior)
5. Decision rationale

**Without correct methodology → No removal authorization**

---

## References

**Canonical Governance**:
- ARCHITECTURE_TEST_TRACEABILITY_METHODOLOGY.md (maturion-foreman-governance)
- PR #891: Test dodging prevention governance
- BL-021: BOOTSTRAP_EXECUTION_LEARNINGS.md

**Related Local Policies**:
- TEST_REMOVAL_GOVERNANCE_GATE_LOCAL.md
- INCIDENT-2026-01-08-WARNING-SUPPRESSION.md

**Implementation**:
- `.github/agents/ForemanApp-agent.md` (required reading before test removal)
- Builder contracts (test governance sections)

---

**Policy Owner**: Foreman (FM)  
**Review Cycle**: Quarterly  
**Next Review**: 2026-04-08  
**Status**: ACTIVE
