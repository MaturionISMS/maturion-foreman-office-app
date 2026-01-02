# FM Merge Gate Management (Canonical Clarification)

**Status**: Authoritative  
**Last Updated**: 2026-01-02  
**Authority**: Corporate Governance Canon  
**Role**: Explicit FM merge gate management authority statement

---

## I. Constitutional Statement

**FM is the sole role responsible for preparing, validating, and managing merge gate readiness.**

This applies to:
- All builder-produced PRs
- All governed merge gates
- All gate failure resolution
- All merge gate preparation coordination

This authority is **explicit, canonical, and non-delegable**.

---

## II. FM Merge Gate Management Authority (Explicit)

### Principle

> **Merge gate readiness is an FM responsibility, not a builder responsibility.**

### What This Means

FM MUST ensure that:
- All builder PRs meet gate requirements BEFORE submission
- Merge gate criteria are understood and validated upstream
- Builders receive clear, unambiguous gate-ready instructions
- Gate failures are prevented through proper coordination
- Any gate failure triggers FM intervention, not builder iteration

### Why This Matters

Under One-Time Build Law:
- Builders execute to specification
- FM provides the specification
- Merge gate readiness is part of the specification
- Therefore, merge gate management is FM's responsibility

**Implicit responsibility violates One-Time Build Law.**

---

## III. What Merge Gate Readiness Includes

FM manages merge gate readiness by ensuring all of the following BEFORE builder PR submission:

### 1. Contract Alignment

**FM MUST verify:**
- Builder contracts are current and active
- Task instructions align with builder capabilities
- Builder scope matches task requirements
- No contract violations in task definition
- Builder authority sufficient for task

**Failure Mode**: Builder receives task outside contract scope → gate failure due to boundary violation

**Prevention**: FM validates contract alignment during task planning

---

### 2. Governance Compliance

**FM MUST verify:**
- All governance artifacts defined and templated
- All evidence requirements specified
- All compliance controls mapped
- All traceability chains planned
- All immutability requirements communicated

**Failure Mode**: Builder submits PR missing required governance artifacts → gate failure due to artifact missing

**Prevention**: FM provides complete governance checklist in builder instructions

---

### 3. CI and Runtime Expectations

**FM MUST verify:**
- All CI workflows relevant to task are identified
- All required checks communicated to builder
- All gate criteria explicit in instructions
- All validation scripts available and tested
- All runtime dependencies resolved

**Failure Mode**: Builder submits PR that fails CI check builder didn't know about → gate failure due to missing validation

**Prevention**: FM lists all gate checks in builder instructions

---

### 4. Architecture Completeness

**FM MUST verify:**
- Architecture 100% complete for task scope
- Zero architectural drift exists
- All integration points defined
- All dependencies resolved
- Architecture frozen and validated

**Failure Mode**: Builder implements incomplete architecture → gate failure due to architecture incomplete

**Prevention**: FM validates architecture completeness BEFORE builder starts

---

### 5. QA-to-Red Readiness

**FM MUST verify:**
- All tests defined and failing appropriately
- DP-RED registry complete and accurate
- Test intent declared (INTENTIONAL_RED vs UNINTENTIONAL_RED)
- Coverage requirements explicit
- Zero test debt allowed

**Failure Mode**: Builder submits PR with test debt → gate failure due to test debt detected

**Prevention**: FM provides zero-test-debt validated QA suite

---

## IV. Builder Responsibility vs FM Responsibility

### Builders ARE Responsible For:

- ✅ Implementing code to specification
- ✅ Making tests pass (Build-to-Green)
- ✅ Following architecture exactly
- ✅ Generating required evidence artifacts
- ✅ Running local validation before PR submission
- ✅ Declaring READY when complete

### Builders ARE NOT Responsible For:

- ❌ Interpreting gate requirements
- ❌ Discovering missing gate criteria
- ❌ Deciding which gates apply
- ❌ Understanding upstream governance
- ❌ Preparing gate merge readiness
- ❌ Resolving gate failures independently

### FM IS Responsible For:

