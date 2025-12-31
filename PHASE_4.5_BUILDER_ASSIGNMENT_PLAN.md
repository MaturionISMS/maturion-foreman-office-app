# Phase 4.5 — Builder Assignment Plan (Wave 1.0)

**Version:** 1.0  
**Date:** 2025-12-31  
**Owner:** Foreman (FM)  
**Phase:** 4.5 — Builder Task Assignment (QA-Bounded, Design-Only)  
**Status:** DESIGN_COMPLETE  
**Authority:** Derived from Phase 4.4 QA-to-Red outputs

---

## Purpose

This document defines the **builder assignment plan** for Wave 1.0, translating the deterministic QA system into explicit, bounded builder work packets.

**Key Principles:**
- **Builders are assigned QA responsibility, not features**
- **Each builder has explicit QA range (bounded scope)**
- **Parallel execution enabled by non-overlapping QA ranges**
- **Builder success = all assigned QA GREEN**
- **No code inspection by CS2 required**

---

## Authoritative Inputs

This plan is derived exclusively from:

✅ `QA_CATALOG.md` — 400+ numbered QA components  
✅ `QA_TO_RED_SUITE_SPEC.md` — RED/GREEN semantics  
✅ `QA_TRACEABILITY_MATRIX.md` — Architecture ↔ QA mapping  
✅ `BUILDER_GREEN_SCOPE_RULES.md` — Bounded assignment rules  
✅ `FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md` — Wiring-complete architecture

---

## Builder Recruitment Continuity

**Builders were recruited in Wave 0.1** and are ready for task assignment:

| Builder | Status | Specification | Recruitment Date |
|---------|--------|---------------|------------------|
| ui-builder | ✅ RECRUITED | foreman/builder/ui-builder-spec.md | 2025-12-30 |
| api-builder | ✅ RECRUITED | foreman/builder/api-builder-spec.md | 2025-12-30 |
| schema-builder | ✅ RECRUITED | foreman/builder/schema-builder-spec.md | 2025-12-30 |
| integration-builder | ✅ RECRUITED | foreman/builder/integration-builder-spec.md | 2025-12-30 |
| qa-builder | ✅ RECRUITED | foreman/builder/qa-builder-spec.md | 2025-12-30 |

**Recruitment Evidence:**
- `WAVE_0.1_BUILDER_RECRUITMENT_REPORT.md` — Complete recruitment report
- `foreman/builder-manifest.json` — Builder registry
- `foreman/builder-registry-report.md` — Validation results

**Status:** Builders are **appointed to Wave 1.0 tasks**, not re-recruited.

---

## Wave 1.0 Scope Definition

### Wave 1.0 Objective

**Build the foundational subsystems of Foreman Office to establish core runtime capability.**

**Wave 1.0 includes:**
- Core execution and orchestration components
- Intent processing and decision resolution
- UI and dashboard foundation
- Governance hooks and evidence infrastructure

**Wave 1.0 explicitly excludes:**
- Advanced analytics and cost tracking (Wave 2+)
- Complex failure mode handling (Wave 2+)
- Deep integration scenarios (Wave 2+)
- System-wide scalability optimizations (Wave 2+)

### Wave 1.0 QA Range

**Wave 1.0 QA Range:** **QA-001 to QA-210**

**Total QA Components in Wave 1.0:** 210

**Category Breakdown:**
- Component-Based QA: QA-001 to QA-199 (foundation components)
- Flow-Based QA (partial): QA-200 to QA-210 (core flows only)

**Allowed RED (Wave 1.0):**
- QA-211 to QA-400+ (deferred to Wave 2+)

---

## Builder Assignment Strategy

### Strategy Rationale

**Example slicing guidance considered and adapted:**

