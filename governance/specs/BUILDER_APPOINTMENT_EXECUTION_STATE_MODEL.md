# Builder Appointment Execution State Model

**Version**: 1.0.0  
**Status**: Active  
**Authority**: Governance Layer-Down from `governance/ROLE_APPOINTMENT_PROTOCOL.md`  
**Addresses**: BL-0007 (Irresponsible Appointment of Officials Will Collapse the Model)  
**Last Updated**: 2026-01-03

---

## I. Purpose

This document defines the **execution state model** for tracking builder appointments and execution status within the Maturion Foreman Office App.

**Context**: This model extends `governance/specs/foreman-execution-state-model.md` to provide explicit state tracking for builder appointments, addressing the requirement that appointment completeness and execution state must be **observable, not remembered**.

**Scope**: Documentation and schema specification for state persistence. Implementation is deferred to FM App development cycles.

---

## II. State Categories

Builder appointment and execution are tracked through **three independent state categories**:

### A. Appointment Status (Pre-Execution)

Tracks the **completeness and validity** of builder appointment.

**States**:
- `NOT_APPOINTED`: Builder identified but not yet appointed
- `APPOINTMENT_INCOMPLETE`: Appointment verification in progress
- `APPOINTMENT_COMPLETE`: All verification items passed, builder acknowledged, ready for execution

**Transitions**:
```
NOT_APPOINTED → APPOINTMENT_INCOMPLETE (FM begins appointment verification)
APPOINTMENT_INCOMPLETE → APPOINTMENT_COMPLETE (All verification passed, builder acknowledged)
APPOINTMENT_INCOMPLETE → NOT_APPOINTED (Appointment failed, must restart)
```

**Persistence**: `memory/governance/appointments/<task-id>.json` field: `appointment_status`

---

### B. Execution Status (During Execution)

Tracks the **current execution state** of the builder.

**States**:
- `BLOCKED`: Builder has encountered legitimate blocker requiring FM resolution
- `EXECUTING`: Builder is actively implementing Build-to-Green instructions
- `COMPLETE`: Builder has reached 100% QA green and awaits FM validation

**Transitions**:
```
(none) → EXECUTING (FM authorizes execution after APPOINTMENT_COMPLETE)
EXECUTING → BLOCKED (Builder hits STOP condition)
BLOCKED → EXECUTING (FM resolves blocker, builder resumes)
EXECUTING → COMPLETE (Builder reaches 100% green)
```

**Persistence**: `memory/governance/appointments/<task-id>.json` field: `execution_status`

**Notes**:
- `EXECUTING` is the default active state
- `BLOCKED` is the only permitted pause state (OPOJD enforcement)
- `COMPLETE` is terminal for builder; FM validation required for closure

---

### C. Intervention Status (Exceptional States)

Tracks **FM interventions** that halt or revoke builder execution.

**States**:
- `NONE`: No intervention active
- `HALTED`: FM has halted execution due to complexity (BL-016)
- `REVOKED`: FM has revoked execution due to appointment or mindset violation

**Transitions**:
```
NONE → HALTED (FM detects complexity exceeding manageable threshold)
NONE → REVOKED (FM detects appointment scope violation or mindset violation)
HALTED → NONE (CS2 resolves complexity issue, authorizes resume)
REVOKED → (terminal) (Builder appointment terminated, requires new appointment)
```

**Persistence**: `memory/governance/appointments/<task-id>.json` field: `intervention_status`

**Notes**:
- `HALTED` is recoverable with CS2 authorization
- `REVOKED` is terminal; builder must be re-appointed if work continues
- Interventions override execution status

---

## III. Combined State Logic

The three state categories operate independently but combine to determine overall appointment status:

| Appointment | Execution | Intervention | Effective State | Action Required |
|-------------|-----------|--------------|-----------------|-----------------|
| NOT_APPOINTED | - | - | Idle | FM must initiate appointment |
| APPOINTMENT_INCOMPLETE | - | - | Verification In Progress | FM must complete verification |
| APPOINTMENT_COMPLETE | - | NONE | Ready to Execute | FM must authorize execution |
| APPOINTMENT_COMPLETE | EXECUTING | NONE | Active Execution | Monitor progress |
| APPOINTMENT_COMPLETE | BLOCKED | NONE | Builder Blocked | FM must resolve blocker |
| APPOINTMENT_COMPLETE | COMPLETE | NONE | Awaiting Validation | FM must validate and close |
| APPOINTMENT_COMPLETE | EXECUTING | HALTED | Execution Halted | CS2 must resolve complexity |
| APPOINTMENT_COMPLETE | * | REVOKED | Appointment Revoked | Terminate; new appointment required |

