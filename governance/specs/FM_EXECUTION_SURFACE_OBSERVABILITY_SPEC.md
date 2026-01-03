# FM Execution Surface Observability Specification

**Version**: 1.0.0  
**Status**: ACTIVATED  
**Date Activated**: 2026-01-03  
**Authority**: Johan Ras  
**Scope**: FM App Execution Surface Requirements  
**Purpose**: Define observability requirements for FM execution states, including escalation, halt, and capability selection

---

## I. Constitutional Grounding

This specification implements observability requirements derived from:

- **FM_AI_ESCALATION_AND_CAPABILITY_SCALING_SPEC.md** (parent specification)
- **FM_EXECUTION_MANDATE.md** Section VI (STOP and Escalation Semantics)
- **AGENT_CONSTITUTION.md** Section VIII.3 (Escalate When Blocked)

**Key Principle**: Governance activation cannot remain "theoretical at runtime". All governance-defined behaviors MUST be observable.

---

## II. Execution State Model

### A. Required States

FM execution surface MUST support representation of the following states:

```
PLANNING       → FM planning activities (wave/task definition)
EXECUTING      → Normal execution (builder coordination, monitoring)
HALTED         → FM-initiated proactive halt (cognitive limit)
BLOCKED        → Gate or governance block (policy enforcement)
FAILED         → Execution failure (technical/QA error)
ESCALATED      → Escalation pending resolution
AWAITING_INPUT → Waiting for Johan decision
COMPLETED      → Successful completion
ABORTED        → Explicitly aborted by FM or Johan
```

### B. State Transitions

Valid state transitions:

```
PLANNING → EXECUTING
PLANNING → HALTED (if complexity detected during planning)
PLANNING → BLOCKED (if governance violation detected)

EXECUTING → HALTED (cognitive limit reached)
EXECUTING → BLOCKED (gate failure)
EXECUTING → FAILED (execution error)
EXECUTING → ESCALATED (escalation initiated)
EXECUTING → COMPLETED (success)

HALTED → ESCALATED (escalation sent)
BLOCKED → ESCALATED (cannot resolve independently)
FAILED → ESCALATED (repeated failure)

ESCALATED → AWAITING_INPUT (waiting for Johan)
AWAITING_INPUT → EXECUTING (resume authorized)
AWAITING_INPUT → ABORTED (abort authorized)

HALTED → EXECUTING (after escalation resolved, resume authorized)
BLOCKED → EXECUTING (after gate/governance issue resolved)

Any State → ABORTED (Johan explicit abort)
```

### C. State Metadata

Each state MUST have associated metadata:

```json
{
  "current_state": "HALTED | BLOCKED | FAILED | ESCALATED | etc.",
  "state_entered_at": "ISO-8601",
  "state_duration_seconds": "integer",
  "state_reason": "string",
  "previous_state": "string",
  "next_possible_states": ["string"],
  "resolution_required": "boolean",
  "resolution_authority": "string or null"
}
```

---

## III. Escalation Observability

### A. Escalation Event Stream

FM MUST emit escalation events with the following structure:

```json
{
  "event_type": "ESCALATION_INITIATED | ESCALATION_RESOLVED | ESCALATION_OVERRIDDEN",
  "escalation_id": "uuid",
  "timestamp": "ISO-8601",
  "escalation_type": "COGNITIVE_LIMIT | COMPLEXITY_THRESHOLD | GOVERNANCE_AMBIGUITY | NOVEL_PATTERN",
  "task_context": "string",
  "complexity_indicators": ["string"],
  "escalation_target": "Johan Ras",
  "resolution_status": "PENDING | RESOLVED | OVERRIDDEN",
  "resolution_timestamp": "ISO-8601 or null"
}
```

### B. Escalation History

FM execution surface MUST maintain:

- **Escalation log** — All escalations with full context
- **Escalation count** — Per task, per wave, per program
- **Resolution time** — Average time to resolution
- **Repeat escalations** — Same issue escalated multiple times

### C. Escalation UI Representation

UI MUST:

