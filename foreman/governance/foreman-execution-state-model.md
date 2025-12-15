# Foreman Execution State Model (Minimal)

**Version**: 1.0.0  
**Status**: Temporary Model (Until PIT Implementation)  
**Authority**: Foreman Execution Playbook  
**Last Updated**: 2025-12-15

---

## I. Purpose

This document defines a **minimal execution state model** for Maturion Foreman to track operational state and support resumption after interruption.

**Temporary Status**: This is a simplified model until Platform Intelligence Tracker (PIT) is implemented. PIT will provide comprehensive state management, task tracking, and orchestration capabilities.

**Scope**: Documentation only - no automation or tooling implementation required.

---

## II. Execution States

### State Definitions

Foreman operates in one of these states at any given time:

#### IDLE
**Definition**: No active task, awaiting instruction or monitoring platform.

**Characteristics**:
- No builds in progress
- No pending decisions
- No active escalations
- Available for new work
- May be performing passive monitoring

**Typical Duration**: Variable (minutes to days)

**Next States**: PLANNING (task received)

#### PLANNING
**Definition**: Task received and being analyzed; architecture and QA being designed.

**Characteristics**:
- Task classified (PROGRAM/WAVE/TASK)
- Scope being determined
- Architecture being designed
- QA being designed
- Build plan being created
- Dependencies being mapped

**Typical Duration**: Hours to days (depends on complexity)

**Activities**:
- Load memory and context
- Classify task
- Design architecture
- Validate architecture completeness
- Design QA suite
- Validate QA-of-QA
- Confirm QA RED status
- Create build plan
- Sequence tasks

**Next States**: 
- DESIGN_COMPLETE (planning successful)
- BLOCKED (scope unclear, missing info, dependencies)

#### DESIGN_COMPLETE
**Definition**: Architecture validated, QA validated as RED, ready to issue Build-to-Green.

**Characteristics**:
- Architecture 100% complete and frozen
- QA suite complete, RED status, zero test debt, frozen
- Build-to-Green instruction prepared
- Builder identified
- May be awaiting approval to proceed

**Typical Duration**: Minutes to hours

**Activities**:
- Final architecture validation
- Final QA validation
- Prepare Build-to-Green instruction
- Request approval if needed
- Await green light to proceed

**Next States**:
- BUILDING (Build-to-Green issued)
- WAITING_FOR_DECISION (approval needed)
- BLOCKED (issue discovered before issuing)

#### BUILDING
**Definition**: Build-to-Green issued, builder(s) executing, Design Freeze active.

**Characteristics**:
- One or more builders executing
- Architecture and QA frozen
- Design Freeze active
- Monitoring builder progress
- Responding to escalations
- Evidence being collected

**Typical Duration**: Hours to days

**Activities**:
- Monitor builder progress
- Respond to builder escalations
- Provide guidance when requested
- Track iterations
- Maintain evidence trail
- Enforce Design Freeze

**Next States**:
- COMPLETE (build successful, all tests pass)
- BLOCKED (issue encountered, cannot proceed)
- ABORTED (fundamental issue, must stop)

#### BLOCKED
**Definition**: Execution cannot proceed; waiting for resolution of specific issue.

**Characteristics**:
- Specific blocker identified
- Issue documented
- Resolution path identified (or being investigated)
- May have escalation pending
- Work is paused

**Typical Duration**: Hours to days

**Common Blockers**:
- Unclear scope (needs stakeholder clarification)
- Missing dependency (another task must complete first)
- Architecture-QA mismatch (needs resolution)
- Technical impossibility (architecture needs revision)
- Resource unavailable (builder not available)
- External dependency (waiting for third party)

**Activities**:
- Document blocker clearly
- Investigate resolution options
- Escalate if needed
- Monitor for resolution
- Communicate status

**Next States**:
- PLANNING (blocker resolved, restart design)
- BUILDING (blocker resolved during build, resume)
- ABORTED (cannot resolve, must abandon)
- WAITING_FOR_DECISION (escalated for decision)

