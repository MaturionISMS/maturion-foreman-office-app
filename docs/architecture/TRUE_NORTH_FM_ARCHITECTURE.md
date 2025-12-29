# FM App True North Architecture

**Version:** 1.0  
**Date:** 2025-12-29  
**Status:** FROZEN - Canonical Architecture  
**Purpose:** Single source of truth for FM App architecture  
**Authority:** Governance Agent (ARCH-RECOVERY-01) - Pending Johan Approval  
**Precedence:** This document supersedes all prior architecture documents upon approval

---

## Document Status and Authority

**THIS DOCUMENT IS THE CANONICAL ARCHITECTURE.**

Upon approval by Johan (CS2), this document becomes the **single, authoritative** definition of the FM App architecture. All prior architecture documents, specifications, and design artifacts are subordinate to this document.

**Derivation Order (Constitutional Hierarchy):**
```
Governance Repository (Constitutional Authority)
    ↓
BUILD_PHILOSOPHY.md (Supreme Build Authority)
    ↓
APP_DESCRIPTION.md (Authoritative Product Intent)
    ↓
FM_FUNCTIONAL_SPEC.md (Functional Baseline)
    ↓
TRUE_NORTH_FM_ARCHITECTURE.md (THIS DOCUMENT - Frozen Architecture)
    ↓
Implementation (Governed by this architecture)
```

**Modification Rules:**
- This document may only be modified with explicit Johan (CS2) approval
- All modifications must go through governance change management
- No implementation may deviate from this architecture
- No builder may interpret this architecture differently

---

## 1. Executive Summary

The FM App is a **continuous supervisory control system** that provides orchestration, governance enforcement, and operational visibility for autonomous AI-driven software construction.

**Core Problem Solved:**  
Burst-based AI platforms cannot provide continuous supervision, persistent awareness, or governance enforcement across long-running build programs.

**Core Solution:**  
FM provides the missing supervisory layer with:
- Persistent execution state awareness
- Program/Wave/Task orchestration
- Governance enforcement (Build Authorization Gate, QA, Evidence, Memory)
- Liveness monitoring and stall detection
- Human-in-the-loop escalation and intervention

---

## 2. Architectural Scope and Boundaries

### 2.1 What FM App IS

1. **Supervisory Runtime** - Always-on orchestration and governance enforcement
2. **Execution Cockpit** - Real-time visibility for human authority (Johan)
3. **Governance Enforcer** - Validates and enforces all governance rules
4. **Memory Manager** - Manages operational memory with privacy/tenant isolation
5. **Intervention Controller** - Provides safe human intervention with audit trail

### 2.2 What FM App IS NOT

1. **Not a CI/CD System** - Does not replace GitHub Actions
2. **Not a Code Editor** - Does not edit code directly
3. **Not a GitHub Replacement** - GitHub remains system of record for code
4. **Not a Passive Dashboard** - Actively governs and controls execution
5. **Not a Governance Author** - Consumes governance, does not create it

### 2.3 Authority Boundaries

**FM App Authority:**
- Orchestrate builder agents
- Enforce governance rules
- Manage execution state
- Escalate to human authority

**FM App CANNOT:**
- Modify governance rules
- Bypass Build Authorization Gate
- Override QA requirements
- Approve its own work
- Implement features directly (delegates to builders)

---

## 3. Core Architecture Components (Adopted from Implementation)

This section explicitly adopts the 53 "adopt as-is" components identified in Phase 2 as the canonical architecture.

### 3.1 FM Orchestration Layer

**Purpose:** Browser-accessible control panel for build orchestration and intervention

**Canonical Components (Adopted):**

