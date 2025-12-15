# FOREMAN_ARCHITECTURE_v1.0.md

## Johan's Foreman Office — Complete Architecture Specification

**Version**: 1.0  
**Date**: 2025-12-15  
**Status**: Constitutional Authority  
**Aligned to**: APP_DESCRIPTION.md, Architecture Design Checklist v1.1.0

---

## 1. ARCHITECTURAL OVERVIEW

### 1.1 System Purpose

Johan's Foreman Office is an always-on supervisory application that provides persistent governance, orchestration, and monitoring for AI-assisted software development in the Maturion ISMS ecosystem.

### 1.2 Core Architecture Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                     Johan (Human Governor)                   │
│                    Live Interaction Surface                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────────┐
│                   FOREMAN OFFICE (Core)                      │
│  ┌─────────────┐ ┌──────────────┐ ┌────────────────────┐  │
│  │  Planning   │ │ Governance   │ │   Monitoring &     │  │
│  │   Engine    │ │   Engine     │ │  Stall Detection   │  │
│  └─────────────┘ └──────────────┘ └────────────────────┘  │
│  ┌─────────────┐ ┌──────────────┐ ┌────────────────────┐  │
│  │ Orchestration│ │  Evidence &  │ │    Provenance      │  │
│  │   Engine    │ │  Audit Trail │ │     Tracking       │  │
│  └─────────────┘ └──────────────┘ └────────────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────────┐
│                    Builder Agents                            │
│  [UI] [API] [Schema] [Integration] [QA]                     │
└─────────────────────────────────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────────┐
│                  Maturion ISMS Modules                       │
└─────────────────────────────────────────────────────────────┘
```

### 1.3 Key Architectural Principles

1. **Persistent Supervision**: Never sleeps, maintains context across sessions
2. **Governance First**: All rules enforced automatically before execution
3. **Evidence-Driven**: Complete audit trail for every action
4. **Fail-Safe**: Builder failures do not collapse the program
5. **PIT-Ready**: Execution telemetry designed to emerge as PIT naturally

---

## 2. DOMAIN / BUSINESS LOGIC ARCHITECTURE

### 2.1 Core Domain Concepts

#### Program
**Definition**: A high-level initiative with objectives, scope, and success criteria

**Properties**:
- `program_id` (UUID)
- `name` (string)
- `description` (text)
- `objectives` (array of strings)
- `state` (enum: planned, in-progress, blocked, completed, failed)
- `progress_percentage` (0-100)
- `created_at`, `updated_at` (timestamps)
- `evidence_location` (path)

**Invariants**:
- Program must have at least one wave
- Program cannot be marked completed if any wave is failed
- Program progress = weighted average of wave progress

#### Wave
**Definition**: Ordered, dependency-aware execution phase containing related tasks

**Properties**:
- `wave_id` (UUID)
- `program_id` (foreign key)
- `name` (string)
- `sequence_number` (integer)
- `dependencies` (array of wave_ids)
- `state` (enum: planned, in-progress, blocked, completed, failed)
- `progress_percentage` (0-100)
- `created_at`, `updated_at` (timestamps)

**Invariants**:
- Wave sequence numbers must be unique within program
- Wave cannot start if dependencies are not completed
- Wave progress = average of task progress
- Wave cannot be marked completed if any task is failed

#### Task
**Definition**: Atomic build unit with clear architecture, QA, and acceptance criteria

**Properties**:
- `task_id` (UUID)
- `wave_id` (foreign key)
- `name` (string)
- `architecture_reference` (path)
- `qa_suite_location` (path)
- `acceptance_criteria` (text)
- `assigned_builder` (enum: ui, api, schema, integration, qa)
- `state` (enum: planned, assigned, in-progress, blocked, completed, failed)
- `progress_percentage` (0-100)
- `created_at`, `updated_at`, `started_at`, `completed_at` (timestamps)
- `evidence_location` (path)

**Invariants**:
- Task must reference existing architecture document
- Task must reference existing QA suite
- Task cannot be assigned if architecture or QA is incomplete
- Task cannot be marked completed if acceptance criteria not met
- Task must have evidence trail before completion

#### Builder
**Definition**: Execution agent responsible for implementing code according to specifications

**Properties**:
- `builder_id` (enum: ui-builder, api-builder, schema-builder, integration-builder, qa-builder)
- `backend_type` (enum: local, hosted, burst)
- `current_task_id` (nullable foreign key)
- `state` (enum: idle, active, blocked, failed)
- `last_heartbeat` (timestamp)
- `provenance` (JSON: model, escalation_rationale)

**Invariants**:
- Builder can only work on one task at a time
- Builder must send heartbeat every 60 seconds during execution
- Builder cannot start new task if previous task is incomplete

#### Blocker
**Definition**: Impediment preventing task or wave progress

**Properties**:
- `blocker_id` (UUID)
- `entity_type` (enum: program, wave, task)
- `entity_id` (UUID)
- `classification` (enum: architecture_qa_mismatch, impossible_requirements, protected_path, repeated_failures, constitutional_violation)
- `description` (text)
- `detected_at` (timestamp)
- `resolved_at` (nullable timestamp)
- `resolution_action` (nullable text)

**Invariants**:
- Blocker must be associated with existing entity
- Blocked entity cannot progress until blocker resolved
- Blocker resolution must be logged in evidence trail

### 2.2 Business Rules

#### BR-1: Architecture Completeness Rule
**Rule**: No task may be assigned to a builder unless architecture passes 100% of checklist validation

**Logic**:
```
IF task.architecture_reference NOT validated THEN
    REJECT task assignment
    LOG governance_violation
    RETURN error("Architecture incomplete")
