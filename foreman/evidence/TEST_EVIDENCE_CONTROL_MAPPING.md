# Test → Evidence → Control Mapping

**Version:** 1.0.0  
**Date:** 2025-12-16  
**Authority:** Issue B3 - Evidence Contract Alignment  
**Purpose:** Define clear mappings between QA tests, evidence artifacts, and compliance controls

---

## 1. Overview

This document establishes the canonical mapping between:
1. **QA Tests** - Tests that validate system behavior
2. **Evidence Artifacts** - Structured evidence generated during builds
3. **Compliance Controls** - Requirements from standards (ISO, NIST, COBIT, etc.)

**Core Principle:** Every QA test generates evidence that supports one or more compliance controls.

---

## 2. Evidence Type Definitions

### 2.1 Build Initiation Evidence
- **File:** `build-initiation.json`
- **Schema:** `EVIDENCE_SCHEMA_CANON.json#/schemas/build-initiation`
- **Purpose:** Record the start of a build task with all requirements
- **Immutable:** Yes, created once at build start
- **Audit Replay Role:** Establishes initial state and requirements

### 2.2 Validation Results Evidence
- **File:** `validation-results.json`
- **Schema:** `EVIDENCE_SCHEMA_CANON.json#/schemas/validation-results`
- **Purpose:** Record pre-build validation gate results
- **Immutable:** Yes, created once after validation
- **Audit Replay Role:** Proves build met prerequisites

### 2.3 Iteration Evidence
- **File:** `iterations/iteration-NNN.json`
- **Schema:** `EVIDENCE_SCHEMA_CANON.json#/schemas/iteration`
- **Purpose:** Record each build iteration's changes and QA results
- **Immutable:** Yes, created once per iteration
- **Audit Replay Role:** Allows replay of build progression step-by-step

### 2.4 Final Validation Evidence
- **File:** `final-validation.json`
- **Schema:** `EVIDENCE_SCHEMA_CANON.json#/schemas/final-validation`
- **Purpose:** Record comprehensive final validation before reporting GREEN
- **Immutable:** Yes, created once at build completion
- **Audit Replay Role:** Proves all quality gates passed

---

## 3. Test Category Mappings

### 3.1 Evidence Generation Tests

#### Test: `test_build_initiation_evidence_is_generated`
**Evidence Generated:**
- `build-initiation.json`

**Compliance Controls:**
- **ISO 27001:A.12.1.1** - Documented operating procedures
- **NIST CSF:ID.AM-1** - Physical devices and systems managed
- **COBIT:APO09.03** - Manage service agreements

**Validation:**
- Evidence file exists at expected path
- Evidence conforms to `build-initiation` schema
- Evidence includes all required fields (task_id, architecture_path, timestamp, etc.)

---

#### Test: `test_iteration_evidence_is_generated_per_iteration`
**Evidence Generated:**
- `iterations/iteration-001.json`
- `iterations/iteration-002.json`
- `iterations/iteration-NNN.json` (one per iteration)

**Compliance Controls:**
- **ISO 27001:A.12.1.2** - Change management
- **ISO 27001:A.14.2.9** - System acceptance testing
- **NIST 800-53:CM-3** - Configuration Change Control
- **COBIT:BAI06.01** - Evaluate, prioritize and authorize change requests

**Validation:**
- One evidence file per iteration, numbered sequentially
- Each conforms to `iteration` schema
- Each includes QA status before/after, code changes, test targeted
- Traceability via parent_evidence_id

---

#### Test: `test_final_validation_evidence_is_generated`
**Evidence Generated:**
- `final-validation.json`

**Compliance Controls:**
- **ISO 27001:A.14.2.8** - System security testing
- **ISO 27001:A.14.2.9** - System acceptance testing
- **NIST 800-53:SA-11** - Developer Security Testing
- **COBIT:BAI03.10** - Maintain systems