| Component | Location | Status | Role |
|-----------|----------|--------|------|
| Build Control API | `fm/orchestration/build_control_api.py` | **CANONICAL** | REST API providing orchestration endpoints |
| Build Authorization Gate | `fm/orchestration/build_authorization_gate.py` | **CANONICAL** | Validates 8 preconditions before build execution |
| Build Node Inspector | `fm/orchestration/build_node_inspector.py` | **CANONICAL** | Inspection/drill-down for Program/Wave/Task nodes |
| Build Intervention Controller | `fm/orchestration/build_intervention.py` | **CANONICAL** | Human intervention with audit trail (G-C10) |

**UI Components (Development/Testing):**

| Component | Location | Status | Constraint |
|-----------|----------|--------|------------|
| Build Control Panel UI | `fm/orchestration/static/` | **DEV/TEST ONLY** | Vanilla HTML/JS - mark as non-production |
| Inspector UI | `fm/orchestration/static/inspector.*` | **DEV/TEST ONLY** | Vanilla HTML/JS - mark as non-production |
| Intervention UI | `fm/orchestration/static/intervention.*` | **DEV/TEST ONLY** | Vanilla HTML/JS - mark as non-production |

**UI Framework Decision (Future):**  
Production UI framework (React/Next.js vs vanilla JS) is not yet frozen. Current UIs are functional for development/testing but should not be considered the canonical production UI approach.

**Architectural Contracts:**
- Build Authorization Gate MUST validate before ANY build execution
- Intervention MUST create audit trail for all stop/resume actions
- Inspector MUST provide "no status without explanation" (G-C9)
- All actions MUST require explicit human authorization

### 3.2 FM Runtime / Watchdog

**Purpose:** Runtime observability and escalation

**Canonical Components (Adopted):**

| Component | Location | Status | Role |
|-----------|----------|--------|------|
| Watchdog Alert Reader | `fm/runtime/watchdog/alert_reader.py` | **CANONICAL** | Reads and parses watchdog alerts |
| Watchdog Escalation Reporter | `fm/runtime/watchdog/escalation_reporter.py` | **CANONICAL** | Reports escalations to appropriate channels |

**Architectural Contracts:**
- All runtime alerts MUST be routed through Alert Reader
- All escalations MUST be logged with full context

### 3.3 Foreman Runtime / Orchestration Engine

**Purpose:** Core orchestration logic managing Program/Wave/Task lifecycle

**Canonical Components (Adopted):**

| Component | Location | Status | Role |
|-----------|----------|--------|------|
| Program Manager | `foreman/runtime/program_manager.py` | **CANONICAL** | Manages programs, status aggregation, progress tracking |
| Task Manager | `foreman/runtime/task_manager.py` | **CANONICAL** | Manages task lifecycle, state transitions, assignments |
| Blocker Manager | `foreman/runtime/blocker_manager.py` | **CANONICAL** | Manages blockers, detects blocked states |
| Notification Manager | `foreman/runtime/notification_manager.py` | **CANONICAL** | Routes notifications to appropriate channels |
| Build Executor | `foreman/runtime/build_executor.py` | **CANONICAL** | Executes build operations based on orchestration |
| Recovery Guide | `foreman/runtime/recovery_guide.py` | **CANONICAL** | Provides recovery guidance for failures |

**Architectural Contracts:**
- Program Manager MUST aggregate status from Wave → Task hierarchy
- Task Manager MUST validate state transitions
- Blocker Manager MUST classify blockers (transient vs permanent)
- All state changes MUST be logged

### 3.4 Foreman Runtime / Liveness Monitoring

**Purpose:** Detect silent stalls (core FM value proposition)

**Canonical Components (Adopted):**

| Component | Location | Status | Role |
|-----------|----------|--------|------|
| Heartbeat Monitor | `foreman/runtime/liveness/heartbeat_monitor.py` | **CANONICAL** | Monitors agent/builder heartbeats |
| Stall Detector | `foreman/runtime/liveness/stall_detector.py` | **CANONICAL** | Detects silent stalls in execution |
| Recovery Manager | `foreman/runtime/liveness/recovery_manager.py` | **CANONICAL** | Manages recovery from stalls/failures |

