# FM Runtime Cognitive Hygiene Protocol (CHP) - Memory Integration Architecture

**Document Type:** Architecture Specification  
**Version:** 1.0.0  
**Status:** Draft  
**Owner:** Maturion Foreman  
**Created:** 2025-12-24

---

## 1. Purpose

This document defines the **runtime integration architecture** between the Cognitive Hygiene Protocol (CHP) and the Memory Fabric in the FM (Foreman Maturion) application.

The CHP is responsible for:
- **Detecting AI reasoning drift** - When agent responses deviate from governance, architecture, or established patterns
- **Proposing corrections** - Suggesting realignment actions without authority to enforce
- **Learning from patterns** - Identifying recurring issues to improve governance

This architecture ensures CHP can read memory safely while **preventing authority leakage** - CHP proposes, it never decides.

This is an **architecture and specification document only** - no implementation is included.

---

## 2. Scope

This architecture applies to:

- **CHP Runtime Component** - Active cognitive hygiene monitoring
- **Memory Fabric** - Unified memory accessed by CHP
- **Proposal System** - How CHP proposals are generated, routed, and approved

This architecture is **separate from but aligned with**:
- Memory lifecycle state machine (see `MEMORY_LIFECYCLE_STATE_MACHINE.md`)
- Memory observability (see `MEMORY_OBSERVABILITY_ARCHITECTURE.md`)
- Memory behavior rules (see `foreman/behaviours/memory-rules.md`)

---

## 3. Core Principle: No Authority Leakage

**CHP Proposes, Never Decides**

The CHP is a **detection and advisory system**, not a decision-making authority. It:
- ✅ Reads memory to understand governance, architecture, and patterns
- ✅ Detects drift between observed behavior and expected behavior
- ✅ Proposes corrective actions or improvements
- ❌ **Never** auto-applies changes to architecture, governance, or code
- ❌ **Never** overrides Foreman decisions
- ❌ **Never** directly modifies memory without approval

**Authority Hierarchy:**
1. **Johan** - Ultimate authority, approves all governance changes
2. **Foreman** - Architecture and build governance authority
3. **CHP** - Advisory only, proposes to Foreman or Johan

---

## 4. CHP Memory Read Authorization

### 4.1 Authorized Memory Scopes

CHP is **authorized to read** the following memory scopes:

#### 4.1.1 GLOBAL Scope (Read-Only)

**Purpose:** Understand platform-wide governance, architecture principles, and patterns.

**Authorized Content:**
- Build philosophy (one-time correctness, zero regression)
- Architecture standards and templates
- Governance policies and rules
- QA and compliance requirements
- Privacy guardrails

**Access Pattern:**
- **Frequency:** On CHP initialization, then cached
- **Refresh:** Hourly or on governance update event
- **Tags:** `governance`, `architecture`, `philosophy`, `qa`, `compliance`
- **Importance:** `high` or `critical` only

**Why Allowed:**
- CHP needs to understand **what correctness means** to detect drift
- Global scope contains no tenant-specific or sensitive data
- Read-only access ensures no tampering

---

#### 4.1.2 FOREMAN Scope (Read-Only)

**Purpose:** Understand Foreman's decisions, past build outcomes, and reasoning patterns.

**Authorized Content:**
- Architecture decisions and rationales
- Build wave outcomes and failures
- Task distribution decisions
- QA validation results
- Module boundary definitions

**Access Pattern:**
- **Frequency:** On-demand when analyzing agent behavior
- **Tags:** `architecture`, `build`, `qa`, `decision`, `module`
- **Importance:** `medium`, `high`, or `critical`

**Why Allowed:**
- CHP needs to understand **Foreman's reasoning history** to detect when agents deviate
- Foreman scope contains governance-level decisions, not tenant data
- Helps CHP learn patterns: "Foreman consistently prioritizes X over Y"

---

#### 4.1.3 EXPERIENCE Scope (Proposed - Read-Only)

**Purpose:** Learn from historical incidents, lessons learned, and improvement patterns.

**Authorized Content:**
- Past drift incidents and resolutions
- Lessons learned from build failures
- Recurring issue patterns
- Improvement suggestions previously accepted/rejected

