# CI Workflow Classification

## Overview

This document provides a canonical classification of all CI workflows in this repository according to FM-CI-HYGIENE-01 standards.

Each workflow is classified as:
- **Hard Gate**: Must pass; code failures block merge
- **Advisory Gate**: Provides guidance; does not block merge
- **Tooling Gate**: Infrastructure-dependent; may have infra failures distinct from code failures

## Workflow Classifications

### 1. Build-to-Green Enforcement (`build-to-green-enforcement.yml`)

**Classification**: Hard Gate

**Purpose**: Enforces Build-to-Green contract by running test suite and checking for test dodging patterns

**Gate Characteristics**:
- Runs complete test suite via `npm test`
- Detects test dodging (`.skip`, `.only`, etc.)
- Checks for DP-RED registry presence
- Phase-gated (can be paused during certain build waves)

**Failure Semantics**:
- Test failures → Code failure → Block merge
- Test dodging detected → Governance violation → Block merge
- Build errors → Code failure → Block merge

**Infrastructure Failure Handling**:
- Test runner unavailable → Infrastructure failure
- Timeout on test execution → Infrastructure failure (if workload-based)
- Dependency installation failure → Infrastructure failure

**Timeout Configuration**:
- Job-level timeout: 15 minutes (sufficient for current test suite ~4s)
- Step-level timeouts: No explicit timeout needed

---

### 2. Agent QA Boundary Enforcement (`agent-boundary-gate.yml`)

**Classification**: Hard Gate

**Purpose**: Enforces agent-scoped QA boundaries (Builder QA by builders, FM QA by FM, Governance QA by governance)

**Gate Characteristics**:
- Validates QA report attribution
- Ensures no cross-agent QA execution
- Checks QA report schema compliance

**Failure Semantics**:
- Wrong agent attribution → Catastrophic governance violation → Block merge + escalation
- Missing QA report (when expected) → Block merge
- Schema invalid → Block merge

**Infrastructure Failure Handling**:
- File system access issues → Infrastructure failure
- JSON parsing errors (malformed files) → Code failure
- Script execution failure → Infrastructure failure

**Timeout Configuration**:
- Job-level timeout: 10 minutes (simple validation only)

---

### 3. Builder QA Gate (`builder-qa-gate.yml`)

**Classification**: Hard Gate

**Purpose**: Validates Builder QA Report presence, schema, and READY status

**Gate Characteristics**:
- Checks for `builder-qa-report.json`
- Validates report schema
- Verifies READY status declaration
- Checks agent attribution and immutability

**Failure Semantics**:
- Builder declares NOT_READY → Expected workflow → Block merge (trust builder)
- Schema invalid → Code failure → Block merge
- Wrong agent attribution → Catastrophic governance violation → Block merge + escalation
- Report not immutable → Code failure → Block merge

**Infrastructure Failure Handling**:
- File system access issues → Infrastructure failure
- JSON parsing errors → Code failure
- Script execution failure → Infrastructure failure

**Timeout Configuration**:
- Job-level timeout: 10 minutes (simple validation only)

---

### 4. FM Architecture Gate (`fm-architecture-gate.yml`)

**Classification**: Hard Gate

**Purpose**: Enforces FM architecture completeness (100%) and drift status (NONE) for FM Agent role only

**Gate Characteristics**:
- Role-based applicability (FM Agent only)
- Validates architecture build artifacts exist
- Checks for 100% completeness
- Verifies drift status = NONE
- Enforces "no agent conclusion while incomplete" rule

**Failure Semantics**:
- Architecture incomplete → Block merge + agent must fix/escalate/halt
- Drift detected → Block merge + escalation
- Missing artifacts → Block merge + agent must fix
- Wrong role → Skip gate (not applicable)

**Infrastructure Failure Handling**:
- File system access issues → Infrastructure failure
- Missing BUILD_ACTIVE file → Code failure (architecture incomplete)
- Invalid validation.md → Code failure

**Timeout Configuration**:
- Job-level timeout: 10 minutes (file-based validation only)

---

### 5. Model Scaling Check (`model-scaling-check.yml`)

**Classification**: Advisory Gate

**Purpose**: Placeholder for future model scaling checks

**Gate Characteristics**:
- Currently minimal/empty
- Intended for future model performance checks

**Failure Semantics**:
- N/A (minimal implementation)

**Infrastructure Failure Handling**:
- N/A

**Timeout Configuration**:
- Job-level timeout: 5 minutes

---

## Gate Applicability Matrix

| Workflow                          | Gate Type       | FM Agent | Builder Agent | Governance Agent |
|-----------------------------------|-----------------|----------|---------------|------------------|
| Build-to-Green Enforcement        | Hard Gate       | ✅ Apply | ✅ Apply      | ⏭️ Skip (docs)   |
| Agent QA Boundary Enforcement     | Hard Gate       | ✅ Apply | ✅ Apply      | ✅ Apply         |
| Builder QA Gate                   | Hard Gate       | ⏭️ Skip  | ✅ Apply      | ⏭️ Skip          |
| FM Architecture Gate              | Hard Gate       | ✅ Apply | ⏭️ Skip       | ⏭️ Skip          |
| Model Scaling Check               | Advisory Gate   | ℹ️ Info  | ℹ️ Info       | ℹ️ Info          |

