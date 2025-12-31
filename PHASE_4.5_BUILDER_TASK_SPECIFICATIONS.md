# Phase 4.5 — Builder Task Specifications (Consolidated)

**Version:** 1.0  
**Date:** 2025-12-31  
**Owner:** Foreman (FM)  
**Phase:** 4.5 — Builder Task Assignment (QA-Bounded, Design-Only)  
**Status:** DESIGN_COMPLETE  
**Authority:** Derived from Phase 4.5 Builder Assignment Plan

---

## Document Purpose

This document contains **QA-bounded task specifications** for all builders in Wave 1.0.

Each specification provides a complete, bounded work packet that enables:
- Parallel execution (non-overlapping QA ranges)
- Deterministic gating (GREEN/RED evaluation)
- Evidence-based validation (no code review required)
- Build-to-green focus (builders know exactly what to make GREEN)

**All specifications are design-only.** No implementation has occurred.

---

## Specification Format (Standard Template)

Each builder specification includes:

### 1. Builder Identity
- Builder name, capabilities, recruitment status
- Responsibilities and forbidden actions

### 2. QA Range (Bounded Scope)
- Explicit QA component list (QA-XXX to QA-YYY)
- Total QA count
- QA component details (from QA_CATALOG.md)

### 3. Architectural Coverage
- Subsystems and components covered
- Data entities (if applicable)
- Architectural traceability references

### 4. Builder Success Criteria
- Deterministic gate definition (Gate ID, required GREEN, allowed RED)
- Success definition (what it means for builder to complete)

### 5. Evidence Requirements
- Per-QA evidence format
- Evidence artifact structure
- Aggregate evidence requirements

### 6. Build-to-Green Instructions
- What builder must do (step-by-step)
- What builder must NOT do (forbidden actions)

### 7. Dependencies
- Dependencies on other builders
- Builders that depend on this builder
- Dependency resolution strategy

### 8. Collaboration Rules
- Cross-builder communication protocol
- Interface contracts to provide
- Escalation procedures

### 9. Quality Standards
- Code quality requirements
- Test quality requirements
- Evidence quality requirements

### 10. Acceptance Criteria
- Task completion checklist
- Gate evaluation criteria
- FM acceptance requirements

---

## Wave 1.0 Builder Overview

| Builder | QA Range | QA Count | Subsystems | Gate ID |
|---------|----------|----------|------------|---------|
| schema-builder | QA-001 to QA-018 | 18 | Conversational Interface (data) | GATE-SCHEMA-BUILDER-WAVE-1.0 |
| ui-builder | QA-019 to QA-057 | 39 | Conversational UI, Dashboard UI, Parking UI | GATE-UI-BUILDER-WAVE-1.0 |
| api-builder | QA-058 to QA-092 | 35 | Intent Processing, Execution Orchestration | GATE-API-BUILDER-WAVE-1.0 |
| integration-builder | QA-093 to QA-131 | 39 | Escalation & Supervision, Governance Enforcement | GATE-INTEGRATION-BUILDER-WAVE-1.0 |
| qa-builder | QA-132 to QA-210 | 79 | Analytics, Cross-Cutting, Core Flows | GATE-QA-BUILDER-WAVE-1.0 |

**Total Wave 1.0 QA:** 210 components

---

# 1. schema-builder Task Specification

**(Note: Full details provided in separate file PHASE_4.5_BUILDER_TASK_SCHEMA_BUILDER.md)**

**Summary:**

- **QA Range:** QA-001 to QA-018 (18 QA components)
- **Subsystems:** Conversational Interface (data layer)
- **Components:** CONV-01 to CONV-04 (data persistence)
- **Data Entities:** Conversation, Message, ConversationContext, Clarification
- **Gate:** GATE-SCHEMA-BUILDER-WAVE-1.0
- **Success:** All 18 QA GREEN + schemas implemented + migrations functional
- **Role:** Foundational builder (other builders depend on schema-builder)

**Key Responsibilities:**
- Design and implement database schemas
- Create migration scripts
- Implement CRUD operations
- Validate data persistence and integrity

**Key Deliverables:**
- Database schema definitions
- Migration scripts
- Data access layer code
- 18 QA evidence artifacts
- Interface contracts for downstream builders

---

