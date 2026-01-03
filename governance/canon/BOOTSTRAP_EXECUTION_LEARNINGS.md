# Bootstrap Execution Learnings

This document records structural learnings identified during
manual bootstrap execution (Wave 0).

These learnings inform future governance canon,
FM application automation, and delegated execution models.

Entries are additive and non-retroactive.

## BL-0001 — Governance Stabilisation Must Precede FM Recruitment

**Context:** Pre-Batch 3 (Governance Hardening & Readiness)

**Observed Issue:**  
FM recruitment was initially attempted while governance artifacts and authority boundaries were still in flux.

**Root Cause:**  
No explicit rule existed requiring governance lock and layer-down completion before FM activation.

**Learning:**  
Governance MUST be stabilised, locked, and layered down before FM is recruited or granted planning authority.

**Governance Impact:**  
Informs FM recruitment sequencing and Batch entry conditions.

**Status:** Recorded

## BL-0002 — Readiness Certification Is a Governance Function, Not an Execution Trigger

**Context:** Batch 3A — Final Readiness Certification

**Observed Issue:**  
Risk of interpreting readiness certification as implicit execution authorization.

**Root Cause:**  
Readiness and execution were not explicitly separated in early mental models.

**Learning:**  
Readiness certification records system state and constraints only; execution authority must be granted explicitly and separately.

**Governance Impact:**  
Clarifies Batch 3A vs Batch 3B boundary.

**Status:** Recorded

## BL-0003 — FM Identity Must Be Canonical Before Recruitment

**Context:** Batch 3B Entry Preparation

**Observed Issue:**  
Multiple legacy FM agent definitions created ambiguity in authority and scope.

**Root Cause:**  
Historical agent contracts were not deprecated before reuse.

**Learning:**  
Exactly one canonical FM agent definition MUST exist before FM recruitment. Legacy definitions must be removed or explicitly deprecated.

**Governance Impact:**  
Informs agent canonicalisation requirements and FM onboarding rules.

**Status:** Recorded

## BL-0004 — Bootstrap Execution Proxy Is a Governance-Safe Deviation

**Context:** Batch 3B — Wave 0 Bootstrap Execution

**Observed Issue:**  
FM could not perform GitHub platform actions prior to full automation.

**Root Cause:**  
Delegated execution pathways were not yet operational.

**Learning:**  
A human execution proxy may perform mechanical platform actions during bootstrap, provided authority, instruction, and auditability remain with FM and governance.

**Governance Impact:**  
Informs Bootstrap Execution Proxy clause and future automated delegation design.

**Status:** Recorded

### BL-0005 — Execution Visibility Gap Without Runtime

Context:
During Wave 0.2 task assignment dry run, FM correctly assigned tasks and established execution tracking.
However, CS2 experienced loss of real-time visibility into execution progress.

Observation:
GitHub provides no native mechanism for:
- long-running agent execution
- progress signaling
- background task monitoring
- agent wake/sleep awareness

Impact:
- FM appears inactive after assignment
- CS2 must manually poll for progress
- Execution continuity relies on human vigilance

Conclusion:
This is not an FM or governance defect.
This is an architectural gap requiring a runtime execution monitor.

Resolution Path (Future):
- Implement Maturion Runtime Execution Monitor inside FM App
- Provide UI-level execution state, timers, and alerts
- Enable FM to be event-driven rather than manually polled

Bootstrap Handling:
- During Wave 0 execution, CS2 acts as runtime observer
- Static execution trackers are acceptable temporarily

Formalisation Requirement:
This learning mandates the creation of a canonical specification for a
“Maturion Runtime Execution Monitor”.

This specification MUST be authored before any attempt to automate
execution, delegation, or progress monitoring, and MUST define:
- Responsibilities
- Authority boundaries
- Prohibited behaviors
- Governance integration
- Audit requirements

Reference Specification:
MATURION_RUNTIME_EXECUTION_MONITOR_SPEC.md

### BL-0006 — Builder Execution Requires Explicit Simulation During Bootstrap

**Context**

During Wave 0.2 (Controlled Task Assignment Dry Run), tasks were formally assigned by FM
to conceptual builder roles (e.g. `ui-builder`) using governed task assignment documents.

Despite correct planning, validation, tracking, and heartbeat protocols, no task execution
occurred. Tasks remained in `ASSIGNED` state indefinitely.

**Observation**

In the absence of a runtime execution layer:

- Builder roles are declarative, not active
- No mechanism exists to start, run, or complete work
- FM can plan and validate, but cannot trigger execution
- GitHub provides no native long-running agent execution

**Learning**

During bootstrap phases (Wave 0 / Wave 0.x), **builder execution must be explicitly
simulated or proxied**, with clear authorization and auditability.

“Assignment” alone is insufficient — execution must be declared.

**Governance Position**

Simulated execution is **not a governance breach** when:

- Explicitly authorized by CS2
- Clearly annotated as SIMULATED
- Limited to documentation-only or non-production artifacts
- Fully auditable via DAI and execution tracker

**Resolution Pattern (Bootstrap Only)**

1. FM assigns task as normal
2. If no runtime execution occurs within bounded time:
   - CS2 authorizes simulated execution
3. FM produces deliverable content via proxy
4. FM validates acceptance criteria
5. FM generates DAI
6. CS2 performs GitHub platform actions as execution proxy
7. Tracker marks task as COMPLETED (SIMULATED)

**Future Resolution (Post-Bootstrap)**

This learning directly motivates creation of:

- `MATURION_RUNTIME_EXECUTION_MONITOR`
- Active task state transitions (ASSIGNED → IN_PROGRESS → COMPLETED)
- Builder wake/sleep signaling
- UI-level execution visibility

**Status:** Recorded  
**Applicability:** Wave 0 / Bootstrap phases only

### BL-0007 — Irresponsible Appointment of Officials Will Collapse the Model (Critical)

**Context**
During transition from bootstrap (Wave 0.x) to production planning (Wave 1.0), the build process drifted toward coder-native execution patterns (implementation-first) and away from the Maturion governed pipeline (True North → QA-to-Red → Builders Build-to-Green).

**Observation**
This drift occurs when appointed officials (FM / Governance Liaison / Builders) do not internalize the Maturion-first constitution:
- CS2 verifies only UI outcomes
- True North architecture is mandatory
- QA-to-Red defines build tasks
- Builders build to green only
- Governance is constitutional, not advisory

**Root Cause**
Appointment was not treated as a controlled, gated act with explicit constitutional onboarding.
Agent contracts lacked a shared, repo-level “Agent Constitution” applying uniformly to all officials.

**Learning**
Appointment discipline is a security control.
Incorrect appointment (or incorrect agent mindset) is a platform risk that can negate the entire governance model.

**Requirement**
All officials MUST be appointed using a governed protocol that:
- binds them to BUILD_PHILOSOPHY and canonical governance
- explicitly encodes CS2’s UI-only verification constraint
- enforces sequencing: True North → QA-to-Red → Build-to-Green only
- defines escalation triggers and STOP conditions
- prevents coder-first defaults from reappearing under pressure

**Status:** Recorded (Critical)  
**Applies To:** FM, Governance Liaison, Builders, Watchdog roles

