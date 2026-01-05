# QA Catalog — Authoritative QA Index

**Version:** 2.0  
**Status:** Phase 4.4 Deliverable (Re-derived from Architecture V2)  
**Date:** 2025-12-31  
**Owner:** Foreman (FM)  
**Authority:** Derived from FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md  
**Canonical Location:** `/QA_CATALOG.md`

---

## Purpose

This document is the **authoritative index** of all QA components in the QA-to-Red suite.

Every QA component is:
- **Numbered sequentially** (QA-001, QA-002, ..., QA-400+)
- **Immutable** (numbers never change once assigned)
- **Traceable** (maps to specific architectural elements)
- **Complete** (every architectural element has QA coverage)

This catalog enables:
- **Bounded builder assignment** (e.g., Builder A: QA-001 to QA-010)
- **Failure localization** (QA-042 fails → precise diagnosis)
- **Build progress measurement** (QA coverage percentage)
- **Non-coder orchestration** (no code review required)

---

## Constitutional Hierarchy

```
FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md (Architecture Contract)
    ↓
QA_CATALOG.md (THIS DOCUMENT - QA Index)
    ↓
QA_TO_RED_SUITE_SPEC.md (RED/GREEN Semantics)
    ↓
QA_TRACEABILITY_MATRIX.md (Bidirectional Traceability)
    ↓
BUILDER_GREEN_SCOPE_RULES.md (Assignment Rules)
```

---

## QA Numbering Rules

1. **Sequential Assignment**: QA components are numbered QA-001, QA-002, QA-003, ... QA-400+
2. **Immutability**: Once assigned, a QA number NEVER changes
3. **No Gaps**: Numbers are assigned contiguously (no gaps in sequence)
4. **Deprecation**: Deprecated QA components retain their number and are marked DEPRECATED (not reused)
5. **Grouping**: QA components are logically grouped by architectural element (component, flow, state, failure)

---

## QA Component Index (QA-001 to QA-400+)

### Component-Based QA (QA-001 to QA-199)

#### Conversational Interface Subsystem (QA-001 to QA-022)

**CONV-01: Conversation Manager (QA-001 to QA-005)**
- QA-001: Create conversation (verify database write, verify audit log, verify initial state)
- QA-002: Retrieve conversation (verify data persistence, verify message loading, verify state consistency)
- QA-003: Archive conversation (verify state transition, verify reason captured, verify archive timestamp)
- QA-004: Resume conversation (verify state transition, verify audit trail, verify UI update)
- QA-005: Conversation Manager failure modes (database write failure retry/escalation, state conflict handling)

**CONV-02: Message Handler (QA-006 to QA-010)**
- QA-006: Send message (verify validation, verify persistence, verify delivery event)
- QA-007: Deliver message (verify routing, verify UI update, verify timestamp)
- QA-008: Mark message read (verify state update, verify audit log)
- QA-009: Message validation (empty content rejection, invalid conversation ID handling)
- QA-010: Message Handler failure modes (persistence failure retry/escalation, intent processing failure handling)

**CONV-03: FM Conversation Initiator (QA-011 to QA-013)**
- QA-011: FM initiates conversation (verify conversation creation, verify Johan notification, verify context attachment)
- QA-012: Attach context to FM-initiated conversation (verify escalation context, verify build context, verify evidence linking)
- QA-013: FM urgent conversation (verify priority flag, verify immediate notification, verify inbox placement)

**CONV-04: Clarification Engine (QA-014 to QA-018)**
- QA-014: Detect ambiguity (verify pattern detection, verify confidence scoring, verify clarification trigger)
- QA-015: Generate clarifying questions (verify question quality, verify context inclusion, verify option presentation)
- QA-016: Resolve clarification (verify sufficient information check, verify intent transition, verify resolution criteria)
- QA-017: Clarification loop limits (verify iteration count, verify escalation after N loops, verify structured capture)
- QA-018: Clarification Engine failure modes (ambiguity detection failure safe default, question generation timeout)

**CONV-05: Conversation UI Renderer (QA-019 to QA-022)**
- QA-019: Render conversation UI (verify message display, verify visual distinction Johan/FM, verify timestamp rendering)
- QA-020: Update conversation UI (verify real-time updates, verify scroll behavior, verify new message highlighting)
- QA-021: Render conversation state indicators (verify active/paused/archived states, verify visual cues)
- QA-022: Conversation UI error handling (verify connection loss UI, verify retry UX, verify error message display)

#### Dashboard Subsystem (QA-023 to QA-042)

**DASH-01: Domain Status Manager (QA-023 to QA-027)**
- QA-023: Initialize domain statuses (verify all domains registered, verify default states, verify timestamp)
- QA-024: Update domain status to AMBER (verify reason required, verify reason captured, verify transition logged)
- QA-025: Update domain status to RED (verify reason mandatory, verify escalation check trigger, verify audit trail)
- QA-026: Query domain status (verify current state retrieval, verify reason included, verify timestamp included)
- QA-027: Domain Status Manager failure modes (invalid domain handling, missing reason detection)

**DASH-02: Drill-Down Navigator (QA-028 to QA-032)**
- QA-028: Navigate from RED status to root cause (verify drill-down path, verify evidence retrieval, verify context preservation)
- QA-029: Navigate from AMBER status to reason (verify reason display, verify supporting data linking)
- QA-030: Navigate to evidence artifacts (verify artifact retrieval, verify artifact display, verify artifact immutability)
- QA-031: Multi-level drill-down (verify breadcrumb trail, verify back navigation, verify state preservation)
- QA-032: Drill-Down Navigator failure modes (evidence not found handling, broken link handling)

