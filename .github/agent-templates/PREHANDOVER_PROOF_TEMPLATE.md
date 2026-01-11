# PREHANDOVER PROOF TEMPLATE

**Purpose:** Standardized template for documenting local PR-gate execution before handover  
**Required For:** ALL handovers (no exceptions)  
**Authority:** Governance Rule — PR_GATE_LOCAL_EXECUTION_REQUIREMENT.md  
**Protocol Version:** 2.0.0+ (Execution Bootstrap Protocol)

---

## Instructions

1. Copy this template to create your PREHANDOVER_PROOF document
2. Fill in ALL sections completely
3. Execute **Category 0: 7-Step Execution Bootstrap Protocol** (MANDATORY)
4. Execute ALL PR-gate workflows locally
5. Document results for EACH step and gate
6. Provide explicit attestation
7. Include this proof in PR before marking Ready for Review

**Incomplete proofs will result in handover rejection.**

---

## PREHANDOVER PROOF — [PR Number] — [Brief Description]

**Agent:** [Your Agent Name]  
**PR:** #[Number]  
**Branch:** [branch-name]  
**Date:** [YYYY-MM-DD]  
**Latest Commit:** [commit-hash]  
**Protocol Version:** 2.0.0+

---

## Category 0: Execution Bootstrap Protocol (MANDATORY v2.0.0+)

**Status**: [COMPLETE | INCOMPLETE]  
**All Steps GREEN**: [YES | NO]

### Step 1: Identify Execution Artifacts

**Artifacts Created/Modified:**
- [ ] Workflow: [path/to/workflow.yml]
- [ ] Script: [path/to/script.py]
- [ ] Gate: [path/to/gate-config]
- [ ] Other: [describe]

**Total Artifacts**: [N]

### Step 2: Local Execution

**Execution Environment:**
- Agent: [Agent Name]
- Environment: [Local/Container/VM]
- OS: [Operating System]
- Tools: [List relevant tools/versions]

**Execution Log:**
```bash
$ [command executed]

[PASTE COMPLETE OUTPUT HERE]
```

### Step 3: Validate Exit Codes

**Exit Code Validation:**
- [ ] All exit codes = 0 (SUCCESS)
- [ ] No warnings detected
- [ ] No errors detected

**Exit Codes by Artifact:**
| Artifact | Exit Code | Status |
|----------|-----------|--------|
| [Artifact 1] | 0 | ✅ PASS |
| [Artifact 2] | 0 | ✅ PASS |

### Step 4: Evidence Collection

**Evidence Files:**
- Execution logs: [path or attached]
- Output files: [path or attached]
- Screenshots: [path or attached]
- Error logs (if any): [N/A or path]

**Evidence Summary:**
[Brief description of evidence collected]

### Step 5: Failure Remediation

**Failures Detected**: [YES | NO]

**If YES, document remediation:**
- **Failure 1**: [Description]
  - Root Cause: [Cause]
  - Fix Applied: [Fix description]
  - Re-execution Result: [PASS/FAIL]
  - Commit: [commit-hash]

**If NO**: All executions passed on first attempt.

### Step 6: Green Attestation

**I attest that:**
- [x] All execution artifacts identified
- [x] All artifacts executed locally
- [x] All exit codes = 0 (success)
- [x] All evidence collected and linked
- [x] Any failures were fixed and re-tested
- [x] **ALL CHECKS GREEN on commit [commit-hash]**

### Step 7: Handover Authorization

**Authorization Statement:**

> "I, [Agent Name], authorize handover for PR #[Number]. All execution artifacts have been locally verified with GREEN status on commit [commit-hash]. All 7 steps of the Execution Bootstrap Protocol have been completed successfully. Evidence is documented above."

**Handover Status**: ✅ AUTHORIZED

**Hard Rule Compliance**: CI is confirmation only, NOT diagnostic. All failures discovered and fixed locally before handover.

---

## Local PR-Gate Execution Evidence

### Gate 1: Agent QA Boundary Enforcement

**Workflow:** `.github/workflows/agent-boundary-gate.yml`  
**Script:** `governance/scripts/validate_agent_boundaries.py`

**Local Execution:**
```bash
$ python3 governance/scripts/validate_agent_boundaries.py --reports "." --current-repo "MaturionISMS/maturion-foreman-office-app"

[PASTE OUTPUT HERE]
```

**Exit Code:** [0 for pass]  
**Result:** ✅ PASS / ❌ FAIL

---

### Gate 2: Build-to-Green Enforcement

**Workflow:** `.github/workflows/build-to-green-enforcement.yml`  
**Script:** `foreman/scripts/detect-test-debt.py`

**Local Execution:**
```bash
$ python3 foreman/scripts/detect-test-debt.py --test-dir tests

[PASTE OUTPUT HERE]
```

**Exit Code:** [0 for pass]  
**Result:** ✅ PASS / ❌ FAIL

---

[Continue for all applicable gates...]

---

## Agent Attestation

I, **[Agent Name]**, attest that:

- [x] All applicable PR-gate workflows were executed locally
- [x] All gates returned GREEN (exit code 0)
- [x] All logs were inspected
- [x] This evidence is accurate and complete
- [x] Constitutional compliance verified (BL-024): All Tier-1 requirements preserved
- [x] If procedural guidance adapted: Adaptations documented with justification

**Handover is authorized based on local verification.**

**Signature:** [Agent Name]  
**Date:** [YYYY-MM-DD]  
**Commit:** [commit-hash]

---

*END OF PREHANDOVER PROOF*