END IF
```

#### BR-2: QA Completeness Rule
**Rule**: No task may be assigned unless QA suite exists and is RED (failing tests)

**Logic**:
```
IF task.qa_suite_location NOT exists THEN
    REJECT task assignment
    LOG governance_violation
    RETURN error("QA suite missing")
END IF

IF qa_status NOT = "RED" THEN
    REJECT task assignment
    LOG governance_violation
    RETURN error("QA must be RED before build")
END IF
```

#### BR-3: Zero Test Debt Rule
**Rule**: No task may be marked completed if any test debt exists

**Logic**:
```
IF test_debt_count > 0 THEN
    REJECT task completion
    LOG quality_integrity_incident
    RETURN error("Test debt detected: " + test_debt_details)
END IF
```

**Test Debt Includes**:
- Failing tests
- Skipped tests (.skip(), .todo(), commented out)
- Incomplete tests (stubs, no assertions, TODO comments)
- Incomplete test infrastructure

#### BR-4: Governance Supremacy Rule (GSR)
**Rule**: Governance violations halt execution automatically

**Logic**:
```
ON governance_violation THEN
    HALT current_task
    SET task.state = "blocked"
    CREATE blocker(classification: constitutional_violation)
    ESCALATE to_foreman
    NOTIFY johan
END ON
```

#### BR-5: Heartbeat Monitoring Rule
**Rule**: Builder must send heartbeat every 60 seconds; stall detected after 120 seconds

**Logic**:
```
IF (current_time - builder.last_heartbeat) > 120 seconds THEN
    SET builder.state = "failed"
    SET task.state = "blocked"
    CREATE blocker(classification: "builder_stall")
    TRIGGER recovery_workflow
END IF
```

#### BR-6: Wave Dependency Rule
**Rule**: Wave cannot start if any dependency wave is not completed

**Logic**:
```
FOR each dependency IN wave.dependencies DO
    IF dependency.state NOT = "completed" THEN
        REJECT wave_start
        RETURN error("Dependency not met: " + dependency.name)
    END IF
END FOR
```

#### BR-7: Progress Calculation Rule
**Rule**: Progress is deterministically calculated bottom-up

**Logic**:
```
task.progress_percentage = (completed_steps / total_steps) * 100

wave.progress_percentage = AVG(task.progress_percentage for task in wave)

program.progress_percentage = WEIGHTED_AVG(wave.progress_percentage for wave in program)
```

### 2.3 Domain Constraints

- **Unique Program Names**: Program names must be unique globally
- **Unique Wave Sequences**: Wave sequence numbers must be unique within program
- **Valid State Transitions**: State changes must follow defined state machine
- **Evidence Requirement**: All state changes must be logged in evidence trail
- **Isolation Requirement**: No cross-program data sharing (future: cross-tenant isolation)

### 2.4 Deterministic Logic

#### Architecture Validation Score
```
validation_score = (passed_items / total_checklist_items) * 100