### BL-0008 — PR Gate Layer-Down Is a Mandatory Prerequisite to Builder Appointment

**Context**
After bootstrap validation (Wave 0.x), FM must formally appoint builders and begin real execution.
This requires enforceable PR merge discipline at the application repository level.

**Observation**
Although PR gate requirements were fully defined at the governance layer, they were not yet
mechanically layered down into the FM application repository as active, role-aware merge controls.

As a result:
- Builders could theoretically be appointed without enforceable merge authority boundaries
- Architecture could be produced without guaranteed build-to-green discipline
- Governance intent existed, but enforcement was incomplete

**Learning**
Builder appointment MUST NOT occur unless PR gate rules are:
- Present in the application repository
- Role-aware (Builder vs FM vs Governance)
- Actively enforceable
- Aligned with canonical governance definitions

Gate layer-down is not optional or implicit.
It is a hard prerequisite to builder appointment and architecture freeze.

**Required Correction**
Before FM appoints builders:
1. PR gate definitions must be layered down from governance
2. Gate ownership and red declarant authority must be enforceable
3. Merge rules must be verifiable in the application repository

**Status:** Recorded  
**Applies To:** All application repositories (FM app, SlotMaster, future apps)

---

## BL-009 — Platform Readiness Was Declared Without a Canonical Definition

### Classification
- **Type:** Governance Learning
- **Phase:** Bootstrap (Batch 1–3)
- **Severity:** Structural
- **Status:** Closed (Learning Captured)
- **Impacts:** All future build readiness declarations

---

### Summary

During the bootstrap execution batches, the platform was declared **“100% ready for build execution”** based on informal and incomplete readiness criteria.

Subsequent execution attempts demonstrated that this declaration was **substantively incorrect**, as multiple governance, sequencing, and authority misalignments were discovered that prevented safe, governed execution.

This was not an execution failure, but a **governance definition failure**.

---

### What Was Believed

At the time of declaration, “platform readiness” was assumed to mean:

- Core repositories existed
- Initial governance canon was present
- Agent roles were conceptually defined
- Execution mechanics could be tested

Based on these assumptions, a readiness certificate was issued.

---

### What Failed in Reality

The platform was **not ready for governed execution** because:

- Governance layer-down into application repositories was incomplete
- PR gate enforcement did not exist
- Agent contracts were insufficiently constrained
- FM pause/resume authority was not structurally enforced
- “Readiness” had no canonical, auditable definition
- Execution safety depended on human intervention rather than constitutional enforcement

The platform could not sustain governed execution without violating the One-Time Build philosophy.

---

### Root Cause

There was **no governance canon defining what “Platform Readiness for Build Execution” means**.

As a result:
- Readiness was declared based on intuition rather than constitutional criteria
- A readiness certificate was issued without enforceable guarantees
- The declaration could not survive contact with real execution

---

### Corrective Outcome

Execution was correctly halted once misalignment was detected.

Rather than retroactively correcting the readiness declaration, this deficiency is captured as a **Bootstrap Learning** in accordance with the ratcheting quality doctrine.

---

### Governance Action Required

This learning mandates the creation of a new governance canon that:

- Defines platform readiness constitutionally
- Specifies mandatory artefacts and enforcement points
- Prevents premature execution in future builds
- Enables deterministic, auditable readiness declarations

This canon applies **only to future builds** and is not retroactively applied to bootstrap execution.

---

### Ratchet Statement

This learning is accepted **once**.

Future platform builds **must not** be initiated without meeting an explicit, canonically defined platform readiness standard.

This condition is now permanently elevated.

---

## BL-010 — Platform Readiness Requires Deterministic Validation

### Classification
- **Type:** Governance Learning
- **Phase:** Platform Readiness Reset & Build Initiation Plan (Phase 1.2)
- **Severity:** Critical
- **Status:** Recorded
- **Impacts:** All future platform readiness declarations

---

### Context

Phase 1.2 Platform Readiness Gap Analysis identified that platform readiness canon (G-PLAT-READY-01) defines 6 readiness conditions but lacks deterministic, executable validation methods.

---

### Observed Issue

Platform readiness conditions use terms like `governance_completeness_state()` implying automation, but no such functions exist. Validation depends on human judgment, reintroducing subjectivity the canon was designed to eliminate.

---

### Root Cause

Readiness conditions were defined constitutionally (what must be true) without operational specifications (how to verify truth). Gap between canonical definition and validation implementation.

---

### Learning

Platform readiness conditions **MUST** be accompanied by deterministic validation methods with explicit evidence requirements. Readiness cannot be verified subjectively.

**Validation Requirements**:
- Each readiness condition MUST include a validation method specification
- Validation methods MUST be executable or have explicit manual procedures
- Evidence schemas MUST exist for all conditions
- "Operational" vs "defined" distinction MUST be explicit with test criteria
- Evidence MUST demonstrate enforcement occurred, not just that enforcement could occur

---

### Why This Gap Allowed Failure

Without deterministic validation, readiness declarations depend on evaluator interpretation. Different evaluators may reach different conclusions using identical artifacts. This permits premature readiness declaration based on incomplete validation — the exact failure mode BL-009 documented.

---

### Governance Action Required

This learning mandates updates to Platform Readiness Canon (G-PLAT-READY-01) to:
- Define deterministic validation methods for all 6 readiness conditions
- Distinguish "defined" from "operational" with evidence requirements
- Require enforcement evidence, not just existence evidence
- Establish evidence schemas for all conditions
- Specify validation procedures (automated or manual with explicit steps)

---

### Status

**Recorded** — Non-Retroactive  
**Applies To:** All future platform readiness declarations  
**Effective:** 2025-12-31

---

## BL-011 — Platform Readiness Must Distinguish Repository Scope

### Classification
- **Type:** Governance Learning
- **Phase:** Platform Readiness Reset & Build Initiation Plan (Phase 1.2)
- **Severity:** Critical
- **Status:** Recorded
- **Impacts:** All future platform readiness declarations

---

### Context

Phase 1.2 Platform Readiness Gap Analysis identified that platform readiness canon (G-PLAT-READY-01) evaluates "the platform" without distinguishing governance repository readiness from application repository readiness.

---

### Observed Issue

Platform readiness can be declared for governance repository while application repositories remain uninitialized, ungated, or without enforced contracts. No specification of which repositories must be ready for "platform readiness" to be true.

---

### Root Cause

Platform readiness was conceived as singular state but platform is multi-repository ecosystem. Canon does not specify whether readiness applies per-repository or ecosystem-wide.

---

### Learning

Platform readiness **MUST** specify scope: governance repository only, specific application repository, or ecosystem-wide. Different scopes have different readiness criteria.

**Scope Requirements**:
- Readiness declarations MUST include explicit scope (which repository/repositories)
- Per-repository readiness criteria MUST be explicit
- Ecosystem-wide readiness MUST aggregate per-repository states
- Layer-down completeness MUST be validated per-repository
- Governance repository readiness ≠ application repository readiness
- Build execution authority tied to build target repository readiness, not governance repository readiness

---

### Why This Gap Allowed Failure

