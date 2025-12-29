# Build Intervention and Alert Model (G-C10)

**Version**: 1.0.0  
**Status**: Active  
**Authority**: BUILD_TREE_EXECUTION_MODEL.md (G-C8)  
**Last Updated**: 2025-12-29  
**Owner**: Johan (MaturionISMS)  
**Code**: G-C10

---

## I. Purpose

This document defines the **canonical model for build intervention controls and attention routing**, establishing explicit mechanisms for human authority to intervene in build execution at any point in the build tree hierarchy.

**Scope**: This specification covers UI controls, routing models, and governance constraints for intervention. It does NOT include automated enforcement logic or self-healing capabilities.

**Core Principle**: **"No automated intervention; all stops and alerts require explicit human decision."**

---

## II. Intervention Types

### 2.1 Alert (Non-Blocking)

**Definition**: A non-blocking signal that notifies responsible parties of a concern, question, or need for attention without halting execution.

**Characteristics**:
- Does NOT stop execution
- Does NOT prevent state transitions
- Routes to appropriate authority for review
- May escalate if no response within defined timeframe
- Maintains full audit trail
- Execution continues while alert is being reviewed

**Use Cases**:
- Unexpected behavior requiring attention
- Questions about scope or requirements
- Non-critical anomalies
- Request for guidance
- Status update requests
- Documentation clarifications

**Authority**:
- Can be triggered by: Builder agents, FM, watchdogs, human operators
- Routes to: FM, governance oversight, human authority (as defined by scope)

### 2.2 Emergency Stop (Immediately Binding)

**Definition**: An immediate, unconditional halt of execution at the specified scope level, taking effect instantly and preventing all further automated progress.

**Characteristics**:
- Takes effect IMMEDIATELY upon confirmation
- STOPS all execution at specified scope
- Prevents state transitions
- Prevents automated resumption
- Requires explicit authorization to resume
- Creates full evidence package
- Logs all context at moment of stop

**Use Cases**:
- Critical security concern detected
- Architecture violation discovered
- Governance breach identified
- Catastrophic test failure
- Scope contamination risk
- Data integrity threat
- Privacy violation detected
- Unauthorized changes in progress

**Authority**:
- Can be triggered by: Human operators, FM (with rationale), governance watchdogs
- Routes to: Human authority, FM, governance oversight
- Resumption requires: Explicit authorization from human authority

---

## III. Scope Hierarchy

Interventions can target different levels of the build tree:

### 3.1 Step Scope

**Target**: Individual task execution step (e.g., "architecture validation", "test execution")

**Impact**:
- Alert: Notifies responsible builder/FM
- Stop: Halts current step only, task remains in progress

**Recovery**: 
- Alert: No recovery needed, execution continues
- Stop: Resume step after issue resolution

### 3.2 Sub-Wave Scope

**Target**: Group of related tasks within a wave

**Impact**:
- Alert: Notifies wave coordinator and FM
- Stop: Halts all tasks in sub-wave

**Recovery**:
- Alert: No recovery needed, execution continues
- Stop: Resume sub-wave after issue resolution

### 3.3 Wave Scope

**Target**: Complete wave of build execution

**Impact**:
- Alert: Notifies program manager and FM
- Stop: Halts entire wave, all tasks stop

**Recovery**:
- Alert: No recovery needed, execution continues
- Stop: Resume wave after issue resolution and re-authorization

### 3.4 Application/Program Scope

**Target**: Entire build program (all waves)

**Impact**:
- Alert: Notifies all stakeholders, escalates to human authority
- Stop: Catastrophic halt - ALL execution stops immediately

**Recovery**:
- Alert: High-priority review, no execution halt
- Stop: Full program review required, explicit re-authorization from Johan or designated authority

---

## IV. Intervention Flow

### 4.1 Alert Flow

```
[Trigger] → [Scope Selection] → [Rationale Entry] → [Confirmation Modal]
    ↓
[Alert Logged] → [Route to Authority] → [Context Package Prepared]
    ↓
[Notification Sent] → [Execution Continues] → [Response Tracked]
    ↓
[Resolution Logged] ← [Authority Response]
```

### 4.2 Emergency Stop Flow