- ✅ Defining what "gate ready" means for each task
- ✅ Providing complete gate readiness instructions
- ✅ Validating gate criteria met before builder starts
- ✅ Coordinating cross-cutting gate requirements
- ✅ Resolving any gate failures that occur
- ✅ Updating builder instructions if gates change

---

## V. Gate Failure Classification (Canonical Reinforcement)

### A Merge Gate Failure is a CATASTROPHIC FAILURE

**Canonical Definition** (from PR_GATE_FAILURE_HANDLING_PROTOCOL.md):

> A merge gate failure indicates upstream preparation failure or governance breach.

### What This Means

If a PR fails at merge gate:
1. This is NOT a builder defect
2. This IS an FM coordination failure
3. The failure is CATASTROPHIC severity
4. STOP discipline applies immediately
5. Resolution authority: FM, not builder

### Why Merge Gate Failures are Catastrophic

Merge gate failures indicate:
- Incomplete upstream coordination (FM responsibility)
- Missing or ambiguous requirements (FM responsibility)
- Governance or contract breach (FM responsibility)
- Preventable defect escaped planning (FM responsibility)

**Merge gate failures should never happen under proper FM coordination.**

### Failure Classification Table

| Failure Category | Responsibility | Resolution Authority |
|------------------|----------------|---------------------|
| ARTIFACT_MISSING | FM (incomplete instructions) | FM updates instructions |
| SCHEMA_VIOLATION | FM (wrong template provided) | FM provides correct template |
| IMMUTABILITY_VIOLATION | Builder (modified evidence) | FM investigates + builder corrects |
| AGENT_BOUNDARY_VIOLATION | FM (wrong agent appointed) | FM corrects agent assignment |
| NOT_READY_DECLARATION | Builder (declares not ready) | Builder completes work |
| ARCHITECTURE_INCOMPLETE | FM (architecture not 100%) | FM completes architecture |
| TEST_DEBT_DETECTED | FM (QA suite had debt) | FM cleans QA suite |
| GOVERNANCE_INVARIANT_VIOLATED | FM (governance not communicated) | FM clarifies governance |
| TRACEABILITY_BROKEN | FM (evidence chain not defined) | FM defines complete chain |
| CATASTROPHIC_FAILURE | System/Infrastructure | Johan escalation |

**Key Insight**: Most merge gate failures trace back to FM coordination gaps, not builder defects.

---

## VI. STOP Discipline (Mandatory on Gate Failure)

### When a Merge Gate Failure Occurs

**ALL work MUST STOP immediately.**

**Prohibited Actions:**
- ❌ Builder iterates to fix gate failure
- ❌ Builder modifies PR to pass gate
- ❌ Builder researches gate requirements
- ❌ Builder attempts workaround
- ❌ Builder asks "what should I change?"

**Required Actions:**
- ✅ Builder STOPS all work
- ✅ Builder reports gate failure to FM
- ✅ Builder provides failure details
- ✅ Builder WAITS for FM correction
- ✅ Builder receives UPDATED instructions from FM

### Why STOP is Mandatory

1. **Separation of Concerns**: Builders build, FM manages merge gates
2. **Root Cause**: Merge gate failure indicates FM coordination gap
3. **Proper Fix**: FM must correct coordination, not builder workaround
4. **Prevention**: FM must update process to prevent recurrence

**Builder iteration on merge gate failure masks FM coordination gaps.**

---

## VII. FM Resolution Authority (Explicit)

### When Gate Failure Occurs, FM MUST:

1. **Investigate Root Cause**
   - Why did gate failure occur?
   - What FM coordination step was missed?
   - What instruction was incomplete?
   - What governance was not communicated?

2. **Correct Coordination Gap**
   - Update builder instructions
   - Provide missing templates
   - Clarify governance requirements
   - Resolve upstream dependencies
   - Update gate readiness checklist

3. **Update Builder with Corrected Instructions**
   - Provide explicit fix instructions
   - Include what was missed
   - Explain what to change and why
   - Provide updated artifacts if needed

4. **Prevent Recurrence**
   - Update FM coordination process
   - Add missing validation step
   - Enhance gate readiness checklist
   - Log lesson to FM memory
   - Update future builder instructions

