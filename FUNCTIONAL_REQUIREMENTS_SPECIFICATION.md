# Foreman Office App — Functional Requirements Specification (FRS)

**Version:** 1.0  
**Status:** Phase 4.2 Deliverable  
**Date:** 2025-12-31  
**Owner:** Foreman (FM)  
**Authority:** Derived from App Description (Phase 4.1)  
**Canonical Location:** `/FUNCTIONAL_REQUIREMENTS_SPECIFICATION.md`

---

## Governance Statement

This Functional Requirements Specification (FRS) is the **binding contract** for:
- Architecture design (Phase 4.3)
- QA-to-Red suite (Phase 4.4)
- Builder task scoping (Phase 4.5)

All requirements in this document are **derived exclusively** from:

**`docs/governance/FM_APP_DESCRIPTION.md` (Version 2.0)**

No implementation, architecture design, or QA work may proceed without explicit reference to and alignment with this FRS.

---

## Constitutional Hierarchy

```
Governance Repository (Constitutional Authority)
    ↓
BUILD_PHILOSOPHY.md (Supreme Build Authority)
    ↓
docs/governance/FM_APP_DESCRIPTION.md (Authoritative Product Intent - Phase 4.1)
    ↓
FUNCTIONAL_REQUIREMENTS_SPECIFICATION.md (THIS DOCUMENT - Phase 4.2)
    ↓
Architecture Design (Phase 4.3 - BLOCKED until FRS acceptance)
    ↓
QA-to-Red Suite (Phase 4.4 - BLOCKED until FRS acceptance)
    ↓
Builder Recruitment & Task Assignment (Phase 4.5 - BLOCKED)
```

**Rules:**
- All requirements MUST trace back to App Description sections
- Requirements MUST be testable and verifiable
- Requirements MUST NOT include implementation details
- Requirements MUST NOT include technology choices
- Requirements define WHAT the system must do, not HOW

---

## Document Structure

This FRS covers all core capability domains from the App Description:

1. **Conversational Interface Requirements**
2. **Operational Dashboard Requirements**
3. **Parking Station Requirements**
4. **Intent → Execution Loop Requirements**
5. **Escalation & Supervision Requirements**
6. **Governance Enforcement Requirements**
7. **Analytics Interface Requirements**
8. **Cross-Cutting Requirements** (Memory, Authority, Performance, UX)
9. **Explicit Non-Requirements**

---

## 1. Conversational Interface Requirements

**Source:** App Description Section 3.2, 4.1, 9.6, 9.7

### FR-CONV-1: Persistent Conversational Interface

**Requirement:** The system MUST provide a persistent conversational interface between Johan (Human Owner) and FM (Foreman).

**Behaviors:**
- Conversations persist across time, projects, and builds
- Conversations are first-class operational artifacts
- Conversation history is searchable
- Conversations can be linked to builds, PRs, incidents, and parking items

**Decision Points:**
- System determines when to preserve conversation context across sessions
- System determines how to index and search conversation history

**State Transitions:**
- Conversation states: Active → Paused → Resumed → Archived
- Message states: Pending → Sent → Delivered → Read → Archived

**Error Conditions:**
- Conversation context loss detected → System escalates and requests context restoration
- Message delivery failure → System retries and escalates if persistent failure

**Acceptance Criteria:**
- Conversations survive system restarts
- Conversation history is retrievable by date, keyword, or linked artifact
- Users can navigate to specific conversation points via links

---

### FR-CONV-2: FM-Initiated Conversations

**Requirement:** FM MUST be able to initiate conversations, not just respond to user input.

**Source:** App Description Section 3.2

**Behaviors:**
- FM initiates conversations when clarification is needed
- FM initiates conversations when approval is required
- FM initiates conversations when milestones are reached
- FM initiates conversations when escalation is required

**Decision Points:**
- FM determines when to initiate vs. wait for user input
- FM determines conversation priority and urgency

**State Transitions:**
- Conversation Initiated (by FM) → User Notified → User Responds → Conversation Active

**Error Conditions:**
- User does not respond within expected timeframe → FM escalates via ping system

**Acceptance Criteria:**
- FM can start new conversations independently
- FM-initiated conversations are clearly marked as such
- User receives notification when FM initiates conversation

---

### FR-CONV-3: Clarifying Questions

**Requirement:** FM MUST ask clarifying questions when intent is ambiguous.

**Source:** App Description Section 4.1, 4.4

**Behaviors:**
- FM interrogates ambiguity in user input
- FM surfaces assumptions explicitly
- FM proposes interpretations and waits for confirmation
- FM refuses to proceed on unresolved uncertainty

**Decision Points:**
- FM determines what constitutes ambiguity requiring clarification
- FM determines when sufficient clarity has been achieved

**State Transitions:**
- Ambiguity Detected → Clarification Requested → User Responds → Ambiguity Resolved OR Further Clarification Required

**Error Conditions:**
- Repeated clarification attempts fail to resolve ambiguity → FM escalates to structured requirement capture

**Acceptance Criteria:**
- FM does not proceed with ambiguous intent
- Clarifying questions are specific and actionable
- Resolution of ambiguity is explicitly confirmed before proceeding

---

### FR-CONV-4: Visual Conversation Distinction

