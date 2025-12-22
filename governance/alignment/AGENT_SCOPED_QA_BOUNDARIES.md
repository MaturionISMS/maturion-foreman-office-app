# Agent-Scoped QA Boundaries (Canonical Mirror)

**Status**: Authoritative  
**Last Updated**: 2025-12-22  
**Authority**: Corporate Governance Canon  
**Source**: `maturion-foreman-governance` repository  
**Role**: FM enforcement mirror (strict separation of duties)

---

## I. Constitutional Statement

**Agent-scoped QA is a governance invariant.**

Each agent type has exclusive QA responsibility for its domain:
- Builder agents → Builder QA (implementation correctness)
- Governance agents → Governance QA (governance compliance)
- FM agents → FM QA (FM app correctness)

**Cross-agent QA execution is a catastrophic governance violation.**

---

## II. Agent QA Scope Definitions

### Builder QA (Builder Agents Only)

**Scope**: Implementation correctness within agent's responsibility domain

**Includes**:
- ✅ Functional correctness (features work as specified)
- ✅ Schema correctness (data models match architecture)
- ✅ UI correctness (UI matches specifications)
- ✅ Edge case handling (boundary conditions)
- ✅ Integration correctness (APIs and contracts)
- ✅ Unit tests, integration tests, E2E tests
- ✅ Code coverage metrics
- ✅ Performance benchmarks (if specified)

**Excludes**:
- ❌ Governance compliance validation (Governance QA)
- ❌ FM app runtime behavior (FM QA)
- ❌ Cross-repository governance (Governance QA)
- ❌ Architecture validation (Foreman/Governance QA)

**QA Execution Authority**: Builder agents exclusively

**QA Report Format**: Builder QA Report (canonical schema)

**QA Report Location**: Builder repository evidence directory

---

### Governance QA (Governance Agents Only)

**Scope**: Governance compliance and canonical alignment

**Includes**:
- ✅ Governance artifact schema compliance
- ✅ Governance invariant enforcement
- ✅ Policy compliance validation
- ✅ Constitutional rule enforcement
- ✅ Canonical alignment verification
- ✅ Governance drift detection
- ✅ Governance evidence chain validation

**Excludes**:
- ❌ Implementation correctness (Builder QA)
- ❌ Feature functionality (Builder QA)
- ❌ FM app runtime behavior (FM QA)
- ❌ Code quality (Builder QA)

**QA Execution Authority**: Governance agents exclusively

**QA Report Format**: Governance QA Report (canonical schema)

**QA Report Location**: Governance repository evidence directory

---

### FM QA (FM Agents Only)

**Scope**: FM application correctness and runtime behavior

**Includes**:
- ✅ FM app feature correctness
- ✅ FM orchestration logic
- ✅ FM dashboard functionality
- ✅ FM enforcement workflows
- ✅ FM integration with governance
- ✅ FM runtime monitoring
- ✅ FM evidence collection

**Excludes**:
- ❌ Builder implementation QA (Builder QA)
- ❌ Governance policy compliance (Governance QA)
- ❌ Canonical governance validation (Governance QA)
- ❌ ISMS module QA (Builder QA)

**QA Execution Authority**: FM agents exclusively

**QA Report Format**: FM QA Report (canonical schema)

**QA Report Location**: FM repository evidence directory

---

## III. QA Attribution Requirements

### Builder QA Report Attribution

**Required Fields**:
```json
{
  "qa_report_metadata": {
    "agent_type": "builder",
    "agent_id": "ui-builder | api-builder | schema-builder | integration-builder | qa-builder",
    "agent_version": "string",
    "scope": "builder-qa",
    "repository": "repository name",
    "timestamp": "ISO-8601"
  }
}
```

**Enforcement**:
- FM MUST validate `agent_type` = `"builder"`
- FM MUST validate `scope` = `"builder-qa"`
- FM MUST reject if wrong agent type

---

### Governance QA Report Attribution

**Required Fields**:
```json
{
  "qa_report_metadata": {
    "agent_type": "governance",
    "agent_id": "governance-administrator | governance-liaison",
    "agent_version": "string",
    "scope": "governance-qa",
    "repository": "maturion-foreman-governance",
    "timestamp": "ISO-8601"
  }
}
```