**Architectural Contracts:**
- Heartbeat Monitor MUST detect missing heartbeats within defined threshold
- Stall Detector MUST escalate on prolonged silence
- Recovery Manager MUST provide recovery strategies
- "No update" is a CRITICAL signal, not neutral state

### 3.5 Foreman Governance Enforcement

**Purpose:** Enforce governance rules without human micromanagement

**Canonical Components (Adopted):**

| Component | Location | Status | Role |
|-----------|----------|--------|------|
| Task Completion Governance | `foreman/governance/task_completion.py` | **CANONICAL** | Enforces task completion criteria |
| QA Enforcement | `foreman/governance/qa_enforcement.py` | **CANONICAL** | Enforces QA policies and coverage |
| Memory Governance | `foreman/governance/memory.py` | **CANONICAL** | Governs memory read/write operations |
| Evidence Gate | `foreman/governance/evidence_gate.py` | **CANONICAL** | Validates evidence before progression |
| Architecture Freeze | `foreman/governance/architecture_freeze.py` | **CANONICAL** | Enforces architecture freeze rules |
| CS2 Approval | `foreman/governance/cs2_approval.py` | **CANONICAL** | Handles Johan approval workflows |
| Audit Replay | `foreman/governance/audit_replay.py` | **CANONICAL** | Replays audit logs for validation |
| Build State Governance | `foreman/governance/build_state.py` | **CANONICAL** | Governs build state transitions |

**Architectural Contracts:**
- Governance rules are CONSTITUTIONAL, not advisory
- All governance violations MUST halt or escalate (per hard/soft stop rules)
- NO silent continuation on governance violation
- NO weakening of governance to proceed

### 3.6 Foreman Decision Support

**Purpose:** Decision recording, replay, and task decomposition

**Canonical Components (Adopted):**

| Component | Location | Status | Role |
|-----------|----------|--------|------|
| Completion Validator | `foreman/decision/completion_validator.py` | **CANONICAL** | Validates task/wave/program completion |
| Trace Recorder | `foreman/decision/trace_recorder.py` | **CANONICAL** | Records decision traces for audit |
| Trace Replayer | `foreman/decision/trace_replayer.py` | **CANONICAL** | Replays decision traces for analysis |
| Task Decomposer | `foreman/decision/task_decomposer.py` | **CANONICAL** | Decomposes high-level tasks |
| Recovery Strategy Selector | `foreman/decision/recovery_strategy_selector.py` | **CANONICAL** | Selects recovery strategies |

**Architectural Contracts:**
- All decisions MUST be traceable
- Trace replay MUST be deterministic
- Decomposition MUST respect governance constraints

### 3.7 Foreman Domain Models

**Purpose:** Core data models for Program/Wave/Task hierarchy

**Canonical Components (Adopted):**

| Component | Location | Status | Role |
|-----------|----------|--------|------|
| Program | `foreman/domain/program.py` | **CANONICAL** | Program domain model |
| Wave | `foreman/domain/wave.py` | **CANONICAL** | Wave domain model |
| Task | `foreman/domain/task.py` | **CANONICAL** | Task domain model |
| Blocker | `foreman/domain/blocker.py` | **CANONICAL** | Blocker domain model |

**Architectural Contracts:**
- Program contains Waves
- Wave contains Tasks
- Task may have Blockers
- All models MUST support state transitions

### 3.8 Foreman Evidence System

**Purpose:** Evidence collection, validation, and audit trail

**Canonical Components (Adopted):**

| Component | Location | Status | Role |
|-----------|----------|--------|------|
| Evidence Tracer | `foreman/evidence/tracer.py` | **CANONICAL** | Traces evidence collection |
| Evidence Schema Validator | `foreman/evidence/schema_validator.py` | **CANONICAL** | Validates evidence against schemas |
| Evidence Generator | `foreman/evidence/generator.py` | **CANONICAL** | Generates evidence artifacts |