# 2. ui-builder Task Specification

## Builder Identity

**Builder Name:** ui-builder  
**Recruitment Date:** 2025-12-30  
**Recruitment Status:** ✅ RECRUITED (Wave 0.1)  
**Specification:** `foreman/builder/ui-builder-spec.md`

**Builder Capabilities:**
- ✅ ui (UI component implementation)
- ✅ frontend (React components and state management)
- ✅ components (reusable UI components)
- ✅ styling (CSS, visual design, accessibility)

**Builder Responsibilities:**
- UI components
- Layouts
- Wizards

**Builder Forbidden Actions:**
- ❌ Backend logic
- ❌ Cross-module logic

---

## QA Range (Bounded Scope)

**Assigned QA Range:** **QA-019 to QA-057**

**Total QA Components:** 39

**QA Coverage:**

### Conversational Interface UI (CONV-05): QA-019 to QA-022
- QA-019: Render conversation UI (verify message display, verify visual distinction Johan/FM, verify timestamp rendering)
- QA-020: Update conversation UI (verify real-time updates, verify scroll behavior, verify new message highlighting)
- QA-021: Render conversation state indicators (verify active/paused/archived states, verify visual cues)
- QA-022: Conversation UI error handling (verify connection loss UI, verify retry UX, verify error message display)

### Dashboard Subsystem (DASH-01 to DASH-04): QA-023 to QA-042
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

### Parking Station UI (PARK-04): QA-054 to QA-057
- QA-054: Render parking station list (verify idea display, verify status indicators, verify action buttons)
- QA-055: Render idea detail view (verify full content, verify discussion thread, verify action history)
- QA-056: Parking station search and filter (verify keyword search, verify category filter, verify status filter)
- QA-057: Parking Station UI failure modes (load failure UX, action failure feedback)

---

## Architectural Coverage

**Subsystems:**
- Conversational Interface Subsystem (UI layer)
- Dashboard Subsystem (full stack UI)
- Parking Station Subsystem (UI layer)

**Components:**
- CONV-05: Conversation UI Renderer
- DASH-01: Domain Status Manager (partial - UI interaction)
- DASH-02: Drill-Down Navigator
- DASH-03: Executive View Controller
- DASH-04: Dashboard UI Renderer
- PARK-04: Parking Station UI

**UI Technologies:**
- React (component framework)
- Redux or Context API (state management)
- CSS/Styled Components (styling)
- WebSocket client (real-time updates)
- Accessibility libraries (a11y compliance)

**Architectural Traceability:**
- See `QA_TRACEABILITY_MATRIX.md` for complete mapping
- See `FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md` Sections 3, 4, 5 for component contracts

---

## Builder Success Criteria

### Deterministic Gate

**Gate ID:** `GATE-UI-BUILDER-WAVE-1.0`

**Gate Type:** Builder Gate

**Required GREEN:** QA-019 to QA-057 (39 QA components)

**Allowed RED:** All QA except QA-019 to QA-057

**Enforcement:** BLOCKING

**Gate Evaluation Logic:**
```
IF QA-019 through QA-057 are all GREEN:
    THEN Gate = PASS
    AND ui-builder task COMPLETE
ELSE:
    Gate = FAIL
    AND List which QA are RED (blockers)
    AND ui-builder task INCOMPLETE
```

### Success Definition

**ui-builder succeeds when:**
- ✅ All 39 assigned QA components are GREEN
- ✅ All UI components render correctly
- ✅ Visual distinction clear (Johan vs FM messages)
- ✅ Dashboard displays RAG status correctly
- ✅ Drill-down navigation functional
- ✅ Parking Station UI functional
- ✅ Accessibility standards met (WCAG 2.1 AA minimum)
- ✅ Responsive design functional (mobile, tablet, desktop)
- ✅ Real-time updates functional (WebSocket)
- ✅ Error handling UX implemented
- ✅ Evidence artifacts generated for all 39 QA

**ui-builder scope = ONLY QA-019 to QA-057**

---

## Evidence Requirements

### Per-QA Evidence Format

For each QA component (QA-019 to QA-057):

