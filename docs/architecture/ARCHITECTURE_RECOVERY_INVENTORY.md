# FM App Architecture Recovery Inventory

**Version:** 1.0  
**Date:** 2025-12-29  
**Status:** Phase 1 Complete - Descriptive Inventory  
**Purpose:** Comprehensive inventory of all artifacts in the FM App repository  
**Authority:** Governance Agent (ARCH-RECOVERY-01)

---

## Overview

This document inventories all artifacts currently present in the FM App repository, categorized into:
- **Table A:** Implemented Artifacts (code, runtime systems, operational components)
- **Table B:** Designed but Not Implemented (specifications without corresponding code)
- **Table C:** Legacy / Experimental / Transitional (questionable or transitional items)

This is a **descriptive-only** document. No decisions, deletions, or refactors are made at this stage.

---

## Table A — Implemented Artifacts

Artifacts with working code, operational runtime systems, or functional implementations.

| Name | Location | Problem Solved | Apparent Scope |
|------|----------|----------------|----------------|
| Build Control API | `fm/orchestration/build_control_api.py` | Provides REST API for Build Control Panel UI, handles build execution requests | Orchestration / UI Backend |
| Build Authorization Gate | `fm/orchestration/build_authorization_gate.py` | Validates 8 mandatory preconditions before build can proceed | Orchestration / Governance Enforcement |
| Build Node Inspector | `fm/orchestration/build_node_inspector.py` | Provides inspection and drill-down for build nodes (Program/Wave/Task) | Orchestration / Inspection |
| Build Intervention Controller | `fm/orchestration/build_intervention.py` | Implements intervention controls with audit trail for build stops/alerts | Orchestration / Intervention |
| Build Control Panel UI | `fm/orchestration/static/` (index.html, app.js) | Browser-based UI for build control operations | UI / Orchestration Interface |
| Inspector UI | `fm/orchestration/static/` (inspector.html, inspector-app.js) | Browser-based UI for node inspection | UI / Inspection Interface |
| Intervention UI | `fm/orchestration/static/` (intervention.html, intervention-app.js) | Browser-based UI for intervention operations | UI / Intervention Interface |
| Watchdog Alert Reader | `fm/runtime/watchdog/alert_reader.py` | Reads and parses watchdog alerts from runtime | Runtime / Observability |
| Watchdog Escalation Reporter | `fm/runtime/watchdog/escalation_reporter.py` | Reports escalations from watchdog to appropriate channels | Runtime / Observability |
| Program Manager | `foreman/runtime/program_manager.py` | Manages programs, status aggregation, progress tracking | Orchestration / Lifecycle |
| Task Manager | `foreman/runtime/task_manager.py` | Manages task lifecycle, state transitions, assignments | Orchestration / Lifecycle |
| Blocker Manager | `foreman/runtime/blocker_manager.py` | Manages blockers, detects blocked states | Orchestration / Lifecycle |
| Notification Manager | `foreman/runtime/notification_manager.py` | Routes notifications to appropriate channels | Orchestration / Observability |
| Build Executor | `foreman/runtime/build_executor.py` | Executes build operations based on orchestration decisions | Orchestration / Execution |
| Recovery Guide | `foreman/runtime/recovery_guide.py` | Provides recovery guidance for failures | Orchestration / Recovery |
| Heartbeat Monitor | `foreman/runtime/liveness/heartbeat_monitor.py` | Monitors agent/builder heartbeats for liveness | Runtime / Observability |
| Stall Detector | `foreman/runtime/liveness/stall_detector.py` | Detects silent stalls in execution | Runtime / Observability |
| Recovery Manager | `foreman/runtime/liveness/recovery_manager.py` | Manages recovery from stalls and failures | Runtime / Recovery |
| Task Completion Governance | `foreman/governance/task_completion.py` | Enforces task completion criteria | Governance Enforcement |
| QA Enforcement | `foreman/governance/qa_enforcement.py` | Enforces QA policies and coverage requirements | Governance Enforcement |
| Memory Governance | `foreman/governance/memory.py` | Governs memory read/write operations | Governance Enforcement |
| Evidence Gate | `foreman/governance/evidence_gate.py` | Validates evidence requirements before progression | Governance Enforcement |
| Architecture Freeze | `foreman/governance/architecture_freeze.py` | Enforces architecture freeze rules | Governance Enforcement |
| CS2 Approval | `foreman/governance/cs2_approval.py` | Handles CS2 (Johan) approval workflows | Governance Enforcement |
| Audit Replay | `foreman/governance/audit_replay.py` | Replays audit logs for governance validation | Governance Enforcement |
| Build State Governance | `foreman/governance/build_state.py` | Governs build state transitions | Governance Enforcement |
| Completion Validator | `foreman/decision/completion_validator.py` | Validates task/wave/program completion | Decision Support |
| Trace Recorder | `foreman/decision/trace_recorder.py` | Records decision traces for audit | Decision Support |
| Trace Replayer | `foreman/decision/trace_replayer.py` | Replays decision traces for analysis | Decision Support |
| Task Decomposer | `foreman/decision/task_decomposer.py` | Decomposes high-level tasks into sub-tasks | Decision Support |
| Recovery Strategy Selector | `foreman/decision/recovery_strategy_selector.py` | Selects appropriate recovery strategies | Decision Support |
| Domain Models | `foreman/domain/` (program.py, wave.py, task.py, blocker.py) | Core domain models for Program/Wave/Task/Blocker | Domain / Data Models |
| Evidence Tracer | `foreman/evidence/tracer.py` | Traces evidence collection for audit | Evidence / Audit |
| Evidence Schema Validator | `foreman/evidence/schema_validator.py` | Validates evidence against schemas | Evidence / Validation |
| Evidence Generator | `foreman/evidence/generator.py` | Generates evidence artifacts | Evidence / Generation |
| TypeScript Memory Client | `lib/memory/client.ts` | Memory fabric integration for TypeScript/JS apps | Memory / Integration |
| Memory Store | `lib/memory/store.ts` | Memory persistence and retrieval | Memory / Storage |
| Memory Dashboard | `lib/memory/dashboard.ts` | Memory observability dashboard | Memory / UI |
| Memory Health Monitor | `lib/memory/health-monitor.ts` | Monitors memory fabric health | Memory / Observability |
| Memory Lifecycle Manager | `lib/memory/lifecycle-manager.ts` | Manages memory entry lifecycle | Memory / Lifecycle |
| Memory Observability Service | `lib/memory/observability-service.ts` | Observability for memory operations | Memory / Observability |
| Memory Observability Integration | `lib/memory/observability-integration.ts` | Integrates memory with observability systems | Memory / Integration |
| Memory Privacy Checker | `lib/memory/privacy-checker.ts` | Validates privacy rules for memory operations | Memory / Privacy |
| Memory Audit Logger | `lib/memory/audit-logger.ts` | Logs memory operations for audit | Memory / Audit |
| Memory Schema Validator | `lib/memory/schema-validator.ts` | Validates memory entries against schemas | Memory / Validation |
| Memory Runtime Loader | `lib/memory/runtime-loader.ts` | Loads memory at runtime | Memory / Runtime |
| Commissioning Controller | `lib/commissioning/CommissioningController.ts` | Controls Foreman app commissioning lifecycle | Lifecycle / Governance |
| GitHub Model Routing | `lib/github/model-routing.ts` | Routes GitHub operations to appropriate models | Integration / Tooling |
| Commissioning State | `runtime/commissioning/state.example.json` | Example commissioning state structure | Lifecycle / Configuration |
| Tenant Memory Architecture | `memory/TENANT_MEMORY_ARCHITECTURE.md` | Architecture for tenant-isolated memory | Memory / Architecture |
| Memory Schemas | `memory/schema/` (*.json) | JSON schemas for memory structures | Memory / Schemas |
| Tenant Memory Simulation | `memory/tenant/simulation/org-test-001/` | Simulation environment for tenant memory | Memory / Testing |
| Platform Memory | `memory/platform/runtime-events.json` | Platform-level memory events | Memory / Platform |
| Foreman Memory | `memory/foreman/` (build-events.json, governance-events.json) | Foreman-specific memory entries | Memory / Foreman |
| Global Memory Seed | `memory/global/seed-*.json` | Seed memory entries for bootstrapping | Memory / Bootstrap |
| Memory Authority Docs | `memory/AUTHORITY/` (*.md) | Authority and policy documents for memory | Memory / Governance |
| Agent Context Sync Script | `scripts/sync-agent-context.py` | Syncs agent context with memory fabric | Tooling / Integration |
| Reset Tenant Memory Script | `scripts/reset-tenant-memory.py` | Resets tenant memory for testing | Tooling / Testing |
| Wave 0 Red QA Tests | `tests/wave0_minimum_red/` (test_*.py) | Red QA tests for Wave 0 validation | QA / Testing |
| Governance Memory Sync Test | `tests/test_governance_memory_sync.py` | Tests governance-memory synchronization | QA / Testing |
| Global Memory Runtime Test | `tests/test_global_memory_runtime.py` | Tests global memory runtime integration | QA / Testing |
| Watchdog Runtime Test | `tests/test_watchdog_runtime.py` | Tests watchdog runtime components | QA / Testing |
| Build Control API Test | `tests/test_build_control_api.py` | Tests Build Control API endpoints | QA / Testing |
| Build Node Inspector Test | `tests/test_build_node_inspector.py` | Tests Build Node Inspector | QA / Testing |
| Build Intervention Test | `tests/test_build_intervention.py` | Tests Build Intervention Controller | QA / Testing |
| Build Authorization Gate Test | `tests/test_build_authorization_gate.py` | Tests Build Authorization Gate | QA / Testing |
| Memory Proposals Test | `tests/test_memory_proposals.py` | Tests memory proposal workflow | QA / Testing |
| CHP Memory Integration Test | `tests/test_chp_memory_integration.py` | Tests CHP-memory integration | QA / Testing |
| Commissioning Controller Test | `tests/test_commissioning_controller.py` | Tests Commissioning Controller | QA / Testing |
| Memory Lifecycle Runtime Test | `tests/test_memory_lifecycle_runtime.py` | Tests memory lifecycle at runtime | QA / Testing |
| Builder Initialization | `foreman/init_builders.py` | Initializes and validates builder agents | Orchestration / Initialization |

