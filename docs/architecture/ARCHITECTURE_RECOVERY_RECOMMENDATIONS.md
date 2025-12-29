# FM App Architecture Recovery Recommendations

**Version:** 1.0  
**Date:** 2025-12-29  
**Status:** Phase 2 Complete - Classification & Recommendations  
**Purpose:** Governance recommendations for each implemented artifact  
**Authority:** Governance Agent (ARCH-RECOVERY-01)  
**Input:** ARCHITECTURE_RECOVERY_INVENTORY.md (Phase 1)

---

## Overview

This document provides governance recommendations for each implemented artifact identified in Phase 1. For each artifact, we propose one of four classifications:

1. **Adopt as-is** — Component is production-ready and aligns with governance
2. **Adopt with constraints** — Component is valuable but requires boundaries/limitations
3. **Refactor later** — Component works but needs improvement in future iteration
4. **Deprecate** — Component should be removed or replaced

Each recommendation includes:
- Classification
- Governance rationale
- Risks if kept
- Risks if dropped

---

## FM Orchestration Components

### Build Control API
**Classification:** Adopt as-is  
**Rationale:** Provides essential REST API for UI-backend communication. Clean implementation with proper separation of concerns. Implements Flask best practices with CORS support.  
**Risks if kept:** None significant. Standard Flask app.  
**Risks if dropped:** Would require complete reimplementation to support any UI.  

### Build Authorization Gate
**Classification:** Adopt as-is  
**Rationale:** Implements critical governance control - validates 8 mandatory preconditions before build execution. This is a core governance enforcement mechanism referenced in governance documentation.  
**Risks if kept:** None. This is a governance-critical component.  
**Risks if dropped:** Builds could proceed without proper validation, violating governance.  

### Build Node Inspector
**Classification:** Adopt as-is  
**Rationale:** Implements "No status without explanation" principle from G-C9 specification. Provides essential inspection capabilities for Program/Wave/Task nodes. Well-structured with clear separation of concerns.  
**Risks if kept:** None significant. Inspection is read-only and safe.  
**Risks if dropped:** Would lose visibility into build tree structure and status explanations.  

### Build Intervention Controller
**Classification:** Adopt as-is  
**Rationale:** Implements G-C10 BUILD_INTERVENTION_AND_ALERT_MODEL.md specification. Enforces "no automated intervention" principle with full audit trail. Critical safety mechanism.  
**Risks if kept:** None. This is a safety-critical component with proper audit.  
**Risks if dropped:** Would lose ability to safely stop builds with human authorization.  

### Build Control Panel UI (HTML/JS)
**Classification:** Adopt with constraints  
**Rationale:** Provides functional browser-based interface. However, UI is basic and may not align with final production UI framework decisions (React/Next.js vs vanilla JS). Useful for development/testing.  
**Constraints:** Mark as "development/testing UI only" until production UI framework is selected. Should not be considered the canonical production UI.  
**Risks if kept:** May create expectation that vanilla HTML/JS is the production UI approach.  
**Risks if dropped:** Would lose working UI for development/testing of backend APIs.  

### Inspector UI
**Classification:** Adopt with constraints  
**Rationale:** Same as Build Control Panel UI. Functional but may not represent final UI approach.  
**Constraints:** Mark as "development/testing UI only."  
**Risks if kept:** UI framework ambiguity.  
**Risks if dropped:** Would lose inspection UI for testing.  

### Intervention UI
**Classification:** Adopt with constraints  
**Rationale:** Same as Build Control Panel UI. Functional but may not represent final UI approach.  
**Constraints:** Mark as "development/testing UI only."  
**Risks if kept:** UI framework ambiguity.  
**Risks if dropped:** Would lose intervention UI for testing.  

---

## FM Runtime Components

### Watchdog Alert Reader
**Classification:** Adopt as-is  
**Rationale:** Implements essential runtime observability. Reads and parses watchdog alerts. Clean implementation with clear responsibilities.  
**Risks if kept:** None significant.  
**Risks if dropped:** Would lose watchdog alert integration capability.  

### Watchdog Escalation Reporter
**Classification:** Adopt as-is  
**Rationale:** Routes escalations to appropriate channels. Essential for runtime observability and human-in-the-loop escalation.  
**Risks if kept:** None significant.  
**Risks if dropped:** Would lose escalation reporting capability.  

---

## Foreman Runtime Components

### Program Manager
**Classification:** Adopt as-is  
**Rationale:** Core orchestration component managing program lifecycle. Implements status aggregation and progress tracking. Essential for Program/Wave/Task model.  
**Risks if kept:** None. Core component.  
**Risks if dropped:** Would lose program-level orchestration.  