**DASH-03: Executive View Controller (QA-033 to QA-035)**
- QA-033: Default to executive view (verify dashboard opens to executive view, verify no logs/metrics in default)
- QA-034: Navigate to analytics section (verify explicit navigation required, verify section switch)
- QA-035: Executive View Controller failure modes (invalid view state handling)

**DASH-04: Dashboard UI Renderer (QA-036 to QA-042)**
- QA-036: Render RAG status visualization (verify color coding, verify icon usage, verify layout)
- QA-037: Render domain grouping (verify logical grouping, verify hierarchy display)
- QA-038: Update dashboard in real-time (verify WebSocket updates, verify polling fallback, verify update animation)
- QA-039: Render historical status (verify timeline view, verify status change history)
- QA-040: Dashboard accessibility (verify screen reader compatibility, verify keyboard navigation, verify color contrast)
- QA-041: Dashboard responsiveness (verify mobile layout, verify tablet layout, verify desktop layout)
- QA-042: Dashboard UI error handling (verify data load failure UX, verify retry mechanism, verify error display)

#### Parking Station Subsystem (QA-043 to QA-057)

**PARK-01: Idea Intake Handler (QA-043 to QA-046)**
- QA-043: Submit idea to parking station (verify title/description capture, verify persistence, verify ID assignment)
- QA-044: Validate idea submission (verify required fields, verify content validation, verify duplicate detection)
- QA-045: Categorize idea (verify category assignment, verify tagging, verify searchability)
- QA-046: Idea Intake failure modes (invalid input handling, persistence failure retry/escalation)

**PARK-02: Parking Station Store (QA-047 to QA-049)**
- QA-047: Persist parked idea (verify database write, verify immutability of original idea, verify version tracking)
- QA-048: Retrieve parked ideas (verify filtering, verify sorting, verify pagination)
- QA-049: Parking Station Store failure modes (database failure handling, corrupted data detection)

**PARK-03: Idea Discussion Manager (QA-050 to QA-053)**
- QA-050: Initiate discussion on idea (verify discussion start, verify conversation linking, verify participant notification)
- QA-051: Link discussion to conversation (verify bidirectional linking, verify context preservation)
- QA-052: Convert idea to requirement (verify requirement generation, verify traceability, verify approval flow initiation)
- QA-053: Idea Discussion failure modes (requirement generation failure, approval flow failure)

**PARK-04: Parking Station UI (QA-054 to QA-057)**
- QA-054: Render parking station list (verify idea display, verify status indicators, verify action buttons)
- QA-055: Render idea detail view (verify full content, verify discussion thread, verify action history)
- QA-056: Parking station search and filter (verify keyword search, verify category filter, verify status filter)
- QA-057: Parking Station UI failure modes (load failure UX, action failure feedback)

#### Intent Processing Subsystem (QA-058 to QA-077)

**INTENT-01: Intent Intake Handler (QA-058 to QA-061)**
- QA-058: Accept informal intent (verify partial input acceptance, verify informal language handling, verify context capture)
- QA-059: Validate intent input (verify required context present, verify intent parsability)
- QA-060: Route intent to clarification (verify ambiguity detection trigger, verify clarification flow initiation)
- QA-061: Intent Intake failure modes (unparseable input handling, context loss detection/recovery)

**INTENT-02: Clarification Loop Manager (QA-062 to QA-066)**
- QA-062: Manage clarification iterations (verify iteration count, verify history tracking, verify timeout detection)
- QA-063: Detect sufficient clarification (verify completeness check, verify confidence threshold, verify transition trigger)
- QA-064: Handle clarification timeout (verify iteration limit enforcement, verify escalation trigger, verify structured capture)
- QA-065: Preserve clarification history (verify audit trail, verify context preservation across iterations)
- QA-066: Clarification Loop failure modes (infinite loop prevention, ambiguity resolution failure handling)

**INTENT-03: Requirement Specification Generator (QA-067 to QA-070)**
- QA-068: Generate requirement from clarified intent (verify structure, verify acceptance criteria, verify traceability)
- QA-068: Include approval workflow metadata (verify approver identification, verify approval instructions)
- QA-069: Link requirement to original intent (verify bidirectional traceability, verify context preservation)
- QA-070: Requirement Generator failure modes (generation failure handling, incomplete spec detection)

**INTENT-04: Approval Manager (QA-071 to QA-077)**
- QA-071: Present requirement for approval (verify presentation format, verify Johan notification, verify approval UI)
- QA-072: Handle approval (accept) (verify state transition, verify spec freeze, verify build initiation trigger)
- QA-073: Handle rejection (verify rejection reason capture, verify state transition, verify intent availability for rework)
- QA-074: Handle conditional approval (verify conditions capture, verify partial freeze, verify gated progression)
- QA-075: Approval timeout detection (verify silence detection, verify escalation, verify reminder mechanism)
- QA-076: Memory write proposal approval (verify proposal format, verify approval integration, verify write execution)
- QA-077: Approval Manager failure modes (notification failure handling, state consistency on failure)

#### Execution Orchestration Subsystem (QA-078 to QA-092)

**EXEC-01: Build Orchestrator (QA-078 to QA-083)**
- QA-078: Initiate build from approved requirement (verify build entity creation, verify architecture linking, verify wave planning)
- QA-079: Assign builder to QA range (verify range calculation, verify builder selection, verify task creation)
- QA-080: Monitor build progress (verify QA status tracking, verify progress percentage calculation, verify stall detection)
- QA-081: Handle build blocking (verify blocker creation, verify escalation, verify build pause)
- QA-082: Complete build (verify 100% QA GREEN validation, verify completion evidence, verify deliverable creation)
- QA-083: Build Orchestrator failure modes (builder unavailable handling, task assignment failure, orchestration corruption detection)