```
[Trigger] → [Scope Selection] → [Rationale Entry] → [CRITICAL Confirmation Modal]
    ↓
[IMMEDIATE STOP] → [Execution State Frozen] → [Evidence Package Created]
    ↓
[Stop Logged] → [Route to Authority] → [Full Context Package Prepared]
    ↓
[Investigation] → [Resolution Decision] → [Explicit Resume Authorization]
    ↓
[Resume Logged] → [Execution State Restored] → [Audit Trail Updated]
```

---

## V. Confirmation Modals

### 5.1 Alert Confirmation

**Title**: "Issue Build Alert"

**Content**:
- Scope: `[Step/Sub-Wave/Wave/Application]`
- Current Node: `[node_id]`
- Impact: "Execution will continue. Alert will be routed to [authority]."
- Rationale: `[user-entered text, required]`
- Authority Context: "This alert will be reviewed by [FM/Governance/Human Authority]."

**Actions**:
- "Send Alert" (primary)
- "Cancel" (secondary)

**Validation**:
- Rationale must be at least 20 characters
- Scope must be selected
- User must acknowledge impact

### 5.2 Emergency Stop Confirmation

**Title**: "⚠️ EMERGENCY STOP"

**Content**:
- **WARNING**: "This will IMMEDIATELY halt execution at [scope] level."
- Scope: `[Step/Sub-Wave/Wave/Application]`
- Current Node: `[node_id]`
- Impact: "All execution at [scope] will stop immediately. Resumption requires explicit authorization."
- Critical Rationale: `[user-entered text, required, minimum 50 characters]`
- Authority Context: "This stop requires authorization from [Human Authority] to resume."
- **Confirmation**: "I understand this stop takes immediate effect and cannot be automated." (checkbox required)

**Actions**:
- "STOP EXECUTION" (danger, primary)
- "Cancel" (secondary)

**Validation**:
- Rationale must be at least 50 characters
- Scope must be selected
- Confirmation checkbox must be checked
- Double-confirmation via "Type STOP to confirm" field

---

## VI. Routing and Authority

### 6.1 Alert Routing Table

| Scope | Primary Route | Secondary Route | Escalation (if no response) |
|-------|---------------|-----------------|----------------------------|
| Step | Builder Agent | FM | FM → Human (24h) |
| Sub-Wave | FM | Governance | Governance → Human (12h) |
| Wave | FM + Governance | Human Authority | Immediate escalation |
| Application | Human Authority | FM + Governance | Immediate notification to Johan |

### 6.2 Emergency Stop Routing Table

| Scope | Immediate Route | Required Authorization | Resumption Authority |
|-------|----------------|------------------------|---------------------|
| Step | Builder Agent + FM | Builder Agent | FM |
| Sub-Wave | FM + Governance | FM | Human Authority or FM |
| Wave | FM + Human Authority | Human Authority | Human Authority |
| Application | Johan + All Stakeholders | Johan | Johan only |

---

## VII. Contextual Chat Interface

### 7.1 Purpose

Provide a context-aware communication channel scoped to the specific build node where intervention was triggered.

### 7.2 Preloaded Context

When intervention chat is opened, the interface MUST include:

1. **Node Context**:
   - Node ID, type, name
   - Current execution and activation states
   - Status indicator and explanation
   
2. **Evidence Context**:
   - Governing checks status
   - Requirements satisfaction
   - Evidence artifacts (links)
   - Test results summary
   
3. **Blocker Context** (if applicable):
   - Active blockers
   - Resolution paths
   - Dependencies
   
4. **Decision History**:
   - Recent decisions affecting this node
   - Authority trail
   - Rationale summaries

### 7.3 Chat Features

- **Scope Indicator**: Always visible at top (e.g., "Chat: task-ai-panel")
- **Participants**: Shows who is in the conversation (FM, builders, human authority)
- **Message Types**: 
  - Questions (from agents)
  - Decisions (from authority)
  - Status updates
  - Evidence references
- **Actions**:
  - Send message
  - Attach evidence
  - Reference specific artifacts
  - Request status update
  - Close conversation (with resolution note)

### 7.4 Chat Audit

All chat messages MUST be:
- Logged with timestamp and sender
- Stored as part of node audit trail
- Included in evidence packages
- Preserved for 7 years (ISO 27001)