### Task Manager
**Classification:** Adopt as-is  
**Rationale:** Core orchestration component managing task lifecycle and state transitions. Essential for task execution model.  
**Risks if kept:** None. Core component.  
**Risks if dropped:** Would lose task-level orchestration.  

### Blocker Manager
**Classification:** Adopt as-is  
**Rationale:** Manages blockers and detects blocked states. Essential for execution flow control and escalation.  
**Risks if kept:** None. Core component.  
**Risks if dropped:** Would lose blocker detection and management.  

### Notification Manager
**Classification:** Adopt as-is  
**Rationale:** Routes notifications to appropriate channels. Essential for observability and escalation.  
**Risks if kept:** None. Core component.  
**Risks if dropped:** Would lose notification routing capability.  

### Build Executor
**Classification:** Adopt as-is  
**Rationale:** Executes build operations based on orchestration decisions. Core execution component.  
**Risks if kept:** None. Core component.  
**Risks if dropped:** Would lose build execution capability.  

### Recovery Guide
**Classification:** Adopt as-is  
**Rationale:** Provides recovery guidance for failures. Supports recovery workflows.  
**Risks if kept:** None.  
**Risks if dropped:** Would lose recovery guidance capability.  

### Heartbeat Monitor
**Classification:** Adopt as-is  
**Rationale:** Monitors agent/builder heartbeats for liveness. Essential for detecting silent stalls (core FM problem).  
**Risks if kept:** None. Core observability component.  
**Risks if dropped:** Would lose liveness monitoring capability.  

### Stall Detector
**Classification:** Adopt as-is  
**Rationale:** Detects silent stalls in execution. Core FM capability addressing primary problem statement (burst platforms cannot detect stalls).  
**Risks if kept:** None. Core component.  
**Risks if dropped:** Would lose primary value proposition of FM.  

### Recovery Manager
**Classification:** Adopt as-is  
**Rationale:** Manages recovery from stalls and failures. Essential for resilient execution.  
**Risks if kept:** None. Core component.  
**Risks if dropped:** Would lose automated recovery capability.  

---

## Foreman Governance Components

### Task Completion Governance
**Classification:** Adopt as-is  
**Rationale:** Enforces task completion criteria. Core governance enforcement mechanism.  
**Risks if kept:** None. Governance-critical.  
**Risks if dropped:** Tasks could complete without proper validation.  

### QA Enforcement
**Classification:** Adopt as-is  
**Rationale:** Enforces QA policies and coverage requirements. Core governance enforcement mechanism.  
**Risks if kept:** None. Governance-critical.  
**Risks if dropped:** QA policies could be bypassed.  

### Memory Governance
**Classification:** Adopt as-is  
**Rationale:** Governs memory read/write operations. Ensures privacy and tenant isolation. Core governance mechanism.  
**Risks if kept:** None. Governance-critical.  
**Risks if dropped:** Memory operations could violate privacy/isolation rules.  

### Evidence Gate
**Classification:** Adopt as-is  
**Rationale:** Validates evidence requirements before progression. Core governance enforcement mechanism.  
**Risks if kept:** None. Governance-critical.  
**Risks if dropped:** Could progress without proper evidence.  

### Architecture Freeze
**Classification:** Adopt as-is  
**Rationale:** Enforces architecture freeze rules. Core governance enforcement mechanism.  
**Risks if kept:** None. Governance-critical.  
**Risks if dropped:** Architecture could be modified during frozen states.  

### CS2 Approval
**Classification:** Adopt as-is  
**Rationale:** Handles CS2 (Johan) approval workflows. Core human-in-the-loop mechanism.  
**Risks if kept:** None. Governance-critical.  
**Risks if dropped:** Would lose human approval workflow.  

### Audit Replay
**Classification:** Adopt as-is  
**Rationale:** Replays audit logs for governance validation. Essential for audit trail and determinism.  
**Risks if kept:** None. Audit-critical.  
**Risks if dropped:** Would lose audit replay capability.  

### Build State Governance
**Classification:** Adopt as-is  
**Rationale:** Governs build state transitions. Core governance enforcement mechanism.  
**Risks if kept:** None. Governance-critical.  
**Risks if dropped:** Build states could transition without proper validation.  

---

## Foreman Decision Components

### Completion Validator
**Classification:** Adopt as-is  
**Rationale:** Validates task/wave/program completion. Essential for progression logic.  
**Risks if kept:** None. Core component.  
**Risks if dropped:** Completion would not be validated.  

