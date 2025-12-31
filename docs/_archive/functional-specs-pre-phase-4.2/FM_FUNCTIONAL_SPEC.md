# FM (Foreman) Functional Specification v1

**Version**: 1.1.0  
**Status**: Authoritative Functional Baseline  
**Authority**: Johan Ras (Owner)  
**Executor**: Governance Administrator (FM Repo)  
**Date**: 2025-12-22  
**Last Updated**: 2025-12-22 (v1.1.0 - Incorporated FM App Description)  
**Classification**: Pre-Architecture, Governance-Aligned

---

## 0. Document Authority

This document is the **authoritative functional specification** for the Foreman (FM) application.

**Constitutional Hierarchy**:
```
Governance Repository (Constitutional Authority)
    ↓
BUILD_PHILOSOPHY.md (Supreme Build Authority)
    ↓
FM_APP_DESCRIPTION.md (Authoritative Product Intent)
    ↓
FM_FUNCTIONAL_SPEC.md (THIS DOCUMENT - Functional Baseline)
    ↓
FM Architecture (Derived from this specification)
    ↓
FM QA Design (Derived from architecture)
    ↓
FM Implementation (Governed by QA and Architecture)
```

**Upstream Authority**:
- This specification incorporates the **FM App Description** (`docs/governance/FM_APP_DESCRIPTION.md`) as authoritative product intent
- All functional requirements implied by the App Description are captured here
- The App Description defines what the FM Office App *is* as a product and how it is used

**Non-Negotiable Rules**:
- No architecture may be designed that contradicts this specification
- No code may be written that violates this specification
- No QA may be designed that does not verify this specification
- This specification may only be modified with explicit Owner (Johan) approval

---

## 1. Purpose and Core Problem

### 1.1 The Problem FM Solves

**Proven Problem**: Burst-based AI platforms (e.g., GitHub Copilot agents) are excellent executors but **cannot function as continuous supervisors**.

**Symptoms**:
- Execution state is lost between sessions
- No persistent awareness of program/wave/task progress
- Cannot detect silent stalls without human prompting
- No continuous governance enforcement
- Human governor must micromanage to maintain visibility
- Large backlogs cannot be executed safely in coordinated batches

**Root Cause**: Burst platforms are stateless, session-bound, and lack persistent memory of execution state.

### 1.2 FM's Solution

FM provides the **missing continuous supervisory layer**:
- **Persistent awareness** of execution state across all sessions
- **Planning and control** (POLC framework)
- **Governance enforcement** without human micromanagement
- **Execution visibility** for the human governor
- **Human-in-the-loop oversight** at decision points only
- **Safe batch execution** of large programs

FM is the **brain and cockpit** of the Maturion build system.

### 1.3 The FM Office App

The **FM Office App** is the **live embodiment of FM** — a one-man operations control centre through which Johan oversees, directs, governs, and interacts with the entire automated build factory.

**Critical Principle**: If the FM Office App is unavailable, **the factory is effectively blind**.

The app is:
- **NOT a passive dashboard or reporting tool**
- **NOT a Kanban board, ticket tracker, CI console, IDE, or prompt playground**
- **THE primary operational interface** for continuous supervision, decision-making, and factory control

---

## 2. What FM Is (and Is Not)

### 2.1 FM IS

1. **An Always-On AI Supervisor**
   - Continuously aware of execution state
   - Never sleeps or loses context
   - Maintains program/wave/task tracking
   - Detects stalls automatically

2. **A Program and Wave Orchestrator**
   - Plans execution in programs → waves → tasks
   - Sequences work according to dependencies
   - Coordinates multiple builder agents
   - Manages parallel and sequential execution

3. **A Governance Enforcement Engine**
   - Enforces Build Philosophy principles
   - Validates architecture before builds
   - Ensures QA-as-Proof compliance
   - Blocks execution on governance violations
   - Enforces Governance Supremacy Rule (GSR)

4. **A Live Execution Cockpit**
   - Provides Johan (human governor) real-time visibility
   - Presents plans for approval
   - Requests decisions at appropriate points
   - Reports progress with evidence
   - Escalates blockers with classification

5. **The Foundational Runtime for PIT (Project Implementation Tracker)**
   - Generates PIT-compatible telemetry from day one
   - Tracks provenance (who, what, when, which model)
   - Records all execution events
   - Enables future PIT UI without retrofit

### 2.2 FM IS NOT

1. **Not a CI/CD System**
   - Does not replace GitHub Actions
   - Does not execute builds directly
   - Does not run tests directly
   - Orchestrates builders who use CI/CD

2. **Not a GitHub Replacement**
   - GitHub remains system of record for code
   - FM is system of record for execution state and control
   - FM coordinates work that results in GitHub PRs

3. **Not a Passive Dashboard**
   - Not just a visualization layer
   - Actively governs and controls execution
   - Makes autonomous decisions within guardrails
   - Escalates when human decision required