**Validation:**
- Evidence file exists
- Conforms to `final-validation` schema
- All quality gates passed (QA 100%, build success, lint pass, etc.)
- Evidence is immutable

---

#### Test: `test_evidence_generation_is_automatic_not_manual`
**Evidence Generated:**
- Full evidence chain (initiation → validation → iterations → final)

**Compliance Controls:**
- **ISO 27001:A.18.2.2** - Compliance with security policies
- **NIST 800-53:AU-2** - Audit Events (automatic logging)
- **COBIT:MEA03.01** - Identify and collect monitoring data

**Validation:**
- Evidence generated without explicit manual calls
- Evidence directory structure created automatically
- All mandatory evidence files present

---

### 3.2 Schema Validation Tests

#### Test: `test_build_initiation_evidence_conforms_to_schema`
**Evidence Generated:**
- `build-initiation.json` (validated)

**Compliance Controls:**
- **ISO 27001:A.18.1.5** - Regulation of cryptographic controls
- **NIST 800-53:SA-15** - Development Process, Standards, and Tools
- **COBIT:BAI02.03** - Manage requirements definition

**Validation:**
- Evidence validates against JSON schema
- Schema validator catches malformed evidence
- Governance Gate can reject invalid evidence

---

#### Test: `test_iteration_evidence_conforms_to_schema`
**Evidence Generated:**
- `iterations/iteration-*.json` (validated)

**Compliance Controls:**
- **ISO 27001:A.14.2.1** - Secure development policy
- **NIST 800-53:SA-15** - Development Process, Standards, and Tools
- **COBIT:BAI03.03** - Design solution components

**Validation:**
- Iteration evidence validates against schema
- Required fields present (iteration_number, timestamps, QA status, etc.)
- Enumerated values enforced (next_action, test_debt_detected, etc.)

---

#### Test: `test_schema_validation_catches_missing_required_fields`
**Evidence Generated:**
- Invalid evidence (rejected)

**Compliance Controls:**
- **ISO 27001:A.18.2.3** - Technical compliance review
- **NIST 800-53:CM-6** - Configuration Settings
- **COBIT:MEA03.03** - Ensure compliance with external requirements

**Validation:**
- Schema validator detects missing required fields
- Validation errors are descriptive
- Governance Gate rejects incomplete evidence

---

#### Test: `test_schema_validation_catches_incorrect_field_types`
**Evidence Generated:**
- Invalid evidence (rejected)

**Compliance Controls:**
- **ISO 27001:A.18.2.3** - Technical compliance review
- **NIST 800-53:SI-10** - Information Input Validation
- **COBIT:BAI03.08** - Perform quality reviews

**Validation:**
- Schema validator detects type mismatches
- String/integer/boolean types enforced
- ISO 8601 timestamp format enforced

---

#### Test: `test_evidence_schema_is_versioned`
**Evidence Generated:**
- Schema metadata with version information

**Compliance Controls:**
- **ISO 27001:A.12.1.2** - Change management
- **NIST 800-53:CM-3** - Configuration Change Control
- **COBIT:BAI06.03** - Manage changes

**Validation:**
- Schemas have version numbers
- Evidence includes schema_version in metadata
- Version changes tracked for compatibility

---

### 3.3 Traceability Tests

#### Test: `test_evidence_includes_traceability_chain`
**Evidence Generated:**
- Evidence with parent_evidence_id references

**Compliance Controls:**
- **ISO 27001:A.12.4.1** - Event logging
- **ISO 27001:A.12.4.3** - Administrator and operator logs
- **NIST 800-53:AU-3** - Content of Audit Records
- **COBIT:MEA03.02** - Review effectiveness of system controls

**Validation:**
- Iteration evidence references build initiation
- Evidence chain is complete and unbroken
- Parent references are valid (exist and match task_id)

---

#### Test: `test_evidence_chain_can_be_traversed_backwards`
**Evidence Generated:**
- Complete evidence chain with bidirectional traceability

