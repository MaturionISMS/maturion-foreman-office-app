# Agent Gate Autonomy Specification

**Status**: PARKED — NOT YET RATIFIED  
**Authority**: Foreman Governance (Pending CS2 Ratification)  
**Date**: 2025-12-31  
**Version**: 1.0.0-DRAFT  
**Source**: Issue — PARKED GOVERNANCE CLARIFICATION — Agent Autonomy After Gate Fixes

---

## I. Purpose

This specification defines **agent autonomy boundaries** after PR gate semantics are explicitly defined and system defects are resolved.

**Core Issue Addressed**:  
During Phase 2.2 (Governance Layer-Down), an agent paused handover awaiting human clarification after PR gate behavior was fixed and merged. This revealed an implicit ambiguity regarding agent responsibility for deterministic decision-making once gate semantics are defined.

**Governance Gap**:  
Current governance does not explicitly state whether agents must:
- Interpret gate outcomes autonomously after fixes are deployed
- Execute handover decisions based on deterministic gate outcomes
- Escalate for human interpretation of already-defined gate semantics

This ambiguity contradicts the sandbox model and creates unnecessary human dependency.

---

## II. Constitutional Authority

This specification derives authority from:

1. **BUILD_PHILOSOPHY.md — Section IX: One-Prompt One-Job Doctrine (OPOJD)**
   - Builders must execute autonomously
   - Default assumption: PERMISSION GRANTED
   - "Do NOT ask for permission to continue normal work"

2. **Sandbox Execution Model**
   - Agents operate within defined boundaries
   - Humans define rules, not runtime decisions
   - Agents interpret and execute deterministically

3. **Separation of Duties**
   - Humans: Define governance, fix systems, authorize exceptions
   - Agents: Execute within governance, interpret deterministically, escalate ambiguity

---

## III. Core Principle

**Agent Autonomy After Gate Definition**

Once PR gate semantics are:
1. **Explicitly defined** (in specification or workflow)
2. **Fixed** (where defective behavior was corrected)
3. **Available** (deployed and accessible to the agent)

**Then agents are RESPONSIBLE for:**
- Running gates autonomously
- Interpreting gate outcomes deterministically
- Proceeding with handover when gate conditions are met
- Making proceed/hold decisions based on explicit gate outcomes

**Humans are RESPONSIBLE for:**
- Defining gate semantics and rules
- Fixing gate system defects when escalated
- Authorizing governance exceptions
- Reviewing agent decisions after execution (not before)

**Humans are NOT responsible for:**
- Interpreting gate outcomes after semantics are defined
- Making runtime proceed/hold decisions when gates are deterministic
- Acting as real-time decision-makers for operational gates

---

## IV. Decision Authority Model

### A. Agent Decision Authority (Autonomous)

Agents MUST make autonomous decisions when:

1. **Gate Semantics Are Defined**
   - Gate behavior is specified in `governance/specs/` documentation
   - Gate workflow logic is explicit and unambiguous
   - Gate outcomes are enumerated (GREEN/SKIP/FAIL)

2. **Gate Outcomes Are Deterministic**
   - Gate returns explicit outcome (not ambiguous status)
   - Outcome classification is documented (blocking vs non-blocking)
   - Decision logic is Boolean (proceed if X, hold if Y)

3. **No Governance Ambiguity Exists**
   - Gate specification covers the current scenario
   - No conflicting governance rules apply
   - No undefined edge cases are encountered

**Agent Action**: Execute handover, proceed with next phase, or escalate violation — **without human confirmation**.

---

### B. Human Decision Authority (Governance Definition)

Humans MUST make decisions when:

1. **Gate Semantics Are Undefined**
   - No specification exists for gate behavior
   - Gate logic is ambiguous or contradictory
   - Outcome classifications are not documented

2. **System Defects Require Fixes**
   - Gate is returning incorrect outcomes (system bug)
   - Gate specification contradicts implementation
   - Gate behavior is non-deterministic (flaky)

3. **Governance Exceptions Are Needed**
   - Situation requires override of normal gate behavior
   - Constitutional boundary needs temporary adjustment
   - Emergency governance bypass is required

**Human Action**: Define new governance, fix system defects, authorize exceptions — **then delegate execution back to agents**.

---

## V. Handover Decision Protocol

### When Gate Outcomes Are GREEN/SKIP (Non-Blocking)

**Agent Responsibility**:
1. Verify all required gates have run
2. Confirm all outcomes are GREEN or SKIP
3. Check for any explicit FAIL outcomes
4. If all gates pass: **Proceed with handover autonomously**
5. If any gate fails: **Halt and escalate**

**No human confirmation required for proceed decision.**

