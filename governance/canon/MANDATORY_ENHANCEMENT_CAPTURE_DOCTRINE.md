# Mandatory Enhancement Capture Doctrine

**Version**: 1.0.0  
**Status**: CANONICAL  
**Authority**: BUILD_PHILOSOPHY.md § Continuous Improvement  
**Date**: 2026-01-05  
**Type**: Behavioral Doctrine

---

## I. Constitutional Foundation

This doctrine establishes **Mandatory Enhancement Capture** as a constitutional behavioral requirement for all agents (builders, FM agents, and governance liaison agents) in the Maturion ISMS ecosystem.

**Core Principle**: After completing every job, agents must reflect on and capture potential future improvements, or explicitly state that none exist.

This doctrine prevents drift toward "execute and forget" behavior, ensures continuous improvement intelligence is captured, and maintains alignment with Maturion's One-Time Build philosophy.

---

## II. Doctrine Statement

### A. Universal Application

**Applies to**:
- All builder agents (UI, API, schema, integration, QA)
- Foreman (FM) agents (ForemanApp, FMRepoBuilder)
- Governance liaison agents

**Does NOT apply to**:
- Halted work (incomplete due to escalation)
- Aborted work (stopped due to blocking conditions)
- Work explicitly redirected by Johan

### B. Triggering Condition

Enhancement capture is MANDATORY at the **COMPLETE** terminal state of any work unit:
- Builder completing a build task
- FM completing a wave/subwave orchestration
- Governance liaison completing a governance alignment task

### C. Mandatory Reflection Prompt

At completion of ANY work unit, the agent MUST evaluate:

> "Are there structural, ergonomic, or governance improvements that:
> - Would reduce future work or friction,
> - Improve observability, safety, or clarity,
> - Close small obvious gaps intentionally left out-of-scope,
> - Strengthen architecture, QA, or compliance discipline?"

### D. Required Output

The agent MUST produce **exactly ONE** of:

1. **Enhancement proposal(s)** — one or more clearly scoped suggestions for future work, OR
2. **Explicit negation** — a statement that no material enhancements were identified

**Silence is NOT acceptable.**

---

## III. Enhancement Proposal Format

When enhancements are identified, agents MUST:

### A. Submit in Plain Language

- Use clear, concise bullets or short paragraphs
- No prescriptive implementation detail (unless architecturally relevant)
- No urgency language ("MUST", "CRITICAL", "URGENT")
- Frame as future opportunities, not current defects

### B. Mark as Parked

All enhancement proposals MUST be marked:

```
PARKED — NOT AUTHORIZED FOR EXECUTION
```

This signals that:
- The enhancement is **recognized** but **not approved** for immediate execution
- Execution requires **explicit FM authorization** (for builders) or **Johan authorization** (for FM/governance agents)
- The enhancement is **routed to the Parking Station** for future planning

### C. Route to Appropriate Authority

- **Builder enhancements** → Route to FM (Foreman App Parking Station)
- **FM enhancements** → Route to Johan (via escalation)
- **Governance enhancements** → Route to Johan (via escalation)

---

## IV. Explicit Negation Format

When no enhancements are identified, agents MUST state:

```
No material future enhancements identified beyond current scope.
```

Or equivalent clear statement that:
- Reflection was performed
- No meaningful improvements were found
- Current work is complete and sufficient

---

## V. Prohibitions (Scope Creep Prevention)

This doctrine does **NOT** authorize:

- ❌ Expanding current job scope to include enhancements
- ❌ Implementing enhancements proactively without authorization
- ❌ Skipping gates to "quickly add" enhancements
- ❌ Violating OPOJD (One Principle, One Job Discipline)
- ❌ Converting enhancement ideas into immediate tasks
- ❌ Escalating enhancements as blockers
- ❌ Treating enhancements as defects requiring immediate fix

**Clear Boundary**:
- **Capture** is mandatory (this doctrine)
- **Execution** requires authorization (separate governance)

---

## VI. Integration with OPOJD and One-Time Build

### A. Compatibility with One-Time Build

Enhancement capture does NOT conflict with One-Time Build Correctness because:
- Enhancements are **future work**, not current rework
- Enhancements are **parked**, not immediately executed
- Current job remains focused and complete
- No iteration toward perfection required

### B. Compatibility with OPOJD

Enhancement capture does NOT conflict with OPOJD because:
- Enhancements are captured **after** job completion
- Enhancements are **not added to current scope**
- Each enhancement is a potential **future job** with its own single principle
- Current job remains single-responsibility