IF validation_score < 100 THEN
    architecture_status = "INCOMPLETE"
    build_readiness = "NOT_READY"
ELSE
    architecture_status = "COMPLETE"
    build_readiness = "READY"
END IF
```

#### QA Pass Rate Calculation
```
qa_pass_rate = (passing_tests / total_tests) * 100

IF qa_pass_rate < 100 THEN
    qa_status = "RED" or "PARTIAL"
    task_completion = "BLOCKED"
ELSE IF qa_pass_rate = 100 THEN
    qa_status = "GREEN"
    task_completion = "ALLOWED"
END IF
```

**Note**: 99% is NOT acceptable. 301/303 passing = TOTAL FAILURE.

#### Builder Execution Continuity
```
execution_continuity = (active_time / total_time) * 100

target_continuity = 95%

IF execution_continuity < 95 THEN
    LOG low_continuity_incident
    INVESTIGATE pauses_and_interruptions
END IF
```

### 2.5 Domain Logic Separation

**Domain Layer**: Core business logic (programs, waves, tasks, builders, blockers)
- Pure logic, no UI concerns
- No database concerns (repositories handle persistence)
- Testable in isolation

**Application Layer**: Orchestrates domain logic and coordinates workflows
- Planning engine, governance engine, orchestration engine
- Uses domain logic, delegates to infrastructure

**Infrastructure Layer**: Persistence, external systems, UI
- Database repositories
- GitHub integration
- Builder backend integration
- UI components

---

## 3. DECISION & EVALUATION PIPELINES

### 3.1 Architecture Validation Pipeline

**Purpose**: Validate architecture completeness before task assignment

**Stages**:

#### Stage 1: Document Existence Check
**Input**: `architecture_reference` (path)  
**Output**: `document_exists` (boolean)  
**Logic**: Check if architecture document exists at specified path  
**Failure**: → Reject task, return "Architecture document not found"

#### Stage 2: Checklist Validation
**Input**: Architecture document content  
**Output**: `validation_results` (object with pass/fail per section)  
**Logic**: Execute all 14 sections of Architecture Design Checklist v1.1.0  
**Failure**: → Log failed items, return "Architecture incomplete"

#### Stage 3: Pass Rate Calculation
**Input**: `validation_results`  
**Output**: `pass_rate` (percentage)  
**Logic**: `(passed_items / total_items) * 100`  
**Failure**: If pass_rate < 100% → Reject task

#### Stage 4: Build Readiness Determination
**Input**: `pass_rate`  
**Output**: `build_readiness` ("READY" | "NOT_READY")  
**Logic**: `IF pass_rate = 100 THEN "READY" ELSE "NOT_READY"`  
**Failure**: If NOT_READY → Block task assignment

**Auditability**: Each stage logged with inputs, outputs, timestamp, decision rationale

**Evidence Generated**: Validation report with checklist results

---

### 3.2 QA Validation Pipeline

**Purpose**: Validate QA suite exists and is RED before task assignment

**Stages**:

#### Stage 1: QA Suite Existence Check
**Input**: `qa_suite_location` (path)  
**Output**: `qa_suite_exists` (boolean)  
**Logic**: Check if QA suite exists at specified path  
**Failure**: → Reject task, return "QA suite not found"

#### Stage 2: QA Execution
**Input**: QA suite path  
**Output**: `qa_results` (object: total, passing, failing, skipped)  
**Logic**: Execute QA suite, collect results  
**Failure**: If execution fails → Escalate

#### Stage 3: RED Status Validation
**Input**: `qa_results`  
**Output**: `is_red` (boolean)  
**Logic**: `failing_tests > 0 AND skipped_tests = 0`  
**Failure**: If tests all pass → Reject task (nothing to build)  
**Failure**: If tests skipped → Reject task (test debt exists)

#### Stage 4: Test Debt Detection
**Input**: QA suite content  
**Output**: `test_debt_list` (array of test debt items)  
**Logic**: Scan for .skip(), .todo(), commented tests, stub tests  
**Failure**: If test_debt_list.length > 0 → Reject task

**Auditability**: Each stage logged with QA results, test debt details

**Evidence Generated**: QA execution report, test debt report (if any)

---

### 3.3 Task Assignment Pipeline

**Purpose**: Assign task to builder after all validations pass

**Stages**:

#### Stage 1: Governance Pre-Check
**Input**: Task details  
**Output**: `governance_ok` (boolean)  
**Logic**: Verify no governance violations exist  
**Failure**: → Reject assignment, log violation

#### Stage 2: Architecture Validation Pipeline
**Input**: `task.architecture_reference`  
**Output**: `architecture_validated` (boolean)  
**Failure**: → Reject assignment

#### Stage 3: QA Validation Pipeline
**Input**: `task.qa_suite_location`  
**Output**: `qa_validated` (boolean)  
**Failure**: → Reject assignment

#### Stage 4: Builder Selection
**Input**: Task type (ui, api, schema, integration, qa)  
**Output**: `selected_builder` (builder_id)  
**Logic**: Select builder based on task type and builder availability  
**Failure**: If no builder available → Queue task, wait

#### Stage 5: Builder Assignment
**Input**: `task_id`, `builder_id`  
**Output**: Task assigned, builder state updated  
**Logic**: Update task.assigned_builder, task.state = "assigned"  
**Failure**: If assignment fails → Rollback, log error

#### Stage 6: "Build to Green" Instruction Generation
**Input**: Task details, architecture, QA  
**Output**: Structured "Build to Green" instruction  
**Logic**: Format instruction per Builder Agent Contract  
**Failure**: If formatting fails → Escalate

**Auditability**: Each stage logged, assignment provenance recorded

**Evidence Generated**: Task assignment record, builder assignment log, "Build to Green" instruction

---

### 3.4 Task Completion Validation Pipeline

**Purpose**: Validate task completion before marking complete

**Stages**:

#### Stage 1: QA Execution (Final)
**Input**: `task.qa_suite_location`  
**Output**: `final_qa_results`  
**Logic**: Execute full QA suite  
**Failure**: If any test fails → Reject completion

#### Stage 2: 100% Pass Validation
**Input**: `final_qa_results`  
**Output**: `all_tests_passing` (boolean)  
**Logic**: `passing_tests = total_tests AND failing_tests = 0 AND skipped_tests = 0`  
**Failure**: If NOT all passing → Reject completion

#### Stage 3: Test Debt Re-Check
**Input**: QA suite content  
**Output**: `test_debt_count` (integer)  
**Logic**: Scan for any test debt  
**Failure**: If test_debt_count > 0 → Reject completion, log quality incident

#### Stage 4: Build Quality Checks
**Input**: Task code  
**Output**: `build_quality_results` (object: lint, typecheck, build)  
**Logic**: Run lint, typecheck, build  
**Failure**: If any check fails → Reject completion

#### Stage 5: Interface Integrity Check
**Input**: Task code  
**Output**: `interface_integrity_ok` (boolean)  
**Logic**: Verify all Record<UnionType, T> complete, imports valid, no breaking changes  
**Failure**: If integrity issues → Reject completion

#### Stage 6: Evidence Completeness Check
**Input**: `task.evidence_location`  
**Output**: `evidence_complete` (boolean)  
**Logic**: Verify evidence trail exists and is complete  
**Failure**: If evidence incomplete → Reject completion

**Auditability**: Each stage logged, completion decision recorded

**Evidence Generated**: Final validation report, QA results, build quality results

---

### 3.5 Stall Detection Pipeline

**Purpose**: Detect and recover from builder stalls

**Stages**:

#### Stage 1: Heartbeat Monitoring
**Input**: `builder.last_heartbeat`, `current_time`  
**Output**: `time_since_heartbeat` (seconds)  
**Logic**: `current_time - last_heartbeat`  
**Trigger**: If > 120 seconds → Proceed to Stage 2

#### Stage 2: Stall Classification
**Input**: Builder state, task state  
**Output**: `stall_type` (enum: no_progress, blocked_waiting, crashed)  
**Logic**: Analyze last builder activity and task state  
**Deterministic**: Based on state history

#### Stage 3: Recovery Strategy Selection
**Input**: `stall_type`, `task_context`  
**Output**: `recovery_strategy` (enum: restart_builder, reassign_task, escalate_to_johan)  
**Logic**:
```
IF stall_type = "no_progress" AND attempts < 3 THEN
    strategy = "restart_builder"
