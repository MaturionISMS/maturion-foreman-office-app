# Ratchet Condition Enforcement: Builder Recruitment Automation (BL-016)
## Permanent Governance Constraint

**Ratchet ID**: BL-016  
**Classification**: CATASTROPHIC  
**Date Activated**: 2026-01-01  
**Authority**: Bootstrap Execution Learnings  
**Status**: ✅ ACTIVE — PERMANENTLY ENFORCED

---

## Ratchet Statement

> **Builder recruitment without `.github/agents/` automation is permanently prohibited.**

This ratchet condition is activated as a result of the catastrophic failure in Phase 4.5/Wave 0.1 where builder recruitment was misclassified as documentation instead of system configuration.

**One-Time Acceptance**: This failure has been accepted ONCE. Future violations are prohibited.

---

## Mandatory Requirements (Non-Negotiable)

All future builder recruitment MUST include:

### 1. GitHub-Native Location
- ✅ Builder contracts MUST exist in `.github/agents/<builder-name>.md`
- ❌ Root-level documentation files are insufficient
- ❌ Internal-only artifacts (foreman/ only) are insufficient

### 2. Machine-Readable Format
- ✅ Contracts MUST use YAML frontmatter + Markdown body
- ✅ YAML frontmatter must be parseable by standard tools
- ❌ Pure documentation/narrative is insufficient

### 3. Schema Conformance
- ✅ Contracts MUST conform to `.github/agents/BUILDER_CONTRACT_SCHEMA.md`
- ✅ Schema validation MUST pass
- ❌ Non-conformant contracts are invalid

### 4. Automated Validation
- ✅ Platform readiness MUST validate builder contract presence
- ✅ Validation MUST be automated (script or CI)
- ❌ Manual inspection is insufficient

### 5. Programmatic Integration
- ✅ Builder selection MUST be automatable via contracts
- ✅ Gate binding MUST reference contracts
- ❌ Manual coordination is insufficient

---

## Prohibited Actions (Permanent)

The following actions are permanently prohibited:

### ❌ 1. Documentation-Only Recruitment
Creating builder documentation without `.github/agents/` contracts is prohibited.

**Example Violation**:
```
# PROHIBITED
1. Create builderui-builder.md in root
2. Write comprehensive documentation
3. Declare "recruited and validated"
```

**Correct Approach**:
```
# REQUIRED
1. Create .github/agents/ui-builder.md with YAML frontmatter
2. Validate against schema
3. Test automated recruitment mechanism
4. Update platform readiness with validation proof
```

### ❌ 2. Root-Level Contract Location
Placing builder contracts in repository root or foreman/ directory without `.github/agents/` is prohibited.

**Rationale**: GitHub Actions and automation tools require `.github/agents/` location.

### ❌ 3. Recruitment Without Validation
Declaring "recruitment complete" without automated validation proof is prohibited.

**Required Proof**:
- ✅ Validation script execution results
- ✅ Schema conformance confirmation
- ✅ Platform readiness approval with builder contract verification

### ❌ 4. Platform Readiness Without Builder Contracts
Approving platform readiness without verifying builder contract presence is prohibited.

**Required Verification**:
- [ ] All required builders have contracts in `.github/agents/`
- [ ] All contracts conform to schema
- [ ] Automated recruitment mechanism is testable
- [ ] Builder selection can be performed programmatically

### ❌ 5. Manual-Only Recruitment
Builder recruitment that cannot be automated is prohibited.

**Requirement**: All recruitment steps must be automatable via:
- Contract parsing (YAML frontmatter)
- Programmatic builder selection
- Automated gate binding
- Scripted validation

---

## Enforcement Mechanism

### Level 1: Platform Readiness Gate (BLOCKING)

**Rule**: Platform readiness CANNOT be approved without builder contract verification.

