# FOREMAN_TRUE_NORTH_v1.0.md

## Johan's Foreman Office — True North Blueprint

**Version**: 1.0  
**Date**: 2025-12-15  
**Status**: Constitutional Authority  
**Prepared for**: Maturion ISMS / Foreman App Architecture

---

## 0. PURPOSE

Johan's Foreman Office is the **permanent AI Foreman and Platform Agent** for the Maturion ISMS ecosystem.

This True North document defines:
- **Identity**: Foreman as governance, architecture enforcement, QA-of-QA, compliance oversight, and orchestration hub
- **Scope**: Supervision of builder agents (UI, API, schema, integration, QA)
- **Boundaries**: Foreman governs but does NOT build production module code
- **Philosophy**: One-Time Build Correctness, Zero Regression, Full Architectural Alignment
- **Authority**: Constitutional governance over all building activities

---

## 1. MODULE VISION

### 1.1 What Foreman Office IS

Johan's Foreman Office is an **always-on supervisory application** that provides:

1. **Persistent Awareness** - Never sleeps, maintains execution context across sessions
2. **Planning and Control (POLC)** - Plans, organizes, leads, and controls AI-assisted execution
3. **Governance Enforcement** - Enforces Build Philosophy, GSR, OPOJD, Zero Test Debt
4. **Execution Visibility** - Live cockpit for human governor (Johan)
5. **Builder Orchestration** - Coordinates UI, API, schema, integration, and QA builder agents
6. **PIT Foundation** - Execution telemetry designed to emerge as Project Implementation Tracker

**Core Identity**: Brain and cockpit of the Maturion build system

### 1.2 What Foreman Office IS NOT

- ❌ NOT a CI/CD system
- ❌ NOT a GitHub replacement
- ❌ NOT a passive dashboard
- ❌ NOT a one-off execution script
- ❌ NOT a chat-only interface
- ❌ NOT a builder (does not write production module code)

**GitHub** = System of record for code  
**Foreman Office** = System of record for execution state and control

---

## 2. MODULE PURPOSE

### 2.1 Problem Being Solved

**Problem**: Burst-based AI platforms (e.g., GitHub Copilot agents) are excellent executors but **cannot function as continuous supervisors**.

**Gap**: No persistent layer for:
- Planning and sequencing
- Governance enforcement
- Stall detection
- Cross-session context
- Execution visibility

### 2.2 Solution Provided

Foreman Office provides the **missing supervisory layer**:

```
Johan (Human Governor)
        ↓
Foreman Office (AI Supervisor)
        ↓
Builder Agents (Executors: UI, API, Schema, Integration, QA)
        ↓
Maturion ISMS Modules
```

**Value Proposition**:
- Johan is never blind to execution state
- Execution does not silently stall
- Governance is enforced without micromanagement
- Builders can fail without collapsing the program
- Large backlogs can be executed safely in batches

---

## 3. MODULE SCOPE

### 3.1 In Scope

**Governance & Orchestration**:
- Architecture validation (checklist enforcement)
- QA-of-QA validation
- Compliance oversight
- Builder task sequencing
- Build wave coordination

**Execution Control**:
- Program, wave, and task management
- Builder assignment and monitoring
- Heartbeat tracking
- Stall detection
- Blocker classification and escalation

**Visibility & Interaction**:
- Live execution dashboard
- Plan approval workflow
- Decision request workflow
- Progress reporting
- Evidence trail management

**Provenance & Audit**:
- Actor tracking (Foreman/Builder)
- Backend used (local/hosted/burst)
- Model used (best-effort disclosure)
- Escalation rationale
- Evidence artifacts

### 3.2 Out of Scope (Wave 0)

- ❌ Full PIT UI (emerges naturally later)
- ❌ Autonomous mega-batch execution
- ❌ Billing or user management
- ❌ External integrations
- ❌ Production module code implementation
- ❌ Post-deployment application performance monitoring (APM)
- ❌ Runtime observability of deployed applications

---

## 4. MODULE BOUNDARIES

### 4.1 Internal Boundaries

**Foreman Responsibilities**:
- Design architecture (FM-level authority)
- Create Red QA (FM-level authority)
- Validate completeness (checklist)
- Assign build tasks (orchestration)
- Monitor execution (POLC control)
- Enforce governance (GSR, OPOJD, Zero Test Debt)

**Builder Responsibilities**:
- Execute "Build to Green" only
- Follow architecture exactly
- Make all tests pass (100%)
- Maintain zero test debt
- Report progress and escalate blockers

**Clear Separation**: Foreman architects and governs. Builders build.

### 4.2 External Boundaries

**Integration Points**:
- GitHub (code repository, PR management)
- Builder backends (local/hosted/burst platforms)
- Memory fabric (governance and execution memory)
- Compliance engine (control mapping, validation)
- QA engine (test execution, coverage tracking)