**Access Pattern:**
- **Frequency:** On-demand when analyzing similar incidents
- **Tags:** `incident`, `lesson`, `improvement`, `pattern`
- **Importance:** All levels

**Why Allowed:**
- CHP learns from experience: "Last time X happened, Y was the fix"
- No tenant-specific data in experience memory
- Helps CHP improve proposal quality over time

---

### 4.2 Prohibited Memory Scopes

CHP is **NOT authorized to read** the following:

#### 4.2.1 RUNTIME Scope (Prohibited)

**Reason:** Contains tenant-specific operational data (performance metrics, anomalies, incidents tied to organisations).

**Risk:** CHP could inadvertently leak tenant context into proposals.

**Exception:** CHP may read **anonymized aggregate patterns** only (e.g., "40% of tenants experienced slow API response in module X"), not raw tenant data.

---

#### 4.2.2 PLATFORM Scope (Prohibited)

**Reason:** Contains platform-wide operational state, potentially including tenant identifiers or sensitive monitoring data.

**Risk:** CHP could be influenced by current operational state, biasing proposals.

**Exception:** CHP may receive **filtered, anonymized summaries** for context (e.g., "Platform health: degraded, cause: database contention"), not raw telemetry.

---

### 4.3 Read Audit Requirements

**Every CHP memory read MUST be audited:**

```json
{
  "timestamp": "2025-12-24T14:30:00Z",
  "actor": "CHP",
  "action": "read_memory",
  "scopes_accessed": ["global", "foreman"],
  "tags_queried": ["architecture", "governance"],
  "importance_min": "high",
  "entries_returned": 15,
  "reason": "Analyzing agent deviation from module boundary rules",
  "session_id": "chp-session-789"
}
```

**Audit Storage:** `/runtime/audit/chp-memory-reads.json` (append-only, immutable)

**Audit Retention:** 7 years (compliance requirement)

**Audit Consumers:**
- **Foreman** - Reviews CHP access patterns during QA
- **Watchdog** - Monitors for unauthorized access attempts
- **Johan** - Audits CHP behavior for governance compliance

---

## 5. When CHP Reads Memory

### 5.1 CHP Initialization (Startup)

**Trigger:** CHP runtime component starts.

**Memory Reads:**
1. Load `global` scope, tags: `governance`, `architecture`, `philosophy`
2. Load `foreman` scope, tags: `architecture`, `decision`, `governance`
3. Load `experience` scope, tags: `lesson`, `pattern`

**Purpose:** Establish baseline understanding of "correct" behavior.

**Frequency:** Once per CHP session, then cached for session duration.

---

### 5.2 Drift Detection Event

**Trigger:** CHP detects potential agent drift (e.g., agent proposes architecture change without Foreman approval).

**Memory Reads:**
1. Query `global` for relevant architecture rules
2. Query `foreman` for past decisions on similar situations
3. Query `experience` for similar drift incidents

**Purpose:** Determine if drift is genuine or acceptable exception.

**Frequency:** On-demand per drift event.

---

### 5.3 Proposal Generation

**Trigger:** CHP decides to generate a correction proposal.

**Memory Reads:**
1. Query `foreman` for context on affected module/area
2. Query `experience` for precedents (successful past proposals)
3. Query `global` for governance rules relevant to proposal

**Purpose:** Craft well-informed, precedent-based proposal.

**Frequency:** Once per proposal.

---

### 5.4 Periodic Hygiene Scan

**Trigger:** Scheduled (e.g., daily or weekly).

**Memory Reads:**
1. Scan `foreman` for recent decisions
2. Scan `experience` for unresolved patterns
3. Query `global` for governance updates

**Purpose:** Proactive identification of emerging drift patterns.

**Frequency:** Configurable (default: daily).

---

## 6. How CHP Reads Memory (Technical Flow)

### 6.1 Read Request Flow

```
1. CHP determines need for memory context
2. CHP constructs read query:
   - Scopes: ['global', 'foreman', 'experience']
   - Tags: ['architecture', 'governance']
   - Importance: 'high'
   - Reason: "Analyzing agent deviation from module boundary"
3. CHP calls Memory Fabric API: `queryMemory(query)`
4. Memory Fabric validates CHP authorization:
   - Check: Is CHP authorized for requested scopes? ✅
   - Check: Are requested scopes allowed for CHP? ✅
   - Check: Is memory in USABLE or DEGRADED state? ✅
5. Memory Fabric logs audit entry (immutable)
6. Memory Fabric returns filtered entries
7. CHP processes entries and caches for session
8. CHP proceeds with drift analysis or proposal generation
```