---

## VIII. Explicit Prohibitions

### 8.1 Automatic Resumption

❌ **Prohibited**: Any automated logic that resumes execution after Emergency Stop

**Rationale**: Human authority must explicitly review and authorize resumption to ensure issue is resolved and safe to proceed.

### 8.2 Silent Interventions

❌ **Prohibited**: Any intervention that does not create audit trail

**Rationale**: All interventions must be traceable for governance and audit purposes.

### 8.3 Agent Self-Authorization

❌ **Prohibited**: Agents authorizing their own resumption after stop

**Rationale**: Separation of concerns - agents can request resumption but cannot approve it.

### 8.4 Scope Escalation Without Authority

❌ **Prohibited**: Automatically escalating intervention scope without human decision

**Rationale**: Scope changes have significant impact and require explicit authorization.

---

## IX. Audit and Logging

### 9.1 Alert Logging

Each alert MUST log:
- Alert ID (unique)
- Timestamp (ISO 8601)
- Triggered by (user/agent identity)
- Scope level
- Target node ID
- Rationale (full text)
- Routing (primary and secondary recipients)
- Response timeline
- Resolution (when closed)
- Evidence package link

### 9.2 Emergency Stop Logging

Each emergency stop MUST log:
- Stop ID (unique)
- Timestamp (ISO 8601)
- Triggered by (user/agent identity)
- Scope level
- Target node ID
- Critical rationale (full text)
- Execution state at moment of stop
- Affected tasks/nodes
- Evidence package (full snapshot)
- Investigation timeline
- Resolution decision
- Resumption authorization
- Resumption timestamp
- Authority identity

### 9.3 Audit Trail Requirements

All intervention audit logs MUST:
- Be immutable (append-only)
- Include cryptographic signatures (future)
- Be retained for 7 years minimum
- Be indexed for searchability
- Support compliance reporting (ISO 27001, SOC 2)
- Be included in annual audit reviews

---

## X. Data Model

### 10.1 Alert Schema

```typescript
interface BuildAlert {
  alert_id: string;
  alert_type: 'alert';
  triggered_at: string; // ISO 8601
  triggered_by: {
    type: 'human' | 'agent' | 'watchdog';
    identity: string;
    ip_address?: string;
  };
  scope: {
    level: 'step' | 'sub-wave' | 'wave' | 'application';
    target_node_id: string;
    target_node_type: string;
  };
  rationale: string; // minimum 20 characters
  routing: {
    primary: string[];
    secondary: string[];
    escalation_after_hours: number;
  };
  status: 'open' | 'acknowledged' | 'resolved' | 'escalated';
  response_timeline: {
    acknowledged_at?: string;
    resolved_at?: string;
    escalated_at?: string;
  };
  resolution?: {
    resolved_by: string;
    resolution_note: string;
    action_taken: string;
  };
  context_package: {
    node_state: object;
    evidence: string[];
    blockers: string[];
  };
}
```

### 10.2 Emergency Stop Schema

```typescript
interface EmergencyStop {
  stop_id: string;
  stop_type: 'emergency_stop';
  triggered_at: string; // ISO 8601
  triggered_by: {
    type: 'human' | 'agent' | 'watchdog';
    identity: string;
    ip_address?: string;
  };
  scope: {
    level: 'step' | 'sub-wave' | 'wave' | 'application';
    target_node_id: string;
    target_node_type: string;
    affected_nodes: string[]; // all nodes halted
  };
  critical_rationale: string; // minimum 50 characters
  confirmation: {
    acknowledged_impact: boolean;
    typed_confirmation: string; // must be "STOP"
  };
  execution_snapshot: {
    frozen_state: object;
    active_tasks: string[];
    pending_transitions: string[];
  };
  routing: {
    immediate: string[]; // notified immediately
    required_authorization: string; // who can resume
  };
  status: 'active' | 'investigating' | 'resolved' | 'resumed';
  timeline: {
    stopped_at: string;
    investigation_started_at?: string;
    resolved_at?: string;
    resumed_at?: string;
  };
  resumption?: {
    authorized_by: string;
    authorization_timestamp: string;
    resolution_summary: string;
    resume_conditions: string[];
  };
  evidence_package: {
    full_snapshot: string; // path to snapshot
    logs: string[];
    artifacts: string[];
    decisions: string[];
  };
}
```