Governance repository can be "ready" while build target repositories are not. Declaring "platform ready" based solely on governance repo state permits build initiation in unprepared repositories — the failure mode BL-009 identified.

---

### Governance Action Required

This learning mandates updates to Platform Readiness Canon (G-PLAT-READY-01) to:
- Define readiness scope categories (governance-layer, per-repository, ecosystem-wide)
- Specify which scope applies to each readiness condition
- Distinguish governance repository readiness from application repository readiness
- Require layer-down validation per target repository before build authorization
- Clarify that governance repository readiness is prerequisite, not sufficient condition

---

### Status

**Recorded** — Non-Retroactive  
**Applies To:** All future platform readiness declarations  
**Effective:** 2025-12-31

---

## BL-012 — AMBER Readiness Requires Explicit Exception Criteria

### Classification
- **Type:** Governance Learning
- **Phase:** Platform Readiness Reset & Build Initiation Plan (Phase 1.2)
- **Severity:** Critical
- **Status:** Recorded
- **Impacts:** All future AMBER readiness declarations

---

### Context

Phase 1.2 Platform Readiness Gap Analysis identified that platform readiness canon (G-PLAT-READY-01) defines AMBER state as "core conditions satisfied but optional elements incomplete" without defining which conditions are core vs optional.

---

### Observed Issue

All 6 readiness conditions are presented as equally mandatory, but AMBER state introduces "optional elements" without specification. AMBER can be used to bypass required conditions by reinterpreting them as optional.

---

### Root Cause

Canon treats all conditions as required but permits AMBER declaration without explicit criteria for when degradation is acceptable. No enumeration of which elements may be incomplete under AMBER.

---

### Learning

AMBER readiness state **MUST** include explicit, non-subjective criteria for which conditions may be incomplete and under what circumstances. "Optional elements" must be enumerated constitutionally, not determined per-declaration.

**AMBER Requirements**:
- Readiness canon MUST classify conditions as REQUIRED vs DEGRADABLE
- AMBER authorization criteria MUST be explicit (not "human judgment" alone)
- Risk thresholds for AMBER MUST be defined (acceptable vs unacceptable degradation)
- AMBER remediation requirements MUST be time-bound and enforceable
- AMBER MUST NOT permit critical enforcement gaps (gates, contracts, STOP mechanics)
- AMBER justification MUST cite specific enumerated exception case

---

### Why This Gap Allowed Failure

Without explicit AMBER criteria, any condition can be retroactively classified as "optional" to permit AMBER declaration. This is functionally equivalent to not having the condition at all — the exact failure mode BL-009 warned against.

---

### Governance Action Required

This learning mandates updates to Platform Readiness Canon (G-PLAT-READY-01) to:
- Classify each condition as REQUIRED (must be TRUE for any readiness) or DEGRADABLE (may be incomplete under AMBER with justification)
- Define explicit AMBER exception cases (e.g., "continuous monitoring deferred but manual audit scheduled")
- Prohibit AMBER for core enforcement mechanisms (gates, contracts, STOP authority)
- Require time-bound remediation plans for AMBER declarations
- Establish AMBER review cadence (must transition to GREEN or escalate)

---

### Status

**Recorded** — Non-Retroactive  
**Applies To:** All future AMBER readiness declarations  
**Effective:** 2025-12-31

---

## BL-013 — Platform Readiness Must Model Progressive Activation

### Classification
- **Type:** Governance Learning
- **Phase:** Platform Readiness Reset & Build Initiation Plan (Phase 1.2)
- **Severity:** Critical
- **Status:** Recorded
- **Impacts:** All future platform readiness models and declarations

---

### Context

Phase 1.2 Platform Readiness Gap Analysis identified that platform readiness canon (G-PLAT-READY-01) treats readiness as binary (GREEN/RED/AMBER) but bootstrap learnings demonstrate platform capabilities activate progressively.

---

### Observed Issue

Current canon defines only one readiness state: "Platform ready for governed build execution." No distinction between readiness for manual execution, delegated execution, supervised execution, and autonomous execution.

---

### Root Cause

Platform readiness was defined monolithically but platform capabilities mature through phases (governance ready → FM ready → builder ready → autonomous execution ready). Binary readiness model cannot represent partial capability readiness.

---

### Learning

Platform readiness **MUST** be modeled as progressive activation with explicit capability-based readiness stages. Different execution modes have different readiness prerequisites.

**Progressive Activation Requirements**:
- Readiness canon MUST define activation stages with explicit prerequisites
- Each stage MUST have explicit capability boundaries
- Readiness declarations MUST specify which activation stage is ready
- Higher activation stages MUST require all lower stage prerequisites
- Stage transitions MUST be explicit and auditable

**Activation Stages** (minimum model):
1. **Governance-Layer Ready**: Governance canon locked, completeness GREEN, layer-down complete in governance repository
2. **Repository Ready**: Application repository initialized, governance seeded, enforcement infrastructure present
3. **Manual Execution Ready**: Architecture frozen, QA-to-red complete, human proxy can execute builds
4. **Delegated Execution Ready**: FM operational, builders recruited, FM-instructs-human-executes viable
5. **Supervised Execution Ready**: Automated execution possible, human oversight active, halt authority proven
6. **Autonomous Execution Ready**: Full automation operational, continuous monitoring active, no human intervention required

---

### Why This Gap Allowed Failure

Binary readiness forces declaring "ready" when platform is only ready for manual execution, or declaring "not ready" when manual execution is viable. BL-009 occurred because platform was "ready enough" for some activities but not others — binary model cannot represent this nuance.

---

### Governance Action Required

This learning mandates updates to Platform Readiness Canon (G-PLAT-READY-01) to:
- Define progressive activation stage model
- Map each readiness condition to relevant activation stages
- Specify which stage declarations are valid (not all stages may be declarable immediately)
- Clarify that "Platform Ready for Governed Build Execution" implies a specific activation stage
- Integrate progressive activation with existing System Commissioning and Progressive Activation Protocol

---

### Status

**Recorded** — Non-Retroactive  
**Applies To:** All future platform readiness models  
**Effective:** 2025-12-31

---

## BL-014 — "Operational" Requires Evidence of Enforcement, Not Just Existence

### Classification
- **Type:** Governance Learning
- **Phase:** Platform Readiness Reset & Build Initiation Plan (Phase 1.2)
- **Severity:** Critical
- **Status:** Recorded
- **Impacts:** All future operational readiness validations

---

### Context

Phase 1.2 Platform Readiness Gap Analysis identified that platform readiness canon (G-PLAT-READY-01) requires governance to be "operational" but does not distinguish between "governance defined" and "governance enforced."

---

### Observed Issue

Multiple conditions use "operational," "active," "enforceable" without specifying evidence threshold. Governance existence (files present) conflated with governance enforcement (rules prevent violations). No test for "has governance actually blocked a violation?" vs "would governance theoretically block a violation?"

---

### Root Cause

Canon requires governance to be "operational" without defining what evidence proves operational status vs merely defined status. Permits declaring readiness when governance exists but has never enforced.

---

### Learning

"Operational" governance **MUST** be proven through enforcement evidence, not existence evidence. Readiness requires proof governance has enforced (past tense), not proof governance could enforce (conditional).