**Architectural Contracts:**
- All evidence MUST be schema-validated
- Evidence MUST be traceable to source action
- Evidence MUST be immutable after generation

### 3.9 Memory Fabric (TypeScript/JavaScript)

**Purpose:** Memory integration for TypeScript/JS applications (Next.js/Vercel)

**Canonical Components (Adopted):**

| Component | Location | Status | Role |
|-----------|----------|--------|------|
| Memory Client | `lib/memory/client.ts` | **CANONICAL** | TypeScript memory fabric client |
| Memory Store | `lib/memory/store.ts` | **CANONICAL** | Memory persistence and retrieval |
| Memory Health Monitor | `lib/memory/health-monitor.ts` | **CANONICAL** | Monitors memory fabric health |
| Memory Lifecycle Manager | `lib/memory/lifecycle-manager.ts` | **CANONICAL** | Manages memory entry lifecycle |
| Memory Observability Service | `lib/memory/observability-service.ts` | **CANONICAL** | Observability for memory operations |
| Memory Observability Integration | `lib/memory/observability-integration.ts` | **CANONICAL** | Integrates with observability systems |
| Memory Privacy Checker | `lib/memory/privacy-checker.ts` | **CANONICAL** | Validates privacy rules (tenant isolation) |
| Memory Audit Logger | `lib/memory/audit-logger.ts` | **CANONICAL** | Logs memory operations for audit |
| Memory Schema Validator | `lib/memory/schema-validator.ts` | **CANONICAL** | Validates memory entries against schemas |
| Memory Runtime Loader | `lib/memory/runtime-loader.ts` | **CANONICAL** | Loads memory at runtime |

**UI Components (Development/Testing):**

| Component | Location | Status | Constraint |
|-----------|----------|--------|------------|
| Memory Dashboard | `lib/memory/dashboard.ts` | **DEV/TEST ONLY** | Subject to production UI framework decision |

**Architectural Contracts:**
- ALL memory operations MUST pass privacy checks (tenant isolation)
- ALL memory writes MUST be logged for audit
- ALL memory entries MUST be schema-validated
- Memory is READ-ONLY at runtime; writes are PROPOSALS only

### 3.10 Commissioning System

**Purpose:** Controls FM App lifecycle (NOT_COMMISSIONED → ACTIVE → SUSPENDED)

**Canonical Components (Adopted):**

| Component | Location | Status | Role |
|-----------|----------|--------|------|
| Commissioning Controller | `lib/commissioning/CommissioningController.ts` | **CANONICAL** | Governs app commissioning lifecycle |
| Commissioning State | `runtime/commissioning/state.example.json` | **CANONICAL** | Example state structure |

**Architectural Contracts:**
- App MUST NOT operate unless state >= COMMISSIONED
- State transitions MUST be audited
- Decommissioning MUST be explicit, never automatic

### 3.11 Memory Storage and Authority

**Purpose:** Persistent memory storage with governance

**Canonical Components (Adopted):**

| Component | Location | Status | Role |
|-----------|----------|--------|------|
| Tenant Memory Architecture | `memory/TENANT_MEMORY_ARCHITECTURE.md` | **CANONICAL** | Architecture for tenant-isolated memory |
| Memory Schemas | `memory/schema/*.json` | **CANONICAL** | JSON schemas for memory structures |
| Platform Memory | `memory/platform/runtime-events.json` | **CANONICAL** | Platform-level memory events |
| Foreman Memory | `memory/foreman/*.json` | **CANONICAL** | Foreman-specific memory entries |
| Global Memory Seed | `memory/global/seed-*.json` | **CANONICAL** | Seed memory for bootstrapping |
| Memory Authority Docs | `memory/AUTHORITY/*.md` | **CANONICAL** | Authority and policy for memory |

