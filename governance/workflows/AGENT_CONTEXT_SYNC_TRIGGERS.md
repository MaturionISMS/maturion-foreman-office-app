# Agent Context Sync Trigger Events

**Status**: Operational  
**Version**: 1.0.0  
**Authority**: Corporate Governance Canon  
**Last Updated**: 2025-12-24

---

## I. Purpose

This document defines all trigger events that initiate agent context synchronisation workflows.

**Core Principle**: Agent context sync must be triggered by canonical governance changes, not by arbitrary events or agent behavior.

---

## II. Trigger Event Categories

### Category 1: Governance Rule Changes

**Trigger When**:
- New governance rule added to canonical governance
- Existing governance rule modified
- Governance rule deprecated or removed
- Governance rule priority changed

**Examples**:
- Governance Supremacy Rule updated
- Zero Test Debt rule strengthened
- Design Freeze Rule clarified
- Build-to-Green enforcement modified

**Affected Agents**:
- `foreman.agent.md` (primary)
- `ForemanApp-agent.md`
- `governance-liaison.md`

**Priority**: HIGH (for breaking changes) | MEDIUM (for additions)

---

### Category 2: Agent Contract Template Updates

**Trigger When**:
- Agent contract structure changed
- New required field added to contract
- Field semantics modified
- Contract versioning scheme updated

**Examples**:
- New `governance_sync` section added to agent frontmatter
- `authority` field semantics changed
- `escalation_triggers` format updated
- Contract validation rules modified

**Affected Agents**: ALL agents

**Priority**: CRITICAL (if breaking) | HIGH (if additive)

---

### Category 3: Policy Updates

**Trigger When**:
- New policy introduced in canonical governance
- Policy requirements changed
- Policy scope expanded or reduced
- Policy enforcement mechanism changed

**Examples**:
- New privacy guardrail policy
- APP_DESCRIPTION_REQUIREMENT_POLICY updated
- Change policy modified
- Security escalation policy updated

**Affected Agents**:
- `foreman.agent.md`
- Builder agents (if build policies affected)
- `governance-liaison.md` (all policy changes)

**Priority**: HIGH (for enforcement policies) | MEDIUM (for guidance policies)

---

### Category 4: Compliance Control Changes

**Trigger When**:
- New compliance control added
- Control mapping updated
- Control evidence requirements changed
- Control validation logic modified

**Examples**:
- New ISO 27001 control mapped
- NIST CSF control updated
- GDPR compliance check added
- Audit evidence schema changed

**Affected Agents**:
- `foreman.agent.md` (compliance monitoring)
- `governance-liaison.md` (compliance alignment)

**Priority**: HIGH

---

### Category 5: Architecture Standard Changes

**Trigger When**:
- Architecture checklist updated
- Naming conventions modified
- Folder structure requirements changed
- Module template updated
- True North specification changed

**Examples**:
- Architecture Design Checklist section added
- MARS template field added
- Versioning rules updated
- Integration pattern standardized

**Affected Agents**:
- `foreman.agent.md` (architecture validation)
- `ForemanApp-agent.md` (architecture enforcement)
- Builder agents (if standards affect builds)

**Priority**: MEDIUM (most cases) | HIGH (if breaking)

---

### Category 6: QA and QA-of-QA Changes

**Trigger When**:
- QA governance rules updated
- Minimum coverage requirements changed
- Test category definitions modified
- QA-of-QA criteria updated
- Builder QA Report schema changed

**Examples**:
- Minimum test coverage increased
- New test category added
- QA evidence schema extended
- Zero Test Debt rule strengthened

**Affected Agents**:
- `foreman.agent.md` (QA oversight)
- Builder agents (QA execution)

**Priority**: HIGH

---

### Category 7: Memory Model Changes

**Trigger When**:
- Memory schema updated
- Memory governance rules changed
- Memory fabric structure modified
- Memory sync contract updated

**Examples**:
- Memory entry schema version incremented
- New memory category added
- Memory retention policy changed
- Memory read/write boundaries updated

**Affected Agents**:
- `foreman.agent.md` (memory management)
- FM agents (memory operations)

**Priority**: MEDIUM (if backward compatible) | HIGH (if breaking)

---

### Category 8: Build Philosophy Updates

**Trigger When**:
- Build Philosophy document updated
- Core build principles modified
- Build sequencing rules changed
- Build-to-Green rule updated

**Examples**:
- One-Time Build Correctness principle clarified
- Zero Regression definition updated
- Build sequencing constraints added
- Builder coordination protocol modified

**Affected Agents**: ALL agents

**Priority**: CRITICAL (Build Philosophy is supreme authority)

---

## III. Trigger Event Detection

### 3.1 Detection Methods