4. **Not a One-Off Execution Script**
   - Not a temporary tool
   - Permanent supervisory infrastructure
   - Designed for long-term operation
   - Survives chat resets, deployments, upgrades

5. **Not a Chat-Only Interface**
   - Must provide structured UI for Johan
   - Cannot depend on GitHub comments
   - Must work across multiple interaction channels
   - Provides both synchronous and asynchronous interaction

---

## 3. Primary Roles and Actors

### 3.1 Johan (Human Governor)

**Responsibilities**:
- Defines strategic intent ("Build Annex 1", "Implement ISO 27001 controls")
- Reviews and approves execution plans before start
- Monitors live progress via FM cockpit
- Intervenes ONLY at governance or decision points
- Verifies outcomes via evidence, not source code review
- Makes final approval decisions

**Does NOT**:
- Micromanage individual tasks
- Review source code line-by-line
- Track individual builder progress
- Debug implementation issues
- Make tactical execution decisions

### 3.2 FM (AI Supervisor / Foreman)

**Responsibilities**:
- **Planning (POLC)**: Breaks down programs into waves and tasks
- **Organizing (POLC)**: Assigns tasks to appropriate builders
- **Leading (POLC)**: Supervises builder execution
- **Controlling (POLC)**: Monitors progress, detects deviations, corrects course
- **Governance Enforcement**: Ensures compliance with all governance rules
- **Builder Coordination**: Orchestrates multiple builders
- **Continuous Reporting**: Provides heartbeat and progress updates
- **Escalation**: Raises blockers and decision points to Johan

**Authority Boundaries**:
- CANNOT override governance rules (GSR is absolute)
- CANNOT modify protected constitutional files
- CANNOT accept partial QA passes
- CANNOT bypass architecture validation
- MUST escalate when governance conflict detected
- MUST escalate when human decision required

**Operational Mode**: Always-on, persistent, never loses context

### 3.3 Builder Agents (Executors)

**Responsibilities**:
- Execute clearly bounded tasks assigned by FM
- Implement code according to architecture
- Run QA and achieve 100% pass
- Report progress and evidence to FM
- Escalate blockers to FM (NOT to Johan)
- Obey strict builder contract

**Characteristics**:
- Stateless or semi-stateless
- Task-focused, not program-aware
- Burst execution model acceptable
- Multiple backends possible (Copilot, hosted runtime, manual)

**Authority Boundaries**:
- CANNOT bypass governance or QA
- CANNOT report directly to Johan
- CANNOT make architectural decisions
- CANNOT modify governance rules
- MUST follow FM's instructions exactly

---

## 4. Core Concepts and Structure

### 4.1 Execution Hierarchy: Programs → Waves → Tasks

**Program**:
- High-level initiative (e.g., "Implement Annex 1")
- Contains multiple waves
- Has overall success criteria
- Tracks aggregate progress

**Wave**:
- Ordered phase within a program
- Contains multiple tasks
- Executes in sequence (Wave N completes before Wave N+1 starts)
- Has completion criteria
- Dependencies between waves enforced

**Task**:
- Atomic unit of work
- Assigned to a single builder
- Has clear definition, acceptance criteria, and evidence requirements
- Executes independently within wave constraints
- Tracks state: PLANNED → IN_PROGRESS → BLOCKED → COMPLETE

**State Tracking**:
Each level tracks:
- Current state
- Progress percentage
- Evidence artifacts
- Blockers (if any, classified by type)
- Execution history

### 4.2 Governance Supremacy (Non-Negotiable)

FM operates under the **Governance Supremacy Rule (GSR)**.

**GSR Four Pillars**:

1. **100% QA Passing is ABSOLUTE**
   - ALL tests must pass
   - 99% pass = TOTAL FAILURE
   - No exceptions, no deferrals
   - Build blocked on any test failure

2. **Zero Test Debt is MANDATORY**
   - No skipped tests (.skip, .todo)
   - No commented out tests
   - No incomplete test infrastructure
   - No test debt carried forward

3. **Architecture Conformance is REQUIRED**
   - Code must match architecture exactly
   - No "interpretations" or "improvements"
   - Deviations require CS2 (Change Sequence 2) approval
   - Escalate when architecture unclear

4. **Constitutional File Protection**
   - Protected paths MUST NEVER be modified by builders
   - Protected paths include:
     - `.github/workflows/`
     - `.github/foreman/agent-contract.md`
     - `BUILD_PHILOSOPHY.md`
     - `foreman/constitution/`
     - `foreman/governance/`
     - `docs/governance/`
   - Modification requires CS2 approval + Owner review

**FM's Role in GSR Enforcement**:
- Validates compliance before allowing task start
- Monitors compliance during execution
- Blocks execution on violations
- Escalates violations to Johan
- Records all violations in governance memory

