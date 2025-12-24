# Agent Canonical Context Synchronisation Workflow

**Status**: Operational  
**Version**: 1.0.0  
**Authority**: Corporate Governance Canon  
**Last Updated**: 2025-12-24

---

## I. Purpose

This workflow governs how agent context files (`.agent` files in `.github/agents/` and `governance/agents/`) are synchronized when canonical governance changes occur.

**Core Principle**: Agent context must remain aligned with canonical governance at all times, but updates must be controlled, audited, and admin-mediated for FM agents.

---

## II. Scope

### In Scope
- Detection of canonical governance trigger events
- Evaluation of affected agents based on governance changes
- Controlled update of agent context files
- Admin-agent-mediated FM `.agent` file updates
- Audit logging of all synchronisation events
- Version tracking of agent context

### Explicitly Out of Scope
- ❌ Agent learning mechanisms
- ❌ Runtime memory writes
- ❌ Autonomous agent adaptation
- ❌ Automatic agent file modification without approval
- ❌ Agent behavioral training
- ❌ Agent capability expansion beyond governance

---

## III. Workflow Overview

```
┌─────────────────────────────────────────┐
│  Canonical Governance Change            │
│  (maturion-foreman-governance)          │
└──────────────┬──────────────────────────┘
               │
               ↓
┌──────────────────────────────────────────┐
│  1. TRIGGER DETECTION                    │
│  - Monitor canonical repo for changes    │
│  - Identify governance artifacts updated │
│  - Generate trigger event                │
└──────────────┬───────────────────────────┘
               │
               ↓
┌──────────────────────────────────────────┐
│  2. AGENT EVALUATION                     │
│  - Map changed governance to agents      │
│  - Identify affected agent context files │
│  - Determine update requirements         │
└──────────────┬───────────────────────────┘
               │
               ↓
┌──────────────────────────────────────────┐
│  3. UPDATE PREPARATION                   │
│  - Generate context update diff          │
│  - Create update proposal                │
│  - Validate against agent contract       │
└──────────────┬───────────────────────────┘
               │
               ↓
┌──────────────────────────────────────────┐
│  4. APPROVAL GATE                        │
│  - FM agents: Admin-agent approval       │
│  - Builder agents: Auto-approve if safe  │
│  - Breaking changes: Human approval      │
└──────────────┬───────────────────────────┘
               │
               ↓
┌──────────────────────────────────────────┐
│  5. CONTROLLED UPDATE                    │
│  - Apply approved context changes        │
│  - Update agent version metadata         │
│  - Validate post-update consistency      │
└──────────────┬───────────────────────────┘
               │
               ↓
┌──────────────────────────────────────────┐
│  6. AUDIT LOGGING                        │
│  - Record synchronisation event          │
│  - Capture before/after state            │
│  - Log approval chain                    │
└──────────────────────────────────────────┘
```

---

## IV. Phase 1: Trigger Detection

### 4.1 Canonical Governance Monitoring

**Monitor Locations**:
- `maturion-foreman-governance` repository
- Governance canon directories
- Agent contract templates
- Policy documents

**Trigger Events**:
1. **Governance Rule Change**
   - New governance rule added
   - Existing rule modified
   - Rule deprecated or removed

2. **Agent Contract Template Update**
   - Contract structure changed
   - New required field added
   - Field semantics modified

3. **Policy Update**
   - New policy introduced
   - Policy requirements changed
   - Policy scope modified

4. **Compliance Control Change**
   - New control added
   - Control mapping updated
   - Control evidence requirements changed

5. **Architecture Standard Change**
   - Architecture checklist updated
   - Naming conventions modified
   - Folder structure requirements changed

**Detection Method**:
```python
def detect_canonical_trigger():
    """
    Detect canonical governance changes requiring agent sync.
    
    Returns:
        TriggerEvent: Canonical change details
    """
    # Compare current canonical state with last sync
    canonical_current = fetch_canonical_state()
    canonical_last_sync = load_last_sync_state()
    
    # Identify differences
    changes = diff_governance_state(canonical_current, canonical_last_sync)
    
    if not changes:
        return None
    
    # Create trigger event
    trigger = TriggerEvent(
        timestamp=datetime.utcnow(),
        canonical_commit=canonical_current.commit_sha,
        changes=changes,
        affected_areas=identify_affected_areas(changes)
    )
    
    return trigger
```

### 4.2 Trigger Event Schema

See: `governance/events/AGENT_SYNC_TRIGGER_EVENT_SCHEMA.json`