**Method 1: Canonical Repository Monitoring (Automated)**
```python
class CanonicalGovernanceMonitor:
    """
    Monitor maturion-foreman-governance repository for changes.
    """
    
    def detect_trigger_events(self):
        """
        Detect trigger events from canonical repository changes.
        
        Returns:
            list[TriggerEvent]: Detected trigger events
        """
        triggers = []
        
        # Fetch latest canonical state
        canonical_state = self.fetch_canonical_state()
        last_sync_state = self.load_last_sync_state()
        
        # Detect changes by category
        governance_changes = self.detect_governance_changes(
            canonical_state, last_sync_state
        )
        if governance_changes:
            triggers.append(self.create_trigger(
                category='GOVERNANCE_RULE_CHANGE',
                changes=governance_changes,
                priority='HIGH'
            ))
        
        contract_changes = self.detect_contract_changes(
            canonical_state, last_sync_state
        )
        if contract_changes:
            triggers.append(self.create_trigger(
                category='CONTRACT_TEMPLATE_UPDATE',
                changes=contract_changes,
                priority='CRITICAL' if self.is_breaking(contract_changes) else 'HIGH'
            ))
        
        policy_changes = self.detect_policy_changes(
            canonical_state, last_sync_state
        )
        if policy_changes:
            triggers.append(self.create_trigger(
                category='POLICY_UPDATE',
                changes=policy_changes,
                priority='HIGH'
            ))
        
        # Continue for all categories...
        
        return triggers
```

**Monitoring Schedule**: Daily automated check at 00:00 UTC

---

**Method 2: Manual Trigger (Admin-Initiated)**
```bash
python3 scripts/sync-agent-context.py \
    --manual \
    --trigger-category "GOVERNANCE_RULE_CHANGE" \
    --trigger-reason "Post-incident governance update" \
    --canonical-commit abc123def
```

**Use Cases**:
- Emergency governance updates
- Missed automatic detection
- Post-incident realignment
- Governance drift correction

---

**Method 3: Scheduled Audit Trigger (Automated)**
```python
class ScheduledAuditTrigger:
    """
    Periodic audit to detect missed governance changes.
    """
    
    def perform_audit(self):
        """
        Weekly audit to ensure no governance drift.
        
        Returns:
            list[TriggerEvent]: Any missed trigger events
        """
        # Compare full canonical state with FM state
        canonical_full = self.fetch_full_canonical_state()
        fm_full = self.load_full_fm_state()
        
        # Detect any drift
        drift = self.detect_governance_drift(canonical_full, fm_full)
        
        if drift:
            return [self.create_trigger(
                category='GOVERNANCE_DRIFT_DETECTED',
                changes=drift,
                priority='HIGH'
            )]
        
        return []
```

**Audit Schedule**: Weekly on Sunday at 00:00 UTC

---

### 3.2 Trigger Event Schema

See: `governance/events/AGENT_SYNC_TRIGGER_EVENT_SCHEMA.json`

**Structure**:
```json
{
  "event_id": "trigger-001",
  "timestamp": "2025-12-24T10:00:00Z",
  "trigger_category": "GOVERNANCE_RULE_CHANGE | CONTRACT_TEMPLATE_UPDATE | ...",
  "priority": "LOW | MEDIUM | HIGH | CRITICAL",
  "canonical_commit": "abc123def",
  "canonical_repository": "MaturionISMS/maturion-foreman-governance",
  "governance_area": "governance/policies/governance-supremacy-rule.md",
  "change_type": "ADDED | MODIFIED | REMOVED | DEPRECATED",
  "change_description": "Human-readable description of what changed",
  "affected_files": [
    "governance/policies/governance-supremacy-rule.md",
    "governance/policies/zero-test-debt-constitutional-rule.md"
  ],
  "breaking_change": true,
  "backward_compatible": false,
  "estimated_impact": {
    "affected_agents_count": 3,
    "update_complexity": "LOW | MEDIUM | HIGH",
    "approval_required": true,
    "human_review_required": true
  }
}
```

---

## IV. Trigger Priority Levels

### Priority: CRITICAL

**Definition**: Immediate action required. Affects fundamental agent behavior or governance authority.

**Examples**:
- Build Philosophy updated
- Agent contract structure changed (breaking)
- Governance Supremacy Rule modified

**Response Time**: Immediate (< 1 hour)

**Approval**: Human (Johan) required

---

### Priority: HIGH

**Definition**: Important change requiring prompt attention. Affects governance enforcement or compliance.

**Examples**:
- New governance rule added
- Compliance control modified
- QA governance updated
- Breaking policy change

**Response Time**: 24 hours

**Approval**: Admin-agent required (FM agents), auto-approve allowed (builders, if additive)

---

### Priority: MEDIUM

**Definition**: Standard governance update. Non-breaking, additive changes.

**Examples**:
- Architecture standard clarified
- Policy guidance added
- Memory model extended (backward compatible)
- Non-breaking contract field added

**Response Time**: 1 week

**Approval**: Auto-approve allowed (if validation passes)

---

### Priority: LOW

**Definition**: Minor documentation or clarification. No functional impact.