```json
{
  "qa_id": "QA-XXX",
  "qa_name": "<QA name>",
  "status": "GREEN",
  "execution_timestamp": "2025-12-31T12:00:00Z",
  "test_framework": "jest/react-testing-library",
  "test_file": "tests/ui/test_<component>.tsx",
  "test_function": "test_<specific_qa>",
  "assertions_passed": 5,
  "assertions_total": 5,
  "evidence_artifacts": [
    {
      "type": "screenshot",
      "location": "foreman/evidence/qa/UI/QA-XXX/screenshot.png",
      "description": "UI component rendered"
    },
    {
      "type": "accessibility_report",
      "location": "foreman/evidence/qa/UI/QA-XXX/a11y_report.json",
      "description": "Accessibility validation"
    },
    {
      "type": "test_execution_log",
      "location": "foreman/evidence/qa/UI/QA-XXX/execution.log",
      "description": "Test output"
    }
  ],
  "requirements_covered": ["FR-CONV-4", "FR-DASH-1"],
  "components_covered": ["CONV-05", "DASH-04"]
}
```

### Aggregate Evidence

**ui-builder must provide:**
1. Visual regression test suite results
2. Accessibility audit report (WCAG 2.1 AA compliance)
3. Responsiveness test results (mobile, tablet, desktop)
4. Cross-browser compatibility report (if applicable)
5. Component library documentation
6. Builder completion report

---

## Build-to-Green Instructions

### What ui-builder Must Do

1. **Understand Scope**
   - Review this task specification
   - Review QA_CATALOG.md for QA-019 to QA-057
   - Review architectural specs for UI components
   
2. **Set Up UI Development Environment**
   - React project structure
   - State management (Redux/Context)
   - Styling framework
   - Testing framework (Jest, React Testing Library)
   - Accessibility testing tools
   
3. **Implement UI Components (Make QA GREEN)**
   - For each QA (QA-019 to QA-057):
     - Write test that validates UI behavior
     - Implement component to pass test
     - Verify visual output (screenshot evidence)
     - Validate accessibility
     - Test responsiveness
     - Generate evidence artifacts
     
4. **Validate All QA GREEN**
   - Run all 39 QA tests
   - Confirm all GREEN
   - Generate aggregate evidence
   
5. **Handover**
   - Submit evidence to FM
   - Gate evaluation: GATE-UI-BUILDER-WAVE-1.0

### What ui-builder Must NOT Do