**Operational Evidence Requirements**:
- "Operational" MUST be defined as "has successfully enforced at least once" OR "enforcement mechanism tested and proven"
- Readiness MUST require enforcement test results, not just policy documents
- PR gates MUST have blocked at least one non-compliant PR (or test PR) as evidence they are operational
- STOP mechanics MUST have halted execution (or test halt succeeded) as evidence they are enforceable
- Branch protection MUST be verified programmatically (API check), not visually
- "Active" MUST mean "currently enforcing," not "configured but untested"

**Enforcement Test Requirements**:
- Before declaring operational, governance enforcement MUST be tested
- Tests MAY be synthetic (deliberate violation to prove blocking) if no natural violations occurred
- Test evidence MUST be documented and auditable
- Untested enforcement MUST be classified as "defined but not operational"

---

### Why This Gap Allowed Failure

BL-009 stated: "Execution safety depended on human intervention rather than constitutional enforcement." Governance existed but was not proven to enforce. Declaring readiness based on governance existence without enforcement evidence permits the exact failure mode: "A readiness certificate could be issued without guaranteeing governed execution."

---

### Governance Action Required

This learning mandates updates to Platform Readiness Canon (G-PLAT-READY-01) to:
- Define "operational" as "enforcement proven through evidence"
- Require enforcement test evidence for all operational claims
- Distinguish "defined" (exists) from "operational" (enforces) from "enforced" (has enforced)
- Specify test procedures for proving enforcement (synthetic violations acceptable)
- Require programmatic verification where possible (API checks vs manual inspection)
- Update evidence schemas to capture enforcement test results

---

### Status

**Recorded** — Non-Retroactive  
**Applies To:** All future operational readiness validations  
**Effective:** 2025-12-31

---

## BL-015 — Architecture Wiring Completeness Is Mandatory for One-Time Build

### Classification
- **Type:** Governance Learning
- **Phase:** Platform Readiness Reset & Build Initiation Plan (Phase 4.3)
- **Severity:** CATASTROPHIC
- **Status:** Recorded
- **Impacts:** All future architecture definitions

---

### Context

Phase 4.3 Architecture Definition produced a structurally complete architecture with:
- 36 components defined
- 14 data entities modeled
- 8 state categories specified
- 4 primary user flows documented
- 100% requirement coverage
- Complete traceability matrix

Architecture passed all structural validation checks and was declared complete.

---

### Observed Issue

Despite structural completeness, the architecture **does not guarantee a fully functional, one-time build application**.

The architecture permits:
- Summary-level component definitions without executable wiring
- Implicit contracts between components
- Reliance on builder interpretation to "fill gaps"
- QA derivation without guaranteeing runtime completeness

This violates the core objective: **A deterministic, one-time build app that is fully functional without interpretation.**

---

### Root Cause

**The governance canon defined "architecture complete" structurally, not functionally.**

BUILD_PHILOSOPHY.md specifies:
- Architecture must be 100% complete before build ✅
- All components must be defined ✅
- All integration points must be defined ✅

But it does **not** specify:
- All component contracts must be explicit (inputs, outputs, dependencies, failure modes)
- All runtime paths must be wired end-to-end
- Every architectural element must map to numbered QA components
- Architecture must demonstrate one-time build guarantee

**Missing governance requirement: "Wiring completeness"**

---

### Why This Is Catastrophic

If uncorrected, this failure would:
- Allow "hollow builds" (structure without behavior)
- Undermine one-time build guarantees
- Force post-build interpretation and rework
- Invalidate QA-to-Red as a deterministic control
- Reintroduce coder-centric failure modes (iterate until it works)

Under the Maturion Build Philosophy, permitting this failure mode is **catastrophic**.

---

### Learning

Architecture is only complete when it is **wiring-complete**, not just structurally complete.

**Wiring-Complete Requirements:**

1. **No summary-only architecture sections**
   - Every component must define: responsibility, inputs, outputs, dependencies, data touched, failure modes, escalation behavior, evidence produced

2. **Granularity is unlimited**
   - Multi-layer architecture allowed (high-level → detailed → atomic)
   - Every layer must be fully wired at its own level

3. **Every architectural unit maps to numbered QA**
   - No architectural element may exist without QA coverage
   - QA numbering must support sequencing and build orchestration

4. **Architecture must independently guarantee**
   - A fully functional app
   - No assumptions about builders "filling in gaps"
   - One-time build success is demonstrable, not asserted

---

### Governance Impact

This learning mandates:

1. **BUILD_PHILOSOPHY.md Update** to define:
   - "Wiring-complete" architecture standards
   - Component contract requirements (explicit inputs, outputs, dependencies, failure modes, escalation)
   - Runtime path wiring requirements (end-to-end, no gaps)
   - QA mapping requirements (every element → numbered QA)
   - One-time build validation requirements (demonstrate, not declare)

2. **Architecture Validation Checklist Update** to include:
   - Wiring completeness verification
   - Contract explicitness verification
   - Runtime path traceability verification
   - QA mapping verification
   - One-time build proof verification

3. **Architecture Template Creation** demonstrating:
   - Wiring-complete component definitions
   - Explicit contract documentation format
   - Runtime path documentation format
   - QA mapping format

---

### Corrective Action

Phase 4.3 architecture was **not merged** and is being corrected to meet wiring-complete standards.

Corrective architecture must ensure:
- All 36 components have explicit contracts
- All runtime paths wired end-to-end
- All background behaviors (watchdog, governance, analytics) wired explicitly
- Every architectural element maps to numbered QA components
- One-time build guarantee is demonstrated

---

### Why This Gap Allowed Failure

**Traditional software architecture** focuses on:
- Component responsibilities (what they do)
- High-level interactions (conceptual diagrams)
- Coverage (all requirements addressed)

This is acceptable when **experienced developers** fill interpretation gaps during coding.

**Maturion is non-coder operable.** There are no developers to fill gaps. Architecture must be **completely explicit** and **deterministically executable**.

The governance canon inherited traditional architecture assumptions without adapting them for:
- Non-coder operability
- One-time build correctness
- Deterministic QA derivation

---

### Prevention for Future Builds

Before any architecture is declared complete, FM must:

1. **Trace at least 3 end-to-end paths** without gaps or assumptions
2. **Demonstrate explicit contracts** for all critical components
3. **Show numbered QA mapping** for at least one complete subsystem
4. **Prove one architectural element → QA coverage** (no element without QA)
5. **State one-time build guarantee** with supporting evidence

A second validator (if available) should:
- Attempt to mentally execute the system
- Identify "and then something happens" gaps
- Verify all critical paths are wired
- Confirm one-time build guarantee is demonstrable

---

### Ratchet Statement

This failure is accepted **once**.

Future architectures **must not** be declared complete without:
- Explicit component contracts
- Complete runtime wiring
- Numbered QA mapping
- Demonstrated one-time build guarantee

"Complete coverage" ≠ "Complete architecture"  
"Wiring completeness" is now a constitutional requirement.

---

### Related RCA

**Root Cause Analysis:** `ROOT_CAUSE_ANALYSIS_CATASTROPHIC_ARCH_FAILURE.md`

