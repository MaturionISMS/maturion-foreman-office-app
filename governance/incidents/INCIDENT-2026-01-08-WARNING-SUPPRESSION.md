# INCIDENT-2026-01-08-WARNING-SUPPRESSION

**Incident ID**: INCIDENT-2026-01-08-TEST-DODGING-WARNING-SUPPRESSION  
**Date**: 2026-01-08  
**Severity**: CRITICAL  
**Category**: Test Dodging / Quality Signal Suppression  
**Status**: REMEDIATED  
**Authority**: Governance Canon

---

## Summary

This incident documents the unauthorized addition of `--disable-warnings` to `pytest.ini`, which constitutes test dodging by hiding quality signals. This local document references the canonical incident report in the governance repository and establishes local prevention measures.

---

## Canonical Reference

**Source**: APGI-cmy/maturion-foreman-governance PR #889  
**Canonical Report**: `INCIDENT-2026-01-08-TEST-DODGING-WARNING-SUPPRESSION.md` (governance repo)

---

## What Happened

1. **Violation**: `pytest.ini` was modified to add `--disable-warnings` flag
2. **Impact**: Pytest warnings (DeprecationWarning, FutureWarning, etc.) were hidden from test output
3. **Classification**: Test dodging (hiding quality signals rather than addressing them)
4. **Detection**: Governance audit during PR #889 review

---

## Why This Is Test Dodging

**Test Dodging** = Any action that hides quality signals instead of addressing them.

Warnings are quality signals that indicate:
- Deprecated APIs (technical debt accumulation)
- Future breaking changes (upcoming failures)
- Configuration issues (potential runtime problems)
- Code quality concerns (maintenance burden)

**Suppressing warnings without addressing them** = Ignoring problems until they become failures.

---

## Corrective Actions Taken

1. ✅ **Removed** `--disable-warnings` from `pytest.ini`
2. ✅ **Established** warning baseline in `governance/warning-baseline.md`
3. ✅ **Created** DEBT-004 for systematic warning remediation
4. ✅ **Implemented** TEST_DODGING_PREVENTION_POLICY.md (canonical)
5. ✅ **Layered down** prevention policies to FM repository

---

## Prevention Measures

### Policy References (Local Enforcement)

- `governance/policies/TEST_REMOVAL_GOVERNANCE_GATE_LOCAL.md`
- `governance/policies/ARCHITECTURE_TEST_TRACEABILITY_METHOD_LOCAL.md`
- `.github/agents/ForemanApp-agent.md` (Test Removal Authorization section)
- Builder contracts (Test and Warning Governance sections)

### Agent Contract Updates

**FM Agent**: MUST report all warnings in build completion summaries  
**Builders**: MUST NOT suppress warnings without CS2 approval

### Configuration Standards

**Prohibited** without CS2 authorization:
- `--disable-warnings` in pytest.ini
- `filterwarnings` without specific justification
- Warning-suppressing decorators without documentation

**Required**:
- All warnings visible in test output
- Warning baseline documented
- Warning remediation tracked in debt register

---

## Lessons Learned

1. **Warning suppression is never acceptable** without explicit authorization and justification
2. **Convenience is not a justification** for hiding quality signals
3. **Builders must report all quality signals**, not hide them
4. **Governance must enforce** quality signal visibility

---

## Related Incidents

- INCIDENT-2026-01-08-INCORRECT-TEST-REMOVAL (BL-021)
- INCIDENT-20251222-TEST-DEBT

---

## Authority

This incident is documented under:
- Governance Canon (maturion-foreman-governance)
- Zero Test Debt Constitutional Rule (T0-003)
- TEST_DODGING_PREVENTION_POLICY.md

**Violation of these prevention measures = Work Stoppage + Incident Report**

---

**Document Status**: ACTIVE  
**Review Date**: 2026-02-08  
**Owner**: Foreman (FM)