---

### When Gate Outcomes Are FAIL (Blocking)

**Agent Responsibility**:
1. Identify which gate(s) failed
2. Extract failure reason from gate output
3. Determine if failure is:
   - **True violation** → Escalate with violation details
   - **System defect** → Escalate with defect evidence
   - **Governance ambiguity** → Escalate with ambiguity description
4. **Halt and escalate** — do not proceed

**No autonomous override of FAIL outcomes.**

---

### When Gate Outcomes Are Ambiguous (e.g., `action_required`)

**Agent Responsibility**:
1. Recognize ambiguous outcome status
2. Classify as **system defect** (gate semantics not deterministic)
3. **Escalate immediately** with:
   - Gate that returned ambiguous status
   - Expected outcomes (GREEN/SKIP/FAIL)
   - Request: Define deterministic behavior

**Ambiguous gate outcomes are always governance/system failures, not agent decision points.**

---

## VI. Forbidden Behaviors

### Agents MUST NOT:

1. **Wait for human gate interpretation after semantics are defined**
   - If gate spec exists and gate ran successfully, interpret autonomously
   - If gate returned GREEN/SKIP, proceed without confirmation
   - If gate returned FAIL, escalate without asking "should I proceed?"

2. **Revert to human-gated CI mental model**
   - Do not treat gates as "advisory" requiring human review
   - Do not pause for human approval when gates are GREEN
   - Do not ask "may I proceed?" when governance authorizes autonomy

3. **Inject artificial human dependency**
   - Do not create checkpoints where governance requires none
   - Do not escalate decisions that are deterministically resolvable
   - Do not defer to humans when agent authority is sufficient

---

## VII. Examples

### Example 1: Documentation-Only PR Gate Outcomes

**Scenario**:
- PR is documentation-only (governance layer-down)
- Gate spec: `DOCUMENTATION_ONLY_PR_GATE_BEHAVIOR_SPEC.md` defines behavior
- Gates return: Agent QA Boundary (SKIP), Build-to-Green (SKIP), Builder QA (SKIP), Governance Compliance (GREEN)

**Correct Agent Behavior**:
1. Agent reads gate outcomes: 3x SKIP (non-blocking) + 1x GREEN (passed)
2. Agent checks gate spec: SKIP is explicitly defined as non-blocking
3. Agent verifies no FAIL outcomes exist
4. **Agent proceeds with handover autonomously** (no human confirmation)

**Incorrect Agent Behavior**:
- Agent sees SKIP outcomes and escalates: "Gate returned SKIP, should I proceed?"
- Agent waits for human interpretation of SKIP status
- Agent treats SKIP as ambiguous despite specification defining it

**Why Incorrect**: Gate semantics are defined. SKIP is explicitly non-blocking. Agent has authority to interpret and proceed.

---

### Example 2: Code PR Gate Failure

**Scenario**:
- PR includes code changes
- Gate spec: Code PRs require passing tests
- Gates return: Build-to-Green (FAIL - 5 tests failing)

**Correct Agent Behavior**:
1. Agent reads gate outcome: FAIL (blocking)
2. Agent recognizes FAIL blocks handover
3. **Agent escalates**: "Build-to-Green gate failed: 5 tests failing. Handover blocked. Evidence: [link to test results]"
4. Agent does NOT ask "should I proceed anyway?"

**Incorrect Agent Behavior**:
- Agent asks: "Gate failed but tests may be unrelated, should I proceed?"
- Agent proceeds despite FAIL outcome (governance override without authority)

**Why Incorrect**: FAIL is blocking. Agent lacks authority to override. Must escalate, not proceed.

---

### Example 3: Gate Semantic Fix Deployment

**Scenario**:
- Agent previously encountered ambiguous `action_required` status
- Human fixed gate workflows to return explicit GREEN/SKIP/FAIL
- New PR triggers same gates, now returns SKIP

**Correct Agent Behavior**:
1. Agent recognizes gate semantics were previously ambiguous (history)
2. Agent checks current gate spec: SKIP is now defined as non-blocking
3. Agent verifies gate implementation matches spec (returns SKIP correctly)
4. **Agent proceeds autonomously** based on new deterministic behavior

**Incorrect Agent Behavior**:
- Agent remembers previous ambiguity and escalates: "Gate used to be ambiguous, should I trust SKIP now?"
- Agent waits for human confirmation that fix is working

**Why Incorrect**: Gate semantics are now defined. Fix is deployed. Agent must trust current system state, not historical ambiguity.

---

## VIII. Escalation Triggers (When Agent MUST Escalate)

Agent MUST escalate (not decide autonomously) when:

1. **Gate Returns Undefined Outcome**
   - Outcome status is not in {GREEN, SKIP, FAIL}
   - Outcome is ambiguous (e.g., `action_required`, `warning`, `needs_review`)

2. **Gate Spec Does Not Exist**
   - No specification document defines gate behavior for this scenario
   - Gate logic is not documented

3. **Gate Spec Conflicts With Implementation**
   - Spec says gate should return GREEN, but gate returns FAIL
   - Spec defines behavior X, but implementation does behavior Y

4. **Multiple Gates Conflict**
   - One gate says proceed (GREEN), another says halt (FAIL) for same validation
   - No precedence rule exists in governance

5. **Governance Is Ambiguous**
   - Multiple governance documents provide conflicting guidance
   - No clear authority chain for decision

**Escalation Format**:
```
ESCALATION: Gate Autonomy Blocked

Reason: [Gate returns undefined outcome | Gate spec missing | Spec conflicts with impl | Gates conflict | Governance ambiguous]

Context:
- PR: [link]
- Gates run: [list with outcomes]
- Expected behavior: [per spec, if exists]
- Actual behavior: [what happened]
- Decision required: [what agent cannot determine]

Evidence: [links to gate outputs, specs, governance]

Agent Status: HALTED — Awaiting governance clarification or system fix
```

---

## IX. Ratification Requirements

### Status: PARKED

This specification is **PARKED** and **NOT YET ENFORCED**.