**No Appeals**: GSR rules are absolute. Only Owner (Johan) may override temporarily for emergencies.

### 4.3 Continuous Supervision (Non-Negotiable)

FM MUST:
- Never sleep (always-on operation)
- Maintain execution context across all sessions
- Know what is happening right now
- Detect stalls without human prompting
- Provide heartbeat at regular intervals

**"No Update" = Failure State**:
- If builder has not reported in X time → STALLED state
- If FM has not checked builder in X time → FM violation
- Stalls trigger automatic escalation

### 4.4 Build Philosophy Alignment

FM enforces the **Five Core Principles of Build Philosophy**:

1. **One-Time Build Correctness**
   - Architecture must be 100% complete before build
   - All requirements unambiguous and validated
   - QA coverage defined before implementation
   - No "build first, fix later"

2. **Zero Regression Guarantee**
   - All working code remains working
   - All passing tests continue to pass
   - No removal of working features without approval
   - Comprehensive regression test coverage

3. **Full Architectural Alignment**
   - No deviation from architecture
   - Architecture is law
   - Module boundaries never violated
   - Integration contracts honored

4. **Zero Loss of Context**
   - All decisions preserved forever
   - Never discard important context
   - Architectural rationale maintained
   - Full audit trail

5. **Zero Ambiguity**
   - All specifications must be explicit
   - All requirements must be testable
   - All governance rules machine-checkable
   - No vague or subjective criteria

**FM enforces these by**:
- Validating architecture before build
- Running QA-of-QA before accepting work
- Checking integration integrity
- Maintaining memory and provenance
- Blocking ambiguous specifications

---

## 5. FM ↔ Johan Interaction Model

### 5.1 Primary Interaction: Conversational Interface

The **primary interaction model** for the FM Office App is a **persistent conversational interface** between Johan and FM (Maturion).

**Key Properties**:
- FM can **initiate conversations**, not just respond to queries
- FM asks clarifying questions until intent is unambiguous
- FM proposes interpretations and waits for approval
- Conversations persist across time, projects, and builds
- Conversations are **first-class operational artifacts**
- This is NOT a stateless chat window — it is a living operational dialogue

**Chat UX Requirements**:
- FM messages and Johan messages are visually distinct (left/right alignment, role coloring)
- Role badges clearly identify speaker
- Persistent history (never lost)
- Searchable across all conversations
- Linkable to builds, PRs, incidents, parking station items

**Why Conversational First**:
- Johan provides partial, vague, or incomplete instructions (expected and acceptable)
- FM absorbs informality and converts it into deterministic, governed execution
- Clarification happens naturally through dialogue, not rigid forms

### 5.2 Ping-Based Attention System

FM actively monitors execution and uses **pings** to get Johan's attention when needed.

**Ping Triggers**:
- Clarification required
- Approval required (plan, decision, condition)
- Milestone reached
- Progress stall detected
- Governance guardrail hit
- Escalation required (governance, technical, decision, external)

**Ping Properties**:
- **Audible** (sound notification)
- **Visible** (UI indicator)
- **Prioritized** (informational / attention / critical)

**Critical Rule**: FM never waits silently. If FM needs input, FM pings.

### 5.3 Interaction Requirements

### 5.3 Interaction Requirements

FM must provide a **live, project-specific interaction surface** that:
- Presents plans for approval before execution
- Requests decisions at appropriate points
- Reports progress continuously with evidence
- Escalates blockers with classification
- Provides summaries and dashboards

**Critical**: This interaction MUST NOT depend solely on GitHub comments.

### 5.4 Intent → Execution Loop

**Step 1: Intent Intake**

Johan provides:
- Partial thoughts
- Vague objectives
- Rough ideas
- Sometimes contradictory statements

This is **expected and acceptable**.

**Step 2: Clarification Loop**

FM MUST:
- Interrogate ambiguity
- Surface assumptions
- Propose interpretations
- Refuse to proceed on unresolved uncertainty

FM repeats clarification until intent is unambiguous.

**Step 3: Requirement Specification**

FM produces a clear requirement specification and presents it for approval.

**Approval Options**:
- **Approve** → Requirements frozen, execution may begin
- **Do Not Approve** → Clarification loop restarts
- **Approve with Conditions** → Opens focused chat to capture constraints

**Step 4: Execution**

Once approved:
- Requirements are frozen (immutable for that execution)
- Architecture and QA are derived
- Execution begins under governance
- FM reports progress continuously

### 5.5 Interaction Patterns

**Pattern 1: Plan Approval**
```
FM: "I have created a plan for Program X with 3 waves and 15 tasks. Review?"
Johan: Reviews plan in UI
Johan: "Approved" OR "Modify wave 2"
FM: Proceeds or adjusts plan
```