- ✅ Show escalation status prominently (not buried in logs)
- ✅ Distinguish escalation from failure
- ✅ Display escalation reason and context
- ✅ Show resolution authority (Johan Ras)
- ✅ Indicate when awaiting resolution
- ✅ Link to escalation details

**Example UI States**:

```
⬆️ Escalated: Cognitive limit reached on architecture validation
   Awaiting resolution from Johan Ras
   Escalation ID: esc-20260103-001
   [View Details]
```

---

## IV. Halt Observability

### A. Halt Event Stream

FM MUST emit halt events with the following structure:

```json
{
  "event_type": "HALT_TRIGGERED | HALT_RELEASED",
  "halt_id": "uuid",
  "timestamp": "ISO-8601",
  "halt_reason": "COGNITIVE_LIMIT | GOVERNANCE_AMBIGUITY | NOVEL_PATTERN | RIPPLE_CASCADE | CONSTITUTIONAL_RISK",
  "execution_context": "string",
  "halt_rationale": "string",
  "associated_escalation_id": "uuid or null",
  "resolution_status": "PENDING | RESOLVED | OVERRIDDEN"
}
```

### B. Halt State Representation

UI MUST clearly represent halt state:

**Visual Distinction**:

| State | Icon | Color | Label |
|-------|------|-------|-------|
| HALTED | ⏸️ | Yellow/Amber | "Halted (Complexity)" |
| BLOCKED | 🚫 | Red | "Blocked (Gate)" |
| FAILED | ❌ | Red | "Failed (Error)" |
| ESCALATED | ⬆️ | Blue | "Escalated" |

**Example UI Representation**:

```
⏸️ HALTED: Complexity Assessment
   FM has proactively halted execution due to cognitive complexity limit.
   
   Reason: Ripple cascade affects 15+ artifacts
   Escalation: esc-20260103-001 (Pending)
   
   [View Halt Details] [View Escalation]
```

### C. Halt vs Failure Distinction

UI MUST make distinction clear:

**HALT** (Proactive):
- "FM has proactively paused execution"
- "Cognitive complexity assessment triggered halt"
- Icon: ⏸️ (Pause)
- Color: Amber/Yellow

**FAILURE** (Reactive):
- "Execution failed due to error"
- "Test failure detected"
- Icon: ❌ (Error)
- Color: Red

---

## V. Capability Selection Observability

### A. Capability Selection Event Stream

FM MUST emit capability selection events:

```json
{
  "event_type": "CAPABILITY_SELECTED | CAPABILITY_SWITCHED",
  "selection_id": "uuid",
  "timestamp": "ISO-8601",
  "task_id": "string",
  "capability_class_selected": "STANDARD | EXTENDED | SPECIALIST | HUMAN",
  "previous_capability": "string or null",
  "selection_rationale": "string",
  "selection_criteria": ["string"]
}
```

### B. Capability History

FM execution surface MUST track:

- **Capability usage** — Which tasks used which capability class
- **Capability switches** — When and why capability class changed
- **Capability effectiveness** — Did Extended/Specialist resolve issue?

### C. Capability UI Representation

UI SHOULD indicate active capability class:

**Example**:

```
🔧 Active Capability: Extended
   Reason: Complex architecture validation required
   Task: Architecture completeness check
   
   [View Capability History]
```

---

## VI. Event Persistence

### A. Event Log Requirements

FM MUST persist all events to structured log:

**Log Location**: `governance/events/fm-execution-log.jsonl` (JSON Lines format)

**Log Entry Structure**:

```json
{
  "event_id": "uuid",
  "timestamp": "ISO-8601",
  "event_category": "STATE_CHANGE | ESCALATION | HALT | CAPABILITY | GATE",
  "event_type": "string",
  "event_data": { /* event-specific structure */ },
  "execution_context": {
    "task_id": "string or null",
    "wave_id": "string or null",
    "program_id": "string or null"
  },
  "immutable": true
}
```

### B. Event Queryability

Events MUST be queryable by:

- **Event category** — All escalations, all halts, etc.
- **Time range** — Events in last 7 days, etc.
- **Task/Wave/Program** — All events for Wave 1.0
- **Event type** — All HALT_TRIGGERED events

---

## VII. Dashboard Requirements

