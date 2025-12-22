# Governance Ripple Compatibility (Canonical Mirror)

**Status**: Authoritative  
**Last Updated**: 2025-12-22  
**Authority**: Corporate Governance Canon  
**Source**: `maturion-foreman-governance` repository  
**Role**: Bidirectional governance evolution support

---

## I. Constitutional Statement

**Governance must evolve without breaking FM.**

FM governance structures must support:
- **Downward ripple**: Canon updates propagate into FM automatically
- **Upward ripple**: FM-detected lessons learned promote back to governance canon

**This must work without hard-coding assumptions that block evolution.**

---

## II. Governance Ripple Model

```
┌─────────────────────────────────────────┐
│   Canonical Governance (Authoritative)  │
│   maturion-foreman-governance          │
└──────────────┬──────────────────────────┘
               │
               │ Downward Ripple
               ↓ (Canon → FM)
┌──────────────────────────────────────────┐
│   FM Governance (Execution Mirror)       │
│   maturion-foreman-office-app/governance│
└──────────────┬───────────────────────────┘
               │
               │ Upward Ripple
               ↑ (FM → Canon)
               │
┌──────────────────────────────────────────┐
│   FM-Detected Lessons Learned            │
│   Governance Improvement Proposals       │
└──────────────────────────────────────────┘
```

---

## III. Downward Ripple (Canon → FM)

### Purpose

Ensure FM enforcement mirrors canonical governance without delay.

---

### Ripple Trigger Events

Downward ripple triggered when:
- New governance rule added to canon
- Existing governance rule updated
- PR gate requirement changed
- Failure classification added/modified
- QA schema updated
- Compliance control added
- Architecture checklist updated

---

### Detection Mechanism

**Automated Monitoring**:
```python
class CanonicalGovernanceMonitor:
    """Monitor canonical governance for changes"""
    
    def __init__(self):
        self.canonical_repo = 'https://github.com/MaturionISMS/maturion-foreman-governance'
        self.last_sync_commit = self.load_last_sync()
    
    def detect_changes(self):
        """
        Detect changes in canonical governance since last sync.
        
        Returns:
            dict: {
                changes_detected: bool,
                new_commits: list,
                affected_areas: list,
                sync_required: bool
            }
        """
        # Fetch canonical repo latest commit
        latest_commit = self.fetch_latest_canonical_commit()
        
        # Compare with last sync
        if latest_commit == self.last_sync_commit:
            return {
                'changes_detected': False,
                'sync_required': False
            }
        
        # Get commit diff
        commits = self.fetch_commits_since(self.last_sync_commit)
        
        # Analyze affected areas
        affected_areas = self.analyze_affected_areas(commits)
        
        return {
            'changes_detected': True,
            'new_commits': commits,
            'affected_areas': affected_areas,
            'sync_required': True,
            'latest_canonical_commit': latest_commit
        }
    
    def analyze_affected_areas(self, commits):
        """Determine which FM areas affected by canonical changes"""
        affected = []
        
        for commit in commits:
            # Check which files changed
            if self.affects_pr_gates(commit):
                affected.append('pr-gates')
            if self.affects_failure_handling(commit):
                affected.append('failure-handling')
            if self.affects_qa_schemas(commit):
                affected.append('qa-schemas')
            if self.affects_compliance(commit):
                affected.append('compliance')
            if self.affects_architecture(commit):
                affected.append('architecture')
        
        return list(set(affected))
```

**Monitoring Schedule**: Daily automated check

---

### Propagation Workflow

When canonical changes detected:

**Step 1: Change Detection**
- Automated monitor detects canonical change
- Identifies affected FM areas
- Creates governance alignment issue

**Step 2: Impact Analysis**
- Governance Liaison reviews changes
- Determines FM update requirements
- Assesses breaking vs. non-breaking changes
- Estimates update effort

**Step 3: Translation**
- Translate canonical changes to FM constraints
- Update PR gate workflows
- Update governance validation scripts
- Update documentation

**Step 4: Validation**
- Run FM governance validation
- Verify no drift introduced
- Test PR gates with updated requirements
- Verify backward compatibility (if applicable)

**Step 5: Deployment**
- Merge FM governance updates
- Update last_sync_commit reference
- Log propagation in governance memory
- Close alignment issue

**SLA**: 24 hours for critical changes, 1 week for non-critical

---

### Prohibited During Downward Ripple

FM MUST NOT:
- ❌ Reinterpret canonical changes
- ❌ Selectively adopt changes (cherry-picking)
- ❌ Weaken requirements during propagation
- ❌ Delay critical governance updates
- ❌ Fork canonical governance

---

### Downward Ripple Examples

#### Example 1: New PR Gate Added

**Canonical Change**:
```
New PR gate requirement added:
- Gate Name: "security-scan-gate"
- Requirement: All code must pass security scan
- Failure Category: SECURITY_VULNERABILITY_DETECTED
```

**FM Propagation**:
1. Create `.github/workflows/security-scan-gate.yml`
2. Add `SECURITY_VULNERABILITY_DETECTED` to failure classifications
3. Update PR gate requirements documentation
4. Add security scan validation script
5. Test gate with known-good and known-bad cases
6. Deploy within 24 hours