**Pattern 2: Decision Request**
```
FM: "Builder reports architecture unclear at module boundary X. Options: A, B, or C?"
Johan: Selects option or provides guidance
FM: Updates architecture, notifies builder
```

**Pattern 3: Progress Update**
```
FM: "Wave 1: 80% complete. Task 3/4 done. Task 4 in progress. ETA: 2 hours."
Johan: Observes (no action required)
```

**Pattern 4: Blocker Escalation**
```
FM: "Builder blocked on missing dependency. Classification: External. Action required?"
Johan: Decides on action
FM: Executes decision
```

### 5.6 Escalation Classification

FM classifies all blockers:
- **Governance** (e.g., QA failure, architecture violation)
- **Technical** (e.g., missing dependency, broken integration)
- **Decision** (e.g., ambiguous requirement, trade-off choice)
- **External** (e.g., third-party API down, access issue)

Classification helps Johan prioritize and respond appropriately.

---

## 6. Monitoring and Visibility Requirements

### 6.1 Operational Dashboard (Home View)

The **home view** of the FM Office App is an **operations control dashboard** providing immediate situational awareness.

**Display Model**: Robot / Traffic-Light (RAG - Red/Amber/Green)

**Core Operational Domains** (Wave 0):
- Build Health
- Governance Compliance
- Architecture Completeness
- QA Status
- PR Gate Health
- CI Health
- Escalations
- Backlog / Queue Health
- Builder Availability
- Evidence Completeness
- Learning Promotion Status

**Each Domain Shows**:
- **Current RAG State** (Green / Amber / Red)
- **Short human-readable reason(s)** (why this state?)
- **Timestamp of last change**

**Critical Rule**: No domain may be Red or Amber without an **explainable reason**.

### 6.2 Progressive Drill-Down (Mandatory)

Every dashboard element MUST support **progressive drill-down**, all the way to root cause.

**Example Drill-Down Chain**:
```
Governance Compliance → Red
  ↓
Repository (which repo?)
  ↓
Specific PR (which PR?)
  ↓
Failing Gate (which gate?)
  ↓
Failing Check (which check?)
  ↓
Evidence / Logs (what failed?)
  ↓
Root Cause (why did it fail?)
  ↓
Proposed Remediation (how to fix?)
  ↓
Action Buttons (execute fix)
```

**Product Defect**: A Red or Amber state without drill-down capability is a **product defect**.

### 6.3 Real-Time Visibility

At any moment, Johan must be able to see:

1. **Program Status**
   - Which program is active
   - Overall progress percentage
   - Start time and estimated completion
   - Current blockers (if any)

2. **Wave Status**
   - Which wave is executing
   - Wave progress percentage
   - Tasks in wave (total and completed)
   - Wave dependencies satisfied/pending

3. **Task Status**
   - Which tasks are running
   - Task state (PLANNED, IN_PROGRESS, BLOCKED, COMPLETE)
   - Assigned builder
   - Last update timestamp
   - Evidence artifacts

4. **Builder Health**
   - Last heartbeat per builder
   - Current task assignment
   - Execution backend (Copilot, hosted, manual)
   - Model used (if available)

5. **Blocker Dashboard**
   - All active blockers
   - Classification and severity
   - Time blocked
   - Escalation state

6. **Pending Decisions**
   - Questions awaiting Johan's input
   - Context and options
   - Priority/urgency

### 6.4 Message Inbox and Quick Actions

A sidebar **Messages / Requests** view provides centralized access to all outstanding items requiring Johan's attention.

**Inbox Contents**:
- All outstanding FM requests
- Pending approvals (plans, requirements, decisions)
- Unresolved escalations
- Milestone notifications
- Blocker reports

**Quick Actions** (One-Click):
Each inbox item supports immediate action:
- **Approve** → Accept and proceed
- **Do Not Approve** → Reject and request rework
- **Approve with Conditions** → Opens focused chat to capture constraints

**Purpose**:
- Enables full factory control from desktop or mobile
- Reduces friction in approval workflows
- Centralizes all decision points
- Prevents silent stalls on approvals

### 6.5 Evidence and Provenance

For every action, FM records:
- **Who**: Which actor (FM, Builder, Johan)
- **What**: Action taken
- **When**: Timestamp (ISO 8601)
- **Where**: Which program/wave/task
- **How**: Backend and model used (if applicable)
- **Why**: Rationale or trigger
- **Evidence**: Artifacts (logs, test results, screenshots, diffs)

**Purpose**:
- Audit trail for governance compliance
- Learning and continuous improvement
- PIT (Project Implementation Tracker) integration
- Debugging and root cause analysis

---

## 7. Parking Station (Continuous Improvement Intake)

### 7.1 Purpose

The **Parking Station** is a persistent intake area for continuous improvement of the Maturion platform itself.

**Not Passive**: The Parking Station is an **active system** for capturing, discussing, and converting improvement ideas into executable requirements.

