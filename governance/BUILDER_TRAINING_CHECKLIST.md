# Builder Training Checklist

**Document**: Builder Training and Policy Acknowledgment Checklist  
**Version**: 1.3 (Updated 2026-01-11)  
**Authority**: CS2 (Johan Ras) + FM  
**Status**: MANDATORY - All Builders  
**Change**: Added BL-026 Automated Deprecation Detection Gate training

---

## Purpose

This checklist ensures all builders are trained on governance policies, understand quality standards, and commit to zero-tolerance enforcement before being assigned work.

**Requirement**: ALL items must be completed before builder receives ANY task assignment.

---

## Pre-Assignment Training Checklist

### A. Core Governance Documents (MANDATORY)

All builders MUST read and acknowledge understanding of:

- [ ] **BUILD_PHILOSOPHY.md** - One-Time Build Correctness principle
- [ ] **governance/policies/governance-supremacy-rule.md** (T0-002) - 99% is 0% rule
- [ ] **governance/policies/zero-test-debt-constitutional-rule.md** (T0-003) - 100% GREEN mandate
- [ ] **governance/zero-debt-campaign/GOVERNANCE_LEARNING_BRIEF.md** - Why warnings are debt

### A2. Constitutional Sandbox Pattern (MANDATORY - NEW 2026-01-09)

All builders MUST understand judgment framework:

- [ ] **Read CONSTITUTIONAL_SANDBOX_PATTERN.md** ([governance repo](https://github.com/APGI-cmy/maturion-foreman-governance/blob/main/governance/canon/CONSTITUTIONAL_SANDBOX_PATTERN.md))
- [ ] **Understand Tier-1 vs Tier-2 distinction** - Constitutional (immutable) vs Procedural (adaptable)
- [ ] **Recognize builder judgment authority** - May adapt procedural guidance within constitutional boundaries
- [ ] **Commit to documenting adaptations** - All judgment/optimization decisions must be documented with rationale

### A3. Automated Deprecation Detection Gate (MANDATORY - NEW 2026-01-11)

All builders writing Python code MUST understand BL-026:

- [ ] **Read AUTOMATED_DEPRECATION_DETECTION_GATE.md** (`governance/policies/AUTOMATED_DEPRECATION_DETECTION_GATE.md`)
- [ ] **Understand deprecated API patterns** - datetime.utcnow(), typing.Dict, typing.List, etc.
- [ ] **Know modern replacements** - datetime.now(timezone.utc), dict[], list[], etc.
- [ ] **Understand auto-fix capability** - Run `ruff check --select UP --fix .` for most fixes
- [ ] **Understand exception process** - Requires FM approval, quarterly review, code comments
- [ ] **Commit to zero deprecated APIs** - All code must pass deprecation gate before merge

### B. Test Dodging Prevention (MANDATORY - NEW 2026-01-08)

All builders MUST complete policy training:

- [ ] **Read POLICY-NO-ONLY-LANGUAGE in full** (`governance/policies/POLICY-NO-ONLY-LANGUAGE.md`)
- [ ] **Study BOOTSTRAP-TEST-DODGING-001 case study** (`bootstrap/learnings/BOOTSTRAP-TEST-DODGING-001.md`)
- [ ] **Pass policy quiz (10/10 required)** - Contact FM for quiz access
- [ ] **Sign acknowledgment of banned language policy** (see Section D below)

### C. Quality Standards (MANDATORY)

All builders MUST understand:

- [ ] **Zero-tolerance policy** - One warning = FAIL, one debt test = FAIL
- [ ] **100% GREEN requirement** - No partial credit, no "close enough"
- [ ] **Test removal governance** - Read `governance/policies/TEST_REMOVAL_GOVERNANCE_GATE_LOCAL.md`
- [ ] **Warning handling doctrine** - Read `governance/policies/ZERO_WARNING_TEST_DEBT_IMMEDIATE_REMEDY_DOCTRINE.md`

### D. Builder Responsibilities (MANDATORY)

All builders MUST commit to:

- [ ] **Write warning-free code** - Fix all warnings before submission
- [ ] **Write complete tests** - All tests GREEN or documented QA-to-Red
- [ ] **Perform code checking** - Review generated code for correctness
- [ ] **Use accurate language** - No minimizing language ("only", "just", "minor")
- [ ] **Immediate remedy** - Fix own warnings/debt immediately when discovered
- [ ] **Honest status reporting** - "100% GREEN" or "NOT READY - X failing"

---

## Builder Policy Acknowledgment

**I, [BUILDER NAME], acknowledge that I have:**

1. ✅ Read all mandatory governance documents listed above
2. ✅ Completed POLICY-NO-ONLY-LANGUAGE training
3. ✅ Studied BOOTSTRAP-TEST-DODGING-001 case study
4. ✅ Passed policy quiz with 10/10 score
5. ✅ Understand the zero-tolerance policy (no warnings, no debt tests)
6. ✅ Understand the 100% GREEN mandate (99% = 0%)
7. ✅ Commit to using accurate, non-minimizing language
8. ✅ Understand Constitutional Sandbox Pattern (BL-024): Tier-1 vs Tier-2
9. ✅ Understand Automated Deprecation Detection Gate (BL-026): Zero deprecated APIs
10. ✅ Understand consequences of policy violations (PR rejection, accountability review)

**I understand that:**

- **Constitutional requirements** (Tier-1) are ABSOLUTE: Zero Test Debt, 100% GREEN, One-Time Build, etc.
- **Procedural guidance** (Tier-2) may be adapted when justified, with documentation
- **Judgment authority** exists within constitutional boundaries
- **Minimizing language** ("only", "just", "minor", "non-blocking") is **BANNED**
- **Status reporting** must be binary: "100% tests passing" OR "NOT READY - X failing"
- **Test dodging** will result in immediate work rejection
- **Policy violations** may result in builder removal from project
- **Zero tolerance** means NO exceptions without CS2 approval

**I commit to:**

- **Never introduce warnings** in my work
- **Fix warnings immediately** if they appear
- **Write complete tests** (GREEN or documented RED)
- **Report status accurately** without minimizing language
- **Maintain 100% GREEN** as mandatory standard
- **Document judgment decisions** when adapting procedural guidance
- **Preserve constitutional requirements** at all times

---

**Builder Signature**: ________________________________  
**Date**: ________________________________  
**Builder ID**: ________________________________  
**FM Witness**: ________________________________  

---

## Policy Quiz (10 Questions - 10/10 Required)

**Contact FM to schedule policy quiz. Must achieve 100% score to pass.**

### Quiz Topics

1. Identify banned minimizing language
2. Rewrite minimizing statements accurately
3. Explain psychological impact of minimizing language
4. Define zero-tolerance policy
5. Describe 100% GREEN mandate
6. Explain governance supremacy rule (99% is 0%)
7. Identify test dodging patterns
8. Describe correct status reporting
9. Explain warning handling doctrine
10. Understand enforcement consequences

**Passing Score**: 10/10 (100%)  
**Retake Policy**: Unlimited attempts, 24-hour wait between attempts  
**Contact**: Foreman (FM) for quiz access

---

## Builder Training Record

**Builder Name**: ________________________________  
**Builder ID**: ________________________________  
**Training Date**: ________________________________  

### Training Completion Status

| Item | Status | Date | FM Verification |
|------|--------|------|-----------------|
| Core Governance Documents | ☐ COMPLETE | _____ | _____ |
| Constitutional Sandbox (BL-024) | ☐ COMPLETE | _____ | _____ |
| POLICY-NO-ONLY-LANGUAGE | ☐ COMPLETE | _____ | _____ |
| BOOTSTRAP-TEST-DODGING-001 | ☐ COMPLETE | _____ | _____ |
| Policy Quiz (10/10) | ☐ COMPLETE | _____ | _____ |
| Signed Acknowledgment | ☐ COMPLETE | _____ | _____ |

**Overall Training Status**: ☐ INCOMPLETE / ☐ COMPLETE

**FM Approval for Task Assignment**: ________________________________  
**Date**: ________________________________

---

## Refresher Training Requirements

### Annual Refresher (MANDATORY)

All builders MUST complete annual refresher training:

- [ ] Re-read all core governance documents
- [ ] Review policy updates from past year
- [ ] Retake policy quiz (10/10 required)
- [ ] Re-sign acknowledgment

**Next Refresher Due**: [DATE + 1 year]

### Triggered Refresher (As Needed)

Refresher training REQUIRED if:

- **Policy violation** detected (minimizing language, test dodging)
- **Major governance update** published
- **Builder reassignment** to new role
- **Incident involvement** (as learning opportunity)

---

## Training Materials Location

**All training materials available at:**

- **Core Governance**: Root directory (`BUILD_PHILOSOPHY.md`, etc.)
- **Policies**: `governance/policies/` directory
- **Bootstrap Learnings**: `bootstrap/learnings/` directory
- **Zero-Debt Campaign**: `governance/zero-debt-campaign/` directory
- **Builder Contracts**: `.github/agents/` directory

**Questions**: Contact Foreman (FM) or Governance Administrator (GA)

---

## Enforcement

### Pre-Assignment Verification

**FM MUST verify completion before task assignment:**

1. ✅ All checklist items completed
2. ✅ Policy quiz passed (10/10)
3. ✅ Acknowledgment signed
4. ✅ Training record documented

**NO exceptions**: Builder cannot receive tasks without complete training.

### Post-Assignment Accountability

**If policy violation detected:**

1. **First Violation**: Work REJECTED, policy re-training required
2. **Second Violation**: Mandatory FM accountability review
3. **Third Violation**: Builder removal consideration

**Violations include:**

- Use of minimizing language in any communication
- Submission of work with warnings
- Submission of work with debt tests
- False completion claims (< 100% GREEN)
- Test dodging patterns

---

## Builder Types and Training Scope

### All Builders (Universal Training)

**Applies to:**
- UI Builder
- API Builder
- Schema Builder
- Integration Builder
- QA Builder

**Scope**: ALL sections of this checklist (no exceptions)

### Specialized Training (Role-Specific)

**Additional training may be required based on role:**

- **QA Builder**: Advanced QA governance training
- **Schema Builder**: Data integrity and migration training
- **Integration Builder**: External system compliance training

**Contact FM** for role-specific training requirements.

---

## Document Status

**Status**: ACTIVE - Mandatory for All Builders  
**Authority**: CS2 (Johan Ras) + FM  
**Maintenance**: Updated as policies evolve  
**Version**: 1.1 (2026-01-08)

**Recent Updates**:
- **2026-01-09**: Added Constitutional Sandbox Pattern (BL-024) training requirement
- **2026-01-08**: Added POLICY-NO-ONLY-LANGUAGE training requirement
- **2026-01-08**: Added BOOTSTRAP-TEST-DODGING-001 case study requirement
- **2026-01-08**: Enhanced acknowledgment section with banned language

---

## Summary

**Before ANY task assignment, ALL builders MUST:**

1. ✅ Read mandatory governance documents
2. ✅ Complete Constitutional Sandbox Pattern (BL-024) training
3. ✅ Complete POLICY-NO-ONLY-LANGUAGE training
4. ✅ Study BOOTSTRAP-TEST-DODGING-001 case study
5. ✅ Pass policy quiz (10/10)
6. ✅ Sign policy acknowledgment
7. ✅ Receive FM verification

**Zero exceptions. Zero tolerance. 100% compliance required.**

---

**Questions or Training Requests**: Contact Foreman (FM)

---

**END OF BUILDER TRAINING CHECKLIST**