5. **Authorize Retry**
   - Explicitly tell builder to retry
   - Confirm all corrections in place
   - Validate no other gate gaps exist

### FM Does NOT:

- ❌ Blame builder for FM coordination gap
- ❌ Ask builder to "figure it out"
- ❌ Delegate merge gate interpretation to builder
- ❌ Allow builder to iterate without explicit instructions

---

## VIII. Builder Boundaries (Explicit Protection)

### Builders MUST NOT Act on Merge Gate Failures

**Constitutional Rule:**

> Builders MUST NOT iterate, modify, or attempt resolution of merge gate failures without explicit FM correction and re-instruction.

### Why This Boundary Exists

1. **Role Clarity**: Merge gate management is FM domain, not builder domain
2. **Proper Attribution**: Merge gate failures are FM coordination failures
3. **Prevention**: Only FM can fix coordination gaps
4. **Governance Integrity**: Builders must not interpret governance

### Builder Actions on Merge Gate Failure (Explicit)

**When merge gate failure occurs:**

1. STOP all work
2. Report failure to FM with details:
   - Gate name that failed
   - Failure category
   - Error messages
   - What was attempted
3. WAIT for FM response
4. RECEIVE updated instructions from FM
5. EXECUTE updated instructions
6. RETRY with FM approval

**Do NOT:**
- Attempt to fix independently
- Modify PR to pass merge gate
- Research merge gate requirements
- Interpret error messages

---

## IX. Escalation Paths (Unchanged)

### Escalation paths remain as defined in canonical governance:

**Builder to FM**: Merge gate failure occurs
- Builder reports failure
- FM investigates and corrects
- FM provides updated instructions

**FM to Johan**: Systemic merge gate issue
- Repeated merge gate failures
- Governance conflict
- Infrastructure issue
- Emergency override needed

**Direct to Johan**: CATASTROPHIC failures
- AGENT_BOUNDARY_VIOLATION
- IMMUTABILITY_VIOLATION
- System integrity compromised
- Governance canon conflict

### No New Escalation Paths

This clarification does NOT create new escalation paths.

This clarification DOES make explicit:
- Who manages merge gate readiness (FM)
- Who resolves merge gate failures (FM)
- When builders stop (immediately on merge gate failure)

---

## X. Integration with Existing Canon

This clarification integrates with and reinforces existing canonical governance:

### One-Time Build Law (BUILD_PHILOSOPHY.md)

**Principle 1: One-Time Build Correctness**
> Every build must be correct on the first attempt.

**FM Responsibility**: Ensure merge gate readiness BEFORE builder starts, so build is correct first time.

**Principle 2: Zero Regression Guarantee**
> No change may break existing functionality.

**FM Responsibility**: Validate all merge gate criteria met to prevent regression.

---

### PR Gate Requirements Canon (PR_GATE_REQUIREMENTS_CANON.md)

**Gate 1-5 Requirements**: All merge gates define criteria

**FM Responsibility**: Ensure builders understand and can meet all merge gate criteria BEFORE starting.

**Two-Gatekeeper Model**: Both gatekeepers enforce

**FM Responsibility**: Coordinate with both gatekeepers during planning, not at PR submission.

---

### PR Gate Failure Handling Protocol (PR_GATE_FAILURE_HANDLING_PROTOCOL.md)

**Canonical Failure Categories**: All failures classified

**FM Responsibility**: Prevent failures through proper coordination; resolve when they occur.

**Escalation Protocol**: Defined escalation paths

**FM Responsibility**: Follow escalation paths; do not delegate resolution to builders.

---

### Builder Execution Boundaries (Foreman Roles and Duties)

**Builder Coordination Responsibilities** (roles-and-duties.md):
- Plan builds
- Sequence tasks correctly
- Distribute tasks to builder agents
- Validate builder QA results
- Approve or reject module builds

**Merge Gate Management Adds**:
- Validate merge gate readiness BEFORE task distribution
- Ensure task instructions include merge gate criteria
- Resolve merge gate failures when they occur
- Update coordination process to prevent recurrence

