# Builder Ripple Intelligence Boundary Specification

**Version**: 1.0.0  
**Date**: 2026-01-02  
**Status**: Canonical — Constitutional Authority  
**Authority**: Governance Clarification Ratchet (One-Time Build Law Compliance)  
**Purpose**: Explicit boundary definition for builder ripple awareness vs. authority

---

## I. Constitutional Statement

**Builders are Ripple-AWARE but are NOT Ripple-INITIATORS, PROPAGATORS, or COORDINATORS.**

This boundary is absolute and non-negotiable under One-Time Build Law.

All authority and responsibility limits must be explicit and auditable.
Implicit boundaries are unacceptable.

---

## II. Builder Ripple Awareness (PERMITTED)

Builders MAY:

- ✅ **Receive ripple context** from FM during task assignment
- ✅ **Acknowledge ripple awareness** in execution reports
- ✅ **Escalate concerns to FM** when ripple context affects assigned scope
- ✅ **Reference ripple context** in evidence and completion documentation
- ✅ **Validate alignment** with ripple-affected specifications during build

---

## III. Builder Ripple Authority Boundaries (PROHIBITED)

Builders MUST NOT:

- ❌ **Initiate ripple signals** — Only Governance may originate ripple
- ❌ **Propagate ripple across repositories** — Only FM coordinates downstream impact
- ❌ **Coordinate ripple responses** — Only FM orchestrates execution changes
- ❌ **Interpret ripple impact beyond assigned scope** — Only FM determines system-wide implications
- ❌ **Modify governance artifacts based on ripple** — Only Governance Liaison propagates canonical changes
- ❌ **Update other agents' contracts due to ripple** — Only FM updates agent instructions
- ❌ **Assume ripple authority from awareness** — Awareness ≠ Authority

---

## IV. Authority Hierarchy (Unchanged)

This specification confirms and does NOT alter the existing authority hierarchy:

### Ripple Origination Authority
**Sole Authority**: Governance (Canonical Governance Repository)
- Creates governance rules and standards
- Issues governance evolution signals
- Originates all ripple triggers

### Ripple Coordination Authority
**Sole Authority**: FM (Foreman App Agent)
- Interprets ripple impact on execution domain
- Coordinates downstream propagation to builders
- Updates agent context and instructions
- Escalates contract changes beyond FM authority

### Execution Authority
**Scope-Limited Authority**: Builders (Builder Agents)
- Execute assigned tasks within frozen architecture
- Report completion evidence
- Escalate blockers to FM
- **Consume** ripple context, do NOT **act** on ripple beyond assigned scope

---

## V. Ripple Intelligence vs. Ripple Authority

**Ripple Intelligence** (Awareness):
- Information about governance changes or structural impacts
- Provided to builders as **context** for execution
- Ensures builders understand current governance state
- Supports One-Time Build Correctness through complete context

**Ripple Authority** (Action):
- Power to initiate, propagate, or coordinate ripple responses
- Reserved to Governance (origin) and FM (coordination)
- NOT granted to builders under any circumstances
- Separation prevents authority drift and governance fragmentation

**Key Distinction**: Builders are **informed** by ripple, but do NOT **act** on ripple beyond their assigned scope.

---

## VI. Escalation Requirements

When builders encounter ripple-related concerns:

**MUST Escalate to FM** when:
- Ripple context conflicts with frozen architecture
- Ripple context suggests specification gaps
- Ripple impact extends beyond assigned scope
- Ripple creates ambiguity in requirements
- Uncertainty exists about ripple implications

**Escalation Format**:
```
RIPPLE_CONCERN_ESCALATION:
- Builder: [builder-id]
- Task: [task-id]
- Concern: [specific concern]
- Ripple Context: [relevant ripple information]
- Requested Action: [what builder needs from FM]
```

**Escalation Path**: Builder → FM → Governance (if needed)

Builders MUST NOT attempt to resolve ripple concerns independently.

---

## VII. Enforcement

This boundary is enforced through:

1. **Builder Contract Requirements**
   - All builder contracts MUST reference GOVERNANCE_RIPPLE_COMPATIBILITY.md (ripple model)
   - All builder contracts MUST acknowledge this specification (ripple boundaries)
   - Both documents serve complementary roles:
     - GOVERNANCE_RIPPLE_COMPATIBILITY.md: Defines overall ripple intelligence model
     - BUILDER_RIPPLE_BOUNDARY_SPEC.md: Defines specific builder authority limits
   - Ripple boundary acknowledgment mandatory in contract body (Section 6)

2. **FM Supervision**
   - FM monitors builder actions for ripple authority violations
   - FM verifies builders stay within execution scope
   - FM blocks unauthorized ripple propagation attempts

3. **Governance Audits**
   - Periodic review of builder behavior patterns
   - Detection of ripple authority drift
   - Corrective action for boundary violations

---

## VIII. Rationale