---

### 6.2 Read Authorization Enforcement

**Enforcement Points:**

1. **API Gateway** - Validates CHP identity and scope authorization
2. **Memory Lifecycle Manager** - Ensures memory is in safe state (USABLE or DEGRADED, not FAILED)
3. **Privacy Checker** - Filters out any entries with tenant-specific data (defense-in-depth)
4. **Audit Logger** - Records all CHP reads (append-only, immutable)

**Authorization Matrix:**

| Scope | CHP Read | CHP Write | Rationale |
|-------|----------|-----------|-----------|
| `global` | ✅ Allowed | ❌ Denied | CHP needs governance context, but cannot modify |
| `foreman` | ✅ Allowed | ❌ Denied | CHP needs Foreman decisions, but cannot override |
| `experience` | ✅ Allowed | ⚠️ Proposal Only | CHP learns from experience, writes only via approved proposals |
| `platform` | ❌ Denied | ❌ Denied | Contains tenant data, CHP must not access |
| `runtime` | ❌ Denied | ❌ Denied | Contains tenant operations, CHP must not access |

---

## 7. How CHP Generates Proposals

### 7.1 Proposal Structure

Every CHP proposal follows a standard structure:

```json
{
  "proposal_id": "CHP-2025-001234",
  "timestamp": "2025-12-24T15:00:00Z",
  "proposer": "CHP",
  "category": "architecture_drift",
  "severity": "medium",
  "title": "Agent proposed module boundary violation without Foreman approval",
  "description": "UI Builder attempted to add direct database access to Asset module, bypassing API layer. This violates module boundary rule defined in ARCH-2024-089.",
  "evidence": {
    "drift_detected_at": "2025-12-24T14:45:00Z",
    "agent": "ui-builder",
    "action": "add_database_import",
    "module": "Asset",
    "violated_rule": "ARCH-2024-089: All modules must use API layer for cross-module data access",
    "memory_reference": "foreman/2024-03-15.json#entry-abc123"
  },
  "recommended_action": {
    "type": "revert_and_educate",
    "steps": [
      "Revert UI Builder's database import change",
      "Update UI Builder context with module boundary rules",
      "Re-attempt via API layer instead"
    ]
  },
  "precedent": {
    "similar_incident": "CHP-2024-567",
    "resolution": "Agent re-educated, change reverted, compliant solution applied",
    "memory_reference": "experience/2024-08-20.json#entry-xyz789"
  },
  "requires_approval_from": "Foreman",
  "auto_apply": false,
  "escalate_to_johan_if_rejected": false
}
```

---

### 7.2 Proposal Categories

| Category | Severity | Approval Required | Auto-Apply Allowed |
|----------|----------|-------------------|-------------------|
| `architecture_drift` | Medium-High | Foreman | ❌ Never |
| `governance_violation` | High-Critical | Johan | ❌ Never |
| `qa_gap` | Medium | Foreman | ❌ Never |
| `documentation_gap` | Low-Medium | Foreman | ⚠️ Only if low-risk |
| `pattern_improvement` | Low | Foreman | ⚠️ Only if low-risk |
| `privacy_violation` | Critical | Johan | ❌ Never (immediate escalation) |

---

### 7.3 Proposal Generation Flow

```
1. CHP detects drift or issue
2. CHP queries memory for context and precedent
3. CHP constructs proposal (see structure above)
4. CHP determines proposal category and severity
5. CHP determines approval authority (Foreman or Johan)
6. CHP writes proposal to proposal queue: `/runtime/proposals/pending/`
7. CHP emits event: `chp.proposal.generated`
8. Proposal routing system delivers to approver:
   - Low/Medium → Foreman review queue
   - High/Critical → Johan notification
9. Approver reviews and decides:
   - APPROVED → Proposal moves to `/runtime/proposals/approved/`
   - REJECTED → Proposal moves to `/runtime/proposals/rejected/` with reason
   - ESCALATED → Proposal routed to Johan
10. If APPROVED:
    - Action is executed (by Foreman or designated agent)
    - Outcome logged to `experience` scope
    - CHP learns from outcome
```