The guidance suggested 4 builders (A, B, C, D) with ranges:
- Builder A: QA-001 → QA-060 (Core Execution & Orchestration)
- Builder B: QA-061 → QA-120 (Intent & Decision Core)
- Builder C: QA-121 → QA-170 (UI & Dashboard Foundation)
- Builder D: QA-171 → QA-210 (Governance & Evidence)

**FM adaptation:**

We have **5 recruited builders** with specialized capabilities:
1. **ui-builder** — Frontend, UI components, styling
2. **api-builder** — Backend, API endpoints, business logic
3. **schema-builder** — Database schemas, models, migrations
4. **integration-builder** — Inter-component wiring, events, integration
5. **qa-builder** — QA implementation, test coverage, evidence generation

**Assignment approach:**
- **Component-aligned assignment:** Assign QA ranges that map to architectural subsystems
- **Capability-aligned assignment:** Match builder capabilities to QA architectural focus
- **Balanced workload:** Distribute ~40-50 QA components per builder
- **Minimize cross-builder dependencies:** Group related QA together

---

## Builder Assignments (Wave 1.0)

### Builder 1: **api-builder** (Core Execution & Backend Logic)

**QA Range:** **QA-058 to QA-092** (35 QA components)

**Architectural Coverage:**
- Intent Processing Subsystem (INTENT-01 to INTENT-04): QA-058 to QA-077 (20 QA)
- Execution Orchestration Subsystem (EXEC-01 to EXEC-03): QA-078 to QA-092 (15 QA)

**Builder Responsibility:**
- Implement intent intake, clarification loop, requirement generation, approval logic
- Implement build orchestration, state management, progress tracking
- All backend logic and API endpoints for these subsystems

**Builder Capability Alignment:**
- ✅ api (API endpoint implementation)
- ✅ backend (business logic and orchestration)
- ✅ logic (decision workflows and state management)
- ✅ routes (routing and command handling)

**Gate ID:** `GATE-API-BUILDER-WAVE-1.0`

**Success Criteria:** QA-058 to QA-092 all GREEN

**Evidence Required:**
- Test execution results for QA-058 to QA-092
- API endpoint functional tests
- State transition validations
- Backend logic unit tests

---

### Builder 2: **ui-builder** (UI & Dashboard Foundation)

**QA Range:** **QA-019 to QA-057** (39 QA components)

**Architectural Coverage:**
- Conversational Interface UI (CONV-05): QA-019 to QA-022 (4 QA)
- Dashboard Subsystem (DASH-01 to DASH-04): QA-023 to QA-042 (20 QA)
- Parking Station UI (PARK-04): QA-054 to QA-057 (4 QA)
- Escalation UI (ESC-04): QA-110 to QA-116 (7 QA, from extended range)
- Additional UI components: QA-089 to QA-092 (4 QA, Build Visibility UI)

**Adjusted QA Range (to stay within Wave 1.0 and balance workload):**  
**QA-019 to QA-022, QA-036 to QA-042, QA-054 to QA-057, QA-089 to QA-092, QA-110 to QA-116**

**Simplified for bounded range:**  
**QA-019 to QA-022, QA-036 to QA-042, QA-054 to QA-057** (15 QA components base)

**Re-scoped for balance:**  
**QA-019 to QA-057** (39 QA components)

**Builder Responsibility:**
- Implement all UI renderers and components
- Conversation UI, Dashboard UI, Parking Station UI
- Visual design, responsiveness, accessibility
- Real-time UI updates

**Builder Capability Alignment:**
- ✅ ui (UI component implementation)
- ✅ frontend (React components and state management)
- ✅ components (reusable UI components)
- ✅ styling (CSS, visual design, accessibility)

**Gate ID:** `GATE-UI-BUILDER-WAVE-1.0`

**Success Criteria:** QA-019 to QA-057 all GREEN

**Evidence Required:**
- UI component tests for QA-019 to QA-057
- Visual regression tests
- Accessibility validation
- Responsiveness tests

---

### Builder 3: **schema-builder** (Data & State Foundation)

