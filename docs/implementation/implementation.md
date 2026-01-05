# FM Implementation Strategy — Memory Era + Watchdog Era Alignment

**Document Type:** Implementation Strategy & Coordination Artifact  
**Version:** 1.0.0  
**Status:** Active  
**Owner:** Johan Ras  
**Created:** 2025-12-24  
**Last Updated:** 2025-12-24

---

## 0. Authority and Purpose

### 0.1 Document Authority

**This document is a COORDINATION ARTIFACT, NOT A SOURCE OF AUTHORITY.**

- **Authority resides in:** Governance canon (maturion-foreman-governance repository) and architecture specifications (this repository)
- **This document's role:** Maps canonical governance to concrete implementation work, sequences execution, tracks progress
- **This document does NOT:** Define new governance rules, override canon, introduce new requirements, specify runtime behavior

### 0.2 Purpose

This document provides:
1. **Gap Analysis** - What governance requires vs. what is currently implemented
2. **Work Mapping** - Maps identified gaps to specific governance and FM runtime architecture issues
3. **Execution Sequencing** - Defines blocking dependencies and work order
4. **Progress Tracking** - Current status of each workstream
5. **Scope Clarity** - Explicit boundaries of what is and isn't addressed

---

## 1. Source Surveys and Assessment

### 1.1 Completed Surveys

This strategy is based on four completed surveys:

| Survey ID | Title | Date Completed | Key Findings |
|-----------|-------|----------------|--------------|
| **ARCH-ALIGN-01** | Architecture Readiness Alignment | 2025-12-24 | Runtime architecture specifications complete; implementation pending |
| **MEM-AUTH-01** | Memory Authority Boundary Audit | 2025-12-24 | Clear authority boundaries defined; enforcement mechanisms needed |
| **FM-RESP-01** | Foreman Memory Responsibility Gap Analysis | 2025-12-24 | Foreman roles clear; memory supervision workflow undefined |
| **WD-OBS-01** | Watchdog Observability Readiness | 2025-12-24 | Observability architecture defined; dashboards and query surfaces unimplemented |

### 1.2 Survey Alignment with Governance

All surveys align with governance canon introduced in:
- **G-COG-A2** - Cognitive Hygiene Protocol governance
- **G-COG-A3** - Memory authority boundaries
- **G-C2** - Commissioning phase 2 requirements
- **G-C3** - Commissioning phase 3 requirements  
- **G-C4** - Commissioning phase 4 requirements

**Governance Canon Status:** Strong and non-contradictory. No conflicts detected.

---

## 2. Identified Gaps

### 2.1 BLOCKING Gaps (Must Resolve Before Build Execution Features)

#### GAP-1: Memory Lifecycle State Machine Implementation
**Description:** Runtime memory lifecycle (UNINITIALIZED → LOADING → VALIDATING → USABLE/DEGRADED/FAILED) is architecturally defined but not implemented in FM runtime.

**Impact:** Foreman cannot verify memory is safe before accepting builds. Agents may operate on stale/corrupted memory.

**Canonical Source:** 
- Architecture: `docs/architecture/runtime/memory/MEMORY_LIFECYCLE_STATE_MACHINE.md` (Completed)
- Governance: `foreman/behaviours/memory-rules.md`

**Status:** ❌ Architecture complete, implementation pending

---

#### GAP-2: CHP Memory Integration and Authorization
**Description:** CHP reads memory to detect drift, but read authorization layer, audit logging, and proposal workflow are not implemented.

**Impact:** CHP cannot detect drift safely. No audit trail of CHP memory access. Proposal queue and approval workflow missing.

**Canonical Source:**
- Architecture: `docs/architecture/runtime/cognitive-hygiene/CHP_MEMORY_INTEGRATION_ARCHITECTURE.md` (Completed)
- Governance: `foreman/behaviours/memory-rules.md`, `foreman/privacy-guardrails.md`

**Status:** ❌ Architecture complete, implementation pending

---

#### GAP-3: Memory State Observability and Audit Query Surfaces
**Description:** Foreman and Watchdog cannot observe memory health, state transitions, or access patterns. No audit query APIs exist.

**Impact:** No visibility into memory fabric health. Cannot diagnose failures. Cannot demonstrate compliance. No forensic capability.

**Canonical Source:**
- Architecture: `docs/architecture/runtime/observability/MEMORY_OBSERVABILITY_ARCHITECTURE.md` (Completed)
- Governance: `foreman/qa-governance.md`, `foreman/compliance/compliance-qa-spec.md`

**Status:** ❌ Architecture complete, implementation pending

---