**Enforcement**:
- FM MUST validate `agent_type` = `"governance"`
- FM MUST validate `scope` = `"governance-qa"`
- FM MUST reject if wrong agent type

---

### FM QA Report Attribution

**Required Fields**:
```json
{
  "qa_report_metadata": {
    "agent_type": "fm",
    "agent_id": "fm-builder | fm-agent",
    "agent_version": "string",
    "scope": "fm-qa",
    "repository": "maturion-foreman-office-app",
    "timestamp": "ISO-8601"
  }
}
```

**Enforcement**:
- FM MUST validate `agent_type` = `"fm"`
- FM MUST validate `scope` = `"fm-qa"`
- FM MUST reject if wrong agent type

---

## IV. Boundary Violation Detection

### Violation Type 1: Cross-Agent QA Execution

**Definition**: Agent executes QA outside its scope

**Examples**:
- Builder agent runs Governance QA
- Governance agent runs Builder QA
- FM agent runs Builder QA
- Any agent runs another agent's QA

**Detection**:
```python
def detect_cross_agent_qa(qa_report):
    """Detect cross-agent QA boundary violations"""
    
    metadata = qa_report.get('qa_report_metadata', {})
    agent_type = metadata.get('agent_type')
    scope = metadata.get('scope')
    
    # Define valid combinations
    valid_combinations = {
        'builder': ['builder-qa'],
        'governance': ['governance-qa'],
        'fm': ['fm-qa']
    }
    
    # Check if combination is valid
    if agent_type not in valid_combinations:
        return {
            'violation': True,
            'type': 'UNKNOWN_AGENT_TYPE',
            'severity': 'CATASTROPHIC',
            'message': f'Unknown agent type: {agent_type}'
        }
    
    if scope not in valid_combinations[agent_type]:
        return {
            'violation': True,
            'type': 'CROSS_AGENT_QA_EXECUTION',
            'severity': 'CATASTROPHIC',
            'message': f'{agent_type} agent executed {scope} (prohibited)'
        }
    
    return {'violation': False}
```

**Enforcement Action**:
- BLOCK merge immediately
- Escalate to Johan Ras
- Require root cause analysis
- Update agent contract to prevent recurrence

---

### Violation Type 2: Missing Agent Attribution

**Definition**: QA report lacks agent attribution metadata

**Examples**:
- QA report missing `agent_type` field
- QA report missing `scope` field
- QA report missing `agent_id` field

**Detection**:
```python
def detect_missing_attribution(qa_report):
    """Detect missing agent attribution"""
    
    metadata = qa_report.get('qa_report_metadata', {})
    required_fields = ['agent_type', 'agent_id', 'scope', 'repository', 'timestamp']
    
    missing = []
    for field in required_fields:
        if field not in metadata:
            missing.append(field)
    
    if missing:
        return {
            'violation': True,
            'type': 'MISSING_AGENT_ATTRIBUTION',
            'severity': 'HIGH',
            'missing_fields': missing,
            'message': f'QA report missing required attribution: {missing}'
        }
    
    return {'violation': False}
```

**Enforcement Action**:
- BLOCK merge
- Return missing field list
- Require complete attribution

---

### Violation Type 3: Incorrect Repository Attribution

**Definition**: QA report claims execution in wrong repository

**Examples**:
- Builder QA report claims governance repository
- Governance QA report claims builder repository
- FM QA report claims ISMS repository

**Detection**:
```python
def detect_incorrect_repository(qa_report, current_repo):
    """Detect incorrect repository attribution"""
    
    metadata = qa_report.get('qa_report_metadata', {})
    reported_repo = metadata.get('repository')
    agent_type = metadata.get('agent_type')
    
    # Define expected repositories per agent type
    expected_repos = {
        'builder': ['isms-*', 'maturion-isms-*'],  # Any ISMS module repo
        'governance': ['maturion-foreman-governance'],
        'fm': ['maturion-foreman-office-app']
    }
    
    # Check if reported repo matches expected pattern
    if agent_type == 'builder':
        # Builder QA can be in any ISMS module repo
        if not any(reported_repo.startswith(prefix) for prefix in expected_repos['builder']):
            return {
                'violation': True,
                'type': 'INCORRECT_REPOSITORY_ATTRIBUTION',
                'severity': 'HIGH',
                'message': f'Builder QA report claims repository {reported_repo}'
            }
    else:
        if reported_repo not in expected_repos.get(agent_type, []):
            return {
                'violation': True,
                'type': 'INCORRECT_REPOSITORY_ATTRIBUTION',
                'severity': 'HIGH',
                'message': f'{agent_type} QA in wrong repository: {reported_repo}'
            }
    
    return {'violation': False}
```