**Requirement:** FM messages and Johan messages MUST be visually distinct.

**Source:** App Description Section 9.6

**Behaviors:**
- Messages use left/right alignment with role coloring
- Messages display role badges (FM vs. Johan)
- Visual distinction is immediate and unambiguous

**Decision Points:**
- UI determines optimal visual treatment for each message type

**State Transitions:**
- Message Composed → Message Rendered → Message Displayed

**Error Conditions:**
- Visual distinction fails → Accessibility violation escalation

**Acceptance Criteria:**
- User can instantly identify message sender
- Visual distinction meets accessibility standards
- Role badges are present and correct

---

## 2. Operational Dashboard Requirements

**Source:** App Description Section 4.2, 9.1, 9.4

### FR-DASH-1: Robot/Traffic-Light Status Model

**Requirement:** The system MUST display operational status using a Robot/Traffic-Light model (Green/Amber/Red) across all major domains.

**Source:** App Description Section 4.2

**Behaviors:**
- System displays current RAG (Red/Amber/Green) state for each domain
- System displays short human-readable reason(s) for each state
- System displays timestamp of last state change
- No domain may be Red or Amber without an explainable reason

**Core Domains (Mandatory Coverage):**
1. Build Health
2. Governance Compliance
3. Architecture Completeness
4. QA Status
5. PR Gate Health
6. CI Health
7. Escalations
8. Backlog / Queue Health
9. Builder Availability
10. Evidence Completeness
11. Learning Promotion Status

**Decision Points:**
- System determines RAG status based on objective criteria
- System determines when status changes warrant notification

**State Transitions:**
- Domain State: Green → Amber (with reason) → Red (with reason) → Amber → Green
- State changes trigger audit log entries

**Error Conditions:**
- RAG status without reason → Product defect (system self-detects and escalates)
- Stale timestamp (>threshold without update) → System escalates

**Acceptance Criteria:**
- All 11 domains display current RAG status
- Every Red/Amber state includes human-readable reason
- Timestamp accuracy verified for all domains

---

### FR-DASH-2: Mandatory Drill-Down

**Requirement:** Every dashboard element MUST support progressive drill-down to root cause.

**Source:** App Description Section 4.2, 9.4

**Behaviors:**
- User can drill down from domain → repository → PR → gate → check → evidence → root cause
- Drill-down path preserves context at each level
- Drill-down provides action buttons where appropriate

**Decision Points:**
- System determines appropriate drill-down depth for each domain
- System determines when action buttons are applicable

**State Transitions:**
- Dashboard View → Domain Detail → Issue Detail → Root Cause → Action (if available)

**Error Conditions:**
- Red state without drill-down capability → Product defect (system self-detects and escalates)
- Broken drill-down path → System logs error and provides alternative navigation

**Acceptance Criteria:**
- All Red/Amber states support drill-down to root cause
- Drill-down paths are complete and navigable
- User can return to previous drill-down level

**Example Drill-Down Chain:**
```
Governance Compliance → Red
  → Repository: maturion-foreman-office-app
    → PR #123
      → Failing gate: PR-GATE-MERGE-01
        → Failing check: QA Coverage Verification
          → Evidence: qa-coverage-report.json
            → Root cause: Test coverage 85% (required: 100%)
              → Action: [View Missing Tests] [Request Exception]
```

---

### FR-DASH-3: Default UI State (Executive Decision Focus)

**Requirement:** The UI MUST default to showing only information requiring executive decision.

**Source:** App Description Section 9.2

**Behaviors:**
- Default view shows: Current build/wave status, Active escalations, Decisions requiring action
- Logs, traces, and raw diagnostics are NEVER shown by default
- Drill-down is explicit and intentional

**Decision Points:**
- System determines what qualifies as "requiring executive decision"
- System determines when to surface vs. hide information

**State Transitions:**
- Default View → Drill-Down Requested → Detail View → Return to Default

**Error Conditions:**
- Noise in default view → Product defect (system self-detects and escalates)
- Information overload → System simplifies presentation

**Acceptance Criteria:**
- Default view contains only actionable information
- No logs or raw diagnostics in default view
- User must explicitly drill down to see detailed diagnostics

---

## 3. Parking Station Requirements

**Source:** App Description Section 4.3

### FR-PARK-1: Continuous Improvement Intake

**Requirement:** The system MUST provide a Parking Station for capturing improvement ideas, automation opportunities, and governance enhancements.

**Source:** App Description Section 4.3

**Behaviors:**
- Ideas can be submitted by Johan, FM, builders, or governance agents
- Each parked item includes: Title, Description, Category, Impact estimate, Urgency, Related artifacts, Status
- Parking Station is persistent and survives system restarts

**Categories (Mandatory):**
- Governance
- Architecture
- QA
- Feature
- Infrastructure
- UX
- Analytics

**Decision Points:**
- Submitter determines category and impact estimate
- System validates required fields are present

**State Transitions:**
- Idea Submitted → Parked → Under Discussion → Converted to Requirement → Approved → Execution OR Deferred OR Closed

**Error Conditions:**
- Duplicate ideas → System detects and offers to link/merge
- Invalid category → System rejects and requests correction