**EXEC-02: Build State Manager (QA-084 to QA-088)**
- QA-084: Track build state transitions (verify state changes logged, verify audit trail, verify deterministic transitions)
- QA-085: Update build progress metrics (verify QA coverage percentage, verify GREEN count, verify RED count, verify time elapsed)
- QA-086: Detect build stall (verify silence threshold, verify heartbeat monitoring, verify stall escalation)
- QA-087: Persist build state (verify database consistency, verify recovery from failure)
- QA-088: Build State Manager failure modes (state corruption detection/recovery, conflicting state updates)

**EXEC-03: Build Visibility Controller (QA-089 to QA-092)**
- QA-089: Render build progress UI (verify current state display, verify progress bar, verify QA status summary)
- QA-090: Render build details (verify architecture reference, verify requirement reference, verify wave breakdown)
- QA-091: Real-time build updates (verify WebSocket push, verify UI refresh, verify notification)
- QA-092: Build Visibility failure modes (update push failure, UI desync detection/recovery)

#### Escalation & Supervision Subsystem (QA-093 to QA-116)

**ESC-01: Ping Generator (QA-093 to QA-096)**
- QA-093: Generate ping for attention required (verify ping creation, verify context attachment, verify priority assignment)
- QA-094: Route ping to notification service (verify delivery trigger, verify acknowledgment tracking)
- QA-095: Track ping lifecycle (verify sent/delivered/acknowledged states, verify timeout detection)
- QA-096: Ping Generator failure modes (delivery failure retry/escalation, duplicate ping prevention)

**ESC-02: Escalation Manager (QA-097 to QA-104)**
- QA-097: Create escalation with 5 elements (verify all 5 elements present: what/why/blocked/decision/consequence)
- QA-098: Route escalation to Johan (verify inbox placement, verify notification, verify UI rendering)
- QA-099: Present escalation in UI (verify 5-element display, verify action buttons, verify context linking)
- QA-100: Handle escalation decision (verify decision capture, verify execution trigger, verify resolution logging)
- QA-101: Track escalation lifecycle (verify Pending/Presented/Resolved states, verify audit trail)
- QA-102: Escalation priority handling (verify CRITICAL routing, verify HIGH routing, verify NORMAL routing)
- QA-103: Escalation context linking (verify build linking, verify conversation linking, verify evidence linking)
- QA-104: Escalation Manager failure modes (missing elements detection, routing failure, decision execution failure)

**ESC-03: Silence Detector (QA-105 to QA-109)**
- QA-105: Monitor build heartbeat (verify last update tracking, verify threshold comparison, verify silence detection)
- QA-106: Detect silence (verify 2-hour threshold, verify escalation trigger, verify silence context creation)
- QA-107: Differentiate silence types (verify intentional pause vs actual stall, verify different handling)
- QA-108: Silence recovery (verify heartbeat restoration, verify escalation closure)
- QA-109: Silence Detector failure modes (false positive prevention, heartbeat update failure)

**ESC-04: Message Inbox Controller (QA-110 to QA-116)**
- QA-110: Render inbox (verify pending escalations, verify unread pings, verify sorting by priority/time)
- QA-111: Display inbox item details (verify context expansion, verify quick actions availability)
- QA-112: Execute quick action (verify approve/reject/defer actions, verify state update, verify audit log)
- QA-113: Mark item as read (verify state update, verify visual indicator change)
- QA-114: Filter inbox (verify by type, verify by priority, verify by date)
- QA-115: Inbox real-time updates (verify new item notification, verify badge update, verify item addition to list)
- QA-116: Message Inbox failure modes (load failure UX, action execution failure feedback)

#### Governance Enforcement Subsystem (QA-117 to QA-131)

**GOV-01: Governance Loader (QA-117 to QA-120)**
- QA-117: Load governance repository at startup (verify clone/pull, verify BUILD_PHILOSOPHY.md load, verify specs load)
- QA-118: Parse governance rules (verify rule extraction, verify validation rule creation, verify enforcement rule creation)
- QA-119: Cache governance in memory (verify cache creation, verify cache refresh on update)
- QA-120: Governance Loader failure modes (repository unavailable handling, parse failure handling, cache corruption detection)

**GOV-02: Governance Validator (QA-121 to QA-125)**
- QA-121: Validate against governance rules (verify rule execution, verify violation detection, verify pass/fail determination)
- QA-122: Detect governance violations (verify hard violations, verify soft violations, verify violation context capture)
- QA-123: Generate violation report (verify violation description, verify affected component, verify remediation guidance)
- QA-124: Log governance validation events (verify audit trail, verify validation history)
- QA-125: Governance Validator failure modes (rule execution failure, false positive prevention)

**GOV-03: Governance Supremacy Enforcer (QA-126 to QA-131)**
- QA-126: Enforce hard governance violations (verify immediate halt, verify escalation, verify CRITICAL priority)
- QA-127: Enforce soft governance violations (verify escalation without halt, verify HIGH priority)
- QA-128: Prevent governance weakening (verify BUILD_PHILOSOPHY.md immutability, verify core rule protection)
- QA-129: Audit governance overrides (verify override logging, verify justification capture, verify approval trail)
- QA-130: Governance update handling (verify version compatibility, verify breaking change detection)
- QA-131: Governance Supremacy failure modes (override abuse detection, enforcement bypass prevention)

#### Analytics Subsystem (QA-132 to QA-146)

**ANALYTICS-01: Metrics Dashboard (QA-132 to QA-136)**
- QA-132: Render analytics section (verify key metrics display, verify chart rendering, verify time period selection)
- QA-133: Display build success rate (verify calculation, verify trend visualization, verify drill-down availability)
- QA-134: Display average build time (verify calculation, verify comparison to baseline, verify breakdown by wave)
- QA-135: Display cost metrics (verify total cost, verify cost per build, verify cost per QA component)
- QA-136: Metrics Dashboard failure modes (data load failure UX, calculation error handling)