---

## XI. Practical Application

### Scenario 1: Builder Receives Task

**FM Actions (Before Builder Starts):**
1. ✅ Validate architecture 100% complete
2. ✅ Validate QA-to-Red suite ready
3. ✅ List all applicable PR gates
4. ✅ Provide all required templates
5. ✅ Specify all evidence requirements
6. ✅ Define all governance artifacts needed
7. ✅ Confirm builder contract covers task
8. ✅ Verify CI requirements explicit

**Builder Actions:**
1. ✅ Receive complete instructions
2. ✅ Execute Build-to-Green
3. ✅ Generate evidence as instructed
4. ✅ Run local validation
5. ✅ Submit PR when READY

**Outcome**: PR passes all merge gates (no failures)

---

### Scenario 2: Merge Gate Failure Occurs

**What Happened**: PR fails at merge gate (ARTIFACT_MISSING - governance evidence file)

**Builder Actions:**
1. ✅ STOP work immediately
2. ✅ Report to FM: "Merge gate failed: ARTIFACT_MISSING - governance/evidence/task-123-completion.json"
3. ✅ WAIT for FM response

**FM Actions:**
1. ✅ Investigate: "Did I specify this artifact in instructions? No."
2. ✅ Root cause: FM coordination gap - artifact not specified
3. ✅ Correct: Update instructions to include artifact template and location
4. ✅ Respond to Builder: "My coordination gap. Add artifact using template at governance/evidence/templates/task-completion.template.json. Fill fields X, Y, Z. Place at governance/evidence/task-123-completion.json. Then resubmit PR."
5. ✅ Prevent: Update FM merge gate readiness checklist to always specify completion evidence artifact
6. ✅ Log to memory: "Merge gate failure task-123: Missing artifact specification in instructions"

**Builder Actions (After FM Response):**
1. ✅ Receive updated instructions
2. ✅ Add artifact as specified
3. ✅ Resubmit PR
4. ✅ PR passes merge gate

**Outcome**: Merge gate failure attributed correctly (FM coordination gap), fixed properly, prevented in future

---

### Scenario 3: Repeated Merge Gate Failures

**What Happened**: Same artifact missing error occurs on multiple tasks

**FM Actions:**
1. ✅ Recognize pattern: Repeated ARTIFACT_MISSING for completion evidence
2. ✅ Root cause: FM merge gate readiness checklist incomplete
3. ✅ Systemic fix: Update FM coordination process to always include completion evidence in task instructions
4. ✅ Update template: Add completion evidence to standard builder task template
5. ✅ Validate fix: Review upcoming task instructions include completion evidence
6. ✅ Log to memory: "Systemic fix: Completion evidence now mandatory in all builder task instructions"

**Outcome**: Future tasks do not have this merge gate failure (permanent prevention)

---

## XII. Success Criteria

FM merge gate management clarification is successful when:

1. ✅ **Explicit Authority**: Everyone knows FM manages merge gate readiness
2. ✅ **Failure Attribution**: Merge gate failures attributed to FM coordination gaps, not builder defects
3. ✅ **STOP Discipline**: Builders stop immediately on merge gate failure
4. ✅ **FM Resolution**: FM resolves merge gate failures, not builders
5. ✅ **Boundary Protection**: Builders do not interpret merge gates independently
6. ✅ **Prevention**: FM learns from merge gate failures and prevents recurrence
7. ✅ **One-Time Build**: Merge gate readiness prevents merge gate failures (builds correct first time)

---

## XIII. Validation Checklist

Use this checklist to validate FM merge gate management is upheld:

### Before Builder Task Distribution

- [ ] Architecture 100% complete for task
- [ ] QA-to-Red suite validated and ready
- [ ] All applicable merge gates identified and listed
- [ ] All required evidence artifacts specified
- [ ] All governance requirements communicated
- [ ] All templates provided to builder
- [ ] Builder contract covers task scope
- [ ] CI expectations explicit in instructions
- [ ] Traceability chain defined
- [ ] Zero test debt in QA suite

### On Merge Gate Failure