---

## IV. State Persistence Schema

### A. Appointment Record Structure

```json
{
  "scope": "governance",
  "key": "appointment-<task-id>",
  "task_id": "<task-id>",
  "builder_id": "<builder-id>",
  "role": "<role-name>",
  "appointed_by": "Maturion Foreman (FM)",
  "appointed_at": "<ISO-8601-timestamp>",
  
  "appointment_status": "NOT_APPOINTED | APPOINTMENT_INCOMPLETE | APPOINTMENT_COMPLETE",
  "execution_status": "BLOCKED | EXECUTING | COMPLETE",
  "intervention_status": "NONE | HALTED | REVOKED",
  
  "appointment_verification": {
    "builder_contract_current": true,
    "frozen_architecture_available": true,
    "qa_to_red_available": true,
    "appointment_instruction_complete": true,
    "ripple_intelligence_aligned": true,
    "verified_at": "<ISO-8601-timestamp>"
  },
  
  "ripple_alignment": {
    "governance_canon_version": "<version-or-commit-ref>",
    "last_canonical_sync": "<ISO-8601-timestamp>",
    "ripple_status": "STABLE | IN_PROGRESS | CONFLICT",
    "builder_contract_version": "<version>",
    "canonical_authorities_current": true,
    "alignment_confirmed": true,
    "confirmed_at": "<ISO-8601-timestamp>"
  },
  
  "appointment_instruction": {
    "architecture_reference": "<absolute-path>",
    "qa_suite_location": "<absolute-path>",
    "qa_current_status": "RED (<count> tests failing)",
    "acceptance_criteria": "All tests must pass (100%)",
    "scope_boundaries": {
      "in_scope": ["<item-1>", "<item-2>"],
      "not_in_scope": ["<item-1>", "<item-2>"]
    },
    "governance_constraints": [
      "Design Freeze: ACTIVE",
      "Zero Test Debt: MANDATORY",
      "100% QA Pass: REQUIRED",
      "Gate Compliance: MANDATORY"
    ]
  },
  
  "acknowledgment": {
    "acknowledged": true,
    "acknowledged_at": "<ISO-8601-timestamp>",
    "blocking_questions": [],
    "acknowledgment_text": "<full-acknowledgment>"
  },
  
  "execution_log": [
    {
      "timestamp": "<ISO-8601-timestamp>",
      "event": "EXECUTION_AUTHORIZED",
      "details": "FM authorized execution after appointment complete"
    },
    {
      "timestamp": "<ISO-8601-timestamp>",
      "event": "EXECUTION_STARTED",
      "details": "Builder began Build-to-Green execution"
    }
  ],
  
  "intervention_log": [
    {
      "timestamp": "<ISO-8601-timestamp>",
      "intervention_type": "HALTED | REVOKED",
      "reason": "<detailed-reason>",
      "evidence": "<supporting-evidence>",
      "resolution_status": "PENDING | RESOLVED | TERMINAL"
    }
  ],
  
  "completion": {
    "completed": false,
    "completed_at": null,
    "success_criteria_met": false,
    "validation_passed": false,
    "evidence_location": null
  }
}
```

### B. State Update Operations

**Record Creation** (FM initiates appointment):
```json
{
  "appointment_status": "NOT_APPOINTED",
  "execution_status": null,
  "intervention_status": "NONE"
}
```

**Appointment Verification In Progress**:
```json
{
  "appointment_status": "APPOINTMENT_INCOMPLETE",
  "appointment_verification": { ... },
  "ripple_alignment": { ... }
}
```

**Appointment Complete**:
```json
{
  "appointment_status": "APPOINTMENT_COMPLETE",
  "acknowledgment": { "acknowledged": true, ... }
}
```

**Execution Authorized**:
```json
{
  "execution_status": "EXECUTING",
  "execution_log": [ { "event": "EXECUTION_AUTHORIZED", ... } ]
}
```

**Builder Blocked**:
```json
{
  "execution_status": "BLOCKED",
  "execution_log": [ { "event": "BLOCKER_ENCOUNTERED", "details": "..." } ]
}
```

**Builder Complete**:
```json
{
  "execution_status": "COMPLETE",
  "execution_log": [ { "event": "EXECUTION_COMPLETE", ... } ]
}
```

**FM Halts Execution**:
```json
{
  "intervention_status": "HALTED",
  "intervention_log": [ { "intervention_type": "HALTED", "reason": "BL-016: Complexity exceeds threshold", ... } ]
}
```

