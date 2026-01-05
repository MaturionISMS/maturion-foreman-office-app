# In-Between Wave Reconciliation (IBWR) Specification

**Version**: 1.0.0  
**Status**: Active  
**Authority**: Canonical Governance (PR #867)  
**Date**: 2026-01-04  
**Purpose**: Layer-down governance requirement into operational execution surface

---

## I. Constitutional Grounding

### Purpose

In-Between Wave Reconciliation (IBWR) is a **mandatory governance requirement** that captures execution learnings and reconciles systemic issues revealed during wave execution BEFORE authorizing the next wave.

### Authority

This specification implements the governance-level requirement established in PR #867 and makes it **operationally binding** within the FM execution surface.

### Problem Statement

Wave 1 execution demonstrated that without explicit IBWR:
- Corrections occur reactively instead of proactively
- Ripple propagation is delayed or missed
- Execution relies on human memory instead of structure
- Systemic patterns are not captured between waves
- Next wave may repeat failures from previous wave

### Solution

IBWR creates a **structural gate** between waves that:
- CANNOT be skipped
- BLOCKS next wave authorization until complete
- Produces canonical artifacts
- Captures learnings systematically
- Propagates corrections to governance and contracts

---

## II. IBWR Definition

### What IBWR Is

In-Between Wave Reconciliation is a **mandatory execution phase** that occurs:

**TRIGGER**: After wave gate declares PASS (all builders GREEN, all gates satisfied)

**BEFORE**: Next wave authorization or planning begins

**OUTCOME**: Wave Reconciliation PASS or corrective actions identified

### What IBWR Is NOT

- ❌ NOT a retrospective meeting (this is structural, not conversational)
- ❌ NOT optional learning capture (this is mandatory gate)
- ❌ NOT post-mortem only for failures (applies to ALL waves)
- ❌ NOT human-memory dependent (produces canonical artifacts)

---

## III. IBWR Triggers

IBWR MUST be executed when:

1. ✅ **Wave Gate Declares PASS**
   - All assigned builders report GREEN
   - All PR gates passed
   - All QA validation complete
   - FM declares wave complete

2. ✅ **Wave Contains Learning Opportunities**
   - Any builder escalation occurred
   - Any gate failure occurred (even if later resolved)
   - Any architecture clarification was needed
   - Any governance ambiguity was discovered
   - Any novel pattern was encountered

3. ✅ **Next Wave Authorization Is Requested**
   - Cannot authorize Wave N+1 without Wave N IBWR PASS

### Bootstrap Exception

**Wave 0** (Builder Recruitment): IBWR may be abbreviated as no implementation execution occurred.

**Wave 1+**: Full IBWR mandatory for all waves.

---

## IV. IBWR Responsibilities

### FM Responsibilities (Execution Authority)

FM MUST:

1. ✅ **Initiate IBWR** immediately after wave gate PASS
2. ✅ **Collect Execution Evidence**
   - Builder escalations and resolutions
   - Gate failures and corrections
   - Architecture clarifications
   - Governance ambiguities discovered
   - Iteration patterns and counts
3. ✅ **Identify Systemic Issues**
   - Patterns affecting multiple builders
   - Governance gaps requiring correction
   - Architecture template improvements
   - Contract clarifications needed
4. ✅ **Generate Canonical Artifacts** (see Section VI)
5. ✅ **Verify Ripple Propagation**
   - Governance updates if needed
   - Contract updates if needed
   - Builder re-instruction if needed
6. ✅ **Declare IBWR Status** (PASS / CORRECTIVE_ACTIONS_REQUIRED)
7. ✅ **Block Next Wave** until IBWR PASS

FM MUST NOT:

- ❌ Skip IBWR to "save time"
- ❌ Authorize next wave without IBWR PASS
- ❌ Treat IBWR as optional
- ❌ Rely on human memory instead of artifacts

---

### Governance Responsibilities (Governance Authority)

Governance MUST:

1. ✅ **Review IBWR Artifacts** when corrective actions identified
2. ✅ **Validate Ripple Signals** if governance changes needed
3. ✅ **Approve Corrective Governance Changes** if required
4. ✅ **Verify FM Compliance** with IBWR requirements

Governance MUST NOT:

- ❌ Execute IBWR on FM's behalf (FM owns execution)
- ❌ Bypass IBWR requirement
- ❌ Authorize next wave without IBWR verification

---

### Builder Responsibilities (Execution Agents)

Builders MUST:

1. ✅ **Acknowledge IBWR Existence** in contracts
2. ✅ **Respond to Retroactive Clarification Requests** from IBWR
3. ✅ **Accept Wave Completion as Provisional** until IBWR complete

Builders MUST NOT:

- ❌ Assume wave completion is final before IBWR
- ❌ Advance to next wave without FM authorization post-IBWR
- ❌ Treat IBWR clarifications as rework (they are clarifications)

**Critical Distinction**: IBWR may request clarification or evidence from builders, but does NOT grant rework authority.

---

## V. IBWR Execution Workflow

### Phase 1: Initiation (FM)

**Trigger**: Wave gate declares PASS

**Actions**:
1. FM initiates IBWR phase
2. FM updates execution state: `WAVE_N_IBWR_IN_PROGRESS`
3. FM emits IBWR_INITIATED event

**Duration**: Immediate (< 1 hour)

---

### Phase 2: Evidence Collection (FM)

**Actions**:
1. Gather all builder execution reports
2. Collect all gate pass/fail events
3. Collect all escalation records
4. Collect all architecture clarifications
5. Collect all iteration patterns
6. Identify systemic vs. isolated issues

**Duration**: 1-4 hours (depends on wave complexity)

**Output**: Evidence collection complete

---

### Phase 3: Analysis & Pattern Recognition (FM)

**Actions**:
1. Identify recurring patterns across builders
2. Detect governance gaps
3. Identify architecture template improvements
4. Recognize novel patterns for memory storage
5. Assess ripple impact scope

**Duration**: 2-8 hours

**Output**: Analysis summary with identified issues

---

### Phase 4: Corrective Action Planning (FM + Governance if needed)

**Actions**:
1. For each systemic issue:
   - Define corrective action
   - Identify ripple scope
   - Assign responsibility (FM / Governance / Builder)
   - Estimate completion time
2. Create Corrective Action Summary
3. Escalate to Governance if governance changes needed
4. Await Governance approval if escalated

**Duration**: 4-16 hours (may span days if governance changes)

**Output**: Corrective Action Plan approved

---

### Phase 5: Ripple Propagation (FM or Governance)

**Actions**:
1. Execute approved corrective actions
2. Update governance artifacts if needed
3. Update contract artifacts if needed
4. Update builder instructions if needed
5. Validate ripple completeness

**Duration**: 2-24 hours (depends on ripple scope)

**Output**: All corrective actions complete

---

### Phase 6: Artifact Generation (FM)

**Actions**:
1. Generate Wave Reconciliation Report
2. Generate Retrospective Certification
3. Generate Corrective Actions Summary (if applicable)
4. Store artifacts in canonical location
5. Index artifacts for future reference

**Duration**: 1-2 hours

**Output**: Canonical artifacts complete

---

### Phase 7: IBWR Declaration (FM)

**Actions**:
1. FM reviews all phases complete
2. FM declares IBWR status:
   - **PASS**: No corrective actions OR all corrective actions complete
   - **CORRECTIVE_ACTIONS_REQUIRED**: Actions identified but not complete
3. FM updates execution state
4. FM emits IBWR_COMPLETE event (if PASS)

**Duration**: < 1 hour

**Output**: IBWR status declared

---

### Phase 8: Next Wave Authorization Gate (FM)

**Condition**: IBWR status = PASS

**Actions**:
1. FM verifies IBWR PASS
2. FM authorizes next wave planning
3. FM loads learnings into next wave context

**Condition NOT Met**: IBWR status ≠ PASS

**Actions**:
1. FM BLOCKS next wave authorization
2. FM waits for corrective actions to complete
3. FM returns to Phase 7 when ready

---

## VI. Mandatory Canonical Artifacts

IBWR MUST produce the following artifacts:

### 1. Wave Reconciliation Report

**Filename**: `WAVE_<N>_RECONCILIATION_REPORT.md`

**Location**: `/governance/reports/waves/`

**Purpose**: Comprehensive evidence and analysis of wave execution

**Required Sections**:
- Wave Summary (scope, builders, tasks, duration)
- Execution Evidence (escalations, iterations, clarifications)
- Systemic Issues Identified
- Isolated Issues Noted
- Pattern Recognition
- Ripple Impact Assessment
- IBWR Status Declaration

**Template**: `governance/templates/WAVE_RECONCILIATION_REPORT_TEMPLATE.md`

---

### 2. Retrospective Certification

**Filename**: `WAVE_<N>_RETROSPECTIVE_CERTIFICATION.md`

**Location**: `/governance/reports/waves/`

**Purpose**: FM certification that IBWR was executed completely

**Required Sections**:
- IBWR Phases Completed (checklist)
- Evidence Sources Referenced
- Systemic Issues Count
- Corrective Actions Status
- Ripple Propagation Verified
- Next Wave Authorization Status
- FM Signature and Date

**Template**: `governance/templates/WAVE_RETROSPECTIVE_CERTIFICATION_TEMPLATE.md`

---

### 3. Corrective Actions Summary (Conditional)

**Filename**: `WAVE_<N>_CORRECTIVE_ACTIONS.md`

**Location**: `/governance/reports/waves/`

**Purpose**: Track corrective actions identified and their completion

**Required Only If**: Corrective actions were identified

**Required Sections**:
- Corrective Action ID and Description
- Root Cause
- Ripple Scope
- Responsible Party (FM / Governance / Builder)
- Status (PENDING / IN_PROGRESS / COMPLETE)
- Verification Evidence
- Completion Date

**Template**: `governance/templates/WAVE_CORRECTIVE_ACTIONS_TEMPLATE.md`

---

## VII. IBWR Blocking Conditions

### Next Wave CANNOT Be Authorized If:

1. ❌ IBWR not initiated
2. ❌ IBWR phases incomplete
3. ❌ Mandatory artifacts missing
4. ❌ IBWR status ≠ PASS
5. ❌ Corrective actions identified but not complete
6. ❌ Ripple propagation not verified

### Enforcement

**Gate**: Next wave authorization is structurally blocked in FM execution logic

**Verification**: FM MUST verify IBWR PASS before proceeding to Wave N+1 planning

**Escalation**: If IBWR cannot complete within reasonable time (5 business days), FM MUST escalate to Johan

---

## VIII. IBWR and Bootstrap Mode

### Wave 0 (Builder Recruitment)

**IBWR Required?**: Abbreviated

**Rationale**: No implementation execution occurred, only recruitment

**Minimum IBWR**:
- Verify all builders recruited
- Verify all contracts valid
- Verify no recruitment issues
- Generate Retrospective Certification only (no Reconciliation Report needed)

---

### Wave 1+ (Implementation Waves)

**IBWR Required?**: Full IBWR mandatory

**Rationale**: Implementation execution occurred, learnings exist

**Full IBWR**: All phases and artifacts required

---

## IX. IBWR and Failure Modes

### IBWR Purpose for Successful Waves

IBWR applies to **all waves**, not just failed waves.

**Successful Wave** still produces:
- Learnings about what worked well
- Minor improvements to process
- Pattern recognition for scaling
- Memory capture for future waves

---

### IBWR Purpose for Challenged Waves

**Challenged Wave** (multiple failures, escalations) produces:
- Systemic root cause analysis
- Corrective governance actions
- Contract clarifications
- Architecture template improvements
- Preventive measures for future waves

---

## X. IBWR Integration Points

### Integration with FM Agent Contract

FM agent contract (`.github/agents/ForemanApp-agent.md`) MUST:
- Reference this specification as mandatory
- Require IBWR execution between waves
- Prohibit next wave authorization without IBWR PASS
- Define IBWR verification as FM responsibility

---

### Integration with Builder Contracts

All builder contracts MUST:
- Acknowledge IBWR existence
- Accept wave completion as provisional until IBWR
- Respond to retroactive clarification requests
- Distinguish clarification from rework authority

---

### Integration with Execution State Model

Execution state model (`governance/specs/foreman-execution-state-model.md`) MUST:
- Include IBWR states: `WAVE_N_IBWR_IN_PROGRESS`, `WAVE_N_IBWR_COMPLETE`
- Define state transitions including IBWR phases
- Emit IBWR events for observability

---

### Integration with Wave Planning

Next wave planning MUST:
- Verify previous wave IBWR PASS before starting
- Load IBWR learnings into planning context
- Reference IBWR artifacts for pattern avoidance

---

## XI. IBWR Success Criteria

IBWR is successful when:

✅ All IBWR phases executed completely  
✅ All mandatory artifacts generated and indexed  
✅ All systemic issues identified and analyzed  
✅ All corrective actions complete (if any)  
✅ All ripple effects propagated and verified  
✅ Retrospective Certification signed by FM  
✅ IBWR status = PASS  
✅ Next wave authorization unblocked  

---

## XII. Anti-Patterns (Prohibited)

The following are **explicitly prohibited**:

❌ **Skipping IBWR** - "Wave was simple, no need"  
❌ **Informal IBWR** - "I remember what happened, no artifacts needed"  
❌ **Partial IBWR** - "Just the report, skip certification"  
❌ **Delayed IBWR** - "Start next wave, do IBWR later"  
❌ **Human-Memory IBWR** - "Johan knows, don't need to document"  
❌ **Reactive-Only IBWR** - "Only do IBWR if wave failed"  

---

## XIII. Observability Requirements

FM execution surface MUST support:

1. **IBWR State Visibility** - Show IBWR in progress
2. **IBWR Phase Tracking** - Show which phase currently executing
3. **IBWR Artifact Status** - Show artifacts generated/pending
4. **IBWR Blocking Status** - Show next wave blocked/unblocked
5. **IBWR Event History** - Show all IBWR events for wave

**Reference**: `governance/specs/FM_EXECUTION_SURFACE_OBSERVABILITY_SPEC.md`

---

## XIV. IBWR and Continuous Improvement

### Memory Fabric Integration

IBWR artifacts MUST be:
- Indexed in FM memory fabric
- Searchable for pattern recognition
- Referenced in future wave planning
- Used for governance improvement

---

### Governance Evolution

IBWR enables:
- Continuous governance refinement
- Evidence-based policy updates
- Pattern-driven template improvements
- Systemic issue prevention

---

## XV. Version History

**Version 1.0.0** (2026-01-04):
- Initial specification
- Layer-down from governance requirement (PR #867)
- Makes IBWR operationally binding
- Defines complete workflow and artifacts

---

## XVI. References

**Governance Authority**:
- PR #867 (In-Between Wave Reconciliation requirement)
- BUILD_PHILOSOPHY.md (One-Time Build Correctness)
- governance/alignment/FM_MERGE_GATE_MANAGEMENT_CANON.md

**Related Specifications**:
- `governance/specs/foreman-execution-state-model.md` (Execution states)
- `governance/specs/FM_EXECUTION_SURFACE_OBSERVABILITY_SPEC.md` (Observability)
- `.github/agents/ForemanApp-agent.md` (FM authority)

**Learning Sources**:
- `foreman/ai-memory/build-wave-1-learnings.md` (Wave 1 execution learnings)
- `WAVE1_COMPLETION_SUMMARY.md` (Wave 1 completion)

---

**Specification Status**: ✅ ACTIVE  
**Authority**: Canonical Governance  
**Enforcement**: Structural (non-skippable)  
**Compliance**: Mandatory for Wave 1+

---

*END OF IN-BETWEEN WAVE RECONCILIATION SPECIFICATION*