**QA Range:** **QA-001 to QA-018** (18 QA components)

**Architectural Coverage:**
- Conversational Interface Data (CONV-01 to CONV-04): QA-001 to QA-018 (18 QA)
- Conversation Manager, Message Handler, FM Initiator, Clarification Engine (data layer)

**Builder Responsibility:**
- Implement database schemas for Conversation, Message, Clarification entities
- Data persistence layer
- Database migrations
- Data model validation

**Builder Capability Alignment:**
- ✅ schema (database schema design)
- ✅ models (entity models and relationships)
- ✅ migrations (schema versioning and evolution)

**Gate ID:** `GATE-SCHEMA-BUILDER-WAVE-1.0`

**Success Criteria:** QA-001 to QA-018 all GREEN

**Evidence Required:**
- Database schema validation for QA-001 to QA-018
- Migration tests
- Data integrity tests
- CRUD operation tests

---

### Builder 4: **integration-builder** (Inter-Component Wiring & Events)

**QA Range:** **QA-093 to QA-131** (39 QA components)

**Architectural Coverage:**
- Escalation & Supervision Subsystem (ESC-01 to ESC-04): QA-093 to QA-116 (24 QA)
- Governance Enforcement Subsystem (GOV-01 to GOV-03): QA-117 to QA-131 (15 QA)

**Builder Responsibility:**
- Implement ping generation, escalation manager, silence detector
- Implement governance loader, validator, supremacy enforcer
- Event routing and inter-component messaging
- Integration contracts

**Builder Capability Alignment:**
- ✅ integration (inter-component wiring)
- ✅ inter-module (event routing and messaging)
- ✅ events (event bus and pub/sub patterns)

**Gate ID:** `GATE-INTEGRATION-BUILDER-WAVE-1.0`

**Success Criteria:** QA-093 to QA-131 all GREEN

**Evidence Required:**
- Integration tests for QA-093 to QA-131
- Event routing validation
- Inter-component communication tests
- Governance enforcement tests

---

### Builder 5: **qa-builder** (QA Implementation & Evidence)

**QA Range:** **QA-132 to QA-210** (79 QA components)

**Architectural Coverage:**
- Analytics Subsystem (ANALYTICS-01 to ANALYTICS-03): QA-132 to QA-146 (15 QA)
- Cross-Cutting Components (CROSS-01 to CROSS-06): QA-147 to QA-199 (53 QA)
- Flow-Based QA (partial): QA-200 to QA-210 (11 QA)

**Builder Responsibility:**
- Implement QA-to-Red test suite for assigned QA range
- Generate evidence artifacts for all QA components
- Implement test infrastructure and framework
- Validate cross-cutting concerns (memory, authority, audit, evidence, notification, watchdog)
- Validate core user flows (Intent → Build Execution flow initial steps)

**Builder Capability Alignment:**
- ✅ testing (test implementation and execution)
- ✅ coverage (test coverage analysis and reporting)
- ✅ qa-of-qa (meta-testing and QA validation)

**Gate ID:** `GATE-QA-BUILDER-WAVE-1.0`

**Success Criteria:** QA-132 to QA-210 all GREEN

**Evidence Required:**
- QA execution results for QA-132 to QA-210
- Test coverage reports (must be 100% for assigned QA)
- Evidence artifact validation
- QA-of-QA reports

**Special Note:**  
qa-builder's work is **cross-builder validation**. While other builders make their QA GREEN through implementation, qa-builder implements the **test code itself** and validates cross-cutting concerns.

---

## Assignment Summary Table