#### WAITING_FOR_DECISION
**Definition**: Escalated to Johan or awaiting human approval; cannot proceed until decision received.

**Characteristics**:
- Escalation issued
- Decision clearly articulated
- Options presented
- Waiting for response
- All relevant information provided

**Typical Duration**: Hours to days (business days)

**Common Decision Types**:
- Architectural decision (business logic interpretation)
- Breaking change approval (CS2 required)
- Protected path modification (constitutional change)
- Resource allocation (priority, assignment)
- Scope clarification (what's in/out)
- Security risk acceptance

**Activities**:
- Monitor for decision response
- Answer follow-up questions
- Provide additional information if requested
- Update stakeholders on wait status

**Next States**:
- PLANNING (approved to restart with changes)
- BUILDING (approved to continue build)
- ABORTED (rejected or cannot proceed)

#### COMPLETE
**Definition**: Build finished successfully; all tests passing, evidence validated, ready for merge.

**Characteristics**:
- Builder reported completion
- Evidence reviewed and validated
- 100% tests passing
- Zero test debt
- Build quality validated
- Completion approved by Foreman
- Design Freeze released
- Ready for human approval and merge

**Typical Duration**: Minutes to hours (until merge)

**Activities**:
- Final evidence validation
- Create completion report
- Update memory with lessons learned
- Request human approval (if required)
- Prepare for merge

**Next States**:
- IDLE (task done, merge complete or scheduled)

#### ABORTED
**Definition**: Build stopped before completion; issue could not be resolved during build.

**Characteristics**:
- Build cannot proceed
- Fundamental issue identified
- Architecture or QA needs revision
- Will restart after fixes
- Design Freeze released
- Lessons learned captured

**Typical Duration**: Immediate (transition to IDLE or PLANNING)

**Common Abort Reasons**:
- Architecture fundamentally flawed
- Architecture-QA mismatch cannot be resolved during build
- Impossible requirements discovered
- Critical security issue in design
- Scope too large (needs decomposition)
- Repeated builder failures (3+)

**Activities**:
- Document abort reason clearly
- Capture lessons learned
- Update memory
- Release Design Freeze
- Determine restart path (if applicable)

**Next States**:
- IDLE (task abandoned)
- PLANNING (restart with fixes)

---

## III. State Transition Diagram

### Valid Transitions

```
IDLE
  ↓
PLANNING ←──────────┐
  ↓ ↓               │
  │ BLOCKED ────────┤
  │   ↓             │
  │ WAITING_FOR_DECISION
  │   ↓             │
  ↓   │             │
DESIGN_COMPLETE     │
  ↓                 │
BUILDING ───────────┤
  ↓ ↓               │
  │ BLOCKED ────────┤
  │   ↓             │
  │ WAITING_FOR_DECISION
  │   ↓             │
  │ ABORTED ────────┤
  ↓                 │
COMPLETE            │
  ↓                 │
IDLE ←──────────────┘
```

### Transition Rules

**FROM IDLE**:
- → PLANNING (when task received)

**FROM PLANNING**:
- → DESIGN_COMPLETE (architecture and QA complete)
- → BLOCKED (scope unclear, missing info)

**FROM DESIGN_COMPLETE**:
- → BUILDING (Build-to-Green issued)
- → WAITING_FOR_DECISION (approval needed before building)
- → BLOCKED (issue discovered pre-build)

**FROM BUILDING**:
- → COMPLETE (build successful, all tests pass)
- → BLOCKED (issue encountered during build)
- → ABORTED (fundamental issue, cannot continue)

**FROM BLOCKED**:
- → PLANNING (blocker resolved, restart from design)
- → BUILDING (blocker resolved during build, resume)
- → ABORTED (cannot resolve blocker)
- → WAITING_FOR_DECISION (escalated for decision)

**FROM WAITING_FOR_DECISION**:
- → PLANNING (approved to restart with changes)
- → BUILDING (approved to continue build)
- → ABORTED (rejected or cannot proceed)

**FROM COMPLETE**:
- → IDLE (task done, ready for next task)

**FROM ABORTED**:
- → IDLE (task abandoned)
- → PLANNING (restart with fixes)

---

## IV. State Recording

### Recording Format

Record state transitions in memory:

```json
{
  "scope": "foreman",
  "key": "execution-state-<task-id>-<timestamp>",
  "task_id": "<task-id>",
  "state": "<STATE>",
  "previous_state": "<PREVIOUS_STATE>",
  "reason": "<why state changed>",
  "metadata": {
    "blocker": "<if BLOCKED, what is the blocker>",
    "decision_needed": "<if WAITING_FOR_DECISION, what decision>",
    "abort_reason": "<if ABORTED, why>",
    "completion_summary": "<if COMPLETE, brief summary>"
  },
  "timestamp": "<ISO 8601>"
}
```

### State Query

To determine current state:

```typescript
// Get latest state for task
const latestState = queryMemory({
  scope: 'foreman',
  key_prefix: 'execution-state-<task-id>',
  limit: 1,
  sort: 'timestamp_desc'
})

// Get all state transitions for task
const stateHistory = queryMemory({
  scope: 'foreman',
  key_prefix: 'execution-state-<task-id>',
  limit: 100,
  sort: 'timestamp_asc'
})
```

---

## V. Heartbeat Mechanism

### Purpose

Heartbeat detects if Foreman becomes unresponsive, loses context, or gets stuck in a state.

### Heartbeat Frequency

Record heartbeat at these events:

- State transition
- Builder communication (send/receive)
- Validation completion
- Decision point
- Escalation
- Every 30 minutes if in active state (PLANNING, BUILDING)

### Heartbeat Format

```json
{
  "scope": "foreman",
  "key": "heartbeat-<timestamp>",
  "task_id": "<active-task-id or null>",
  "state": "<current-state>",
  "last_action": "<description of last action>",
  "timestamp": "<ISO 8601>"
}
```

### Heartbeat Monitoring

**Normal Heartbeat Patterns**:
- IDLE: Heartbeat every few hours (passive monitoring)
- PLANNING: Heartbeat every 30-60 minutes (active design)
- DESIGN_COMPLETE: Heartbeat every 15 minutes (preparing to build)
- BUILDING: Heartbeat every 30 minutes (active supervision)
- BLOCKED: Heartbeat every 1-2 hours (waiting for resolution)
- WAITING_FOR_DECISION: Heartbeat every few hours (waiting for human)
- COMPLETE: Heartbeat when transitioning (brief state)
- ABORTED: Heartbeat when transitioning (brief state)

**Anomaly Detection**:

**No Heartbeat**:
- IDLE: No concern (waiting for work)
- PLANNING for 24+ hours without heartbeat: Context likely lost
- BUILDING for 1+ hour without heartbeat: Investigate (may be stuck)
- BLOCKED for 7+ days without heartbeat: Likely forgotten
- WAITING_FOR_DECISION for 7+ days without heartbeat: Escalation lost or ignored

**Rapid Heartbeats**:
- 10+ heartbeats in 1 minute: Possible loop or confusion
- State changing rapidly (multiple transitions per minute): Issue requiring attention

### Heartbeat Failure Response

**If No Heartbeat for Extended Period**:

1. **Review Last Recorded State**:
   - What was Foreman doing?
   - What was the task?
   - What was the last action?

2. **Review Evidence Trail**:
   - Is there evidence of work in progress?
   - Where did it stop?

3. **Determine Context Status**:
   - Is context preserved in memory?
   - Can execution resume from last state?
   - Or is context lost (chat reset, session end)?

4. **Resume or Restart**:
   - If context preserved: Resume from last state
   - If context lost but recoverable: Reload memory and resume
   - If context lost and not recoverable: Escalate to Johan

5. **Document Gap**:
   ```json
   {
     "scope": "foreman",
     "key": "heartbeat-gap-<incident-id>",
     "task_id": "<task-id>",
     "last_heartbeat": "<ISO 8601>",
     "gap_duration_hours": X,
     "resolution": "<how context was restored>",
     "timestamp": "<ISO 8601>"
   }
   ```

---

## VI. State Persistence

### Memory as State Storage

State is stored in **Memory Fabric** (version-controlled JSON/Markdown files).

**Survives**:
- Chat resets
- Context window limits
- Model upgrades
- Repository changes
- Platform restarts

**Does NOT Survive** (without intervention):
- Memory directory deletion
- Repository corruption
- Git history loss

### State Recovery After Interruption

**Step 1: Load Latest State**

```typescript
const latestState = queryMemory({
  scope: 'foreman',
  tags: ['execution-state'],
  limit: 1,
  sort: 'timestamp_desc'
})
```

**Step 2: Validate State Integrity**

Check:
- Does state make sense?
- Is timestamp recent or old?
- Are there pending actions?
- Is task still relevant?

**Step 3: Resume or Reset**

**If state is recent (<24 hours) and valid**:
- Resume from recorded state
- Continue planned actions
- Notify stakeholders of resumption

**If state is old (>24 hours)**:
- Review for relevance
- Check if task still active
- Escalate if unclear
- May need to restart from IDLE

---

## VII. Multi-Task State Management

### Handling Multiple Concurrent Tasks

Foreman may have multiple tasks in different states simultaneously.

**Example**:
- Task A: BUILDING (builder executing)
- Task B: WAITING_FOR_DECISION (escalated to Johan)
- Task C: BLOCKED (waiting for Task A to complete, dependency)
- Task D: PLANNING (new task just received)

### State Tracking Per Task

Each task has independent state:

```json
{
  "scope": "foreman",
  "key": "task-states-snapshot-<timestamp>",
  "tasks": [
    {
      "task_id": "task-a",
      "state": "BUILDING",
      "builder": "ui-builder",
      "started": "2025-12-15T10:00:00Z"
    },
    {
      "task_id": "task-b",
      "state": "WAITING_FOR_DECISION",
      "escalated": "2025-12-14T15:30:00Z",
      "decision_needed": "Breaking change approval"
    },
    {
      "task_id": "task-c",
      "state": "BLOCKED",
      "blocker": "Depends on task-a completion"
    },
    {
      "task_id": "task-d",
      "state": "PLANNING",
      "started": "2025-12-15T14:00:00Z"
    }
  ],
  "timestamp": "<ISO 8601>"
}
```

### State Prioritization

When multiple tasks need attention:

**Priority Order**:
1. **BUILDING** - Active builds need supervision (highest priority)
2. **BLOCKED** - Resolve blockers to unblock progress
3. **WAITING_FOR_DECISION** - Check if decisions received
4. **DESIGN_COMPLETE** - Ready to start, can begin when capacity available
5. **PLANNING** - Continue when higher priorities addressed
6. **COMPLETE** - Can wait briefly for merge approval
7. **ABORTED** - Review lessons, no immediate action

---

## VIII. State Transition Recording Best Practices

### When to Record State Transition

Record immediately when:
- State actually changes (not just planning to change)
- Decision is made that triggers transition
- Event occurs that causes transition

### What to Include in Transition Record

**Always Include**:
- Task ID
- New state
- Previous state
- Reason for transition
- Timestamp

**Include When Relevant**:
- Blocker description (if transitioning to BLOCKED)
- Decision needed (if transitioning to WAITING_FOR_DECISION)
- Abort reason (if transitioning to ABORTED)
- Completion summary (if transitioning to COMPLETE)
- Evidence location
- Next planned action

### State Transition Audit Trail

Complete state transition history provides:
- Full audit trail of task lifecycle
- Visibility into where time was spent
- Identification of common blockers
- Pattern recognition (e.g., "always gets blocked at X")
- Process improvement insights

---

## IX. Integration with Foreman Execution Playbook

This state model supports the Foreman Execution Playbook:

**Playbook Section → State Mapping**:

- **Task Acceptance and Classification** → Transition from IDLE to PLANNING
- **Scope Boundary Determination** → Within PLANNING state
- **When to Design Architecture** → Within PLANNING state
- **When to Design QA** → Within PLANNING state
- **When to Issue Build-to-Green** → Transition from DESIGN_COMPLETE to BUILDING
- **How to Supervise Builders** → Within BUILDING state
- **How to Evaluate Evidence** → Within BUILDING state (continuous) and transition to COMPLETE
- **Completion vs Escalation Decision** → Transition to COMPLETE or BLOCKED/ABORTED/WAITING_FOR_DECISION
- **When Foreman Must STOP** → Transition to BLOCKED or ABORTED
- **When Foreman Must Escalate** → Transition to WAITING_FOR_DECISION
- **When Foreman Must Wait** → BLOCKED or WAITING_FOR_DECISION state

---

## X. Limitations of Minimal Model

### What This Model Does NOT Provide

This minimal model does NOT include:

**Task Tracking**:
- No task assignment tracking
- No task dependencies graph
- No task priority management
- No task deadline tracking

**Builder Coordination**:
- No builder availability tracking
- No builder workload balancing
- No builder communication queue

**Detailed Metrics**:
- No time-in-state analytics
- No performance metrics
- No velocity tracking
- No forecasting

**Automated Workflows**:
- No automatic state transitions
- No automatic escalations
- No automatic notifications
- No scheduled actions

**UI/Dashboard**:
- No visual state representation
- No real-time monitoring interface
- No alerts or notifications

### These Capabilities Require PIT

All advanced features above will be provided by **Platform Intelligence Tracker (PIT)** when implemented.

**PIT Scope**:
- Comprehensive task tracking
- Builder coordination and load balancing
- Dependency management
- State machine automation
- Metrics and analytics
- Alerting and notifications
- Dashboard and visualization
- API for integration

**Current Status**: PIT is planned but not yet implemented.

---

## XI. Transition to PIT

### When PIT is Implemented

PIT will replace this minimal model with:

**Automated State Management**:
- PIT will automatically track state transitions
- PIT will detect anomalies (missing heartbeats, stuck states)
- PIT will trigger notifications for state changes

**Enhanced Visibility**:
- Dashboard showing all tasks and their states
- Visual state machine representation
- Time-in-state analytics
- Bottleneck identification

**Integration**:
- PIT will integrate with memory fabric
- PIT will integrate with builder agents
- PIT will integrate with governance systems

### Migration Path

**Backward Compatibility**:
- Memory-based state records will be preserved
- PIT will import historical state data
- Existing processes will continue to work

**Enhanced Capabilities**:
- PIT will provide additional features
- PIT will not remove existing functionality
- Manual state tracking will remain as fallback

---

## XII. Version and Authority

**Version**: 1.0.0  
**Status**: Active (Temporary Until PIT)  
**Authority**: Foreman Execution Playbook  
**Last Updated**: 2025-12-15  
**Owner**: Johan (MaturionISMS)  
**Maintained By**: Maturion Foreman

**Changelog**:
- 1.0.0 (2025-12-15): Initial minimal execution state model

---

## XIII. Summary

This minimal execution state model provides:

1. ✅ **8 Clear States** - IDLE, PLANNING, DESIGN_COMPLETE, BUILDING, BLOCKED, WAITING_FOR_DECISION, COMPLETE, ABORTED
2. ✅ **State Transition Rules** - Valid transitions defined
3. ✅ **State Recording** - Memory-based persistence
4. ✅ **Heartbeat Mechanism** - Detect unresponsiveness
5. ✅ **Multi-Task Support** - Handle concurrent tasks
6. ✅ **Recovery After Interruption** - Resume from last state

**Temporary until PIT provides comprehensive state management.**

---

*END OF FOREMAN EXECUTION STATE MODEL (MINIMAL)*
