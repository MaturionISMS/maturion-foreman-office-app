# Build Tree Execution Model (G-C8)

**Version**: 1.0.0  
**Status**: Active  
**Authority**: FM Functional Specification  
**Last Updated**: 2025-12-25  
**Owner**: Johan (MaturionISMS)  
**Code**: G-C8

---

## I. Purpose

This document defines the **canonical build tree structure** and **execution state hierarchy** for the Maturion FM build system.

The build tree represents the hierarchical decomposition of work from strategic initiatives down to atomic execution units, along with their execution states, activation states, and commissioning evidence.

**Scope**: This is a governance and data model specification. It defines WHAT the tree is and HOW states propagate. It does NOT define UI implementation.

---

## II. Hierarchical Structure

### 2.1 Core Hierarchy

The FM build system organizes work in a 3-level hierarchy:

```
Program
  ├─ Wave 1
  │   ├─ Task 1.1
  │   ├─ Task 1.2
  │   └─ Task 1.3
  ├─ Wave 2
  │   ├─ Task 2.1
  │   └─ Task 2.2
  └─ Wave 3
      └─ Task 3.1
```

### 2.2 Node Definitions

#### Program
**Definition**: High-level strategic initiative or goal

**Characteristics**:
- Contains multiple waves
- Has overall success criteria
- Tracks aggregate progress
- Represents long-term deliverable (weeks to months)

**Examples**:
- "Implement ISO 27001 Annex A.1"
- "Build Multi-Module ISMS Platform"
- "Governance Hardening Wave 2.6"

**State Properties**:
- Execution state (derived from waves)
- Activation state (can be DRAFT, ACTIVE, SUSPENDED, COMPLETED, ARCHIVED)
- Overall completion percentage
- Risk status (Red/Amber/Green)

#### Wave
**Definition**: Ordered phase within a program containing related tasks

**Characteristics**:
- Part of exactly one program
- Contains multiple tasks
- Executes in sequence (Wave N must complete before Wave N+1 starts)
- Has completion criteria
- Dependencies between waves enforced

**Examples**:
- "Wave 0: Foundation Setup"
- "Wave 1: Multi-Module Skeleton"
- "Wave 1.1: Global UI Shell"
- "Wave 2: Core Functionality"

**State Properties**:
- Execution state (derived from tasks)
- Activation state (can be PLANNED, READY, IN_PROGRESS, BLOCKED, COMPLETE)
- Completion percentage (tasks complete / tasks total)
- Risk status (Red/Amber/Green)
- Blocker information (if BLOCKED)

#### Task
**Definition**: Atomic unit of work assigned to a builder

**Characteristics**:
- Part of exactly one wave
- Assigned to a single builder agent
- Has clear definition and acceptance criteria
- Has evidence requirements
- Executes independently within wave constraints
- Represents hours to days of work

**Examples**:
- "Design PIT schema architecture"
- "Implement QA test suite for ERM"
- "Build UI component library"
- "Create API endpoints for Risk Assessment"

**State Properties**:
- Execution state (PLANNED, IN_PROGRESS, BLOCKED, COMPLETE, ABORTED)
- Activation state (ASSIGNED, APPROVED, EXECUTING, REVIEW, MERGED)
- Completion percentage (0% or 100%, no partial)
- Risk status (Red/Amber/Green)
- Builder assignment
- Evidence artifacts
- PR links

### 2.3 Optional Sub-Structure: Sub-Waves

For complex waves, an optional **Sub-Wave** level may be introduced:

```
Program
  └─ Wave 1
      ├─ Sub-Wave 1.1
      │   ├─ Task 1.1.1
      │   └─ Task 1.1.2
      └─ Sub-Wave 1.2
          └─ Task 1.2.1
```

**Sub-Wave** is functionally equivalent to Wave but indicates logical grouping within a parent wave.

**Use When**:
- Wave contains >10 tasks
- Tasks naturally cluster by builder, module, or feature
- Parallel execution tracks needed

**State Properties**: Same as Wave

---

## III. Execution States

### 3.1 Task-Level Execution States

Tasks follow the state model defined in `foreman-execution-state-model.md`:

- **PLANNED**: Task defined, not started
- **IN_PROGRESS**: Builder actively executing
- **BLOCKED**: Cannot proceed, waiting for resolution
- **COMPLETE**: All acceptance criteria met, 100% QA pass, evidence validated
- **ABORTED**: Abandoned, will not complete

### 3.2 Wave-Level Execution States

Waves derive their state from constituent tasks:

- **PLANNED**: All tasks PLANNED
- **READY**: All dependencies satisfied, can start
- **IN_PROGRESS**: At least one task IN_PROGRESS, none BLOCKED
- **BLOCKED**: At least one task BLOCKED
- **COMPLETE**: All tasks COMPLETE

**State Transition Rules**:
- PLANNED → READY (when dependencies satisfied)
- READY → IN_PROGRESS (when first task starts)
- IN_PROGRESS → BLOCKED (when any task becomes BLOCKED)
- BLOCKED → IN_PROGRESS (when all blockers resolved)
- IN_PROGRESS → COMPLETE (when all tasks COMPLETE)

### 3.3 Program-Level Execution States

Programs derive their state from constituent waves:

- **DRAFT**: Program defined, waves not finalized
- **ACTIVE**: At least one wave IN_PROGRESS
- **SUSPENDED**: Temporarily paused
- **COMPLETE**: All waves COMPLETE
- **ARCHIVED**: Completed and archived

---

## IV. Activation States

Activation states track the **approval and authorization** status independent of execution progress.

### 4.1 Activation State Definitions

#### DRAFT
**Meaning**: Not yet approved for execution

**Applies To**: Programs, Waves

**Properties**:
- Planning in progress
- Architecture may be incomplete
- Not authorized to start execution
- Can be edited freely

#### APPROVED
**Meaning**: Authorized to execute

**Applies To**: Programs, Waves, Tasks

**Properties**:
- Architecture complete and validated
- QA designed and RED status confirmed
- Build-to-Green instruction prepared
- Ready to assign to builder

#### ACTIVE
**Meaning**: Currently executing

**Applies To**: Programs, Waves, Tasks

**Properties**:
- Builder assigned (Tasks)
- Execution in progress
- Design Freeze active
- Progress being monitored

#### REVIEW
**Meaning**: Execution complete, awaiting validation

**Applies To**: Tasks

**Properties**:
- Builder reports completion
- Evidence submitted
- QA results available
- Foreman reviewing

#### MERGED
**Meaning**: Accepted and merged

**Applies To**: Tasks

**Properties**:
- Evidence validated
- QA 100% pass
- PR merged
- Artifact preserved

#### BLOCKED
**Meaning**: Activation cannot proceed due to dependency or blocker

**Applies To**: Programs, Waves, Tasks

**Properties**:
- Specific blocker identified
- Resolution path defined or being investigated
- Execution paused

### 4.2 Activation State Transitions

**Task Activation Flow**:
```
DRAFT → APPROVED → ACTIVE → REVIEW → MERGED
         ↓           ↓         ↓
       BLOCKED ←───────────────┘
```

**Wave/Program Activation Flow**:
```
DRAFT → APPROVED → ACTIVE → COMPLETE
         ↓           ↓
       BLOCKED ←─────┘
```

---

## V. Commissioning Evidence

Every node in the build tree tracks **commissioning evidence** — artifacts proving completion and compliance.

### 5.1 Evidence Categories

#### Architecture Evidence
- Architecture document (Markdown)
- Component diagrams
- Data models
- API specifications
- Integration contracts

#### QA Evidence
- QA test suite (code)
- QA execution results (logs, JSON)
- QA-of-QA validation report
- Test coverage metrics
- DP-RED registry entries

#### Build Evidence
- PR link (GitHub)
- Code diff
- CI/CD logs
- Build artifacts
- Deployment confirmation

#### Completion Evidence
- Evidence validation report
- Foreman sign-off
- Merge confirmation
- Memory entries (decisions, learnings)

### 5.2 Evidence Requirements by Level

**Task**:
- MUST have architecture evidence
- MUST have QA evidence (100% pass)
- MUST have build evidence (PR)
- MUST have completion evidence (validation report)

**Wave**:
- MUST have planning document
- MUST have all task evidence
- MAY have wave-level summary report