### A. FM Execution Dashboard

FM App SHOULD provide dashboard showing:

1. **Current State** — EXECUTING, HALTED, ESCALATED, etc.
2. **Recent Events** — Last 10 events (escalations, halts, capability switches)
3. **Escalation Summary** — Open escalations, average resolution time
4. **Halt Summary** — Total halts, halt reasons distribution
5. **Capability Usage** — Breakdown of capability class usage
6. **Gate Status** — Current gate states (RED/GREEN)

### B. Escalation Dashboard

FM App SHOULD provide escalation-specific dashboard:

1. **Open Escalations** — All pending escalations
2. **Escalation Details** — Reason, context, indicators
3. **Resolution Status** — Awaiting decision, resolved, overridden
4. **Escalation History** — Resolved escalations with outcomes
5. **Repeat Escalations** — Same issue escalated multiple times

### C. Observability Priority

Dashboards are **SHOULD** (not MUST) for initial activation.

**MUST** requirements are:

- ✅ State model implemented
- ✅ Events emitted and logged
- ✅ Halt/escalation/capability events distinguishable
- ✅ Logs queryable

Dashboards can be added incrementally.

---

## VIII. Implementation Phases

### Phase 1: State Model (MANDATORY for activation)

- [ ] Implement execution state enum
- [ ] Implement state transitions
- [ ] Implement state metadata
- [ ] Log state changes to event log

### Phase 2: Event Emission (MANDATORY for activation)

- [ ] Emit escalation events
- [ ] Emit halt events
- [ ] Emit capability selection events
- [ ] Persist events to structured log

### Phase 3: Basic Observability (MANDATORY for activation)

- [ ] Log file accessible and queryable
- [ ] Events distinguishable (halt vs failure vs block)
- [ ] Escalation status visible in logs
- [ ] Capability selection visible in logs

### Phase 4: UI Representation (Recommended, not blocking)

- [ ] UI shows current execution state
- [ ] UI shows escalation status
- [ ] UI distinguishes halt from failure
- [ ] UI shows capability class

### Phase 5: Dashboards (Future enhancement)

- [ ] FM Execution Dashboard
- [ ] Escalation Dashboard
- [ ] Capability Usage Dashboard

**Activation Gate**: Phases 1-3 MUST be complete. Phases 4-5 are enhancements.

---

## IX. Ripple Requirements

When this specification is activated:

1. **FM Agent Contract** MUST reference this specification
2. **FM Execution Code** MUST implement state model
3. **FM Event Logger** MUST emit required events
4. **FM UI** SHOULD represent states (if UI exists)
5. **Builder Contracts** MUST acknowledge FM state authority

---

## X. Validation Criteria

This specification is successfully implemented when:

1. ✅ FM can transition to HALTED state
2. ✅ FM can emit ESCALATION_INITIATED event
3. ✅ FM can emit HALT_TRIGGERED event
4. ✅ FM can emit CAPABILITY_SELECTED event
5. ✅ Events are logged to structured log file
6. ✅ Events are distinguishable and queryable
7. ✅ Halt is visually/textually distinct from failure
8. ✅ Escalation status is observable
9. ✅ Capability selection is observable
10. ✅ No human inference required to understand state

---

## XI. Enforcement

This specification is **MANDATORY** and **ACTIVATED** as of 2026-01-03.

**Violation Handling**:

- FM execution without state model → **Governance Gap**
- FM escalation without event emission → **Observability Gap**
- FM halt indistinguishable from failure → **Observability Gap**
- Event log missing or inaccessible → **Governance Gap**

---

## XII. References

- **FM_AI_ESCALATION_AND_CAPABILITY_SCALING_SPEC.md** (parent specification)
- **FM_EXECUTION_MANDATE.md** Section VI (STOP and Escalation Semantics)
- **AGENT_CONSTITUTION.md** Section VIII.3 (Escalate When Blocked)
- **PR_GATE_FAILURE_HANDLING_PROTOCOL.md** Section III (Failure Record Schema)

---

**Make governance visible. Make escalation observable. Make halt distinct.**

*END OF FM EXECUTION SURFACE OBSERVABILITY SPECIFICATION*