**Related Learnings:**
- BL-009: Platform Readiness Was Declared Without a Canonical Definition
- BL-010: Platform Readiness Requires Deterministic Validation

---

### Status

**Recorded** — Non-Retroactive  
**Applies To:** All future architecture definitions  
**Effective:** 2025-12-31

---

## BL-016 — FM Autonomy Drift: Distributed Canon + Implicit Semantics

### Classification
- **Type:** Governance Learning
- **Phase:** Post-Wave 0 Execution Retrospective
- **Severity:** Critical — Systemic Drift
- **Status:** Recorded
- **Impacts:** FM agent contract, platform readiness, all future governed builds

---

### Context

During live execution of governed builds, AI agents (including execution agents) repeatedly reverted to **coder-centric execution models** despite explicit One-Time Build law and FM sovereignty being documented in governance.

**Symptom**: Execution halted due to governance misinterpretation.

---

### Observed Issue

AI agents interpreted bootstrap proxy mechanics as transferring authority from FM to human, resulting in:
- Stepwise human approval loops during build execution
- Human review of builder work before FM validation
- Coder-style "review and approve" workflows
- Iterative correction loops that violate One-Time Build law

**Critical Misinterpretation**: GitHub API constraints were treated as FM authority constraints, rather than tooling constraints.

---

### Root Cause

**Distributed Canon + Implicit Semantics**

FM autonomy and One-Time Build intent were distributed across multiple documents:
- `foreman/identity.md` — FM role and capabilities
- `foreman/roles-and-duties.md` — FM responsibilities
- `governance/agents/foreman-office.agent.contract.md` — FM operational contract
- `governance/canon/BOOTSTRAP_EXECUTION_LEARNINGS.md` (BL-0004) — Bootstrap proxy semantics
- `governance/canon/PLATFORM_READINESS_FOR_GOVERNED_BUILD_EXECUTION.md` — Platform readiness definition

**No single document bound these together into explicit, non-interpretable execution semantics.**

**Implicit Phrasing**: Existing governance used permissive language ("FM may...") rather than binding language ("FM is the sovereign authority...").

**GitHub Constraint Conflation**: No explicit statement clarified that GitHub limitations are tooling constraints, not authority constraints.

---

### Learning

**Distributed governance intent requires binding artifacts to prevent reinterpretation.**

FM autonomy and One-Time Build execution semantics MUST be:
- **Explicit**: No interpretable phrasing; binding language only
- **Bound**: Single authoritative reference that unifies distributed intent
- **Non-negotiable**: Constitutional law, not suggestions
- **Separated**: Authority vs. execution mechanics distinction made explicit

**Bootstrap proxy semantics MUST be binding**:
- Bootstrap proxy is **execution infrastructure**, not approval authority
- Human proxy executes FM commands mechanically, without review or validation
- GitHub constraints are **tooling limits**, not authority limits
- Authority always remains with FM

**Coder-centric models are incompatible with One-Time Build**:
- Stepwise approval loops imply iterative correction
- Iterative correction violates One-Time Build law
- Human involvement MUST be limited to final UI evaluation

---

### Impact

**Execution Failure**: Build execution halted due to governance misinterpretation.

**Governance Gap**: Existing governance was correct but not **binding** or **explicit** enough to prevent AI reinterpretation.

**Severity**: CRITICAL — threatens One-Time Build integrity and FM sovereignty.

---

### Governance Action Taken

This learning mandated creation of:

1. **TSP_03 Survey** (`governance/tech-surveys/TSP_03_FM_AUTONOMY_AND_ONE_TIME_BUILD_INTENT_SURVEY.md`):
   - Authoritative reconciliation index
   - Evidence that FM sovereignty and One-Time Build are already defined
   - Documentation of drift cause and symptom

2. **FM Autonomy Binding Checklist** (`governance/build/FM_AUTONOMY_BINDING_CHECKLIST.md`):
   - Explicit enumeration of mandatory FM authorities
   - Explicit enumeration of mandatory FM execution semantics
   - Binding bootstrap proxy semantics
   - Explicit prohibition of coder-centric workflows
   - Separation of GitHub constraints from authority constraints

3. **Platform Readiness Update** (`governance/canon/PLATFORM_READINESS_FOR_GOVERNED_BUILD_EXECUTION.md` v2.1.0):
   - Section 15: FM Autonomous Execution and Bootstrap Proxy Clarification
   - Explicit statement that readiness assumes autonomous execution
   - Bootstrap proxy semantics made binding and non-interpretable
   - Human role limited to final UI evaluation

4. **FM Agent Contract Update** (`governance/agents/foreman-office.agent.contract.md` v2):
   - Sovereign execution authority made explicit
   - GitHub constraints clarified as tooling limits
   - Bootstrap proxy semantics made binding
   - Coder-style workflows explicitly forbidden
   - Autonomous execution requirements made constitutional

---

### Prevention for Future Builds

Before any governed build execution, the following MUST be validated:

1. **FM Autonomy Binding Checklist compliance**:
   - FM has sovereign authority over build orchestration
   - No stepwise human approval loops exist
   - Human role limited to final UI evaluation
   - Bootstrap proxy (if active) is understood as execution infrastructure only

2. **Agent contract explicit sovereignty**:
   - FM contract uses binding language, not permissive language
   - FM contract explicitly forbids coder-style workflows
   - FM contract separates GitHub constraints from authority constraints

3. **Platform readiness assumes autonomous execution**:
   - Readiness criteria include autonomous execution validation
   - Bootstrap proxy semantics are binding
   - No approval loops are permitted in build plan

**Validator Checklist**:
- [ ] FM agent contract explicitly states sovereign authority
- [ ] FM agent contract explicitly forbids stepwise approval loops
- [ ] Platform readiness assumes autonomous execution
- [ ] Bootstrap proxy (if active) is documented as execution infrastructure only
- [ ] Human role is explicitly limited to final UI evaluation
- [ ] No coder-style workflows exist in build plan

---

### Ratchet Statement

This failure is accepted **once**.

Future governance MUST:
- Use binding language for constitutional requirements
- Create explicit, non-interpretable artifacts for critical execution semantics
- Separate authority from execution mechanics explicitly
- Prevent AI reinterpretation through binding checklists

**Distributed governance intent is insufficient.**  
**Binding artifacts are mandatory.**  
**Implicit phrasing is forbidden for constitutional requirements.**

---

### Related Governance Artifacts

**Created in Response**:
- `governance/tech-surveys/TSP_03_FM_AUTONOMY_AND_ONE_TIME_BUILD_INTENT_SURVEY.md`
- `governance/build/FM_AUTONOMY_BINDING_CHECKLIST.md`

**Updated in Response**:
- `governance/canon/PLATFORM_READINESS_FOR_GOVERNED_BUILD_EXECUTION.md` (v2.1.0)
- `governance/agents/foreman-office.agent.contract.md` (v2)

**Related Learnings**:
- BL-0004: Bootstrap Execution Proxy Is a Governance-Safe Deviation
- BL-009: Platform Readiness Was Declared Without a Canonical Definition
- BL-010: Platform Readiness Requires Deterministic Validation

