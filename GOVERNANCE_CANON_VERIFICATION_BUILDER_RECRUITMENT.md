# Governance Canon Verification: Builder Recruitment Requirements
## Audit Report

**Date**: 2026-01-01  
**Auditor**: Maturion Foreman (FM)  
**Scope**: Builder recruitment requirements in governance canon  
**Purpose**: Identify gaps, ambiguities, and required updates  
**Status**: AUDIT_COMPLETE

---

## Executive Summary

This audit examines governance canon to determine:
1. Whether builder recruitment automation is explicitly specified
2. Whether `.github/agents/` builder artifacts are mandated
3. Whether enforcement rules exist
4. What gaps or ambiguities enabled the Phase 4.5 failure

**Finding**: Governance canon DOES specify `.github/agents/` requirement but enforcement was incomplete and cross-referencing was insufficient.

---

## 1. Canonical Requirements Found

### 1.1 Platform Readiness Canon (PRIMARY REFERENCE)

**Location**: `governance/canon/PLATFORM_READINESS_FOR_GOVERNED_BUILD_EXECUTION.md`

**Specification** (Line 271-273):
```
1. **Contract Existence Validation** (per agent role, per repository):
   - Verify FM contract exists: `.github/agents/foreman.md` or repository-specific path
   - Verify Builder contracts exist: `.github/agents/<builder-role>.md` (e.g., `ui-builder.md`)
   - Verify Governance Admin contract exists: `.github/agents/governance-administrator.md`
```

**Status**: ✅ EXPLICIT — `.github/agents/<builder-role>.md` IS mandated

**Schema Requirements** (Line 276-279):
```
2. **Schema Conformance Validation**:
   - Load `.agent.schema.md` required sections list
   - For each contract: parse markdown and verify all required sections present
   - Verify no sections are placeholder text (e.g., "TBD", "TODO")
```

**Status**: ✅ SCHEMA VALIDATION IS mandated

**Assessment**: Canon clearly requires `.github/agents/` location and schema validation.

### 1.2 Builder Initialization Documentation

**Location**: `foreman/BUILDER_INITIALIZATION.md`

**Specification** (Line 8-20):
```
## Recruitment Status

**Builder Recruitment**: ✅ **COMPLETE (Wave 0.1)**  
**CS2 Approval**: ✅ **GRANTED**  
**Canonical Status**: **ACTIVE AND CONTINUOUS ACROSS WAVES**

All 5 builder agents listed below were **canonically recruited in Wave 0.1**
```

**Structure Described** (Line 34-98):
- `foreman/builder-manifest.json`
- `foreman/builder/builder-capability-map.json`
- `foreman/builder/builder-permission-policy.json`
- `foreman/builder/*-builder-spec.md`

**Status**: ⚠️ AMBIGUOUS — Describes internal structure but does NOT mandate `.github/agents/`

**Assessment**: This document focuses on foreman-internal structure and does not cross-reference the platform readiness canon requirement for `.github/agents/`.

### 1.3 Wave 0.1 Builder Recruitment Spec

**Location**: `WAVE_0.1_BUILDER_RECRUITMENT_SPEC.md`

**Scope Defined** (Line 86-100):
```
### 2.2 Recruitment Process

For each builder:

1. **Specification Review**
   - Load builder specification from `foreman/builder/<builder>-spec.md`
   - Verify responsibilities align with manifest
   - Confirm forbidden actions are clearly defined

2. **Capability Validation**
   - Cross-reference with `foreman/builder/builder-capability-map.json`

3. **Permission Validation**
   - Cross-reference with `foreman/builder/builder-permission-policy.json`
```

**Status**: ❌ INCOMPLETE — Does NOT mention `.github/agents/` requirement

**Assessment**: Wave 0.1 spec treated builder recruitment as validation of `foreman/` artifacts only. No reference to platform readiness canon or `.github/agents/` requirement.

---

## 2. Gaps Identified

### 2.1 Cross-Referencing Gap

**Gap**: `foreman/BUILDER_INITIALIZATION.md` and `WAVE_0.1_BUILDER_RECRUITMENT_SPEC.md` do not reference `governance/canon/PLATFORM_READINESS_FOR_GOVERNED_BUILD_EXECUTION.md`.

**Impact**: Execution planning proceeded without awareness of `.github/agents/` requirement.

**Severity**: HIGH — Enabled catastrophic failure

**Required Fix**: 
- Add explicit cross-reference from `foreman/BUILDER_INITIALIZATION.md` to platform readiness canon
- Update Wave 0.1+ specs to mandate `.github/agents/` validation

### 2.2 Enforcement Checkpoint Gap

**Gap**: No validation checkpoint in Wave 0.1 or Platform Readiness verification required proof of `.github/agents/<builder>.md` existence.

**Impact**: "Recruitment complete" status granted without automation artifacts.

**Severity**: HIGH — Enforcement failure

**Required Fix**:
- Add mandatory checkpoint: "Verify `.github/agents/<builder>.md` exists for all 5 builders"
- Update platform readiness validation to reject approval without builder contracts

### 2.3 Schema Definition Gap

**Gap**: Platform readiness canon references `.agent.schema.md` but this schema is not present in repository.

**Impact**: Cannot validate builder contract conformance.

**Severity**: MODERATE — Schema undefined

**Required Fix**:
- Create `.github/agents/.agent.schema.md` or equivalent
- Define required sections for builder contracts
- Implement schema validation tooling

### 2.4 Automation Mechanism Gap

**Gap**: No specification exists for HOW builder contracts enable automation (selection mechanism, gate binding, task routing).

**Impact**: Even with contracts present, automation mechanism unclear.