### Trace Recorder
**Classification:** Adopt as-is  
**Rationale:** Records decision traces for audit. Essential for audit trail and determinism.  
**Risks if kept:** None. Audit-critical.  
**Risks if dropped:** Would lose decision audit trail.  

### Trace Replayer
**Classification:** Adopt as-is  
**Rationale:** Replays decision traces for analysis. Essential for debugging and determinism verification.  
**Risks if kept:** None. Audit-critical.  
**Risks if dropped:** Would lose decision replay capability.  

### Task Decomposer
**Classification:** Adopt as-is  
**Rationale:** Decomposes high-level tasks into sub-tasks. Core orchestration logic.  
**Risks if kept:** None. Core component.  
**Risks if dropped:** Would lose task decomposition capability.  

### Recovery Strategy Selector
**Classification:** Adopt as-is  
**Rationale:** Selects appropriate recovery strategies. Essential for resilient execution.  
**Risks if kept:** None. Core component.  
**Risks if dropped:** Would lose recovery strategy selection.  

---

## Foreman Domain Components

### Domain Models (Program, Wave, Task, Blocker)
**Classification:** Adopt as-is  
**Rationale:** Core domain models representing the Program/Wave/Task hierarchy. Essential foundation for all orchestration logic.  
**Risks if kept:** None. These are fundamental models.  
**Risks if dropped:** Would require complete reimplementation of orchestration model.  

---

## Foreman Evidence Components

### Evidence Tracer
**Classification:** Adopt as-is  
**Rationale:** Traces evidence collection for audit. Essential for audit trail.  
**Risks if kept:** None. Audit-critical.  
**Risks if dropped:** Would lose evidence audit trail.  

### Evidence Schema Validator
**Classification:** Adopt as-is  
**Rationale:** Validates evidence against schemas. Essential for evidence integrity.  
**Risks if kept:** None. Governance-critical.  
**Risks if dropped:** Evidence could be invalid or incomplete.  

### Evidence Generator
**Classification:** Adopt as-is  
**Rationale:** Generates evidence artifacts. Essential for audit trail.  
**Risks if kept:** None. Audit-critical.  
**Risks if dropped:** Would lose evidence generation capability.  

---

## TypeScript/JavaScript Library Components

### TypeScript Memory Client
**Classification:** Adopt as-is  
**Rationale:** Provides memory fabric integration for TypeScript/JS applications. Well-structured with proper typing. Essential for Next.js/Vercel integration.  
**Risks if kept:** None. Clean, well-typed implementation.  
**Risks if dropped:** Would lose TypeScript memory integration.  

### Memory Store
**Classification:** Adopt as-is  
**Rationale:** Memory persistence and retrieval. Core memory infrastructure.  
**Risks if kept:** None. Core component.  
**Risks if dropped:** Would lose memory persistence.  

### Memory Dashboard
**Classification:** Adopt with constraints  
**Rationale:** Memory observability dashboard. May need UI framework alignment (same constraint as other UIs).  
**Constraints:** Mark as "development/testing only" if implemented in non-production UI framework.  
**Risks if kept:** UI framework ambiguity.  
**Risks if dropped:** Would lose memory observability UI.  

### Memory Health Monitor
**Classification:** Adopt as-is  
**Rationale:** Monitors memory fabric health. Essential for operational observability.  
**Risks if kept:** None. Core observability.  
**Risks if dropped:** Would lose memory health monitoring.  

### Memory Lifecycle Manager
**Classification:** Adopt as-is  
**Rationale:** Manages memory entry lifecycle. Core memory infrastructure.  
**Risks if kept:** None. Core component.  
**Risks if dropped:** Would lose memory lifecycle management.  

### Memory Observability Service
**Classification:** Adopt as-is  
**Rationale:** Observability for memory operations. Essential for operational visibility.  
**Risks if kept:** None. Core observability.  
**Risks if dropped:** Would lose memory observability.  

### Memory Observability Integration
**Classification:** Adopt as-is  
**Rationale:** Integrates memory with observability systems. Essential for platform observability.  
**Risks if kept:** None. Core integration.  
**Risks if dropped:** Would lose memory observability integration.  

### Memory Privacy Checker
**Classification:** Adopt as-is  
**Rationale:** Validates privacy rules for memory operations. Governance-critical for tenant isolation and privacy guardrails.  
**Risks if kept:** None. Governance-critical.  
**Risks if dropped:** Memory operations could violate privacy rules.  

