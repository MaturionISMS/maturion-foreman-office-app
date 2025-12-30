# PR-Gate Failure Response Guide

**Purpose**: Deterministic failure classification and local resolution for builders

**Constitutional Authority**:
- `governance/alignment/PR_GATE_FAILURE_HANDLING_PROTOCOL.md` (Canonical)
- `governance/build/PR_GATE_RELEASE_CHECKS_SYSTEM_SPEC.md`

**Version**: 1.0.0  
**Date**: 2025-12-30

---

## Critical Principle: Local Detection BEFORE PR Submission

**You MUST be able to detect and resolve ALL failure categories locally BEFORE submitting PR.**

CI confirms what you already know. CI does NOT discover issues for you.

If CI fails, you either:
1. Submitted PR prematurely (most common)
2. Encountered gate infrastructure issue (rare)

---

## Failure Category Reference

### Category 1: ARTIFACT_MISSING

**Definition**: Required artifact not present in PR

**Local Detection Method**:
```bash
# Check for required artifacts before PR
ls -la foreman/evidence/builder-qa-report.json
ls -la foreman/evidence/*.json
```

**Local Verification Command**:
```bash
# Verify all required artifacts exist
python governance/scripts/validate-builder-artifacts.py --check-presence
```

**Resolution Steps**:
1. Identify which artifact is missing (check error message)
2. Generate the missing artifact using appropriate tool
3. Verify artifact exists at expected location
4. Re-run local validation
5. Only then submit PR

**Re-verification**:
```bash
# Confirm all artifacts present
python governance/scripts/validate-builder-artifacts.py --check-presence
# Should output: All required artifacts present
```

**CI Confirmation Output** (confirmatory only):
```
✅ Artifact Presence Check: PASS
   - Builder QA Report: FOUND
   - Evidence artifacts: FOUND (3 files)
```

**Severity**: HIGH (blocks merge)

---

### Category 2: SCHEMA_VIOLATION

**Definition**: Artifact present but schema non-compliant

**Local Detection Method**:
```bash
# Validate artifact schemas locally
python -c "
import json
import jsonschema

with open('foreman/builder/templates/builder-qa-report-schema.json') as schema_file:
    schema = json.load(schema_file)

with open('foreman/evidence/builder-qa-report.json') as report_file:
    report = json.load(report_file)

try:
    jsonschema.validate(report, schema)
    print('✅ Schema valid')
except jsonschema.ValidationError as e:
    print(f'❌ Schema violation: {e.message}')
"
```

**Local Verification Command**:
```bash
# Validate all artifact schemas
python governance/scripts/validate-builder-artifacts.py --check-schemas
```

**Resolution Steps**:
1. Identify which field violated schema (check error message)
2. Review schema requirements: `foreman/builder/templates/builder-qa-report-schema.json`
3. Fix the violating field in your artifact
4. Re-run schema validation locally
5. Only then submit PR

**Common Schema Violations**:
- Missing required field (add the field)
- Wrong field type (e.g., string instead of integer)
- Invalid enum value (use allowed value from schema)
- Extra fields not in schema (remove or check `additionalProperties`)

**Re-verification**:
```bash
python governance/scripts/validate-builder-artifacts.py --check-schemas
# Should output: All artifacts schema-compliant
```

**CI Confirmation Output** (confirmatory only):
```
✅ Schema Validation: PASS
   - Builder QA Report: VALID
   - Evidence artifacts: VALID (3 files)
```

**Severity**: HIGH (blocks merge)

---

### Category 3: IMMUTABILITY_VIOLATION

**Definition**: Artifact modified after generation (integrity violation)

**Local Detection Method**:
```bash
# Check immutability flag in artifacts
grep '"immutable"' foreman/evidence/builder-qa-report.json
# Should show: "immutable": true
```

**Local Verification Command**:
```bash
# Verify immutability flags
python governance/scripts/validate-builder-artifacts.py --check-immutability
```

