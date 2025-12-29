# Red Gate Authority and Ownership

**Version**: 1.0.0  
**Status**: Constitutional Authority  
**Last Updated**: 2025-12-29  
**Authority**: Johan Ras  
**Addresses**: Issue #86 - FM-BEHAV-1

---

## I. Constitutional Statement

**A "Red Gate" is any governance gate that evaluates to FAIL/BLOCKED/NOT_READY.**

This document establishes:
1. Who has authority to declare a gate RED
2. Who owns RED gates once declared
3. What must happen when gates are RED
4. Who has authority to resolve RED gates

**Core Principle**: Red gates STOP builds. This is not negotiable.

---

## II. Red Gate Authority Matrix

### Who Can Declare a Gate RED?

| Gate Type | Declarant Authority | Rationale |
|-----------|---------------------|-----------|
| **Builder QA Gate** | Builder Agent ONLY | Builder agents execute QA and declare READY/NOT_READY. No other agent may override. |
| **Architecture Gate** | Governance Liaison ONLY | Validates architecture completeness per canonical compilation contract. |
| **Build Authorization Gate** | Governance Liaison ONLY | Validates all preconditions (architecture, QA, FL/CI learning) before build may proceed. |
| **Agent Boundary Gate** | PR Gate Workflow (Automated) | Detects cross-agent QA violations mechanically. No human/agent interpretation. |
| **Governance Compliance Gate** | Governance Liaison ONLY | Validates governance artifact presence, schema, and immutability. |

**Unbreakable Rule**: Only the authority listed above may declare their respective gate RED.

**Prohibition**: No agent may declare another agent's gate RED.

---

## III. Red Gate Ownership

### Definition of Ownership

**The agent/system that declares a gate RED owns that gate until it is resolved to GREEN.**

### Ownership Responsibilities

When an agent/system owns a RED gate, they MUST:

1. **Provide Clear Failure Classification**
   - Use canonical failure categories (ARTIFACT_MISSING, SCHEMA_VIOLATION, IMMUTABILITY_VIOLATION, etc.)
   - Never use vague classifications like "general failure" or "unknown"

2. **Provide Actionable Resolution Steps**
   - Explicit list of what must be done to resolve
   - No ambiguous statements like "fix the issues"
   - No dismissals like "this is legacy debt"

3. **Maintain Gate State Visibility**
   - RED gates must be visible in PR gate status
   - RED gates must be logged to governance memory
   - RED gates must be traceable to specific violations

4. **Block Build/Merge Until Resolved**
   - RED gates MUST block merge
   - RED gates MUST block build progression
   - No bypasses, no temporary overrides (except Johan)

### Ownership Transfer

**RED gate ownership CANNOT be transferred.**

The declaring authority remains owner until:
- Gate is resolved to GREEN, OR
- Johan Ras issues explicit emergency override

---

## IV. Build Stop Authority

### Who Can Stop a Build?

**Answer (Definitive)**: Any agent/system with authority to declare a gate RED can stop a build.

| Authority | Mechanism | Rationale |
|-----------|-----------|-----------|
| **Builder Agent** | Declares Builder QA Gate = NOT_READY | If Builder QA fails, build cannot proceed. Builder has authority to stop via QA declaration. |
| **Governance Liaison** | Declares Architecture/Build Auth Gate = FAIL | If governance preconditions not met, build cannot proceed. |
| **PR Gate Workflows** | Automated gate evaluation = RED | Mechanical enforcement of canonical rules. Gates stop builds automatically. |
| **Johan Ras** | Manual intervention / escalation response | Ultimate authority. Can stop any build for any reason. |

### Build Stop Procedure

When a gate is declared RED:

```
Gate Declared RED
    ↓
PR Merge = BLOCKED (automatic)
    ↓
Build Progression = HALTED (automatic)
    ↓
Gate Owner Provides Resolution Steps
    ↓
Responsible Agent Executes Resolution
    ↓
Gate Re-Evaluated
    ↓
GREEN? → Continue
RED? → Remains Blocked
```

**No Build May Proceed Past a RED Gate.**

---

## V. Red Gate Resolution Authority

### Who Can Resolve a RED Gate?

**General Rule**: The agent/team responsible for the failing precondition resolves the gate.

| Gate | Declarant | Resolver | Resolution Method |
|------|-----------|----------|-------------------|
| **Builder QA Gate** | Builder Agent | Builder Agent | Fix failing tests, fix implementation, re-run QA, declare READY |
| **Architecture Gate** | Governance Liaison | Architecture Author + Governance Liaison | Complete missing architecture elements, re-validate |
| **Build Auth Gate** | Governance Liaison | Multiple (depends on failing precondition) | Satisfy all preconditions, re-validate |
| **Agent Boundary Gate** | Automated | Violating Agent | Remove cross-agent QA, follow agent scope boundaries |
| **Governance Compliance Gate** | Governance Liaison | PR Author + Governance Liaison | Add missing artifacts, fix schema violations |

**Key Distinction**:
- **Declarant** = Authority that evaluates and declares gate status
- **Resolver** = Agent/team that performs work to satisfy gate requirements

### Resolution Validation

After resolution work is complete:
1. Resolver commits changes
2. Declarant re-evaluates gate
3. Declarant declares GREEN (if all requirements met) or remains RED (if still failing)
4. PR gates update automatically

**No Self-Service GREEN**: An agent cannot declare their own gate GREEN. Only the declarant authority may update gate status.

---

## VI. Escalation When RED Gates Cannot Be Resolved

### Escalation Triggers