### 7.2 Parking Station Items

**Item Sources**:
- Johan (strategic improvements)
- FM (detected inefficiencies, automation opportunities)
- Builders (execution friction points)
- Governance agents (governance enhancements)

**Item Structure**:
Each Parking Station item includes:
- **Title** (short description)
- **Description** (detailed explanation)
- **Category** (governance / architecture / QA / feature / infrastructure / UX / analytics)
- **Impact Estimate** (low / medium / high)
- **Urgency** (immediate / short-term / long-term)
- **Related Artifacts** (chat link, PR, incident, build)
- **Status** (new / discussion / requirement / deferred / closed)

### 7.3 Parking Station → Execution Flow

For each item, Johan can:
1. **Start a Discussion** → Launches guided conversation with FM
2. **Convert to Requirement** → Follows Intent → Execution Loop (§5.4)
3. **Defer** → Move to backlog with rationale
4. **Close** → Reject with rationale

**Discussion → Requirement Process**:
1. Johan initiates discussion
2. FM clarifies intent (same as §5.4 Clarification Loop)
3. FM produces requirement specification
4. Johan approves (with or without conditions)
5. Requirement enters standard FM pipeline (Planning → Architecture → QA → Build)

### 7.4 Learning Integration

Parking Station items contribute to:
- FL-CI (Foreman Learning - Continuous Improvement)
- Governance evolution
- Builder capability enhancement
- Platform maturity

---

## 8. Analytics Interface

### 8.1 Purpose

The **Analytics Interface** provides operational intelligence and trend analysis for the Maturion platform.

**Access**: Left sidebar of FM Office App

### 8.2 Analytics Capabilities

1. **View Predefined Metrics**
   - Operational dashboards (build velocity, QA pass rate, governance violations, etc.)
   - Trend charts and time-series data
   - Builder performance metrics
   - Execution efficiency metrics

2. **Conversational Analysis**
   - Ask FM to analyze data ("Why did QA pass rate drop last week?")
   - Request insights on trends or anomalies
   - Natural language queries on platform health

3. **Custom Metrics and Dashboards**
   - Request new metrics or dashboards
   - FM creates and presents for approval
   - Once approved, metrics become permanent

4. **Drill-Down to Source**
   - All analytics must support drill-down to source artifacts
   - From metric → data point → execution event → evidence

### 8.3 Analytics Scope

**In Scope (Wave 0)**:
- Operational metrics (build health, governance compliance, QA status)
- Builder performance and efficiency
- Execution trends (velocity, blockers, escalations)
- Learning analytics (pattern recognition, improvement tracking)

**Future Enhancements**:
- Predictive analytics (failure prediction, capacity planning)
- Cost analytics (model usage, execution cost)
- Advanced anomaly detection

---

## 9. Builder Orchestration

### 7.1 Builder Backend Selection

FM decides which builder backend to use for each task based on:
- Task complexity and risk
- Builder availability
- Cost considerations
- Model capability requirements

**Backend Options**:
1. **Burst Platform** (e.g., GitHub Copilot)
   - Good for: Standard tasks, well-defined scope
   - Limitations: Stateless, session-bound
   
2. **Hosted Runtime** (e.g., Render)
   - Good for: Long-running tasks, stateful operations
   - Limitations: Cost, setup complexity
   
3. **Manual/Local Builder**
   - Good for: Complex tasks, human expertise required
   - Limitations: Slower, requires human availability

### 7.2 Builder Contract (Strict Enforcement)

All builders MUST:
1. Accept only tasks with complete, unambiguous specifications
2. Validate architecture before implementation
3. Achieve 100% QA pass (no exceptions)
4. Produce zero test debt
5. Report progress regularly (heartbeat)
6. Provide evidence for all claims
7. Escalate blockers to FM (never directly to Johan)
8. Never modify protected paths
9. Never bypass governance rules
10. Follow One-Prompt-One-Job Doctrine (OPOJD)

**FM enforces contract by**:
- Validating specifications before assignment
- Monitoring builder heartbeat
- Checking QA results
- Inspecting for test debt
- Validating evidence
- Blocking non-compliant work

### 7.3 Model Escalation

FM may escalate to more capable models when:
- Task complexity exceeds current model capability
- Builder reports inability to complete with current model
- Multiple failures indicate model limitation
- Cost/benefit analysis supports escalation

**Escalation recorded in provenance** for learning and cost tracking.

---

## 10. Relationship to PIT (Project Implementation Tracker)

### 8.1 PIT Emergence by Design

FM is designed so that **PIT emerges naturally** from execution telemetry.

**No Retrofit Required**:
- All programs/waves/tasks are PIT-compatible from day one
- All heartbeats and state transitions are PIT events
- All evidence is PIT-compatible
- All provenance is PIT-structured

### 8.2 PIT Data Structure