**Resolution Steps**:
1. **NEVER modify evidence after generation** - This is the root cause
2. If you need to change evidence, regenerate it (don't edit)
3. Ensure `immutable: true` is set when generating evidence
4. Verify timestamps are not manually changed
5. Only then submit PR

**Re-verification**:
```bash
python governance/scripts/validate-builder-artifacts.py --check-immutability
# Should output: All artifacts properly marked immutable
```

**CI Confirmation Output** (confirmatory only):
```
✅ Immutability Check: PASS
   - All artifacts marked immutable: true
   - No timestamp inconsistencies detected
```

**Severity**: CRITICAL (integrity violation) - **Escalate to Foreman if detected**

---

### Category 4: AGENT_BOUNDARY_VIOLATION

**Definition**: Agent executed QA outside its scope

**Local Detection Method**:
```bash
# Check agent ID in Builder QA Report
grep '"agent_id"' foreman/evidence/builder-qa-report.json
# Should match YOUR builder agent (e.g., "ui-builder" for UI work)

# Verify using checklist
cat foreman/builder/templates/agent-boundary-checklist.md
# Work through checklist before PR
```

**Local Verification Command**:
```bash
# Validate agent boundaries
python governance/scripts/validate_agent_boundaries.py
```

**Resolution Steps**:
1. Review `foreman/builder/templates/agent-boundary-checklist.md`
2. Identify which QA was executed by wrong agent
3. Remove QA executed by wrong agent
4. Re-run QA with correct agent
5. Update Builder QA Report with correct agent_id
6. Only then submit PR

**Common Violations**:
- UI builder ran API QA (should be api-builder)
- Builder ran governance QA (should be governance agent)
- Builder ran FM QA (should be FM agent)
- Agent ID missing or incorrect in report

**Re-verification**:
```bash
python governance/scripts/validate_agent_boundaries.py
# Should output: All agent boundaries respected
```

**CI Confirmation Output** (confirmatory only):
```
✅ Agent Boundary Check: PASS
   - Builder QA executed by: ui-builder
   - No cross-agent QA detected
   - Agent attribution correct
```

**Severity**: CATASTROPHIC - **ESCALATE IMMEDIATELY to Foreman if detected**

---

### Category 5: NOT_READY_DECLARATION

**Definition**: Builder explicitly declares NOT_READY status

**Local Detection Method**:
```bash
# Check QA status in Builder QA Report
grep '"qa_status"' foreman/evidence/builder-qa-report.json
# Should show: "qa_status": "READY"
```

**Local Verification Command**:
```bash
# Check readiness status
python -c "
import json
with open('foreman/evidence/builder-qa-report.json') as f:
    report = json.load(f)
    status = report.get('qa_status')
    if status == 'READY':
        print('✅ READY for PR')
    else:
        print(f'❌ NOT READY: {status}')
"
```

**Resolution Steps**:
1. **Do NOT submit PR with NOT_READY status** - This is intentional blocking
2. Identify why status is NOT_READY (check test failures, incomplete work)
3. Complete all required work
4. Verify all QA-to-Red tests pass
5. Update Builder QA Report to `qa_status: READY`
6. Only then submit PR

**Why NOT_READY?** Common reasons:
- Some QA-to-Red tests still failing
- Implementation incomplete
- Evidence chain incomplete
- Known issues not yet resolved

**Re-verification**:
```bash
# Verify READY status
grep '"qa_status"' foreman/evidence/builder-qa-report.json | grep READY
# Should output: "qa_status": "READY"
```

**CI Confirmation Output** (confirmatory only):
```
✅ Readiness Check: PASS
   - Builder QA status: READY
   - All QA-to-Red tests: PASS
```

**Severity**: HIGH (blocks merge, but expected workflow)

---

### Category 6: ARCHITECTURE_INCOMPLETE

**Definition**: Architecture declares completeness < 100% or drift present

**Local Detection Method**:
```bash
# Check architecture completeness (if applicable to your task)
# This is typically FM responsibility, but builders should be aware
```

**Local Verification Command**:
```bash
# Verify architecture alignment (for your specific task)
python governance/scripts/validate-architecture-alignment.py --task-id <your-task-id>
```

**Resolution Steps**:
1. Review architecture specification for your task
2. Verify all required architecture components implemented
3. Check for architectural drift (deviations from spec)
4. Implement missing components or fix drift
5. Re-run architecture validation
6. Only then submit PR

**Builder Responsibility**:
- Implement architecture as specified (no deviation)
- Report architecture completion for your task
- Do NOT implement architecture not in your task scope

**Re-verification**:
```bash
python governance/scripts/validate-architecture-alignment.py --task-id <your-task-id>
# Should output: Architecture alignment: COMPLIANT
```

**CI Confirmation Output** (confirmatory only):
```
✅ Architecture Alignment: PASS
   - Task architecture: COMPLETE
   - Drift detected: NONE
```

**Severity**: HIGH (blocks merge)

---

### Category 7: TEST_DEBT_DETECTED

**Definition**: Test dodging patterns or DP-RED violations detected

**Local Detection Method**:
```bash
# Search for test dodging patterns
grep -r "\.skip()" tests/
grep -r "\.only()" tests/
grep -r "\.todo()" tests/
grep -r "// TODO:" tests/ | grep -i test

# Check for commented out tests
grep -r "// it(" tests/
grep -r "// describe(" tests/
```

**Local Verification Command**:
```bash
# Verify zero test debt
python governance/scripts/validate-test-debt.py
```

**Resolution Steps**:
1. **Remove ALL test dodging patterns** - Zero test debt is constitutional
2. Implement all skipped tests
3. Remove `.only()` (run all tests, not just one)
4. Convert `.todo()` to actual test implementation
5. Uncomment all commented tests (or remove if truly unnecessary)
6. Re-run all tests → all should pass
7. Only then submit PR

**Test Dodging Patterns to Remove**:
- `.skip()` - DO NOT skip tests, implement them
- `.only()` - DO NOT run only one test, run all
- `.todo()` - DO NOT defer tests, implement them
- Commented tests - DO NOT comment, implement or remove

**Re-verification**:
```bash
python governance/scripts/validate-test-debt.py
# Should output: Zero test debt detected
```

**CI Confirmation Output** (confirmatory only):
```
✅ Test Debt Check: PASS
   - No .skip() detected
   - No .only() detected
   - No .todo() detected
   - All tests implemented
```

**Severity**: HIGH (constitutional violation)

---

### Category 8: GOVERNANCE_INVARIANT_VIOLATED

**Definition**: Governance rule or invariant broken

**Local Detection Method**:
```bash
# Validate governance compliance
python governance/scripts/governance-gate.py --validate
```

**Local Verification Command**:
```bash
# Check all governance invariants
python governance/scripts/validate-governance-compliance.py
```

**Resolution Steps**:
1. Identify which governance rule was violated (check error message)
2. Review canonical governance documentation
3. Fix the violation (comply with governance)
4. Re-run governance validation
5. Only then submit PR

**Common Governance Violations**:
- Mandatory field missing in governance artifact
- Policy not followed (e.g., naming conventions)
- Compliance control not satisfied
- Constitutional rule violated

**Re-verification**:
```bash
python governance/scripts/validate-governance-compliance.py
# Should output: All governance invariants satisfied
```

**CI Confirmation Output** (confirmatory only):
```
✅ Governance Compliance: PASS
   - All invariants satisfied
   - Compliance controls: MET
```

**Severity**: HIGH (governance violation)

---

### Category 9: TRACEABILITY_BROKEN

**Definition**: Evidence chain incomplete or parent references missing

**Local Detection Method**:
```bash
# Check evidence chain in Builder QA Report
grep '"evidence_chain"' foreman/evidence/builder-qa-report.json

# Verify all referenced evidence exists
python -c "
import json
with open('foreman/evidence/builder-qa-report.json') as f:
    report = json.load(f)
    for evidence_path in report.get('evidence_chain', []):
        import os
        if os.path.exists(evidence_path):
            print(f'✅ {evidence_path}')
        else:
            print(f'❌ MISSING: {evidence_path}')
"
```

**Local Verification Command**:
```bash
# Validate evidence chain completeness
python governance/scripts/validate-evidence-chain.py
```

**Resolution Steps**:
1. Identify missing evidence in chain
2. Generate missing evidence artifacts
3. Update evidence_chain array in Builder QA Report
4. Verify all evidence paths are correct and exist
5. Re-run traceability validation
6. Only then submit PR

**Evidence Chain Requirements**:
- All evidence artifacts referenced must exist
- Evidence chain must be chronologically consistent
- Parent references must be valid
- No gaps in traceability

**Re-verification**:
```bash
python governance/scripts/validate-evidence-chain.py
# Should output: Evidence chain complete
```

**CI Confirmation Output** (confirmatory only):
```
✅ Traceability Check: PASS
   - Evidence chain: COMPLETE
   - All references: VALID
   - Chronology: CONSISTENT
```

**Severity**: HIGH (audit trail incomplete)

---

### Category 10: CATASTROPHIC_FAILURE

**Definition**: Unexpected failure requiring immediate escalation

**Examples**:
- PR gate script crashes
- Build environment failure
- Canonical governance unreachable
- System integrity compromised

**What to Do**:
1. **STOP all work immediately**
2. **DO NOT attempt to fix yourself**
3. **ESCALATE to Foreman with full error details**
4. **Wait for investigation and guidance**

**This is NOT a builder issue to resolve locally.**

**Severity**: CATASTROPHIC - **ESCALATE IMMEDIATELY**

---

## Local Verification Workflow (Complete)

### Before Submitting ANY PR

Run this complete verification sequence locally:

```bash
# 1. Artifact presence check
python governance/scripts/validate-builder-artifacts.py --check-presence

# 2. Schema validation
python governance/scripts/validate-builder-artifacts.py --check-schemas

# 3. Immutability check
python governance/scripts/validate-builder-artifacts.py --check-immutability

# 4. Agent boundary check
python governance/scripts/validate_agent_boundaries.py

# 5. Readiness check
grep '"qa_status": "READY"' foreman/evidence/builder-qa-report.json

# 6. Architecture alignment (if applicable)
python governance/scripts/validate-architecture-alignment.py --task-id <your-task-id>

# 7. Test debt check
python governance/scripts/validate-test-debt.py

# 8. Governance compliance
python governance/scripts/validate-governance-compliance.py

# 9. Evidence chain check
python governance/scripts/validate-evidence-chain.py

# 10. Checklists
# Review and complete:
# - foreman/builder/templates/agent-boundary-checklist.md
# - foreman/builder/templates/build-to-green-checklist.md
```

### If ALL Pass → Submit PR

Only submit PR when:
- ✅ All local validations pass
- ✅ All checklists completed
- ✅ QA status is READY
- ✅ All tests pass

### If ANY Fail → Fix and Re-verify

Do NOT submit PR until all validations pass.

---

## CI Role (Confirmatory Only)

**Remember**: CI is confirmatory, not diagnostic.

### Expected CI Behavior

If you verified locally and all passed:
- ✅ CI SHOULD pass
- ✅ CI confirms what you already knew
- ✅ CI output matches your local verification

If CI fails after local verification passed:
1. Check if gate infrastructure changed
2. Check if new gate added since you started work
3. Escalate to Foreman if infrastructure issue

**CI is NOT**:
- ❌ A debugging tool
- ❌ A discovery mechanism
- ❌ An iterative feedback loop
- ❌ A substitute for local verification

---

## Quick Reference Card

| Failure Category | Detect Locally With | Fix By | Severity |
|------------------|---------------------|--------|----------|
| ARTIFACT_MISSING | `ls` evidence files | Generate missing artifacts | HIGH |
| SCHEMA_VIOLATION | JSON schema validation | Fix schema violations | HIGH |
| IMMUTABILITY_VIOLATION | Check `immutable: true` | Regenerate (never edit) | CRITICAL |
| AGENT_BOUNDARY_VIOLATION | Agent boundary checklist | Use correct agent | CATASTROPHIC |
| NOT_READY_DECLARATION | Check `qa_status` | Complete work | HIGH |
| ARCHITECTURE_INCOMPLETE | Architecture validation | Complete architecture | HIGH |
| TEST_DEBT_DETECTED | Grep for `.skip()` etc | Implement all tests | HIGH |
| GOVERNANCE_INVARIANT_VIOLATED | Governance validation | Comply with governance | HIGH |
| TRACEABILITY_BROKEN | Check evidence chain | Complete evidence chain | HIGH |
| CATASTROPHIC_FAILURE | N/A | Escalate immediately | CATASTROPHIC |

---

## References

- **Canonical Failure Protocol**: `governance/alignment/PR_GATE_FAILURE_HANDLING_PROTOCOL.md`
- **PR Gate Requirements**: `governance/alignment/PR_GATE_REQUIREMENTS_CANON.md`
- **Agent Boundaries**: `governance/alignment/AGENT_SCOPED_QA_BOUNDARIES.md`
- **Build Philosophy**: `BUILD_PHILOSOPHY.md` - One-Time Build Correctness

---

**Version**: 1.0.0  
**Last Updated**: 2025-12-30  
**Maintained By**: Foreman (FM)