**Test/Simulation Components:**

| Component | Location | Status | Constraint |
|-----------|----------|--------|------------|
| Tenant Memory Simulation | `memory/tenant/simulation/` | **SIMULATION ONLY** | NEVER use with production data |

**Architectural Contracts:**
- Tenant isolation MUST be enforced at all times
- Memory schemas MUST be versioned
- All memory writes MUST be proposals, not automatic
- Simulation data MUST be clearly marked

### 3.12 Tooling and Scripts

**Purpose:** Integration utilities and testing tools

**Canonical Components (Adopted):**

| Component | Location | Status | Role |
|-----------|----------|--------|------|
| Agent Context Sync | `scripts/sync-agent-context.py` | **CANONICAL** | Syncs agent context with memory |
| GitHub Model Routing | `lib/github/model-routing.ts` | **CANONICAL** | Routes GitHub operations |

**Testing Tools:**

| Component | Location | Status | Constraint |
|-----------|----------|--------|------------|
| Reset Tenant Memory | `scripts/reset-tenant-memory.py` | **TESTING ONLY** | MUST include strong warnings, require confirmation |

**Architectural Contracts:**
- Testing tools MUST be clearly marked "TESTING ONLY"
- Testing tools MUST require confirmation for destructive operations
- Testing tools MUST NEVER be used in production

### 3.13 Builder Initialization

**Purpose:** Initialize and validate builder agents

**Canonical Components (Adopted):**

| Component | Location | Status | Role |
|-----------|----------|--------|------|
| Builder Initialization | `foreman/init_builders.py` | **CANONICAL** | Initializes and validates builder agents |

**Architectural Contracts:**
- Builder initialization MUST validate builder capabilities
- Builder initialization MUST enforce builder permissions

---

## 4. QA and Testing Architecture

**Purpose:** Ensure implementation quality and governance compliance

**Canonical QA Components (Adopted):**

| Component | Location | Status | Role |
|-----------|----------|--------|------|
| Wave 0 Red QA Tests | `tests/wave0_minimum_red/` | **CANONICAL** | Red QA for Wave 0 validation |
| Governance Memory Sync Test | `tests/test_governance_memory_sync.py` | **CANONICAL** | Tests governance-memory sync |
| Global Memory Runtime Test | `tests/test_global_memory_runtime.py` | **CANONICAL** | Tests global memory runtime |
| Watchdog Runtime Test | `tests/test_watchdog_runtime.py` | **CANONICAL** | Tests watchdog components |
| Build Control API Test | `tests/test_build_control_api.py` | **CANONICAL** | Tests Build Control API |
| Build Node Inspector Test | `tests/test_build_node_inspector.py` | **CANONICAL** | Tests Build Node Inspector |
| Build Intervention Test | `tests/test_build_intervention.py` | **CANONICAL** | Tests Build Intervention Controller |
| Build Authorization Gate Test | `tests/test_build_authorization_gate.py` | **CANONICAL** | Tests Build Authorization Gate |
| Memory Proposals Test | `tests/test_memory_proposals.py` | **CANONICAL** | Tests memory proposal workflow |
| CHP Memory Integration Test | `tests/test_chp_memory_integration.py` | **CANONICAL** | Tests CHP-memory integration |
| Commissioning Controller Test | `tests/test_commissioning_controller.py` | **CANONICAL** | Tests Commissioning Controller |
| Memory Lifecycle Runtime Test | `tests/test_memory_lifecycle_runtime.py` | **CANONICAL** | Tests memory lifecycle |

**QA Governance Contracts:**
- Red QA tests MUST pass before any progression
- All components MUST have test coverage
- Governance violations MUST be tested (negative tests)
- Test failures MUST block builds

---

## 5. Explicitly Out of Scope (Not Implemented)

The following are **designed but not yet implemented**. They remain in the backlog:

- Foreman v1.0 Architecture Suite (60+ specification documents in `foreman/architecture/`, `foreman/builder/`, etc.)
- Builder Specifications (API, UI, Schema, Integration, QA builders)
- QA System (beyond Red QA tests)
- Compliance Engine
- Platform Components (dashboards, reporting)
- Innovation System
- Admin Features
- Survey System

**Governance Rule:**  
These specifications exist as DESIGN INTENT but are NOT canonical until implemented and adopted. Implementation must follow this True North Architecture, not directly from those specifications.

---

## 6. Role Boundaries and Authority

### 6.1 Governance Agent Role

**Permitted:**
- Read repository contents
- Create/update governance, architecture, policy documents
- Propose (but not execute) changes
- Classify and recommend

**Forbidden:**
- Modify implementation code (`fm/`, `foreman/`, `lib/`, `scripts/`, `tests/`)
- Modify runtime logic
- Add features
- Refactor implementations
- Touch canonical implementation paths

### 6.2 Builder Agent Role

**Permitted:**
- Implement features under Foreman direction
- Execute scoped technical work
- Create tests
- Escalate blockers

**Forbidden:**
- Self-govern
- Self-approve
- Interpret governance independently
- Modify governance documents
- Modify architecture documents

### 6.3 FM (Foreman) Role

**Permitted:**
- Orchestrate builders
- Enforce governance
- Manage execution state
- Escalate to human authority

**Forbidden:**
- Modify governance rules
- Bypass Build Authorization Gate
- Override QA requirements
- Approve own work
- Implement features directly

### 6.4 Human Authority (Johan/CS2) Role

**Authority:**
- Final approval on all architecture changes
- Final approval on governance changes
- Final approval on build progression
- Final intervention decisions

---

## 7. Lifecycle and Build Phases

### 7.1 Commissioning Lifecycle

```
NOT_COMMISSIONED → COMMISSIONING → COMMISSIONED → ACTIVE → SUSPENDED
```

**Rules:**
- App MUST NOT operate in NOT_COMMISSIONED state
- Commissioning requires explicit human authorization
- Decommissioning requires explicit human authorization
- State transitions MUST be audited

### 7.2 Build Lifecycle

```
Program → Wave → Task → Execution → QA → Evidence → Completion
```

**Gates:**
- Build Authorization Gate (8 preconditions)
- Architecture Freeze Gate
- QA Gate (Red QA must pass)
- Evidence Gate
- Completion Validation

### 7.3 Memory Lifecycle

```
Proposal → Validation → Privacy Check → Schema Validation → Persistence → Audit
```

**Rules:**
- Memory writes are PROPOSALS, not automatic
- ALL writes pass privacy check (tenant isolation)
- ALL writes are schema-validated
- ALL writes are audited

---

## 8. Non-Authoritative / Scaffolding / Bootstrap Elements

The following are explicitly marked as **non-authoritative** or **bootstrap-only**:

### 8.1 Root-Level Utility Scripts (Refactor Later - Non-Blocking)

Scripts in repository root should be moved to `scripts/` directory:
- `plan-build.py`, `plan-build-wave-1.py`
- `create-build-tasks.py`, `create-build-tasks-wave-1.py`
- `generate-build-status-wave-1.py`, `summarize-build-cycle.py`, `summarize-build-wave-1.py`
- `generate-wave1-change-records.py`
- `bulk-generate-architecture.py`, `generate-arch-part1.py`
- `standardise-architecture.py`
- `validate-repository.py`, `validate-build-wave-1.py`
- `test-foreman-integration.py`
- `init-memory-fabric.py`
- `export-runtime-context.py`
- `activate-compliance-engine.py`
- `index-isms-architecture.py`

**Status:** These work but need proper placement. Non-blocking refactor.

### 8.2 Root-Level Build Artifacts (Deprecate - Cleanup Required)

