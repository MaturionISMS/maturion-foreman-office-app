# Governance Supremacy Rule (GSR)

**Version**: 1.0.0  
**Status**: Constitutional Authority  
**Authority**: Build Philosophy + Foreman Constitutional Authority  
**Last Updated**: 2025-12-15

---

## I. Principle

**Governance rules override ALL other considerations.**

No "good enough" compromises.  
No "we'll fix it later" deferrals.  
No "context-dependent" exceptions.  

**Rules are absolute.**

---

## II. The Four Pillars of Governance Supremacy

### Pillar 1: 100% QA Passing is ABSOLUTE

**Rule**: ALL tests must pass. No exceptions.

**What This Means**:
- ✅ 100% passing = PASS
- ❌ 99% passing = TOTAL FAILURE
- ❌ 301/303 tests = TOTAL FAILURE
- ❌ ANY test failure = BUILD BLOCKED

**No Context-Dependent Passes**:
- ❌ "The failing test is minor" → REJECTED
- ❌ "We'll fix it in the next PR" → REJECTED
- ❌ "It's just a flaky test" → REJECTED
- ❌ "The feature works, test is wrong" → REJECTED

**Action on Failure**:
1. STOP build immediately
2. Do NOT merge
3. Do NOT accept partial completion
4. Fix ALL failures
5. Re-run full suite
6. Verify 100% pass
7. THEN continue

**Enforcement**: Automated blocking in CI/CD + Foreman validation

---

### Pillar 2: Zero Test Debt is MANDATORY

**Rule**: No test debt of any kind is permitted.

**Forms of Test Debt (ALL FORBIDDEN)**:
- ❌ Skipped tests (`.skip()`, `.todo()`, `.only()` left in)
- ❌ Commented out tests
- ❌ Incomplete tests (stubs with no assertions)
- ❌ Tests marked "TODO" or "FIXME"
- ❌ Incomplete test infrastructure (stub helpers, broken mocks)
- ❌ Hidden test debt (suppressed errors, excluded tests)
- ❌ Failing tests carried forward

**Action on Detection**:
```
TEST DEBT DETECTED
    ↓
STOP EXECUTION
    ↓
FIX ALL DEBT
    ↓
RE-RUN QA
    ↓
VERIFY ZERO DEBT
    ↓
CONTINUE (only if zero debt)
```

**No Deferrals**:
- ❌ "We'll finish the test later" → REJECTED
- ❌ "Let's skip this for now" → REJECTED
- ❌ "This test is hard, we'll come back" → REJECTED

**Enforcement**: Pre-merge validation + Foreman QA-of-QA

---

### Pillar 3: Architecture Conformance is REQUIRED

**Rule**: Code must match architecture exactly. No deviations without CS2 approval.

**What This Means**:
- ✅ Architecture says X → Implement X exactly
- ❌ Architecture says X → Implement X+ → REJECTED
- ❌ Architecture says X → Implement Y (better idea) → REJECTED
- ❌ Architecture is silent → Guess what to do → REJECTED

**No "Interpretation"**:
- When architecture is unclear → ESCALATE to Foreman
- When architecture conflicts with QA → ESCALATE to Foreman
- When architecture is incomplete → ESCALATE to Foreman
- Do NOT proceed with uncertainty

**No "Improvements"**:
- ❌ "I have a better way" → REJECTED (unless CS2 approved)
- ❌ "Let me optimize this" → REJECTED (unless CS2 approved)
- ❌ "Let me add this nice feature" → REJECTED (unless in architecture)

**CS2 (Change Sequence 2) Approval Required For**:
- Breaking interface changes
- Module boundary modifications
- Integration contract changes
- Protected path modifications

**Action on Deviation**:
1. STOP implementation
2. Document the deviation
3. Escalate to Foreman
4. WAIT for CS2 approval or architecture update
5. Do NOT proceed without approval

**Enforcement**: Architecture validation checklist + Foreman review

---

### Pillar 4: Constitutional File Protection

**Rule**: Protected paths MUST NEVER be modified by builders.

**Protected Paths**:
```
.github/workflows/                           # CI/CD workflows
.github/foreman/agent-contract.md            # Foreman constitution
.github/agents/foreman.agent.md              # Foreman agent definition
BUILD_PHILOSOPHY.md                          # Build Philosophy
foreman/constitution/                        # Constitutional documents
foreman/architecture-design-checklist.md     # Architecture checklist
foreman/builder-specs/build-to-green-rule.md # Builder protocol
foreman/governance/                          # Governance rules
docs/governance/                             # Governance documentation
maturion/philosophy-tree.md                  # Platform ontology (if exists)
```

**Action on Attempted Modification**:
1. **HALT** immediately
2. Return `GovernanceViolation` error
3. Log incident to governance memory
4. Escalate to Foreman
5. Do NOT modify the file
6. Do NOT proceed with task

**Error Response**:
```json
{
  "success": false,
  "error": "GovernanceViolation",
  "message": "Cannot modify protected path",
  "details": {
    "attempted_path": "<path that was attempted>",
    "reason": "This path is constitutionally protected",
    "requires": "CS2 Architecture Approval Workflow",
    "action": "Escalate to Foreman for architectural decision"
  },
  "timestamp": "<ISO 8601 timestamp>"
}
```

**CS2 Required**: Any modification requires explicit CS2 approval workflow with Owner (Johan) involvement.

**Enforcement**: File system checks + Builder contract validation

---

## III. Governance Violation Response Protocol

### When Violation is Detected