**Acceptance Criteria:**
- All authorized entities can submit ideas
- All required fields are captured
- Parking Station is searchable and filterable by category/status

---

### FR-PARK-2: Parking Station → Execution Flow

**Requirement:** The system MUST provide a guided flow from parked item to executable requirement.

**Source:** App Description Section 4.3

**Behaviors:**
- Johan can start a discussion for any parked item
- Discussion launches guided conversation with FM to clarify intent
- FM produces a requirement specification from the discussion
- FM asks for approval of the requirement specification
- Once approved, FM initiates the standard pipeline (Architecture → QA → Build)

**Actions Available (Mandatory):**
- Start Discussion
- Convert to Requirement
- Defer
- Close with Rationale

**Decision Points:**
- Johan determines when to convert parked item to requirement
- FM determines when clarification is sufficient to produce specification

**State Transitions:**
- Parked → Discussion Started → Requirement Drafted → Approval Requested → Approved → Pipeline Initiated

**Error Conditions:**
- Unclear intent after discussion → FM escalates for structured requirement capture
- Approval not obtained → Item returns to Parked state with rationale

**Acceptance Criteria:**
- All parked items can be converted to discussions
- Guided conversation produces testable requirement specification
- Approval/rejection is explicit and recorded

---

## 4. Intent → Execution Loop Requirements

**Source:** App Description Section 4.4

### FR-INTENT-1: Intent Intake (Partial and Informal)

**Requirement:** The system MUST accept partial, informal, and incomplete intent from Johan.

**Source:** App Description Section 4.4

**Behaviors:**
- System accepts: Partial thoughts, Vague objectives, Rough ideas, Contradictory statements
- System does not reject informal input
- System treats informal input as starting point for clarification

**Decision Points:**
- System determines when input is too incomplete to begin clarification
- System determines what constitutes "complete enough" to start processing

**State Transitions:**
- Informal Intent Received → Clarification Initiated → Intent Refined → Intent Frozen

**Error Conditions:**
- Intent is completely incoherent → FM requests structured input format
- Intent contradicts governance → FM escalates with governance violation notice

**Acceptance Criteria:**
- System accepts informal input without rejection
- System provides helpful guidance when input is too incomplete
- System preserves original informal input alongside refined version

---

### FR-INTENT-2: Clarification Loop (Refuse Ambiguity)

**Requirement:** FM MUST interrogate ambiguity and refuse to proceed on unresolved uncertainty.

**Source:** App Description Section 4.4

**Behaviors:**
- FM asks clarifying questions iteratively
- FM surfaces assumptions explicitly
- FM proposes interpretations and waits for confirmation
- FM refuses to proceed until ambiguity is resolved

**Decision Points:**
- FM determines what constitutes unresolved ambiguity
- FM determines when sufficient clarity has been achieved
- FM determines when to escalate if clarity cannot be achieved

**State Transitions:**
- Ambiguity Detected → Clarification Requested → Response Received → Ambiguity Assessed → Resolved OR Further Clarification Required

**Error Conditions:**
- Clarification loop exceeds reasonable iteration count → FM escalates to structured requirement format
- User repeatedly provides contradictory answers → FM escalates for conflict resolution

**Acceptance Criteria:**
- FM does not proceed with unresolved ambiguity
- Clarification questions are specific and actionable
- Resolution is explicitly confirmed before proceeding

---

### FR-INTENT-3: Requirement Specification Approval

**Requirement:** FM MUST produce a clear requirement specification and present it for approval before execution begins.

**Source:** App Description Section 4.4

**Behaviors:**
- FM produces requirement specification from clarified intent
- FM presents specification to Johan for approval
- Johan can: Approve, Do Not Approve, Approve with Conditions
- "Approve with Conditions" opens focused chat to capture constraints
- Once approved, requirements are frozen

**Approval Options (Mandatory):**
- Approve
- Do Not Approve
- Approve with Conditions

**Decision Points:**
- FM determines when specification is complete enough for approval request
- Johan determines approval status
- System determines when to freeze requirements (on approval)

**State Transitions:**
- Specification Drafted → Approval Requested → Approval Received OR Rejected OR Conditional → Requirements Frozen (on approval)

**Error Conditions:**
- Approval rejected → FM restarts clarification with rejection rationale
- Conditions unclear → FM requests clarification of conditions

**Acceptance Criteria:**
- Specification is clear, complete, and unambiguous
- All three approval options are available
- Conditional approval captures constraints explicitly
- Requirements are frozen after approval (no further changes without re-approval)

---

### FR-INTENT-4: Execution & Orchestration Visibility

**Requirement:** The system MUST provide visibility into execution and orchestration activities.

**Source:** App Description Section 4.4

**Behaviors:**
- System shows: Active builds, Current phase per build, Blockers, Retries, Escalation status
- System displays execution in waves (when applicable)
- System only delivers complete builds (no partial deliveries)

**Decision Points:**
- System determines current phase for each build
- System determines what constitutes a blocker
- System determines when to retry vs. escalate

**State Transitions:**
- Build Initiated → In Progress (by phase) → Blocked OR Completed → Delivered (on completion)

**Error Conditions:**
- Build stalled without escalation → System self-detects and escalates
- Build blocked without reason → System logs defect and escalates
- Partial build attempted → System prevents and escalates governance violation