ELSE IF stall_type = "blocked_waiting" THEN
    strategy = "escalate_to_johan"
ELSE
    strategy = "reassign_task"
END IF
```

#### Stage 4: Recovery Execution
**Input**: `recovery_strategy`  
**Output**: Recovery action taken  
**Logic**: Execute selected strategy  
**Failure**: If recovery fails → Escalate to Johan

**Auditability**: Stall detected, classification, strategy, execution logged

**Evidence Generated**: Stall detection report, recovery action log

---

### 3.6 Governance Violation Detection Pipeline

**Purpose**: Detect and halt on governance violations

**Stages**:

#### Stage 1: Continuous Monitoring
**Input**: Builder actions, task state changes  
**Output**: `potential_violations` (array)  
**Logic**: Monitor for protected path access, test debt, incomplete architecture  
**Trigger**: On any suspicious action

#### Stage 2: Violation Classification
**Input**: `potential_violations`  
**Output**: `violation_type` (enum per Builder Agent Contract)  
**Logic**: Classify violation based on rule violated  
**Deterministic**: Based on governance rules

#### Stage 3: Automatic Halt
**Input**: `violation_type`  
**Output**: Execution halted, task blocked  
**Logic**: HALT current task, SET state = "blocked"  
**Immediate**: No delay

#### Stage 4: Blocker Creation
**Input**: `violation_type`, `task_id`  
**Output**: Blocker record created  
**Logic**: CREATE blocker with classification and details  
**Logged**: In governance memory

#### Stage 5: Escalation
**Input**: Blocker details  
**Output**: Johan notified  
**Logic**: Send escalation with violation details and recommended action  
**Evidence**: Full violation evidence attached

**Auditability**: Violation detected, halt timestamp, escalation logged

**Evidence Generated**: Governance violation report, blocker record

---

### 3.7 Decision Pipeline Precedence

**Order of Execution**:
1. Governance checks (highest priority, can halt immediately)
2. Architecture validation
3. QA validation
4. Task assignment
5. Builder execution (continuous monitoring)
6. Stall detection (parallel monitoring)
7. Task completion validation

**Failure Fallback**:
- All failures escalate to Foreman
- Foreman logs incident in governance memory
- Foreman decides: retry, adjust plan, or escalate to Johan

---

## 4. MODULE PROCESSES

### 4.1 Program Initialization Process

1. Johan defines program intent
2. Foreman creates program record
3. Foreman decomposes into waves
4. Foreman decomposes waves into tasks
5. Foreman validates architecture for each task
6. Foreman creates QA suites for each task (QA-to-Red)
7. Foreman presents plan to Johan for approval
8. On approval: Program state = "planned", ready for execution

### 4.2 Wave Execution Process

1. Check wave dependencies (all must be completed)
2. If dependencies met: Wave state = "in-progress"
3. Assign tasks to builders (per Task Assignment Pipeline)
4. Monitor builder heartbeats
5. Track task progress
6. On all tasks completed: Wave state = "completed"
7. Proceed to next wave or program completion

### 4.3 Task Execution Process

1. Task assigned to builder (via Task Assignment Pipeline)
2. Builder receives "Build to Green" instruction
3. Builder executes build (continuous monitoring)
4. Builder reports progress (heartbeat every 60s)
5. On builder completion claim: Execute Task Completion Validation Pipeline
6. If validation passes: Task state = "completed"
7. If validation fails: Task state = "blocked", create blocker, escalate

### 4.4 Builder Orchestration Process

1. Foreman maintains pool of builder backends (local, hosted, burst)
2. For each task: Foreman selects appropriate builder backend
3. Selection criteria: task complexity, priority, builder availability
4. Foreman sends "Build to Green" instruction to selected backend
5. Foreman monitors execution via heartbeats
6. On stall: Execute Stall Detection Pipeline
7. On completion: Execute Task Completion Validation Pipeline

---

## 5. COMPONENT STRUCTURE

### 5.1 Core Components

#### Planning Engine
**Responsibility**: Decompose programs into waves and tasks  
**Key Functions**:
- `createProgram(intent)`: Create program from Johan's intent
- `decomposeIntoWaves(program)`: Break program into waves
- `decomposeIntoTasks(wave)`: Break wave into tasks
- `validatePlan(program)`: Validate plan completeness

#### Governance Engine
**Responsibility**: Enforce governance rules automatically  
**Key Functions**:
- `validateArchitecture(architecture_ref)`: Execute Architecture Validation Pipeline
- `validateQA(qa_suite_location)`: Execute QA Validation Pipeline
- `detectViolation(action)`: Monitor for governance violations
- `enforceGSR()`: Halt on governance violation
- `enforceZeroTestDebt()`: Reject test debt

#### Orchestration Engine
**Responsibility**: Assign tasks to builders and monitor execution  
**Key Functions**:
- `assignTask(task, builder)`: Execute Task Assignment Pipeline
- `monitorHeartbeat(builder)`: Monitor builder heartbeats
- `detectStall(builder)`: Execute Stall Detection Pipeline
- `recoverFromStall(builder, strategy)`: Execute recovery strategy

#### Monitoring & Stall Detection Engine
**Responsibility**: Detect stalls and report status  
**Key Functions**:
- `trackHeartbeat(builder, timestamp)`: Record builder heartbeat
- `checkStallCondition()`: Check if stall occurred
- `classifyStall(builder)`: Determine stall type
- `generateStatusReport()`: Create status report for Johan

#### Evidence & Audit Trail Engine
**Responsibility**: Record all actions for audit and provenance  
**Key Functions**:
- `logAction(actor, action, context)`: Log action
- `recordProvenance(task, builder, model)`: Record provenance
- `generateEvidenceTrail(entity)`: Create complete evidence trail
- `validateEvidenceCompleteness(entity)`: Ensure evidence complete

#### Provenance Tracking Engine
**Responsibility**: Track who did what with which model  
**Key Functions**:
- `recordActor(action, actor)`: Record actor (Foreman/Builder)
- `recordBackend(action, backend)`: Record backend used
- `recordModel(action, model)`: Record model used
- `recordEscalation(action, rationale)`: Record escalation rationale

### 5.2 Component Relationships

```
Planning Engine
    ↓ (creates programs/waves/tasks)