---

#### Example 2: Failure Classification Updated

**Canonical Change**:
```
Failure category updated:
- OLD: ARTIFACT_MISSING (severity: HIGH)
- NEW: ARTIFACT_MISSING (severity: CRITICAL)
- Reason: Missing artifacts block audit trail
```

**FM Propagation**:
1. Update failure handling protocol severity
2. Update escalation logic (now escalates to Johan)
3. Update failure logging (severity field)
4. Update failure handling tests
5. Deploy immediately (critical change)

---

#### Example 3: QA Schema Extended

**Canonical Change**:
```
Builder QA Report schema extended:
- New field: "security_scan_results"
- Required: true
- Type: object
- Purpose: Capture security scan outcomes
```

**FM Propagation**:
1. Update Builder QA Report validation schema
2. Update schema validation scripts
3. Update PR gate to check new field
4. Update documentation
5. Notify builders of schema change
6. Deploy within 1 week (allows builder update time)

---

## IV. Upward Ripple (FM → Canon)

### Purpose

Promote FM-detected lessons learned back to canonical governance to strengthen entire ecosystem.

---

### Ripple Trigger Events

Upward ripple triggered when:
- FM detects systemic gate failure pattern
- FM identifies governance gap
- FM discovers new failure mode
- FM learns prevention measure
- FM detects governance ambiguity
- FM identifies governance conflict

---

### Lesson Learned Detection

**Automated Detection**:
```python
class LessonLearnedDetector:
    """Detect patterns requiring governance evolution"""
    
    def detect_systemic_patterns(self):
        """
        Analyze failure history for systemic patterns.
        
        Returns:
            list: Lessons learned requiring governance update
        """
        lessons = []
        
        # Load failure history
        failures = self.load_failure_history(days=90)
        
        # Detect repeat failures
        repeats = self.detect_repeat_failures(failures)
        if len(repeats) > 0:
            lessons.append({
                'type': 'REPEAT_FAILURE_PATTERN',
                'pattern': repeats,
                'recommendation': 'Strengthen precondition validation',
                'governance_area': 'pr-gates'
            })
        
        # Detect common failure categories
        common_categories = self.detect_common_categories(failures)
        if common_categories:
            lessons.append({
                'type': 'COMMON_FAILURE_CATEGORY',
                'categories': common_categories,
                'recommendation': 'Add preventive gate or improve existing',
                'governance_area': 'failure-prevention'
            })
        
        # Detect governance gaps
        gaps = self.detect_governance_gaps(failures)
        if gaps:
            lessons.append({
                'type': 'GOVERNANCE_GAP',
                'gaps': gaps,
                'recommendation': 'Define new governance rule',
                'governance_area': 'policies'
            })
        
        return lessons
```

**Detection Schedule**: Weekly automated analysis

---

### Propagation Workflow

When lesson learned detected:

**Step 1: Lesson Capture**
- FM detects pattern or gap
- Creates lesson learned record
- Includes evidence (failure records, patterns)
- Proposes governance improvement

**Step 2: FM Validation**
- Verify lesson is generalizable (not FM-specific)
- Verify lesson applies to other repos
- Verify prevention measure is feasible
- Assess impact on existing governance

**Step 3: Proposal Creation**
- Create governance improvement proposal
- Document problem statement
- Provide evidence from FM failures
- Suggest canonical governance change
- Estimate implementation effort

**Step 4: Canonical Submission**
- Submit proposal to `maturion-foreman-governance` repository
- Create issue or pull request
- Include all evidence and analysis
- Request governance review

**Step 5: Wait for Canonical Decision**
- Governance repository reviews proposal
- May accept, reject, or request changes
- Decision is authoritative
- FM implements decision (not proposal)

**Step 6: Implement Canonical Decision**
- If accepted: Wait for downward ripple (canonical change → FM)
- If rejected: Log reason, close proposal
- If modified: Wait for modified version to ripple down

**SLA**: 2 weeks for proposal creation, no SLA for canonical decision

---

### Prohibited During Upward Ripple

FM MUST NOT:
- ❌ Implement proposed change before canonical acceptance
- ❌ Create FM-specific governance workaround
- ❌ Bypass canonical governance process
- ❌ Fork governance to implement proposal
- ❌ Pressure for canonical acceptance

---

### Upward Ripple Examples

#### Example 1: Repeat Failure Pattern

**FM Detection**:
```
Pattern: SCHEMA_VIOLATION for Builder QA Report
Occurrences: 5 in last 30 days
Root Cause: Schema validation too lenient
```

**FM Proposal**:
```
Proposed Governance Change:
- Strengthen Builder QA Report schema validation
- Add required field: test_framework_version
- Add validation: pass_rate must equal 100.0 for READY status
- Rationale: Prevent ambiguous pass rates (99.9% vs 100%)
```

**Canonical Decision**: ACCEPTED (with modification)
- Change accepted with stricter pass_rate validation
- Added to canonical schema
- Ripples down to all repos (downward ripple)

---

#### Example 2: Governance Gap

