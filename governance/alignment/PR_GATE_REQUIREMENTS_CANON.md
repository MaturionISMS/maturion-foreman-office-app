# PR Gate Requirements (Canonical Mirror)

**Status**: Authoritative  
**Last Updated**: 2025-12-22  
**Authority**: Corporate Governance Canon  
**Source**: `maturion-foreman-governance` repository  
**Role**: FM enforcement mirror (no interpretation, no reinterpretation)

---

## I. Constitutional Statement

**This document mirrors canonical PR gate requirements without modification.**

FM Repository Role:
- ✅ Enforce canonical requirements mechanically
- ✅ Validate artifact presence and schema compliance
- ❌ NEVER reinterpret gate logic
- ❌ NEVER invent gate requirements
- ❌ NEVER weaken gate enforcement
- ❌ NEVER run Builder QA (enforcement-only)

---

## II. Canonical PR Gate Requirements

### Gate 1: Builder QA Report (Source of Truth)

**Requirement**: Builder QA Report MUST exist, be schema-compliant, and declare READY status.

**Canonical Definition**:
- Builder agents run Builder QA exclusively
- Builder QA Report is the **sole source of truth** for build readiness
- PR gates validate report presence and schema, NOT correctness
- PR gates do NOT re-run QA
- PR gates do NOT discover defects
- PR gates do NOT inspect CI logs for QA status

**FM Enforcement**:
```yaml
# What FM MUST check:
- Builder QA Report artifact exists
- Report conforms to canonical schema
- Report declares READY or NOT_READY explicitly
- Report includes required evidence fields
- Report is immutable (not modified post-generation)

# What FM MUST NOT check:
- Whether tests actually passed (trust Builder QA)
- CI log inspection for defects (no CI-discovery)
- Test coverage metrics (Builder's responsibility)
- Code quality scores (Builder's responsibility)
```

**Failure Classification**:
- Missing report → `PR_GATE_BLOCK` (artifact missing)
- Invalid schema → `PR_GATE_BLOCK` (schema violation)
- NOT_READY status → `PR_GATE_BLOCK` (Builder declared not ready)
- Report modified → `PR_GATE_BLOCK` (immutability violation)

**Escalation**:
- FM MUST NOT override Builder QA status
- FM MUST NOT allow merge if report declares NOT_READY
- Emergency override requires Johan authorization only

---

### Gate 2: Agent-Scoped QA Boundary Compliance

**Requirement**: Builder QA MUST be executed by Builder agents only.

**Canonical Definition**:
- Builder agents run Builder QA
- Governance agents run Governance QA
- FM agents run FM QA
- Cross-agent QA execution is **catastrophic governance violation**

**FM Enforcement**:
```yaml
# What FM MUST check:
- Builder QA Report author field = Builder agent
- Governance QA Report author field = Governance agent
- FM QA Report author field = FM agent
- No QA report authored by wrong agent

# What FM MUST NOT check:
- QA test content (out of scope)
- QA methodology (Builder's domain)
- QA coverage (Builder's responsibility)
```

**Failure Classification**:
- Wrong agent authored QA → `CATASTROPHIC_GOVERNANCE_VIOLATION`
- Multiple agents authored same QA → `CATASTROPHIC_GOVERNANCE_VIOLATION`
- Agent attribution missing → `PR_GATE_BLOCK`

**Escalation**:
- Catastrophic violations require immediate escalation to Johan
- Build MUST halt until violation resolved
- Root cause analysis mandatory

---

### Gate 3: Governance Artifact Compliance

**Requirement**: All governance artifacts MUST be schema-compliant and immutable.

**Canonical Definition**:
- Governance artifacts follow canonical schemas
- Evidence is immutable once generated
- Governance invariants enforced mechanically
- FM validates presence and schema only

**FM Enforcement**:
```yaml
# What FM MUST check:
- Evidence schema compliance
- Immutability flag set
- Required governance artifacts present
- Timestamps in ISO 8601 format
- Traceability chain complete

# What FM MUST NOT check:
- Governance artifact content correctness (trust upstream)
- Governance rule interpretation (no reinterpretation)
- Policy compliance logic (enforcement-only)
```

**Failure Classification**:
- Schema violation → `PR_GATE_BLOCK`
- Immutability violation → `PR_GATE_BLOCK`
- Missing artifact → `PR_GATE_BLOCK`
- Invalid timestamp → `PR_GATE_BLOCK`

---

### Gate 4: Architecture Completeness

**Requirement**: Architecture MUST declare 100% completeness and zero drift.

**Canonical Definition**:
- Architecture completeness = 100% (not 99%)
- Drift status = NONE
- Canonical checklist reference required
- Validation report required