---

## VII. Governance Position

### A. Enhancement Capture is Mandatory

- All agents MUST perform enhancement reflection at completion
- All agents MUST produce output (proposal or negation)
- Silence is a governance violation

### B. Enhancement Execution Requires Authorization

- Builders MUST NOT execute enhancements without FM authorization
- FM MUST NOT execute enhancements without Johan authorization
- Governance liaison MUST NOT execute enhancements without Johan authorization

### C. Parking Station is the Default Route

- All unexecuted enhancements go to Parking Station
- Parking Station is managed by FM (for builder enhancements) or Johan (for FM/governance enhancements)
- Parking Station is a planning input, not a backlog

---

## VIII. Evidence and Audit Trail

### A. Enhancement Proposals

When enhancements are captured:
- Store in completion report, PR body, or issue comment
- Mark with `PARKED — NOT AUTHORIZED FOR EXECUTION`
- Reference work unit that triggered the enhancement
- Include agent ID and timestamp

### B. Explicit Negations

When no enhancements are found:
- State explicitly in completion report or PR body
- No additional documentation required

---

## IX. Rationale

### A. Why Mandatory?

1. **Prevents "Execute and Forget" Behavior**: Ensures agents reflect on their work
2. **Captures Improvement Intelligence**: Builds institutional memory of improvement opportunities
3. **Supports Continuous Improvement**: Aligns with Maturion philosophy of iterative governance strengthening
4. **Reduces Repeated Discovery**: Future agents can reference prior enhancement proposals
5. **Maintains OPOJD Discipline**: Separates capture from execution, preventing scope creep

### B. Why Not Advisory?

Making enhancement capture **advisory** would:
- Allow agents to skip reflection
- Lose improvement intelligence
- Weaken continuous improvement discipline
- Create inconsistent completion semantics

---

## X. Applicability by Agent Type

### A. Builder Agents

**MUST capture enhancements related to**:
- Architecture clarity/completeness
- QA coverage/effectiveness
- Implementation patterns/practices
- Tool/library selection
- Build ergonomics

**Example**:
```
PARKED — NOT AUTHORIZED FOR EXECUTION

Potential Enhancement: Add TypeScript strict mode to reduce type safety gaps
Context: During Wave 2.1, several type errors were caught late in build
Impact: Would catch errors earlier in development cycle
Route: FM Parking Station for Wave 3+ consideration
```

### B. FM Agents (ForemanApp)

**MUST capture enhancements related to**:
- Wave orchestration efficiency
- Builder coordination patterns
- Gate enforcement mechanisms
- Evidence collection/validation
- Governance enforcement tooling

**Example**:
```
PARKED — NOT AUTHORIZED FOR EXECUTION

Potential Enhancement: Automate QA-Catalog-Alignment Gate pre-checks
Context: Manual gate execution prone to human error
Impact: Would reduce gate failure rate by 40% (estimated)
Route: Escalate to Johan for governance consideration
```

### C. Governance Liaison Agents

**MUST capture enhancements related to**:
- Governance alignment automation
- Ripple intelligence handling
- Canon validation tooling
- Cross-repo synchronization
- Governance observability

**Example**:
```
PARKED — NOT AUTHORIZED FOR EXECUTION

Potential Enhancement: Create automated Tier-0 canon consistency checker
Context: Manual validation missed 2 inconsistencies in PR #338
Impact: Would prevent canon drift and reduce validation burden
Route: Escalate to Johan for governance repo implementation
```

---

## XI. Integration with Existing Doctrine

### A. References

This doctrine integrates with:
- **BUILD_PHILOSOPHY.md** — One-Time Build Correctness, OPOJD
- **governance/policies/governance-supremacy-rule.md** — Governance defines scope
- **governance/policies/design-freeze-rule.md** — No mid-execution scope expansion
- **.github/agents/BUILDER_CONTRACT_SCHEMA.md** — Mandatory Enhancement Capture section template

### B. Alignment

- **No conflict** with existing doctrine
- **Strengthens** continuous improvement discipline
- **Clarifies** enhancement capture vs. execution boundary
- **Supports** institutional learning

---

## XII. Canonical Section Template

All agent contracts MUST include the following section (or close variant):