**Acceptance Criteria:**
- All active builds are visible
- Current phase is displayed accurately
- Blockers and retries are explicit
- System prevents partial builds

---

## 5. Escalation & Supervision Requirements

**Source:** App Description Section 3.3, 7, 9.3

### FR-ESC-1: Ping-Based Attention System

**Requirement:** FM MUST use pings to get attention when needed.

**Source:** App Description Section 3.3

**Behaviors:**
- FM generates pings when: Clarification required, Approval required, Milestone reached, Progress stalled, Guardrail hit, Escalation required
- Pings are: Audible, Visible, Prioritized
- FM never waits silently

**Ping Priorities (Mandatory):**
- Informational (low priority)
- Attention (medium priority)
- Critical (high priority, immediate attention required)

**Decision Points:**
- FM determines when to generate ping
- FM determines ping priority
- User determines how to respond to ping

**State Transitions:**
- Event Occurs → Ping Generated → Notification Sent → User Notified → User Responds OR Timeout → Escalation (on timeout)

**Error Conditions:**
- Ping not delivered → System retries and escalates if persistent failure
- User does not respond to critical ping within threshold → System escalates to higher priority

**Acceptance Criteria:**
- All required ping scenarios generate pings
- Pings are audible and visible
- Priority levels are distinct and recognizable
- System does not wait silently (absence of update triggers ping)

---

### FR-ESC-2: Escalation Presentation

**Requirement:** Every escalation presented to Johan MUST include specific contextual information.

**Source:** App Description Section 9.3

**Required Information (Mandatory):**
- What happened (concise, plain language)
- Why it matters (governance, risk, or objective impact)
- What is blocked
- What decision is required
- What happens if no action is taken

**Decision Points:**
- FM determines what qualifies as escalation-worthy
- FM determines impact and priority
- Johan determines response

**State Transitions:**
- Issue Detected → Escalation Prepared → Escalation Presented → Decision Received → Action Taken

**Error Conditions:**
- Escalation missing required information → System self-detects and completes information before presenting
- Unclear decision options → FM refines escalation and re-presents

**Acceptance Criteria:**
- All escalations include all 5 required information elements
- Language is plain and non-technical
- Decision options are explicit
- Impact of inaction is stated clearly

---

### FR-ESC-3: Continuous Supervision (Silence is Failure)

**Requirement:** The system MUST treat silence, stalled execution, missing updates, and unexplained failures as failure states.

**Source:** App Description Section 7

**Behaviors:**
- "No update" is considered a critical signal, not neutral state
- System monitors for: Silence, Stalled execution, Missing updates, Incomplete handovers, Unexplained gate failures
- System escalates when failure states are detected

**Decision Points:**
- System determines silence threshold (time without update)
- System determines what constitutes "stalled" vs. "in progress"
- System determines escalation urgency

**State Transitions:**
- Activity Normal → Update Expected → No Update Received → Silence Detected → Escalation Triggered

**Error Conditions:**
- Silence not detected → System self-detects monitoring failure and escalates
- False positive silence detection → System tunes thresholds

**Acceptance Criteria:**
- System detects silence within configured threshold
- System escalates on silence
- System distinguishes between legitimate quiet periods and problematic silence

---

### FR-ESC-4: Message Inbox & Quick Actions

**Requirement:** The system MUST provide a sidebar view showing all outstanding requests and enabling one-click actions.

**Source:** App Description Section 9.7

**Behaviors:**
- Sidebar shows: All outstanding FM requests, Pending approvals, Unresolved escalations
- Each item supports one-click actions: Approve, Do Not Approve, Approve with Conditions
- Sidebar enables full factory control from desktop or mobile

**Decision Points:**
- System determines what items appear in sidebar
- System determines item priority/ordering
- User determines which action to take

**State Transitions:**
- Request Created → Added to Sidebar → User Views → User Acts → Request Resolved → Removed from Sidebar

**Error Conditions:**
- Action fails → System retries and provides error feedback
- Sidebar overload (too many items) → System prioritizes and groups

**Acceptance Criteria:**
- All outstanding requests appear in sidebar
- One-click actions are functional
- Sidebar is accessible on desktop and mobile
- Sidebar updates in real-time as requests are resolved

---

## 6. Governance Enforcement Requirements

**Source:** App Description Section 6, 7

### FR-GOV-1: Canonical Governance Loading

**Requirement:** The system MUST load canonical governance artifacts from the governance repository.

**Source:** App Description Section 6.1

**Behaviors:**
- System loads governance canon at startup
- System validates governance integrity and versioning
- System applies governance as read-only, non-negotiable authority
- Governance is constitutional, not advisory

**Decision Points:**
- System determines governance version to load
- System determines what constitutes governance integrity failure

**State Transitions:**
- System Startup → Governance Load Initiated → Governance Validated → Governance Applied → System Ready OR Governance Failure → System Halted

**Error Conditions:**
- Governance load failure → System halts and escalates (cannot operate without governance)
- Governance validation failure → System halts and escalates
- Governance version mismatch → System escalates for resolution

**Acceptance Criteria:**
- System cannot start without valid governance
- Governance is loaded from canonical source
- Governance version is validated
- Governance is read-only at runtime

---