**FM Enforcement**:
```yaml
# What FM MUST check:
- validation.md declares "ARCHITECTURE_COMPLETENESS: 100%"
- validation.md declares "DRIFT_STATUS: NONE"
- validation.md includes canonical checklist reference
- drift-report.md declares "DRIFT_STATUS: NONE"
- Required architecture artifacts present

# What FM MUST NOT check:
- Architecture design quality (not a gate concern)
- Architecture implementation approach (Builder's domain)
- Architecture testing strategy (Builder's domain)
```

**Failure Classification**:
- Completeness < 100% → `PR_GATE_BLOCK`
- Drift present → `PR_GATE_BLOCK`
- Missing validation → `PR_GATE_BLOCK`

---

### Gate 5: Build-to-Green Enforcement

**Requirement**: All tests MUST pass 100% before merge.

**Canonical Definition**:
- 100% pass rate (not 99%, not 301/303)
- Zero skipped tests
- Zero test debt
- DP-RED cleared before Build-to-Green phase

**FM Enforcement**:
```yaml
# What FM MUST check:
- Test dodging patterns absent (.skip, .only, .todo)
- DP-RED registry cleared (if Build-to-Green phase)
- Builder QA Report declares 100% pass
- No test debt markers (TODO, FIXME in tests)

# What FM MUST NOT check:
- Test implementation quality (Builder's domain)
- Test coverage percentage (Builder validates)
- Test execution logs (no CI-discovery)
```

**Failure Classification**:
- Test dodging detected → `PR_GATE_BLOCK`
- DP-RED present in Build-to-Green → `PR_GATE_BLOCK`
- Builder QA not 100% → `PR_GATE_BLOCK`

---

## III. Two-Gatekeeper Model

### Gatekeeper 1: Governance Administrator (Agent-Level)

**Role**: Validate governance artifacts and schemas

**Scope**:
- ✅ Schema compliance validation
- ✅ Governance artifact presence
- ✅ Governance invariant enforcement
- ✅ Drift detection
- ❌ NOT Builder QA execution
- ❌ NOT implementation defect discovery

**Authority**: Read-only on Builder QA results

---

### Gatekeeper 2: Foreman App Builder (FM Runtime Layer)

**Role**: Orchestrate enforcement workflows

**Scope**:
- ✅ Aggregate governance signals
- ✅ Enforce merge eligibility
- ✅ Execute PR gate workflows
- ❌ NOT governance rule interpretation
- ❌ NOT gate requirement invention
- ❌ NOT canonical gate weakening

**Authority**: Enforcement only, no override

---

## IV. Enforcement Semantics

### READY Declaration

**Meaning**: Builder declares build ready for merge.

**FM Action**:
- Validate all PR gates pass
- Allow merge if all gates GREEN
- Block merge if any gate RED

**FM MUST NOT**:
- Question Builder's READY declaration
- Re-run Builder QA to verify
- Discover implementation defects

---

### NOT_READY Declaration

**Meaning**: Builder declares build not ready for merge.

**FM Action**:
- Block merge immediately
- No further validation needed
- Builder must fix and redeclare READY

**FM MUST NOT**:
- Override NOT_READY status
- Allow partial merge
- Weaken enforcement

---

### PR_GATE_FAILURE

**Meaning**: PR gate detected violation.

**FM Action**:
- Block merge immediately
- Log failure with canonical classification
- Return detailed failure reason
- Require fix before retry

**FM MUST NOT**:
- Ignore gate failure
- Auto-retry without fix
- Weaken gate to pass

---

## V. Canonical Failure Classifications

All PR gate failures MUST use canonical failure categories:

### ARTIFACT_MISSING
- Required artifact not present
- Builder QA Report missing
- Governance evidence missing

### SCHEMA_VIOLATION
- Artifact schema non-compliant
- Invalid JSON structure
- Missing required fields

### IMMUTABILITY_VIOLATION
- Artifact modified post-generation
- Evidence tampered with
- Timestamp inconsistent

### AGENT_BOUNDARY_VIOLATION
- Wrong agent authored QA
- Cross-agent QA execution detected
- Agent attribution incorrect

### ARCHITECTURE_INCOMPLETE
- Architecture completeness < 100%
- Drift present
- Validation missing

### TEST_DEBT_DETECTED
- Test dodging patterns found
- Skipped tests present
- DP-RED in Build-to-Green phase

### GOVERNANCE_INVARIANT_VIOLATED
- Governance rule broken
- Constitutional requirement violated
- Mandatory field missing

---

## VI. Governance Ripple Support

### Downward Ripple (Canon → FM)

**Mechanism**: Canonical PR gate changes propagate to FM automatically.

**FM Responsibility**:
1. Monitor canonical governance repository
2. Detect PR gate requirement changes
3. Update FM gate workflows within 24 hours
4. Maintain alignment with canon
5. Never weaken requirements during update

**Prohibited**:
- ❌ Delay canonical updates
- ❌ Selectively adopt changes
- ❌ Reinterpret new requirements
- ❌ Weaken requirements during adoption