**Required Fields**:
- `event_id`: Unique identifier
- `timestamp`: ISO-8601 timestamp
- `canonical_commit`: Source commit SHA
- `change_type`: Type of governance change
- `affected_governance_areas`: List of affected areas
- `priority`: LOW | MEDIUM | HIGH | CRITICAL

---

## V. Phase 2: Agent Evaluation

### 5.1 Agent-Governance Mapping

**Mapping Rules**:

| Governance Area | Affected Agents |
|----------------|-----------------|
| Architecture standards | `foreman.agent.md`, `ForemanApp-agent.md` |
| QA governance | `foreman.agent.md`, builder agents |
| Compliance controls | `foreman.agent.md`, `governance-liaison.md` |
| Build philosophy | All agents |
| Memory model | `foreman.agent.md`, FM agents |
| Privacy guardrails | All agents |

### 5.2 Context Dependency Analysis

**Analyze**:
1. Which agent context files reference changed governance
2. Which agent capabilities depend on changed policies
3. Which agent constraints are affected by changes
4. Which agent escalation rules need updating

**Analysis Output**:
```json
{
  "affected_agents": [
    {
      "agent_file": ".github/agents/foreman.agent.md",
      "agent_role": "governance",
      "impact_level": "HIGH",
      "required_updates": [
        {
          "section": "responsibilities.governance",
          "change_type": "ADD_RULE",
          "governance_source": "GSR_v2.1",
          "update_description": "Add new governance supremacy clause"
        }
      ]
    }
  ]
}
```

### 5.3 Update Requirements Determination

**For Each Affected Agent**:
1. Identify specific context sections requiring update
2. Determine if update is additive or breaking
3. Assess backward compatibility
4. Generate update diff

---

## VI. Phase 3: Update Preparation

### 6.1 Context Update Generation

**Process**:
1. Load current agent context
2. Parse YAML frontmatter and markdown body
3. Apply governance change to appropriate section
4. Preserve agent-specific customizations
5. Validate updated context against contract

**Update Types**:

**Additive Update** (Safe):
- Add new constraint
- Add new responsibility
- Add new reference document
- Add new protected path

**Modification Update** (Review Required):
- Change existing constraint
- Modify responsibility scope
- Update escalation trigger
- Change authority level

**Breaking Update** (Human Approval Required):
- Remove capability
- Restrict existing permission
- Change fundamental behavior
- Alter contract structure

### 6.2 Validation Rules

**Pre-Update Validation**:
- ✅ Agent contract structure intact
- ✅ Required fields present
- ✅ YAML frontmatter valid
- ✅ Governance references resolvable
- ✅ No conflicting constraints

**Post-Update Validation**:
- ✅ Updated context is valid YAML
- ✅ All mandatory fields present
- ✅ Governance alignment maintained
- ✅ No syntax errors
- ✅ Version metadata updated

---

## VII. Phase 4: Approval Gate

### 7.1 Approval Requirements

**FM Agents** (`.github/agents/foreman.agent.md`, `ForemanApp-agent.md`):
- **ALL updates require admin-agent approval**
- **Rationale**: FM agents have elevated authority and direct governance enforcement role
- **Approver**: Governance Administrator or Johan Ras
- **Process**: Create approval request issue with update diff

**Builder Agents**:
- **Additive updates**: Auto-approve
- **Modification updates**: Admin-agent approval
- **Breaking updates**: Human approval (Johan)

**Governance Liaison Agent**:
- **All updates require admin-agent approval**
- **Rationale**: Liaison mediates canonical governance adoption

### 7.2 Approval Workflow

```
┌─────────────────────────────────┐
│  Update Proposal Generated      │
└──────────────┬──────────────────┘
               │
               ↓
       ┌───────────────┐
       │ Update Type?  │
       └───────┬───────┘
               │
       ┌───────┴───────┐
       │               │
       ↓               ↓
   Additive        Modification/Breaking
       │               │
       ↓               ↓
   Auto-approve    Requires Approval
       │               │
       │               ↓
       │       ┌──────────────────┐
       │       │ Agent Type?      │
       │       └──────┬───────────┘
       │              │
       │      ┌───────┴────────┐
       │      │                │
       │      ↓                ↓
       │   FM Agent      Builder Agent
       │      │                │
       │      ↓                ↓
       │  Admin-Agent    ┌──────────────┐
       │  Approval       │ Breaking?    │
       │      │          └──────┬───────┘
       │      │                 │
       │      │         ┌───────┴───────┐
       │      │         │               │
       │      │         ↓               ↓
       │      │   Admin-Agent       Human
       │      │   Approval         Approval
       │      │         │               │
       └──────┴─────────┴───────────────┘
                        │
                        ↓
               ┌────────────────┐
               │ Apply Update   │
               └────────────────┘
```