**Program**:
- MUST have program charter
- MUST have all wave evidence
- MUST have program completion report

### 5.3 Evidence Validation Rules

**Task cannot transition to COMPLETE unless**:
- Architecture document exists and is validated
- QA suite exists and shows 100% pass
- Zero test debt
- PR merged
- Evidence validation report exists

**Wave cannot transition to COMPLETE unless**:
- All tasks COMPLETE
- All task evidence validated

**Program cannot transition to COMPLETE unless**:
- All waves COMPLETE
- All wave evidence validated
- Program completion report created

---

## VI. Status Indicators (Red/Amber/Green)

Status indicators provide at-a-glance health assessment independent of execution/activation states.

### 6.1 Status Definitions

#### Green ✅
**Meaning**: Healthy, on track, no issues

**Criteria**:
- Execution state matches expected state
- No blockers
- Progress within tolerance
- All governance checks pass

#### Amber ⚠️
**Meaning**: Attention needed, potential risk

**Criteria**:
- Minor deviations detected
- Progress slower than expected
- Non-critical blockers present
- QA pass rate <100% but >90%
- Approaching deadline

#### Red 🔴
**Meaning**: Critical issue, immediate action required

**Criteria**:
- Execution blocked
- Critical governance violation
- QA pass rate <90%
- Deadline missed
- Architecture-QA mismatch
- Constitutional violation

### 6.2 Status Roll-Up Rules

**Task Status**: Determined by task's own state and progress

**Wave Status**: **WORST-CASE PROPAGATION**
- If ANY task is RED → Wave is RED
- Else if ANY task is AMBER → Wave is AMBER
- Else → Wave is GREEN

**Program Status**: **WORST-CASE PROPAGATION**
- If ANY wave is RED → Program is RED
- Else if ANY wave is AMBER → Program is AMBER
- Else → Program is GREEN

**Critical Rule**: Parent status MUST NEVER be better than worst child status.

---

## VII. Completion Percentage

### 7.1 Calculation Rules

**Task Completion**:
- 0% (not started or in progress)
- 100% (COMPLETE state only)

**Wave Completion**:
```
wave_completion = (completed_tasks / total_tasks) * 100
```

**Program Completion**:
```
program_completion = (completed_waves / total_waves) * 100
```

OR (for weighted calculation):
```
program_completion = SUM(wave_weight * wave_completion) / SUM(wave_weight)
```

### 7.2 Percentage vs. Authorization

**CRITICAL RULE**: Completion percentage is **informational ONLY**.

- 100% completion does NOT mean ready to merge
- 100% completion does NOT authorize next phase
- Authorization comes from Activation State + Evidence Validation
- Percentage shows progress, not readiness

**Why This Matters**:
- Prevents "almost done" syndrome
- Enforces evidence-based authorization
- Prevents premature handover
- Maintains governance rigor

---

## VIII. Deterministic Roll-Up

### 8.1 Roll-Up Principles

1. **State Propagation**: Child states determine parent states
2. **Worst-Case Wins**: Parent status = worst child status
3. **No Optimism**: Parent never better than worst child
4. **Explainability**: Roll-up logic must be auditable
5. **Automation**: Roll-up must be computed, never guessed

### 8.2 Roll-Up Algorithm

**For each parent node**:

1. **Collect child states**
   ```
   child_states = [state for each child]
   ```

2. **Determine parent execution state**
   - If ALL children COMPLETE → Parent COMPLETE
   - Else if ANY child BLOCKED → Parent BLOCKED
   - Else if ANY child IN_PROGRESS → Parent IN_PROGRESS
   - Else if ALL children PLANNED → Parent PLANNED
   - Else → Parent READY

3. **Determine parent status (Red/Amber/Green)**
   - If ANY child RED → Parent RED
   - Else if ANY child AMBER → Parent AMBER
   - Else → Parent GREEN

4. **Calculate parent completion**
   ```
   parent_completion = (completed_children / total_children) * 100
   ```

5. **Propagate blocking information**
   - If parent BLOCKED, identify which child(ren) are BLOCKED
   - Attach blocker descriptions to parent

### 8.3 Roll-Up Frequency

