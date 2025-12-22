# FM Office Visibility Events (Placeholder)

**Status**: Placeholder (Non-Functional)  
**Last Updated**: 2025-12-22

---

## Purpose

This directory is a **placeholder** for future FM Office dashboard governance-alignment events.

**Current State**: No automation exists. This is forward compatibility only.

**Future State**: This directory will record governance-relevant events that power the FM Office dashboard and audible alert system.

---

## Directory Purpose

### What This Directory Will Contain

When FM Agent is implemented, this directory will store:

1. **Governance Alignment Events**
   - When governance canon changes detected
   - When FM constraints updated to match governance
   - When governance drift detected and resolved

2. **Build Compliance Events**
   - When PR gates enforce governance
   - When FM Builder provides pre-handover proof
   - When governance constraints block non-compliant work

3. **Violation Events**
   - When governance violations detected
   - When violations resolved
   - When gates strengthened to prevent recurrence

4. **Evidence Collection Events**
   - When evidence automatically collected
   - When compliance reports generated
   - When audit trail entries created

---

## Event Structure (Planned)

### Event File Format

Each event will be stored as a JSON file:

```
events/
├── 2025-12-22T10-30-45_governance_change_detected.json
├── 2025-12-22T10-35-12_constraints_updated.json
├── 2025-12-22T11-00-00_pr_gate_enforced.json
└── 2025-12-22T11-15-30_prehandover_proof_provided.json
```

### Event Schema (Planned)

```json
{
  "event_id": "uuid",
  "event_type": "governance_change_detected | constraints_updated | pr_gate_enforced | etc.",
  "timestamp": "ISO-8601 timestamp",
  "severity": "info | warning | error | critical",
  "source": "governance_liaison | fm_builder | pr_gate | fm_agent",
  "description": "Human-readable description",
  "details": {
    // Event-specific details
  },
  "evidence": {
    // Links to evidence files, commits, PRs, etc.
  },
  "resolution": {
    // If event was a problem, how was it resolved
  }
}
```

---

## Event Types (Planned)

### 1. Governance Change Events

**Type**: `governance_change_detected`

**Triggered When**: Corporate governance canon changes

**Content**:
- What changed in governance canon
- Link to governance commit
- Impact assessment on FM execution

---

**Type**: `constraints_updated`

**Triggered When**: FM execution constraints updated to match governance

**Content**:
- Which constraints were updated
- What PRs/commits made the changes
- Link to updated PR gate configurations

---

### 2. Build Compliance Events

**Type**: `pr_gate_enforced`

**Triggered When**: PR gate blocks non-compliant PR

**Content**:
- Which gate blocked
- What constraint was violated
- Link to PR and failure logs

---

**Type**: `prehandover_proof_provided`

**Triggered When**: FM Builder provides pre-handover proof

**Content**:
- PR number
- List of checks that were green
- Link to proof comment

---

**Type**: `handover_authorized`

**Triggered When**: FM Builder hands over with all gates green

**Content**:
- PR number
- All gate statuses
- Evidence of compliance

---

### 3. Violation Events

**Type**: `governance_violation_detected`

**Triggered When**: Governance violation detected (should be rare)

**Content**:
- What constraint was violated
- Where (PR, commit, file)
- How it bypassed gates (if applicable)

---

**Type**: `violation_resolved`

**Triggered When**: Governance violation fixed

**Content**:
- Link to original violation event
- How it was fixed
- What prevention measures added

---

### 4. Drift Events

**Type**: `governance_drift_detected`

**Triggered When**: FM execution has drifted from governance canon

**Content**:
- What drifted
- How detected
- Gap between canon and execution

---

**Type**: `governance_drift_resolved`

**Triggered When**: Drift corrected

**Content**:
- Link to drift detection event
- Actions taken to resolve
- Verification that alignment restored

---

## Integration with FM Office Dashboard (Future)

### Dashboard Views (Planned)

1. **Governance State View**
   - Current alignment with corporate governance canon
   - Last governance update timestamp
   - Pending governance changes

2. **Real-Time Events View**
   - Live stream of governance events
   - Filterable by event type and severity
   - Clickable for full details

3. **Compliance Metrics View**
   - Governance compliance percentage
   - Violations over time
   - Time-to-resolution for violations

4. **Evidence View**
   - All compliance evidence in one place
   - Searchable and filterable
   - Audit-ready export

### Audible Alerts (Planned)

Different event types will trigger different sounds:

- **Governance Change**: Informational chime
- **PR Gate Enforced**: Warning sound
- **Violation Detected**: Urgent alert sound
- **Handover Authorized**: Success chime
- **Drift Detected**: Attention sound

---

## Current Status

**Automation**: None  
**Event Generation**: None  
**Dashboard**: Not implemented  
**Alerts**: Not implemented

**Purpose**: Forward compatibility only

This directory exists to:
1. Establish the event structure concept
2. Document planned event types
3. Prepare for future FM Agent implementation
4. Avoid breaking changes when automation is added

---

## When Will This Become Functional?

### Phase 1: Manual Event Recording (Near Future)
- Events created manually by Governance Liaison
- Simple JSON files documenting key governance actions
- Used for reporting and audit trail

### Phase 2: Automated Event Generation (Future)
- PR gates generate events automatically
- FM Builder generates events during build
- Events stored in this directory

### Phase 3: FM Office Dashboard (Future)
- Dashboard reads events from this directory
- Real-time event stream visualization
- Compliance metrics calculated from events

### Phase 4: Full FM Agent Integration (Long-term)
- Events generated in real-time during development
- Audible alerts active
- Predictive events (warn before violation)
- Complete audit trail automatic

---

## Design Rationale

### Why Create This Now?

1. **Forward Compatibility**
   - Establishes structure before automation
   - Avoids breaking changes later
   - Clear evolution path

2. **Documentation**
   - Documents planned event model
   - Provides reference for future implementation
   - Sets expectations

3. **Alignment with Governance Philosophy**
   - Governance first, automation later
   - Structure before implementation
   - No premature optimization

---

## Rules for This Directory

### While Non-Functional

1. ❌ Do NOT create event files (not yet automated)
2. ❌ Do NOT build dashboard (not yet functional)
3. ❌ Do NOT implement alerts (not yet ready)
4. ✅ DO document planned event types
5. ✅ DO maintain this README
6. ✅ DO update schema as governance evolves

### When Becoming Functional

1. ✅ Start with simple manual events
2. ✅ Evolve to automated generation
3. ✅ Build dashboard only when events exist
4. ✅ Keep event schema backward-compatible

---

## References

- **Governance Alignment Overview**: `governance/alignment/GOVERNANCE_ALIGNMENT_OVERVIEW.md`
- **FM Governance Adoption Policy**: `governance/policies/FM_GOVERNANCE_ADOPTION_POLICY.md`
- **Future FM Agent Role**: Defined in Governance Alignment Overview

---

*This directory is a placeholder. No automation exists yet.*