### 2.2 NON-BLOCKING Gaps (Clarity and Operational Improvements)

#### GAP-4: Foreman Role Canon Clarifications
**Description:** Foreman's memory supervision duties (constraint enforcement, integrity monitoring) are implicit but not explicitly enumerated in canonical role documents.

**Impact:** Ambiguity in Foreman's responsibilities. Potential for missed supervision duties.

**Canonical Source:**
- `foreman/identity.md`
- `foreman/roles-and-duties.md`

**Status:** ⚠️ Clarification needed (non-blocking)

---

#### GAP-5: Watchdog Implementation Readiness
**Description:** Watchdog directory structures, report generation workflows, and escalation artifact locations are undefined.

**Impact:** Watchdog cannot generate daily/weekly reports. Escalation artifacts have no defined storage location.

**Canonical Source:**
- `foreman/platform/watchdog-spec.md` (if exists)
- Governance: `foreman/platform/governance-watchdog-spec.md` (if exists)

**Status:** ⚠️ Needs definition (non-blocking for memory work)

---

## 3. Gap-to-Issue Mapping

### 3.1 Governance Issues (Canonical Clarifications)

| Gap ID | Governance Issue | Description | Repository |
|--------|------------------|-------------|------------|
| GAP-4 | G-FM-ROLE-01 | Explicitly enumerate Foreman memory supervision duties | maturion-foreman-governance |
| GAP-5 | G-WD-IMPL-01 | Define Watchdog directory structure and report artifacts | maturion-foreman-governance |

**Note:** These are governance clarifications, not new rules. Authority for resolving these resides with Johan in the governance repository.

---

### 3.2 FM Runtime Architecture Issues (Implementation Work)

| Gap ID | FM Runtime Issue | Description | Repository |
|--------|------------------|-------------|------------|
| GAP-1 | FM-MEM-RT-01 | Implement Memory Lifecycle State Machine runtime component | maturion-foreman-office-app |
| GAP-2 | FM-CHP-INT-01 | Implement CHP memory authorization, audit, and proposal workflow | maturion-foreman-office-app |
| GAP-3 | FM-OBS-RT-01 | Implement memory observability APIs and dashboard integration | maturion-foreman-office-app |

**Status of FM Runtime Issues:**
- FM-MEM-RT-01: ✅ Architecture complete (2025-12-24), implementation pending
- FM-CHP-INT-01: ✅ Architecture complete (2025-12-24), implementation pending
- FM-OBS-RT-01: ✅ Architecture complete (2025-12-24), implementation pending

**Reference:** See `PREHANDOVER_PROOF_RUNTIME_MEMORY_ARCH.md` for architecture completion evidence.

---

## 4. Execution Sequencing and Dependencies

### 4.1 Workstream Definitions

#### WS1: Memory Lifecycle Runtime (BLOCKING)
**Goal:** Implement Memory Lifecycle Manager and state machine logic.

**Dependencies:**
- None (architecture complete)

**Deliverables:**
1. Memory Lifecycle Manager component
2. State transition logic (UNINITIALIZED → LOADING → VALIDATING → USABLE/DEGRADED/FAILED)
3. Failure mode handlers (hard stop vs. degrade)
4. Health check endpoint
5. State history logging

**Blocks:** WS2, WS3, WS5 (all downstream work)

**Estimated Effort:** 2-3 sprints

**Status:** ⏳ Not started

---

#### WS2: Memory Observability Implementation (BLOCKING)
**Goal:** Implement observability APIs and dashboard integration.

**Dependencies:**
- WS1 (must complete first - observability depends on lifecycle manager)

**Deliverables:**
1. Health Status API (`/api/internal/memory/health`)
2. State Transition History API (`/api/internal/memory/lifecycle/history`)
3. Memory Access Audit API (`/api/internal/memory/audit/access`)
4. Memory Write Audit API (`/api/internal/memory/audit/write`)
5. Privacy Compliance Report API (`/api/internal/memory/compliance/privacy`)
6. Performance Metrics API (`/api/internal/memory/metrics/performance`)
7. Dashboard integration (Foreman, Watchdog, Johan panels)

**Blocks:** WS5 (build console features)

**Estimated Effort:** 2-3 sprints

**Status:** ⏳ Not started

---

#### WS3: CHP Memory Integration (BLOCKING)
**Goal:** Implement CHP memory authorization, audit logging, and proposal workflow.

**Dependencies:**
- WS1 (must complete first - CHP reads depend on lifecycle manager)