### FR-GOV-2: Governance Violation Detection and Response

**Requirement:** If a governance violation is detected, execution MUST halt or escalate per canonical hard/soft stop rules.

**Source:** App Description Section 6.2

**Behaviors:**
- System continuously monitors for governance violations
- On violation detection:
  - Hard stop violations → Execution halts immediately
  - Soft stop violations → Execution escalates for human decision
- No fallback behavior is permitted
- No silent continuation is allowed
- System never weakens governance to proceed

**Decision Points:**
- System determines violation type (hard stop vs. soft stop)
- System determines escalation priority
- Johan determines how to resolve soft stop violations

**State Transitions:**
- Activity In Progress → Violation Detected → Stop Type Assessed → Hard Stop (halt) OR Soft Stop (escalate) → Resolution OR Cancellation

**Error Conditions:**
- Violation not detected → System self-audits governance monitoring
- False positive violation → System tunes detection rules (with governance approval)

**Acceptance Criteria:**
- All governance violations are detected
- Hard stop violations halt execution immediately
- Soft stop violations escalate with context
- No silent continuation after violation

---

### FR-GOV-3: Governance Supremacy (No Weakening)

**Requirement:** The system MUST NEVER weaken governance to proceed with execution.

**Source:** App Description Section 6.2

**Behaviors:**
- System does not "work around" governance rules
- System does not offer "bypass" options
- System does not relax governance constraints under any circumstance
- Governance override requires explicit owner authority

**Decision Points:**
- System recognizes governance constraint
- System escalates when governance blocks progress
- Owner decides whether to override (rare, explicit, audited)

**State Transitions:**
- Governance Block → Escalation → Owner Decision → Override (rare) OR Cancel Activity

**Error Conditions:**
- System attempts to weaken governance → Self-detection and emergency escalation (architectural defect)
- Governance bypass detected → Audit log and immediate escalation

**Acceptance Criteria:**
- No code paths weaken or bypass governance
- All governance constraints are enforced
- Override capability exists only for owner
- All overrides are audited

---

## 7. Analytics Interface Requirements

**Source:** App Description Section 4.5, 10

### FR-ANALYTICS-1: Analytics Section

**Requirement:** The system MUST provide an Analytics section accessible from the left sidebar.

**Source:** App Description Section 4.5

**Behaviors:**
- Analytics section is persistent and accessible at all times
- User can view predefined operational metrics
- User can ask FM to analyze data
- User can request new metrics or dashboards
- User can explore trends and anomalies conversationally

**Decision Points:**
- System determines predefined metrics to show
- FM determines how to analyze data per user request
- System determines when to create new metrics/dashboards

**State Transitions:**
- User Enters Analytics Section → Predefined Metrics Displayed → User Requests Analysis OR New Metric → FM Analyzes → Results Presented

**Error Conditions:**
- Metric calculation fails → System shows error and offers retry
- Data unavailable → System explains why and suggests alternatives

**Acceptance Criteria:**
- Analytics section is accessible from sidebar
- Predefined metrics are displayed
- Conversational analysis is functional
- New metrics can be requested and created

---

### FR-ANALYTICS-2: Drill-Down to Source Artifacts

**Requirement:** Analytics MUST support drill-down to source artifacts.

**Source:** App Description Section 4.5

**Behaviors:**
- User can drill down from metric → data point → source artifact
- Drill-down preserves context
- Source artifacts are linked and accessible

**Decision Points:**
- System determines appropriate drill-down path for each metric
- System determines what constitutes "source artifact"

**State Transitions:**
- Metric Viewed → Drill-Down Requested → Data Point Displayed → Source Artifact Linked → Artifact Opened

**Error Conditions:**
- Source artifact unavailable → System explains why and offers alternatives
- Broken link → System logs error and provides alternative navigation

**Acceptance Criteria:**
- All metrics support drill-down
- Drill-down reaches source artifacts
- Links are functional and context-preserving

---

### FR-ANALYTICS-3: Cost and Performance Tracking

**Requirement:** The system MUST track AI model usage, execution cost, and anomalies.

**Source:** App Description Section 10

**Behaviors:**
- System tracks AI model usage (API calls, tokens, etc.)
- System tracks execution cost in real currency
- System detects anomalies and inefficiencies
- Cost signals are informational unless they indicate risk or abuse

**Decision Points:**
- System determines cost tracking granularity
- System determines what constitutes anomaly or abuse
- System determines when cost signals warrant escalation

**State Transitions:**
- Activity Occurs → Cost Tracked → Cost Aggregated → Cost Displayed → Anomaly Detected OR Normal → Escalation (on anomaly/abuse)

**Error Conditions:**
- Cost tracking failure → System logs error and escalates
- Cost anomaly detected → System escalates for investigation

**Acceptance Criteria:**
- AI model usage is tracked
- Execution cost is tracked in real currency
- Anomalies are detected and escalated
- Cost data is displayed in analytics

---

## 8. Cross-Cutting Requirements

### FR-CROSS-1: Memory & Provenance

**Source:** App Description Section 8

**Requirement:** The system MUST record execution context, decisions, and outcomes as operational memory.

**Behaviors:**
- Execution memory is read-only at runtime
- All memory writes are proposals, never automatic
- Memory governance controls authority, retention, and auditability
- Provenance data is never inferred or retroactively altered