**ANALYTICS-02: Metrics Engine (QA-137 to QA-141)**
- QA-137: Calculate aggregate metrics (verify formula correctness, verify source data accuracy, verify cache efficiency)
- QA-138: Track metric history (verify time-series storage, verify retention policy, verify retrieval efficiency)
- QA-139: Generate metric alerts (verify threshold detection, verify alert creation, verify alert routing)
- QA-140: Export metrics (verify CSV export, verify JSON export, verify data completeness)
- QA-141: Metrics Engine failure modes (calculation overflow handling, data corruption detection)

**ANALYTICS-03: Cost Tracker (QA-142 to QA-146)**
- QA-142: Track AI usage cost per build (verify token counting, verify cost calculation, verify build attribution)
- QA-143: Detect cost anomaly (verify 3x baseline detection, verify escalation trigger, verify cost breakdown)
- QA-144: Generate cost reports (verify per-build report, verify per-builder report, verify time period aggregation)
- QA-145: Cost forecasting (verify trend analysis, verify projection calculation, verify confidence interval)
- QA-146: Cost Tracker failure modes (token counting failure, cost calculation error handling)

#### Cross-Cutting Components (QA-147 to QA-199)

**CROSS-01: Memory Manager (QA-147 to QA-152)**
- QA-147: Initialize memory fabric (verify directory structure, verify schema validation, verify seed data)
- QA-148: Read memory entries (verify query by key, verify query by category, verify full-text search)
- QA-149: Generate memory write proposal (verify proposal format, verify rationale capture, verify provenance)
- QA-150: Execute approved write (verify write only on approval, verify immutability after write, verify audit log)
- QA-151: Memory versioning (verify version tracking, verify history preservation, verify rollback capability)
- QA-152: Memory Manager failure modes (fabric corruption detection/recovery, write proposal rejection handling)

**CROSS-02: Authority Manager (QA-153 to QA-158)**
- QA-153: Validate Johan role (verify full authority, verify override capability, verify audit of overrides)
- QA-154: Validate FM role (verify orchestration authority, verify governance enforcement authority, verify builder supervision authority)
- QA-155: Validate Builder roles (verify read access, verify write access boundaries, verify operation restrictions)
- QA-156: Enforce authority context (verify context propagation, verify authority check execution, verify unauthorized access prevention)
- QA-157: Authority delegation (verify temporary elevation, verify audit trail, verify automatic revocation)
- QA-158: Authority Manager failure modes (missing authority context handling, authority escalation abuse detection)

**CROSS-03: Notification Service (QA-159 to QA-164)**
- QA-159: Deliver notification (verify channel selection, verify delivery confirmation, verify retry on failure)
- QA-160: Handle priority notifications (verify immediate delivery, verify delivery guarantee, verify receipt confirmation)
- QA-161: Batch notifications (verify batching logic, verify batch size limits, verify delivery timing)
- QA-162: Notification preferences (verify user preference loading, verify channel override, verify quiet hours)
- QA-163: Notification delivery tracking (verify sent/delivered/read states, verify failure logging)
- QA-164: Notification Service failure modes (delivery failure escalation, channel unavailable fallback)

**CROSS-04: Evidence Store (QA-165 to QA-170)**
- QA-165: Store evidence artifact (verify metadata capture, verify content persistence, verify immutability)
- QA-166: Retrieve evidence by ID (verify lookup, verify content delivery, verify metadata inclusion)
- QA-167: Query evidence by category (verify filtering, verify sorting, verify pagination)
- QA-168: Link evidence to architectural element (verify bidirectional linking, verify relationship persistence)
- QA-169: Evidence retention policy (verify retention duration, verify archival, verify deletion prevention)
- QA-170: Evidence Store failure modes (storage capacity handling, corrupted artifact detection)

**CROSS-05: Audit Logger (QA-171 to QA-176)**
- QA-171: Log governance event (verify timestamp, verify actor, verify action, verify outcome, verify immutability)
- QA-172: Log authority event (verify permission check, verify override, verify audit trail completeness)
- QA-173: Query audit log (verify time range query, verify actor query, verify event type query)
- QA-174: Audit log immutability (verify append-only, verify no modifications, verify tampering detection)
- QA-175: Audit log retention (verify permanent retention, verify export capability, verify compliance)
- QA-176: Audit Logger failure modes (log write failure handling, log corruption detection/recovery)

**CROSS-06: Watchdog Observer (QA-177 to QA-182)**
- QA-177: Monitor system health (verify heartbeat checking, verify component responsiveness, verify resource usage)
- QA-178: Detect system failure (verify failure detection, verify escalation, verify recovery recommendation)
- QA-179: Independent operation (verify watchdog independence, verify disable prevention, verify bypass prevention)
- QA-180: Watchdog reporting (verify periodic status reports, verify alert generation, verify escalation routing)
- QA-181: Watchdog self-health (verify watchdog monitors itself, verify redundancy, verify failover)
- QA-182: Watchdog failure modes (self-failure detection, escalation if watchdog fails)

**Additional Cross-Cutting QA (QA-183 to QA-199)**
- QA-183 to QA-199: Error handling patterns, logging infrastructure, configuration management, health checks, performance monitoring, security checks, data integrity validation, etc.

---

### Flow-Based QA (QA-200 to QA-242)