**Severity**: MODERATE — Implementation guidance missing

**Required Fix**:
- Document builder selection mechanism (how FM reads contracts)
- Document gate binding mechanism (how workflows reference builders)
- Document task routing mechanism (how builders receive assignments)

---

## 3. Enforcement Rule Analysis

### 3.1 Existing Enforcement

**Platform Readiness Canon** specifies validation requirements but does NOT specify:
- When validation occurs (pre-Wave 1.0? pre-Phase 5.0?)
- Who performs validation (FM? CI? Manual?)
- What happens if validation fails (block? escalate?)

**Assessment**: Requirements exist but enforcement mechanism is underspecified.

### 3.2 Missing Enforcement

No enforcement rules found for:
- Automatic rejection of "recruitment complete" without `.github/agents/` proof
- CI checks that validate builder contract presence
- Automated schema validation on builder contract changes
- Gate binding validation (ensure contracts are used by workflows)

**Assessment**: Enforcement is manual and non-blocking.

---

## 4. Required Governance Updates

### 4.1 Immediate Updates (This Issue)

1. **Create `.github/agents/` Builder Contracts** (5 files)
   - `ui-builder.md`
   - `api-builder.md`
   - `schema-builder.md`
   - `integration-builder.md`
   - `qa-builder.md`

2. **Define Builder Contract Schema**
   - Create `.github/agents/BUILDER_CONTRACT_SCHEMA.md`
   - Specify required sections and format

3. **Update `foreman/BUILDER_INITIALIZATION.md`**
   - Add cross-reference to platform readiness canon
   - Mandate `.github/agents/` location
   - Document automation mechanism

4. **Update Platform Readiness Checklist**
   - Add: "Verify all 5 builder contracts exist in `.github/agents/`"
   - Add: "Verify builder contracts conform to schema"
   - Add: "Verify builder selection mechanism is testable"

### 4.2 Post-Fix Updates (Future Issues)

1. **Create Automated Validation Tooling**
   - CI check that validates builder contract presence
   - Schema validation on contract changes
   - Automated recruitment mechanism tests

2. **Update Wave Planning Templates**
   - Require platform readiness canon review before Wave 0.1
   - Mandate `.github/agents/` validation checkpoint

3. **Consolidate Builder Recruitment Governance**
   - Merge requirements from multiple locations into single spec
   - Establish single source of truth for builder recruitment

---

## 5. Canon Status Assessment

### 5.1 What Canon Got Right

✅ **Clear Specification**: Canon explicitly requires `.github/agents/<builder-role>.md`  
✅ **Schema Awareness**: Canon anticipates need for schema validation  
✅ **Multi-Agent Coverage**: Canon covers FM, builders, and governance admin

### 5.2 What Canon Missed

❌ **Enforcement Timing**: When validation must occur  
❌ **Enforcement Mechanism**: Who validates and how  
❌ **Failure Mode**: What happens when validation fails  
❌ **Automation Detail**: How contracts enable automation  
❌ **Cross-Referencing**: Not linked from execution specs

### 5.3 Overall Canon Quality

**Assessment**: Canon specification is CORRECT but INSUFFICIENT.

The requirement is present but:
- Not enforced at appropriate checkpoints
- Not cross-referenced from execution planning
- Not validated during Wave 0.1 execution
- Not accompanied by enforcement mechanism

---

## 6. Corrective Design Implications

Based on this audit, the corrective design MUST include:

1. **Builder Contracts** (`.github/agents/<builder>.md`)
   - YAML frontmatter with machine-readable metadata
   - Markdown body with human-readable documentation
   - Schema-conformant structure

2. **Contract Schema** (`.github/agents/BUILDER_CONTRACT_SCHEMA.md`)
   - Required sections definition
   - Metadata format specification
   - Validation rules

3. **Automation Mechanism Documentation**
   - How FM selects builders from contracts
   - How workflows bind gates to builders
   - How task routing uses contracts

4. **Enforcement Updates**
   - Platform readiness validation includes builder contracts
   - CI checks validate contract presence and schema
   - Wave planning templates require canon review

---

## 7. Governance Gap Classification

| Gap | Location | Severity | Fix Required |
|-----|----------|----------|--------------|
| Cross-referencing missing | `foreman/BUILDER_INITIALIZATION.md` | HIGH | Add canon reference |
| Enforcement checkpoint missing | Wave 0.1 spec | HIGH | Add validation step |
| Schema undefined | `.github/agents/` | MODERATE | Create schema |
| Automation mechanism unspecified | Canon | MODERATE | Document mechanism |
| Validation timing unclear | Canon | LOW | Specify timing |
| Failure mode undefined | Canon | LOW | Specify consequences |

---

## 8. Conclusion

**Primary Finding**: Governance canon correctly specifies `.github/agents/<builder>.md` requirement, but enforcement was insufficient and cross-referencing was incomplete.

**Root Governance Gap**: Execution planning (`WAVE_0.1_BUILDER_RECRUITMENT_SPEC.md`) did not cross-reference or validate against platform readiness canon requirement.

**Secondary Governance Gap**: Platform readiness validation did not include builder contract verification checkpoint.

**Tertiary Governance Gap**: No automated enforcement mechanism (CI checks) for builder contract presence.

**Recommendation**: Canon specification is sound. Gaps are in:
1. Enforcement checkpoints
2. Cross-referencing from execution specs
3. Automated validation tooling
4. Automation mechanism documentation

**Status**: ✅ AUDIT COMPLETE — Proceeding to Corrective Design

---

**Auditor**: Maturion Foreman (FM)  
**Date**: 2026-01-01  
**Next Action**: Design Automated Builder Recruitment Mechanism