```markdown
## Post-Job Enhancement Reflection — MANDATORY

After declaring a job **COMPLETE**, this agent MUST:

1. Pause and consider whether there are structural, ergonomic, or governance improvements that:
   - Would reduce future work or friction,
   - Improve observability, safety, or clarity,
   - Or close small obvious gaps that were intentionally left out-of-scope.

2. If such improvements exist and are within this agent's governance boundaries:
   - Record them explicitly under a **"Possible Future Enhancements"** heading
     in the PR body, completion report, or issue comment.
   - Each enhancement must be framed as **future work**, not silently folded
     into the current job.
   - Mark all enhancements: `PARKED — NOT AUTHORIZED FOR EXECUTION`
   - Route to appropriate authority (FM for builders, Johan for FM/governance)

3. If no meaningful enhancements are identified:
   - State this explicitly (e.g., `No material future enhancements identified beyond current scope.`).

**This section does not authorize scope creep in the current job.**  
It mandates **capturing** enhancements for future planning under OPOJD and One-Time Build discipline.

**Canonical Authority**: `governance/canon/MANDATORY_ENHANCEMENT_CAPTURE_DOCTRINE.md`
```

---

## XIII. One-Time Permission for Governance Agent Self-Update

### A. Special Case Authorization

For **THIS GOVERNANCE ISSUE ONLY**, the governance liaison agent is granted a **one-time, explicit, and bounded permission** to:

1. Add the "Post-Job Enhancement Reflection — MANDATORY" section to their own agent contract file
2. Document in the PR body that this was done under this governance issue's authority
3. Include no other self-authorization or privilege escalation

### B. Constraints

- **Scope**: ONLY add the enhancement reflection section
- **No other changes**: No changes to role, authority, or permissions
- **Evidence required**: PR must document this exception explicitly
- **Review required**: PR must be reviewed/approved by Johan or equivalent human authority
- **One-time only**: This permission expires after this issue is complete

### C. Transparency

This exception is:
- **Documented** in this canonical doctrine
- **Bounded** to a single section addition
- **Transparent** via PR documentation
- **Reviewed** by human authority

This prevents precedent for unrestricted self-modification while allowing necessary doctrinal alignment.

---

## XIV. Layer-Down Plan

### A. FM Repository (maturion-foreman-office-app)

**Target Agents**:
1. ✅ UI Builder (already has section)
2. ✅ API Builder (already has section)
3. ✅ Schema Builder (already has section)
4. ✅ Integration Builder (already has section)
5. ✅ QA Builder (already has section)
6. ⬜ ForemanApp agent (needs section)
7. ⬜ Governance Liaison FM (needs section)

**Action Required**:
- Add canonical section to ForemanApp-agent.md
- Add canonical section to governance-liaison.md (one-time self-update authorized)
- Update references in BUILDER_CONTRACT_SCHEMA.md (already compliant)

### B. Other ISMS Repos (Future)

**IF** other repositories use `.agent` contracts:
- Open follow-up issues to propagate the same standard section
- Reference this canonical doctrine
- Apply consistently across all agent types

### C. Governance Repository (maturion-foreman-governance)

**Action Required** (separate issue):
- Mirror this doctrine in governance repo (if not already present)
- Ensure cross-repo governance alignment
- Update any governance agent contracts in governance repo

---

## XV. Completion Criteria

This doctrine is **COMPLETE** and **ACTIVE** when:

- ✅ This canonical document exists and is approved
- ✅ Standard section template is defined and documented
- ✅ One-time permission for governance agent self-update is documented
- ✅ Layer-down plan is articulated for FM repo and other repos
- ✅ FM agent contracts updated to include the section
- ✅ Governance liaison contract updated to include the section (one-time authorized)
- ✅ All changes validated and merged

---

## XVI. Constitutional Status

**Tier**: Behavioral Doctrine (Tier 1 equivalent)  
**Authority**: BUILD_PHILOSOPHY.md § Continuous Improvement  
**Binding**: All agents in Maturion ISMS ecosystem  
**Enforcement**: Via agent contracts, completion validation, and governance review  
**Modification**: Requires Johan approval and governance repo alignment

---

## XVII. Version History

| Version | Date | Changes | Authority |
|---------|------|---------|-----------|
| 1.0.0 | 2026-01-05 | Initial canonization | Johan Ras (CS2) |

---

**This doctrine is now CANONICAL and ACTIVE across the Maturion ISMS ecosystem.**

**Doctrine Authority**: Johan Ras (CS2)  
**Implementation Authority**: Governance Liaison Agent (FM repo)  
**Enforcement Authority**: Foreman (FM) and Human Review

---

*END OF MANDATORY ENHANCEMENT CAPTURE DOCTRINE*