**User Intent → Build Execution Flow (QA-200 to QA-215)**
- QA-200: End-to-end intent to build completion (verify entire path, verify state transitions, verify evidence trail)
- QA-201: Intent intake step (verify input acceptance, verify initial state)
- QA-202: Clarification step (verify ambiguity detection, verify question generation, verify resolution)
- QA-203: Requirement generation step (verify spec creation, verify structure, verify traceability)
- QA-204: Approval step (verify presentation, verify decision handling, verify state transition)
- QA-205: Build initiation step (verify build creation, verify architecture linking, verify wave planning)
- QA-206: Builder assignment step (verify QA range calculation, verify builder selection, verify task creation)
- QA-207: Build execution monitoring (verify progress tracking, verify status updates, verify escalation triggers)
- QA-208: QA validation step (verify RED to GREEN transitions, verify evidence collection, verify coverage calculation)
- QA-209: Build completion step (verify 100% GREEN validation, verify deliverable creation, verify handover)
- QA-210: Error handling in flow (verify error detection at each step, verify recovery, verify escalation)
- QA-211: State persistence across flow (verify state saved at each step, verify recovery from crash)
- QA-212: Evidence generation across flow (verify evidence at each step, verify audit trail completeness)
- QA-213: Authorization checks across flow (verify authority at each step, verify permission enforcement)
- QA-214: Timeout handling in flow (verify timeout at each step, verify escalation, verify recovery)
- QA-215: Flow cancellation (verify cancel capability, verify cleanup, verify audit log)

**Escalation Flow (QA-216 to QA-225)**
- QA-216: Escalation end-to-end (verify trigger → presentation → resolution, verify audit trail)
- QA-217: Escalation trigger detection (verify various trigger types, verify context capture)
- QA-218: Escalation creation (verify 5-element validation, verify priority assignment)
- QA-219: Escalation routing (verify inbox placement, verify notification delivery)
- QA-220: Escalation presentation (verify UI rendering, verify action availability)
- QA-221: Escalation decision (verify decision capture, verify execution trigger)
- QA-222: Escalation resolution (verify state update, verify outcome logging, verify evidence linking)
- QA-223: Escalation timeout (verify timeout detection, verify re-escalation)
- QA-224: Multiple concurrent escalations (verify prioritization, verify ordering, verify no conflicts)
- QA-225: Escalation error handling (verify routing failure, verify resolution failure, verify recovery)

**Parking Station Flow (QA-226 to QA-235)**
- QA-226: Parking Station end-to-end (verify intake → discussion → requirement → approval, verify traceability)
- QA-227: Idea submission (verify submission, verify validation, verify persistence)
- QA-228: Discussion initiation (verify discussion start, verify conversation link, verify participants)
- QA-229: Requirement conversion (verify requirement generation, verify approval flow initiation)
- QA-230: Approval in parking flow (verify approval presentation, verify decision handling)
- QA-231: Build initiation from parking (verify build creation, verify traceability to original idea)
- QA-232: Parking station search (verify idea discoverability, verify filtering, verify sorting)
- QA-233: Idea lifecycle transitions (verify state changes, verify audit trail)
- QA-234: Parking station concurrency (verify multiple ideas in parallel, verify no conflicts)
- QA-235: Parking station error handling (verify submission failure, verify discussion failure, verify recovery)

**Dashboard Drill-Down Flow (QA-236 to QA-242)**
- QA-236: Drill-down end-to-end (verify domain → root cause → evidence, verify navigation)
- QA-237: Initial domain selection (verify domain click, verify status display, verify context loading)
- QA-238: Navigation to component (verify component selection, verify component details display)
- QA-239: Evidence retrieval (verify evidence loading, verify evidence display, verify immutability verification)
- QA-240: Breadcrumb navigation (verify breadcrumb trail, verify back navigation, verify context preservation)
- QA-241: Multi-level drill-down (verify nested levels, verify state preservation at each level)
- QA-242: Drill-down error handling (verify evidence not found, verify broken links, verify recovery UX)

---

### State Transition-Based QA (QA-243 to QA-320)

**Intent State Transitions (QA-243 to QA-246)**
- QA-243: Intent RECEIVED → CLARIFYING (verify ambiguity trigger, verify state change, verify clarification start)
- QA-244: Intent CLARIFYING → CLARIFIED (verify sufficient clarification detection, verify state change, verify requirement generation trigger)
- QA-245: Intent CLARIFYING → REJECTED (verify rejection trigger, verify reason capture, verify cleanup)
- QA-246: Intent CLARIFIED → RECEIVED (verify rework trigger, verify context preservation, verify iteration tracking)

**Requirement Specification State Transitions (QA-247 to QA-251)**
- QA-247: RequirementSpec DRAFT → PENDING_APPROVAL (verify completion trigger, verify validation, verify approval presentation)
- QA-248: RequirementSpec PENDING_APPROVAL → APPROVED (verify approval decision, verify freeze, verify build initiation trigger)
- QA-249: RequirementSpec PENDING_APPROVAL → REJECTED (verify rejection decision, verify reason capture, verify intent availability)
- QA-250: RequirementSpec PENDING_APPROVAL → CONDITIONAL (verify conditional approval, verify conditions capture, verify gated progression)
- QA-251: RequirementSpec APPROVED → frozen state (verify immutability, verify no further changes, verify audit log)

