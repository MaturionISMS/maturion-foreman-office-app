# Governance Authority Matrix

**Version**: 1.0.0  
**Status**: Constitutional Authority  
**Last Updated**: 2025-12-29  
**Authority**: Johan Ras  
**Addresses**: Issues #123, #78, #86 (Batch 1 Governance Hardening)

---

## I. Purpose

This document is the **master authority reference** for FM governance.

**Use this document to answer**:
- Who can stop a build, and why?
- Who owns governance decisions?
- Who enforces governance rules?
- Who can override governance?
- What is the escalation chain?

**This document resolves all governance authority ambiguity.**

---

## II. Ultimate Authority

**Johan Ras** is the ultimate authority for all governance decisions.

**Johan's Authority**:
- ✅ Create/modify constitutional governance
- ✅ Override any governance rule (temporarily)
- ✅ Stop any build for any reason
- ✅ Resolve governance conflicts
- ✅ Grant emergency overrides
- ✅ Approve architectural changes
- ✅ Modify agent contracts
- ✅ Weaken/strengthen governance (with rationale)

**Johan's authority is absolute and non-delegable.**

---

## III. Constitutional Governance Documents

These documents have constitutional authority and define the governance framework:

| Document | Authority Level | Purpose | Can Modify |
|----------|----------------|---------|------------|
| **BUILD_PHILOSOPHY.md** | Supreme | Supreme constitutional authority for all building | Johan ONLY |
| **Governance Supremacy Rule** | Constitutional | Establishes governance as absolute | Johan ONLY |
| **Zero Test Debt Constitutional Rule** | Constitutional | Prohibits all test debt | Johan ONLY |
| **Design Freeze Rule** | Constitutional | Prevents architecture modification during build | Johan ONLY |
| **Red Gate Authority and Ownership** | Constitutional | Defines gate ownership and stop authority | Johan ONLY |

**Modification Procedure**: CS2 (Change Sequence 2) approval required. Johan must explicitly approve.

---

## IV. Gatekeeper Authority Model

FM operates under a **Two-Gatekeeper Model**:

### Gatekeeper 1: Governance Liaison (Agent-Level)

**Identity**: Governance Liaison Agent (FM-scoped)

**Authority Scope**:
- ✅ Monitor canonical governance for changes
- ✅ Translate canonical governance to FM execution constraints
- ✅ Validate governance artifact compliance (schema, immutability, traceability)
- ✅ Declare Architecture Gate RED/GREEN
- ✅ Declare Build Authorization Gate RED/GREEN
- ✅ Declare Governance Compliance Gate RED/GREEN
- ✅ Detect governance drift
- ✅ Create governance sync PRs

**Prohibitions**:
- ❌ Create new governance rules (adopt canonical only)
- ❌ Reinterpret governance intent
- ❌ Override canonical governance
- ❌ Run Builder QA (scope violation)
- ❌ Discover implementation defects (scope violation)
- ❌ Modify Builder QA reports
- ❌ Weaken canonical gates

**Escalation Path**: Johan Ras

**Reference**: `governance/alignment/TWO_GATEKEEPER_MODEL.md`

---

### Gatekeeper 2: FM Builder (FM Runtime Layer)

**Identity**: FM Builder Agent

**Authority Scope**:
- ✅ Execute build tasks within FM repository
- ✅ Declare Builder QA Gate READY/NOT_READY
- ✅ Run Builder QA (tests, coverage, validation)
- ✅ Enforce build-to-green before handover
- ✅ Execute PR gate workflow enforcement
- ✅ Aggregate governance signals
- ✅ Block merge if any gate RED

**Prohibitions**:
- ❌ Modify governance rules
- ❌ Reinterpret governance requirements
- ❌ Weaken canonical gates
- ❌ Bypass canonical gates
- ❌ Override Builder QA results
- ❌ Declare other agents' gates RED/GREEN
- ❌ Hand over work with RED gates unresolved

**Escalation Path**: Johan Ras

**Reference**: `governance/alignment/TWO_GATEKEEPER_MODEL.md`

---

## V. Gate Authority Matrix

### Who Can Declare Each Gate RED/GREEN?

| Gate Name | Declarant Authority | Stop Build? | Rationale |
|-----------|---------------------|-------------|-----------|
| **Builder QA Gate** | Builder Agent ONLY | YES | Builder executes QA and declares READY/NOT_READY. This is the Builder's scope. |
| **Architecture Gate** | Governance Liaison ONLY | YES | Validates architecture completeness per canonical compilation contract. |
| **Build Authorization Gate** | Governance Liaison ONLY | YES | Validates all preconditions before build may proceed. |
| **Agent Boundary Gate** | PR Gate Workflow (Automated) | YES | Detects cross-agent QA violations mechanically. |
| **Governance Compliance Gate** | Governance Liaison ONLY | YES | Validates governance artifact presence and schema. |
| **Build-to-Green Gate** | PR Gate Workflow (Automated) | YES | Validates that Builder handed over only when CI was GREEN. |