**Real-Time**: Roll-up MUST update immediately when any child state changes

**Never Manual**: Roll-up MUST be automatic, never manually set

---

## IX. Real-Time Updates

### 9.1 Update Mechanisms

**Polling** (Minimum Viable):
- Client polls server every N seconds (e.g., 5-10 seconds)
- Server returns full tree or incremental changes
- Simple to implement

**Event-Driven** (Preferred):
- Server pushes updates to client via WebSocket/SSE
- Client receives state changes immediately
- Efficient, scales better

**Hybrid** (Recommended):
- Event-driven for active sessions
- Polling as fallback
- Heartbeat mechanism to detect stale connections

### 9.2 Update Scope

**Full Tree Refresh**:
- Use for initial load
- Use after network reconnection
- Use after extended idle

**Incremental Updates**:
- Send only changed nodes
- Include node ID, new state, new status
- Client merges changes into tree

**Optimistic Updates**:
- Client may render expected state immediately
- Server confirms or corrects
- Rollback if server rejects

---

## X. Data Model Specification

### 10.1 Program Node

```typescript
interface ProgramNode {
  id: string;                      // Unique identifier
  type: 'program';
  name: string;                    // Display name
  description: string;
  
  // State
  execution_state: 'DRAFT' | 'ACTIVE' | 'SUSPENDED' | 'COMPLETE' | 'ARCHIVED';
  activation_state: 'DRAFT' | 'APPROVED' | 'ACTIVE' | 'BLOCKED' | 'COMPLETE';
  status: 'RED' | 'AMBER' | 'GREEN';
  
  // Progress
  completion_percentage: number;   // 0-100
  
  // Children
  waves: WaveNode[];
  
  // Evidence
  evidence: Evidence[];
  
  // Metadata
  created_at: string;              // ISO 8601
  updated_at: string;
  owner: string;                   // Johan, typically
}
```

### 10.2 Wave Node

```typescript
interface WaveNode {
  id: string;
  type: 'wave' | 'sub-wave';
  name: string;
  description: string;
  sequence_number: number;         // Order within program
  
  // State
  execution_state: 'PLANNED' | 'READY' | 'IN_PROGRESS' | 'BLOCKED' | 'COMPLETE';
  activation_state: 'DRAFT' | 'APPROVED' | 'ACTIVE' | 'BLOCKED' | 'COMPLETE';
  status: 'RED' | 'AMBER' | 'GREEN';
  
  // Progress
  completion_percentage: number;
  tasks_total: number;
  tasks_complete: number;
  
  // Dependencies
  dependencies: string[];          // IDs of prerequisite waves
  
  // Children
  tasks: TaskNode[];
  sub_waves?: WaveNode[];          // Optional sub-structure
  
  // Blockers
  blockers: Blocker[];
  
  // Evidence
  evidence: Evidence[];
  
  // Metadata
  created_at: string;
  updated_at: string;
}
```

### 10.3 Task Node

```typescript
interface TaskNode {
  id: string;
  type: 'task';
  name: string;
  description: string;
  
  // State
  execution_state: 'PLANNED' | 'IN_PROGRESS' | 'BLOCKED' | 'COMPLETE' | 'ABORTED';
  activation_state: 'DRAFT' | 'APPROVED' | 'ACTIVE' | 'REVIEW' | 'MERGED' | 'BLOCKED';
  status: 'RED' | 'AMBER' | 'GREEN';
  
  // Progress
  completion_percentage: 0 | 100;  // Binary for tasks
  
  // Assignment
  builder: string;                 // ui-builder, api-builder, etc.
  assigned_at?: string;
  
  // Blockers
  blockers: Blocker[];
  
  // Evidence
  evidence: Evidence[];
  pr_link?: string;
  
  // Metadata
  created_at: string;
  updated_at: string;
  started_at?: string;
  completed_at?: string;
}
```

### 10.4 Supporting Types