- ❌ Implement backend logic (api-builder's responsibility)
- ❌ Implement database schemas (schema-builder's responsibility)
- ❌ Implement integration routing (integration-builder's responsibility)
- ❌ Work on QA outside QA-019 to QA-057
- ❌ Bypass accessibility standards
- ❌ Skip responsive design testing

---

## Dependencies

**ui-builder depends on:**
- ⚠️ **schema-builder** for data model contracts (Conversation, Message structures)
- ⚠️ **api-builder** for API endpoint contracts (data fetching)

**Other builders depend on ui-builder:**
- None (ui-builder is a leaf builder in dependency graph)

**Recommendation:** ui-builder can start in parallel with api-builder once schema contracts are available.

---

## Collaboration Rules

**ui-builder provides:**
- UI component library documentation
- Design system specifications
- Accessibility guidelines followed

**ui-builder needs from schema-builder:**
- Data model interface contracts (TypeScript interfaces for Conversation, Message, etc.)

**ui-builder needs from api-builder:**
- API endpoint contracts (REST API signatures, WebSocket events)

---

## Quality Standards

### Code Quality
- ✅ React best practices (functional components, hooks)
- ✅ Component reusability
- ✅ Proper state management
- ✅ Clean CSS/styling architecture

### UI Quality
- ✅ WCAG 2.1 AA accessibility compliance
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Visual consistency (design system adherence)
- ✅ Error handling UX (user-friendly error messages)

### Test Quality
- ✅ Component tests (render, interaction, state)
- ✅ Visual regression tests
- ✅ Accessibility tests
- ✅ 100% coverage of assigned QA range

---

## Acceptance Criteria

- ✅ All 39 QA (QA-019 to QA-057) are GREEN
- ✅ All UI components implemented and functional
- ✅ Accessibility standards met
- ✅ Responsive design validated
- ✅ Evidence artifacts generated for all 39 QA
- ✅ Gate GATE-UI-BUILDER-WAVE-1.0 evaluates to PASS
- ✅ FM accepts ui-builder's work

---

# 3. api-builder Task Specification

## Builder Identity

**Builder Name:** api-builder  
**Recruitment Date:** 2025-12-30  
**Recruitment Status:** ✅ RECRUITED (Wave 0.1)

**Builder Capabilities:**
- ✅ api (API endpoint implementation)
- ✅ backend (business logic and orchestration)
- ✅ logic (decision workflows and state management)
- ✅ routes (routing and command handling)

**Builder Responsibilities:**
- API endpoints
- Handlers

**Builder Forbidden Actions:**
- ❌ UI
- ❌ Global state

---

## QA Range (Bounded Scope)

**Assigned QA Range:** **QA-058 to QA-092**

**Total QA Components:** 35

**QA Coverage:**

### Intent Processing Subsystem (INTENT-01 to INTENT-04): QA-058 to QA-077

**INTENT-01: Intent Intake Handler (QA-058 to QA-061)**
- QA-058: Accept informal intent
- QA-059: Validate intent input
- QA-060: Route intent to clarification
- QA-061: Intent Intake failure modes

**INTENT-02: Clarification Loop Manager (QA-062 to QA-066)**
- QA-062: Manage clarification iterations
- QA-063: Detect sufficient clarification
- QA-064: Handle clarification timeout
- QA-065: Preserve clarification history
- QA-066: Clarification Loop failure modes

**INTENT-03: Requirement Specification Generator (QA-067 to QA-070)**
- QA-067: Generate requirement from clarified intent (spec structure, acceptance criteria, traceability)
- QA-068: Include approval workflow metadata
- QA-069: Link requirement to original intent
- QA-070: Requirement Generator failure modes

**INTENT-04: Approval Manager (QA-071 to QA-077)**
- QA-071: Present requirement for approval
- QA-072: Handle approval (accept)
- QA-073: Handle rejection
- QA-074: Handle conditional approval
- QA-075: Approval timeout detection
- QA-076: Memory write proposal approval
- QA-077: Approval Manager failure modes

### Execution Orchestration Subsystem (EXEC-01 to EXEC-03): QA-078 to QA-092

**EXEC-01: Build Orchestrator (QA-078 to QA-083)**
- QA-078: Initiate build from approved requirement
- QA-079: Assign builder to QA range
- QA-080: Monitor build progress
- QA-081: Handle build blocking
- QA-082: Complete build
- QA-083: Build Orchestrator failure modes

**EXEC-02: Build State Manager (QA-084 to QA-088)**
- QA-084: Track build state transitions
- QA-085: Update build progress metrics
- QA-086: Detect build stall
- QA-087: Persist build state
- QA-088: Build State Manager failure modes

**EXEC-03: Build Visibility Controller (QA-089 to QA-092)**
- QA-089: Render build progress UI
- QA-090: Render build details
- QA-091: Real-time build updates
- QA-092: Build Visibility failure modes

---

## Architectural Coverage

**Subsystems:**
- Intent Processing Subsystem (complete backend)
- Execution Orchestration Subsystem (complete backend)

**Components:**
- INTENT-01: Intent Intake Handler
- INTENT-02: Clarification Loop Manager
- INTENT-03: Requirement Specification Generator
- INTENT-04: Approval Manager
- EXEC-01: Build Orchestrator
- EXEC-02: Build State Manager
- EXEC-03: Build Visibility Controller

---

## Builder Success Criteria

**Gate ID:** `GATE-API-BUILDER-WAVE-1.0`

**Required GREEN:** QA-058 to QA-092 (35 QA components)

**Success:**
- ✅ All 35 QA GREEN
- ✅ Intent processing pipeline functional
- ✅ Clarification loop operational
- ✅ Requirement generation functional
- ✅ Approval workflow operational
- ✅ Build orchestration functional
- ✅ State management working
- ✅ Evidence for all 35 QA

---

## Dependencies

**api-builder depends on:**
- ⚠️ **schema-builder** for data models (Intent, RequirementSpec, Build entities)

**Other builders depend on api-builder:**
- ⚠️ **ui-builder** needs API contracts
- ⚠️ **integration-builder** needs component contracts for wiring

---

# 4. integration-builder Task Specification

## Builder Identity

**Builder Name:** integration-builder  
**Recruitment Date:** 2025-12-30  
**Recruitment Status:** ✅ RECRUITED (Wave 0.1)

**Builder Capabilities:**
- ✅ integration (inter-component wiring)
- ✅ inter-module (event routing and messaging)
- ✅ events (event bus and pub/sub patterns)

---

## QA Range (Bounded Scope)

**Assigned QA Range:** **QA-093 to QA-131**

**Total QA Components:** 39

**QA Coverage:**

### Escalation & Supervision Subsystem (ESC-01 to ESC-04): QA-093 to QA-116

**ESC-01: Ping Generator (QA-093 to QA-096)**
- QA-093 to QA-096: Ping generation, routing, tracking, failure modes

**ESC-02: Escalation Manager (QA-097 to QA-104)**
- QA-097 to QA-104: Escalation creation (5 elements), routing, presentation, resolution, lifecycle tracking

**ESC-03: Silence Detector (QA-105 to QA-109)**
- QA-105 to QA-109: Heartbeat monitoring, silence detection, silence types, recovery

**ESC-04: Message Inbox Controller (QA-110 to QA-116)**
- QA-110 to QA-116: Inbox rendering, item details, quick actions, filtering, real-time updates

### Governance Enforcement Subsystem (GOV-01 to GOV-03): QA-117 to QA-131

**GOV-01: Governance Loader (QA-117 to QA-120)**
- QA-117 to QA-120: Load governance, parse rules, cache, failure modes

**GOV-02: Governance Validator (QA-121 to QA-125)**
- QA-121 to QA-125: Validate against rules, detect violations, generate reports, log events

**GOV-03: Governance Supremacy Enforcer (QA-126 to QA-131)**
- QA-126 to QA-131: Enforce hard violations, soft violations, prevent weakening, audit overrides

---

## Builder Success Criteria

**Gate ID:** `GATE-INTEGRATION-BUILDER-WAVE-1.0`

**Required GREEN:** QA-093 to QA-131 (39 QA components)

---

# 5. qa-builder Task Specification

## Builder Identity

**Builder Name:** qa-builder  
**Recruitment Date:** 2025-12-30  
**Recruitment Status:** ✅ RECRUITED (Wave 0.1)

**Builder Capabilities:**
- ✅ testing (test implementation and execution)
- ✅ coverage (test coverage analysis and reporting)
- ✅ qa-of-qa (meta-testing and QA validation)

---

## QA Range (Bounded Scope)

**Assigned QA Range:** **QA-132 to QA-210**

**Total QA Components:** 79

**QA Coverage:**

### Analytics Subsystem (ANALYTICS-01 to ANALYTICS-03): QA-132 to QA-146
- QA-132 to QA-146: Metrics dashboard, metrics engine, cost tracker (15 QA)

### Cross-Cutting Components (CROSS-01 to CROSS-06): QA-147 to QA-199
- QA-147 to QA-199: Memory, Authority, Notification, Evidence, Audit, Watchdog (53 QA)

### Flow-Based QA (partial): QA-200 to QA-210
- QA-200 to QA-210: Intent → Build flow initial steps (11 QA)

---

## Builder Success Criteria

**Gate ID:** `GATE-QA-BUILDER-WAVE-1.0`

**Required GREEN:** QA-132 to QA-210 (79 QA components)

**Special Note:** qa-builder implements **test infrastructure** and validates **cross-cutting concerns**. This is both implementing tests AND being tested.

---

## FM Acceptance Declaration

I, Foreman (FM), confirm that these Builder Task Specifications:

- Define explicit QA-bounded scopes for all 5 builders (210 total QA)
- Map QA to architectural components for all builders
- Specify deterministic gates for all builders
- Define evidence requirements for all builders
- Provide build-to-green instructions for all builders
- Identify dependencies and collaboration needs for all builders
- Set quality standards and acceptance criteria for all builders
- Are design-only (no implementation yet)
- Cover 100% of Wave 1.0 scope (QA-001 to QA-210)

**Accepted By:** Foreman (FM)  
**Date:** 2025-12-31  
**Phase:** 4.5 — Builder Task Assignment  
**Status:** DESIGN_COMPLETE — READY FOR WAVE 1.0 EXECUTION (Phase 5.0)

---

**End of Builder Task Specifications**