**Checklist Addition**:
```markdown
## Builder Contract Validation (BL-016)

- [ ] All required builders have contracts in `.github/agents/`
- [ ] All builder contracts conform to BUILDER_CONTRACT_SCHEMA.md
- [ ] Schema validation script passes
- [ ] Automated builder selection is testable
- [ ] Gate binding mechanism is operational

**Enforcement**: Ratchet BL-016 — Builder recruitment without automation is prohibited
```

**Blocking Condition**: If any checkbox fails, platform readiness is RED.

### Level 2: Wave Planning Gate (BLOCKING)

**Rule**: Wave 1.0+ execution CANNOT proceed without builder recruitment verification.

**Wave Planning Checklist Addition**:
```markdown
## Builder Recruitment Verification (BL-016)

Before Wave 1.0+ execution:
- [ ] Verify builder recruitment continuity from Wave 0.1
- [ ] Verify all builder contracts exist in `.github/agents/`
- [ ] Verify builder contracts are schema-conformant
- [ ] Verify no new builders require recruitment
- [ ] If new builders required, follow BL-016 enforcement

**Enforcement**: Ratchet BL-016 — No Wave execution without builder contract verification
```

**Blocking Condition**: Wave execution CANNOT start if verification fails.

### Level 3: CI Validation (RECOMMENDED)

**Rule**: CI SHOULD validate builder contracts on changes to `.github/agents/`.

**CI Workflow Design**:
```yaml
# .github/workflows/validate-builder-contracts.yml
name: Validate Builder Contracts

on:
  pull_request:
    paths:
      - '.github/agents/*-builder.md'
      - '.github/agents/BUILDER_CONTRACT_SCHEMA.md'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate Contracts
        run: python scripts/validate_builder_contracts.py
```

**Status**: RECOMMENDED (not yet mandatory, but should be implemented)

### Level 4: CS2 Override Authority (EXCEPTIONAL)

**Rule**: Only CS2 (Johan) can authorize deviation from BL-016.

**Override Process**:
1. Explicit CS2 approval required
2. Rationale must be documented
3. Temporary exception only (must be corrected)
4. Override documented in issue/PR

**Use Cases**:
- Emergency hotfix requiring builder work before contracts can be created
- Experimental/prototype builder not yet formalized
- Migration/transition scenarios with explicit timeline

**Expectation**: Overrides should be RARE (ideally zero).

---

## Validation Checklist

### For New Builder Recruitment (Future)

Before declaring a new builder "recruited":

1. **Contract Creation**
   - [ ] Create `.github/agents/<builder-id>.md`
   - [ ] Populate YAML frontmatter with all required fields
   - [ ] Write all required markdown sections
   - [ ] Set `status: recruited`

2. **Schema Validation**
   - [ ] Run `python scripts/validate_builder_contracts.py`
   - [ ] Confirm validation passes
   - [ ] Fix any validation errors

3. **Integration**
   - [ ] Update `foreman/builder-manifest.json`
   - [ ] Update `foreman/builder/builder-capability-map.json`
   - [ ] Update `foreman/builder/builder-permission-policy.json`
   - [ ] Create `foreman/builder/<builder>-spec.md`

4. **Verification**
   - [ ] Test automated builder selection
   - [ ] Test gate binding with test PR
   - [ ] Update platform readiness validation

5. **Approval**
   - [ ] Generate recruitment report
   - [ ] Present evidence to CS2
   - [ ] Obtain explicit approval

### For Wave Re-Entry (Existing Builders)

Before starting Wave 1.0+ with existing builders:

1. **Continuity Verification**
   - [ ] Verify builder recruitment from Wave 0.1
   - [ ] Verify contracts exist in `.github/agents/`
   - [ ] Verify contracts are schema-conformant
   - [ ] Verify builder status is `recruited` or `active`

2. **No Re-Recruitment**
   - [ ] Confirm builders do NOT need re-recruitment
   - [ ] Proceed directly to task assignment (appointment, not recruitment)

---

## Failure Scenarios and Responses