**FM Detection**:
```
Gap: No gate validates agent identity
Failure: Agent impersonation possible
Risk: Wrong agent could author QA reports
```

**FM Proposal**:
```
Proposed Governance Change:
- Add new PR gate: Agent Identity Verification
- Requirement: All QA reports must include agent signature
- Failure Category: AGENT_IDENTITY_VIOLATION
- Rationale: Prevent agent impersonation
```

**Canonical Decision**: ACCEPTED
- New gate added to canonical PR gates
- Agent signature requirement added to schemas
- Ripples down to all repos

---

#### Example 3: Prevention Measure

**FM Detection**:
```
Lesson: Test debt detection prevented 12 violations
Effectiveness: 100% (all test debt caught before merge)
Recommendation: Make test debt detection mandatory in all repos
```

**FM Proposal**:
```
Proposed Governance Change:
- Elevate test debt detection to constitutional requirement
- Add to canonical PR gates
- Make test debt detection part of Build-to-Green
- Rationale: Proven effectiveness, prevents quality degradation
```

**Canonical Decision**: ACCEPTED
- Test debt detection elevated to constitutional requirement
- Added to all repo PR gates via downward ripple
- Success metric tracked across ecosystem

---

## V. Ripple Compatibility Requirements

### Version Compatibility

**FM Governance Structure Must**:
- ✅ Support versioned canonical references
- ✅ Track last canonical sync commit
- ✅ Detect canonical version changes
- ✅ Handle backward-compatible changes gracefully
- ✅ Flag breaking changes for manual review

**Version Tracking**:
```json
{
  "governance_version": {
    "canonical_repo": "maturion-foreman-governance",
    "last_sync_commit": "commit-sha",
    "last_sync_timestamp": "ISO-8601",
    "fm_governance_version": "1.0.0",
    "canonical_governance_version": "2.3.1",
    "sync_status": "ALIGNED | DRIFT_DETECTED | SYNC_REQUIRED"
  }
}
```

---

### Schema Evolution Support

**Schema Changes Must**:
- Support backward-compatible additions (new optional fields)
- Flag backward-incompatible changes (breaking changes)
- Provide migration path for breaking changes
- Maintain schema version in all artifacts

**Schema Versioning**:
```json
{
  "schema_version": "1.2.0",
  "schema_source": "maturion-foreman-governance",
  "backward_compatible": true,
  "migration_required": false
}
```

---

### Configuration Externalization

**Hard-Coding Prohibitions**:
- ❌ NO hard-coded gate requirements in code
- ❌ NO hard-coded failure categories in code
- ❌ NO hard-coded severity levels in code
- ❌ NO hard-coded escalation rules in code

**Configuration Sources**:
- ✅ PR gate requirements from canonical config
- ✅ Failure categories from canonical taxonomy
- ✅ Severity levels from canonical classification
- ✅ Escalation rules from canonical protocol

**Configuration Location**: `governance/alignment/canonical_config.json`

---

## VI. Ripple Testing

### Downward Ripple Tests

**Test Scenarios**:
1. New PR gate added to canon → FM gate created
2. Failure category severity changed → FM severity updated
3. QA schema extended → FM validation updated
4. Governance rule modified → FM enforcement updated
5. Breaking change introduced → FM flags for review

**Test Location**: `tests/governance/test_downward_ripple.py`

---

### Upward Ripple Tests

**Test Scenarios**:
1. FM detects repeat failure → Proposal created
2. FM identifies governance gap → Gap documented
3. FM learns prevention measure → Proposal submitted
4. Canonical accepts proposal → FM implements via downward ripple
5. Canonical rejects proposal → FM logs and closes

**Test Location**: `tests/governance/test_upward_ripple.py`

---

## VII. Success Criteria

Governance ripple is successful when:

1. ✅ Canonical changes ripple to FM within SLA
2. ✅ FM lessons learned ripple to canon (proposals)
3. ✅ No hard-coded assumptions block evolution
4. ✅ Version compatibility maintained
5. ✅ Schema evolution supported
6. ✅ Configuration externalized
7. ✅ Breaking changes detected and reviewed
8. ✅ Entire ecosystem benefits from FM learnings

---

## VIII. Version and Authority

**Version**: 1.0.0  
**Status**: Authoritative (Canonical Mirror)  
**Canonical Source**: `maturion-foreman-governance/governance-evolution/`  
**Last Canonical Sync**: 2025-12-22  
**Owner**: Johan Ras (Authority)  
**Maintainer**: Governance Liaison (FM-scoped)

---

## IX. References

- **Canonical Governance Canon**: https://github.com/MaturionISMS/maturion-foreman-governance
- **PR Gate Requirements**: `/governance/alignment/PR_GATE_REQUIREMENTS_CANON.md`
- **Governance Alignment Overview**: `/governance/alignment/GOVERNANCE_ALIGNMENT_OVERVIEW.md`
- **Two-Gatekeeper Model**: `/governance/alignment/TWO_GATEKEEPER_MODEL.md`

---

**Governance evolves. FM adapts. Lessons learned propagate.**

*END OF GOVERNANCE RIPPLE COMPATIBILITY (CANONICAL MIRROR)*
