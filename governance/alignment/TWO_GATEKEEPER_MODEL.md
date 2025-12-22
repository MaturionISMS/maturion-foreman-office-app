# Two-Gatekeeper Model (Canonical Mirror)

**Status**: Authoritative  
**Last Updated**: 2025-12-22  
**Authority**: Corporate Governance Canon  
**Source**: `maturion-foreman-governance` repository  
**Role**: Dual gatekeeper enforcement model

---

## I. Constitutional Statement

**FM governance operates under a dual gatekeeper model.**

Neither gatekeeper may override the other.  
Both defer to canonical governance.  
Neither may weaken, bypass, or reinterpret canonical requirements.

---

## II. Gatekeeper Roles

### Gatekeeper 1: Governance Administrator (Agent-Level)

**Identity**: Governance Liaison (FM-scoped)

**Responsibility**: Maintain governance canon awareness and validate governance artifacts

**Authority**: Read-only on governance canon, write access to FM execution configuration

**Scope**:
- ✅ Monitor `maturion-foreman-governance` repository for changes
- ✅ Translate canonical governance into FM execution constraints
- ✅ Validate governance artifact schema compliance
- ✅ Detect governance drift
- ✅ Ensure FM remains aligned with canonical governance

**Prohibited Actions**:
- ❌ Create new governance rules
- ❌ Modify governance meaning
- ❌ Override governance canon
- ❌ Run Builder QA
- ❌ Discover implementation defects
- ❌ Reinterpret governance intent

**Escalation Path**: Johan Ras (for governance ambiguities or conflicts)

---

### Gatekeeper 2: Foreman App Builder (FM Runtime Layer)

**Identity**: FM Builder Agent

**Responsibility**: Orchestrate enforcement workflows and enforce merge eligibility

**Authority**: Enforcement-only, zero authority to modify governance

**Scope**:
- ✅ Execute PR gate workflows
- ✅ Aggregate governance signals from Gatekeeper 1
- ✅ Enforce merge / handover eligibility
- ✅ Validate Builder QA Report presence and schema
- ✅ Block merge if any gate RED

**Prohibited Actions**:
- ❌ Modify governance rules
- ❌ Reinterpret governance requirements
- ❌ Weaken canonical gates
- ❌ Bypass canonical gates
- ❌ Run Builder QA
- ❌ Discover implementation defects
- ❌ Override Builder QA READY/NOT_READY status

**Escalation Path**: Johan Ras (for blockers or governance conflicts)

---

## III. Gatekeeper Interaction Model

### Governance Change Flow

```
Canonical Governance Update (maturion-foreman-governance)
                ↓
        Gatekeeper 1 detects change
                ↓
        Gatekeeper 1 translates to FM constraints
                ↓
        Gatekeeper 1 updates PR gate workflows
                ↓
        Gatekeeper 2 executes updated workflows
                ↓
        Merge eligibility enforced with new constraints
```

**Key Invariants**:
- Gatekeeper 1 translates, does NOT interpret
- Gatekeeper 2 enforces, does NOT decide
- Neither weakens canonical requirements
- Neither creates local governance

---

### PR Merge Flow

```
PR opened
    ↓
Gatekeeper 1 validates governance artifacts
    ↓ (schema, immutability, traceability)
    ↓
Gatekeeper 1 signals: GOVERNANCE_VALID or GOVERNANCE_INVALID
    ↓
Gatekeeper 2 validates Builder QA Report
    ↓ (presence, schema, READY status)
    ↓
Gatekeeper 2 aggregates signals
    ↓
ALL GATES GREEN? → ALLOW MERGE
ANY GATE RED? → BLOCK MERGE
```

**Key Invariants**:
- Gatekeeper 1 validates governance only
- Gatekeeper 2 validates Builder QA only
- Both must approve for merge
- Neither may override the other

---

### Failure Escalation Flow

```
PR Gate Failure Detected
        ↓
    Which Gatekeeper?
        ↓
    ┌───┴───┐
    ↓       ↓
Gatekeeper 1    Gatekeeper 2
(Governance)    (Builder QA)
    ↓               ↓
Governance      Builder QA
violation       not READY
    ↓               ↓
Log canonical   Trust Builder
classification  declaration
    ↓               ↓
    └───┬───┘
        ↓
    BLOCK MERGE
        ↓
Return detailed failure reason
        ↓
Require fix before retry
```