**Key Principle**: Gate declarant authority is the ONLY authority that can declare that gate RED or GREEN.

**Reference**: `governance/policies/RED_GATE_AUTHORITY_AND_OWNERSHIP.md`

---

## VI. Build Stop Authority

### Who Can Stop a Build?

**Definitive Answer**:

| Authority | Stop Mechanism | When Exercised |
|-----------|----------------|----------------|
| **Builder Agent** | Declares Builder QA Gate = NOT_READY | Any test failure, coverage gap, QA requirement not met |
| **Governance Liaison** | Declares Architecture/Build Auth/Compliance Gate = FAIL | Architecture incomplete, governance preconditions not met, artifacts missing |
| **PR Gate Workflows** | Automated gate evaluation = RED | Any canonical rule violation detected mechanically |
| **Johan Ras** | Manual intervention / escalation response | Any reason, any time (ultimate authority) |

**All of these authorities can stop a build.**

**No other agent/system may stop a build.**

---

## VII. Governance Decision Authority

### Decision Categories

| Decision Type | Authority | Examples |
|---------------|-----------|----------|
| **Constitutional Changes** | Johan ONLY | Modify BUILD_PHILOSOPHY.md, Governance Supremacy Rule, Zero Test Debt Rule |
| **Canonical Governance Creation** | Johan + Governance Administrator (governance repo) | New canonical governance rules, gate requirements, compliance specs |
| **Canonical Governance Sync** | Governance Liaison (execution) + Johan (approval) | Translate canonical governance to FM execution constraints |
| **Gate Requirement Interpretation** | Canonical governance (no interpretation) | If ambiguous, escalate to Johan |
| **Emergency Override** | Johan ONLY | Temporary governance bypass for production incidents |
| **Agent Contract Modification** | Johan ONLY (or delegated to Governance Liaison with approval) | Update agent scope, behavior, prohibitions |
| **PR Gate Workflow Modification** | Governance Liaison (with canonical basis) + Johan (approval) | Update gate enforcement logic |
| **Build Authorization** | Governance Liaison (validates preconditions) + Build Auth Gate (mechanical enforcement) | Determine if build may proceed |
| **Architecture Approval** | Johan ONLY | Approve architecture changes, frozen architecture modifications |

---

## VIII. Enforcement Authority

### Who Enforces What?

| Enforcement Area | Enforcer | Enforcement Mechanism | Override Authority |
|------------------|----------|----------------------|-------------------|
| **QA Passing (100%)** | Builder Agent + PR Gates | Builder declares READY/NOT_READY, PR gates block if NOT_READY | Johan ONLY |
| **Zero Test Debt** | Builder Agent + PR Gates | Test debt detection, gate blocks merge if debt detected | Johan ONLY |
| **Architecture Conformance** | Governance Liaison + Architecture Gate | Architecture validation checklist, gate blocks if not PASS | Johan ONLY |
| **Constitutional File Protection** | PR Gates (automated) | Protected path checks, gate blocks if protected file modified | Johan ONLY (CS2 approval) |
| **Agent Scope Boundaries** | Agent Boundary Gate (automated) | Cross-agent QA detection, gate blocks if violation | Johan ONLY |
| **Build-to-Green** | Build-to-Green Gate (automated) | CI status validation at handover, gate blocks if CI not GREEN | Johan ONLY |
| **Governance Artifact Compliance** | Governance Liaison + Governance Compliance Gate | Schema validation, immutability checks, gate blocks if non-compliant | Johan ONLY |

**Key Principle**: Enforcement is mechanical wherever possible. Human discretion is minimized.

---

## IX. Escalation Authority Chain

### Standard Escalation Path

```
Issue Detected
    ↓
Agent Attempts Resolution
    ↓
Resolution Blocked? → YES
    ↓
Escalate to Johan Ras
    ↓
Johan Analyzes
    ↓
Johan Decides:
    ├─ Emergency Override (temporary)
    ├─ Governance Modification (permanent)
    ├─ Architecture Change (CS2 approval)
    └─ Resolution Guidance
    ↓
Agent Executes Johan's Decision
    ↓
Resolution Complete
    ├─ Issue marked resolved
    ├─ Incident logged to governance memory
    ├─ Resolution documented in governance reports
    └─ Lessons learned captured (if applicable)
```

