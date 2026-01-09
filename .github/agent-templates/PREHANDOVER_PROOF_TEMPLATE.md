# PREHANDOVER PROOF TEMPLATE

**Purpose:** Standardized template for documenting local PR-gate execution before handover  
**Required For:** ALL handovers (no exceptions)  
**Authority:** Governance Rule — PR_GATE_LOCAL_EXECUTION_REQUIREMENT.md

---

## Instructions

1. Copy this template to create your PREHANDOVER_PROOF document
2. Fill in ALL sections completely
3. Execute ALL PR-gate workflows locally
4. Document results for EACH gate
5. Provide explicit attestation
6. Include this proof in PR before marking Ready for Review

**Incomplete proofs will result in handover rejection.**

---

## PREHANDOVER PROOF — [PR Number] — [Brief Description]

**Agent:** [Your Agent Name]  
**PR:** #[Number]  
**Branch:** [branch-name]  
**Date:** [YYYY-MM-DD]  
**Latest Commit:** [commit-hash]

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
