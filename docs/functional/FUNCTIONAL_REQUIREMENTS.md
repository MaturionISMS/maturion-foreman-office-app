# FM App Functional Requirements

**Version:** 1.0  
**Date:** 2025-12-29  
**Status:** Derived from Frozen Architecture  
**Authority:** Governance Agent (ARCH-RECOVERY-01) - Pending Johan Approval  
**Derivation:** TRUE_NORTH_FM_ARCHITECTURE.md v1.0

---

## Document Authority and Derivation

This document is **derived from** the frozen True North FM Architecture (docs/architecture/TRUE_NORTH_FM_ARCHITECTURE.md).

**Constitutional Hierarchy:**
```
Governance Repository (Constitutional Authority)
    ↓
BUILD_PHILOSOPHY.md (Supreme Build Authority)
    ↓
APP_DESCRIPTION.md (Authoritative Product Intent)
    ↓
TRUE_NORTH_FM_ARCHITECTURE.md (Frozen Architecture)
    ↓
FUNCTIONAL_REQUIREMENTS.md (THIS DOCUMENT - Derived Requirements)
    ↓
Implementation (Governed by requirements and architecture)
```

**Rules:**
- Requirements MUST align with frozen architecture
- Requirements MAY NOT contradict architecture
- Requirements serve as testable specifications of architecture

---

## FR-1: Orchestration Requirements

### FR-1.1: Build Control API
**Source:** TRUE_NORTH Section 3.1  
**Requirement:** FM App MUST provide a REST API for orchestration operations  
**Components:** `fm/orchestration/build_control_api.py`  
**Acceptance:**
- API provides endpoints for build control operations
- API supports CORS for local development
- API integrates with Build Authorization Gate
- API serves UI assets

**Priority:** CRITICAL  
**Status:** IMPLEMENTED

### FR-1.2: Build Authorization Gate
**Source:** TRUE_NORTH Section 3.1  
**Requirement:** FM App MUST validate 8 mandatory preconditions before ANY build execution  
**Components:** `fm/orchestration/build_authorization_gate.py`  
**Acceptance:**
- Gate validates all 8 preconditions
- Gate returns PASS or FAIL (binary)
- Gate provides evidence paths for each precondition
- Gate blocks execution on FAIL
- Gate never auto-approves

**Priority:** CRITICAL  
**Status:** IMPLEMENTED

**8 Mandatory Preconditions:**
1. Architecture exists and is frozen
2. QA design exists and is complete
3. Red QA tests exist and define failure
4. Governance rules are loaded and valid
5. Builder agents are initialized and ready
6. Evidence collection is configured
7. Memory fabric is operational
8. Human authority (Johan) has approved this specific build