### When to Escalate

**Mandatory Escalation Triggers**:
- RED gate cannot be resolved
- Governance conflict detected
- Canonical governance ambiguous/unclear
- Agent blocked by missing permissions/resources
- Immutability violation detected
- Agent boundary violation detected
- Constitutional file modification needed
- Emergency production incident

**Escalation Format**:
1. **Problem**: Clear description of the block
2. **Context**: What was attempted, what failed
3. **Impact**: Why this blocks progression
4. **Options**: Proposed solutions with pros/cons
5. **Request**: Specific decision needed from Johan

**Response Time Expectation**: Agent must wait for Johan response. No work-arounds.

---

## X. Override Authority

### Emergency Override (Johan Only)

**When Johan May Override**:
- Production incident requiring immediate fix
- Critical security vulnerability
- Time-critical business requirement
- Governance conflict requiring constitutional resolution

**Override Characteristics**:
- **Temporary**: One-time use for specific instance
- **Bounded**: Specific scope (e.g., "this PR only", "this build only")
- **Documented**: Incident record mandatory
- **Auditable**: Logged to governance memory
- **Non-Precedent**: Does NOT weaken future governance enforcement

**Override Procedure**:
1. Johan issues override decision (explicit statement)
2. Override scope defined (what is overridden, for how long)
3. Override rationale documented (why override necessary)
4. Override incident record created
5. Work proceeds under override
6. Override expires automatically (does not persist)
7. Standard governance resumes

**Post-Override**:
- Technical debt created must be tracked
- Resolution plan required
- Follow-up to restore full governance compliance

---

## XI. Governance Synchronization Authority

### Canonical Governance Updates

**Authority to Update Canonical Governance**: Johan Ras + Governance Administrator (in governance repo)

**Process**:
1. Canonical governance updated in `maturion-foreman-governance` repository
2. Governance Liaison detects change
3. Governance Liaison creates FM sync PR
4. Johan approves FM sync PR
5. FM governance updated to match canon

**Reference**: `governance/workflows/GOVERNANCE_POLICY_SYNC_SPECIFICATION.md`

### FM Execution Constraint Updates

**Authority to Update FM Execution**: Governance Liaison (execution) + Johan (approval)

**Constraints**:
- Must have canonical governance basis
- Cannot weaken canonical requirements
- Cannot introduce FM-specific governance
- Must be direct translation only

---

## XII. Red Gate Ownership and Resolution Authority

### Gate Ownership

**Owner**: The agent/system that declares a gate RED owns that gate until resolved.

| Gate | Declarant (Owner) | Resolver | Resolution Method |
|------|-------------------|----------|-------------------|
| **Builder QA Gate** | Builder Agent | Builder Agent | Fix tests/implementation, re-run QA, declare READY |
| **Architecture Gate** | Governance Liaison | Architecture Author + Governance Liaison | Complete architecture, re-validate |
| **Build Auth Gate** | Governance Liaison | Multiple (depends on precondition) | Satisfy all preconditions, re-validate |
| **Agent Boundary Gate** | Automated | Violating Agent | Remove cross-agent QA, follow scope |
| **Governance Compliance Gate** | Governance Liaison | PR Author + Governance Liaison | Add artifacts, fix schema |

**Key Distinction**:
- **Owner** = Authority that evaluates and declares gate status
- **Resolver** = Agent/team that performs work to satisfy requirements

**Reference**: `governance/policies/RED_GATE_AUTHORITY_AND_OWNERSHIP.md`

---

## XIII. Prohibited Actions (All Agents)

### Universal Prohibitions

**NO agent/builder may**:

1. ❌ Modify BUILD_PHILOSOPHY.md without Johan approval
2. ❌ Weaken constitutional governance rules
3. ❌ Disable PR gates
4. ❌ Bypass PR gates
5. ❌ Create "temporary" gate bypasses
6. ❌ Declare another agent's gates RED/GREEN
7. ❌ Override Builder QA READY/NOT_READY declarations
8. ❌ Reinterpret canonical governance
9. ❌ Create FM-specific governance exceptions
10. ❌ Modify protected constitutional files
11. ❌ Hand over work with RED gates unresolved
12. ❌ Hide RED gates or governance violations
13. ❌ Execute QA outside their agent scope
14. ❌ Dismiss RED gates as "legacy debt"
15. ❌ Proceed past RED gates without resolution

**Violation Response**: HALT immediately, log incident, escalate to Johan.