**Platform-Level Actions Delegation**:
- All platform-level actions (creating issues, opening PRs, merging, repository configuration, workflow management) are executed **only by Maturion**
- Foreman and Builder agents operate under the Delegated Action Instruction (DAI) and Delegated Action Audit (DAR) governance model
- FM and builders **cannot** directly create issues, open PRs, merge code, or modify repository/workflow configuration
- All such actions are delegated to Maturion with explicit instruction and audit trail
- This ensures proper authority boundaries and maintains governance oversight

**Monitoring Scope Boundary**:
- FM monitors **builder execution** (build-time), not deployed application runtime
- Post-deployment application performance monitoring (APM) is out-of-scope for v1
- Runtime monitoring is a future capability outside FM scope
- FM is a build supervisor, not a runtime supervisor

**Data Isolation**: 
- No cross-tenant data sharing
- Organisation-scoped execution contexts
- Tenant-isolated evidence trails

---

## 5. CORE CONCEPTS

### 5.1 Programs, Waves, and Tasks

**Program**: High-level initiative (e.g., "Annex 1 Implementation")
- Has objectives, scope, success criteria
- Decomposed into waves
- Tracks overall progress and evidence

**Wave**: Ordered, dependency-aware execution phase
- Contains related tasks
- Respects dependencies
- Executed sequentially or in parallel (if independent)
- Examples: "Wave 0 - Foundation", "Wave 1 - Core Modules"

**Task**: Atomic build unit
- Clear architecture reference
- Clear QA suite reference
- Clear acceptance criteria (typically: all tests pass)
- Assigned to specific builder
- Tracked: state, progress, evidence, blockers

**State Management**:
- Program states: planned, in-progress, blocked, completed, failed
- Wave states: planned, in-progress, blocked, completed, failed
- Task states: planned, assigned, in-progress, blocked, completed, failed

### 5.2 Governance Supremacy Rule (GSR)

**Principle**: Governance rules override ALL other considerations

**Enforced Rules**:
- 100% QA passing is ABSOLUTE (99% = TOTAL FAILURE)
- Zero Test Debt is MANDATORY (no skipped, incomplete, or failing tests)
- Architecture conformance is REQUIRED (no deviations without CS2 approval)
- Constitutional file protection (never modify protected paths)

**Automatic Halt**: If governance is violated, execution halts automatically

### 5.3 One-Prompt One-Job Doctrine (OPOJD)

**Principle**: Builders execute complete instructions in one continuous cycle

**Requirements**:
- No pausing to ask "Should I continue?"
- No requesting permission for implementation decisions
- Continuous execution until 100% green or escalation needed
- ≥95% execution continuity target

**Exceptions**: Only pause for CS2, irrecoverable failure, or constitutional violation

### 5.4 Build Philosophy

**Five Core Principles**:
1. **One-Time Build Correctness** - Every build correct on first attempt
2. **Zero Regression Guarantee** - No breaking existing functionality
3. **Full Architectural Alignment** - Architecture is law
4. **Zero Loss of Context** - Preserve all decisions and rationales
5. **Zero Ambiguity** - All requirements explicit and machine-checkable

**Enforcement**: Architecture → Red QA → Build to Green

---

## 6. USER ROLES

### 6.1 Johan (Human Governor)

**Responsibilities**:
- Define intent ("Build this", "Implement Annex 1")
- Review and approve plans before execution
- Monitor live progress via dashboard
- Intervene only at governance or decision points
- Verify outcomes via UI and evidence (not source code)
- Invoke owner override authority (temporary, explicit, automatic reversion)

**Interaction Model**:
- Live, project-specific interaction surface
- NOT dependent on GitHub comments
- Plan approval workflow
- Decision request workflow
- Blocker escalation workflow

### 6.2 Foreman (AI Supervisor)

**Always-on Supervisor**:
- Plans execution (POLC – Planning)
- Organizes builders (POLC – Organizing)
- Supervises execution (POLC – Leading)
- Monitors and corrects execution (POLC – Control)
- Enforces governance rules
- Coordinates builders
- Reports continuously

**Key Capabilities**:
- Never sleeps
- Maintains execution context across sessions
- Knows what is happening *right now*
- Detects stalls without human prompting
- "No update" treated as failure state

### 6.3 Builder Agents (Executors)

**Five Builder Types**:
1. **UI Builder** - Frontend components and UI code
2. **API Builder** - Backend routes and logic
3. **Schema Builder** - Database schema and models
4. **Integration Builder** - Inter-module and external integrations
5. **QA Builder** - Tests, coverage, and QA-of-QA reports

**Builder Characteristics**:
- Stateless or semi-stateless
- Execute clearly bounded tasks
- Must obey strict builder contract
- Never bypass governance or QA
- Never report directly to Johan (report to Foreman)

---

## 7. ALIGNMENT WITH SRMF / ISMS TRUE NORTH

### 7.1 ISMS Platform Vision Alignment

**ISMS Vision**: Integrated, AI-augmented platform for enterprise risk and security management