---

## Table B — Designed but Not Implemented

Specifications and design documents without corresponding implementation code.

| Name | Location | Intended Purpose |
|------|----------|------------------|
| FM Functional Spec | `docs/functional/FM_FUNCTIONAL_SPEC.md` | Complete functional specification for FM application |
| FM Functional Spec Governance Alignment | `docs/functional/FM_FUNCTIONAL_SPEC_GOVERNANCE_ALIGNMENT.md` | Alignment of functional spec with governance |
| FM Functional Spec V1.1.0 Change Summary | `docs/functional/FM_FUNCTIONAL_SPEC_V1.1.0_CHANGE_SUMMARY.md` | Change summary for v1.1.0 |
| FM App Description | `docs/governance/FM_APP_DESCRIPTION.md` | Canonical application description |
| Implementation Tracking | `docs/implementation/IMPLEMENTATION_STATUS_TRACKING.md` | Tracks implementation status across components |
| Implementation Document | `docs/implementation/implementation.md` | Implementation guidance and status |
| Runtime Architecture Docs | `docs/architecture/runtime/` (cognitive-hygiene/, memory/, observability/) | Runtime architecture specifications |
| Foreman Architecture v1.0 | `foreman/architecture/FOREMAN_ARCHITECTURE_v1.0.md` | Complete v1.0 architecture specification |
| Foreman Backend Spec v1.0 | `foreman/architecture/FOREMAN_BACKEND_SPEC_v1.0.md` | Backend specification |
| Foreman Database Schema v1.0 | `foreman/architecture/FOREMAN_DATABASE_SCHEMA_v1.0.md` | Database schema specification |
| Foreman Evidence Architecture v1.0 | `foreman/architecture/FOREMAN_EVIDENCE_ARCHITECTURE_v1.0.md` | Evidence architecture specification |
| Foreman Frontend Spec v1.0 | `foreman/architecture/FOREMAN_FRONTEND_SPEC_v1.0.md` | Frontend specification |
| Foreman Integration Spec v1.0 | `foreman/architecture/FOREMAN_INTEGRATION_SPEC_v1.0.md` | Integration specification |
| Foreman True North v1.0 | `foreman/architecture/FOREMAN_TRUE_NORTH_v1.0.md` | True North architecture document |
| Foreman Implementation Guide v1.0 | `foreman/architecture/FOREMAN_IMPLEMENTATION_GUIDE_v1.0.md` | Implementation guide |
| Foreman Sprint Plan v1.0 | `foreman/architecture/FOREMAN_SPRINT_PLAN_v1.0.md` | Sprint planning document |
| Foreman Versioning Strategy v1.0 | `foreman/architecture/FOREMAN_VERSIONING_STRATEGY_v1.0.md` | Versioning strategy |
| Foreman Wireframes v1.0 | `foreman/architecture/FOREMAN_WIREFRAMES_v1.0.md` | UI wireframes |
| Builder Specifications | `foreman/builder/` (api-builder-spec.md, ui-builder-spec.md, etc.) | Builder agent specifications |
| Builder Capability Map | `foreman/builder/builder-capability-map.json` | Maps builder capabilities |
| Builder Collaboration Rules | `foreman/builder/builder-collaboration-rules.md` | Rules for builder collaboration |
| Builder Permission Policy | `foreman/builder/builder-permission-policy.json` | Builder permissions |
| Build-to-Green Rule | `foreman/builder-specs/build-to-green-rule.md` | Build-to-green enforcement rule |
| QA Specifications | `foreman/qa/` (various QA specs) | QA system specifications |
| Compliance Specifications | `foreman/compliance/` (various compliance specs) | Compliance engine specifications |
| Platform Specifications | `foreman/platform/` (various platform specs) | Platform component specifications |
| Innovation Specifications | `foreman/innovation/` (various innovation specs) | Innovation system specifications |
| Admin Specifications | `foreman/admin/` (various admin specs) | Admin feature specifications |
| Survey Specifications | `foreman/survey/` (various survey specs) | Survey system specifications |
| Foreman Identity | `foreman/identity.md` | Foreman identity and role definition |
| Foreman Roles and Duties | `foreman/roles-and-duties.md` | Detailed roles and duties |
| Runtime Agent Plan | `foreman/runtime-agent-plan.md` | Runtime agent planning document |
| Memory Model | `foreman/memory-model.md` | Memory architecture model |
| Privacy Guardrails | `foreman/privacy-guardrails.md` | Privacy enforcement rules |
| Command Grammar | `foreman/command-grammar.md` | Command language grammar |
| Architecture Governance | `foreman/architecture-governance.md` | Architecture governance rules |
| Architecture Naming Conventions | `foreman/architecture-naming-conventions.md` | Naming conventions |
| Architecture Folder Structure | `foreman/architecture-folder-structure.md` | Folder structure standards |
| Architecture Validation Checklist | `foreman/architecture-validation-checklist.md` | Validation checklist |
| Architecture Standardisation Policy | `foreman/architecture-standardisation-policy.md` | Standardization policy |
| QA Governance | `foreman/qa-governance.md` | QA governance rules |
| QA Minimum Coverage Requirements | `foreman/qa-minimum-coverage-requirements.md` | Minimum QA coverage |
| QA of QA | `foreman/qa-of-qa.md` | Meta-QA specifications |
| Minimum Architecture Template | `foreman/minimum-architecture-template.md` | Template for architecture docs |
| Versioning Rules | `foreman/versioning-rules.md` | Version numbering rules |
| System Map | `foreman/system-map.md` | System component map |
| Task Distribution Rules | `foreman/task-distribution-rules.md` | Task distribution logic |
| Context Awareness | `foreman/context-awareness.md` | Context management rules |
| Platform Awareness | `foreman/platform-awareness.md` | Platform integration awareness |
| Change Management Spec | `foreman/change-management-spec.md` | Change management process |
| Foreman Execution Playbook | `foreman/FOREMAN_EXECUTION_PLAYBOOK.md` | Execution playbook |
| Foreman Execution Quick Reference | `foreman/FOREMAN_EXECUTION_QUICK_REFERENCE.md` | Quick reference guide |
| Builder Initialization | `foreman/BUILDER_INITIALIZATION.md` | Builder initialization guide |
| Builder Registry Quick Reference | `foreman/BUILDER_REGISTRY_QUICK_REFERENCE.md` | Builder registry reference |