**Why This Boundary Exists**:

1. **Separation of Concerns**
   - Governance owns canon and ripple origin
   - FM owns execution coordination
   - Builders own scoped implementation
   - Clear boundaries prevent authority creep

2. **Governance Supremacy**
   - Governance must remain sole source of truth
   - No alternate governance authorities
   - No builder-initiated governance changes

3. **FM Coordination Integrity**
   - FM must coordinate all downstream impact
   - No peer-to-peer builder coordination
   - No fragmented ripple responses

4. **One-Time Build Correctness**
   - Complete context prevents implementation errors
   - Awareness without authority prevents scope drift
   - Escalation ensures proper coordination

5. **Auditability**
   - Clear authority lines enable audit trails
   - Explicit boundaries enable violation detection
   - No implicit authority assumptions

---

## IX. Examples

### Example 1: Permitted Ripple Awareness

**Scenario**: Governance updates QA schema requirements (downward ripple)

**FM Action**:
- Receives ripple from Governance
- Updates builder instructions with new QA requirements
- Provides ripple context to affected builders

**Builder Action** (PERMITTED):
- ✅ Acknowledges receipt of updated QA requirements
- ✅ Implements tests according to new schema
- ✅ Reports compliance with updated requirements
- ✅ Documents ripple context in completion evidence

**Builder Action** (PROHIBITED):
- ❌ Does NOT notify other builders of schema change
- ❌ Does NOT update schema documentation independently
- ❌ Does NOT interpret broader system implications
- ❌ Does NOT modify governance artifacts

---

### Example 2: Proper Escalation

**Scenario**: Builder receives ripple context indicating architecture change, but frozen architecture hasn't been updated

**Builder Action** (CORRECT):
```
RIPPLE_CONCERN_ESCALATION:
- Builder: api-builder
- Task: BLD-042
- Concern: Ripple indicates auth model changed, but frozen architecture still references old model
- Ripple Context: GOVERNANCE_RIPPLE: AUTH-002 (OAuth2 → OIDC migration)
- Requested Action: Architecture freeze update or ripple clarification
```

**FM Response**:
- Verifies ripple applicability to current task
- Updates frozen architecture if ripple is current
- OR clarifies ripple is for future wave
- Provides updated instructions to builder

**Builder Action** (INCORRECT):
- ❌ Implementing OIDC based on ripple alone
- ❌ Updating architecture document directly
- ❌ Proceeding with ambiguity
- ❌ Interpreting ripple intent independently

---

### Example 3: Boundary Violation (Prevented)

**Scenario**: Builder detects pattern that might benefit other modules

**Builder Action** (VIOLATION — MUST NOT OCCUR):
- ❌ Creating cross-module ripple signal
- ❌ Updating other builders' task context
- ❌ Propagating pattern to other repositories

**Builder Action** (CORRECT):
- ✅ Complete assigned task
- ✅ Capture enhancement opportunity in completion report
- ✅ Route to FM via Mandatory Enhancement Capture
- ✅ Let FM determine if pattern warrants ripple

**FM Action**:
- Evaluates enhancement proposal
- Determines if pattern is generalizable
- IF generalizable: Creates governance improvement proposal (upward ripple)
- IF applicable now: Updates relevant builder contexts
- Maintains coordination authority

---

## X. Success Criteria

This boundary specification is successful when:

1. ✅ No builder attempts to initiate ripple signals
2. ✅ No builder propagates ripple without FM coordination
3. ✅ All ripple-related concerns properly escalated to FM
4. ✅ Builders demonstrate ripple awareness in execution
5. ✅ No builder assumes ripple authority from awareness
6. ✅ FM remains sole execution coordinator for ripple
7. ✅ Governance remains sole ripple origin authority
8. ✅ Authority hierarchy remains intact and auditable

---

## XI. References

**Constitutional Authorities**:
- `BUILD_PHILOSOPHY.md` — Builder authority constraints
- `governance/GOVERNANCE_AUTHORITY_MATRIX.md` — Authority hierarchy
- `governance/alignment/GOVERNANCE_RIPPLE_COMPATIBILITY.md` — Ripple model
- `governance/specs/FM_RIPPLE_INTELLIGENCE_SPEC.md` — FM ripple responsibilities

**Builder Integration**:
- `.github/agents/BUILDER_CONTRACT_SCHEMA.md` — Builder contract requirements
- `foreman/builder/*.md` — Individual builder specifications

---

## XII. Version History

**Version 1.0.0** (2026-01-02):
- Initial canonical specification
- Explicit awareness vs. authority boundary
- Constitutional authority established
- No behavior change (clarification only)

---

**Status**: ✅ CANONICAL — ACTIVE  
**Authority**: Constitutional (Governance Clarification Ratchet)  
**Scope**: All Maturion builder agents  
**Enforcement**: MANDATORY

*END OF BUILDER RIPPLE BOUNDARY SPECIFICATION*