**FM Revokes Execution**:
```json
{
  "intervention_status": "REVOKED",
  "intervention_log": [ { "intervention_type": "REVOKED", "reason": "Scope violation detected", ... } ]
}
```

---

## V. Observability Requirements

### A. FM Must Be Able to See State

FM MUST NOT rely on memory alone to track appointment and execution state.

**Required Observability**:
- FM can query current appointment status for any task
- FM can query current execution status for any active builder
- FM can query intervention history for any appointment
- FM can verify appointment completeness at any time
- FM can audit execution state transitions

**Storage Location**: `memory/governance/appointments/<task-id>.json`

**Query Operations**:
```python
# Get current appointment state
state = memory.read("governance", f"appointment-{task_id}")

# Check if appointment is complete
is_ready = state["appointment_status"] == "APPOINTMENT_COMPLETE"

# Check if builder is blocked
is_blocked = state["execution_status"] == "BLOCKED"

# Check for interventions
is_intervened = state["intervention_status"] != "NONE"
```

### B. State Must Be Auditable

All state transitions MUST be recorded in `execution_log` or `intervention_log`.

**Audit Trail Requirements**:
- Timestamp for every state change
- Event type and details for every transition
- Authorization trail (who triggered each transition)
- Evidence links for interventions

---

## VI. OPOJD Enforcement via State Model

This state model **enforces OPOJD (One-Prompt One-Job Done)** execution discipline:

### A. No Mid-Execution Pausing

**Permitted States During Execution**:
- `EXECUTING`: Active work
- `BLOCKED`: Legitimate STOP condition encountered
- `COMPLETE`: Work finished

**Prohibited Behaviors** (enforced by state model):
- No "WAITING_FOR_APPROVAL" state
- No "CLARIFICATION_NEEDED" state (unless BLOCKED)
- No "PAUSED" state
- No "IN_REVIEW" state (before COMPLETE)

**Enforcement**: State model does not include non-OPOJD states. Builders cannot transition to states that don't exist.

### B. Continuous Execution from EXECUTING to COMPLETE

**Once in EXECUTING state, builder MUST**:
- Iterate internally to resolve issues
- Only transition to BLOCKED on STOP conditions
- Only transition to COMPLETE on 100% green

**State model prevents**:
- Multiple approval checkpoints
- Stepwise execution with pauses
- "Check before I continue" patterns

---

## VII. Ripple Intelligence Integration

### A. Ripple Alignment Pre-Condition

Builder appointment **CANNOT proceed** to `APPOINTMENT_COMPLETE` unless:
```json
"ripple_alignment": {
  "alignment_confirmed": true,
  "ripple_status": "STABLE"
}
```

**Enforcement**: State transition logic MUST verify ripple alignment before allowing `APPOINTMENT_COMPLETE`.

### B. Ripple Alignment Verification

FM MUST verify ripple alignment using the procedure defined in `governance/ROLE_APPOINTMENT_PROTOCOL.md` Section IV-A:

1. Check governance canon status
2. Verify builder contract currency
3. Evaluate ripple status
4. Document confirmation

**Storage**: Ripple alignment record stored in `ripple_alignment` field of appointment record.

---

## VIII. Integration with Existing State Models

### A. Relationship to FM Execution State Model

This model **extends** `governance/specs/foreman-execution-state-model.md`:

**FM Execution States** (high-level):
- IDLE
- PLANNING
- DESIGN_COMPLETE
- BUILDING
- VALIDATING
- COMPLETE
- BLOCKED

**Builder Appointment States** (detail-level):
- Tracked within FM's `BUILDING` state
- Provides fine-grained execution visibility
- Enables FM monitoring of individual builders

**Integration**: When FM is in `BUILDING` state, FM monitors builder appointment states via this model.

### B. Relationship to Task Tracking

This model **complements** task tracking:

**Task Tracking**: Overall build wave progress (Wave 1.0, Wave 1.1, etc.)
**Appointment Tracking**: Individual builder execution within tasks

**Example**:
- Task: "BUILD-FM-WAVE1-UI-001"
- Task Status: "IN_PROGRESS"
- Builder Appointment Status: "APPOINTMENT_COMPLETE"
- Builder Execution Status: "EXECUTING"

---

## IX. Implementation Guidance

### A. Storage Implementation

**Recommended Storage**:
- Memory Fabric: `memory/governance/appointments/<task-id>.json`
- Database: If FM App implements database, store in `builder_appointments` table

**Schema Validation**:
- Use JSON Schema to validate appointment records
- Enforce state transition rules programmatically

### B. State Transition Logic