| Builder | QA Range | QA Count | Subsystems Covered | Gate ID |
|---------|----------|----------|---------------------|---------|
| schema-builder | QA-001 to QA-018 | 18 | Conversational Interface (data) | GATE-SCHEMA-BUILDER-WAVE-1.0 |
| ui-builder | QA-019 to QA-057 | 39 | Conversational UI, Dashboard UI, Parking UI | GATE-UI-BUILDER-WAVE-1.0 |
| api-builder | QA-058 to QA-092 | 35 | Intent Processing, Execution Orchestration | GATE-API-BUILDER-WAVE-1.0 |
| integration-builder | QA-093 to QA-131 | 39 | Escalation & Supervision, Governance Enforcement | GATE-INTEGRATION-BUILDER-WAVE-1.0 |
| qa-builder | QA-132 to QA-210 | 79 | Analytics, Cross-Cutting, Core Flows | GATE-QA-BUILDER-WAVE-1.0 |

**Total Wave 1.0 QA:** 210 components  
**Total Assigned:** 210 components  
**Coverage:** 100% of Wave 1.0 scope

---

## Assignment Validation

### Validation Checklist

**For each builder:**
- ✅ QA range is explicit and bounded
- ✅ No overlapping QA assignments (each QA assigned to exactly one builder)
- ✅ Builder capability aligns with QA architectural focus
- ✅ Gate ID defined for each builder
- ✅ Success criteria = all assigned QA GREEN

**For the system:**
- ✅ All Wave 1.0 QA (QA-001 to QA-210) are assigned
- ✅ No Wave 1.0 QA are unassigned
- ✅ Wave 1.0 QA ranges are contiguous and complete
- ✅ Wave 2+ QA (QA-211 to QA-400+) are explicitly deferred

**Result:** ✅ Assignment plan is valid and complete

---

## Parallel Execution Capability

### Non-Blocking Assignments

**All builders can work in parallel:**

- **schema-builder** (QA-001 to QA-018) → No dependencies on other builders initially
- **ui-builder** (QA-019 to QA-057) → Depends on schema-builder for data models
- **api-builder** (QA-058 to QA-092) → Depends on schema-builder for data models
- **integration-builder** (QA-093 to QA-131) → Depends on api-builder for components to integrate
- **qa-builder** (QA-132 to QA-210) → Can work in parallel, validates cross-cutting and infrastructure

### Recommended Execution Sequence

**Phase 1 (Parallel Start):**
- schema-builder begins: QA-001 to QA-018
- qa-builder begins (infrastructure): QA-147 to QA-182 (cross-cutting infrastructure)

**Phase 2 (After schema foundation):**
- ui-builder begins: QA-019 to QA-057
- api-builder begins: QA-058 to QA-092
- integration-builder begins: QA-093 to QA-116 (escalation subsystem)

**Phase 3 (Full parallel):**
- All builders working simultaneously
- integration-builder completes: QA-117 to QA-131 (governance)
- qa-builder completes: QA-132 to QA-146 (analytics), QA-183 to QA-210 (flows)

**No strict sequencing required** — dependencies will naturally resolve as builders progress.

---

## Wave 1.0 Completion Criteria

### Wave 1.0 Gate Definition

**Gate ID:** `GATE-WAVE-1.0-COMPLETE`

**Required GREEN:** **QA-001 to QA-210** (all 210 Wave 1.0 QA components)

**Allowed RED:** **QA-211 to QA-400+** (all Wave 2+ components)

**Gate Type:** Wave Gate

**Enforcement:** BLOCKING (no Wave 2.0 start until Wave 1.0 GREEN)

**Evaluation Logic:**
```
IF all QA in range [QA-001 to QA-210] are GREEN:
    THEN Wave 1.0 Gate = PASS
ELSE:
    THEN Wave 1.0 Gate = FAIL
    AND List which QA are still RED (blockers)
```

### Success Criteria