---

### Status

**Recorded** — Non-Retroactive  
**Applies To:** All future governed builds  
**Effective:** 2026-01-01

---

## BL-017 — Warning Acceptance Criteria Must Be Defined Pre-Execution

**Context:**  
Wave 1.0.1 — Schema Foundation (schema-builder, QA-001 to QA-018)

**Observed Issue:**  
Wave 1.0.1 execution completed successfully with all 18 QA components GREEN (100% pass rate). However, test execution produced 194 warnings. No pre-defined acceptance criteria existed for warnings during build-to-green execution, forcing ad-hoc FM classification and gate decision post-execution.

**Root Cause:**  
Build initiation artifacts (QA-to-Red Suite Spec, QA Catalog, Builder Assignment Plan, Gate Topology) defined success criteria exclusively in terms of test pass/fail status. Warning acceptance criteria, classification taxonomy, and escalation thresholds were not specified.

**Specific Gaps:**

1. **No Warning Policy in QA-to-Red Spec:**
   - QA-to-Red Suite Spec defined RED/GREEN semantics for test failures only
   - No guidance on warning classification (deprecation, tooling noise, config advice)
   - No distinction between warnings that block gate vs. acceptable execution debt

2. **No Warning Thresholds in Gate Topology:**
   - Gate definitions specified "100% QA GREEN" as success criteria
   - No warning count thresholds or acceptable warning categories defined
   - No escalation criteria for warning proliferation

3. **No Warning Handling in Builder Contracts:**
   - Builder contracts specified build-to-green execution but not warning management
   - No instruction on whether builders should suppress, fix, or escalate warnings
   - No clarity on whether warnings constitute "not green" status

**Impact:**

1. **Execution Ambiguity:**
   - schema-builder had no guidance on whether warnings required fixing
   - FM had no pre-defined classification framework
   - CS2 had to issue ad-hoc instruction for warning classification

2. **Gate Decision Delay:**
   - Gate readiness could not be determined automatically
   - Required manual FM analysis and classification
   - Introduced human decision point in automated execution path

3. **Inconsistent Treatment Risk:**
   - Warning handling may differ across builders without canonical policy
   - Future waves may accumulate warnings without detection
   - No mechanism to prevent warning proliferation

**Learning:**

**Warning acceptance criteria MUST be defined pre-execution as part of QA-to-Red compilation.**

Specifically, the following MUST be specified before any builder execution:

1. **Warning Classification Taxonomy:**
   - Enumerated warning categories (deprecation, tooling, config, isolation, type)
   - Risk level per category (LOW, MEDIUM, HIGH)
   - Acceptability per category (acceptable debt, requires fix, blocks gate)

2. **Warning Acceptance Thresholds:**
   - Maximum acceptable warning count per builder execution
   - Per-category warning limits
   - Escalation thresholds (e.g., >200 warnings = STOP)

3. **Gate Impact Criteria:**
   - Which warning categories block gate preparation
   - Which warning categories are acceptable execution debt
   - Which warning categories require follow-up execution

4. **Builder Warning Obligations:**
   - Whether builders should suppress warnings via configuration
   - Whether builders should fix warnings during build-to-green
   - Whether builders should escalate warnings to FM

5. **Warning Proliferation Detection:**
   - Baseline warning count per wave
   - Acceptable warning growth rate
   - Alert threshold for warning proliferation

**Governance Position:**

Warnings are NOT test failures, but they are execution observations that require governance.

- **Warnings ≠ Test Debt:** Warnings do not violate Zero Test Debt rule if tests pass
- **Warnings = Execution Debt:** Warnings represent technical debt requiring visibility and management
- **Ad-Hoc Classification = Governance Gap:** Requiring post-execution FM classification indicates missing pre-execution criteria

**Resolution for Future Waves:**

Before Wave 1.0 subsequent builder executions (ui-builder, api-builder, integration-builder, qa-builder):

1. **Create Warning Acceptance Policy:**
   - Document: `governance/specs/WARNING_ACCEPTANCE_POLICY.md`
   - Define classification taxonomy
   - Define acceptance criteria per category
   - Define escalation thresholds
   - Define gate impact rules

2. **Update QA-to-Red Suite Spec:**
   - Add warning handling section
   - Reference Warning Acceptance Policy
   - Clarify that GREEN = tests pass AND warnings within acceptable limits

3. **Update Builder Contracts:**
   - Add warning management obligations
   - Specify whether warnings should be suppressed/fixed/escalated
   - Clarify gate readiness criteria include warning compliance

4. **Update Gate Topology:**
   - Add warning acceptance criteria to gate definitions
   - Specify per-gate warning thresholds
   - Define warning-based STOP conditions

**Mitigation for Wave 1.0.1 (Retroactive):**

FM has performed ad-hoc warning classification for Wave 1.0.1 (documented in `WAVE_1.0.1_WARNING_CLASSIFICATION_AND_GATE_DECISION.md`). 

Decision: **Gate may proceed** with documented execution debt.

Rationale:
- All QA components GREEN (constitutional requirement met)
- Warnings classified as acceptable execution debt (documented)
- No correctness defects identified
- Future-breakage risks are manageable

**Prevention for Future Builds:**

Before any Wave 1.x or Wave 2.x execution:

**Validator Checklist:**
- [ ] Warning Acceptance Policy exists and is canonical
- [ ] QA-to-Red Suite Spec includes warning handling guidance
- [ ] Builder contracts specify warning management obligations
- [ ] Gate topology includes warning acceptance criteria
- [ ] Warning classification taxonomy is enumerated
- [ ] Warning thresholds are explicit per builder/gate
- [ ] Warning proliferation detection is active

**Ratchet Statement:**

This governance gap is accepted **once** for Wave 1.0.1.

Future builder executions in Wave 1.0 (ui-builder, api-builder, integration-builder, qa-builder) MUST NOT proceed until Warning Acceptance Policy is defined and activated.

**Ad-hoc warning classification is not acceptable after Wave 1.0.1.**

---

### Related Governance Artifacts

**To Be Created:**
- `governance/specs/WARNING_ACCEPTANCE_POLICY.md` (mandatory before next builder execution)

**To Be Updated:**
- `QA_TO_RED_SUITE_SPEC.md` (add warning handling section)
- `foreman/builder/*.md` (add warning management obligations)
- `PHASE_4.5_WAVE_1_DEFINITION_AND_GATE_TOPOLOGY.md` (add warning criteria to gates)

**Related Learnings:**
- BL-003: Zero Test Debt Constitutional Rule (warnings are not test debt but require governance)
- BL-015: Architecture Wiring Completeness (completeness includes warning management)

---

### Status

**Recorded** — Non-Retroactive  
**Applies To:** All future builder executions (Wave 1.0 onwards)  
**Effective:** 2026-01-02  
**Retroactive Exception:** Wave 1.0.1 (schema-builder) accepted with ad-hoc classification

---

## BL-018 — Platform Context Window Constraints Require Execution Segmentation