**Recommended Implementation**:
```python
class BuilderAppointmentStateMachine:
    def __init__(self, task_id):
        self.task_id = task_id
        self.state = self._load_state()
    
    def verify_appointment(self):
        """Perform appointment verification."""
        self.state["appointment_status"] = "APPOINTMENT_INCOMPLETE"
        # ... verification logic ...
        if all_verified:
            self.state["appointment_status"] = "APPOINTMENT_COMPLETE"
        self._save_state()
    
    def authorize_execution(self):
        """Authorize builder execution."""
        if self.state["appointment_status"] != "APPOINTMENT_COMPLETE":
            raise InvalidTransition("Cannot execute: appointment not complete")
        
        self.state["execution_status"] = "EXECUTING"
        self._log_event("EXECUTION_AUTHORIZED")
        self._save_state()
    
    def halt_execution(self, reason, evidence):
        """FM halts execution (BL-016)."""
        self.state["intervention_status"] = "HALTED"
        self._log_intervention("HALTED", reason, evidence)
        self._save_state()
    
    def revoke_execution(self, reason, evidence):
        """FM revokes execution (violation)."""
        self.state["intervention_status"] = "REVOKED"
        self._log_intervention("REVOKED", reason, evidence)
        self._save_state()
```

### C. Query Interface

**Recommended Query Interface**:
```python
def get_appointment_state(task_id):
    """Get current appointment state."""
    return memory.read("governance", f"appointment-{task_id}")

def is_builder_ready_to_execute(task_id):
    """Check if builder can execute."""
    state = get_appointment_state(task_id)
    return (
        state["appointment_status"] == "APPOINTMENT_COMPLETE" and
        state["intervention_status"] == "NONE"
    )

def get_blocked_builders():
    """Get all blocked builders."""
    # Query all appointments with execution_status == "BLOCKED"
    pass
```

---

## X. Validation and Testing

### A. State Model Validation

**Required Validations**:
- State transitions follow permitted paths only
- Ripple alignment enforced before APPOINTMENT_COMPLETE
- OPOJD enforcement (no non-OPOJD states exist)
- Intervention logging complete
- Audit trail integrity

### B. Test Scenarios

**Test 1: Successful Appointment and Execution**
```
NOT_APPOINTED → APPOINTMENT_INCOMPLETE → APPOINTMENT_COMPLETE → EXECUTING → COMPLETE
```

**Test 2: Appointment Failure**
```
NOT_APPOINTED → APPOINTMENT_INCOMPLETE → NOT_APPOINTED (verification failed)
```

**Test 3: Builder Blocked**
```
EXECUTING → BLOCKED (STOP condition) → EXECUTING (FM resolves) → COMPLETE
```

**Test 4: FM Halts Execution**
```
EXECUTING → HALTED (BL-016) → (CS2 resolves) → EXECUTING → COMPLETE
```

**Test 5: FM Revokes Execution**
```
EXECUTING → REVOKED (violation) → (terminal, new appointment required)
```

---

## XI. Success Criteria

This state model is successful when:

1. ✅ FM cannot appoint builder without explicit state verification
2. ✅ Appointment completeness is observable, not remembered
3. ✅ OPOJD discipline is enforced by state model (no non-OPOJD states)
4. ✅ FM can see all builder execution states at any time
5. ✅ Interventions (HALT, REVOKE) are explicitly tracked
6. ✅ Ripple alignment is pre-condition for appointment completion
7. ✅ State transitions are auditable
8. ✅ Wave 1.0.7 failure mode cannot recur due to state visibility

---

## XII. References

**Authoritative Governance**:
- `governance/ROLE_APPOINTMENT_PROTOCOL.md` — Appointment protocol
- `governance/canon/BOOTSTRAP_EXECUTION_LEARNINGS.md` — BL-0007, BL-016
- `BUILD_PHILOSOPHY.md` Section IX — OPOJD
- `governance/specs/foreman-execution-state-model.md` — FM execution states

**Agent Contracts**:
- `.github/agents/ForemanApp-agent.md` Section XII-A — FM appointment authority
- `.github/agents/*-builder.md` — Builder appointment compliance

**Ripple Intelligence**:
- `governance/specs/FM_RIPPLE_INTELLIGENCE_SPEC.md` — Ripple responsibilities
- `governance/alignment/GOVERNANCE_RIPPLE_COMPATIBILITY.md` — Ripple canon

---

## XIII. Version and Authority

**Version**: 1.0.0  
**Status**: Active  
**Authority**: Governance Layer-Down (Constitutional)  
**Last Updated**: 2026-01-03  
**Owner**: Maturion Foreman (FM)  
**Enforcer**: FM App Execution Surface

---

*END OF BUILDER APPOINTMENT EXECUTION STATE MODEL*