**Key Invariants**:
- Failures classified canonically
- No subjective pass/fail decisions
- No "smart" failure handling
- No automatic retry without fix

---

## IV. Gatekeeper 1 Implementation

### Governance Artifact Validation

**Location**: `governance/scripts/validate_governance_artifacts.py`

**Responsibilities**:
1. Load all governance artifacts from PR
2. Validate schema compliance (EVIDENCE_SCHEMA_CANON.json)
3. Check immutability flags
4. Verify traceability chain
5. Validate timestamps (ISO 8601)
6. Check governance invariants

**Implementation**:
```python
class GovernanceAdministrator:
    """Gatekeeper 1: Governance artifact validator"""
    
    def __init__(self):
        self.canon_schema_path = Path('governance/specs/EVIDENCE_SCHEMA_CANON.json')
        self.governance_repo_url = 'https://github.com/MaturionISMS/maturion-foreman-governance'
    
    def validate_pr_governance(self, pr_number):
        """
        Validate all governance artifacts in PR.
        
        Returns:
            dict: {
                status: 'GOVERNANCE_VALID' | 'GOVERNANCE_INVALID',
                errors: list,
                warnings: list,
                artifacts_validated: list
            }
        """
        errors = []
        warnings = []
        artifacts = []
        
        # 1. Find all governance artifacts in PR
        governance_artifacts = self.find_governance_artifacts(pr_number)
        
        # 2. Validate each artifact
        for artifact_path in governance_artifacts:
            result = self.validate_artifact(artifact_path)
            artifacts.append({
                'path': artifact_path,
                'valid': result['valid'],
                'errors': result.get('errors', [])
            })
            
            if not result['valid']:
                errors.extend(result['errors'])
            
            if 'warnings' in result:
                warnings.extend(result['warnings'])
        
        # 3. Overall status
        status = 'GOVERNANCE_VALID' if len(errors) == 0 else 'GOVERNANCE_INVALID'
        
        return {
            'status': status,
            'errors': errors,
            'warnings': warnings,
            'artifacts_validated': artifacts,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
    
    def validate_artifact(self, artifact_path):
        """Validate single governance artifact"""
        with open(artifact_path) as f:
            artifact = json.load(f)
        
        # Use governance gate validation
        gate = GovernanceGate()
        artifact_type = self.detect_artifact_type(artifact)
        result = gate.validate_evidence(artifact, artifact_type)
        
        return result
    
    def detect_artifact_type(self, artifact):
        """Detect governance artifact type from structure"""
        if 'qa_report_metadata' in artifact:
            return 'qa-report'
        elif 'evidence_metadata' in artifact:
            return 'evidence'
        elif 'failure_record' in artifact:
            return 'failure-record'
        else:
            return 'unknown'
```

**Exit Codes**:
- 0 = GOVERNANCE_VALID (all artifacts pass)
- 1 = GOVERNANCE_INVALID (one or more artifacts fail)

---

### Governance Drift Detection

**Responsibility**: Detect when FM governance drifts from canonical governance

**Implementation**:
```python
def detect_governance_drift(self):
    """
    Detect drift between FM governance and canonical governance.
    
    Returns:
        dict: {
            drift_detected: bool,
            drift_items: list,
            canonical_version: string,
            fm_version: string
        }
    """
    drift_items = []
    
    # 1. Fetch canonical governance version
    canonical_version = self.get_canonical_governance_version()
    
    # 2. Get FM governance version
    fm_version = self.get_fm_governance_version()
    
    # 3. Compare versions
    if canonical_version != fm_version:
        drift_items.append({
            'type': 'VERSION_MISMATCH',
            'canonical': canonical_version,
            'fm': fm_version,
            'severity': 'HIGH'
        })
    
    # 4. Compare PR gate requirements
    canonical_gates = self.get_canonical_gate_requirements()
    fm_gates = self.get_fm_gate_requirements()
    
    gate_diff = self.compare_gate_requirements(canonical_gates, fm_gates)
    if gate_diff:
        drift_items.extend(gate_diff)
    
    return {
        'drift_detected': len(drift_items) > 0,
        'drift_items': drift_items,
        'canonical_version': canonical_version,
        'fm_version': fm_version,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
```