### 10.3 Chat Message Schema

```typescript
interface InterventionChatMessage {
  message_id: string;
  conversation_id: string; // links to alert_id or stop_id
  sent_at: string; // ISO 8601
  sender: {
    type: 'human' | 'agent';
    identity: string;
    role: string;
  };
  message_type: 'question' | 'answer' | 'decision' | 'status_update' | 'evidence_reference';
  content: string;
  references?: {
    evidence_id?: string;
    artifact_link?: string;
    node_id?: string;
  };
  read_by: {
    identity: string;
    read_at: string;
  }[];
}
```

---

## XI. API Contract

### 11.1 Issue Alert

```
POST /api/build-tree/alert
```

**Request Body**:
```json
{
  "scope_level": "step" | "sub-wave" | "wave" | "application",
  "target_node_id": "string",
  "rationale": "string (min 20 chars)",
  "triggered_by": "string"
}
```

**Response** (201 Created):
```json
{
  "success": true,
  "alert_id": "string",
  "routed_to": ["string"],
  "status": "open"
}
```

### 11.2 Issue Emergency Stop

```
POST /api/build-tree/emergency-stop
```

**Request Body**:
```json
{
  "scope_level": "step" | "sub-wave" | "wave" | "application",
  "target_node_id": "string",
  "critical_rationale": "string (min 50 chars)",
  "confirmation": {
    "acknowledged_impact": true,
    "typed_confirmation": "STOP"
  },
  "triggered_by": "string"
}
```

**Response** (201 Created):
```json
{
  "success": true,
  "stop_id": "string",
  "stopped_at": "ISO 8601",
  "affected_nodes": ["string"],
  "status": "active",
  "resumption_requires": "string"
}
```

### 11.3 Get Intervention Context

```
GET /api/build-tree/intervention/:intervention_id/context
```

**Response** (200 OK):
```json
{
  "success": true,
  "context": {
    "node": { /* node inspection data */ },
    "evidence": [ /* evidence artifacts */ ],
    "blockers": [ /* active blockers */ ],
    "decisions": [ /* recent decisions */ ],
    "timeline": [ /* state history */ ]
  }
}
```

### 11.4 Resume After Stop

```
POST /api/build-tree/emergency-stop/:stop_id/resume
```

**Request Body**:
```json
{
  "authorized_by": "string",
  "resolution_summary": "string (min 50 chars)",
  "resume_conditions": ["string"]
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "resumed_at": "ISO 8601",
  "status": "resumed"
}
```

---

## XII. Security and Privacy

### 12.1 Authorization

- Only authorized users can trigger emergency stops at Application/Wave scope
- Alerts can be triggered by agents but must be routed appropriately
- Resumption authority is explicitly defined per scope level

### 12.2 Data Protection

- All intervention data respects tenant isolation
- No cross-tenant intervention visibility
- Chat messages are encrypted in transit and at rest
- Evidence packages exclude sensitive credentials

### 12.3 Audit Compliance

- ISO 27001: 7-year retention of intervention logs
- SOC 2: Immutable audit trail
- GDPR: PII minimization in intervention logs

---

## XIII. Acceptance Criteria

✅ Alert button issues non-blocking notifications  
✅ Emergency Stop button halts execution immediately  
✅ Scope selection available for all hierarchy levels  
✅ Confirmation modals show authority context  
✅ Routing directs to appropriate authority  
✅ Contextual chat preloaded with node context  
✅ No automated resumption after emergency stop  
✅ All interventions logged and auditable  
✅ Explicit authorization required for resumption

---

## XIV. References

- **BUILD_TREE_EXECUTION_MODEL.md (G-C8)** - Parent specification
- **BUILD_NODE_INSPECTION_MODEL.md (G-C9)** - Context data model
- **ACTIVATION_STATE_MODEL.md** - State definitions
- **WATCHDOG_AUTHORITY_AND_SCOPE.md** - Watchdog authority (when created)
- **FOREMAN_AUTHORITY_AND_SUPERVISION_MODEL.md** - FM authority (when created)

---

*END OF BUILD_INTERVENTION_AND_ALERT_MODEL.md*