```typescript
interface Blocker {
  id: string;
  type: 'SCOPE' | 'DEPENDENCY' | 'ARCHITECTURE' | 'QA' | 'TECHNICAL' | 'GOVERNANCE' | 'EXTERNAL';
  description: string;
  severity: 'MINOR' | 'MAJOR' | 'CRITICAL';
  created_at: string;
  resolved_at?: string;
  resolution?: string;
}

interface Evidence {
  id: string;
  category: 'ARCHITECTURE' | 'QA' | 'BUILD' | 'COMPLETION';
  artifact_type: string;           // 'markdown', 'json', 'pr', 'report'
  artifact_location: string;       // URL or path
  validated: boolean;
  validated_at?: string;
  validated_by?: string;
}
```

---

## XI. Governance Integration

### 11.1 GSR Enforcement

The build tree model enforces **Governance Supremacy Rule (GSR)**:

1. **100% QA Passing**:
   - Task cannot be COMPLETE unless QA 100% pass
   - Wave cannot be COMPLETE unless all tasks 100% QA pass
   - Status = RED if any QA failures

2. **Zero Test Debt**:
   - Evidence must include zero test debt confirmation
   - Skipped tests trigger RED status

3. **Architecture Conformance**:
   - Evidence must include architecture validation
   - Deviations trigger escalation

4. **Constitutional Protection**:
   - Protected path modifications trigger RED status
   - CS2 approval required to proceed

### 11.2 Build Philosophy Alignment

The build tree enforces **Five Build Philosophy Principles**:

1. **One-Time Build Correctness**: Task cannot start unless architecture 100% complete
2. **Zero Regression**: Evidence must include regression test results
3. **Full Architectural Alignment**: Architecture validation required
4. **Zero Loss of Context**: All decisions captured in evidence
5. **Zero Ambiguity**: Acceptance criteria must be explicit and testable

---

## XII. API Contract (Informational)

While this is a governance spec, here is the expected API shape for implementation:

### 12.1 Read Operations

```typescript
// Get full tree for a program
GET /api/build-tree/:program_id

// Get wave with tasks
GET /api/build-tree/wave/:wave_id

// Get task details
GET /api/build-tree/task/:task_id
```

### 12.2 State Updates

```typescript
// Update task state (Foreman only)
PATCH /api/build-tree/task/:task_id/state
{
  execution_state: 'IN_PROGRESS',
  activation_state: 'ACTIVE'
}

// Report blocker (Builder can report, Foreman validates)
POST /api/build-tree/task/:task_id/blocker
{
  type: 'TECHNICAL',
  description: '...',
  severity: 'MAJOR'
}
```

### 12.3 Real-Time Subscriptions

```typescript
// WebSocket connection
WS /api/build-tree/subscribe/:program_id

// Messages
{
  type: 'STATE_CHANGE',
  node_id: 'task-123',
  execution_state: 'COMPLETE',
  status: 'GREEN',
  timestamp: '...'
}
```

---

## XIII. Summary

This Build Tree Execution Model (G-C8) defines:

1. ✅ **Hierarchical Structure**: Program → Wave → Task (with optional Sub-Wave)
2. ✅ **Execution States**: PLANNED, IN_PROGRESS, BLOCKED, COMPLETE, ABORTED
3. ✅ **Activation States**: DRAFT, APPROVED, ACTIVE, REVIEW, MERGED, BLOCKED
4. ✅ **Status Indicators**: Red, Amber, Green (worst-case propagation)
5. ✅ **Commissioning Evidence**: Architecture, QA, Build, Completion
6. ✅ **Deterministic Roll-Up**: Parent states derived from children
7. ✅ **Real-Time Updates**: Polling or event-driven
8. ✅ **Data Models**: TypeScript interfaces for nodes
9. ✅ **Governance Integration**: GSR + Build Philosophy enforcement
10. ✅ **Completion Percentage**: Informational only, never authorizes

**This is a governance specification. UI implementation is defined in separate dashboard specs.**

---

## XIV. Version and Authority

**Version**: 1.0.0  
**Status**: Active  
**Authority**: FM Functional Specification  
**Last Updated**: 2025-12-25  
**Owner**: Johan (MaturionISMS)  
**Maintained By**: Maturion Foreman  
**Code**: G-C8

**Changelog**:
- 1.0.0 (2025-12-25): Initial Build Tree Execution Model

---

*END OF BUILD TREE EXECUTION MODEL (G-C8)*