**Enforcement Action**:
- BLOCK merge
- Log repository mismatch
- Require correct repository attribution

---

## V. QA Report Schema Requirements

### Builder QA Report Schema

**Canonical Fields**:
```json
{
  "qa_report_id": "uuid",
  "qa_report_metadata": {
    "agent_type": "builder",
    "agent_id": "builder-agent-identifier",
    "scope": "builder-qa",
    "repository": "repository-name",
    "timestamp": "ISO-8601"
  },
  "qa_status": "READY | NOT_READY",
  "test_execution": {
    "total_tests": "integer",
    "passed": "integer",
    "failed": "integer",
    "skipped": "integer",
    "pass_rate": "percentage"
  },
  "coverage": {
    "line_coverage": "percentage",
    "branch_coverage": "percentage",
    "function_coverage": "percentage"
  },
  "test_evidence_location": "string (path)",
  "immutable": true
}
```

**Validation**:
- All fields required
- `qa_status` must be explicit
- `immutable` must be `true`
- `pass_rate` must be 100% for READY status

---

### Governance QA Report Schema

**Canonical Fields**:
```json
{
  "qa_report_id": "uuid",
  "qa_report_metadata": {
    "agent_type": "governance",
    "agent_id": "governance-agent-identifier",
    "scope": "governance-qa",
    "repository": "maturion-foreman-governance",
    "timestamp": "ISO-8601"
  },
  "governance_status": "COMPLIANT | NON_COMPLIANT",
  "governance_checks": [
    {
      "check_name": "string",
      "check_type": "schema | invariant | policy | constitutional",
      "status": "PASS | FAIL",
      "details": "string"
    }
  ],
  "governance_evidence_location": "string (path)",
  "immutable": true
}
```

**Validation**:
- All fields required
- `governance_status` must be explicit
- `immutable` must be `true`
- All checks must PASS for COMPLIANT status

---

### FM QA Report Schema

**Canonical Fields**:
```json
{
  "qa_report_id": "uuid",
  "qa_report_metadata": {
    "agent_type": "fm",
    "agent_id": "fm-agent-identifier",
    "scope": "fm-qa",
    "repository": "maturion-foreman-office-app",
    "timestamp": "ISO-8601"
  },
  "fm_status": "OPERATIONAL | NON_OPERATIONAL",
  "fm_checks": [
    {
      "check_name": "string",
      "check_type": "orchestration | enforcement | monitoring | integration",
      "status": "PASS | FAIL",
      "details": "string"
    }
  ],
  "fm_evidence_location": "string (path)",
  "immutable": true
}
```

**Validation**:
- All fields required
- `fm_status` must be explicit
- `immutable` must be `true`
- All checks must PASS for OPERATIONAL status

---

## VI. FM Enforcement Implementation

### PR Gate: Agent Boundary Enforcement

**Workflow**: `.github/workflows/agent-boundary-gate.yml`

**Checks**:
1. Load all QA reports in PR
2. Validate agent attribution for each report
3. Detect cross-agent QA violations
4. Detect missing attribution
5. Detect incorrect repository attribution
6. Block merge if any violation

