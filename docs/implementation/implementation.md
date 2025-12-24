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
┌───────────────────┐  ┌────────────────────┐  ┌──────────────┐
│ WS2: Observability│  │ WS3: CHP Integration│  │ WS4: Canon   │
│ (BLOCKING)        │  │ (BLOCKING)          │  │ Clarify      │
│ → APIs, Dashboards│  │ → Auth, Audit,      │  │ (NON-BLOCK)  │
│                   │  │   Proposals         │  │ → Foreman    │
└─────────┬─────────┘  └──────────┬─────────┘  │   Watchdog   │
          │                       │             │   Roles      │
          └───────────┬───────────┘             └──────────────┘
                      │
                      ▼
            ┌──────────────────┐
            │ WS5: Build       │
            │ Console Features │
            │ (DEPENDENT)      │
            └──────────────────┘
```

**Critical Path:** WS1 → WS2 → WS5

**Parallel Work:** WS3 can run parallel with WS2 after WS1 completes. WS4 can run anytime (governance work).

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

#### Implementation Phase (Pending ⏳)
| Issue ID | Title | Status | Dependencies | Workstream |
|----------|-------|--------|--------------|------------|
| FM-MEM-RT-01 (impl) | Implement Memory Lifecycle State Machine runtime | ⏳ Not Started | None | WS1 |
| FM-OBS-RT-01 (impl) | Implement Memory Observability APIs and dashboards | ⏳ Not Started | FM-MEM-RT-01 (impl) | WS2 |
| FM-CHP-INT-01 (impl) | Implement CHP Memory Integration and proposal workflow | ⏳ Not Started | FM-MEM-RT-01 (impl) | WS3 |
| FM-BUILD-CONS-01 | Implement Build Console memory status features | ⏳ Not Started | FM-MEM-RT-01 (impl), FM-OBS-RT-01 (impl) | WS5 |

**Next Step:** Create implementation issues for WS1, WS2, WS3, WS5 in GitHub.

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

## 10. Version History

- **v1.0.0 (2025-12-24):** Initial implementation strategy document created
  - Mapped gaps from surveys (ARCH-ALIGN-01, MEM-AUTH-01, FM-RESP-01, WD-OBS-01)
  - Defined workstreams and sequencing
  - Tracked current status (architecture complete, implementation pending)
  - Explicitly defined scope boundaries and non-goals

---

## 11. Related Documents

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

### Evidence and Proof Documents
- `PREHANDOVER_PROOF_RUNTIME_MEMORY_ARCH.md` (Architecture completion proof)

---

**END OF IMPLEMENTATION STRATEGY DOCUMENT**

This document is a living coordination artifact. It will be updated as implementation progresses and new information becomes available.