**Action on Drift**:
- Log drift detection
- Create governance alignment issue
- Block merge if drift HIGH severity
- Escalate to Johan if drift unresolvable

---

## V. Gatekeeper 2 Implementation

### Builder QA Report Validation

**Location**: `.github/workflows/builder-qa-gate.yml`

**Responsibilities**:
1. Find Builder QA Report in PR
2. Validate report presence
3. Validate report schema
4. Check READY/NOT_READY status
5. Validate agent attribution
6. Block merge if NOT_READY or invalid

**Implementation**:
```yaml
name: Builder QA Gate

on:
  pull_request:
    types: [opened, synchronize, reopened]

permissions:
  contents: read
  pull-requests: write

jobs:
  validate-builder-qa:
    name: Validate Builder QA Report
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      
      - name: Find Builder QA Report
        id: find-report
        run: |
          # Find Builder QA Report
          REPORT=$(find . -name "builder-qa-report.json" | head -1)
          
          if [ -z "$REPORT" ]; then
            echo "❌ Builder QA Report not found"
            echo "found=false" >> $GITHUB_OUTPUT
            exit 1
          fi
          
          echo "report=$REPORT" >> $GITHUB_OUTPUT
          echo "found=true" >> $GITHUB_OUTPUT
          echo "✅ Builder QA Report found: $REPORT"
      
      - name: Validate Builder QA Report Schema
        run: |
          python governance/scripts/validate_builder_qa_report.py \
            --report "${{ steps.find-report.outputs.report }}"
      
      - name: Check READY Status
        run: |
          QA_STATUS=$(jq -r '.qa_status' "${{ steps.find-report.outputs.report }}")
          
          echo "Builder QA Status: $QA_STATUS"
          
          if [ "$QA_STATUS" != "READY" ]; then
            echo "❌ Builder QA declares NOT_READY"
            echo "Merge blocked until Builder declares READY"
            exit 1
          fi
          
          echo "✅ Builder QA declares READY"
      
      - name: Validate Agent Attribution
        run: |
          AGENT_TYPE=$(jq -r '.qa_report_metadata.agent_type' "${{ steps.find-report.outputs.report }}")
          SCOPE=$(jq -r '.qa_report_metadata.scope' "${{ steps.find-report.outputs.report }}")
          
          if [ "$AGENT_TYPE" != "builder" ]; then
            echo "❌ CATASTROPHIC: QA report not authored by builder agent"
            exit 1
          fi
          
          if [ "$SCOPE" != "builder-qa" ]; then
            echo "❌ CATASTROPHIC: QA report scope not builder-qa"
            exit 1
          fi
          
          echo "✅ Agent attribution valid"
      
      - name: Report Success
        if: success()
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `
              ✅ **Builder QA Gate PASSED**
              
              - Builder QA Report present and valid
              - Report declares READY
              - Agent attribution correct
              - Schema compliant
              
              Gatekeeper 2 approves merge.
              `
            })
      
      - name: Report Failure
        if: failure()
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `
              ❌ **Builder QA Gate BLOCKED**
              
              Gatekeeper 2 blocks merge.
              
              **Possible Reasons**:
              - Builder QA Report missing
              - Report declares NOT_READY
              - Report schema invalid
              - Agent attribution incorrect
              
              Review workflow logs for details.
              `
            })
```

---

### Enforcement Aggregation

**Responsibility**: Aggregate signals from both gatekeepers and decide merge eligibility