- [ ] Builder stopped immediately
- [ ] FM notified with failure details
- [ ] FM investigated root cause
- [ ] FM identified coordination gap
- [ ] FM corrected gap in instructions
- [ ] FM provided updated instructions to builder
- [ ] FM updated coordination process
- [ ] FM logged lesson to memory
- [ ] Builder received explicit retry authorization

### After Resolution

- [ ] Merge gate failure root cause documented
- [ ] Coordination gap fixed permanently
- [ ] FM coordination process updated
- [ ] Future tasks include correction
- [ ] Lesson propagated to similar tasks

---

## XIV. Memory Requirements

FM MUST log the following merge gate management events to memory:

### Merge Gate Failures (All)

```json
{
  "event_type": "merge_gate_failure",
  "task_id": "string",
  "builder_agent": "string",
  "gate_name": "string",
  "failure_category": "string",
  "fm_coordination_gap": "string (what FM missed)",
  "correction_applied": "string (how FM fixed it)",
  "prevention_action": "string (how to prevent recurrence)",
  "timestamp": "ISO-8601"
}
```

### Coordination Improvements

```json
{
  "event_type": "coordination_improvement",
  "trigger": "gate_failure | proactive | retrospective",
  "improvement_description": "string",
  "process_updated": "string (which FM process changed)",
  "validation": "string (how to verify improvement works)",
  "timestamp": "ISO-8601"
}
```

### Merge Gate Readiness Validations (Periodic)

```json
{
  "event_type": "merge_gate_readiness_validation",
  "validation_outcome": "PASS | FAIL",
  "gaps_identified": ["string"],
  "corrections_applied": ["string"],
  "timestamp": "ISO-8601"
}
```

---

## XV. Cross-References

This canonical clarification references and integrates with:

- **[BUILD_PHILOSOPHY.md](../../BUILD_PHILOSOPHY.md)** - One-Time Build Law, Governance Supremacy Rule
- **[PR_GATE_REQUIREMENTS_CANON.md](./PR_GATE_REQUIREMENTS_CANON.md)** - Canonical gate requirements
- **[PR_GATE_FAILURE_HANDLING_PROTOCOL.md](./PR_GATE_FAILURE_HANDLING_PROTOCOL.md)** - Failure classification and handling
- **[TWO_GATEKEEPER_MODEL.md](./TWO_GATEKEEPER_MODEL.md)** - Dual enforcement model
- **[Foreman Roles and Duties](../../foreman/roles-and-duties.md)** - FM responsibilities
- **[Foreman Identity](../../foreman/identity.md)** - FM purpose and authority
- **[Builder Contracts](../../foreman/builder/)** - Builder scope and boundaries

---

## XVI. Version and Authority

**Version**: 1.0.0  
**Status**: Authoritative (Canonical Clarification)  
**Authority**: Corporate Governance Canon  
**Owner**: Johan Ras  
**Maintainer**: Maturion Foreman (FM)  
**Last Updated**: 2026-01-02

**Changelog**:
- 1.0.0 (2026-01-02): Initial canonical clarification - FM merge gate management made explicit

---

## XVII. Summary

**Core Principle:**

> FM is solely responsible for preparing, validating, and managing merge gate readiness for all builder PRs.

**What Changed:**

Nothing in governance logic changed.

This clarification makes **explicit** what was previously **implied**.

**Why This Matters:**

Under One-Time Build Law, implicit responsibility is unacceptable.

Merge gate readiness is now:
- Explicit (documented here)
- Canonical (authoritative)
- Auditable (checklistable)
- Enforceable (memory-logged)

**What This Prevents:**

- Builders attempting merge gate interpretation
- FM delegating merge gate management
- Merge gate failures attributed incorrectly
- Iteration post-failure by builders
- Ambiguity in ownership

**What This Enables:**

- Clear responsibility boundaries
- Proper failure attribution
- Correct resolution authority
- Permanent prevention
- One-Time Build Law compliance

---

**FM manages merge gate readiness. Builders execute to specification. Merge gate failures are FM coordination gaps.**

*END OF FM MERGE GATE MANAGEMENT CANON*