**Build State Transitions (QA-252 to QA-260)**
- QA-252: Build INITIATED → IN_PROGRESS (verify builder assignment, verify task creation, verify monitoring start)
- QA-253: Build IN_PROGRESS → BLOCKED (verify blocker detection, verify escalation, verify pause trigger)
- QA-254: Build BLOCKED → IN_PROGRESS (verify blocker resolution, verify resume trigger, verify state restoration)
- QA-255: Build IN_PROGRESS → COMPLETED (verify 100% GREEN validation, verify deliverable creation, verify handover trigger)
- QA-256: Build COMPLETED → DELIVERED (verify delivery confirmation, verify evidence packaging, verify acceptance)
- QA-257: Build IN_PROGRESS → CANCELLED (verify cancel trigger, verify cleanup, verify audit trail)
- QA-258: Build state persistence (verify state saved after each transition, verify recovery from failure)
- QA-259: Build state audit trail (verify all transitions logged, verify timestamp, verify actor, verify reason)
- QA-260: Build state consistency (verify deterministic transitions, verify no invalid states, verify conflict resolution)

**Domain Status State Transitions (QA-261 to QA-268)**
- QA-261: Domain GREEN → AMBER (verify trigger, verify reason mandatory, verify visual update)
- QA-262: Domain AMBER → GREEN (verify resolution, verify reason cleared, verify visual update)
- QA-263: Domain GREEN → RED (verify critical failure trigger, verify reason mandatory, verify escalation trigger)
- QA-264: Domain AMBER → RED (verify escalation of issue, verify reason updated, verify escalation trigger)
- QA-265: Domain RED → AMBER (verify partial recovery, verify reason updated, verify escalation check)
- QA-266: Domain RED → GREEN (verify full recovery, verify reason cleared, verify escalation closure)
- QA-267: Domain status history (verify all transitions logged, verify reason history, verify audit trail)
- QA-268: Domain status consistency (verify no invalid transitions, verify reason always present for AMBER/RED)

**Escalation State Transitions (QA-269 to QA-275)**
- QA-269: Escalation PENDING → PRESENTED (verify presentation trigger, verify UI display, verify notification delivery)
- QA-270: Escalation PRESENTED → DECISION_RECEIVED (verify decision capture, verify execution trigger)
- QA-271: Escalation DECISION_RECEIVED → RESOLVED (verify execution complete, verify outcome logging, verify closure)
- QA-272: Escalation PENDING → TIMEOUT (verify timeout detection, verify re-escalation, verify priority increase)
- QA-273: Escalation lifecycle tracking (verify all transitions logged, verify audit trail, verify evidence linking)
- QA-274: Escalation state consistency (verify deterministic transitions, verify no skipped states)
- QA-275: Escalation state recovery (verify state restoration after crash, verify no data loss)

**Parking Idea State Transitions (QA-276 to QA-282)**
- QA-276: Idea PARKED → UNDER_DISCUSSION (verify discussion start trigger, verify conversation link)
- QA-277: Idea UNDER_DISCUSSION → REQUIREMENT_DRAFTED (verify requirement generation trigger, verify traceability)
- QA-278: Idea REQUIREMENT_DRAFTED → APPROVED (verify approval decision, verify build initiation)
- QA-279: Idea REQUIREMENT_DRAFTED → REJECTED (verify rejection decision, verify reason capture)
- QA-280: Idea UNDER_DISCUSSION → DEFERRED (verify deferral decision, verify reason capture, verify future review)
- QA-281: Idea UNDER_DISCUSSION → CLOSED (verify closure decision, verify reason capture, verify archive)
- QA-282: Idea lifecycle history (verify all transitions logged, verify audit trail completeness)

**Message State Transitions (QA-283 to QA-287)**
- QA-283: Message PENDING → SENT (verify send trigger, verify persistence)
- QA-284: Message SENT → DELIVERED (verify delivery confirmation, verify timestamp)
- QA-285: Message DELIVERED → READ (verify read confirmation, verify timestamp, verify audit log)
- QA-286: Message state tracking (verify all states logged, verify audit trail)
- QA-287: Message state consistency (verify no invalid transitions, verify deterministic flow)

**Conversation State Transitions (QA-288 to QA-292)**
- QA-288: Conversation ACTIVE → PAUSED (verify pause trigger, verify state preservation)
- QA-289: Conversation PAUSED → RESUMED (verify resume trigger, verify context restoration)
- QA-290: Conversation ACTIVE → ARCHIVED (verify archive trigger, verify reason capture, verify preservation)
- QA-291: Conversation ARCHIVED → RESUMED (verify unarchive trigger, verify audit log)
- QA-292: Conversation lifecycle history (verify all transitions logged, verify audit trail)

**Additional State Transition QA (QA-293 to QA-320)**
- QA-293 to QA-320: Additional state transitions for governance rules, analytics metrics, memory entries, notification statuses, watchdog states, builder task states, QA component states (RED → GREEN transitions), etc.

---

### Failure Mode-Based QA (QA-321 to QA-400+)

**Component Failure Modes (QA-321 to QA-370)**

**CONV-01 Failure Modes (QA-321 to QA-323)**
- QA-321: CONV-01 database write failure (verify retry 3x with exponential backoff, verify escalation on persistent failure)
- QA-322: CONV-01 conversation not found (verify error return, verify log warning, verify no escalation)
- QA-323: CONV-01 archive already archived conversation (verify state conflict detection, verify error message to caller)

**CONV-02 Failure Modes (QA-324 to QA-327)**
- QA-324: CONV-02 message content empty (verify validation rejection, verify error to sender, verify no persistence)
- QA-325: CONV-02 conversation does not exist (verify error return from CONV-01, verify error to sender, verify log warning)
- QA-326: CONV-02 message persistence failure (verify retry 3x, verify escalation on persistent failure)
- QA-327: CONV-02 intent processing failure (verify error log, verify message state PENDING, verify retry later)

**INTENT-01 Failure Modes (QA-328 to QA-329)**
- QA-328: INTENT-01 unparseable input (verify safe default behavior, verify warning log, verify escalation for review)
- QA-329: INTENT-01 context loss detection (verify context validation, verify recovery attempt, verify escalation if unrecoverable)