---

## Table C — Legacy / Experimental / Transitional

Items that are questionable, transitional, or potentially legacy.

| Name | Location | Why Questionable/Transitional |
|------|----------|-------------------------------|
| Root-Level Build Planning Scripts | `plan-build.py`, `plan-build-wave-1.py`, `create-build-tasks.py`, `create-build-tasks-wave-1.py` | These appear to be build orchestration utilities that may belong in `scripts/` or `foreman/scripts/`. Root placement suggests experimental or bootstrap-only usage. |
| Root-Level Build Status Generation | `generate-build-status-wave-1.py`, `summarize-build-cycle.py`, `summarize-build-wave-1.py` | Status generation utilities in root. May be transitional reporting tools. |
| Root-Level Wave 1 Change Generator | `generate-wave1-change-records.py` | Wave-specific utility in root. Likely transitional. |
| Root-Level Architecture Generation Scripts | `bulk-generate-architecture.py`, `generate-arch-part1.py`, `generate-architecture-components.py` | Architecture generation utilities in root. May be bootstrap-only. |
| Root-Level Standardisation Script | `standardise-architecture.py` | Architecture standardization utility in root. May be transitional. |
| Root-Level Validation Scripts | `validate-repository.py`, `validate-build-wave-1.py` | Validation utilities in root. Should likely be in `scripts/`. |
| Root-Level Test Integration Script | `test-foreman-integration.py` | Test script in root rather than `tests/`. Placement is non-standard. |
| Root-Level Memory Initialization Script | `init-memory-fabric.py` | Memory initialization in root. May be bootstrap-only. |
| Root-Level Context Export Script | `export-runtime-context.py` | Context export utility in root. May be transitional. |
| Root-Level Governance Relocation Script | `relocate_governance.py` | One-time migration script. Likely legacy. |
| Root-Level Compliance Activation Script | `activate-compliance-engine.py` | Compliance activation in root. May be bootstrap-only. |
| Root-Level Architecture Indexing Script | `index-isms-architecture.py` | Architecture indexing in root. Should likely be in `scripts/`. |
| Root-Level Build Plan JSON Files | `build-plan.json`, `build-plan-wave-*.json`, `build-status.json`, `build-status-wave-*.json`, `build-tasks.json`, `build-tasks-wave-*.json` | Wave-specific build artifacts in root. Appears to be execution state, not source. May belong in runtime/ or be gitignored. |
| Root-Level Build Cycle Summary | `build-cycle-summary.json` | Build execution artifact in root. Should likely be gitignored or moved to runtime/. |
| Root-Level Standardisation Results | `standardisation_results.json` | Output artifact in root. Should likely be gitignored or in reports/. |
| Root-Level Architecture Index | `ARCHITECTURE_INDEX.json` | Generated artifact in root. Should likely be gitignored or in reports/. |
| Numerous Root-Level Summary Documents | `*_SUMMARY.md`, `*_COMPLETION_SUMMARY.md`, `*_REPORT.md`, `*_PROOF.md` (40+ files) | Large number of completion/summary documents in root. These appear to be historical execution records. Should likely be archived in reports/ or a history/ folder. |
| FM Governance Memory Sync Contract | `fm/governance/MEMORY_SYNC_CONTRACT.md` | Appears to be a specification in an implementation directory. Should specifications be in `docs/`? |
| FM Memory Build History | `fm/memory/build-history/`, `fm/memory/cost-efficiency/`, etc. | Memory subdirectories appear empty or contain operational data. Are these part of the design or runtime artifacts? |
| Foreman Test Scripts in foreman/ | `foreman/test-init-builders.py`, `foreman/scripts/` (test scripts) | Test scripts within the foreman/ specification directory. Should tests be in tests/? |
| Foreman AI Memory | `foreman/ai-memory/` | Contains reasoning patterns and historical issues. Is this operational memory or design artifacts? |
| Foreman Change Management | `foreman/change-management/` | Contains CR (Change Request) JSON files. Are these live operational records or design examples? |
| Builder Manifest JSON | `foreman/builder-manifest.json`, `foreman/builder-task-map.json` | JSON files in specification directory. Are these runtime or design artifacts? |
| Builder Registry Report | `foreman/builder-registry-report.md` | Report in specification directory. Should be in reports/? |
| Governance Policies | `governance/policies/` | Multiple policy documents. Some may overlap with foreman/ specifications. Potential duplication? |
| Governance Events | `governance/events/` | Event schemas. Should these be in foreman/ or remain separate? |
| Maturion ISMS Directory | `maturion-isms/` | Entire directory structure. Purpose unclear. Is this a submodule, external dependency, or legacy? |
| Python Agent Directory | `python_agent/` | Directory purpose unclear. Is this a custom agent implementation or legacy? |
| Examples Directory | `examples/` | Contains example code. Are these current or legacy? |
| Uploads File | `uploads` | Single-byte file. Likely artifact. Should be gitignored. |
| Empty generate-architecture-components.py | `generate-architecture-components.py` (0 bytes) | Empty file. Should be removed. |
| package.json and package-lock.json | Root-level npm files | Minimal content. Are these for a specific purpose or legacy from UI experiments? |