Escalate to Johan Ras when:
- RED gate cannot be resolved within reasonable timeframe
- RED gate resolution requires architectural decision
- RED gate resolution conflicts with other governance requirements
- RED gate resolution blocked by missing permissions/resources
- Multiple RED gates with conflicting resolution paths

### Escalation Protocol

1. **Document the Block**
   - Which gate is RED
   - What resolution was attempted
   - Why resolution cannot proceed
   - What decision is needed

2. **Propose Solution Options**
   - Option A: [Description + Impact]
   - Option B: [Description + Impact]
   - Recommended: [Which option + Why]

3. **Request Specific Decision**
   - "We request Johan decide: [Specific question]"
   - Not: "We're blocked, please help"

4. **Wait for Response**
   - Do NOT proceed until Johan responds
   - Do NOT work around the block
   - Do NOT weaken the gate to pass

### Emergency Override (Johan Only)

Johan may issue emergency override when:
- Production incident requires immediate fix
- Critical security vulnerability must be patched
- Time-critical business requirement

**Override Characteristics**:
- Temporary (one-time use)
- Documented (incident record required)
- Bounded (specific scope, specific PR)
- Auditable (logged to governance memory)
- Does NOT weaken future gate enforcement

---

## VII. Prohibited Actions

### Agents/Builders MUST NOT:

1. ❌ Declare another agent's gate RED/GREEN
2. ❌ Dismiss RED gates as "legacy debt" without resolution
3. ❌ Bypass RED gates via workflow modification
4. ❌ Weaken gate thresholds to force GREEN
5. ❌ Disable RED gates to allow merge
6. ❌ Create "temporary" RED gate bypasses
7. ❌ Hand over work with RED gates unresolved
8. ❌ Transfer RED gate ownership
9. ❌ Declare GREEN without satisfying all requirements
10. ❌ Hide RED gates in documentation/reports

### Violation Response

If any prohibited action is detected:
1. HALT immediately
2. Log governance violation
3. Escalate to Johan
4. Require resolution before any further work

---

## VIII. Red Gate Behavioral Requirements (FM-BEHAV-1)

### Foreman Office App Behavior

When FM encounters RED gates, FM MUST:

1. **Never Dismiss as Legacy Debt**
   - ❌ "This gate is legacy debt, we can ignore it"
   - ✅ "This gate is RED. Resolution required: [specific steps]"

2. **Always Provide Actionable Next Steps**
   - ❌ "Fix the failing tests"
   - ✅ "Builder Agent must: 1) Fix test X in file Y, 2) Re-run QA suite, 3) Verify 100% pass"

3. **Always Identify Gate Owner**
   - ❌ "Someone should fix this"
   - ✅ "Builder Agent (owner) must resolve this gate"

4. **Always Classify Failures Canonically**
   - ❌ "General failure detected"
   - ✅ "ARTIFACT_MISSING: Builder QA Report not found in PR"

5. **Always Block Progression**
   - ❌ "This gate is RED, but we can continue"
   - ✅ "This gate is RED. Build is BLOCKED. No progression until GREEN."

### Enforcement

FM Office App RED gate behavior will be validated via:
- Integration tests (foreman reasoning output validation)
- Agent contract tests (FM behavior validation)
- Dashboard tests (RED gate visibility validation)

**This is mandatory FM behavior, not optional.**

---

## IX. Summary: Who Can Stop a Build?

**Definitive Answer**:

| Authority | Stop Mechanism | When Exercised |
|-----------|----------------|----------------|
| **Builder Agent** | Declares Builder QA Gate = NOT_READY | Any test failure, any QA requirement not met |
| **Governance Liaison** | Declares Architecture/Build Auth Gate = FAIL | Architecture incomplete, governance preconditions not met |
| **PR Gate Workflows** | Automated gate evaluation = RED | Any canonical rule violation detected |
| **Johan Ras** | Manual stop / escalation intervention | Any reason, any time (ultimate authority) |

**All of these authorities can stop a build by declaring their respective gates RED.**

**No agent may declare another agent's gates. Scope boundaries are absolute.**

---

## X. Integration with Existing Governance

This policy integrates with and extends:

- **Governance Supremacy Rule** (`governance/policies/governance-supremacy-rule.md`) - Establishes that governance rules are absolute
- **Two-Gatekeeper Model** (`governance/alignment/TWO_GATEKEEPER_MODEL.md`) - Defines dual gatekeeper authority structure
- **PR Gate Failure Handling Protocol** (`governance/alignment/PR_GATE_FAILURE_HANDLING_PROTOCOL.md`) - Defines canonical failure classifications
- **Build Authorization Gate** (`governance/build/BUILD_AUTHORIZATION_GATE.md`) - Defines preconditions for build authorization
- **FM Governance Adoption Policy** (`governance/policies/FM_GOVERNANCE_ADOPTION_POLICY.md`) - Defines how governance becomes enforcement

**Precedence**: This document is constitutional authority, equal precedence with Governance Supremacy Rule.

---

## XI. Version and Authority

**Version**: 1.0.0  
**Status**: Active and Enforced  
**Authority**: Constitutional Authority  
**Precedence**: Equal to Governance Supremacy Rule  
**Last Updated**: 2025-12-29  
**Owner**: Johan Ras (MaturionISMS)  
**Enforcer**: All Agents + PR Gate Workflows

**Changelog**:
- 1.0.0 (2025-12-29): Initial Red Gate Authority and Ownership Policy (addresses #86)

---

*END OF RED GATE AUTHORITY AND OWNERSHIP POLICY*