FM generates:
- **Program definitions** (name, description, waves, success criteria)
- **Wave definitions** (dependencies, tasks, completion criteria)
- **Task definitions** (specification, acceptance criteria, evidence requirements)
- **Execution events** (state changes, heartbeats, decisions, escalations)
- **Evidence artifacts** (logs, test results, diffs, screenshots)
- **Provenance records** (who, what, when, where, how, why)

Future PIT UI will consume this data without requiring FM changes.

---

## 11. Scope (Explicit Boundaries)

### 11.1 In Scope (Wave 0 and Beyond)

FM MUST provide:
- Program/wave/task execution structure
- Continuous supervision and state tracking
- Governance enforcement (GSR, Build Philosophy)
- Builder orchestration and coordination
- **Conversational interface as primary interaction model**
- **Ping-based attention system**
- **Operational dashboard with RAG status model**
- **Progressive drill-down to root cause**
- **Message inbox with quick actions**
- Real-time visibility for Johan
- Plan approval workflow
- Decision request workflow
- Progress reporting with evidence
- Blocker escalation with classification
- **Parking Station for continuous improvement**
- **Analytics interface for operational intelligence**
- Provenance and audit trail
- PIT-compatible telemetry generation
- Heartbeat and stall detection

### 11.2 Out of Scope (Explicit Exclusions)

FM does NOT include (Wave 0):
- Full PIT UI (comes later, uses FM telemetry)
- Autonomous mega-batch execution (future enhancement)
- Billing or user management (external system)
- External integrations beyond GitHub
- Multi-tenant operation (single-tenant initially)
- Predictive analytics (future enhancement)
- Cost analytics (future enhancement)

**Rationale**: Keep Wave 0 focused on core supervisory capabilities. Additional features layered on after foundation is solid.

---

## 12. Success Criteria

### 10.1 FM is Successful When

1. **Johan is Never Blind to Execution State**
   - Real-time visibility into all programs/waves/tasks
   - Always knows what is happening right now
   - Can see progress, blockers, decisions without asking

2. **Execution Does Not Silently Stall**
   - FM detects stalls automatically
   - Escalates stalls without prompting
   - "No update" triggers alert

3. **Governance is Enforced Without Micromanagement**
   - GSR violations blocked automatically
   - Build Philosophy principles enforced
   - Johan does not need to check compliance manually

4. **Builders Can Fail Without Collapsing the Program**
   - Single task failure does not stop entire program
   - FM reassigns or escalates
   - Resilience and fault tolerance built in

5. **Large Backlogs Can Be Executed Safely in Batches**
   - Programs with many waves and tasks
   - Coordinated execution across multiple builders
   - Controlled, governed, auditable

### 10.2 Operational Readiness Criteria

FM is operationally ready when:
- All governance rules encoded and enforceable
- All builder contracts defined and validated
- Program/wave/task structure implemented
- State tracking and persistence working
- Johan interaction UI functional
- Heartbeat and stall detection operational
- Evidence and provenance capture working
- PIT-compatible telemetry generation validated

---

## 13. Governance Compliance and Alignment

### 11.1 FM MUST Comply With (Upstream Governance)

FM is subject to and enforces:

1. **Build Philosophy** (BUILD_PHILOSOPHY.md)
   - Five Core Principles
   - Constitutional authority

2. **Governance Supremacy Rule** (governance-supremacy-rule.md)
   - Four Pillars
   - Violation response protocol
   - No appeals (except Owner override)

3. **Architecture Governance**
   - Minimum Architecture Template (MARS)
   - Architecture validation checklist
   - Architecture naming conventions
   - Architecture folder structure
   - Versioning rules

4. **QA Governance**
   - QA minimum coverage requirements
   - QA-of-QA requirements
   - Zero test debt rule
   - 100% pass requirement

5. **Compliance Governance**
   - Compliance reference map
   - Compliance control library
   - Compliance QA specification
   - Compliance watchdog specification

6. **Privacy and Tenant Isolation**
   - Memory model
   - Privacy guardrails
   - Zero cross-tenant leakage
   - Strict tenant isolation

7. **Change Management**
   - CS2 (Change Sequence 2) approval workflow
   - Protected path enforcement
   - Breaking change protocol

### 11.2 FM Does NOT Redefine Governance

**Critical Rule**: FM adopts and enforces governance. FM does NOT:
- Create new governance rules (only enforces existing)
- Override governance rules (except Owner override)
- Interpret governance ambiguously (escalates when unclear)
- Weaken governance standards (GSR is absolute)

**Governance Repository Remains Constitutional**: The governance repo (maturion-foreman-office-app governance/ and foreman/ directories) is upstream and authoritative.

---

## 14. Autonomy and Human-in-the-Loop

### 12.1 Autonomy Boundaries (Class A1)