**Deliverables:**
1. CHP memory read authorization layer
2. CHP memory access audit logging
3. Proposal generation workflow
4. Proposal queue storage (`/runtime/proposals/pending/`, `/approved/`, `/rejected/`)
5. Proposal routing system (severity-based routing to Foreman or Johan)
6. Proposal approval workflow integration

**Blocks:** None (parallel with WS2)

**Estimated Effort:** 2-3 sprints

**Status:** ⏳ Not started

---

#### WS4: Governance Canon Clarifications (NON-BLOCKING)
**Goal:** Explicitly enumerate Foreman and Watchdog roles and responsibilities in canonical documents.

**Dependencies:**
- None (governance work, independent of implementation)

**Deliverables:**
1. Updated `foreman/identity.md` with explicit memory supervision duties
2. Updated `foreman/roles-and-duties.md` with memory constraint enforcement
3. Watchdog directory structure definition (if needed)
4. Watchdog report artifact specification (if needed)

**Blocks:** None (non-blocking clarifications)

**Estimated Effort:** 1 sprint (governance repo work)

**Status:** ⏳ Not started

**Authority:** Johan (governance repository)

---

#### WS5: Build Console Features (DEPENDENT)
**Goal:** Implement user-facing build console features that depend on memory lifecycle and observability.

**Dependencies:**
- WS1 (must be complete)
- WS2 (must be complete)
- WS3 (optional, but recommended)

**Deliverables:**
- Build console memory status indicator
- Build pre-flight memory health check
- Build execution gate (block if memory FAILED)
- Real-time memory state display

**Blocks:** None (final milestone)

**Estimated Effort:** 1-2 sprints

**Status:** ⏳ Not started

---

### 4.2 Sequencing Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ WS1: Memory Lifecycle Runtime (BLOCKING)                     │
│ → Implement state machine, failure modes, health checks      │
└───────────────────┬─────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
┌───────────────────┐  ┌────────────────────┐
│ WS2: Observability│  │ WS3: CHP Integration│
│ (BLOCKING)        │  │ (BLOCKING)          │
│ → APIs, Dashboards│  │ → Auth, Audit,      │
│                   │  │   Proposals         │
└─────────┬─────────┘  └──────────┬─────────┘
          │                       │
          └───────────┬───────────┘
                      │
                      ▼
            ┌──────────────────┐
            │ WS5: Build       │
            │ Console Features │
            │ (DEPENDENT)      │
            └──────────────────┘