### 7.3 Approval Request Format

**Issue Title**: `[AGENT-SYNC] Approve context update for <agent-name>`

**Issue Body**:
```markdown
## Agent Context Update Approval Request

**Agent**: `<agent-file-path>`
**Trigger**: Canonical governance change in `<governance-area>`
**Update Type**: ADDITIVE | MODIFICATION | BREAKING
**Priority**: LOW | MEDIUM | HIGH | CRITICAL

### Canonical Change
- **Source**: `<canonical-commit-sha>`
- **Governance Area**: `<area>`
- **Change Description**: <description>

### Proposed Agent Update

#### Diff
```diff
<unified diff of proposed changes>
```

#### Impact Analysis
- **Affected Sections**: <list>
- **Backward Compatible**: YES | NO
- **Risk Level**: LOW | MEDIUM | HIGH

### Validation Results
- ✅ Syntax valid
- ✅ Contract structure intact
- ✅ Required fields present
- ✅ Governance alignment maintained

### Approval Required From
- [ ] Admin-Agent / Governance Administrator
- [ ] Johan Ras (if breaking change)

### Auto-Generated Links
- [View Canonical Change](<link>)
- [View Current Agent Context](<link>)
- [View Proposed Agent Context](<link>)
```

---

## VIII. Phase 5: Controlled Update

### 8.1 Update Application

**Process**:
1. Backup current agent context
2. Apply approved changes
3. Update version metadata
4. Commit with descriptive message
5. Validate post-update state

**Commit Message Format**:
```
[AGENT-SYNC] Update <agent-name> context for <governance-area> change

Canonical commit: <sha>
Change type: <type>
Approval: <approval-reference>
Agent version: <old-version> → <new-version>
```

### 8.2 Version Metadata Update

**Agent Frontmatter** (YAML):
```yaml
version: 1.1.0  # Incremented
last_updated: 2025-12-24
governance_sync:
  canonical_commit: abc123def
  sync_timestamp: 2025-12-24T10:30:00Z
  sync_event_id: sync-001
```

### 8.3 Post-Update Validation

**Checks**:
- ✅ Agent file is valid YAML + Markdown
- ✅ All required fields present
- ✅ Governance references resolve
- ✅ No syntax errors
- ✅ Version incremented correctly
- ✅ Backup created successfully

**On Validation Failure**:
1. Rollback to backup
2. Log failure reason
3. Create incident report
4. Escalate to human (Johan)

---

## IX. Phase 6: Audit Logging

### 9.1 Synchronisation Event Record

**Log Location**: `governance/events/agent-sync-events.json`

**Event Schema**:
```json
{
  "event_id": "sync-001",
  "timestamp": "2025-12-24T10:30:00Z",
  "event_type": "AGENT_CONTEXT_SYNC",
  "canonical_trigger": {
    "commit_sha": "abc123def",
    "governance_area": "compliance-controls",
    "change_type": "NEW_CONTROL_ADDED"
  },
  "affected_agents": [
    {
      "agent_file": ".github/agents/foreman.agent.md",
      "agent_role": "governance",
      "update_type": "ADDITIVE",
      "version_before": "1.0.0",
      "version_after": "1.1.0",
      "approval": {
        "required": true,
        "approver": "governance-administrator",
        "approval_timestamp": "2025-12-24T10:25:00Z",
        "approval_reference": "issue-123"
      }
    }
  ],
  "outcome": "SUCCESS | FAILURE | PARTIAL",
  "validation_results": {
    "pre_update": "PASS",
    "post_update": "PASS"
  },
  "audit_artifacts": [
    "governance/events/agent-sync-001-before.md",
    "governance/events/agent-sync-001-after.md",
    "governance/events/agent-sync-001-diff.patch"
  ]
}
```

### 9.2 Audit Artifacts

**Artifacts Created**:
1. **Before Snapshot**: Complete agent context before update
2. **After Snapshot**: Complete agent context after update
3. **Diff Patch**: Unified diff of changes
4. **Approval Chain**: Record of all approvals
5. **Validation Report**: Pre and post-update validation results

**Storage**: `governance/events/agent-sync/<event-id>/`

---

## X. Error Handling and Escalation

### 10.1 Error Categories

**E1: Detection Failure**
- Cannot access canonical repository
- Cannot parse governance changes
- **Response**: Log error, retry after 1 hour, escalate if persistent

**E2: Evaluation Failure**
- Cannot determine affected agents
- Invalid agent-governance mapping
- **Response**: Manual evaluation required, create incident issue

**E3: Update Generation Failure**
- Cannot generate valid update
- Update violates contract
- **Response**: Skip automatic update, require human intervention