Governance Engine
    ↓ (validates architecture/QA)
Orchestration Engine
    ↓ (assigns tasks)
Monitoring Engine
    ↓ (tracks execution)
Evidence Engine
    ↓ (records all actions)
```

**All components** use **Provenance Tracking Engine** for audit trail.

---

## 6. USER WORKFLOWS

### 6.1 Workflow: Program Initiation

**Actor**: Johan  
**Goal**: Start new program execution

**Steps**:
1. Johan defines intent (e.g., "Build Foreman Office Wave 0")
2. Foreman receives intent
3. Foreman creates program record
4. Foreman decomposes into waves and tasks
5. Foreman validates architecture for each task
6. Foreman creates QA-to-Red for each task
7. Foreman generates plan document
8. Foreman presents plan to Johan for approval
9. Johan reviews plan
10. Johan approves or requests changes
11. On approval: Program execution begins

**Alternate Flows**:
- Johan rejects plan → Foreman adjusts plan, re-presents
- Architecture incomplete → Foreman completes architecture, re-validates

---

### 6.2 Workflow: Monitor Execution

**Actor**: Johan  
**Goal**: Monitor live execution status

**Steps**:
1. Johan opens Foreman Office dashboard
2. Dashboard shows active program
3. Dashboard shows current wave
4. Dashboard shows tasks in progress
5. Dashboard shows builder heartbeats
6. Dashboard shows blockers (if any)
7. Johan reviews status
8. Johan intervenes if decision required

**Alternate Flows**:
- Blocker detected → Dashboard highlights blocker, Johan investigates
- Builder stalled → Dashboard shows stall, Foreman executing recovery

---

### 6.3 Workflow: Resolve Blocker

**Actor**: Johan  
**Goal**: Resolve blocker preventing progress

**Steps**:
1. Foreman detects blocker
2. Foreman classifies blocker
3. Foreman escalates to Johan
4. Johan reviews blocker details
5. Johan decides resolution action
6. Johan approves resolution
7. Foreman executes resolution
8. Blocker marked resolved
9. Execution resumes

**Alternate Flows**:
- Architecture-QA mismatch → Foreman adjusts architecture or QA
- Impossible requirements → Johan adjusts requirements
- Constitutional violation → Johan invokes override (temporary)

---

### 6.4 Workflow: Builder Task Execution

**Actor**: Builder Agent  
**Goal**: Execute "Build to Green" task

**Steps**:
1. Builder receives "Build to Green" instruction
2. Builder validates instruction format
3. Builder loads architecture and QA
4. Builder executes build iterations
5. Builder runs QA after each iteration
6. Builder sends heartbeat every 60s
7. Builder continues until all tests pass
8. Builder reports completion
9. Foreman validates completion
10. Task marked completed

**Alternate Flows**:
- Tests fail after 3 iterations → Builder escalates
- Architecture-QA mismatch → Builder escalates
- Governance violation → Builder halts, escalates

---

## 7. VALIDATION RULES

### 7.1 Architecture Validation Rules

- Architecture document must exist at specified path
- Architecture must pass 100% of checklist items
- Architecture must have no "TBD" or "TODO" markers
- Architecture must have no ambiguous requirements

### 7.2 QA Validation Rules

- QA suite must exist at specified path
- QA suite must be RED (failing tests) before task assignment
- QA suite must be GREEN (100% passing) before task completion
- QA suite must have zero test debt (no skipped, incomplete, or failing tests)

### 7.3 Task Validation Rules

- Task must reference existing architecture
- Task must reference existing QA suite
- Task must have clear acceptance criteria
- Task must be assigned to specific builder
- Task must have evidence trail before completion

### 7.4 Builder Validation Rules

- Builder must send heartbeat every 60 seconds during execution
- Builder must follow "Build to Green" protocol exactly
- Builder must not modify protected paths
- Builder must maintain ≥95% execution continuity

---

## 8. ERROR HANDLING

### 8.1 Error Categories

**Governance Violations**:
- Protected path modification attempt
- Test debt detected
- Incomplete architecture
- QA bypass attempt

**Builder Failures**:
- Stalled execution (no heartbeat)
- Repeated failures (3+ iterations no progress)
- Backend unavailable
- Instruction format violation

**Integration Errors**:
- GitHub API failure
- Memory fabric unavailable
- Compliance engine unavailable

### 8.2 Error Handling Strategies

**Governance Violations**: HALT immediately, create blocker, escalate to Johan

**Builder Failures**: Execute Stall Detection Pipeline, attempt recovery, escalate if recovery fails

**Integration Errors**: Retry with exponential backoff, fallback to local cache, escalate if persistent

### 8.3 Failure Recovery

**Automatic Recovery**:
- Builder stall → Restart builder or reassign task
- Transient network errors → Retry with backoff
- Rate limit errors → Queue and throttle

**Manual Recovery** (requires Johan):
- Architecture-QA mismatch → Adjust architecture or QA
- Impossible requirements → Adjust requirements or scope
- Constitutional violations → Invoke owner override

---

## 9. STATE MANAGEMENT

### 9.1 Program State Machine

```
planned → in-progress → completed
   ↓           ↓             