**Compliance Controls:**
- **ISO 27001:A.12.4.1** - Event logging
- **NIST 800-53:AU-12** - Audit Generation
- **COBIT:MEA03.01** - Identify and collect monitoring data

**Validation:**
- Evidence tracer can traverse from completion to initiation
- All intermediate evidence found
- Chain includes: completion → iterations → validation → initiation

---

#### Test: `test_evidence_includes_architecture_reference`
**Evidence Generated:**
- Build initiation with architecture_path and architecture_hash

**Compliance Controls:**
- **ISO 27001:A.8.1.1** - Inventory of assets
- **ISO 27001:A.14.2.1** - Secure development policy
- **NIST 800-53:CM-8** - Information System Component Inventory
- **COBIT:APO09.02** - Identify services and maintain service catalogue

**Validation:**
- Architecture path recorded in evidence
- Architecture hash/version for immutability
- Traceability to exact architecture used

---

#### Test: `test_evidence_includes_qa_suite_reference`
**Evidence Generated:**
- Build initiation with qa_suite_path and qa_suite_hash

**Compliance Controls:**
- **ISO 27001:A.14.2.8** - System security testing
- **NIST 800-53:SA-11** - Developer Security Testing
- **COBIT:BAI03.10** - Maintain systems

**Validation:**
- QA suite path recorded
- QA suite version/hash for immutability
- Traceability to exact tests executed

---

#### Test: `test_evidence_traceability_to_governance_memory`
**Evidence Generated:**
- Evidence logged to governance memory with tags

**Compliance Controls:**
- **ISO 27001:A.12.4.1** - Event logging
- **ISO 27001:A.18.1.5** - Regulation of cryptographic controls
- **NIST 800-53:AU-9** - Protection of Audit Information
- **COBIT:MEA03.04** - Integrate reporting

**Validation:**
- Evidence logged to memory on generation
- Memory entries tagged appropriately
- Evidence ID traceable in governance memory

---

## 4. Governance Gate Validation Rules

### 4.1 Schema Conformance (MANDATORY)

**Rule:** Evidence MUST conform to canonical schema for its type.

**Tests Validating This:**
- `test_build_initiation_evidence_conforms_to_schema`
- `test_iteration_evidence_conforms_to_schema`
- `test_schema_validation_catches_missing_required_fields`
- `test_schema_validation_catches_incorrect_field_types`

**Governance Gate Action:**
- Load `EVIDENCE_SCHEMA_CANON.json`
- Validate evidence against schema for its type
- If validation fails: REJECT evidence, return detailed errors
- If validation passes: Continue to next gate

**Compliance Controls Satisfied:**
- ISO 27001:A.18.2.3 - Technical compliance review
- NIST 800-53:SA-15 - Development Process, Standards, and Tools
- COBIT:BAI03.08 - Perform quality reviews

---

### 4.2 Immutability (MANDATORY)

**Rule:** Evidence MUST be marked as immutable and never modified post-generation.

**Tests Validating This:**
- All evidence generation tests verify `immutable: true` in metadata
- `test_final_validation_evidence_is_generated` specifically checks immutability

**Governance Gate Action:**
- Check evidence_metadata.immutable === true
- Verify evidence file has not been modified (timestamp, hash)
- If immutability violated: REJECT evidence, flag integrity violation
- If immutable: Continue to next gate

**Compliance Controls Satisfied:**
- ISO 27001:A.12.4.2 - Protection of log information
- NIST 800-53:AU-9 - Protection of Audit Information
- COBIT:MEA03.02 - Review effectiveness of system controls

---

### 4.3 Traceability (MANDATORY)

**Rule:** All evidence MUST include parent_evidence_id or build_initiation_id for chain traceability.

**Tests Validating This:**
- `test_evidence_includes_traceability_chain`
- `test_evidence_chain_can_be_traversed_backwards`
- `test_evidence_includes_architecture_reference`
- `test_evidence_includes_qa_suite_reference`

