# QA-to-Red Test Existence Validation

**Authority:** BL-020 (BOOTSTRAP_EXECUTION_LEARNINGS.md)  
**Purpose:** Prevent FM authorization failures due to missing QA-to-Red tests  
**Status:** ACTIVE

---

## Overview

This validation tool implements the requirements from **BL-020** to prevent FM from authorizing subwaves when QA-to-Red tests are missing or incomplete.

The tool validates:

1. **QA Range Exists** (BL-018): Verifies QA IDs exist in `QA_CATALOG.md`
2. **Semantic Alignment** (BL-019): Shows QA definitions for manual semantic verification
3. **Test File Exists** (BL-020): Verifies test file exists at claimed location in repository
4. **Test Coverage Complete** (BL-020): Verifies all QA numbers have corresponding test functions
5. **Tests Are RED** (BL-020): Verifies tests raise `NotImplementedError` (RED state)

---

## Usage

### Validate from Subwave Specification

```bash
python validate-qa-tests-existence.py --subwave-spec wave2_builder_issues/SUBWAVE_2.5_qa_builder_Advanced_Flow_Scenarios.md
```

This automatically extracts QA range and test file location from the subwave spec.

### Validate Specific QA Range

```bash
python validate-qa-tests-existence.py --qa-range QA-211 QA-225 --test-file tests/wave2_0_qa_infrastructure/test_advanced_flow_scenarios.py
```

### JSON Output for Automation

```bash
python validate-qa-tests-existence.py --qa-range QA-211 QA-225 --test-file tests/wave2_0_qa_infrastructure/test_advanced_flow_scenarios.py --json
```

Output:
```json
{
  "valid": true,
  "qa_range": "QA-211 to QA-225",
  "qa_count": 15,
  "test_file": "tests/wave2_0_qa_infrastructure/test_advanced_flow_scenarios.py",
  "checks": {
    "qa_catalog_exists": {
      "status": "PASS",
      "description": "QA range exists in QA_CATALOG.md (BL-018)",
      "missing": []
    },
    ...
  }
}
```

---

## Exit Codes

- **0**: All validations passed (✅ PASS)
- **1**: One or more validations failed (❌ FAIL)

---

## Integration Points

### FM Pre-Authorization Checklist

Add this step before authorizing any subwave:

```markdown
- [ ] **QA-to-Red Tests Exist**
  - Run: `python validate-qa-tests-existence.py --subwave-spec wave2_builder_issues/SUBWAVE_X.Y_*.md`
  - Status: PASS required
  - Evidence: Validation output attached
```

### CI/CD Pipeline

Add to Wave 2 validation workflow:

```yaml
- name: Validate QA-to-Red Tests
  run: |
    for spec in wave2_builder_issues/SUBWAVE_*.md; do
      python validate-qa-tests-existence.py --subwave-spec "$spec" || exit 1
    done
```

### Subwave Creation Protocol

Before generating subwave sub-issue:

1. Create QA-to-Red test file with all tests in RED state
2. Run validation script to verify completeness
3. Only proceed to sub-issue generation if validation passes

---

## Example Output

### PASS (All Checks Green)

```
================================================================================
QA-to-Red Test Existence Validation (BL-020)
================================================================================

QA Range: QA-211 to QA-225 (15 components)
Test File: tests/wave2_0_qa_infrastructure/test_advanced_flow_scenarios.py

Overall Status: ✅ PASS

Validation Checks:
--------------------------------------------------------------------------------

✅ PASS: QA range exists in QA_CATALOG.md (BL-018)

ℹ️ INFO: QA definitions from catalog (verify semantic alignment manually)
   QA Definitions (verify semantic alignment):
     - QA-211: State persistence across flow
     - QA-212: Evidence generation across flow
     - QA-213: Authorization checks across flow
     - QA-214: Timeout handling in flow
     - QA-215: Flow cancellation
     ... and 10 more

✅ PASS: Test file exists at claimed location (BL-020)

✅ PASS: All QA numbers have corresponding tests (BL-020)

✅ PASS: Tests raise NotImplementedError (RED state)

================================================================================
```

### FAIL (Missing Test File)

```
================================================================================
QA-to-Red Test Existence Validation (BL-020)
================================================================================

QA Range: QA-211 to QA-225 (15 components)
Test File: tests/wave2_0_qa_infrastructure/test_advanced_analytics_phase1_missing.py

Overall Status: ❌ FAIL

Validation Checks:
--------------------------------------------------------------------------------

✅ PASS: QA range exists in QA_CATALOG.md (BL-018)

ℹ️ INFO: QA definitions from catalog (verify semantic alignment manually)
   QA Definitions (verify semantic alignment):
     - QA-211: State persistence across flow
     - QA-212: Evidence generation across flow
     - QA-213: Authorization checks across flow
     - QA-214: Timeout handling in flow
     - QA-215: Flow cancellation
     ... and 10 more

❌ FAIL: Test file exists at claimed location (BL-020)

================================================================================
Exit code: 1
```

---

## Maintenance

**Owner:** Maturion Foreman (FM)  
**Version:** 1.0.0  
**Last Updated:** 2026-01-05

### Future Enhancements

Potential improvements:

1. **Automated Semantic Alignment Check**: Use LLM to verify QA definitions match subwave name/scope
2. **Batch Validation**: Validate all Wave 2 subwaves in single run
3. **GitHub Action**: Create reusable action for PR validation
4. **Evidence Generation**: Automatically generate validation evidence artifacts
5. **Fix Suggestions**: Suggest corrections when validation fails

---

## Related Documentation

- `BOOTSTRAP_EXECUTION_LEARNINGS.md` — BL-018, BL-019, BL-020 learnings
- `QA_CATALOG.md` — Authoritative QA component index
- `WAVE_2_ROLLOUT_PLAN.md` — Wave 2 subwave specifications
- `WAVE_2_IMPLEMENTATION_PLAN.md` — Wave 2 planning basis

---

**END VALIDATION TOOL README**