### Memory Audit Logger
**Classification:** Adopt as-is  
**Rationale:** Logs memory operations for audit. Essential for audit trail and compliance.  
**Risks if kept:** None. Audit-critical.  
**Risks if dropped:** Would lose memory audit trail.  

### Memory Schema Validator
**Classification:** Adopt as-is  
**Rationale:** Validates memory entries against schemas. Essential for data integrity.  
**Risks if kept:** None. Core validation.  
**Risks if dropped:** Memory entries could be invalid.  

### Memory Runtime Loader
**Classification:** Adopt as-is  
**Rationale:** Loads memory at runtime. Essential for runtime memory access.  
**Risks if kept:** None. Core runtime component.  
**Risks if dropped:** Would lose runtime memory loading.  

### Commissioning Controller
**Classification:** Adopt as-is  
**Rationale:** Controls Foreman app commissioning lifecycle. Implements essential governance control - app cannot operate unless commissioned. Architecture-aligned implementation.  
**Risks if kept:** None. Governance-critical.  
**Risks if dropped:** App could operate without proper commissioning.  

### GitHub Model Routing
**Classification:** Adopt as-is  
**Rationale:** Routes GitHub operations to appropriate models. Integration utility.  
**Risks if kept:** None. Integration utility.  
**Risks if dropped:** Would lose GitHub routing capability.  

---

## Runtime Components

### Commissioning State Example
**Classification:** Adopt as-is  
**Rationale:** Example commissioning state structure. Provides reference implementation for commissioning state persistence.  
**Risks if kept:** None. Reference/example only.  
**Risks if dropped:** Would lose commissioning state reference.  

---

## Memory Components

### Tenant Memory Architecture
**Classification:** Adopt as-is  
**Rationale:** Architecture document for tenant-isolated memory. Essential governance specification.  
**Risks if kept:** None. Governance documentation.  
**Risks if dropped:** Would lose tenant isolation specification.  

### Memory Schemas
**Classification:** Adopt as-is  
**Rationale:** JSON schemas for memory structures. Essential for data validation and integrity.  
**Risks if kept:** None. Core schemas.  
**Risks if dropped:** Memory validation would fail.  

### Tenant Memory Simulation
**Classification:** Adopt with constraints  
**Rationale:** Simulation environment for tenant memory. Useful for testing but should be clearly marked as simulation-only.  
**Constraints:** Must be marked as "simulation/testing only" and never used with production data.  
**Risks if kept:** Could be confused with production environment.  
**Risks if dropped:** Would lose tenant memory testing capability.  

### Platform Memory
**Classification:** Adopt as-is  
**Rationale:** Platform-level memory events. Core memory infrastructure.  
**Risks if kept:** None. Core component.  
**Risks if dropped:** Would lose platform memory.  

### Foreman Memory
**Classification:** Adopt as-is  
**Rationale:** Foreman-specific memory entries (build events, governance events). Core memory infrastructure.  
**Risks if kept:** None. Core component.  
**Risks if dropped:** Would lose foreman memory.  

### Global Memory Seed
**Classification:** Adopt as-is  
**Rationale:** Seed memory entries for bootstrapping. Essential for system initialization.  
**Risks if kept:** None. Bootstrap infrastructure.  
**Risks if dropped:** System would lack seed memory.  

### Memory Authority Docs
**Classification:** Adopt as-is  
**Rationale:** Authority and policy documents for memory. Governance documentation.  
**Risks if kept:** None. Governance-critical.  
**Risks if dropped:** Memory authority would be unclear.  

---

## Scripts and Tooling

### Agent Context Sync Script
**Classification:** Adopt as-is  
**Rationale:** Syncs agent context with memory fabric. Essential integration utility.  
**Risks if kept:** None. Integration utility.  
**Risks if dropped:** Would lose agent-memory sync capability.  

### Reset Tenant Memory Script
**Classification:** Adopt with constraints  
**Rationale:** Resets tenant memory for testing. Useful testing utility but MUST be marked as testing-only with strong warnings.  
**Constraints:** Must include strong warnings, require confirmation, and be marked "TESTING ONLY - NEVER USE IN PRODUCTION."  
**Risks if kept:** Could accidentally delete production data if not properly protected.  
**Risks if dropped:** Would lose tenant memory reset capability for testing.  

---

## Testing Components

### Wave 0 Red QA Tests
**Classification:** Adopt as-is  
**Rationale:** Red QA tests for Wave 0 validation. Essential QA infrastructure implementing "Red QA" governance requirement.  
**Risks if kept:** None. QA-critical.  
**Risks if dropped:** Would lose Wave 0 QA validation.  