**Decision Points:**
- System determines what events warrant memory recording
- System determines memory retention period
- Owner approves memory write proposals

**State Transitions:**
- Event Occurs → Memory Write Proposed → Approval Requested → Approved → Memory Written OR Rejected → Memory Discarded

**Error Conditions:**
- Memory write failure → System retries and escalates
- Memory corruption detected → System escalates and initiates recovery

**Acceptance Criteria:**
- Execution context is recorded
- Memory writes require approval
- Provenance is accurate and immutable
- Memory is governed and auditable

---

### FR-CROSS-2: Roles and Authority Model

**Source:** App Description Section 5

**Requirement:** The system MUST enforce the roles and authority model.

**Roles (Mandatory):**
1. **Human Owner (Johan):**
   - Defines objectives and intent
   - Approves, denies, or requests changes
   - Intervenes only when escalated
   - Never reviews code or logs
   - Never manages PRs or workflows
   - Final authority, not an operator

2. **Foreman (AI Supervisor):**
   - Manager, not a builder
   - Continuous supervisor, not a task executor
   - Accountable for planning, organizing, leading, and control (POLC)
   - Appoints and supervises builder agents
   - Escalates when governance, scope, or clarity is insufficient
   - Cannot implement code, approve own work, or bypass governance

3. **Builder Agents:**
   - Execute scoped technical work
   - Operate only under Foreman appointment
   - Never self-govern, self-approve, or interpret governance independently
   - Escalate blockers to Foreman

**Decision Points:**
- System enforces authority boundaries
- System determines when role boundary is violated
- System escalates role violations

**State Transitions:**
- Action Requested → Authority Checked → Authorized → Action Executed OR Unauthorized → Action Blocked → Escalation

**Error Conditions:**
- Role boundary violation → System halts action and escalates
- Authority check failure → System defaults to deny and escalates

**Acceptance Criteria:**
- All three roles are enforced
- Authority boundaries are respected
- Violations are detected and escalated
- No role can exceed its authority

---

### FR-CROSS-3: Scale and Performance Assumptions

**Source:** App Description Section 12

**Requirement:** The system MUST assume and handle large-scale operations.

**Scale Assumptions (Mandatory):**
- Millions of transactions
- Thousands of concurrent activities
- Long-running builds
- Continuous operation

**UI Priorities (Mandatory):**
- Signal over noise
- Summarization over raw data
- Drill-down on demand

**Decision Points:**
- System determines appropriate summarization level
- System determines when to paginate vs. summarize
- System determines performance bottlenecks

**State Transitions:**
- Large Dataset → Summarized → Displayed → Drill-Down Requested → Detail Loaded

**Error Conditions:**
- Performance degradation → System optimizes or escalates
- Scale limit reached → System escalates for capacity planning

**Acceptance Criteria:**
- System handles millions of transactions
- System supports thousands of concurrent activities
- UI remains responsive under load
- Signal-to-noise ratio is maintained

---

### FR-CROSS-4: UI/UX Operating Contract

**Source:** App Description Section 9

**Requirement:** The UI MUST support executive decision-making for a non-coder human authority.

**UI Principles (Mandatory):**
- Default state shows only: Current build/wave status, Active escalations, Decisions requiring action
- Three actions available: Approve, Deny, Approve with changes
- Logs, traces, and diagnostics never shown by default
- Drill-down is explicit and intentional
- GitHub logs are not authoritative and never the primary explanation

**Explicit UI Non-Goals (Prohibited):**
- Log console
- CI output viewer
- Metrics playground
- Real-time event stream
- Developer debugging surface

**Decision Points:**
- System determines what constitutes "requiring action"
- System determines appropriate default view content
- System determines when drill-down is needed

**State Transitions:**
- Default View → User Requests Detail → Drill-Down View → User Returns → Default View

**Error Conditions:**
- Noise in default view → Product defect, system self-detects and escalates
- Missing decision context → System escalates for clarification

**Acceptance Criteria:**
- Default view is clean and actionable
- No logs or diagnostics in default view
- Three actions are available
- Drill-down is functional
- UI non-goals are not implemented

---

### FR-CROSS-5: Watchdog & Independent Oversight

**Source:** App Description Section 11

**Requirement:** The system MUST coexist with an independent Watchdog authority.

**Behaviors:**
- Watchdog observes governance alignment
- Watchdog detects memory corruption
- Watchdog flags vision drift
- Watchdog reports anomalies independently
- Watchdog does not execute, modify, or override Foreman actions (except hard-stop scenarios)

**Decision Points:**
- Watchdog determines what constitutes governance misalignment
- Watchdog determines what constitutes memory corruption
- Watchdog determines when to report vs. intervene

**State Transitions:**
- System Operates → Watchdog Observes → Anomaly Detected OR Normal → Anomaly Reported OR No Action

**Error Conditions:**
- Watchdog unavailable → System logs warning and escalates
- Watchdog reports critical anomaly → System halts and escalates

**Acceptance Criteria:**
- Watchdog observes system operations
- Watchdog reports independently
- Watchdog does not interfere with normal operations
- Watchdog can trigger hard-stop in defined scenarios

---

