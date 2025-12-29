# ARCH-GAP-02 — Post-Deployment Application Performance Monitoring

**Version:** 1.0  
**Date:** 2025-12-29  
**Status:** Architecture Clarification Complete  
**Type:** Scope Boundary Definition  
**Authority:** Architecture Gap Resolution (ARCH-GAP-02)

---

## 1. Context

The FM platform is designed to orchestrate one-time builds that produce production-ready applications.

Once applications are built and deployed, there is an identified future need to:

- Monitor application health and performance
- Observe runtime behavior
- Detect degradation or regressions
- Surface insights to CS2 via the FM UI

This capability was not explicitly addressed in the True North architecture, creating ambiguity about whether this is:
- An FM v1 responsibility
- A future FM module
- Out-of-scope for FM entirely

---

## 2. Scope Question

**Question:** Does FM v1 include post-deployment application performance monitoring (APM)?

**Answer:** **NO** — Post-deployment APM is **explicitly out-of-scope for FM v1**.

---

## 3. Architectural Boundary

### 3.1 What FM DOES Monitor

FM monitors **build-time execution**:

- **Builder Agent Health**: Heartbeats, stalls, execution progress
- **Build Process State**: Program/Wave/Task status, blockers, completion
- **Build Quality Gates**: Architecture validation, QA pass rates, evidence completeness
- **Governance Compliance**: GSR violations, OPOJD adherence, Zero Test Debt
- **Execution Liveness**: Silent stalls, builder failures, escalation needs

**Summary:** FM is a **build supervisor**, not a **runtime supervisor**.

### 3.2 What FM DOES NOT Monitor

FM does **NOT** monitor **post-deployment application runtime**:

- ❌ Application performance metrics (latency, throughput, CPU, memory)
- ❌ Application health checks (availability, uptime, error rates)
- ❌ Application runtime behavior (user activity, API usage, transaction flows)
- ❌ Application degradation detection (performance regression, anomaly detection)
- ❌ Application observability (logs, traces, metrics from deployed apps)

**Summary:** FM is not an APM system.

---

## 4. Rationale

### 4.1 FM is Build-Time, Not Runtime

FM's mission is to orchestrate and govern the **construction** of applications, not their **operation**.

**Build-Time Scope:**
- Architecture validation
- Build orchestration
- Builder supervision
- QA enforcement
- Evidence collection

**Runtime Scope (NOT FM):**
- Application monitoring
- Performance tracking
- Incident detection
- Runtime observability

### 4.2 Separation of Concerns

**FM = Build Supervisor**
- Ensures applications are built correctly
- Enforces governance during construction
- Validates architecture and QA before handoff
- Provides evidence of build quality

**APM = Runtime Supervisor (Future)**
- Monitors deployed application behavior
- Detects performance degradation
- Alerts on runtime failures
- Provides runtime observability

Conflating these concerns would:
- Expand FM scope beyond its core competency
- Create maintenance complexity
- Introduce runtime dependencies
- Blur the boundary between build and runtime

### 4.3 Future Capability

Post-deployment APM is a **valid future need** but belongs to a different module:

**Possible Future Homes:**
1. **PIT (Project Implementation Tracker)** — Could extend to include runtime monitoring
2. **Dedicated Observability Module** — Specialized module for runtime insights
3. **Integration with External APM** — Integrate with existing APM tools (Datadog, New Relic, etc.)

**Not FM v1.**

---

## 5. Architecture Impact

### 5.1 True North Updates

The following sections of `FOREMAN_TRUE_NORTH_v1.0.md` are updated to clarify this boundary:

**Section 3.2 — Out of Scope (Wave 0)**

Add:
- ❌ Post-deployment application performance monitoring (APM)
- ❌ Runtime observability of deployed applications

**Section 4.2 — External Boundaries**

Add clarification:
- FM monitors **builder execution**, not deployed application runtime
- Runtime monitoring is a future capability outside FM scope

### 5.2 No Code Changes Required

This is a **documentation-only clarification**.

No implementation changes are needed because:
- FM does not currently implement APM
- No code removal is required
- No behavior changes

---

## 6. Decision Statement

**Decision:** Post-deployment application performance monitoring (APM) is **explicitly out-of-scope for FM v1**.

**Reasoning:**
1. FM is a build-time orchestration system, not a runtime monitoring system
2. APM introduces different concerns, dependencies, and complexity
3. APM is a valid future capability but belongs in a different module
4. Clear boundary prevents scope creep and maintains architectural integrity

**Future Path:**
- APM capabilities may be added to PIT or a dedicated observability module
- APM integration may be provided via external tool integration
- FM architecture does not preclude future APM modules

**Authority:** Architecture gap resolution (governance-scoped documentation)

---

## 7. Acceptance Criteria

✅ **All Met**

1. ✅ True North architecture includes clear statement regarding post-deployment monitoring
2. ✅ Post-deployment monitoring is marked as **explicitly out-of-scope for v1**
3. ✅ No ambiguity about v1 responsibilities
4. ✅ Future capability path is acknowledged without commitment
5. ✅ Architectural boundary between build-time and runtime is clear

---

## 8. Impact Assessment

- **Code Changes**: None (documentation only)
- **Behavioral Changes**: None
- **Breaking Changes**: None
- **Tests Required**: None (scope clarification)
- **Authority Boundaries**: Reinforced (FM scope limited to build-time)

---

## 9. Versioning

**Version:** 1.0  
**Supersedes:** N/A (new gap resolution)  
**Change Type:** Scope clarification (non-breaking)

---

## 10. Related Documents

- `foreman/architecture/FOREMAN_TRUE_NORTH_v1.0.md` — Updated Section 3.2, 4.2
- `docs/architecture/TRUE_NORTH_FM_ARCHITECTURE.md` — Updated Section 2.2, 2.3
- `ARCH_GAP_01_COMPLETION_PROOF.md` — Prior architecture gap resolution

---

**Completion Date:** 2025-12-29  
**Document Status:** ✅ COMPLETE  
**Architecture Status:** Boundary clarified, no ambiguity remains