---

## 8. No Auto-Promotion Enforcement

**Core Rule:** CHP proposals **MUST NOT** be auto-applied, even for low-severity issues, unless explicitly pre-authorized by governance policy.

### 8.1 Auto-Apply Authorization

**NEVER Auto-Apply:**
- Architecture changes
- Governance rule changes
- Code modifications
- Privacy-related changes
- Security-related changes
- Any change affecting tenant data or operations

**MAY Auto-Apply (If Pre-Authorized):**
- Documentation corrections (typos, formatting)
- Non-functional logging additions
- Telemetry instrumentation (if pre-approved)
- Self-test additions (if low-risk)

**Pre-Authorization Process:**
1. Johan defines auto-apply policy in `governance/chp-auto-apply-policy.json`
2. Policy specifies:
   - Allowed categories
   - Max severity level
   - Required validation steps
   - Rollback procedure
3. CHP checks policy before marking proposal `auto_apply: true`
4. All auto-applied changes logged and audited

---

### 8.2 Enforcement Mechanisms

**Code-Level Enforcement:**
- CHP proposal generation function **cannot** call execution functions directly
- Execution functions require approval token (generated only by Foreman or Johan)
- Approval token includes proposal ID, approver identity, timestamp

**Audit Enforcement:**
- All CHP actions logged with `requires_approval: true/false`
- Watchdog monitors for CHP actions without approval tokens
- Violation triggers immediate escalation to Johan

**Human-in-Loop Enforcement:**
- Critical proposals require explicit Johan approval (email, dashboard action)
- Medium proposals require Foreman acknowledgment
- Low proposals may be auto-approved **only if pre-authorized**

---

## 9. Failure Handling and Degraded Mode

### 9.1 Memory Fabric Unavailable (FAILED State)

**Scenario:** Memory fabric is in FAILED state (e.g., schema corruption, privacy violation detected).

**CHP Behavior:**
- ❌ CHP cannot read memory
- ❌ CHP cannot generate informed proposals
- ⚠️ CHP switches to **Conservative Mode**

**Conservative Mode:**
- CHP detects drift but cannot propose corrections (lacks context)
- CHP logs drift events with: "Memory unavailable, proposal generation blocked"
- CHP escalates to Foreman: "Memory FAILED, CHP operating blind"
- CHP awaits memory recovery before resuming full operation

---

### 9.2 Memory Fabric Degraded (DEGRADED State)

**Scenario:** Memory fabric is in DEGRADED state (e.g., `experience` scope missing, but `global` and `foreman` available).

**CHP Behavior:**
- ✅ CHP can read available scopes (`global`, `foreman`)
- ⚠️ CHP cannot access missing scopes (`experience`)
- ⚠️ CHP proposals may lack precedent context

**Degraded Mode:**
- CHP continues drift detection with available memory
- CHP proposals include disclaimer: "Precedent data unavailable, recommendation based on current rules only"
- CHP proposals marked with elevated risk: `degraded_context: true`
- Approvers notified of degraded context

---

### 9.3 CHP Component Failure

**Scenario:** CHP runtime component crashes or becomes unresponsive.

**Fallback Behavior:**
- Foreman and agents continue operating (CHP is advisory, not critical path)
- Watchdog detects CHP unavailability, alerts Johan
- Drift may go undetected until CHP recovers
- Post-recovery: CHP performs retroactive hygiene scan to catch missed drift

**Recovery:**
- CHP restarts, re-initializes memory context
- CHP reviews recent events since last successful scan
- CHP generates catch-up proposals for any detected drift

---

### 9.4 Proposal Queue Overflow

**Scenario:** CHP generates proposals faster than Foreman can review (e.g., widespread drift detected).

**Backpressure Handling:**
1. CHP detects queue depth exceeds threshold (e.g., >50 pending proposals)
2. CHP prioritizes proposals by severity (Critical > High > Medium > Low)
3. CHP pauses low-severity proposal generation
4. CHP emits alert: `chp.queue.overflow`
5. Foreman notified: "CHP proposal queue backed up, manual review needed"

**Manual Intervention:**
- Johan reviews queue, approves/rejects in batch
- Foreman may request CHP to reset and re-scan with stricter filters