**Implementation**:
```yaml
name: Agent QA Boundary Enforcement

on:
  pull_request:
    types: [opened, synchronize, reopened]

permissions:
  contents: read
  pull-requests: write

jobs:
  enforce-agent-boundaries:
    name: Enforce Agent-Scoped QA Boundaries
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      
      - name: Find QA Reports
        id: find-reports
        run: |
          # Find all QA report JSON files
          QA_REPORTS=$(find . -name "*qa-report*.json" -o -name "*qa_report*.json")
          echo "reports<<EOF" >> $GITHUB_OUTPUT
          echo "$QA_REPORTS" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT
      
      - name: Validate Agent Boundaries
        run: |
          python governance/scripts/validate_agent_boundaries.py \
            --reports "${{ steps.find-reports.outputs.reports }}" \
            --current-repo "${{ github.repository }}"
      
      - name: Report Violations
        if: failure()
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `
              ❌ **CATASTROPHIC GOVERNANCE VIOLATION**
              
              Agent-scoped QA boundary violation detected.
              
              This is a catastrophic governance violation requiring immediate escalation.
              
              **Required Actions**:
              1. Identify which agent executed wrong QA scope
              2. Remove violating QA report
              3. Execute QA in correct agent scope
              4. Update agent contract to prevent recurrence
              5. Escalate to Johan Ras
              
              **Merge blocked until violation resolved.**
              `
            })
```

---

## VII. Catastrophic Violation Protocol

### When Catastrophic Violation Detected

**Immediate Actions**:
1. BLOCK merge (no exceptions)
2. Create catastrophic failure issue
3. Escalate to Johan Ras
4. Halt all related work
5. Require root cause analysis

**Required Investigation**:
- Which agent executed wrong QA?
- Why did agent boundaries fail?
- How did violation bypass checks?
- What contract updates prevent recurrence?
- What governance updates prevent recurrence?

**Resolution Requirements**:
- Remove violating QA report
- Execute QA in correct scope
- Update agent contracts
- Update governance guardrails
- Verify prevention measures
- Document lessons learned

**Sign-off**: Johan Ras only

---

## VIII. Exception Handling

### NO EXCEPTIONS ALLOWED

Agent-scoped QA boundaries are **governance invariants**.

There are NO valid exceptions to:
- Builder agents running Builder QA only
- Governance agents running Governance QA only
- FM agents running FM QA only

**Temporary Override**: NOT PERMITTED

**Emergency Authorization**: NOT PERMITTED

**Reason**: Cross-agent QA execution breaks fundamental governance separation of duties.

---

## IX. Testing Requirements

### Agent Boundary Enforcement Tests

**Required Tests**:
```python
# Test: Builder QA attributed to builder agent (PASS)
# Test: Governance QA attributed to governance agent (PASS)
# Test: FM QA attributed to FM agent (PASS)
# Test: Builder QA attributed to governance agent (FAIL)
# Test: Governance QA attributed to builder agent (FAIL)
# Test: FM QA attributed to builder agent (FAIL)
# Test: Missing agent attribution (FAIL)
# Test: Incorrect repository attribution (FAIL)
```

**Test Location**: `tests/governance/test_agent_boundary_enforcement.py`

---

## X. Success Criteria

Agent-scoped QA boundaries are successful when:

1. ✅ All Builder QA executed by Builder agents only
2. ✅ All Governance QA executed by Governance agents only
3. ✅ All FM QA executed by FM agents only
4. ✅ Zero cross-agent QA violations ever detected
5. ✅ All QA reports correctly attributed
6. ✅ FM enforces boundaries mechanically
7. ✅ Catastrophic violations escalated immediately

---

## XI. Version and Authority

**Version**: 1.0.0  
**Status**: Authoritative (Canonical Mirror)  
**Canonical Source**: `maturion-foreman-governance/agent-qa/`  
**Last Canonical Sync**: 2025-12-22  
**Owner**: Johan Ras (Authority)  
**Maintainer**: Governance Liaison (FM-scoped)

---

## XII. References

- **Canonical Governance Canon**: https://github.com/MaturionISMS/maturion-foreman-governance
- **PR Gate Requirements**: `/governance/alignment/PR_GATE_REQUIREMENTS_CANON.md`
- **QA Governance**: `/governance/specs/qa-governance.md`
- **Build Philosophy**: `/BUILD_PHILOSOPHY.md`

---

**Separation of duties is governance integrity.**

*END OF AGENT-SCOPED QA BOUNDARIES (CANONICAL MIRROR)*