**Before ratification, this specification must**:
1. Be reviewed and approved by Johan (CS2)
2. Be incorporated into canonical governance (maturion-foreman repo or this repo's constitution)
3. Be referenced in agent contracts (`.github/agents/`)
4. Be layered down into relevant agent instructions
5. Receive explicit "RATIFIED" status change in this document

**Trigger Conditions for Ratification**:
- Next governance canon update cycle
- Next agent contract revision
- Next execution autonomy standards update
- Explicit CS2 ratification trigger

Until ratified, this document serves as:
- Proposed governance clarification
- Design intent documentation
- Reference for future governance work

**NOT as**:
- Enforceable governance
- Binding agent contract terms
- Operational policy

---

## X. Governance Alignment

### Non-Conflict Declaration

This specification **does not conflict with** existing governance:

✅ **BUILD_PHILOSOPHY.md Section IX (OPOJD)**
- Aligns with "Assume-Continue Principle"
- Aligns with "Default assumption: PERMISSION GRANTED"
- Extends continuous execution mandate to gate interpretation

✅ **DOCUMENTATION_ONLY_PR_GATE_BEHAVIOR_SPEC.md**
- Complements gate behavior definitions
- Provides agent-side interpretation rules
- Clarifies handover decision authority

✅ **Governance Supremacy Rule**
- Agents operate within defined governance (not outside it)
- Agents escalate when governance is ambiguous (not assume)
- Humans define rules, agents execute deterministically

### Extensions to Governance

This specification **extends** existing governance by:

1. **Explicit Agent Autonomy After Gate Fixes**
   - Current governance: Silent on post-fix agent responsibility
   - This spec: Agents must interpret deterministically after fixes deployed

2. **Handover Decision Authority**
   - Current governance: Unclear who decides proceed/hold after gate runs
   - This spec: Agents decide when gates are deterministic, escalate when ambiguous

3. **Human vs Agent Decision Boundaries**
   - Current governance: Implied separation of duties
   - This spec: Explicit boundaries for runtime decision authority

---

## XI. Implementation Notes (Post-Ratification)

Once ratified, implementation requires:

### A. Agent Contract Updates

Update `.github/agents/ForemanApp-agent.md`:
- Add reference to this specification
- Add explicit gate autonomy rules
- Add handover decision protocol
- Add escalation triggers for gate ambiguity

### B. Builder Agent Updates

Update builder agent contracts:
- Reference this spec for post-gate-run behavior
- Clarify when to proceed vs escalate
- Align with OPOJD continuous execution

### C. Governance Layerdown

Ensure this spec is:
- Indexed in governance structure
- Linked from BUILD_PHILOSOPHY.md
- Referenced in execution playbooks
- Included in agent training materials (if any)

### D. Validation

After implementation:
- Test agent behavior with deterministic gates
- Test agent escalation with ambiguous gates
- Verify no artificial human dependencies introduced
- Confirm handover proceeds autonomously when authorized

---

## XII. Success Criteria

This specification is successful when:

1. ✅ **Agents interpret deterministic gates autonomously**
   - No escalation for proceed/hold decisions when gates are GREEN/SKIP
   - No waiting for human confirmation when gate semantics are defined

2. ✅ **Agents escalate ambiguous gates immediately**
   - Recognize undefined outcomes as system defects
   - Do not attempt to interpret ambiguous statuses

3. ✅ **Human dependency is eliminated for runtime gate decisions**
   - Humans define governance, not interpret it at runtime
   - Agents execute within governance without constant checkpoints

4. ✅ **Separation of duties is maintained**
   - Humans fix system defects when escalated
   - Agents execute deterministically after fixes deployed
   - No role confusion or authority bleed

5. ✅ **Sandbox model is reinforced**
   - Agents operate within defined boundaries
   - Boundaries are governance-defined, not human-gated
   - Autonomy is expected, not exceptional

---

## XIII. Relationship to Other Governance

### Related Governance Documents

- **BUILD_PHILOSOPHY.md (Section IX)**: Foundation for agent autonomy
- **DOCUMENTATION_ONLY_PR_GATE_BEHAVIOR_SPEC.md**: Defines specific gate behaviors
- **GOVERNANCE_GATE_SPEC.md**: Defines evidence validation gate
- **Agent Contract Alignment Requirements**: Ensures agent contracts reflect this spec

### Integration Points

1. **Gate Specifications**
   - All gate specs should define explicit outcomes (GREEN/SKIP/FAIL)
   - All gate specs should state blocking vs non-blocking behavior
   - All gate specs should be referenced in agent autonomy decisions

2. **Agent Contracts**
   - Agent contracts must reference this spec
   - Agent contracts must align with autonomy boundaries
   - Agent contracts must define escalation triggers

3. **Handover Protocols**
   - Handover protocols must assume agent autonomy for gate interpretation
   - Handover protocols must require explicit governance for human gates
   - Handover protocols must escalate ambiguity, not defer to humans by default

---

## XIV. Rationale

This specification preserves:

1. **Agent autonomy inside the sandbox**
   - Agents are not human-supervised at runtime for deterministic decisions
   - Agents have authority to interpret explicit governance

2. **Separation of duties**
   - Humans define rules and fix systems
   - Agents execute rules and escalate defects
   - No role overlap or dependency injection

3. **Non-coder execution model**
   - Execution is autonomous within governance
   - Human intervention is for governance definition, not operational gating

4. **Elimination of human bottlenecks**
   - Gate outcomes are machine-readable and deterministic
   - No human interpretation layer required for explicit outcomes
   - Humans are freed from runtime decision-making for well-defined gates

**Failure to ratify this specification risks**:
- Reintroducing implicit human gating
- Creating artificial execution dependencies
- Contradicting OPOJD and sandbox model
- Slowing execution with unnecessary escalations

---

## XV. Open Questions (For Ratification Discussion)

1. **Scope of "Explicit Definition"**
   - Q: How detailed must gate specifications be to qualify as "explicit"?
   - Proposed: Gate spec must enumerate outcomes and blocking behavior

2. **Historical Ambiguity Memory**
   - Q: Should agents remember previous gate ambiguity and escalate cautiously?
   - Proposed: No — agents trust current system state, not historical issues

3. **Gate Spec Versioning**
   - Q: Should gate specs include version numbers for agent reference?
   - Proposed: Yes — helps agents detect spec updates

4. **Multi-Gate Conflict Resolution**
   - Q: When two gates conflict, who decides precedence?
   - Proposed: Governance must define precedence rules, agents escalate if undefined

---

## XVI. Version History

| Version | Date | Status | Changes |
|---------|------|--------|---------|
| 1.0.0-DRAFT | 2025-12-31 | PARKED | Initial specification (not ratified) |

---

## XVII. References

- **Source Issue**: PARKED GOVERNANCE CLARIFICATION — Agent Autonomy After Gate Fixes
- **BUILD_PHILOSOPHY.md**: Section IX (One-Prompt One-Job Doctrine)
- **DOCUMENTATION_ONLY_PR_GATE_BEHAVIOR_SPEC.md**: Gate behavior definitions
- **GOVERNANCE_GATE_SPEC.md**: Evidence validation gate
- **Gate Release Behavior Resolution Evidence**: GATE_RELEASE_BEHAVIOR_RESOLUTION_EVIDENCE.md

---

**Document Status**: PARKED — NOT YET RATIFIED  
**Authority Status**: Pending CS2 Approval  
**Enforcement Status**: NOT ACTIVE

**Next Steps**:
1. Review by Johan (CS2)
2. Ratification decision
3. If ratified: Update agent contracts, layer down into execution
4. If not ratified: Mark as rejected, document rationale

---

*This specification will remain PARKED until explicitly ratified or rejected.*

*END OF AGENT GATE AUTONOMY SPECIFICATION (DRAFT)*