### Component-Level Tests
**Classification:** Adopt as-is  
**Rationale:** Tests for governance-memory sync, global memory runtime, watchdog runtime, build control API, build node inspector, build intervention, build authorization gate, memory proposals, CHP-memory integration, commissioning controller, memory lifecycle runtime. Essential QA coverage.  
**Risks if kept:** None. QA-critical.  
**Risks if dropped:** Components would be untested.  

### Builder Initialization
**Classification:** Adopt as-is  
**Rationale:** Initializes and validates builder agents. Core orchestration mechanism for builder management.  
**Risks if kept:** None. Core component.  
**Risks if dropped:** Builder initialization would be manual.  

---

## Root-Level Artifacts (Table C Evaluation)

### Root-Level Build Planning Scripts
**Classification:** Refactor later  
**Rationale:** These utilities work and provide value, but placement in root is non-standard. Should be moved to `scripts/` or `foreman/scripts/` in a future cleanup iteration.  
**Risks if kept:** Non-standard repository organization.  
**Risks if dropped:** Would lose build planning utilities.  

### Root-Level Build Status Generation Scripts
**Classification:** Refactor later  
**Rationale:** Same as build planning scripts. Work but need proper placement.  
**Risks if kept:** Non-standard repository organization.  
**Risks if dropped:** Would lose status generation utilities.  

### Root-Level Architecture Generation Scripts
**Classification:** Refactor later  
**Rationale:** May be bootstrap-only utilities. Should be moved to `scripts/bootstrap/` or similar.  
**Risks if kept:** Non-standard repository organization.  
**Risks if dropped:** Would lose architecture generation utilities.  

### Root-Level Validation Scripts
**Classification:** Refactor later  
**Rationale:** Should be in `scripts/` directory. Otherwise appear functional.  
**Risks if kept:** Non-standard repository organization.  
**Risks if dropped:** Would lose validation utilities.  

### Root-Level Build Plan/Status JSON Files
**Classification:** Deprecate  
**Rationale:** These appear to be execution artifacts (runtime state), not source code. Should be gitignored or moved to runtime/ directory.  
**Risks if kept:** Repository clutter, potential merge conflicts on execution artifacts.  
**Risks if dropped:** None if properly regenerated at runtime.  

### Root-Level Summary Documents (40+ files)
**Classification:** Refactor later  
**Rationale:** These appear to be historical completion/execution records. Valuable for audit trail but should be archived in `reports/` or `history/` directory to clean up root.  
**Risks if kept:** Severe repository clutter, difficult navigation.  
**Risks if dropped:** Would lose historical audit trail.  

### Empty or Minimal Files (uploads, empty .py files)
**Classification:** Deprecate  
**Rationale:** No functional value. Should be removed.  
**Risks if kept:** Repository clutter.  
**Risks if dropped:** None.  

### Root-Level package.json/package-lock.json
**Classification:** Adopt with constraints  
**Rationale:** Minimal npm configuration. Should be evaluated: is this for UI experiments, tooling, or production? If experimental, document clearly. If production, expand properly.  
**Constraints:** Document purpose clearly.  
**Risks if kept:** Unclear purpose.  
**Risks if dropped:** May break npm-based tooling.  

---

## Summary of Recommendations

### Adopt as-is (53 components)
Core orchestration, runtime, governance, decision, domain, evidence, memory, and testing components. These are production-ready and align with governance.

### Adopt with constraints (11 components)
- UI components (mark as dev/testing until production UI framework selected)
- Memory dashboard (same constraint)
- Tenant memory simulation (mark as testing-only)
- Reset tenant memory script (add strong warnings)
- Package.json (document purpose)

### Refactor later (6 categories)
- Root-level utility scripts (move to scripts/)
- Root-level summary documents (move to reports/history/)

### Deprecate (2 categories)
- Root-level build artifacts (gitignore or move to runtime/)
- Empty/minimal files (remove)

---

## Next Steps

These recommendations serve as input to **Phase 3: True North Architecture**, which will:
1. Explicitly adopt the 53 "adopt as-is" components as canonical
2. Document constraints for the 11 "adopt with constraints" components
3. Create a backlog for the 6 "refactor later" items (non-blocking)
4. Create a cleanup plan for the 2 "deprecate" categories

The True North architecture will freeze these decisions and establish them as the authoritative baseline.

---

**End of Phase 2 Recommendations**