**E4: Approval Timeout**
- No approval received within SLA
- **Response**: Escalate to Johan, mark as blocked

**E5: Update Application Failure**
- Update creates invalid agent context
- Validation fails post-update
- **Response**: Rollback, log failure, escalate

**E6: Audit Logging Failure**
- Cannot write audit log
- **Response**: Block update until logging succeeds

### 10.2 Escalation Protocol

**Level 1: Admin-Agent**
- All routine approvals
- Non-breaking updates
- **SLA**: 24 hours

**Level 2: Johan Ras**
- Breaking changes
- Approval timeout
- Update failures
- **SLA**: Immediate notification

---

## XI. Monitoring and Metrics

### 11.1 Key Metrics

**Tracked Metrics**:
- Sync events per month
- Average time from trigger to completion
- Approval wait time (by type)
- Update success rate
- Rollback frequency
- Manual intervention rate

### 11.2 Success Criteria

**Sync is Successful When**:
- ✅ Canonical trigger detected within 24 hours
- ✅ Affected agents identified correctly
- ✅ Updates generated and validated
- ✅ Approvals obtained within SLA
- ✅ Updates applied without errors
- ✅ Audit trail complete and auditable
- ✅ No governance drift detected post-sync

---

## XII. Operational Procedures

### 12.1 Manual Sync Trigger

**When to Use**:
- Canonical changes missed by automation
- Post-incident governance realignment
- Governance drift detected

**Command**:
```bash
python3 scripts/sync-agent-context.py --manual --trigger-reason "<reason>"
```

### 12.2 Dry Run Mode

**Test Updates Without Applying**:
```bash
python3 scripts/sync-agent-context.py --dry-run --canonical-commit <sha>
```

### 12.3 Rollback Procedure

**Rollback Last Sync**:
```bash
python3 scripts/sync-agent-context.py --rollback --event-id <event-id>
```

---

## XIII. Integration Points

### 13.1 Governance Ripple Compatibility

**Aligns With**: `governance/alignment/GOVERNANCE_RIPPLE_COMPATIBILITY.md`

**Downward Ripple**:
- This workflow implements downward ripple for agent context
- Canonical governance → FM agent context updates

**Upward Ripple**:
- Agent context issues discovered during sync may trigger proposals
- Proposals submitted to canonical governance repository

### 13.2 Memory Sync Integration

**Aligns With**: `fm/governance/MEMORY_SYNC_CONTRACT.md`

**Relationship**:
- Agent context sync is **separate** from memory sync
- Agent context = governance-derived behavior rules
- Memory = learned patterns and historical events
- Both must remain aligned but use different mechanisms

---

## XIV. Testing and Validation

### 14.1 Test Scenarios

**T1: Additive Update (Auto-Approve)**
- New governance rule added
- Agent context updated automatically
- Audit logged correctly

**T2: Modification Update (Approval Required)**
- Governance rule modified
- Approval request created
- Update applied after approval

**T3: Breaking Update (Human Approval)**
- Governance rule removed
- Human approval required
- Update blocked until approval

**T4: Multi-Agent Update**
- Governance change affects multiple agents
- All agents updated in single sync event
- Audit captures all changes

**T5: Update Failure and Rollback**
- Update creates invalid context
- Automatic rollback triggered
- Incident logged

**T6: Approval Timeout**
- No approval within SLA
- Escalation triggered
- Johan notified

### 14.2 Test Location

`tests/governance/test_agent_context_sync.py`

---

## XV. References

### 15.1 Related Documents

- **Governance Ripple Compatibility**: `governance/alignment/GOVERNANCE_RIPPLE_COMPATIBILITY.md`
- **Agent Sync Triggers**: `governance/workflows/AGENT_CONTEXT_SYNC_TRIGGERS.md`
- **Agent Contract Template**: `governance/contracts/agent-contract-template.md`
- **Memory Sync Contract**: `fm/governance/MEMORY_SYNC_CONTRACT.md`

### 15.2 Canonical Sources

- **Canonical Governance**: `https://github.com/MaturionISMS/maturion-foreman-governance`
- **Agent Contract Standards**: `maturion-foreman-governance/agents/`
- **Governance Canon**: `maturion-foreman-governance/governance/canon/`

---

## XVI. Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2025-12-24 | Initial workflow specification | FM Builder |

---

**Status**: OPERATIONAL  
**Authority**: Corporate Governance Canon  
**Maintainer**: Governance Administrator  
**Review Cycle**: Quarterly or on major canonical change

---

*Agent context remains synchronized. Governance alignment is maintained. Audit trail is complete.*

**END OF AGENT CANONICAL CONTEXT SYNCHRONISATION WORKFLOW**
