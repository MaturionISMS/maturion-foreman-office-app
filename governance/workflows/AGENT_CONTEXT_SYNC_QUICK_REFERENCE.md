# Agent Context Synchronisation - Quick Reference

**Status**: Operational  
**Version**: 1.0.0  
**Last Updated**: 2025-12-24

---

## Quick Start

### Run Dry-Run Test
```bash
python3 scripts/sync-agent-context.py --dry-run --manual \
  --trigger-reason "Testing sync workflow"
```

### Trigger Manual Sync
```bash
python3 scripts/sync-agent-context.py --manual \
  --trigger-reason "Post-incident governance realignment" \
  --canonical-commit abc123def
```

### Check Sync Status
```bash
cat governance/events/agent-sync-events.json | jq '.events | length'
```

---

## Command Reference

### Sync Commands

| Command | Description |
|---------|-------------|
| `--dry-run` | Test updates without applying |
| `--manual --trigger-reason "<reason>"` | Manual sync trigger |
| `--canonical-commit <sha>` | Sync from specific commit |
| `--rollback --event-id <id>` | Rollback previous sync |

### Examples

**Test sync workflow:**
```bash
python3 scripts/sync-agent-context.py --dry-run --manual \
  --trigger-reason "Testing"
```

**Manual sync after governance change:**
```bash
python3 scripts/sync-agent-context.py --manual \
  --trigger-reason "GSR v2.1 adoption" \
  --canonical-commit abc123
```

**Rollback failed sync:**
```bash
python3 scripts/sync-agent-context.py --rollback --event-id sync-001
```

---

## File Locations

| Resource | Path |
|----------|------|
| Main workflow | `governance/workflows/AGENT_CONTEXT_SYNC_WORKFLOW.md` |
| Trigger events spec | `governance/workflows/AGENT_CONTEXT_SYNC_TRIGGERS.md` |
| Sync script | `scripts/sync-agent-context.py` |
| Audit log | `governance/events/agent-sync-events.json` |
| Trigger schema | `governance/events/AGENT_SYNC_TRIGGER_EVENT_SCHEMA.json` |
| Sync event schema | `governance/events/AGENT_SYNC_EVENT_SCHEMA.json` |

---

## Agent Files

| Agent | Path | Approval Required |
|-------|------|-------------------|
| Foreman | `.github/agents/foreman.agent.md` | ✅ Always |
| Foreman App | `.github/agents/ForemanApp-agent.md` | ✅ Always |
| Governance Liaison | `.github/agents/governance-liaison.md` | ✅ Always |
| FM Office Contract | `governance/agents/foreman-office.agent.contract.md` | ✅ Always |

---

## Workflow Phases

```
1. TRIGGER DETECTION    → Canonical governance change detected
2. AGENT EVALUATION     → Identify affected agents
3. UPDATE PREPARATION   → Generate context updates
4. APPROVAL GATE        → Request approvals (if required)
5. CONTROLLED UPDATE    → Apply approved changes
6. AUDIT LOGGING        → Record sync event
```

---

## Approval Matrix

| Agent Type | Additive | Modification | Breaking |
|------------|----------|--------------|----------|
| FM Agents | Admin | Admin | Johan |
| Builder Agents | Auto | Admin | Johan |
| Liaison Agent | Admin | Admin | Johan |

**Legend:**
- **Auto**: Automatically approved
- **Admin**: Admin-agent approval required
- **Johan**: Human (Johan Ras) approval required

---

## Priority Levels

| Priority | Response Time | Approval | Use When |
|----------|--------------|----------|----------|
| CRITICAL | < 1 hour | Human | Build Philosophy, breaking contract |
| HIGH | 24 hours | Admin | Governance rules, compliance |
| MEDIUM | 1 week | Auto (if safe) | Standards, non-breaking |
| LOW | 2 weeks | Auto | Documentation, clarifications |

---

## Common Scenarios

### Scenario 1: New Governance Rule Added
```bash
# Canonical governance adds new rule
# FM detects change automatically (or manual trigger)
python3 scripts/sync-agent-context.py --manual \
  --trigger-reason "New governance rule: XYZ" \
  --canonical-commit abc123

# Result: Foreman and liaison agents updated
# Approval required from admin-agent
```

### Scenario 2: Build Philosophy Updated
```bash
# Build Philosophy document updated
python3 scripts/sync-agent-context.py --manual \
  --trigger-reason "Build Philosophy v2.0" \
  --canonical-commit def456

# Result: ALL agents updated
# Human approval (Johan) required
```

### Scenario 3: Dry-Run Before Real Sync
```bash
# Test first
python3 scripts/sync-agent-context.py --dry-run --manual \
  --trigger-reason "Testing compliance update"

# Review output, then run for real
python3 scripts/sync-agent-context.py --manual \
  --trigger-reason "Compliance control added"
```

---

## Monitoring

### Check Last Sync
```bash
cat governance/events/agent-sync-events.json | \
  jq '.events | sort_by(.timestamp) | last'
```

### Count Sync Events
```bash
cat governance/events/agent-sync-events.json | \
  jq '.events | length'
```

### Find Failed Syncs
```bash
cat governance/events/agent-sync-events.json | \
  jq '.events[] | select(.outcome == "FAILURE")'
```

---

## Troubleshooting

### Issue: Approval Required but Script Continues
**Solution**: Script only prepares updates. Actual application requires approval via GitHub issue or PR.

### Issue: Agent Version Not Incremented
**Solution**: Check that agent file has valid `version:` field in YAML frontmatter.

### Issue: Sync Event Not Logged
**Solution**: Ensure `governance/events/` directory exists and is writable.

---

## Out of Scope

This workflow does NOT:
- ❌ Automatically modify agent behavior (learning)
- ❌ Write to runtime memory
- ❌ Train agents
- ❌ Expand agent capabilities beyond governance

---

## References

- **Main Workflow**: `governance/workflows/AGENT_CONTEXT_SYNC_WORKFLOW.md`
- **Governance Ripple**: `governance/alignment/GOVERNANCE_RIPPLE_COMPATIBILITY.md`
- **Agent Contracts**: `.github/agents/*.md`

---

**For full documentation, see**: `governance/workflows/AGENT_CONTEXT_SYNC_WORKFLOW.md`

**END OF QUICK REFERENCE**