**End-to-End Testing Requirements (Issue #68 - C1):**
- **E2E Governance Gate Dry Run:** Before Wave 0 build execution, an end-to-end dry run of the Build Authorization Gate must be performed to validate:
  - All 8 preconditions can be checked programmatically
  - Gate correctly returns PASS when all preconditions are satisfied
  - Gate correctly returns FAIL when any precondition is not satisfied
  - Evidence paths are valid and accessible for each precondition
  - Gate behavior is deterministic and repeatable
- **Integration Testing:** Gate must be tested in integration with:
  - Build orchestration system (validates gate is consulted before build start)
  - Evidence collection system (validates evidence paths are correct)
  - Memory fabric (validates memory operational check works)
  - Agent initialization system (validates agent readiness check works)
- **Failure Mode Testing:** Gate must be tested with intentionally failing preconditions:
  - Missing architecture document (precondition 1 fails)
  - Invalid governance rules (precondition 4 fails)
  - Agents not initialized (precondition 5 fails)
  - Missing human approval (precondition 8 fails)
  - Verify gate produces clear failure reasons for each case
- **No Auto-Approve Testing:** Gate must be tested to ensure it never auto-approves:
  - Test with partial precondition satisfaction
  - Test with cached/stale approval state
  - Verify gate always performs fresh validation
- **Performance Requirements:** Gate validation must complete within reasonable time:
  - Full gate check completes in < 30 seconds
  - Individual precondition checks complete in < 5 seconds each
  - Gate does not block on external dependencies (timeouts configured)

### FR-1.3: Build Node Inspector
**Source:** TRUE_NORTH Section 3.1  
**Requirement:** FM App MUST provide inspection capabilities for Program/Wave/Task nodes  
**Components:** `fm/orchestration/build_node_inspector.py`  
**Acceptance:**
- Inspector provides "no status without explanation" (G-C9)
- Inspector supports Program, Wave, Task node types
- Inspector provides configurable depth
- Inspector includes children when requested
- Inspector is read-only (no state changes)

**Priority:** HIGH  
**Status:** IMPLEMENTED

### FR-1.4: Build Intervention Controller
**Source:** TRUE_NORTH Section 3.1  
**Requirement:** FM App MUST provide safe human intervention with full audit trail  
**Components:** `fm/orchestration/build_intervention.py`  
**Acceptance:**
- Intervention requires explicit human decision (no automation)
- Stop operations require rationale (min 50 chars)
- Alert operations require rationale (min 20 chars)
- All interventions create audit log
- Resumption requires explicit authorization
- Intervention scope levels: step, sub-wave, wave, application

**Priority:** CRITICAL  
**Status:** IMPLEMENTED

### FR-1.5: Development UI
**Source:** TRUE_NORTH Section 3.1  
**Requirement:** FM App SHOULD provide browser-based UI for development/testing  
**Components:** `fm/orchestration/static/`  
**Acceptance:**
- UI supports build control operations
- UI supports node inspection
- UI supports intervention operations
- UI is marked as DEV/TEST ONLY
- UI does not represent canonical production UI framework

**Priority:** MEDIUM  
**Status:** IMPLEMENTED (DEV/TEST ONLY)

---

## FR-2: Runtime and Liveness Requirements

### FR-2.1: Watchdog Alert Reader
**Source:** TRUE_NORTH Section 3.2  
**Requirement:** FM App MUST read and parse watchdog alerts from runtime  
**Components:** `fm/runtime/watchdog/alert_reader.py`  
**Acceptance:**
- Reader parses alert messages
- Reader extracts alert metadata
- Reader validates alert format

**Priority:** HIGH  
**Status:** IMPLEMENTED

### FR-2.2: Watchdog Escalation Reporter
**Source:** TRUE_NORTH Section 3.2  
**Requirement:** FM App MUST report escalations to appropriate channels  
**Components:** `fm/runtime/watchdog/escalation_reporter.py`  
**Acceptance:**
- Reporter routes escalations by severity
- Reporter includes full context
- Reporter logs all escalations

**Priority:** HIGH  
**Status:** IMPLEMENTED

### FR-2.3: Heartbeat Monitoring
**Source:** TRUE_NORTH Section 3.4  
**Requirement:** FM App MUST monitor agent/builder heartbeats to detect liveness  
**Components:** `foreman/runtime/liveness/heartbeat_monitor.py`  
**Acceptance:**
- Monitor tracks heartbeat timestamps
- Monitor detects missing heartbeats within threshold
- Monitor distinguishes between agents/builders

**Priority:** CRITICAL  
**Status:** IMPLEMENTED

### FR-2.4: Stall Detection
**Source:** TRUE_NORTH Section 3.4  
**Requirement:** FM App MUST detect silent stalls in execution (core value proposition)  
**Components:** `foreman/runtime/liveness/stall_detector.py`  
**Acceptance:**
- Detector identifies prolonged silence
- Detector escalates on stall detection
- Detector treats "no update" as CRITICAL signal
- Detector configurable stall threshold

**Priority:** CRITICAL  
**Status:** IMPLEMENTED

### FR-2.5: Recovery Management
**Source:** TRUE_NORTH Section 3.4  
**Requirement:** FM App MUST provide recovery strategies for stalls and failures  
**Components:** `foreman/runtime/liveness/recovery_manager.py`  
**Acceptance:**
- Manager provides recovery strategy recommendations
- Manager tracks recovery attempts
- Manager escalates on repeated failures

**Priority:** HIGH  
**Status:** IMPLEMENTED

---

## FR-3: Orchestration Engine Requirements

### FR-3.1: Program Management
**Source:** TRUE_NORTH Section 3.3  
**Requirement:** FM App MUST manage Program lifecycle and status aggregation  
**Components:** `foreman/runtime/program_manager.py`  
**Acceptance:**
- Manager maintains Program registry
- Manager aggregates status from Wave → Task hierarchy
- Manager tracks progress
- Manager detects program-level failures

**Priority:** CRITICAL  
**Status:** IMPLEMENTED

### FR-3.2: Task Management
**Source:** TRUE_NORTH Section 3.3  
**Requirement:** FM App MUST manage Task lifecycle and state transitions  
**Components:** `foreman/runtime/task_manager.py`  
**Acceptance:**
- Manager maintains Task registry
- Manager validates state transitions
- Manager assigns tasks to builders
- Manager tracks task history

**Priority:** CRITICAL  
**Status:** IMPLEMENTED

### FR-3.3: Blocker Management
**Source:** TRUE_NORTH Section 3.3  
**Requirement:** FM App MUST manage blockers and detect blocked states  
**Components:** `foreman/runtime/blocker_manager.py`  
**Acceptance:**
- Manager classifies blockers (transient vs permanent)
- Manager detects blocked tasks
- Manager escalates unresolved blockers
- Manager tracks blocker resolution

**Priority:** CRITICAL  
**Status:** IMPLEMENTED

### FR-3.4: Notification Routing
**Source:** TRUE_NORTH Section 3.3  
**Requirement:** FM App MUST route notifications to appropriate channels  
**Components:** `foreman/runtime/notification_manager.py`  
**Acceptance:**
- Manager routes by notification type
- Manager routes by severity
- Manager logs all notifications

**Priority:** HIGH  
**Status:** IMPLEMENTED

### FR-3.5: Build Execution
**Source:** TRUE_NORTH Section 3.3  
**Requirement:** FM App MUST execute build operations based on orchestration decisions  
**Components:** `foreman/runtime/build_executor.py`  
**Acceptance:**
- Executor follows orchestration decisions
- Executor validates preconditions
- Executor logs all executions
- Executor handles execution failures

**Priority:** CRITICAL  
**Status:** IMPLEMENTED

### FR-3.6: Recovery Guidance
**Source:** TRUE_NORTH Section 3.3  
**Requirement:** FM App SHOULD provide recovery guidance for failures  
**Components:** `foreman/runtime/recovery_guide.py`  
**Acceptance:**
- Guide provides context-appropriate recovery steps
- Guide includes rationale
- Guide includes risk assessment

**Priority:** MEDIUM  
**Status:** IMPLEMENTED

---

## FR-4: Governance Enforcement Requirements

### FR-4.1: Task Completion Governance
**Source:** TRUE_NORTH Section 3.5  
**Requirement:** FM App MUST enforce task completion criteria  
**Components:** `foreman/governance/task_completion.py`  
**Acceptance:**
- Enforcer validates completion criteria
- Enforcer blocks progression on incomplete tasks
- Enforcer validates evidence exists
- Enforcer is non-negotiable (constitutional)

**Priority:** CRITICAL  
**Status:** IMPLEMENTED

### FR-4.2: QA Enforcement
**Source:** TRUE_NORTH Section 3.5  
**Requirement:** FM App MUST enforce QA policies and coverage requirements  
**Components:** `foreman/governance/qa_enforcement.py`  
**Acceptance:**
- Enforcer validates QA coverage
- Enforcer validates Red QA passes
- Enforcer blocks builds on QA failures
- Enforcer never allows partial QA passes

**Priority:** CRITICAL  
**Status:** IMPLEMENTED

### FR-4.3: Memory Governance
**Source:** TRUE_NORTH Section 3.5  
**Requirement:** FM App MUST govern memory read/write operations with privacy enforcement  
**Components:** `foreman/governance/memory.py`  
**Acceptance:**
- Governance validates tenant isolation
- Governance validates privacy rules
- Governance blocks cross-tenant access
- Governance requires approval for writes

**Priority:** CRITICAL  
**Status:** IMPLEMENTED

### FR-4.4: Evidence Gate
**Source:** TRUE_NORTH Section 3.5  
**Requirement:** FM App MUST validate evidence requirements before progression  
**Components:** `foreman/governance/evidence_gate.py`  
**Acceptance:**
- Gate validates evidence exists
- Gate validates evidence is complete
- Gate validates evidence is schema-valid
- Gate blocks progression on missing evidence

**Priority:** CRITICAL  
**Status:** IMPLEMENTED

### FR-4.5: Architecture Freeze Enforcement
**Source:** TRUE_NORTH Section 3.5  
**Requirement:** FM App MUST enforce architecture freeze rules  
**Components:** `foreman/governance/architecture_freeze.py`  
**Acceptance:**
- Enforcer detects architecture modifications during freeze
- Enforcer blocks changes during freeze
- Enforcer validates architecture integrity

**Priority:** CRITICAL  
**Status:** IMPLEMENTED

### FR-4.6: CS2 Approval Workflow
**Source:** TRUE_NORTH Section 3.5  
**Requirement:** FM App MUST handle Johan (CS2) approval workflows  
**Components:** `foreman/governance/cs2_approval.py`  
**Acceptance:**
- Workflow presents decisions to Johan
- Workflow supports Approve, Deny, Approve with changes
- Workflow logs all decisions
- Workflow enforces approval requirement

**Priority:** CRITICAL  
**Status:** IMPLEMENTED

### FR-4.7: Audit Replay
**Source:** TRUE_NORTH Section 3.5  
**Requirement:** FM App MUST replay audit logs for governance validation  
**Components:** `foreman/governance/audit_replay.py`  
**Acceptance:**
- Replayer loads audit logs
- Replayer validates governance decisions
- Replayer detects governance violations
- Replayer is deterministic

**Priority:** HIGH  
**Status:** IMPLEMENTED

### FR-4.8: Build State Governance
**Source:** TRUE_NORTH Section 3.5  
**Requirement:** FM App MUST govern build state transitions  
**Components:** `foreman/governance/build_state.py`  
**Acceptance:**
- Governance validates state transitions
- Governance blocks invalid transitions
- Governance logs all transitions

**Priority:** CRITICAL  
**Status:** IMPLEMENTED

### FR-4.9: Governance Supremacy
**Source:** APP_DESCRIPTION Section 4  
**Requirement:** All governance rules MUST be constitutional (not advisory)  
**Acceptance:**
- Governance violations halt or escalate (no silent continuation)
- Governance is never weakened to proceed
- Governance is read-only at runtime
- Governance violations are logged

**Priority:** CRITICAL  
**Status:** ENFORCED BY ARCHITECTURE

---

## FR-5: Decision Support Requirements

### FR-5.1: Completion Validation
**Source:** TRUE_NORTH Section 3.6  
**Requirement:** FM App MUST validate task/wave/program completion  
**Components:** `foreman/decision/completion_validator.py`  
**Acceptance:**
- Validator checks completion criteria
- Validator validates dependencies
- Validator validates evidence
- Validator validates QA

**Priority:** CRITICAL  
**Status:** IMPLEMENTED

### FR-5.2: Decision Tracing
**Source:** TRUE_NORTH Section 3.6  
**Requirement:** FM App MUST record all decisions for audit trail  
**Components:** `foreman/decision/trace_recorder.py`  
**Acceptance:**
- Recorder captures decision context
- Recorder captures decision rationale
- Recorder captures decision outcome
- Recorder timestamps all entries

**Priority:** CRITICAL  
**Status:** IMPLEMENTED

### FR-5.3: Decision Replay
**Source:** TRUE_NORTH Section 3.6  
**Requirement:** FM App MUST replay decision traces for analysis  
**Components:** `foreman/decision/trace_replayer.py`  
**Acceptance:**
- Replayer loads decision traces
- Replayer validates determinism
- Replayer detects divergence

**Priority:** HIGH  
**Status:** IMPLEMENTED

### FR-5.4: Task Decomposition
**Source:** TRUE_NORTH Section 3.6  
**Requirement:** FM App MUST decompose high-level tasks into sub-tasks  
**Components:** `foreman/decision/task_decomposer.py`  
**Acceptance:**
- Decomposer respects governance constraints
- Decomposer validates dependencies
- Decomposer creates valid task hierarchy

**Priority:** HIGH  
**Status:** IMPLEMENTED

### FR-5.5: Recovery Strategy Selection
**Source:** TRUE_NORTH Section 3.6  
**Requirement:** FM App MUST select appropriate recovery strategies  
**Components:** `foreman/decision/recovery_strategy_selector.py`  
**Acceptance:**
- Selector analyzes failure context
- Selector provides strategy recommendations
- Selector considers past success/failure

**Priority:** HIGH  
**Status:** IMPLEMENTED

---

## FR-6: Domain Model Requirements

### FR-6.1: Program/Wave/Task Hierarchy
**Source:** TRUE_NORTH Section 3.7  
**Requirement:** FM App MUST support Program → Wave → Task hierarchy  
**Components:** `foreman/domain/program.py`, `foreman/domain/wave.py`, `foreman/domain/task.py`  
**Acceptance:**
- Program contains Waves
- Wave contains Tasks
- All models support state transitions
- All models support status tracking

**Priority:** CRITICAL  
**Status:** IMPLEMENTED

### FR-6.2: Blocker Model
**Source:** TRUE_NORTH Section 3.7  
**Requirement:** FM App MUST support Blocker model for execution impediments  
**Components:** `foreman/domain/blocker.py`  
**Acceptance:**
- Blocker captures impediment details
- Blocker classifies (transient vs permanent)
- Blocker tracks resolution

**Priority:** HIGH  
**Status:** IMPLEMENTED

---

## FR-7: Evidence Requirements

### FR-7.1: Evidence Tracing
**Source:** TRUE_NORTH Section 3.8  
**Requirement:** FM App MUST trace evidence collection for audit  
**Components:** `foreman/evidence/tracer.py`  
**Acceptance:**
- Tracer captures evidence source
- Tracer timestamps evidence
- Tracer validates evidence chain

**Priority:** CRITICAL  
**Status:** IMPLEMENTED

### FR-7.2: Evidence Schema Validation
**Source:** TRUE_NORTH Section 3.8  
**Requirement:** FM App MUST validate all evidence against schemas  
**Components:** `foreman/evidence/schema_validator.py`  
**Acceptance:**
- Validator loads evidence schemas
- Validator validates evidence structure
- Validator rejects invalid evidence

**Priority:** CRITICAL  
**Status:** IMPLEMENTED

### FR-7.3: Evidence Generation
**Source:** TRUE_NORTH Section 3.8  
**Requirement:** FM App MUST generate evidence artifacts  
**Components:** `foreman/evidence/generator.py`  
**Acceptance:**
- Generator creates evidence in standard format
- Generator includes metadata
- Generator is immutable after generation

**Priority:** CRITICAL  
**Status:** IMPLEMENTED

---

## FR-8: Memory Fabric Requirements

### FR-8.1: TypeScript Memory Client
**Source:** TRUE_NORTH Section 3.9  
**Requirement:** FM App MUST provide TypeScript/JavaScript memory client  
**Components:** `lib/memory/client.ts`  
**Acceptance:**
- Client loads memory entries
- Client proposes memory writes (not automatic)
- Client validates memory structure
- Client supports scopes (global, foreman, tenant, etc.)

**Priority:** CRITICAL  
**Status:** IMPLEMENTED

### FR-8.2: Memory Persistence
**Source:** TRUE_NORTH Section 3.9  
**Requirement:** FM App MUST persist and retrieve memory entries  
**Components:** `lib/memory/store.ts`  
**Acceptance:**
- Store persists to filesystem/database
- Store retrieves by scope/tag/importance
- Store validates schema before persistence

**Priority:** CRITICAL  
**Status:** IMPLEMENTED

### FR-8.3: Memory Health Monitoring
**Source:** TRUE_NORTH Section 3.9  
**Requirement:** FM App MUST monitor memory fabric health  
**Components:** `lib/memory/health-monitor.ts`  
**Acceptance:**
- Monitor checks memory availability
- Monitor validates memory integrity
- Monitor reports health status

**Priority:** HIGH  
**Status:** IMPLEMENTED

### FR-8.4: Memory Lifecycle Management
**Source:** TRUE_NORTH Section 3.9  
**Requirement:** FM App MUST manage memory entry lifecycle  
**Components:** `lib/memory/lifecycle-manager.ts`  
**Acceptance:**
- Manager handles entry creation
- Manager handles entry expiration
- Manager handles entry archival

**Priority:** HIGH  
**Status:** IMPLEMENTED

### FR-8.5: Memory Privacy Enforcement
**Source:** TRUE_NORTH Section 3.9  
**Requirement:** FM App MUST enforce privacy rules for memory operations (tenant isolation)  
**Components:** `lib/memory/privacy-checker.ts`  
**Acceptance:**
- Checker validates tenant isolation
- Checker blocks cross-tenant access
- Checker enforces privacy guardrails
- Checker logs privacy violations

**Priority:** CRITICAL  
**Status:** IMPLEMENTED

### FR-8.6: Memory Audit Logging
**Source:** TRUE_NORTH Section 3.9  
**Requirement:** FM App MUST log all memory operations for audit  
**Components:** `lib/memory/audit-logger.ts`  
**Acceptance:**
- Logger captures read operations
- Logger captures write proposals
- Logger captures privacy checks
- Logger timestamps all entries

**Priority:** CRITICAL  
**Status:** IMPLEMENTED

### FR-8.7: Memory Schema Validation
**Source:** TRUE_NORTH Section 3.9  
**Requirement:** FM App MUST validate all memory entries against schemas  
**Components:** `lib/memory/schema-validator.ts`  
**Acceptance:**
- Validator loads memory schemas
- Validator validates entry structure
- Validator rejects invalid entries

**Priority:** CRITICAL  
**Status:** IMPLEMENTED

### FR-8.8: Memory Runtime Loading
**Source:** TRUE_NORTH Section 3.9  
**Requirement:** FM App MUST load memory at runtime  
**Components:** `lib/memory/runtime-loader.ts`  
**Acceptance:**
- Loader loads memory on app start
- Loader refreshes memory periodically
- Loader validates memory integrity

**Priority:** HIGH  
**Status:** IMPLEMENTED

### FR-8.9: Memory Observability
**Source:** TRUE_NORTH Section 3.9  
**Requirement:** FM App MUST provide observability for memory operations  
**Components:** `lib/memory/observability-service.ts`, `lib/memory/observability-integration.ts`  
**Acceptance:**
- Service tracks memory metrics
- Service exposes memory health
- Integration connects to observability systems

**Priority:** MEDIUM  
**Status:** IMPLEMENTED

### FR-8.10: Memory Write Proposal Workflow
**Source:** TRUE_NORTH Section 7.3  
**Requirement:** All memory writes MUST be proposals, not automatic  
**Acceptance:**
- Writes create proposals
- Proposals require approval
- Proposals are audited
- Approved proposals become memory

**Priority:** CRITICAL  
**Status:** IMPLEMENTED

---

## FR-9: Commissioning Requirements

### FR-9.1: Commissioning Lifecycle
**Source:** TRUE_NORTH Section 3.10, Section 7.1  
**Requirement:** FM App MUST control commissioning lifecycle  
**Components:** `lib/commissioning/CommissioningController.ts`  
**Acceptance:**
- Controller enforces lifecycle: NOT_COMMISSIONED → COMMISSIONING → COMMISSIONED → ACTIVE → SUSPENDED
- App MUST NOT operate in NOT_COMMISSIONED state
- State transitions require explicit authorization
- State transitions are audited

**Priority:** CRITICAL  
**Status:** IMPLEMENTED

### FR-9.2: Commissioning State Persistence
**Source:** TRUE_NORTH Section 3.10  
**Requirement:** FM App MUST persist commissioning state  
**Components:** `runtime/commissioning/state.example.json`  
**Acceptance:**
- State persists across app restarts
- State includes metadata (timestamp, authority)
- State validates on load

**Priority:** HIGH  
**Status:** IMPLEMENTED

---

## FR-10: Testing and QA Requirements

### FR-10.1: Wave 0 Red QA
**Source:** TRUE_NORTH Section 4  
**Requirement:** FM App MUST pass Wave 0 Red QA tests before progression  
**Components:** `tests/wave0_minimum_red/`  
**Acceptance:**
- Red QA tests define failure (not success)
- Red QA tests validate governance
- Red QA tests validate liveness
- Red QA tests validate evidence
- Red QA tests validate decision determinism

**Priority:** CRITICAL  
**Status:** IMPLEMENTED

### FR-10.2: Component Test Coverage
**Source:** TRUE_NORTH Section 4  
**Requirement:** All canonical components MUST have test coverage  
**Components:** `tests/test_*.py`  
**Acceptance:**
- Tests cover all canonical components
- Tests validate expected behavior
- Tests validate error handling
- Tests validate governance enforcement

**Priority:** CRITICAL  
**Status:** IMPLEMENTED

### FR-10.3: Negative Testing
**Source:** TRUE_NORTH Section 4  
**Requirement:** Governance violations MUST be tested (negative tests)  
**Acceptance:**
- Tests attempt to violate governance
- Tests verify violations are blocked
- Tests verify violations are logged

**Priority:** HIGH  
**Status:** IMPLEMENTED

---

## FR-11: Integration and Tooling Requirements

### FR-11.1: Agent Context Sync
**Source:** TRUE_NORTH Section 3.12  
**Requirement:** FM App SHOULD sync agent context with memory fabric  
**Components:** `scripts/sync-agent-context.py`  
**Acceptance:**
- Script loads memory
- Script exports context for agents
- Script validates sync integrity

**Priority:** MEDIUM  
**Status:** IMPLEMENTED

### FR-11.2: GitHub Model Routing
**Source:** TRUE_NORTH Section 3.12  
**Requirement:** FM App SHOULD route GitHub operations to appropriate models  
**Components:** `lib/github/model-routing.ts`  
**Acceptance:**
- Router selects appropriate GitHub model
- Router handles routing errors

**Priority:** LOW  
**Status:** IMPLEMENTED

### FR-11.3: Testing Utilities
**Source:** TRUE_NORTH Section 3.12  
**Requirement:** FM App SHOULD provide testing utilities with strong warnings  
**Components:** `scripts/reset-tenant-memory.py`  
**Acceptance:**
- Utilities marked "TESTING ONLY"
- Utilities require confirmation
- Utilities include strong warnings
- Utilities NEVER used in production

**Priority:** MEDIUM  
**Status:** IMPLEMENTED

### FR-11.4: Builder Initialization
**Source:** TRUE_NORTH Section 3.13  
**Requirement:** FM App MUST initialize and validate builder agents  
**Components:** `foreman/init_builders.py`  
**Acceptance:**
- Initialization validates builder capabilities
- Initialization enforces builder permissions
- Initialization logs builder status

**Priority:** HIGH  
**Status:** IMPLEMENTED

---

## FR-12: Non-Functional Requirements

### FR-12.1: Zero Regression
**Source:** BUILD_PHILOSOPHY  
**Requirement:** FM App MUST maintain zero regression across updates  
**Acceptance:**
- All existing tests pass
- No working functionality breaks
- Audit trail is preserved

**Priority:** CRITICAL  
**Status:** GOVERNANCE ENFORCED

### FR-12.2: Deterministic Behavior
**Source:** TRUE_NORTH Section 3.6  
**Requirement:** FM App decisions MUST be deterministic and replayable  
**Acceptance:**
- Same input produces same output
- Decisions can be replayed
- Divergence is detected

**Priority:** CRITICAL  
**Status:** IMPLEMENTED

### FR-12.3: Audit Trail Completeness
**Source:** APP_DESCRIPTION Section 6  
**Requirement:** FM App MUST maintain complete audit trail  
**Acceptance:**
- All decisions logged
- All state changes logged
- All governance checks logged
- All interventions logged
- Logs are immutable

**Priority:** CRITICAL  
**Status:** IMPLEMENTED

### FR-12.4: Privacy and Tenant Isolation
**Source:** MEMORY_MODEL, PRIVACY_GUARDRAILS  
**Requirement:** FM App MUST enforce strict tenant isolation  
**Acceptance:**
- No cross-tenant data access
- All operations include tenant context
- Privacy violations are blocked
- Privacy violations are logged

**Priority:** CRITICAL  
**Status:** IMPLEMENTED

---

## Summary

**Total Functional Requirements:** 57  
**Implemented:** 56  
**Dev/Test Only:** 1 (UI components pending production framework decision)

**Coverage:**
- ✅ Orchestration (5 requirements)
- ✅ Runtime and Liveness (5 requirements)
- ✅ Orchestration Engine (6 requirements)
- ✅ Governance Enforcement (9 requirements)
- ✅ Decision Support (5 requirements)
- ✅ Domain Models (2 requirements)
- ✅ Evidence (3 requirements)
- ✅ Memory Fabric (10 requirements)
- ✅ Commissioning (2 requirements)
- ✅ Testing and QA (3 requirements)
- ✅ Integration and Tooling (4 requirements)
- ✅ Non-Functional (4 requirements)

**Status:** COMPLETE - Functional requirements fully derived from and aligned with frozen architecture.

---

## Approval and Sign-Off

**Pending Approval By:** Johan Ras (CS2 / Human Authority)

**Approval Checklist:**
- [ ] Requirements align with frozen architecture
- [ ] Requirements are testable
- [ ] Requirements are complete
- [ ] Requirements include acceptance criteria

**Approval Date:** _________________

**Signature:** _________________

---

**End of FM App Functional Requirements v1.0**

This document derives all requirements from the frozen True North Architecture and serves as the testable specification for implementation.