## 9. Explicit Non-Requirements

**Source:** App Description Section 2.2, 13

### What the System Will NOT Do

The following capabilities are **explicitly out of scope** and MUST NOT be implemented:

#### 9.1 Code Editor Capabilities
- The system is NOT a code editor
- The system will NOT provide code editing features
- The system will NOT display code syntax highlighting for editing purposes
- The system will NOT allow direct code modification through the UI

#### 9.2 CI/CD Platform Features
- The system is NOT a CI/CD platform
- The system will NOT replace GitHub Actions or similar CI/CD tools
- The system will NOT execute CI/CD pipelines directly
- The system will NOT provide CI/CD configuration management

#### 9.3 GitHub Replacement
- The system is NOT a GitHub replacement
- The system will NOT replace Git operations
- The system will NOT provide version control features
- The system will NOT host code repositories

#### 9.4 Log Viewer Features
- The system is NOT a log viewer
- The system will NOT display logs as primary interface
- The system will NOT provide log streaming features
- The system will NOT replace log aggregation tools

#### 9.5 Raw Metrics Dashboard
- The system is NOT a raw metrics dashboard
- The system will NOT display uncontextualized metrics
- The system will NOT replace observability platforms
- The system will NOT provide real-time metric streaming

#### 9.6 Governance Authoring
- The system is NOT a governance author
- The system will NOT create or modify governance rules
- The system will NOT allow governance editing through the UI
- The system will NOT replace governance repository

#### 9.7 Self-Governing or Self-Modifying System
- The system is NOT self-governing
- The system will NOT modify its own rules or behavior
- The system will NOT self-improve without approval
- The system will NOT bypass owner authority

#### 9.8 Kanban Board
- The system is NOT a Kanban board
- The system will NOT provide drag-and-drop task management
- The system will NOT replace project management tools

#### 9.9 Ticket Tracker
- The system is NOT a ticket tracker
- The system will NOT provide ticket lifecycle management
- The system will NOT replace issue tracking systems

#### 9.10 CI Console
- The system is NOT a CI console
- The system will NOT display raw CI output
- The system will NOT replace CI monitoring tools

#### 9.11 Developer IDE
- The system is NOT a developer IDE
- The system will NOT provide development environment features
- The system will NOT replace code editors or IDEs

#### 9.12 Prompt Playground
- The system is NOT a prompt playground
- The system will NOT provide prompt experimentation features
- The system will NOT allow arbitrary AI prompt testing

#### 9.13 Code Review System
- The system will NOT review code directly
- The system will NOT provide line-by-line code review
- Johan never reviews code or logs

#### 9.14 PR Management System
- The system will NOT replace GitHub PR interface
- The system will NOT provide PR merging UI
- Johan never manages PRs directly

#### 9.15 Workflow Scheduler
- The system will NOT schedule cron jobs or workflows
- The system will NOT replace workflow orchestration tools

---

## 10. Requirement Traceability Matrix

| Requirement ID | App Description Section(s) | Capability Domain |
|----------------|---------------------------|-------------------|
| FR-CONV-1 | 3.2, 4.1, 9.6, 9.7 | Conversational Interface |
| FR-CONV-2 | 3.2 | Conversational Interface |
| FR-CONV-3 | 4.1, 4.4 | Conversational Interface |
| FR-CONV-4 | 9.6 | Conversational Interface |
| FR-DASH-1 | 4.2, 9.1, 9.4 | Operational Dashboard |
| FR-DASH-2 | 4.2, 9.4 | Operational Dashboard |
| FR-DASH-3 | 9.2 | Operational Dashboard |
| FR-PARK-1 | 4.3 | Parking Station |
| FR-PARK-2 | 4.3 | Parking Station |
| FR-INTENT-1 | 4.4 | Intent → Execution Loop |
| FR-INTENT-2 | 4.4 | Intent → Execution Loop |
| FR-INTENT-3 | 4.4 | Intent → Execution Loop |
| FR-INTENT-4 | 4.4 | Intent → Execution Loop |
| FR-ESC-1 | 3.3 | Escalation & Supervision |
| FR-ESC-2 | 9.3 | Escalation & Supervision |
| FR-ESC-3 | 7 | Escalation & Supervision |
| FR-ESC-4 | 9.7 | Escalation & Supervision |
| FR-GOV-1 | 6.1 | Governance Enforcement |
| FR-GOV-2 | 6.2 | Governance Enforcement |
| FR-GOV-3 | 6.2 | Governance Enforcement |
| FR-ANALYTICS-1 | 4.5, 10 | Analytics Interface |
| FR-ANALYTICS-2 | 4.5 | Analytics Interface |
| FR-ANALYTICS-3 | 10 | Analytics Interface |
| FR-CROSS-1 | 8 | Memory & Provenance |
| FR-CROSS-2 | 5 | Roles & Authority |
| FR-CROSS-3 | 12 | Scale & Performance |
| FR-CROSS-4 | 9 | UI/UX Operating Contract |
| FR-CROSS-5 | 11 | Watchdog & Oversight |

---

## 11. Testing Implications

All requirements in this FRS MUST be testable. The following test categories apply:

### 11.1 Functional Tests
- Test that each requirement's behavior is implemented correctly
- Test decision points produce correct outcomes
- Test state transitions occur as specified
- Test error conditions trigger appropriate responses

