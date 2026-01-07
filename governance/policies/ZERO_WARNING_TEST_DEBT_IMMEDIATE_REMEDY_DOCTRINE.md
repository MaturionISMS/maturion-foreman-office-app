# Zero Warning/Test Debt Immediate Remedy Doctrine

**Version**: 1.0.0  
**Status**: Constitutional Authority  
**Authority**: Derived from governance/policies/zero-test-debt-constitutional-rule.md + governance/contracts/quality-integrity-contract.md  
**Last Updated**: 2026-01-07  
**Source**: Governance Canon Update (PR #887 - maturion-foreman-governance)

---

## I. Constitutional Authority

This doctrine extends and operationalizes the Zero Test Debt Constitutional Rule and Quality Integrity Contract with explicit cross-agent responsibility enforcement.

**Core Principle**: Discovery of prior warning/test debt BLOCKS all downstream work until the responsible agent fixes it.

This rule is absolute, non-negotiable, and enforceable at all build stages.

---

## II. The Immediate Remedy Principle

### A. Definition

**"Immediate Remedy"** means:
1. Discovery of prior warning/test debt triggers IMMEDIATE STOP
2. Downstream work is BLOCKED until issue is resolved
3. Responsible agent is RE-ASSIGNED to fix the issue
4. NO progression occurs until remedy is complete and verified

### B. Scope

This doctrine applies to:
- **Test Debt**: Skipped tests, incomplete tests, test stubs, test TODO/FIXME, failing tests
- **Warnings**: Lint warnings, build warnings, TypeScript warnings, deprecation warnings, console warnings
- **Quality Violations**: Any violation of Quality Integrity Contract standards

---

## III. Discovery and Responsibility Assignment

### A. Discovery Scenarios

**Scenario 1: Builder Discovers Prior Agent's Debt**
```
Wave N Builder discovers Wave N-1 Builder left test debt
    ↓
IMMEDIATE STOP
    ↓
ESCALATE to Foreman
    ↓
Foreman RE-ASSIGNS Wave N-1 Builder
    ↓
Wave N-1 Builder FIXES debt
    ↓
Verify ZERO debt
    ↓
Wave N Builder RESUMES
```

**Scenario 2: QA Builder Discovers Prior Builder's Warnings**
```
QA Builder discovers API Builder left lint warnings
    ↓
IMMEDIATE STOP
    ↓
ESCALATE to Foreman
    ↓
Foreman RE-ASSIGNS API Builder
    ↓
API Builder FIXES warnings
    ↓
Verify ZERO warnings
    ↓
QA Builder RESUMES
```

**Scenario 3: Integration Builder Discovers Multiple Prior Issues**
```
Integration Builder discovers:
- UI Builder: 3 console warnings
- API Builder: 2 skipped tests
- Schema Builder: 1 lint warning
    ↓
IMMEDIATE STOP (all Integration work)
    ↓
ESCALATE to Foreman with complete inventory
    ↓
Foreman RE-ASSIGNS:
  - UI Builder → Fix console warnings
  - API Builder → Fix skipped tests
  - Schema Builder → Fix lint warning
    ↓
ALL fix work COMPLETES
    ↓
Verify ZERO issues across all scopes
    ↓
Integration Builder RESUMES
```

### B. Responsibility Determination

**Who is responsible?**
1. The agent who INTRODUCED the warning/test debt
2. NOT the agent who discovered it
3. Determined by:
   - Git history (which commit/PR introduced it)
   - Agent appointment records
   - Wave/subwave assignment logs
   - Code ownership tracking

**Foreman's Role**:
- Investigate discovery report
- Determine responsible agent
- RE-ASSIGN responsible agent with BLOCKING priority
- HOLD discovering agent in BLOCKED state
- RELEASE discovering agent only after remedy complete

---

## IV. Blocking Protocol (Downstream Work STOPS)

### A. Immediate Actions on Discovery

**Discovering Agent MUST**:
1. STOP all current work immediately
2. Document discovery:
   - What was found (test debt, warnings, etc.)
   - Where it was found (file paths, line numbers)
   - Suspected origin (which prior agent/wave)
   - Impact assessment (how it blocks current work)
3. ESCALATE to Foreman with discovery report
4. Enter BLOCKED state
5. WAIT for remedy completion

**Discovering Agent MUST NOT**:
- Attempt to fix the issue themselves
- Work around the issue
- Continue downstream work
- "Save it for later"
- Suppress or hide the issue

### B. Foreman Response Protocol

**Foreman MUST**:
1. Acknowledge discovery within 1 hour
2. Investigate and assign responsibility within 4 hours
3. RE-ASSIGN responsible agent immediately
4. Create BLOCKING remediation task
5. Halt all dependent work
6. Track remedy progress
7. Verify remedy completion
8. Release discovering agent to resume

**Foreman MUST NOT**:
- Delay investigation
- Assign remedy to discovering agent
- Allow downstream work to continue
- Defer remedy to "later"

### C. Responsible Agent Re-Assignment

**Re-Assignment Characteristics**:
- **Priority**: BLOCKING (highest priority, preempts all other work)
- **Scope**: Fix ONLY the discovered issue (no scope expansion)
- **Timeline**: Immediate execution expected
- **Evidence**: Full remediation evidence required
- **Verification**: Zero-issue confirmation mandatory

**Responsible Agent MUST**:
1. Acknowledge re-assignment immediately
2. STOP current work (if any)
3. Fix discovered issue completely
4. Verify zero warnings/debt in affected scope
5. Provide evidence of remedy
6. Request Foreman verification
7. Wait for release

**Responsible Agent MUST NOT**:
- Claim "not my problem"
- Defer fix to later
- Partial fix or workaround
- Negotiate priority downgrade

---

## V. Verification and Release Protocol

### A. Remedy Verification Requirements

**Foreman MUST verify**:
- ✅ Original issue completely resolved
- ✅ Zero warnings in affected scope
- ✅ Zero test debt in affected scope
- ✅ All Quality Integrity Contract standards met
- ✅ No new issues introduced during fix
- ✅ Build/lint/test all passing
- ✅ Evidence trail complete

**If ANY item not verified → Remedy INCOMPLETE → Responsible agent continues fixing**

### B. Release Procedure

**After Verification**:
1. Foreman declares remedy COMPLETE
2. Foreman updates state: BLOCKED → READY
3. Discovering agent notified to RESUME
4. Discovering agent re-validates (prior issue gone)
5. Discovering agent continues original work

**Evidence Required**:
- Remediation completion report from responsible agent
- Foreman verification checklist (all items checked)
- Test/lint/build output (zero issues)
- Git commit showing fix
- Issue closed in tracking system

---

## VI. Prevention and Early Detection

### A. Pre-Flight Checks (Before Wave Start)

**Foreman MUST execute before authorizing ANY wave**:
1. Scan for accumulated warnings across all modules
2. Scan for accumulated test debt across all test suites
3. Verify zero warnings in baseline
4. Verify zero test debt in baseline
5. Confirm clean slate before wave authorization

**If ANY issues found → BLOCK wave start → Assign remediation → Verify cleanup → THEN authorize wave**

### B. Inter-Wave Reconciliation

**Between waves, Foreman MUST**:
1. Full codebase scan for warnings
2. Full test suite scan for debt
3. Git history review for quality regressions
4. Identify responsible agents for any issues found
5. Require remediation before next wave

**Reference**: `governance/specs/IN_BETWEEN_WAVE_RECONCILIATION_SPEC.md`

### C. Builder Self-Checking Obligation

**Every builder MUST**:
- Run lint checks before claiming complete
- Run full test suite before claiming complete
- Verify zero warnings in own scope
- Verify zero test debt in own scope
- Report any issues discovered (even if prior agent's)

**Builders MUST NOT**:
- Assume "someone else will catch it"
- Hide warnings/debt to avoid blocking
- Claim complete with known issues

---

## VII. Escalation Scenarios

### A. Responsible Agent Unavailable

**If responsible agent cannot be re-assigned**:
1. Foreman escalates to Johan
2. Johan designates replacement agent
3. Replacement agent assigned with BLOCKING priority
4. Process continues as normal

**NOT PERMITTED**: Assigning discovering agent to fix prior agent's debt

### B. Systemic Pattern Detected

**If multiple discoveries indicate systemic issue**:
1. Foreman declares SYSTEMIC QUALITY FAILURE
2. ALL waves/builds HALTED
3. Root cause analysis initiated
4. Governance hardening required
5. Prevention mechanisms implemented
6. Verification of fix across entire codebase
7. Resume only after systemic fix confirmed

**Example**: If 3+ agents discover warnings/debt in same wave → SYSTEMIC

### C. Disagreement on Responsibility

**If responsibility determination disputed**:
1. Foreman reviews git history
2. Foreman reviews agent appointment records
3. Foreman makes binding determination
4. If still unclear → Johan arbitrates
5. Determination is FINAL
6. Responsible agent MUST comply

---

## VIII. Metrics and Reporting

### A. Track These Metrics

**Discovery Metrics**:
- Number of prior-agent issues discovered per wave
- Average time from discovery to escalation
- Average time from escalation to remedy
- Number of re-assignments per wave

**Responsibility Metrics**:
- Issues by responsible agent (who creates most debt?)
- Repeat offenders (agents with multiple re-assignments)
- Remedy completion time by agent

**Impact Metrics**:
- Downstream work blocked (hours)
- Wave delays caused by prior debt
- Cumulative cost of prior-agent remediation

### B. Reporting Requirements

**Every Wave Summary MUST include**:
- Prior-agent issues discovered (count, type, responsible agent)
- Re-assignments issued (agent, reason, remedy time)
- Downstream work blocked (duration, impact)
- Lessons learned
- Prevention measures added

**Continuous Dashboard**:
- Current blocked agents (waiting for prior-agent remedy)
- Open re-assignments (responsible agent fixing)
- Quality debt trend (increasing or decreasing?)

---

## IX. Integration with Existing Governance

### A. Relationship to Zero Test Debt Constitutional Rule

**This doctrine EXTENDS zero-test-debt-constitutional-rule.md by**:
- Adding cross-agent responsibility enforcement
- Adding discovery-triggered blocking protocol
- Adding re-assignment mechanism
- Adding verification and release procedures

**Core rule remains**: Zero test debt is mandatory. This doctrine operationalizes enforcement when debt is discovered after initial agent's completion.

### B. Relationship to Quality Integrity Contract

**This doctrine EXTENDS quality-integrity-contract.md by**:
- Adding immediate remedy requirement
- Adding discovery blocking protocol
- Adding cross-agent responsibility
- Adding re-assignment mechanism

**Core standards remain**: All QIC standards are mandatory. This doctrine operationalizes enforcement when violations are discovered downstream.

### C. Relationship to Agent Constitution

**This doctrine IMPLEMENTS AGENT_CONSTITUTION.md Section VIII by**:
- Defining "Universal Agent Obligations" enforcement mechanism
- Implementing "Escalate When Blocked" procedure
- Enforcing "Zero Test Debt" across agent boundaries

---

## X. Common Objections and Responses

### Objection 1: "This will slow down builds"

**Response**: ❌ REJECTED

**Reality**: 
- Prior debt ALREADY slows builds (forces rework, causes confusion)
- Immediate remedy PREVENTS exponential debt accumulation
- Long-term: Faster builds due to clean codebase
- Prevention is cheaper than accumulated cleanup

### Objection 2: "Discovering agent should just fix it quickly"

**Response**: ❌ REJECTED

**Correct Action**:
- Discovering agent is NOT responsible for prior agent's work
- Fixing prior debt = scope expansion = violates boundaries
- Responsible agent MUST learn from their omissions
- Accountability requires responsibility assignment

### Objection 3: "We'll track it and fix it later"

**Response**: ❌ REJECTED

**Correct Action**:
- "Later" becomes "never"
- Debt accumulates exponentially
- Immediate remedy is MANDATORY
- No deferrals permitted

### Objection 4: "It's just a warning, not a real problem"

**Response**: ❌ REJECTED

**Correct Action**:
- Warnings indicate potential issues
- Zero warnings is constitutional requirement
- Quality Integrity Contract enforces zero warnings
- Fix immediately, always

### Objection 5: "The responsible agent has moved on"

**Response**: ❌ REJECTED

**Correct Action**:
- Re-assignment is MANDATORY
- Responsible agent MUST return to fix
- Accountability follows responsibility
- If unavailable, Johan assigns replacement

---

## XI. Success Criteria

This doctrine is successful when:

1. ✅ **Zero accumulated debt** - No warnings/test debt carried forward between waves
2. ✅ **Immediate discovery response** - All discoveries escalated within 1 hour
3. ✅ **Fast remediation** - 90% of issues resolved within 24 hours
4. ✅ **Accountability enforced** - Responsible agents fix their own issues
5. ✅ **Downstream protection** - No agent works on contaminated baseline
6. ✅ **Prevention working** - Decreasing discovery rate over time
7. ✅ **Clean handovers** - Each agent leaves zero debt for next agent

---

## XII. Version and Authority

**Version**: 1.0.0  
**Status**: Active and Enforced  
**Authority**: Constitutional Authority (Extension of T0-003 + QIC)  
**Precedence**: Enforceable at all build stages, all agent interactions  
**Last Updated**: 2026-01-07  
**Owner**: Johan Ras (MaturionISMS)  
**Enforcer**: Maturion Foreman + All Agents (discovery obligation)

**Source**: Governance Canon Update (PR #887 - maturion-foreman-governance)

**Changelog**:
- 1.0.0 (2026-01-07): Initial doctrine establishing immediate remedy protocol for discovered prior warning/test debt

---

## XIII. Summary: The Commitment

Zero Warning/Test Debt Immediate Remedy Doctrine commits to:

1. ✅ **Discovery Triggers Action** - No ignored discoveries
2. ✅ **Downstream Work Blocks** - No work on contaminated baseline  
3. ✅ **Responsibility Enforced** - Agent who created debt fixes it
4. ✅ **Immediate Remedy Required** - No deferrals permitted
5. ✅ **Verification Mandatory** - No assumption of fix
6. ✅ **Prevention Prioritized** - Early detection and blocking
7. ✅ **Accountability Permanent** - Cannot escape responsibility

**Prior agent debt blocks downstream work.**  
**Responsible agent must fix immediately.**  
**No exceptions. No deferrals. No workarounds.**

---

*END OF ZERO WARNING/TEST DEBT IMMEDIATE REMEDY DOCTRINE*