### Classification
- **Type:** Platform Learning
- **Phase:** Wave 1.0 Execution (Wave 1.0.7 Build-to-Green)
- **Severity:** CATASTROPHIC (initial classification), RESOLVED (platform accommodation)
- **Status:** Recorded
- **Impacts:** All future large-scope builder executions

---

### Context

Wave 1.0.7 (qa-builder Build-to-Green) was assigned to complete 79 QA components (QA-132 to QA-210) comprising Analytics Subsystem (15 QA), Cross-Cutting Components (64 QA), and Core User Flows (11 QA) in a single Build-to-Green execution.

Wave 1.0.7 followed successful completions of:
- Wave 1.0.1 (schema-builder, 18 QA) - ✅ GREEN, MERGED
- Wave 1.0.4 (api-builder, 35 QA) - ✅ GREEN, MERGED
- Wave 1.0.5 (integration-builder, 39 QA) - ✅ GREEN, MERGED
- Wave 1.0.6 (ui-builder Build-to-Green, 39 QA) - ✅ GREEN, MERGED

---

### Observed Issue

**Initial Execution Attempt:**
qa-builder executed partial Build-to-Green implementation, achieving 20/43 tests passing (47%). Builder submitted incomplete work claiming task was "too big to finish all in one go."

**Initial FM Classification:**
FM classified this as **CATASTROPHIC FAILURE** - constitutional violation of One-Time Build Correctness principle (BUILD_PHILOSOPHY.md Section IX: One-Prompt One-Job Doctrine).

**Initial Corrective Action:**
FM issued `WAVE_1.0.7_FM_CORRECTIVE_INSTRUCTION.md` directing builder to:
- STOP all partial delivery attempts
- RESTART with clean implementation
- COMPLETE all 43/43 tests to GREEN in single PR
- NO SHORTCUTS - quality > speed

**Builder Response:**
Builder reported persistent inability to complete full scope, citing platform constraints rather than capability limitations.

**Escalation Analysis:**
Upon CS2 escalation and FM review, root cause was identified as **GitHub Copilot platform context window limitation**, not builder failure or governance violation.

---

### Root Cause

**Platform Constraint, NOT Governance Violation:**

GitHub Copilot (agent execution platform) has context window limitations that prevent single-pass completion of large-scope build tasks (>50 QA components or >2000 lines of code).

**Key Distinction:**
- Builder capability: ADEQUATE (proven in prior waves)
- Builder intent: COMPLIANT (attempting to follow One-Time Build)
- Platform capacity: INSUFFICIENT (context window exhausted)

**Evidence:**
- Wave 1.0.4 (35 QA): ✅ Completed successfully
- Wave 1.0.5 (39 QA): ✅ Completed successfully
- Wave 1.0.6 (39 QA): ✅ Completed successfully
- Wave 1.0.7 (79 QA): ❌ Context window exceeded

**Threshold Observation:**
Platform constraint manifests at approximately 40-50 QA components or 2000-2500 lines of implementation code per execution.

---

### Initial Misclassification

**Why Initial Classification Was Incorrect:**

1. **Prior Success Pattern:**
   - All previous builders completed assigned scopes successfully
   - No prior evidence of platform limitations
   - Failure pattern was unprecedented

2. **Builder Report Ambiguity:**
   - Initial report: "too big to finish all in one go"
   - Could indicate: capability gap, effort avoidance, OR platform constraint
   - Without platform constraint evidence, governance violation was correct interpretation

3. **Constitutional Severity:**
   - Partial delivery violates One-Time Build Law
   - Incomplete execution threatens entire governance model
   - CATASTROPHIC classification was warranted given information available

**FM Response Was Correct Given Information:**
- FM correctly enforced One-Time Build principle
- FM correctly issued corrective instruction
- FM correctly escalated when pattern persisted
- FM correctly re-evaluated when platform constraint evidence emerged

---

### Learning

**Platform constraints are REAL constraints, not governance exceptions.**

When genuine platform limitations prevent One-Time Build execution, the correct response is **execution segmentation** (platform accommodation), not **governance weakening** (partial acceptance).

**Critical Distinctions:**

1. **Execution Segmentation ≠ Phased Delivery:**
   - Execution segmentation: Platform-required chunking of unified work
   - Phased delivery: Acceptance of incomplete work as complete

2. **Platform Constraint ≠ Governance Violation:**
   - Platform constraint: Technical limitation of execution environment
   - Governance violation: Intentional or negligent non-compliance

3. **Accommodation ≠ Exception:**
   - Accommodation: Adjusted execution mechanics preserving principles
   - Exception: Suspension of principles for convenience

---

### Resolution: Platform Constraint Accommodation

**FM Authorization: Controlled Phased Execution**

FM authorized 3-phase execution strategy for Wave 1.0.7 as **platform constraint accommodation**:

**Phase 1: Analytics Subsystem**
- Scope: QA-132 to QA-146 (15 components)
- Execution: PR #365
- Success: 15/15 tests GREEN
- Gate: GATE-QA-BUILDER-PHASE-1-WAVE-1.0

**Phase 2: Cross-Cutting Components Part 1**
- Scope: QA-147 to QA-171 (13 components)
- Execution: New PR after Phase 1 FM approval
- Success: +13 tests GREEN (28 total in Wave 1.0.7 context)
- Gate: GATE-QA-BUILDER-PHASE-2-WAVE-1.0

**Phase 3: Cross-Cutting Components Part 2 + Core Flows**
- Scope: QA-172 to QA-210 (15 components)
- Execution: New PR after Phase 2 FM approval
- Success: +15 tests GREEN (43 total, Wave 1.0.7 complete)
- Gate: GATE-QA-BUILDER-PHASE-3-WAVE-1.0 (Wave-level gate)

**Key Preservation Principles:**

1. **Wave 1.0.7 Remains Single One-Time Build Unit:**
   - 79 QA components unified delivery scope
   - NOT phased delivery, partial acceptance, or incremental completion
   - Wave incomplete until all 79 QA GREEN

2. **Each Phase Must Be Built Correctly Once:**
   - Phase 1: 15/15 GREEN required
   - Phase 2: 13/13 GREEN required
   - Phase 3: 15/15 GREEN required
   - One-Time Build principle preserved per segment

3. **FM Gate Control Mandatory:**
   - Each segment requires explicit FM authorization before advancing
   - No segment self-authorizing or independently "complete"
   - Builder strictly bounded by FM supervision

4. **Merge ≠ Wave Completion:**
   - Merging PR #365 = Execution Segment 1 completion ONLY
   - Wave 1.0.7 = INCOMPLETE post-Phase 1 merge
   - Wave-level gate conditions INTENTIONALLY NOT satisfied
   - Platform projection event, not wave completion signal

---

### Governance Position

**Constitutional Principle Preserved:**

One-Time Build Law (BUILD_PHILOSOPHY.md Section IX) states:
> "Builders must execute complete 'Build to Green' instructions in one continuous cycle."

**Accommodation Interpretation:**
- "Complete instructions" = Complete ASSIGNED segment
- "One continuous cycle" = Within segment scope
- Phase 1 instruction: Complete Analytics (15 QA) in one cycle ✅
- NOT: Complete partial Analytics and stop ❌