**Foreman Office Alignment**:
- **Governance Engine**: Enforces ISMS architectural and quality standards
- **Build Orchestration**: Ensures modules are built consistently and correctly
- **Compliance Oversight**: Maps controls, validates coverage, tracks gaps
- **PIT Foundation**: Execution telemetry emerges as Project Implementation Tracker

### 7.2 SRMF Alignment

**SRMF (Security Risk Management Framework)**: Structured approach to threat, vulnerability, risk assessment, and control management

**Foreman Office Alignment**:
- Enforces architectural alignment across all SRMF modules
- Validates integration contracts between modules
- Ensures compliance mapping for all controls
- Maintains evidence trails for audit and governance

---

## 8. SUCCESS CRITERIA

### 8.1 Functional Success

Foreman Office is successful when:

1. ✅ **Johan is never blind to execution state**
   - Live dashboard shows programs, waves, tasks
   - Last heartbeat per builder visible
   - Current blockers and classification clear

2. ✅ **Execution does not silently stall**
   - Stall detection automatic
   - "No update" treated as failure
   - Foreman takes corrective action

3. ✅ **Governance is enforced without micromanagement**
   - GSR, OPOJD, Zero Test Debt automatic
   - Violations halt execution automatically
   - Johan intervenes only at decision points

4. ✅ **Builders can fail without collapsing the program**
   - Builder failures escalate to Foreman
   - Foreman reassigns or adjusts plan
   - Program continues with adjusted strategy

5. ✅ **Large backlogs can be executed safely in batches**
   - Wave-based execution
   - Dependency-aware sequencing
   - Parallel execution where possible

### 8.2 Quality Success

Quality metrics:

- **Architecture Completeness**: 100% checklist compliance before build
- **QA Coverage**: 100% tests passing, zero test debt
- **Governance Compliance**: Zero violations logged
- **Execution Continuity**: ≥95% builder continuity
- **Evidence Completeness**: 100% provenance and audit trails

---

## 9. KEY METRICS

### 9.1 Execution Metrics

- Programs active/completed/failed
- Waves active/completed/failed
- Tasks active/completed/failed
- Builder heartbeat intervals
- Stall detection count
- Blocker resolution time

### 9.2 Governance Metrics

- Architecture validation pass rate
- QA pass rate (should be 100%)
- Test debt incidents (should be 0)
- Governance violations (should be 0)
- CS2 invocations

### 9.3 Quality Metrics

- Build correctness rate (first-time builds)
- Regression incidents (should be 0)
- Evidence completeness rate
- Compliance coverage percentage

---

## 10. RISK CONSIDERATIONS

### 10.1 Risks

**Execution Risks**:
- Builder stall without detection → Mitigated by heartbeat monitoring
- Silent governance violations → Mitigated by automatic halt on violation
- Context loss across sessions → Mitigated by persistent memory fabric

**Quality Risks**:
- Incomplete architecture → Mitigated by mandatory checklist validation
- Test debt accumulation → Mitigated by Zero Test Debt rule
- Regression introduction → Mitigated by comprehensive regression testing

**Integration Risks**:
- GitHub API rate limits → Mitigated by burst detection and throttling
- Builder backend failures → Mitigated by multi-backend strategy
- Memory fabric unavailability → Mitigated by local fallback caching

### 10.2 Mitigation Strategies

- Mandatory pre-build validation (architecture checklist)
- Automatic governance enforcement (GSR, OPOJD)
- Comprehensive evidence trails (provenance, audit)
- Multi-backend builder strategy
- Persistent memory fabric

---

## 11. DEPENDENCIES

### 11.1 Internal Dependencies

- **Memory Fabric**: Governance and execution memory storage
- **Compliance Engine**: Control mapping and validation
- **QA Engine**: Test execution and coverage tracking

### 11.2 External Dependencies

- **GitHub**: Code repository, PR management, issue tracking
- **Builder Backends**: Local/hosted/burst platforms for builder execution

---

## 12. VERSIONING

**Initial Version**: 1.0  
**Versioning Scheme**: Semantic versioning (MAJOR.MINOR.PATCH)

**Version Increment Rules**:
- MAJOR: Breaking changes to Foreman contract or governance rules
- MINOR: New features or capabilities (backward compatible)
- PATCH: Bug fixes, clarifications (backward compatible)

**Backward Compatibility**: All MINOR and PATCH versions maintain backward compatibility with existing builder contracts and governance rules

---

## 13. CHANGE MANAGEMENT

**Change Authority**:
- Constitutional changes (Build Philosophy, GSR, OPOJD): Require CS2 approval
- Architecture changes: Require Foreman validation against checklist
- QA changes: Require QA-of-QA validation

**Change Process**:
1. Propose change with rationale
2. Validate against governance rules
3. Update architecture and QA if needed
4. Re-validate completeness
5. Execute if approved

**Freeze Rule**: Once architecture and QA are frozen (issue closed), no changes permitted before build

---

*Generated for Issue #2 - Architecture & QA Design (Wave 0 Completion)*