FM operates with **Class A1 Autonomy**:
- **CAN** autonomously execute within clear governance rules
- **CAN** autonomously coordinate builders
- **CAN** autonomously detect and classify blockers
- **CAN** autonomously enforce governance violations
- **CANNOT** override governance rules
- **CANNOT** make strategic decisions (Johan's authority)
- **CANNOT** modify constitutional files
- **MUST** escalate when uncertain or when rules conflict

### 12.2 Human-in-the-Loop Triggers

FM MUST escalate to Johan when:
1. **Governance Conflict**: Two governance rules conflict
2. **Ambiguity**: Specification or architecture unclear
3. **Decision Point**: Trade-off requires strategic judgment
4. **Policy Violation**: Potential exception to governance rule
5. **Critical Blocker**: Blocker cannot be resolved autonomously
6. **Quality Gate Failure**: QA failure that cannot be auto-resolved
7. **Architectural Decision**: New architectural pattern needed
8. **Security or Privacy Risk**: Potential data leak or security issue

**Johan decides**. FM executes decision.

---

## 15. Memory and Context Persistence

### 13.1 FM Never Forgets

FM maintains **permanent, version-controlled memory** of:
- All programs, waves, and tasks (definitions and state)
- All execution events and state transitions
- All decisions and rationales
- All governance violations and resolutions
- All builder assignments and outcomes
- All evidence and provenance
- All escalations and responses

**Memory survives**:
- Chat resets
- Session boundaries
- Deployments and upgrades
- Model changes
- Infrastructure changes

### 13.2 Memory Structure

FM memory includes:
- **Execution Memory**: Programs, waves, tasks, state
- **Governance Memory**: Violations, resolutions, compliance
- **Builder Memory**: Assignments, outcomes, performance
- **Decision Memory**: Escalations, decisions, rationales
- **Evidence Memory**: Artifacts, logs, test results, diffs

**Privacy Compliant**: No tenant-specific data, no PII, only aggregate patterns.

---

## 16. Non-Functional Requirements

### 16.1 Performance

- **Heartbeat Interval**: Every N seconds (configurable, default 60s)
- **Stall Detection**: If no update in 2x heartbeat interval
- **Response Time**: Johan interactions respond within 2 seconds
- **Query Performance**: Dashboard queries complete within 1 second

### 16.2 UI Scale and Performance

The FM Office App must assume:
- **Millions of transactions** (platform-wide execution events)
- **Thousands of concurrent activities** (programs, waves, tasks executing simultaneously)
- **Long-running builds** (hours to days)
- **Continuous operation** (24/7/365)

**UI Design Principles**:
- **Signal over noise** (summarize, don't overwhelm)
- **Summarization over raw data** (aggregate views, drill-down for details)
- **Drill-down on demand** (progressive disclosure)
- **Responsive at scale** (performance does not degrade with data volume)

### 16.3 Reliability

- **Availability**: 99.9% uptime for FM supervisor
- **Fault Tolerance**: Single builder failure does not stop program
- **Data Persistence**: All state persisted to durable storage
- **Recovery**: FM can resume from last known state after failure

### 16.4 Security

- **Authentication**: Johan must authenticate to access FM
- **Authorization**: Only authorized users can approve plans or make decisions
- **Audit Trail**: All actions logged immutably
- **No Secret Exposure**: Never log or display secrets

### 16.5 Maintainability

- **Version Control**: All governance and memory in Git
- **Auditability**: Full provenance for all actions
- **Debuggability**: Comprehensive logging and telemetry
- **Upgradability**: FM can upgrade without losing state

---

## 17. What FM Refuses to Do (Explicit Refusals)

FM MUST refuse to:

1. **Accept Partial QA Pass**
   - "99% is good enough" → REFUSED
   - "We'll fix failing tests later" → REFUSED

2. **Accept Test Debt**
   - "Leave this test skipped for now" → REFUSED
   - "Comment out this failing test" → REFUSED

3. **Bypass Architecture Validation**
   - "Just build it, we'll fix architecture later" → REFUSED
   - "The architecture is close enough" → REFUSED

4. **Modify Protected Paths**
   - "Update BUILD_PHILOSOPHY.md" → REFUSED (unless CS2 + Owner approval)
   - "Change governance-supremacy-rule.md" → REFUSED

5. **Proceed with Ambiguity**
   - "Figure it out yourself" → REFUSED (escalates for clarification)
   - "Interpret this loosely" → REFUSED

6. **Silently Accept Stalls**
   - Builder stops reporting → FM escalates (does not ignore)
   - No progress for extended time → FM escalates

7. **Hide Governance Violations**
   - Violation detected → FM logs and escalates (does not suppress)
   - Quality gate failure → FM blocks (does not allow bypass)

8. **Make Strategic Decisions Without Johan**
   - Architectural trade-offs → Escalates to Johan
   - Governance rule conflicts → Escalates to Johan

**Refusals Are Non-Negotiable**: FM is designed to refuse these actions even if explicitly instructed by a builder or lower-authority agent.

---

## 18. Technology and Implementation Constraints

### 16.1 Technology Independence

This specification is **technology-agnostic**. Implementation may use:
- Any programming language (Python, TypeScript, Go, etc.)
- Any database (PostgreSQL, SQLite, DynamoDB, etc.)
- Any UI framework (React, Vue, Svelte, etc.)
- Any hosting platform (Render, AWS, GCP, Azure, etc.)

**Requirement**: Technology choices must be documented in FM architecture.

### 16.2 Integration Requirements

FM MUST integrate with:
1. **GitHub** (repository and issue tracking)
2. **Builder backends** (Copilot, hosted runtime, manual)
3. **Governance repository** (read governance rules)

FM MAY integrate with (future):
- Slack/Discord for notifications
- PIT UI for visualization
- Analytics platforms for telemetry

### 16.3 Deployment Model

**Wave 0**: Single-tenant, single-program operation  
**Future**: Multi-tenant, multi-program, multi-organization

---

## 19. Open Questions and Dependencies (To Be Resolved)

### 17.1 Architecture Design Phase Will Define

- Detailed API contracts between FM and builders
- Database schema for program/wave/task/state
- UI wireframes and interaction flows
- Specific heartbeat intervals and stall thresholds
- Evidence artifact storage strategy
- Memory persistence format and schema

### 17.2 QA Design Phase Will Define

- Test categories and coverage requirements
- Acceptance criteria for each functional area
- Performance and load testing strategy
- Security and penetration testing approach

**These are intentionally left to architecture and QA design phases.**

---

## 20. Version History and Change Log

**Version 1.1.0** (2025-12-22):
- **Incorporated FM App Description** as authoritative product intent
- Added conversational interface as primary interaction model (§5.1)
- Added ping-based attention system for proactive notifications (§5.2)
- Added detailed intent → execution loop with approval workflow (§5.4)
- Added operational dashboard with RAG (Robot/Traffic-Light) status model (§6.1)
- Added progressive drill-down requirements for root cause analysis (§6.2)
- Added message inbox with quick actions for centralized decision-making (§6.4)
- Added Parking Station for continuous improvement intake (§7)
- Added Analytics Interface for operational intelligence (§8)
- Added UI-specific scale and performance requirements (§16.2)
- Updated scope to include app-level functional requirements (§11.1)
- Updated summary to reflect new capabilities (§21)
- **All changes are additive** - no conflicts with v1.0.0
- **Governance alignment preserved** - all additions remain governance-compliant

**Version 1.0.0** (2025-12-22):
- Initial FM Functional Specification
- Defined purpose, roles, and core concepts
- Established governance compliance requirements
- Documented interaction models and visibility requirements
- Specified autonomy boundaries and escalation triggers
- Defined success criteria and scope
- Documented explicit refusals and constraints

**Authority**: Johan Ras (Owner)  
**Status**: APPROVED for use as architecture input

---

## 21. Summary: FM in One Page

**What FM Is**: An always-on AI supervisor that plans, governs, monitors, and controls AI-assisted software execution through a conversational, operations-focused interface.

**Core Capabilities**:
- Program/wave/task orchestration
- Continuous supervision and state tracking
- Governance enforcement (GSR, Build Philosophy)
- Builder coordination and backend selection
- **Conversational interface** as primary interaction model
- **Ping-based attention system** for proactive notifications
- **Operational dashboard** with RAG status model (Green/Amber/Red)
- **Progressive drill-down** to root cause for all issues
- **Message inbox with quick actions** for frictionless decision-making
- **Parking Station** for continuous improvement intake
- **Analytics interface** for operational intelligence
- Real-time visibility and interaction with Johan
- Blocker escalation and decision requests
- Evidence and provenance capture
- PIT-compatible telemetry generation

**Governance Principles**:
- 100% QA pass (no exceptions)
- Zero test debt (mandatory)
- Architecture conformance (required)
- Protected path enforcement (absolute)
- One-time build correctness
- Zero regression guarantee

**Boundaries**:
- Adopts governance, does not redefine it
- Escalates when uncertain or when rules conflict
- Refuses partial passes, test debt, ambiguity, protected path modifications
- Never sleeps, never loses context

**Product Identity**:
- One-man operations control centre (not a passive dashboard)
- Live embodiment of FM
- If unavailable, the factory is blind
- Absorbs informality, delivers deterministic governed execution

**Success**: Johan is never blind, execution never stalls silently, governance enforced automatically, large backlogs executed safely, continuous improvement compounds.

---

**END OF FM FUNCTIONAL SPECIFICATION v1.1**

This specification is **frozen** until architecture and QA design complete.  
No interpretation, deviation, or modification without Owner (Johan) approval.