The following should be gitignored or moved to `runtime/`:
- `build-plan.json`, `build-plan-wave-*.json`
- `build-status.json`, `build-status-wave-*.json`
- `build-tasks.json`, `build-tasks-wave-*.json`
- `build-cycle-summary.json`
- `standardisation_results.json`
- `ARCHITECTURE_INDEX.json`

**Status:** Execution artifacts that should not be in source control. Cleanup required.

### 8.3 Root-Level Summary Documents (Refactor Later - Archive)

40+ summary/completion/report documents in root should be moved to `reports/` or `history/`:
- `*_SUMMARY.md`
- `*_COMPLETION_SUMMARY.md`
- `*_REPORT.md`
- `*_PROOF.md`
- `*_IMPLEMENTATION_SUMMARY.md`

**Status:** Historical execution records. Should be archived for audit trail. Non-blocking refactor.

### 8.4 Empty/Minimal Files (Deprecate - Remove)

- `uploads` (1-byte file)
- `generate-architecture-components.py` (0 bytes)

**Status:** No functional value. Should be removed.

### 8.5 Package.json (Clarify Purpose)

- `package.json` and `package-lock.json` in root

**Status:** Minimal content. Purpose should be documented. If experimental, mark clearly. If production, expand properly.

---

## 9. Cleanup Backlog (Non-Blocking)

The following cleanup tasks are recommended but **do not block** architecture freeze:

1. **Move utility scripts to scripts/** - Improves repository organization
2. **Gitignore build artifacts** - Reduces repository clutter
3. **Archive historical summaries to reports/history/** - Preserves audit trail, cleans root
4. **Remove empty files** - Reduces repository noise
5. **Document package.json purpose** - Clarifies npm usage

These may be completed in a future "Repository Hygiene" task after architecture freeze.

---

## 10. Architecture Freeze Declaration

Upon Johan (CS2) approval, this architecture is **FROZEN**.

**Freeze Semantics:**
- All 53 "adopt as-is" components are CANONICAL and MAY NOT be modified without governance approval
- All 11 "adopt with constraints" components are CANONICAL with documented constraints
- All "refactor later" items are non-blocking backlog items
- All "deprecate" items should be cleaned up but do not block progression
- All future implementation MUST align with this architecture
- All deviations MUST go through governance change management

**What This Freeze Enables:**
- Builders can implement with confidence that architecture will not change
- QA can test against stable baseline
- Foreman can orchestrate builds knowing the foundation is solid
- Human authority can approve knowing the architecture is complete

**What This Freeze Does NOT Prevent:**
- Bug fixes (within existing architecture)
- Performance improvements (within existing architecture)
- Test additions (supporting existing architecture)
- Documentation improvements
- Repository hygiene (cleanup backlog)

---

## 11. Next Steps After Freeze

1. **Phase 4: Back-Derivation**
   - Update `APP_DESCRIPTION.md` to align with frozen architecture
   - Update/recreate `FUNCTIONAL_REQUIREMENTS.md` to align with frozen architecture

2. **Phase 5: Role Boundary Enforcement**
   - Create mechanical enforcement for role boundaries
   - Define agent permissions and capabilities
   - Implement governance checks

3. **Resume Build Orchestration**
   - FM can safely orchestrate builds
   - Builders can implement with confidence
   - QA can validate against canonical architecture

---

## 12. Approval and Sign-Off

**Pending Approval By:** Johan Ras (CS2 / Human Authority)

**Approval Checklist:**
- [ ] Architecture accurately reflects implemented components
- [ ] Architecture constraints are clear and enforceable
- [ ] Role boundaries are explicit
- [ ] Out-of-scope items are clearly marked
- [ ] Cleanup backlog is non-blocking
- [ ] Freeze semantics are understood

**Approval Date:** _________________

**Signature:** _________________

---

**End of True North FM Architecture v1.0**

This document is the canonical architecture for the FM App and supersedes all prior architecture documents upon approval.