---

## 10. Proposal Routing and Approval

### 10.1 Routing Rules

| Proposal Category | Severity | Routed To | Notification Method |
|-------------------|----------|-----------|---------------------|
| `architecture_drift` | Low-Medium | Foreman | Dashboard queue |
| `architecture_drift` | High-Critical | Foreman + Johan | Dashboard + Email |
| `governance_violation` | Any | Johan | Email + Dashboard (urgent) |
| `qa_gap` | Low-Medium | Foreman | Dashboard queue |
| `qa_gap` | High | Foreman + QA Builder | Dashboard + Agent notification |
| `privacy_violation` | Any | Johan | Immediate escalation (SMS/call) |
| `pattern_improvement` | Low | Foreman | Dashboard queue (non-urgent) |

---

### 10.2 Approval Workflow

```
1. CHP writes proposal to `/runtime/proposals/pending/{proposal_id}.json`
2. Routing system reads proposal, determines approver
3. Notification sent to approver (dashboard, email, etc.)
4. Approver reviews proposal:
   - Reviews evidence (memory references, drift details)
   - Reviews recommended action
   - Reviews precedent (if available)
5. Approver decides:
   - APPROVE → Proposal executed
   - REJECT → Proposal archived with reason
   - DEFER → Proposal flagged for later review
   - ESCALATE → Proposal routed to higher authority (Johan)
6. Decision logged to audit trail
7. If APPROVED:
   - Designated agent executes action
   - Outcome logged to `experience` scope
   - CHP learns from outcome
8. If REJECTED:
   - Reason logged
   - CHP learns rejection pattern (may adjust future proposals)
```

---

### 10.3 Approval SLA

| Severity | Target Review Time | Escalation if Missed |
|----------|-------------------|----------------------|
| Critical | 1 hour | Auto-escalate to Johan |
| High | 24 hours | Notify Johan of delay |
| Medium | 3 days | Flagged in Foreman dashboard |
| Low | 7 days | No escalation (queue managed) |

---

## 11. Learning from Outcomes

### 11.1 Approved Proposal Outcome

**When a CHP proposal is approved and executed:**

1. **Outcome Tracked:**
   - Did the action resolve the drift? (Yes/No)
   - Did the action cause new issues? (Yes/No)
   - Was the recommendation accurate? (Yes/No)

2. **Learning Logged to `experience` Scope:**
   ```json
   {
     "id": "exp-2025-001234",
     "timestamp": "2025-12-24T16:00:00Z",
     "scope": "experience",
     "title": "CHP proposal CHP-2025-001234 resolved architecture drift",
     "summary": "CHP correctly identified module boundary violation. Revert and re-education resolved issue. No recurrence detected.",
     "importance": "medium",
     "tags": ["chp", "proposal", "success", "architecture"],
     "related_proposal": "CHP-2025-001234",
     "outcome": "success",
     "lessons": [
       "UI Builder frequently misses module boundary rules, may need better context injection",
       "Revert + educate pattern effective for boundary violations"
     ]
   }
   ```

3. **CHP Learns:**
   - Successful pattern reinforced: "Revert + educate works for boundary violations"
   - Agent behavior pattern updated: "UI Builder prone to boundary violations"
   - Future proposals reference this precedent

---

### 11.2 Rejected Proposal Outcome

**When a CHP proposal is rejected:**

1. **Rejection Reason Analyzed:**
   - Was the drift detection incorrect? (False positive)
   - Was the recommendation inappropriate?
   - Was the context insufficient?

2. **Learning Logged to `experience` Scope:**
   ```json
   {
     "id": "exp-2025-001235",
     "timestamp": "2025-12-24T16:30:00Z",
     "scope": "experience",
     "title": "CHP proposal CHP-2025-001235 rejected: False positive",
     "summary": "CHP flagged API change as boundary violation, but was actually approved exception. CHP missed exception clause in governance.",
     "importance": "medium",
     "tags": ["chp", "proposal", "rejected", "false-positive"],
     "related_proposal": "CHP-2025-001235",
     "outcome": "rejected",
     "lessons": [
       "CHP must check for approved exceptions before flagging drift",
       "Exception tracking needs improvement"
     ]
   }
   ```