**Governance Gate Action:**
- Check for parent_evidence_id in iteration evidence
- Verify parent exists and matches task_id
- Verify architecture_path and qa_suite_path present
- If traceability incomplete: REJECT evidence, require metadata
- If traceable: Continue to next gate

**Compliance Controls Satisfied:**
- ISO 27001:A.12.4.1 - Event logging
- NIST 800-53:AU-3 - Content of Audit Records
- COBIT:MEA03.01 - Identify and collect monitoring data

---

### 4.4 Timestamp Validity (MANDATORY)

**Rule:** All timestamps MUST be ISO 8601 format and chronologically consistent.

**Tests Validating This:**
- All evidence generation tests include timestamp validation
- `test_iteration_evidence_is_generated_per_iteration` checks timestamps

**Governance Gate Action:**
- Validate timestamp format (ISO 8601)
- Verify chronological order (start < complete, iterations sequential)
- If timestamps invalid: REJECT evidence, require valid timestamps
- If timestamps valid: Continue to next gate

**Compliance Controls Satisfied:**
- ISO 27001:A.12.4.4 - Clock synchronization
- NIST 800-53:AU-8 - Time Stamps
- COBIT:DSS05.03 - Manage endpoint security

---

### 4.5 Completeness (MANDATORY)

**Rule:** All required fields MUST be present with valid values.

**Tests Validating This:**
- `test_schema_validation_catches_missing_required_fields`
- All schema conformance tests

**Governance Gate Action:**
- Validate all required fields present (per schema)
- Validate field values are non-empty and valid
- If incomplete: REJECT evidence, list missing/invalid fields
- If complete: Continue to next gate

**Compliance Controls Satisfied:**
- ISO 27001:A.18.2.3 - Technical compliance review
- NIST 800-53:CM-6 - Configuration Settings
- COBIT:MEA03.03 - Ensure compliance with external requirements

---

### 4.6 Compliance Mapping (RECOMMENDED)

**Rule:** Evidence SHOULD include compliance_mappings for audit trail.

**Tests Validating This:**
- Evidence metadata includes compliance_mappings array
- `test_evidence_traceability_to_governance_memory` validates logging

**Governance Gate Action:**
- Check for compliance_mappings in evidence_metadata
- If missing: WARN, allow evidence but note gap in audit log
- If present: Record mappings for compliance reporting

**Compliance Controls Satisfied:**
- ISO 27001:A.18.2.1 - Independent review of information security
- NIST 800-53:PL-2 - System Security Plan
- COBIT:APO11.06 - Manage quality

---

## 5. Audit Replay Support

### 5.1 Replay Procedure

**Purpose:** Reconstruct complete build process from evidence trail.

**Steps:**
1. **Load Build Initiation**
   - Establishes: task_id, architecture, QA suite, requirements
   - Validates: instruction format was correct, prerequisites met

2. **Load Validation Results**
   - Establishes: all pre-conditions validated
   - Validates: architecture complete, QA RED, acceptance criteria clear

3. **Load Iterations (Sequential)**
   - Establishes: progression from RED to GREEN
   - Validates: each iteration made progress, no regressions, test debt zero

4. **Load Final Validation**
   - Establishes: all quality gates passed
   - Validates: 100% QA, build success, interface integrity

5. **Compare States**
   - Compare replayed state with actual completion state
   - Flag discrepancies as integrity issues

**Tests Validating Replay:**
- `test_evidence_chain_can_be_traversed_backwards`
- `test_evidence_generation_is_automatic_not_manual`

**Compliance Controls Satisfied:**
- ISO 27001:A.12.4.1 - Event logging
- NIST 800-53:AU-12 - Audit Generation
- COBIT:MEA03.01 - Identify and collect monitoring data

---

### 5.2 Required Evidence Chain

**For Successful Build:**
- ✅ `build-initiation.json` (1 required)
- ✅ `validation-results.json` (1 required)
- ✅ `iterations/iteration-*.json` (1+ required)
- ✅ `final-validation.json` (1 required)