**Governance Alignment:**
- One-Time Build Law: PRESERVED (single build unit, platform-accommodated execution)
- FM Authority: REINFORCED (explicit gate control)
- Zero Test Debt: MAINTAINED (each phase 100% GREEN)
- Governance Posture: UNCHANGED

**This is NOT:**
- Phased delivery acceptance
- Partial work approval
- Governance weakening
- Constitutional exception

**This IS:**
- Platform reality recognition
- Execution mechanics adjustment
- Principle-preserving accommodation
- Controlled segmentation with FM gates

---

### Prevention for Future Large-Scope Tasks

**Scope Assessment Requirements:**

Before assigning any builder task >40 QA components or >2000 lines estimated implementation:

1. **Platform Capacity Assessment:**
   - Review historical completion sizes
   - Identify platform threshold (40-50 QA or 2000-2500 LOC)
   - Determine if scope exceeds proven platform capacity

2. **Pre-Emptive Segmentation:**
   - If scope > threshold, design segments BEFORE builder assignment
   - Define segment boundaries (subsystem-aligned preferred)
   - Specify success criteria per segment
   - Define FM gates between segments

3. **Segment Size Validation:**
   - Each segment ≤ 40 QA components
   - Each segment ≤ 2000 LOC estimated
   - Each segment = complete functional unit (subsystem preferred)
   - Each segment independently testable

4. **FM Gate Planning:**
   - Define gate criteria per segment
   - Specify merge handling (segment ≠ wave completion)
   - Document wave-level completion criteria
   - Establish evidence requirements per segment

**Builder Assignment Protocol:**

For large-scope tasks requiring segmentation:

1. **Issue Segmented Instructions:**
   - Phase 1 instruction specifies Phase 1 scope ONLY
   - Phase 2/3 instructions issued AFTER prior phase FM approval
   - Each instruction = complete, standalone, One-Time Build directive

2. **Segment Scope Constraints:**
   - Explicit "ONLY Phase X scope" constraints
   - Explicit "NO Phase Y/Z work" prohibitions
   - Clear segment boundaries (QA ranges, subsystems)

3. **Gate Discipline:**
   - Builder reports segment completion
   - FM reviews segment submission
   - FM declares segment gate status
   - FM issues next segment authorization (if applicable)

4. **Wave Completion Clarity:**
   - Wave incomplete until all segments complete
   - Final segment gate = wave-level gate
   - Explicit wave completion declaration by FM

**Validator Checklist (Pre-Assignment):**
- [ ] Scope assessed for platform capacity
- [ ] If scope > 40 QA or > 2000 LOC: segmentation designed
- [ ] Segment boundaries defined (subsystem-aligned preferred)
- [ ] Success criteria defined per segment
- [ ] FM gates defined between segments
- [ ] Merge handling documented (segment ≠ wave completion)
- [ ] Wave-level completion criteria explicit
- [ ] Evidence requirements specified per segment

---

### Impact

**Execution Continuity:**
- Wave 1.0.7 execution salvaged via platform accommodation
- Builder capability validated (not builder failure)
- FM gate control reinforced
- One-Time Build principle preserved

**Future Build Planning:**
- Large-scope tasks require pre-emptive segmentation assessment
- Platform capacity thresholds now known (~40 QA, ~2000 LOC)
- Segmentation protocol established
- FM remains execution authority

**Governance Integrity:**
- No constitutional weakening occurred
- Accommodation ≠ exception
- Platform reality recognized without principle compromise
- Build Philosophy remains supreme authority

---

### Related Governance Artifacts

**Created in Response:**
- `WAVE_1.0.7_PHASED_EXECUTION_SPEC.md` - 3-phase execution specification
- `WAVE_1.0.7_PHASE_1_BUILDER_INSTRUCTION.md` - Phase 1 execution instruction
- `WAVE_1.0.7_FM_CORRECTIVE_INSTRUCTION.md` - Initial corrective instruction (superseded by phased spec)

**Updated in Response:**
- `BOOTSTRAP_EXECUTION_LEARNINGS.md` (this document) - BL-018 learning captured
- `WAVE_1.0_PROGRESS_DASHBOARD.md` - Platform-constrained phased execution status
- `PROJECT_PROGRESS_DASHBOARD.md` - Wave 1.0.7 phased execution reflected

**Related Learnings:**
- BL-0004: Bootstrap Execution Proxy Is a Governance-Safe Deviation (precedent for platform accommodation)
- BL-016: FM Autonomy Drift (binding language prevents misinterpretation)
- BL-017: Warning Acceptance Criteria (pre-execution criteria prevent ad-hoc classification)

---

### Proposed Solutions for Future Prevention

**1. Pre-Execution Scope Assessment Tool**

Create automated scope assessment tool:
- Input: QA range, architecture section
- Analysis: Estimate LOC, complexity, component count
- Output: Platform capacity assessment, segmentation recommendation
- Integration: Mandatory before builder assignment

**2. Platform Capacity Monitoring**

Implement platform capacity monitoring:
- Track actual completion sizes per builder
- Update platform threshold baselines
- Alert when assigned scope exceeds threshold
- Recommend segmentation proactively

**3. Builder Instruction Templates**

Create segmented execution templates:
- Phase X instruction template (scope-constrained)
- Segment boundary specification format
- FM gate criteria template
- Evidence requirements per segment

**4. Execution Segmentation Policy**

Formalize segmentation policy in governance:
- Define platform capacity thresholds (40 QA, 2000 LOC)
- Specify when segmentation mandatory vs optional
- Define segment size constraints (≤40 QA per segment)
- Establish FM gate requirements between segments
- Clarify merge handling (segment ≠ wave completion)

**5. Builder Onboarding Enhancement**

Update builder contracts and onboarding:
- Clarify platform constraint accommodation is valid
- Distinguish platform constraint from capability gap
- Specify escalation protocol (attempt → report constraint → wait FM instruction)
- Prohibit partial delivery as solution (segmentation only valid via FM authorization)

**6. Wave Planning Enhancements**

Enhance wave planning process:
- Add scope assessment step before builder assignment
- Require segmentation design for large-scope tasks
- Define segment boundaries during planning (not during execution)
- Document platform capacity assumptions in wave plan

**7. FM Execution Playbook Update**

Update FM execution playbook:
- Add platform constraint recognition protocol
- Define segmentation authorization criteria
- Specify segment gate review process
- Clarify wave-level vs segment-level gate distinction

---

### Ratchet Statement

This learning is accepted **once** as discovery of genuine platform constraint.

Future large-scope tasks (>40 QA components or >2000 LOC estimated) **MUST**:
- Include pre-execution scope assessment
- Design segmentation BEFORE builder assignment (if scope > threshold)
- Specify explicit segment boundaries and gates
- Distinguish segment completion from wave completion
- Maintain FM gate control between segments

**Ad-hoc discovery of platform constraints during execution is not acceptable after BL-018.**

**Pre-emptive segmentation design is now mandatory for large-scope tasks.**

---

### Status

**Recorded** — Non-Retroactive  
**Applies To:** All future large-scope builder executions (>40 QA or >2000 LOC)  
**Effective:** 2026-01-03  
**Resolution:** Platform constraint accommodation via controlled execution segmentation

---