INDEPENDENT (can run anytime, no dependencies):
┌──────────────┐
│ WS4: Canon   │
│ Clarify      │
│ (NON-BLOCK)  │
│ → Foreman    │
│   Watchdog   │
│   Roles      │
└──────────────┘
```

**Critical Path:** WS1 → WS2 → WS5

**Parallel Work:** WS3 can run parallel with WS2 after WS1 completes. WS4 is independent and can run anytime (governance work).

---

## 5. Current Implementation Status

### 5.1 Architecture Specifications (Completed ✅)

| Document | Status | Date Completed | Lines | Sections |
|----------|--------|----------------|-------|----------|
| Memory Lifecycle State Machine | ✅ Complete | 2025-12-24 | 777 | 44 |
| CHP Memory Integration | ✅ Complete | 2025-12-24 | 724 | 53 |
| Memory Observability | ✅ Complete | 2025-12-24 | 942 | 45 |

**Total Architecture Documentation:** 2,443 lines across 3 specifications

**Evidence:** `PREHANDOVER_PROOF_RUNTIME_MEMORY_ARCH.md`

**Reference Issues:** FM-MEM-RT-01, FM-CHP-INT-01, FM-OBS-RT-01 (architecture phase)

---

### 5.2 Runtime Implementation (Pending ⏳)

| Workstream | Status | Dependencies Met | Next Action |
|------------|--------|------------------|-------------|
| WS1: Memory Lifecycle | ⏳ Not Started | ✅ Yes (architecture complete) | Create implementation issue |
| WS2: Observability | ⏳ Not Started | ❌ No (blocked by WS1) | Await WS1 completion |
| WS3: CHP Integration | ⏳ Not Started | ❌ No (blocked by WS1) | Await WS1 completion |
| WS4: Canon Clarifications | ⏳ Not Started | ✅ Yes (independent) | Johan to define scope |
| WS5: Build Console | ⏳ Not Started | ❌ No (blocked by WS1, WS2) | Await WS1 + WS2 completion |

**Overall Status:** Architecture phase complete. Implementation phase not yet started.

---

### 5.3 Testing and Validation Status

| Test Category | Status | Evidence |
|---------------|--------|----------|
| Architecture Validation | ✅ PASS | 114 tests passed, 0 failed (pytest tests/ -v -m 'not wave0') |
| Repository Validation | ✅ PASS | validate-repository.py passed (no new issues introduced) |
| Integration Tests | ✅ PASS | All existing integration tests passing |
| Runtime Implementation Tests | ⏳ Pending | No runtime code yet (architecture-only phase) |

**Test Coverage:** Architecture specifications have no runnable code, so implementation tests are pending.

---

## 6. What is NOT Addressed (Explicit Scope Boundaries)

### 6.1 Out of Scope for This Strategy

This implementation strategy does **NOT** address:

1. **UI Design and UX Behavior**
   - Dashboard layouts and visual design
   - User interaction flows
   - Frontend component implementation
   - **Why:** UI/UX is a separate workstream, not part of memory architecture implementation

2. **Build Execution Authorization**
   - Criteria for authorizing build execution
   - Build approval workflows
   - Build sequencing decisions
   - **Why:** Build governance is separate from memory lifecycle implementation

3. **Governance Rule Definition**
   - New governance policies
   - Changes to existing governance canon
   - Authority model modifications
   - **Why:** Governance authority resides in maturion-foreman-governance repository (Johan's authority)

4. **Readiness Gate Definitions**
   - Commissioning phase requirements
   - Evidence collection criteria
   - Approval thresholds
   - **Why:** Readiness gates are governance-level decisions, not implementation details

5. **Compliance Framework Changes**
   - ISO/NIST/COBIT rule additions
   - Compliance control modifications
   - Audit criteria changes
   - **Why:** Compliance framework is canonical, defined in governance repository

6. **Multi-Tenant Runtime Behavior**
   - Tenant provisioning workflows
   - Tenant-specific memory isolation mechanisms
   - Cross-tenant data handling
   - **Why:** Tenant isolation is enforced by privacy guardrails (already canonical), not by memory lifecycle implementation

7. **Performance Tuning and Optimization**
   - Cache sizing strategies
   - Query optimization techniques
   - Load balancing approaches
   - **Why:** Performance optimization is a post-implementation refinement activity

---

### 6.2 Deferred Work (Future Phases)

The following work is acknowledged but deferred to future phases:

1. **Advanced CHP Features**
   - Adaptive learning from proposal outcomes
   - Proactive drift prediction
   - Cross-tenant pattern recognition (anonymized)
   - **Why:** These are enhancement features, not MVP requirements

2. **Advanced Observability**
   - Machine learning-based anomaly detection
   - Predictive memory state transitions
   - Natural language query interface
   - **Why:** These are enhancement features, not MVP requirements

3. **Self-Healing Memory Fabric**
   - Automatic recovery from transient failures
   - Predictive maintenance
   - Auto-scaling for memory fabric
   - **Why:** These are enhancement features, not MVP requirements

4. **Multi-Region Memory Replication**
   - Cross-region memory synchronization
   - Disaster recovery mechanisms
   - Geographic failover
   - **Why:** These are scale/resilience features, not MVP requirements

---

## 7. Acceptance Criteria for Implementation Completion

### 7.1 WS1: Memory Lifecycle Runtime
- ✅ Memory Lifecycle Manager component exists and is operational
- ✅ State machine transitions work correctly (UNINITIALIZED → LOADING → VALIDATING → USABLE/DEGRADED/FAILED)
- ✅ Failure modes trigger correct behavior (hard stop vs. degrade)
- ✅ Health check endpoint returns accurate state
- ✅ State transitions are logged and auditable
- ✅ All 5 states are reachable and tested
- ✅ Recovery strategies execute correctly (auto-recovery where safe)

---

### 7.2 WS2: Memory Observability
- ✅ All 6 observability APIs are implemented and functional
- ✅ Foreman dashboard displays memory status panel
- ✅ Watchdog dashboard displays memory health monitor
- ✅ Johan dashboard provides complete oversight
- ✅ Audit trails are immutable and tamper-proof
- ✅ Privacy filters prevent PII/secret exposure in observability layer
- ✅ Data retention policies are enforced (90 days operational, 7 years audit)

---

### 7.3 WS3: CHP Memory Integration
- ✅ CHP can read authorized memory scopes (`global`, `foreman`, `experience`)
- ✅ CHP cannot read prohibited scopes (`runtime`, `platform`)
- ✅ All CHP memory reads are audited
- ✅ CHP proposal generation works correctly
- ✅ Proposal queue storage is functional (`pending/`, `approved/`, `rejected/`)
- ✅ Proposal routing system delivers proposals to correct approver
- ✅ Approval workflow integrates with Foreman and Johan dashboards
- ✅ No auto-promotion occurs (proposals require explicit approval)

---

### 7.4 Overall Integration
- ✅ Foreman can verify memory is USABLE before accepting builds
- ✅ Foreman can observe memory state and access patterns
- ✅ Watchdog can monitor memory health and detect anomalies
- ✅ Johan can audit all memory operations and enforce governance
- ✅ CHP can detect drift and propose corrections without authority leakage
- ✅ All components integrate correctly with existing FM runtime agent
- ✅ Zero regression: All existing tests continue to pass
- ✅ Privacy guardrails enforced: No tenant data in memory observability

---

## 8. Issue Queue and Tracking

### 8.1 Governance Issues (maturion-foreman-governance repository)

| Issue ID | Title | Status | Owner | Blocks |
|----------|-------|--------|-------|--------|
| G-FM-ROLE-01 | Explicitly enumerate Foreman memory supervision duties | ⏳ Defined | Johan | None |
| G-WD-IMPL-01 | Define Watchdog directory structure and report artifacts | ⏳ Defined | Johan | None |

**Note:** These are governance clarifications, not implementation issues. Johan has authority to define and resolve in governance repository.

---

### 8.2 FM Runtime Architecture Issues (maturion-foreman-office-app repository)

#### Architecture Phase (Completed ✅)
| Issue ID | Title | Status | Date Completed |
|----------|-------|--------|----------------|
| FM-MEM-RT-01 (arch) | Define Memory Lifecycle State Machine architecture | ✅ Complete | 2025-12-24 |
| FM-CHP-INT-01 (arch) | Define CHP Memory Integration architecture | ✅ Complete | 2025-12-24 |
| FM-OBS-RT-01 (arch) | Define Memory Observability architecture | ✅ Complete | 2025-12-24 |

**Evidence:** `PREHANDOVER_PROOF_RUNTIME_MEMORY_ARCH.md`

---

#### Implementation Phase (Active ⏳)
| Issue ID | Title | Status | Dependencies | Workstream |
|----------|-------|--------|--------------|------------|
| [#181](https://github.com/MaturionISMS/maturion-foreman-office-app/issues/181) | FM-MEM-RT-01 (impl) — Implement Memory Lifecycle State Machine runtime | ⏳ Ready to Start | None | WS1 |
| [#182](https://github.com/MaturionISMS/maturion-foreman-office-app/issues/182) | FM-OBS-RT-01 (impl) — Implement Memory Observability APIs and dashboards | ⏳ Blocked by #181 | FM-MEM-RT-01 (impl) | WS2 |
| [#183](https://github.com/MaturionISMS/maturion-foreman-office-app/issues/183) | FM-CHP-INT-01 (impl) — Implement CHP Memory Integration and proposal workflow | ⏳ Blocked by #181 | FM-MEM-RT-01 (impl) | WS3 |
| FM-BUILD-CONS-01 | Implement Build Console memory status features | ⏳ Needs Creation | FM-MEM-RT-01 (impl), FM-OBS-RT-01 (impl) | WS5 |

**Status:** Implementation phase initiated via FM-IMPL-EXEC-01 (2025-12-24).

**Detailed Tracking:** See `IMPLEMENTATION_STATUS_TRACKING.md` for progress updates.

---

## 9. Summary and Next Actions

### 9.1 Current State Summary
- **Governance Canon:** ✅ Strong and non-contradictory (G-COG-A2/A3, G-C2/C3/C4)
- **Architecture Specifications:** ✅ Complete (2,443 lines across 3 documents)
- **Runtime Implementation:** ⏳ Not started (architecture phase complete, implementation phase pending)
- **Blocking Gaps:** 3 identified (Memory Lifecycle, CHP Integration, Observability)
- **Non-Blocking Gaps:** 2 identified (Foreman role clarifications, Watchdog readiness)

---

### 9.2 Critical Path to Unblock Build Execution
1. **WS1: Memory Lifecycle Runtime** (MUST COMPLETE FIRST)
   - Implement state machine and failure modes
   - Enable Foreman to verify memory is safe before builds

2. **WS2: Memory Observability** (MUST COMPLETE SECOND)
   - Implement APIs and dashboards
   - Enable Foreman and Watchdog to monitor memory health

3. **WS3: CHP Integration** (CAN RUN PARALLEL WITH WS2)
   - Implement authorization, audit, and proposal workflow
   - Enable CHP to detect drift safely

4. **WS5: Build Console Features** (FINAL MILESTONE)
   - Integrate memory status into build console
   - Enable user-facing visibility

---

### 9.3 Immediate Next Actions

#### For Johan (Governance Authority)
1. Review and approve this implementation strategy document
2. Define scope for G-FM-ROLE-01 (Foreman role clarifications)
3. Define scope for G-WD-IMPL-01 (Watchdog implementation readiness)
4. Authorize creation of implementation issues (FM-MEM-RT-01, FM-OBS-RT-01, FM-CHP-INT-01, FM-BUILD-CONS-01)

#### For FM Repo Builder (Implementation)
1. Await Johan's approval of this strategy
2. Once approved, create GitHub issues for WS1, WS2, WS3, WS5
3. Begin WS1 implementation (Memory Lifecycle Runtime)
4. Block all build execution features until WS1 + WS2 complete

---

## 10. Governance Gates and Pre-Authorization Requirements

**Authority**: Governance PR #877 (maturion-foreman-governance) - BL-018/BL-019 Canonization  
**Status**: ACTIVE (Mandatory) — Effective 2026-01-05

### Purpose

This section documents the **governance gates** that FM must execute before authorizing any wave or subwave execution. These gates were canonized in response to BL-018 (Wave 2.2 QA Catalog Misalignment) and BL-019 (Second-Time Failure - EMERGENCY).

**Note**: This section describes **conceptual requirements only**. No implementation code changes are required as part of governance layer-down. These gates apply to FM's planning and authorization processes, not to the application runtime.

### QA-Catalog-Alignment Gate (BL-018/BL-019 Prevention)

**Authority**: `governance/specs/QA_CATALOG_ALIGNMENT_GATE_SPEC.md`  
**FM Contract Reference**: `.github/agents/ForemanApp-agent.md` Section XIV.G

#### Gate Purpose
Ensures that before any wave or subwave is authorized:
1. All assigned QA ranges exist in `QA_CATALOG.md`
2. QA catalog entries semantically match the subwave scope intent
3. QA-to-Red tests exist for ALL QA IDs in the assigned range
4. No QA ID collisions exist between subwaves
5. Architecture is frozen and defines all components being tested

#### Gate Execution Points
FM MUST execute this gate:
- Before finalizing wave rollout plan
- Before creating builder sub-issue for any subwave
- Before appointing builder to any subwave
- After any BL/FL/CI that affects QA Catalog structure

#### Gate Checks (MANDATORY)

1. **QA Range Existence Check**
   - Verify all QA IDs in assigned range are defined in `QA_CATALOG.md`
   - Verify no gaps in the QA range sequence

2. **Semantic Alignment Check**
   - Verify QA catalog descriptions match subwave feature scope
   - Example: If subwave is "Parking Station Advanced", QA catalog entries must describe parking station features, not failure modes

3. **QA-to-Red Test Existence Check**
   - Verify test files exist for all QA IDs at expected locations
   - Verify tests are RED (not yet implemented) per QA-to-Red semantics
   - Record test file locations for builder reference

4. **QA ID Collision Check**
   - Verify no QA ID is assigned to multiple subwaves in the same wave
   - Verify no overlapping QA ranges

5. **Architecture Alignment Check**
   - Verify architecture document defines all components/flows/states referenced by QA catalog
   - Verify architecture is FROZEN (not in draft)

#### Gate Outcomes

**PASS**: FM may proceed with subwave authorization, builder appointment, Build-to-Green execution

**FAIL**: FM MUST:
- BLOCK the subwave authorization
- STOP wave progression at this point
- ESCALATE to appropriate correction pathway:
  - Extend QA Catalog if entries missing
  - Reassign QA range if semantic mismatch
  - Complete QA-to-Red foundation if tests missing
  - De-conflict QA ranges if collision detected
  - Complete/freeze architecture if gaps exist
- REGISTER FL/CI entry documenting the failure
- CORRECT the structural gap before retry
- RE-RUN the gate after correction

#### Builder Expectations

Builders MUST expect that FM has passed this gate before appointment. If builders discover gate preconditions are NOT met:
- STOP work immediately
- Declare BLOCKED in appointment issue
- Document specific precondition failure
- Escalate to FM with evidence
- Wait for FM structural correction

**Critical**: Builders have NO AUTHORITY to "invent" missing QA catalog entries or QA-to-Red tests. If foundation is missing, declare BLOCKED.

### BL Forward-Scan Obligation (Pattern Recurrence Prevention)

**Authority**: `governance/specs/BL_FORWARD_SCAN_OBLIGATION_SPEC.md`  
**FM Contract Reference**: `.github/agents/ForemanApp-agent.md` Section XV

#### Forward-Scan Purpose
After ANY BL/FL/CI discovery, FM must:
1. Identify the failure pattern
2. Scan ALL in-scope work for the pattern
3. Correct EVERY instance of the pattern
4. Produce and persist evidence
5. Create governance ratchets to prevent recurrence

#### Forward-Scan Trigger
FM MUST execute forward-scan:
- After any BL entry in `governance/canon/BOOTSTRAP_EXECUTION_LEARNINGS.md`
- After any FL/CI entry in governance registry
- After discovery of second-time failure (EMERGENCY)

#### Forward-Scan Protocol (6 Steps - ALL MANDATORY)

1. **Pattern Identification**
   - Define the failure pattern clearly
   - Generalize pattern to identify other potential occurrences

2. **Scope Determination**
   - Identify ALL work that could exhibit the pattern
   - Current wave subwaves (authorized and planned)
   - Future wave planning documents
   - Architecture/QA/governance documents if pattern relates to them

3. **Systematic Scan Execution**
   - Examine EVERY item in scope for the pattern
   - Document findings (confirmed, suspected, clear)
   - Create scan log with evidence

4. **Correction Execution**
   - Fix ALL confirmed instances (no partial fixes)
   - Verify corrections resolve the pattern
   - Document correction evidence

5. **Evidence Persistence**
   - Create forward-scan evidence document
   - Store permanently (e.g., `WAVE_2_FORWARD_SCAN_QA_ALIGNMENT_VERIFICATION.md`)
   - Link from BL/FL/CI entry

6. **Governance Ratchet Creation**
   - Identify governance/process gaps that allowed the pattern
   - Design ratchet (checklist, gate, automation, policy update)
   - Implement ratchet in governance documents
   - Update agent contracts to enforce ratchet

#### Forward-Scan Blocking Requirement

**BLOCKING**: FM MUST NOT authorize any new subwave or wave until forward-scan is COMPLETE (all steps executed, all findings corrected, evidence persisted).

**Critical Lesson (BL-019)**: BL-019 occurred because forward-scan after BL-018 was NOT completed before issuing next appointment (Subwave 2.3). This demonstrates that forward-scan is BLOCKING and must complete before resuming execution.

### Second-Time Failure Prohibition and TARP Protocol

**Authority**: `governance/specs/SECOND_TIME_FAILURE_PROHIBITION_SPEC.md`  
**FM Contract Reference**: `.github/agents/ForemanApp-agent.md` Section XVI

#### Failure Classification by Occurrence

1. **First-Time Failure**: CATASTROPHIC
   - Handle with great urgency
   - Implement measures to PREVENT recurrence
   - Pattern must NEVER occur again

2. **Second-Time Failure**: BEYOND CATASTROPHIC (EMERGENCY)
   - HALT ALL EXECUTION immediately
   - Invoke TARP (Targeted Analysis and Recovery Plan)
   - Escalate to CS2 (Johan) immediately
   - Wait for CS2 authorization before resuming

3. **Third-Time Failure**: CONSTITUTIONALLY PROHIBITED
   - Must be structurally impossible by governance design
   - If occurs, governance model has failed

#### TARP Protocol (Second-Time Failure Response)

When FM detects second-time failure (same pattern as prior BL/FL/CI), FM MUST:

1. **Emergency Declaration**
   - STOP all active builder work immediately
   - BLOCK all pending subwave authorizations
   - Declare EMERGENCY in all active issues
   - Notify CS2 immediately

2. **Second-Order Root Cause Analysis**
   - WHY did the first-time failure prevention measures fail?
   - Was the ratchet correctly designed?
   - Was the ratchet properly implemented and enforced?
   - What systemic issue allowed recurrence?

3. **Emergency Corrections**
   - Correct ALL instances of second-time failure pattern
   - Fix systemic gap that allowed recurrence
   - Strengthen or replace failing ratchet
   - Add redundant prevention mechanisms

4. **Governance Hardening**
   - Update governance to make third-time failure IMPOSSIBLE
   - Add automation where manual checks failed
   - Add redundant checks and enforcement gates
   - Update agent contracts with strengthened obligations

5. **TARP Evidence Pack**
   - Document complete TARP execution for CS2 review
   - Include timeline, evidence, prevention architecture, residual risk assessment

6. **CS2 Review and Resumption Authorization**
   - Submit TARP Evidence Pack to CS2
   - Obtain explicit CS2 authorization to resume execution
   - FM MUST NOT resume without CS2 approval

#### Pattern Matching Requirement

When registering new BL/FL/CI, FM MUST:
1. Review ALL prior BL/FL/CI entries
2. Compare root causes
3. Classify occurrence count (first, second, third)
4. If second-time failure detected: INVOKE TARP IMMEDIATELY

### Implementation Impact

**No Code Changes Required**: These governance gates and protocols apply to FM's planning and authorization processes. They do not require changes to:
- Application runtime code
- Wave 2 implementation modules
- Test suites or test infrastructure
- Builder implementation code paths

**Documentation Only**: This section provides conceptual guidance for FM execution. The authoritative specifications are in the governance specs referenced above.

### References

**Governance Specifications (Canonical Authority)**:
- `governance/specs/QA_CATALOG_ALIGNMENT_GATE_SPEC.md`
- `governance/specs/BL_FORWARD_SCAN_OBLIGATION_SPEC.md`
- `governance/specs/SECOND_TIME_FAILURE_PROHIBITION_SPEC.md`
- `governance/canon/BL_018_019_GOVERNANCE_INTEGRATION.md`

**Agent Contract Integration**:
- `.github/agents/ForemanApp-agent.md` (Sections XIV.G, XV, XVI)
- `.github/agents/qa-builder.md` (BL-018/BL-019 Awareness section)
- `.github/agents/ui-builder.md` (BL-018/BL-019 Awareness section)
- `.github/agents/api-builder.md` (BL-018/BL-019 Awareness section)
- `.github/agents/schema-builder.md` (BL-018/BL-019 Awareness section)
- `.github/agents/integration-builder.md` (BL-018/BL-019 Awareness section)

**Case Study Documents**:
- `FLCI_REGISTRY_UPDATE_BL_018.md` (First-time QA Catalog misalignment)
- `FLCI_REGISTRY_UPDATE_BL_019_SECOND_FAILURE_CATASTROPHIC.md` (Second-time failure - EMERGENCY)
- `WAVE_2_EMERGENCY_CORRECTIVE_ACTION_PLAN_BL_019.md` (TARP evidence)
- `WAVE_2_FORWARD_SCAN_QA_ALIGNMENT_VERIFICATION.md` (Forward-scan evidence)

---

## 11. Version History

- **v1.0.0 (2025-12-24):** Initial implementation strategy document created
  - Mapped gaps from surveys (ARCH-ALIGN-01, MEM-AUTH-01, FM-RESP-01, WD-OBS-01)
  - Defined workstreams and sequencing
  - Tracked current status (architecture complete, implementation pending)
  - Explicitly defined scope boundaries and non-goals

- **v1.1.0 (2026-01-05):** Added Governance Gates and Pre-Authorization Requirements (Section 10)
  - Documented QA-Catalog-Alignment Gate (BL-018/BL-019 prevention)
  - Documented BL Forward-Scan Obligation (pattern recurrence prevention)
  - Documented Second-Time Failure Prohibition and TARP protocol
  - Cross-referenced to governance PR #877 and FM/builder agent contract updates
  - Clarified: Documentation only, no implementation code changes required

---

## 12. Related Documents

### Architecture Specifications (Completed)
- `docs/architecture/runtime/memory/MEMORY_LIFECYCLE_STATE_MACHINE.md`
- `docs/architecture/runtime/cognitive-hygiene/CHP_MEMORY_INTEGRATION_ARCHITECTURE.md`
- `docs/architecture/runtime/observability/MEMORY_OBSERVABILITY_ARCHITECTURE.md`

### Governance Canon (maturion-foreman-governance repository)
- `governance/policies/memory-model.md`
- `governance/policies/privacy-guardrails.md`
- `foreman/behaviours/memory-rules.md`
- `foreman/identity.md`
- `foreman/roles-and-duties.md`

### Governance Canon (This Repository - BL-018/BL-019 Integration)
- `governance/specs/QA_CATALOG_ALIGNMENT_GATE_SPEC.md` (QA-Catalog-Alignment gate requirements)
- `governance/specs/BL_FORWARD_SCAN_OBLIGATION_SPEC.md` (BL Forward-Scan protocol)
- `governance/specs/SECOND_TIME_FAILURE_PROHIBITION_SPEC.md` (Second-time failure prohibition and TARP)
- `governance/canon/BL_018_019_GOVERNANCE_INTEGRATION.md` (Integration summary from governance PR #877)

### Evidence and Proof Documents
- `PREHANDOVER_PROOF_RUNTIME_MEMORY_ARCH.md` (Architecture completion proof)

### Implementation Tracking
- `IMPLEMENTATION_STATUS_TRACKING.md` (Live progress tracking for all workstreams)
- `FM_IMPL_EXEC_01_COMPLETION_SUMMARY.md` (Phase initiation completion proof)

---

**END OF IMPLEMENTATION STRATEGY DOCUMENT**

This document is a living coordination artifact. It will be updated as implementation progresses and new information becomes available.