**Implementation**:
```python
class EnforcementAggregator:
    """Gatekeeper 2: Enforcement orchestrator"""
    
    def aggregate_gate_signals(self, pr_number):
        """
        Aggregate signals from both gatekeepers.
        
        Returns:
            dict: {
                merge_eligible: bool,
                gatekeeper_1_status: string,
                gatekeeper_2_status: string,
                blocking_gates: list,
                timestamp: string
            }
        """
        # Get Gatekeeper 1 signal
        gk1 = GovernanceAdministrator()
        gk1_result = gk1.validate_pr_governance(pr_number)
        gk1_status = gk1_result['status']
        
        # Get Gatekeeper 2 signal
        gk2_result = self.validate_builder_qa(pr_number)
        gk2_status = gk2_result['status']
        
        # Aggregate
        blocking_gates = []
        
        if gk1_status != 'GOVERNANCE_VALID':
            blocking_gates.append({
                'gatekeeper': 1,
                'gate': 'governance-artifacts',
                'reason': 'Governance artifacts invalid',
                'errors': gk1_result['errors']
            })
        
        if gk2_status != 'BUILDER_QA_READY':
            blocking_gates.append({
                'gatekeeper': 2,
                'gate': 'builder-qa',
                'reason': 'Builder QA not ready',
                'errors': gk2_result['errors']
            })
        
        # Decision
        merge_eligible = len(blocking_gates) == 0
        
        return {
            'merge_eligible': merge_eligible,
            'gatekeeper_1_status': gk1_status,
            'gatekeeper_2_status': gk2_status,
            'blocking_gates': blocking_gates,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
```

---

## VI. Gatekeeper Boundaries

### What Gatekeeper 1 CAN Do

- ✅ Validate governance artifact schemas
- ✅ Check immutability flags
- ✅ Verify traceability chains
- ✅ Detect governance drift
- ✅ Translate canonical updates to FM constraints
- ✅ Update PR gate workflows (configuration only)

### What Gatekeeper 1 CANNOT Do

- ❌ Run Builder QA
- ❌ Validate implementation correctness
- ❌ Discover defects
- ❌ Override Builder QA status
- ❌ Create new governance rules
- ❌ Weaken canonical requirements

---

### What Gatekeeper 2 CAN Do

- ✅ Validate Builder QA Report presence
- ✅ Check Builder QA Report schema
- ✅ Read READY/NOT_READY status
- ✅ Aggregate gatekeeper signals
- ✅ Enforce merge eligibility
- ✅ Block merge if gates RED

### What Gatekeeper 2 CANNOT Do

- ❌ Run Builder QA
- ❌ Re-run tests
- ❌ Override Builder QA READY/NOT_READY
- ❌ Inspect CI logs for defects
- ❌ Modify governance rules
- ❌ Weaken PR gate requirements

---

## VII. Override and Exception Handling

### NO OVERRIDE BY GATEKEEPERS

Neither gatekeeper has authority to:
- Override canonical governance
- Bypass PR gate requirements
- Weaken enforcement
- Grant temporary exceptions

### JOHAN AUTHORIZATION ONLY

Only Johan Ras may authorize:
- Emergency governance override (temporary, bounded, logged)
- Temporary gate bypass (specific instance, tracked, cleanup required)
- Governance rule exception (explicit, time-limited, audited)

**Override Characteristics**:
- Temporary (single instance)
- Explicit (clearly documented)
- Logged (full audit trail)
- Tracked (cleanup issue created)
- Bounded (48-hour cleanup deadline)

---

## VIII. Success Criteria

Two-gatekeeper model is successful when:

1. ✅ Gatekeeper 1 validates governance artifacts only
2. ✅ Gatekeeper 2 validates Builder QA only
3. ✅ Neither gatekeeper overrides the other
4. ✅ Both gatekeepers defer to canonical governance
5. ✅ Merge requires both gatekeepers to approve
6. ✅ No governance reinterpretation occurs
7. ✅ No Builder QA execution by gatekeepers
8. ✅ All overrides by Johan only

---

## IX. Version and Authority

**Version**: 1.0.0  
**Status**: Authoritative (Canonical Mirror)  
**Canonical Source**: `maturion-foreman-governance/enforcement/`  
**Last Canonical Sync**: 2025-12-22  
**Owner**: Johan Ras (Authority)  
**Maintainer**: Governance Liaison (FM-scoped)

---

## X. References

- **Canonical Governance Canon**: https://github.com/MaturionISMS/maturion-foreman-governance
- **PR Gate Requirements**: `/governance/alignment/PR_GATE_REQUIREMENTS_CANON.md`
- **Agent-Scoped QA Boundaries**: `/governance/alignment/AGENT_SCOPED_QA_BOUNDARIES.md`
- **Governance Alignment Overview**: `/governance/alignment/GOVERNANCE_ALIGNMENT_OVERVIEW.md`

---

**Two gatekeepers. Neither overrides. Both enforce.**

*END OF TWO-GATEKEEPER MODEL (CANONICAL MIRROR)*