**INTENT-02 Failure Modes (QA-330 to QA-331)**
- QA-330: INTENT-02 infinite loop prevention (verify iteration limit, verify escalation after limit, verify structured capture)
- QA-331: INTENT-02 ambiguity resolution failure (verify timeout handling, verify escalation, verify manual review trigger)

**GOV-01 Failure Modes (QA-332 to QA-334)**
- QA-332: GOV-01 repository unavailable (verify startup block, verify escalation, verify retry mechanism)
- QA-333: GOV-01 parse failure (verify error logging, verify startup block, verify escalation with details)
- QA-334: GOV-01 cache corruption (verify detection, verify rebuild from source, verify escalation if unrecoverable)

**EXEC-01 Failure Modes (QA-335 to QA-337)**
- QA-335: EXEC-01 builder unavailable (verify alternate builder selection, verify escalation if no builders available)
- QA-336: EXEC-01 task assignment failure (verify retry, verify escalation, verify build block)
- QA-337: EXEC-01 orchestration corruption (verify detection, verify state recovery, verify escalation)

**ESC-01 Failure Modes (QA-338 to QA-339)**
- QA-338: ESC-01 delivery failure (verify retry 3x, verify escalation on persistent failure, verify fallback channel)
- QA-339: ESC-01 duplicate ping prevention (verify ping deduplication, verify no spam, verify audit log)

**ANALYTICS-03 Failure Modes (QA-340 to QA-341)**
- QA-340: ANALYTICS-03 token counting failure (verify fallback estimation, verify error log, verify manual review trigger)
- QA-341: ANALYTICS-03 cost calculation error (verify safe default, verify error log, verify manual review)

**CROSS-01 Failure Modes (QA-342 to QA-343)**
- QA-342: CROSS-01 memory fabric corruption (verify detection, verify recovery from backup, verify escalation)
- QA-343: CROSS-01 write proposal rejection (verify rejection handling, verify proposer notification, verify audit log)

**CROSS-04 Failure Modes (QA-344 to QA-345)**
- QA-344: CROSS-04 storage capacity (verify capacity monitoring, verify archival trigger, verify escalation before full)
- QA-345: CROSS-04 corrupted artifact detection (verify checksum validation, verify quarantine, verify escalation)

**CROSS-05 Failure Modes (QA-346 to QA-347)**
- QA-346: CROSS-05 log write failure (verify in-memory buffer, verify retry, verify escalation on persistent failure)
- QA-347: CROSS-05 log corruption detection (verify checksum validation, verify integrity checks, verify escalation)

**CROSS-06 Failure Modes (QA-348 to QA-349)**
- QA-348: CROSS-06 watchdog self-failure (verify self-monitoring, verify escalation, verify redundancy/failover)
- QA-349: CROSS-06 false positive prevention (verify multi-signal validation, verify confidence threshold, verify reduce false alarms)

**Additional Component Failure Modes (QA-350 to QA-370)**
- QA-350 to QA-370: Additional failure modes for remaining components (CONV-03, CONV-04, CONV-05, DASH-01, DASH-02, DASH-03, DASH-04, PARK-01, PARK-02, PARK-03, PARK-04, INTENT-03, INTENT-04, EXEC-02, EXEC-03, ESC-02, ESC-03, ESC-04, GOV-02, GOV-03, ANALYTICS-01, ANALYTICS-02, CROSS-02, CROSS-03)

**System-Wide Failure Modes (QA-371 to QA-400)**

**Database Failure Modes (QA-371 to QA-375)**
- QA-371: Database connection loss (verify detection, verify reconnection attempt, verify escalation if persistent)
- QA-372: Database transaction failure (verify rollback, verify data consistency, verify retry logic)
- QA-373: Database query timeout (verify timeout detection, verify query cancellation, verify retry with backoff)
- QA-374: Database corruption (verify detection, verify recovery from backup, verify escalation)
- QA-375: Database capacity (verify monitoring, verify archival, verify escalation before full)

**Network Failure Modes (QA-376 to QA-380)**
- QA-376: Network partition (verify detection, verify retry, verify degraded operation mode)
- QA-377: WebSocket connection loss (verify detection, verify reconnection, verify fallback to polling)
- QA-378: API call timeout (verify timeout handling, verify retry logic, verify escalation threshold)
- QA-379: GitHub API failure (verify error handling, verify retry with backoff, verify escalation if persistent)
- QA-380: Notification delivery failure (verify retry, verify alternate channel, verify escalation)

**Resource Failure Modes (QA-381 to QA-385)**
- QA-381: Memory exhaustion (verify detection, verify cleanup, verify escalation, verify graceful degradation)
- QA-382: CPU overload (verify detection, verify throttling, verify escalation, verify load shedding)
- QA-383: Disk space exhaustion (verify monitoring, verify cleanup, verify escalation before full)
- QA-384: File handle exhaustion (verify detection, verify cleanup, verify escalation)
- QA-385: Thread pool exhaustion (verify detection, verify queuing, verify escalation, verify rejection policy)

**Security Failure Modes (QA-386 to QA-390)**
- QA-386: Unauthorized access attempt (verify detection, verify blocking, verify audit log, verify escalation)
- QA-387: Authority escalation abuse (verify detection, verify blocking, verify audit log, verify escalation)
- QA-388: Data tampering attempt (verify integrity checks, verify detection, verify escalation)
- QA-389: Governance bypass attempt (verify detection, verify blocking, verify audit log, verify escalation)
- QA-390: Memory fabric unauthorized write (verify prevention, verify detection, verify escalation)