blocked ← → failed
```

**State Transitions**:
- `planned → in-progress`: On Johan approval
- `in-progress → blocked`: On blocker detected
- `blocked → in-progress`: On blocker resolved
- `in-progress → completed`: On all waves completed
- `in-progress → failed`: On unrecoverable error
- `blocked → failed`: On blocker unresolvable

### 9.2 Wave State Machine

(Same as Program State Machine)

### 9.3 Task State Machine

```
planned → assigned → in-progress → completed
   ↓         ↓            ↓
blocked ← ← ← ← ← ← ← failed
```

**State Transitions**:
- `planned → assigned`: On builder assignment
- `assigned → in-progress`: On builder start
- `in-progress → blocked`: On blocker detected
- `blocked → in-progress`: On blocker resolved
- `in-progress → completed`: On validation pass
- `in-progress → failed`: On unrecoverable error

### 9.4 Builder State Machine

```
idle → active → idle
  ↓       ↓
blocked  failed → idle (on recovery)
```

---

## 10. ASSUMPTIONS

1. GitHub API is available and responsive (fallback: local cache)
2. Memory fabric is persistent and available (fallback: local storage)
3. Builder backends are available (at least local builder always available)
4. Johan reviews plans within reasonable time (SLA: 24 hours)
5. Governance rules are enforced strictly (no exceptions except owner override)
6. All evidence is stored permanently (retention: indefinite)

---

*Generated for Issue #2 - Architecture & QA Design (Wave 0 Completion)*