---

## Inventory Summary

### Counts
- **Implemented Artifacts (Table A):** 69 items
- **Designed but Not Implemented (Table B):** 60+ items
- **Legacy / Experimental / Transitional (Table C):** 40+ items

### Key Observations

1. **Strong Implementation in Core Areas:**
   - FM Orchestration (API, Gate, Inspector, Intervention) is fully implemented
   - Foreman Runtime (Program/Task/Blocker Management, Liveness) is fully implemented
   - Governance Enforcement (Task Completion, QA, Memory, Evidence) is fully implemented
   - Memory Fabric (TypeScript client, store, observability, privacy) is fully implemented
   - Commissioning Lifecycle is implemented

2. **Rich Specification Library:**
   - Comprehensive architecture and specification documents exist in `foreman/`
   - Builder, QA, Compliance, Platform, Innovation, Admin, Survey specs are detailed
   - Functional specifications exist in `docs/functional/`

3. **Significant Root-Level Clutter:**
   - 40+ summary/completion/report documents in root
   - Multiple utility scripts in root (should be in scripts/)
   - Build artifacts (JSON files) in root (should be gitignored or in runtime/)
   - Empty or minimal files

4. **Unclear Boundaries:**
   - Some specifications exist in implementation directories (e.g., `fm/governance/MEMORY_SYNC_CONTRACT.md`)
   - Some tests exist in specification directories (e.g., `foreman/test-init-builders.py`)
   - Potential duplication between `governance/policies/` and `foreman/` specifications

5. **Memory Implementation is Mature:**
   - Complete TypeScript memory client with observability, privacy, audit
   - Tenant memory architecture and simulation
   - Memory schemas and authority policies

6. **Testing is Present:**
   - Wave 0 Red QA tests exist
   - Component-level tests for orchestration, memory, commissioning exist
   - Integration tests exist

---

## Next Steps

This inventory serves as input to **Phase 2: Classification & Recommendation**, where each implemented artifact will be evaluated for:
- Adopt as-is
- Adopt with constraints
- Refactor later
- Deprecate

Phase 2 will provide governance rationale and risk assessment for each decision.

---

**End of Phase 1 Inventory**