### Scenario 1: Builder Contract Missing

**Symptom**: `.github/agents/<builder>.md` does not exist

**Response**:
1. STOP Wave execution immediately
2. Create missing contract following BL-016 requirements
3. Validate contract against schema
4. Update platform readiness
5. Resume Wave execution only after contract validated

**Prohibition**: DO NOT proceed with "we'll add it later" approach.

### Scenario 2: Contract Invalid (Schema Violation)

**Symptom**: Validation script reports schema errors

**Response**:
1. STOP Wave execution immediately
2. Fix schema violations in contract
3. Re-run validation until passing
4. Resume Wave execution only after validation passes

**Prohibition**: DO NOT manually override schema validation.

### Scenario 3: Documentation-Only Recruitment Detected

**Symptom**: Builder "recruited" but no `.github/agents/` contract

**Response**:
1. ESCALATE as ratchet violation (BL-016)
2. Classify as CATASTROPHIC regression
3. Follow corrective action process (RCA, learning, fix)
4. CS2 awareness required

**Prohibition**: This scenario MUST NOT occur (ratchet violation).

### Scenario 4: Automation Not Possible

**Symptom**: Builder selection/gate binding cannot be automated

**Response**:
1. STOP and ESCALATE to CS2
2. Identify why automation is not possible
3. Design corrective solution
4. Implement automation before proceeding

**Prohibition**: DO NOT proceed with manual workarounds.

---

## Ratchet Maintenance

### Continuous Monitoring

**Responsibility**: Foreman (FM)

**Activities**:
- Monitor all builder recruitment activities
- Verify BL-016 compliance before Wave execution
- Report violations immediately
- Update enforcement mechanisms as needed

### Governance Updates

**Responsibility**: Foreman (FM) with CS2 approval

**Trigger**: If BL-016 proves insufficient or if new scenarios emerge

**Process**:
1. Identify gap in current ratchet
2. Propose ratchet update
3. Document rationale
4. Obtain CS2 approval
5. Update BOOTSTRAP_EXECUTION_LEARNINGS.md

### Ratchet Review

**Frequency**: After each major wave or on request

**Purpose**: Verify ratchet remains effective and appropriate

**Criteria**:
- Has ratchet prevented violations?
- Have any violations occurred?
- Are enforcement mechanisms working?
- Are updates needed?

---

## Accountability

### FM Accountability

FM is responsible for:
- ✅ Enforcing BL-016 before all Wave execution
- ✅ Validating builder contracts before platform readiness approval
- ✅ Escalating violations immediately
- ✅ Maintaining ratchet enforcement mechanisms

### CS2 Accountability

CS2 is responsible for:
- ✅ Final approval of builder recruitment
- ✅ Override authority (exceptional cases only)
- ✅ Ratchet update approval
- ✅ Violation adjudication

### Builder Accountability

Builders are responsible for:
- ✅ Operating within contract boundaries
- ✅ Respecting forbidden actions
- ✅ Maintaining contract accuracy

---

## Conclusion

**Ratchet BL-016** is a permanent governance constraint established to prevent recurrence of the catastrophic builder recruitment failure.

**Core Principle**: Builder recruitment MUST be automated, machine-readable, and GitHub-native.

**Enforcement**: Multi-level blocking gates ensure compliance:
1. Platform readiness gate (BLOCKING)
2. Wave planning gate (BLOCKING)
3. CI validation (RECOMMENDED)
4. CS2 override authority (EXCEPTIONAL)

**Status**: ✅ ACTIVE — This ratchet is in force immediately and permanently.

**Violations**: Any violation must be treated as CATASTROPHIC and escalated immediately.

---

**Ratchet Authority**: Maturion Foreman (FM)  
**Ratchet Status**: ✅ ACTIVE — PERMANENTLY ENFORCED  
**Last Updated**: 2026-01-01  
**Next Review**: After Wave 1.0 completion or on CS2 request