3. **CHP Learns:**
   - False positive pattern identified: "Check for exceptions in governance rules"
   - Future proposals include exception check step

---

## 12. Integration with Existing Specifications

This architecture integrates with:

### 12.1 Memory Lifecycle State Machine
- **Source:** `MEMORY_LIFECYCLE_STATE_MACHINE.md`
- **Alignment:** CHP reads memory only when in USABLE or DEGRADED state, switches to Conservative Mode if FAILED

### 12.2 Memory Observability
- **Source:** `MEMORY_OBSERVABILITY_ARCHITECTURE.md`
- **Alignment:** CHP reads are audited and visible to Foreman/Watchdog/Johan via observability layer

### 12.3 Memory Behavior Rules
- **Source:** `foreman/behaviours/memory-rules.md`
- **Alignment:** CHP follows "Memory Before Action" principle, loads context before proposals

### 12.4 Privacy Guardrails (Canonical)
- **Source:** `maturion-foreman-governance/governance/policies/privacy-guardrails.md`
- **Alignment:** CHP reads only non-tenant memory, Privacy Checker filters CHP reads

---

## 13. Non-Functional Requirements

### 13.1 Performance

- **Memory Read Latency:** <200ms for CHP context load
- **Proposal Generation Time:** <5 seconds per proposal
- **Proposal Queue Throughput:** Support 100+ proposals/day without backlog

### 13.2 Reliability

- **CHP Availability:** 95% (advisory system, not critical path)
- **Proposal Delivery:** 100% (no proposals lost)
- **Audit Completeness:** 100% (all CHP reads logged)

### 13.3 Security

- **Authorization Enforcement:** 100% (CHP never accesses prohibited scopes)
- **Audit Immutability:** 100% (audit logs append-only, tamper-proof)
- **No Auto-Promotion:** 100% (no CHP proposals auto-applied without authorization)

---

## 14. Future Enhancements

### 14.1 Adaptive Learning
- CHP learns from approval/rejection patterns
- CHP adjusts drift detection thresholds dynamically
- CHP proposes governance rule updates based on recurring patterns

### 14.2 Proactive Hygiene
- CHP predicts drift before it occurs (based on agent behavior trends)
- CHP suggests preventive actions (e.g., "UI Builder context outdated, refresh recommended")

### 14.3 Cross-Tenant Pattern Recognition
- CHP analyzes anonymized drift patterns across tenants (if authorized)
- CHP proposes platform-wide improvements based on common issues

---

## 15. Summary

This architecture defines a **safe, auditable, and authority-respecting** integration between CHP and the Memory Fabric.

**Key Principles:**
1. **No Authority Leakage** - CHP proposes, never decides
2. **Read Authorization** - CHP reads only `global`, `foreman`, `experience` scopes (no tenant data)
3. **Audit Everything** - All CHP reads and proposals logged immutably
4. **No Auto-Promotion** - Proposals require explicit approval (except pre-authorized low-risk actions)
5. **Fail Safe** - CHP switches to Conservative Mode if memory unavailable
6. **Learn from Outcomes** - CHP improves proposals based on approval/rejection feedback

**CHP Reads:** `global`, `foreman`, `experience` (read-only, audited)

**CHP Writes:** Proposals only (to proposal queue, not directly to memory)

**Authority:** Foreman or Johan approves, CHP executes only after approval

**Failure Handling:** Conservative Mode (memory unavailable), Degraded Mode (partial memory), Queue Overflow (backpressure)

This architecture enables **intelligent drift detection** without compromising governance, privacy, or authority boundaries.

---

**Next Steps:**
1. Review and approve architecture
2. Implement CHP memory read authorization layer
3. Implement proposal generation and routing system
4. Integrate CHP with Foreman approval workflow
5. Add CHP proposal dashboard for Johan/Foreman

---

**Version History:**
- v1.0.0 (2025-12-24): Initial architecture specification

**Related Documents:**
- `MEMORY_LIFECYCLE_STATE_MACHINE.md` - Memory lifecycle states and transitions
- `MEMORY_OBSERVABILITY_ARCHITECTURE.md` - Observability and audit trail
- `foreman/behaviours/memory-rules.md` - Memory behavior requirements
- `foreman/runtime-memory-ingestion.md` - Runtime memory ingestion patterns