Wave 1.0 is complete when:
- ✅ All 5 builder gates PASS (each builder's assigned QA range GREEN)
- ✅ Wave 1.0 Gate PASS (QA-001 to QA-210 all GREEN)
- ✅ Evidence exists for all 210 QA components
- ✅ No regressions (all GREEN QA remain GREEN)
- ✅ Audit trail complete

**Wave 2.0 may begin only when Wave 1.0 Gate = PASS**

---

## Builder Collaboration Rules

### Cross-Builder Dependencies

**Explicit dependencies:**

1. **ui-builder depends on schema-builder**
   - UI components need data models to render
   - Resolution: schema-builder completes data layer first, or provides interface contracts early

2. **api-builder depends on schema-builder**
   - API endpoints need data models to persist
   - Resolution: schema-builder completes data layer first, or provides interface contracts early

3. **integration-builder depends on api-builder**
   - Integration wiring needs components to wire together
   - Resolution: api-builder provides component contracts, integration-builder wires them

4. **qa-builder validates all builders**
   - QA tests validate work by all other builders
   - Resolution: qa-builder works in parallel, tests become GREEN as builders complete implementation

### Dependency Handling

**When a builder is blocked by dependency:**
- Builder escalates via ESC-02 Escalation Manager (5-element escalation)
- FM investigates: expedite upstream builder, reassign QA, or adjust scope
- No silent blocking — all blockers must be escalated

**Example Escalation:**
```
Builder: ui-builder
What: Cannot implement QA-019 (Render conversation UI)
Why: Conversation data model not available
Blocked: schema-builder has not completed QA-001 to QA-005
Decision Required: Should ui-builder wait, or should FM provide mock interface?
Consequence: If no decision, UI work stalls for 1+ days
```

---

## Acceptance Criteria (Phase 4.5)

This Builder Assignment Plan is complete when:

- ✅ Every builder has an explicit QA-bounded scope (5 builders, 5 QA ranges defined)
- ✅ No QA is assigned to more than one builder (validated: no overlaps)
- ✅ All Wave 1.0 QA are accounted for (210 QA assigned, 0 unassigned)
- ✅ Gate semantics are deterministic (5 builder gates + 1 Wave 1.0 gate defined)
- ✅ No implementation activity has occurred (design-only phase confirmed)
- ✅ Builder capability aligns with assigned QA (validated for all 5 builders)
- ✅ Parallel execution enabled (dependencies identified, non-blocking strategy defined)

**FM Acceptance Required:** See end of document

---

## Next Steps (Post-Acceptance)

**After CS2 accepts this Builder Assignment Plan:**

1. **Generate Builder Task Specifications**
   - Create `PHASE_4.5_BUILDER_TASK_<BUILDER_NAME>.md` for each builder
   - Detailed specifications per builder with QA range, architecture, evidence, gate

2. **Define Wave 1.0 Definition Document**
   - Formal declaration of Wave 1.0 completion criteria
   - QA ranges, allowed RED, gate topology

3. **Design Gate Topology**
   - Builder gates (5)
   - Wave 1.0 gate
   - Final system gate (all 400+ QA)

4. **Obtain Final Phase 4.5 Acceptance**
   - All deliverables complete
   - Ready for Phase 5.0 — Wave 1.0 Build-to-Green Execution

---

## FM Acceptance Declaration

I, Foreman (FM), confirm that this Builder Assignment Plan:

- Defines 5 builder assignments with explicit QA ranges
- Covers all Wave 1.0 QA (QA-001 to QA-210) with 100% assignment
- Aligns builder capabilities with QA architectural focus
- Enables parallel builder execution with identified dependencies
- Defines 5 builder gates + 1 Wave 1.0 gate
- Respects bounded assignment principles (no overlaps, no gaps)
- Enables deterministic build-to-green execution
- Requires no code inspection by CS2 (evidence-based validation)
- Is design-only (no implementation occurred)

**Accepted By:** Foreman (FM)  
**Date:** 2025-12-31  
**Phase:** 4.5 — Builder Task Assignment (Design-Only)  
**Status:** DESIGN_COMPLETE — READY FOR DETAILED TASK SPECS

---

**End of Builder Assignment Plan**