---

### Upward Ripple (FM → Canon)

**Mechanism**: FM-detected lessons learned promote back to canonical governance.

**FM Responsibility**:
1. Detect systemic gate failures
2. Analyze root cause
3. Propose canonical gate improvements
4. Submit to governance repository
5. Wait for canonical acceptance

**Prohibited**:
- ❌ Implement local gate workarounds
- ❌ Create FM-specific gates
- ❌ Override canonical gates
- ❌ Fork governance requirements

---

## VII. Explicit Prohibitions

FM Repository PR Gates MUST NOT:

1. ❌ **Reintroduce CI-discovery logic**
   - No inspection of CI logs for defects
   - No test result parsing from logs
   - No build failure root cause analysis from CI

2. ❌ **Duplicate PR gate enforcement**
   - No redundant validation of same requirement
   - No alternative enforcement mechanisms
   - No parallel gate implementations

3. ❌ **Reinterpret governance intent**
   - No "smart" gate logic that infers meaning
   - No contextual gate relaxation
   - No subjective pass/fail decisions

4. ❌ **Perform Builder QA**
   - No test execution by FM gates
   - No test coverage analysis by FM gates
   - No code quality checks by FM gates

5. ❌ **Act as alternative authority**
   - No override of canonical requirements
   - No FM-specific gate creation
   - No governance rule modification

---

## VIII. Success Criteria

PR gate enforcement is successful when:

1. ✅ FM gates mirror canonical requirements exactly
2. ✅ All gate failures use canonical classifications
3. ✅ No CI-discovery logic exists
4. ✅ No duplicate enforcement exists
5. ✅ Builder QA Reports trusted as source of truth
6. ✅ Agent boundaries enforced mechanically
7. ✅ Governance updates ripple cleanly
8. ✅ Zero governance reinterpretation

---

## IX. Integration with FM Workflows

### Current Workflows

**`.github/workflows/build-to-green-enforcement.yml`**
- Aligns with Gate 5 (Build-to-Green)
- Validates test dodging patterns
- Enforces DP-RED governance
- Status: Canonical-aligned ✅

**`.github/workflows/fm-architecture-gate.yml`**
- Aligns with Gate 4 (Architecture Completeness)
- Validates 100% completeness
- Enforces zero drift
- Status: Canonical-aligned ✅

### Required New Workflows

**`.github/workflows/builder-qa-gate.yml`** (Gate 1)
- Validate Builder QA Report presence
- Enforce schema compliance
- Check READY/NOT_READY status
- No Builder QA execution

**`.github/workflows/agent-boundary-gate.yml`** (Gate 2)
- Validate agent attribution
- Detect cross-agent QA violations
- Enforce agent-scoped QA

**`.github/workflows/governance-artifact-gate.yml`** (Gate 3)
- Validate governance schema compliance
- Check immutability flags
- Verify traceability chain

---

## X. Evidence and Audit Trail

### Required Evidence

For each PR gate execution, record:

```json
{
  "gate_execution_id": "uuid",
  "gate_name": "builder-qa-gate",
  "timestamp": "ISO-8601",
  "pr_number": "integer",
  "commit_sha": "string",
  "gate_status": "PASS | FAIL | BLOCKED",
  "failure_classification": "canonical category or null",
  "artifacts_validated": [
    {
      "artifact_name": "builder-qa-report.json",
      "present": true,
      "schema_valid": true,
      "immutable": true
    }
  ],
  "enforcement_decision": "ALLOW_MERGE | BLOCK_MERGE",
  "canonical_reference": "maturion-foreman-governance commit SHA"
}
```

### Audit Trail Requirements

- All gate executions logged
- All failures classified canonically
- All enforcement decisions recorded
- Canonical alignment verified per execution

---

## XI. Version and Authority

**Version**: 1.0.0  
**Status**: Authoritative (Canonical Mirror)  
**Canonical Source**: `maturion-foreman-governance/pr-gates/`  
**Last Canonical Sync**: 2025-12-22  
**Next Sync Check**: Weekly automated  
**Owner**: Johan Ras (Authority)  
**Maintainer**: Governance Liaison (FM-scoped)

---

## XII. References

- **Canonical Governance Canon**: https://github.com/MaturionISMS/maturion-foreman-governance
- **Build Philosophy**: `/BUILD_PHILOSOPHY.md`
- **Governance Alignment Overview**: `/governance/alignment/GOVERNANCE_ALIGNMENT_OVERVIEW.md`
- **Two-Gatekeeper Model**: `/governance/alignment/TWO_GATEKEEPER_MODEL.md`
- **Agent-Scoped QA Boundaries**: `/governance/alignment/AGENT_SCOPED_QA_BOUNDARIES.md`

---

**One canon. Two gatekeepers. Zero reinterpretation.**

*END OF PR GATE REQUIREMENTS (CANONICAL MIRROR)*