---

## Failure Handling Protocol

### Code Failures
**Signal**: CI status = `failure`  
**Action**: Agent must fix code, then re-run  
**Escalation**: If unable to fix, escalate with problem + proposed solution  

### Infrastructure Failures
**Signal**: CI status = `success` + explicit infra-failure comment  
**Action**: Retry job (up to 2 retries)  
**Escalation**: If persistent, escalate with infrastructure context  

### Ambiguous States (PROHIBITED)
- `action_required` without clear reason → Infrastructure failure  
- Silent timeouts without status → Infrastructure failure  
- Canceled jobs without explanation → Infrastructure failure  

---

## Timeout Strategy

### General Principles
1. Set timeouts high enough to accommodate normal workload variance
2. Add bounded retries (max 2) for transient failures
3. Explicitly detect and report timeout-based infrastructure failures
4. Never silently timeout

### Current Timeout Configuration

| Workflow                          | Job Timeout | Rationale                                      |
|-----------------------------------|-------------|------------------------------------------------|
| Build-to-Green Enforcement        | 15 minutes  | Sufficient for test suite + npm install        |
| Agent QA Boundary Enforcement     | 10 minutes  | File validation only                           |
| Builder QA Gate                   | 10 minutes  | File validation only                           |
| FM Architecture Gate              | 10 minutes  | File validation only                           |
| Model Scaling Check               | 5 minutes   | Minimal/placeholder                            |

---

## Test Batching Strategy

### Current State
- Test suite completes in ~4 seconds
- 178 tests (13 deselected wave0 tests)
- No batching currently required

### Future Batching Triggers
If test execution time exceeds 5 minutes:
1. Batch by module: `tests/test_<module>_*.py`
2. Batch by marker: `@pytest.mark.<category>`
3. Run batches in parallel using matrix strategy

### Batching Configuration (Future)
```yaml
strategy:
  matrix:
    batch:
      - memory
      - governance
      - watchdog
      - integration
```

---

## Infrastructure Failure Detection

### Detection Patterns

**Pattern 1: Timeout-based**
```yaml
- name: Detect Timeout
  if: cancelled()
  run: |
    echo "::warning::Job cancelled due to timeout - Infrastructure Failure"
    echo "INFRA_FAILURE=timeout" >> $GITHUB_ENV
```

**Pattern 2: Service unavailable**
```yaml
- name: Detect Service Failure
  if: failure()
  run: |
    if grep -q "503" logs.txt || grep -q "Connection refused" logs.txt; then
      echo "INFRA_FAILURE=service_unavailable" >> $GITHUB_ENV
    fi
```

**Pattern 3: Transient network errors**
```yaml
- name: Detect Network Failure
  if: failure()
  run: |
    if grep -q "ETIMEDOUT" logs.txt || grep -q "ECONNRESET" logs.txt; then
      echo "INFRA_FAILURE=network" >> $GITHUB_ENV
    fi
```

---

## PR Comment Templates

### Infrastructure Failure Comment
```markdown
⚠️ **Infrastructure Failure Detected**

**Workflow**: {workflow_name}  
**Job**: {job_name}  
**Failure Type**: {failure_type}  
**Timestamp**: {timestamp}

This is NOT a code failure. The workflow encountered an infrastructure issue.

**Actions Taken**:
- Job marked as success (no code defect)
- Retry attempted: {retry_count}/2
- Infrastructure failure logged

**Next Steps**:
- Review infrastructure failure log: {artifact_link}
- If persistent, escalate to platform team
- Code changes are not blocked by this failure

**Infrastructure Failure Report**: See attached artifact `infra-failure-report.json`
```

---

## Machine-Readable Failure Artifacts

### Infrastructure Failure Schema
```json
{
  "failure_type": "infrastructure",
  "workflow": "build-to-green-enforcement",
  "job": "build-to-green",
  "failure_category": "timeout|service_unavailable|network|disk_space|permission",
  "timestamp": "2025-12-24T17:45:00Z",
  "retry_count": 1,
  "max_retries": 2,
  "error_details": {
    "exit_code": 124,
    "signal": "SIGTERM",
    "stderr": "timeout: sending signal SIGTERM to command 'npm test'"
  },
  "recommended_action": "retry|escalate|investigate"
}
```

---

## References

- FM-CI-HYGIENE-01: CI Batching, Timeout Hardening & Infrastructure Failure Semantics
- FM Build-to-Green Agent Contract: `.github/copilot-instructions.md`
- Agent Role Gate Applicability: `governance/alignment/AGENT_ROLE_GATE_APPLICABILITY_REFERENCE.md`

---

**Document Status**: Canonical  
**Authority**: FM Governance  
**Last Updated**: 2025-12-24  
**Version**: 1.0.0