**For Failed/Escalated Build:**
- ✅ `build-initiation.json` (1 required)
- ✅ `validation-results.json` (1 required)
- ✅ `iterations/iteration-*.json` (1+ may exist)
- ✅ `escalation-report.md` (1 required if escalated)

**Governance Gate Action:**
- On build completion: Verify complete evidence chain
- If chain incomplete: REJECT completion, flag missing evidence
- If chain complete: Proceed with validation and approval

---

## 6. Compliance Control Library Integration

### 6.1 Evidence-to-Control Mappings

All evidence includes `compliance_mappings` array in metadata:

```json
"evidence_metadata": {
  "compliance_mappings": [
    "ISO_27001:A.12.1.1",
    "ISO_27001:A.14.2.9",
    "NIST_800_53:SA-11",
    "COBIT:BAI03.10"
  ]
}
```

### 6.2 Control Library Lookup

Governance Gate uses `foreman/compliance/compliance-control-library.json`:

**Process:**
1. Load evidence
2. Extract compliance_mappings from evidence_metadata
3. Look up each control in compliance-control-library.json
4. Record control satisfaction in compliance reporting
5. Aggregate across all evidence for overall compliance coverage

**Tests Validating This:**
- `test_evidence_traceability_to_governance_memory`
- Integration tests (to be added in Wave 1)

---

### 6.3 Standard Coverage Summary

| Standard | Evidence Types | Control Count | Coverage |
|----------|---------------|---------------|----------|
| ISO 27001:2022 | All types | 15+ | High |
| NIST 800-53 | All types | 10+ | High |
| COBIT 2019 | All types | 12+ | High |
| NIST CSF | Build initiation | 2+ | Medium |
| ISO 31000 | Risk-related (future) | TBD | Planned |
| ISO 27005 | Risk-related (future) | TBD | Planned |

---

## 7. Implementation Checklist

### 7.1 Evidence Generation

- [x] Schema definitions in `EVIDENCE_SCHEMA_CANON.json`
- [ ] Evidence generator implementation (Wave 1)
- [ ] Automatic evidence generation on build events
- [ ] Evidence file creation with proper structure
- [ ] Evidence metadata population

### 7.2 Schema Validation

- [x] Schema definitions complete
- [ ] Schema validator implementation (Wave 1)
- [ ] Validation on evidence generation
- [ ] Validation at Governance Gate
- [ ] Detailed validation error reporting

### 7.3 Traceability

- [x] Parent evidence reference schema
- [ ] Evidence chain tracer implementation (Wave 1)
- [ ] Backwards traversal support
- [ ] Architecture/QA suite hashing
- [ ] Governance memory integration

### 7.4 Governance Gate

- [x] Validation rules defined
- [ ] Governance Gate implementation (Wave 1)
- [ ] Schema conformance checker
- [ ] Immutability verifier
- [ ] Traceability validator
- [ ] Timestamp validator
- [ ] Completeness checker
- [ ] Compliance mapping recorder

### 7.5 Audit Replay

- [x] Replay procedure defined
- [ ] Replay engine implementation (Wave 1)
- [ ] State reconstruction logic
- [ ] Discrepancy detection
- [ ] Replay validation tests

---

## 8. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-16 | Initial mapping document for Issue B3 |

---

## 9. References

- `foreman/evidence/EVIDENCE_SCHEMA_CANON.json` - Canonical schema definitions
- `foreman/evidence/README.md` - Evidence directory overview
- `foreman/architecture/FOREMAN_EVIDENCE_ARCHITECTURE_v1.0.md` - Evidence architecture
- `foreman/compliance/compliance-control-library.json` - Compliance controls
- `tests/wave0_minimum_red/test_evidence_integrity.py` - Evidence validation tests
- `BUILD_PHILOSOPHY.md` - Section XII: Evidence Requirements

---

*END OF TEST → EVIDENCE → CONTROL MAPPING*