**Examples**:
- Governance documentation typo fixed
- Example added to policy
- Formatting updated

**Response Time**: 2 weeks

**Approval**: Auto-approve

---

## V. Trigger Event Workflow

### 5.1 Event Flow

```
┌────────────────────────┐
│  Trigger Detected      │
└────────┬───────────────┘
         │
         ↓
┌────────────────────────┐
│  Validate Trigger      │
│  - Schema valid?       │
│  - Priority set?       │
│  - Canonical ref?      │
└────────┬───────────────┘
         │
         ↓ YES
┌────────────────────────┐
│  Log Trigger Event     │
│  - Event file created  │
│  - Audit log updated   │
└────────┬───────────────┘
         │
         ↓
┌────────────────────────┐
│  Initiate Sync         │
│  - Start workflow      │
│  - Notify admins       │
└────────────────────────┘
```

### 5.2 Trigger Validation

**Validation Checks**:
1. ✅ Event ID is unique
2. ✅ Timestamp is valid ISO-8601
3. ✅ Trigger category is recognized
4. ✅ Priority is set
5. ✅ Canonical commit SHA is valid
6. ✅ Canonical repository is accessible
7. ✅ Governance area exists
8. ✅ Change type is valid
9. ✅ Affected files list is not empty

**On Validation Failure**:
- Log validation error
- Create incident report
- Escalate to admin
- Do NOT proceed with sync

---

## VI. Trigger Event Storage

### 6.1 Storage Location

**File**: `governance/events/agent-sync-triggers/<year>/<month>/trigger-<event-id>.json`

**Example**: `governance/events/agent-sync-triggers/2025/12/trigger-001.json`

### 6.2 Storage Structure

```
governance/events/agent-sync-triggers/
├── 2025/
│   ├── 12/
│   │   ├── trigger-001.json
│   │   ├── trigger-002.json
│   │   └── trigger-003.json
│   └── ...
├── index.json (searchable index)
└── README.md (storage documentation)
```

### 6.3 Index File

**File**: `governance/events/agent-sync-triggers/index.json`

**Structure**:
```json
{
  "triggers": [
    {
      "event_id": "trigger-001",
      "timestamp": "2025-12-24T10:00:00Z",
      "category": "GOVERNANCE_RULE_CHANGE",
      "priority": "HIGH",
      "file_path": "2025/12/trigger-001.json",
      "sync_status": "COMPLETED | IN_PROGRESS | FAILED | PENDING"
    }
  ],
  "last_updated": "2025-12-24T10:30:00Z"
}
```

---

## VII. Trigger Filtering and Suppression

### 7.1 Suppression Rules

**Suppress Triggers When**:
- Change is documentation-only (no functional impact)
- Change is reverted within 1 hour (false alarm)
- Change is marked as `no-sync-required` in commit message
- Duplicate trigger detected (same canonical commit)

**Suppression Log**: `governance/events/agent-sync-triggers/suppressed.json`

### 7.2 Filtering Rules

**Filter Triggers When**:
- Priority is LOW and similar trigger already pending
- Change does not affect FM agents (builder-only change)
- Change is to non-canonical governance (experimental)

---

## VIII. Error Handling

### 8.1 Detection Failures

**Failure**: Cannot access canonical repository

**Response**:
1. Log connection error
2. Retry after 15 minutes (max 3 retries)
3. If all retries fail, escalate to admin
4. Do NOT assume no changes

---

**Failure**: Cannot parse canonical changes

**Response**:
1. Log parsing error with details
2. Create manual review issue
3. Escalate to admin
4. Block automatic sync until resolved

---

### 8.2 Validation Failures

**Failure**: Trigger event fails schema validation

**Response**:
1. Log validation errors
2. Discard invalid trigger
3. Create incident report
4. Investigate detection logic

---

## IX. Monitoring and Metrics

### 9.1 Key Metrics

**Tracked**:
- Triggers detected per month (by category)
- Trigger detection latency (time from canonical change to detection)
- False positive rate (suppressed triggers / total triggers)
- Missed triggers (found by audit)

### 9.2 Alerts

**Alert When**:
- Detection latency > 24 hours
- False positive rate > 10%
- Missed triggers found by audit
- Detection failures > 3 consecutive

---

## X. References

- **Main Workflow**: `governance/workflows/AGENT_CONTEXT_SYNC_WORKFLOW.md`
- **Event Schema**: `governance/events/AGENT_SYNC_TRIGGER_EVENT_SCHEMA.json`
- **Governance Ripple**: `governance/alignment/GOVERNANCE_RIPPLE_COMPATIBILITY.md`

---

## XI. Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2025-12-24 | Initial trigger specification | FM Builder |

---

**Status**: OPERATIONAL  
**Authority**: Corporate Governance Canon  
**Maintainer**: Governance Administrator

---

*Triggers are precise. Detection is timely. Synchronisation is controlled.*

**END OF AGENT CONTEXT SYNC TRIGGER EVENTS**