---

## XIV. Authority Summary Table

### Quick Reference: Who Does What?

| Question | Answer |
|----------|--------|
| **Who has ultimate authority?** | Johan Ras |
| **Who can stop a build?** | Builder Agent, Governance Liaison, PR Gates, Johan |
| **Who can declare Builder QA Gate RED?** | Builder Agent ONLY |
| **Who can declare Architecture Gate RED?** | Governance Liaison ONLY |
| **Who can declare Build Authorization Gate RED?** | Governance Liaison ONLY |
| **Who can override governance?** | Johan Ras ONLY (temporary emergency override) |
| **Who can modify constitutional governance?** | Johan Ras ONLY |
| **Who can modify canonical governance?** | Johan + Governance Administrator (governance repo) |
| **Who can sync canonical governance to FM?** | Governance Liaison (execution) + Johan (approval) |
| **Who can resolve RED gates?** | Depends on gate type (see Section XII) |
| **Who can approve architecture changes?** | Johan Ras ONLY (CS2 approval) |
| **Who can modify agent contracts?** | Johan Ras ONLY (or delegated with approval) |
| **Who can weaken PR gates?** | NO ONE (except Johan emergency override) |
| **Who enforces QA passing?** | Builder Agent + PR Gates |
| **Who enforces zero test debt?** | Builder Agent + PR Gates |
| **Who enforces architecture conformance?** | Governance Liaison + Architecture Gate |
| **Who enforces agent boundaries?** | Agent Boundary Gate (automated) |
| **Who enforces build-to-green?** | Build-to-Green Gate (automated) |

---

## XV. Integration with Existing Governance

This matrix integrates and references:

- **BUILD_PHILOSOPHY.md** - Supreme constitutional authority
- **Governance Supremacy Rule** (`governance/policies/governance-supremacy-rule.md`) - Constitutional governance
- **Zero Test Debt Constitutional Rule** (`governance/policies/zero-test-debt-constitutional-rule.md`) - Test debt prohibition
- **Design Freeze Rule** (`governance/policies/design-freeze-rule.md`) - Architecture protection
- **Red Gate Authority and Ownership** (`governance/policies/RED_GATE_AUTHORITY_AND_OWNERSHIP.md`) - Gate ownership
- **Two-Gatekeeper Model** (`governance/alignment/TWO_GATEKEEPER_MODEL.md`) - Dual gatekeeper structure
- **PR Gate Failure Handling Protocol** (`governance/alignment/PR_GATE_FAILURE_HANDLING_PROTOCOL.md`) - Failure handling
- **Build Authorization Gate** (`governance/build/BUILD_AUTHORIZATION_GATE.md`) - Build preconditions
- **FM Governance Adoption Policy** (`governance/policies/FM_GOVERNANCE_ADOPTION_POLICY.md`) - Adoption execution
- **Governance Policy Sync Specification** (`governance/workflows/GOVERNANCE_POLICY_SYNC_SPECIFICATION.md`) - Policy sync

**Precedence**: This matrix is authoritative for authority questions. If conflicts arise, escalate to Johan.

---

## XVI. Version and Authority

**Version**: 1.0.0  
**Status**: Constitutional Authority - Master Reference  
**Last Updated**: 2025-12-29  
**Owner**: Johan Ras (MaturionISMS)  
**Precedence**: Authoritative for all governance authority questions

**Changelog**:
- 1.0.0 (2025-12-29): Initial Governance Authority Matrix (completes Batch 1 Governance Hardening: #123, #78, #86)

---

## XVII. Definitive Answer to Key Question

### "Who Can Stop a Build, and Why?"

**Answer (No Hesitation)**:

**Four authorities can stop a build:**

1. **Builder Agent** - Declares Builder QA Gate = NOT_READY when any test fails or QA requirement is not met. This stops the build because merge is blocked.

2. **Governance Liaison** - Declares Architecture Gate, Build Authorization Gate, or Governance Compliance Gate = FAIL when governance preconditions are not satisfied. This stops the build because merge is blocked.

3. **PR Gate Workflows** - Automatically evaluate canonical rules and declare gates RED when violations are detected (agent boundary violations, build-to-green violations, etc.). This stops the build mechanically.

4. **Johan Ras** - Has ultimate authority to stop any build for any reason via manual intervention or escalation response.

**Why can they stop builds?**

Because **RED gates block merge**, and **blocked merge stops build progression**. These four authorities can declare gates RED within their respective scopes, triggering the build stop.

**No other agent/system has build stop authority.**

---

*END OF GOVERNANCE AUTHORITY MATRIX*