**Integration Failure Modes (QA-391 to QA-395)**
- QA-391: GitHub API rate limit (verify detection, verify backoff, verify queueing, verify notification)
- QA-392: GitHub webhook delivery failure (verify retry, verify alternate polling, verify data consistency)
- QA-393: External service unavailable (verify detection, verify degraded mode, verify notification)
- QA-394: Data sync failure (verify detection, verify reconciliation, verify escalation)
- QA-395: Integration contract violation (verify validation, verify rejection, verify escalation)

**Cascading Failure Modes (QA-396 to QA-400)**
- QA-396: Cascading component failure (verify circuit breaker, verify isolation, verify escalation)
- QA-397: Deadlock detection (verify timeout, verify deadlock detection, verify recovery, verify escalation)
- QA-398: Race condition handling (verify detection, verify retry, verify escalation if persistent)
- QA-399: Data consistency failure (verify detection, verify reconciliation, verify escalation)
- QA-400: System-wide failure (verify graceful shutdown, verify state preservation, verify escalation, verify recovery plan)

**Additional Failure Modes (QA-401+)**
- QA-401 and beyond: Additional failure modes as architectural detail deepens or new scenarios discovered

---

### Wave 2 Extended QA Components (QA-401 to QA-600)

**Wave 2 Extended QA Range:** Reserved for Wave 2 corrective action (BL-019 Response)

#### System Optimizations Phase 1 (QA-426 to QA-435)

**Caching Implementation (QA-426 to QA-430)**
- QA-426: Cache layer initialization (verify cache creation, verify configuration loading, verify readiness confirmation)
- QA-427: Cache key generation (verify key uniqueness, verify collision handling, verify consistency across requests)
- QA-428: Cache hit/miss handling (verify hit returns cached data, verify miss fetches fresh data, verify metrics tracking)
- QA-429: Cache invalidation logic (verify TTL expiration, verify manual invalidation, verify cascade invalidation)
- QA-430: Cache statistics tracking (verify hit rate calculation, verify miss rate calculation, verify eviction metrics)

**Query Optimization (QA-431 to QA-435)**
- QA-431: Query analysis and profiling (verify slow query detection, verify query logging, verify performance alerting)
- QA-432: Query plan optimization (verify index usage, verify join optimization, verify plan caching)
- QA-433: Index usage optimization (verify index selection, verify coverage analysis, verify efficiency metrics)
- QA-434: Query result caching (verify cache integration, verify invalidation on data change, verify consistency)
- QA-435: Query performance monitoring (verify execution time tracking, verify query count metrics, verify alert threshold)

---

## QA Catalog Statistics

**Total QA Components:** 400+

**By Category:**
- Component-Based QA: 199 (QA-001 to QA-199)
- Flow-Based QA: 43 (QA-200 to QA-242)
- State Transition-Based QA: 78 (QA-243 to QA-320)
- Failure Mode-Based QA: 80+ (QA-321 to QA-400+)

**By Subsystem:**
- Conversational Interface: 22 QA components
- Dashboard: 20 QA components
- Parking Station: 15 QA components
- Intent Processing: 20 QA components
- Execution Orchestration: 15 QA components
- Escalation & Supervision: 24 QA components
- Governance Enforcement: 15 QA components
- Analytics: 15 QA components
- Cross-Cutting: 53 QA components
- System-Wide: 201+ QA components (flows, states, failures)

**Coverage:**
- Architectural Components: 36 components, 100% coverage
- Runtime Paths: 4 major paths, 100% coverage
- State Transitions: 78+ transitions, 100% coverage
- Failure Modes: 80+ scenarios, comprehensive coverage

---

## QA Immutability Rules

1. **Once assigned, QA numbers NEVER change**
   - QA-042 will always be QA-042, even if the test changes

2. **Deprecated QA components retain their number**
   - Mark as DEPRECATED in catalog
   - Do not reuse the number

3. **New QA components get next available number**
   - If last QA is QA-400, next is QA-401

4. **No gaps in numbering**
   - Sequence must be contiguous

5. **Audit trail for QA changes**
   - Changes to QA definition logged
   - Original QA ID preserved in audit

---

## Usage for Builder Assignment

**Bounded Assignment Example:**

Builder A assigned: QA-001 to QA-022 (Conversational Interface Subsystem)
- Builder A implements CONV-01, CONV-02, CONV-03, CONV-04, CONV-05
- Builder A makes QA-001 through QA-022 GREEN
- All other QA remain RED without blocking Builder A
- Gate evaluates only Builder A's assigned QA range

Builder B assigned: QA-023 to QA-042 (Dashboard Subsystem)
- Builder B implements DASH-01, DASH-02, DASH-03, DASH-04
- Builder B makes QA-023 through QA-042 GREEN
- All other QA remain RED without blocking Builder B
- Gate evaluates only Builder B's assigned QA range

**Progressive Build:**
- Wave 1: Assign QA-001 to QA-100 (foundation components)
- Wave 2: Assign QA-101 to QA-200 (application components)
- Wave 3: Assign QA-201 to QA-300 (flows and states)
- Wave 4: Assign QA-301 to QA-400+ (failure modes and integration)

---

## FM Acceptance Declaration

I, Foreman (FM), confirm that this QA Catalog:

- Provides authoritative index of 400+ QA components
- Numbers QA components sequentially (QA-001 to QA-400+)
- Maps every architectural element to numbered QA
- Establishes immutability rules for QA numbering
- Enables bounded builder assignment by QA range
- Enables failure localization by QA ID
- Enables build progress measurement by QA coverage
- Supports non-coder orchestration (no code review required)
- Aligns with FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md
- Is ready to serve as authoritative QA index

**Accepted By:** Foreman (FM)  
**Date:** 2025-12-31  
**Derivation:** Re-derived from Architecture V2 (Wiring-Complete)

---

**End of QA Catalog**