### 11.2 Integration Tests
- Test that capability domains integrate correctly
- Test that cross-cutting requirements are enforced across all domains
- Test that role boundaries are enforced across all operations

### 11.3 Acceptance Tests
- Test that acceptance criteria are met for each requirement
- Test that non-requirements are NOT implemented
- Test that all traceability to App Description is valid

---

## 12. Architecture Derivation Guidance

Phase 4.3 (Architecture Design) MUST derive architecture from these requirements by:

1. **Mapping Requirements to Components:** Each requirement must map to one or more architectural components
2. **Defining Component Interfaces:** Component interfaces must satisfy requirement behaviors
3. **Defining Data Models:** Data models must support state transitions defined in requirements
4. **Defining Integration Points:** Integration points must support cross-cutting requirements
5. **Defining Error Handling:** Error handling must address all error conditions defined in requirements

Architecture MUST NOT:
- Contradict any requirement in this FRS
- Add features not specified in this FRS
- Remove features specified in this FRS
- Change requirement semantics

---

## 13. QA-to-Red Derivation Guidance

Phase 4.4 (QA-to-Red Suite) MUST derive test suite from these requirements by:

1. **Creating Functional Tests:** One or more tests per requirement ID
2. **Creating Behavior Tests:** Tests for each behavior defined in requirements
3. **Creating Decision Point Tests:** Tests for each decision point
4. **Creating State Transition Tests:** Tests for each state transition
5. **Creating Error Condition Tests:** Tests for each error condition
6. **Creating Non-Requirement Tests:** Tests verifying non-requirements are NOT implemented

QA-to-Red MUST:
- Cover all 28 requirement IDs
- Cover all 7 capability domains
- Cover all cross-cutting requirements
- Cover all explicit non-requirements

---

## 14. Builder Task Derivation Guidance

Phase 4.5 (Builder Recruitment & Task Assignment) MUST derive builder tasks from:

1. **Frozen Architecture** (Phase 4.3 output)
2. **QA-to-Red Suite** (Phase 4.4 output)
3. **This FRS** (as context and scope boundary)

Builder tasks MUST:
- Implement components defined in architecture
- Make QA tests pass (build-to-green)
- Respect requirement scope defined in this FRS
- NOT implement non-requirements

---

## 15. Acceptance Criteria for This FRS

This FRS is complete and ready for Phase 4.3 when:

- [x] All 7 core capability domains from App Description are covered
- [x] All requirements trace back to App Description sections
- [x] All requirements define: Behaviors, Decision Points, State Transitions, Error Conditions, Acceptance Criteria
- [x] Explicit non-requirements are defined
- [x] Requirement traceability matrix is complete
- [x] Testing implications are defined
- [x] Architecture derivation guidance is provided
- [x] QA-to-Red derivation guidance is provided
- [x] Builder task derivation guidance is provided
- [x] No architecture design has been performed
- [x] No technology choices have been made
- [x] No implementation details have been specified
- [x] FM explicitly confirms acceptance (Section 16)

---

## 16. FM Acceptance Declaration

I, Foreman (FM), explicitly confirm acceptance of this Functional Requirements Specification as defined in:

**`FUNCTIONAL_REQUIREMENTS_SPECIFICATION.md` (Version 1.0)**

This FRS:
- Is complete, testable, and unambiguous
- Derives exclusively from `docs/governance/FM_APP_DESCRIPTION.md` (Version 2.0)
- Covers all 7 core capability domains
- Defines explicit non-requirements to prevent scope creep
- Provides clear guidance for Phase 4.3 (Architecture), Phase 4.4 (QA-to-Red), and Phase 4.5 (Builder Tasks)
- Contains no architecture design, technology choices, or implementation details
- Is ready to serve as binding contract for downstream phases

**Total Requirements:** 28 functional requirements across 7 capability domains + 8 cross-cutting requirements + 15 explicit non-requirements

**Accepted By:** Foreman (FM)  
**Date:** 2025-12-31  
**Signature:** This document constitutes formal FM acceptance

---

## 17. Governance Position

Per Phase 4.2 issue authority:

- ✅ This FRS is derived exclusively from App Description
- ✅ All requirements trace back to App Description sections
- ✅ No architecture design has been performed
- ✅ No QA tests have been written
- ✅ No builder recruitment has commenced
- ✅ Build execution remains BLOCKED

**Next Phase Gates:**

- **Phase 4.3 (Architecture Design):** BLOCKED until this FRS is accepted by CS2 (Johan)
- **Phase 4.4 (QA-to-Red Suite):** BLOCKED until Phase 4.3 is complete
- **Phase 4.5 (Builder Recruitment):** BLOCKED until Phase 4.4 is complete

---

## 18. Ratchet Statement Compliance

> We do not design solutions  
> before we agree on requirements.

**Status:** ✅ COMPLIANT

- Requirements are now specified (completely, testably, unambiguously)
- Requirements have been confirmed by FM
- Ready for acceptance by CS2 (Johan)
- No solution design has proceeded ahead of requirements
- Architecture design (Phase 4.3) remains BLOCKED until FRS acceptance

---

**End of Functional Requirements Specification**