**Immediate Actions**:
1. **STOP** all execution immediately
2. **LOG** violation to governance memory
3. **CREATE** incident report
4. **ESCALATE** to Foreman
5. **WAIT** for resolution
6. **DO NOT** proceed until resolved

### Violation Types

#### Type 1: QA Failure (Partial Pass)
- **Severity**: High
- **Action**: Block merge, fix all failures, re-run
- **Resolution**: 100% pass required

#### Type 2: Test Debt Detected
- **Severity**: High
- **Action**: Stop build, fix all debt, verify zero debt
- **Resolution**: Zero debt verification required

#### Type 3: Architecture Deviation
- **Severity**: Critical
- **Action**: Stop build, escalate to Foreman, await CS2 approval
- **Resolution**: Architecture update OR implementation correction

#### Type 4: Protected Path Modification
- **Severity**: Critical
- **Action**: Halt immediately, escalate, require CS2 approval
- **Resolution**: CS2 approval + Owner review

### Incident Report Format

```markdown
# Governance Violation Incident Report

## Incident ID
<unique-incident-id>

## Violation Type
<qa_failure | test_debt | architecture_deviation | protected_path>

## Severity
<high | critical>

## Timestamp
<ISO 8601 timestamp>

## Description
<Clear description of what was violated and how>

## Detected By
<agent-id | human | automated-check>

## Impact Assessment
<What is the impact of this violation?>

## Remediation Required
<What must be done to resolve this?>

## Status
<open | in_progress | resolved>

## Resolution
<How was this resolved? (if resolved)>

## Prevention
<What can prevent this in the future?>
```

---

## IV. Enforcement Mechanisms

### Level 1: Automated Enforcement

**Automated Checks (Run Continuously)**:
- CI/CD test validation (100% pass required)
- Lint validation (zero errors, zero warnings)
- TypeScript compilation (must succeed)
- Build validation (must succeed)
- File path protection (prevent protected path modifications)
- Test debt detection (scan for .skip(), .todo(), etc.)

**Action on Failure**: Block merge, notify Foreman, log incident

### Level 2: Foreman Enforcement

**Foreman Validation (Before Merge)**:
- Architecture conformance validation
- QA coverage validation
- QA-of-QA validation
- Integration integrity validation
- Evidence trail validation
- Governance compliance validation

**Action on Failure**: Reject PR, request corrections, log incident

### Level 3: Human Oversight

**Human Validation (Final Gate)**:
- Owner (Johan) final approval
- Domain expert review (if required)
- Security review (if required)
- Compliance review (if required)

**Action on Failure**: Reject merge, request architectural review

---

## V. Appeals and Overrides

### Standard Appeals

**Not Permitted**:
- ❌ Appeal to bypass 100% QA pass
- ❌ Appeal to accept test debt
- ❌ Appeal to deviate from architecture without CS2
- ❌ Appeal to modify protected paths without CS2

**These rules are absolute. No appeals accepted.**

### Owner Override (Johan Only)

**Johan may temporarily override GSR for**:
- Emergency production fixes
- Critical security patches
- Time-critical situations

**Override Characteristics**:
- Temporary (applies to specific instance only)
- Explicit (must be clearly stated)
- Automatic reversion (rules return after override)
- Documented (logged in evidence trail)

**Post-Override**:
- Rules return to full enforcement
- Standard governance resumes
- Technical debt created must be resolved in follow-up

---

## VI. Integration with Build Philosophy

GSR is a direct implementation of Build Philosophy Principle #4: **Governance Supremacy**

**Hierarchy**:
```
BUILD_PHILOSOPHY.md (Supreme Authority)
    ↓
governance-supremacy-rule.md (This Document)
    ↓
Specific Governance Documents (GSR Implementation)
```

**GSR Implements**:
- One-Time Build Correctness (via 100% QA pass)
- Zero Regression (via comprehensive QA + architecture conformance)
- Full Architectural Alignment (via architecture conformance rule)
- Zero Ambiguity (via explicit, testable rules)

---

## VII. Compliance and Auditability

### Audit Trail Requirements

All GSR enforcement must be auditable:
- ✅ All violations logged to governance memory
- ✅ All incident reports preserved
- ✅ All resolutions documented
- ✅ All overrides logged with rationale

### Compliance Reporting

GSR status must be reported in:
- Build completion reports
- Module readiness reports
- Governance dashboards
- Compliance audit reports

### Metrics Tracked

- Number of governance violations per build wave
- Types of violations (by category)
- Resolution time per violation
- Repeat violations (patterns)
- Override frequency and justification

---

## VIII. Version and Authority

**Version**: 1.0.0  
**Status**: Active and Enforced  
**Authority**: Constitutional Authority (Build Philosophy Implementation)  
**Precedence**: Second only to BUILD_PHILOSOPHY.md and Owner Override  
**Last Updated**: 2025-12-15  
**Owner**: Johan (MaturionISMS)  
**Enforcer**: Maturion Foreman

**Changelog**:
- 1.0.0 (2025-12-15): Initial Governance Supremacy Rule

---

## IX. Summary: The Commitment

GSR commits to:

1. ✅ **100% QA Passing** - No partial passes, ever
2. ✅ **Zero Test Debt** - No deferrals, no exceptions
3. ✅ **Architecture Conformance** - No deviations without approval
4. ✅ **Constitutional Protection** - Protected paths are sacred

**Governance is not negotiable.**  
**Rules are absolute.**  
**Quality is mandatory.**

---

*END OF GOVERNANCE SUPREMACY RULE*
