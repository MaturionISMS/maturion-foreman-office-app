# Governance Gate Evidence Validation Specification

**Version:** 1.0.0  
**Date:** 2025-12-16  
**Authority:** Issue B3 - Evidence Contract Alignment  
**Purpose:** Define how the Governance Gate validates evidence for consumption

---

## 1. Overview

The **Governance Gate** is the checkpoint that validates all evidence before it can be used for:
- Compliance reporting
- Audit trails
- Build approval
- Quality assurance

**Core Principle:** No evidence enters the system without passing through the Governance Gate.

---

## 2. Governance Gate Responsibilities

### 2.1 Evidence Validation
- Validate evidence conforms to `EVIDENCE_SCHEMA_CANON.json`
- Enforce schema compliance for all evidence types
- Reject malformed or incomplete evidence

### 2.2 Immutability Enforcement
- Verify evidence is marked as immutable (`immutable: true`)
- Detect any post-generation modifications
- Flag integrity violations

### 2.3 Traceability Verification
- Verify evidence chain is complete and unbroken
- Validate parent references exist and are correct
- Ensure chronological consistency of timestamps

### 2.4 Compliance Mapping
- Record compliance controls supported by evidence
- Track evidence-to-control mappings
- Support compliance reporting and audits

### 2.5 Audit Replay Support
- Ensure evidence structure supports full audit replay
- Validate all required evidence artifacts are present
- Enable state reconstruction from evidence trail

---

## 3. Validation Rules

### 3.1 Schema Conformance (MANDATORY)

**Rule:** Evidence MUST conform to canonical schema for its type.

**Implementation:**
```python
from jsonschema import validate, ValidationError
import json

def validate_schema_conformance(evidence, evidence_type):
    """
    Validate evidence against canonical schema.
    
    Args:
        evidence: Evidence object to validate
        evidence_type: Type of evidence (build-initiation, iteration, etc.)
    
    Returns:
        dict: {valid: bool, errors: list}
    """
    # Load canonical schema
    with open('foreman/evidence/EVIDENCE_SCHEMA_CANON.json') as f:
        canon = json.load(f)
    
    schema = canon['schemas'][evidence_type]
    
    try:
        validate(instance=evidence, schema=schema)
        return {'valid': True, 'errors': []}
    except ValidationError as e:
        return {'valid': False, 'errors': [str(e)]}
```

**Action on Violation:**
- REJECT evidence
- Return detailed validation errors
- Log to governance memory with `governance-violation` tag

**Compliance Controls:**
- ISO 27001:A.18.2.3 - Technical compliance review
- NIST 800-53:SA-15 - Development Process, Standards, and Tools
- COBIT:BAI03.08 - Perform quality reviews

---

### 3.2 Immutability Verification (MANDATORY)

**Rule:** Evidence MUST be marked as immutable and never modified post-generation.

**Implementation:**
```python
import hashlib
from pathlib import Path

def verify_immutability(evidence, evidence_path):
    """
    Verify evidence is immutable.
    
    Args:
        evidence: Evidence object
        evidence_path: Path to evidence file
    
    Returns:
        dict: {valid: bool, errors: list}
    """
    errors = []
    
    # Check metadata flag
    if not evidence.get('evidence_metadata', {}).get('immutable', False):
        errors.append("Evidence metadata does not mark evidence as immutable")
    
    # Check file has not been modified (compare hash if stored)
    if evidence_path.exists():
        # Could implement hash checking here
        # For now, just verify flag exists
        pass
    
    if errors:
        return {'valid': False, 'errors': errors}
    else:
        return {'valid': True, 'errors': []}
```

**Action on Violation:**
- REJECT evidence
- Flag integrity violation in governance log
- Escalate to Foreman for investigation

**Compliance Controls:**
- ISO 27001:A.12.4.2 - Protection of log information
- NIST 800-53:AU-9 - Protection of Audit Information
- COBIT:MEA03.02 - Review effectiveness of system controls

---

### 3.3 Traceability Validation (MANDATORY)

**Rule:** All evidence MUST include parent_evidence_id or build_initiation_id for chain traceability.

**Implementation:**
```python
def validate_traceability(evidence, evidence_type):
    """
    Validate evidence traceability chain.
    
    Args:
        evidence: Evidence object
        evidence_type: Type of evidence
    
    Returns:
        dict: {valid: bool, errors: list}
    """
    errors = []
    metadata = evidence.get('evidence_metadata', {})
    
    # Iteration and final-validation require parent reference
    if evidence_type in ['iteration', 'final-validation']:
        if 'parent_evidence_id' not in metadata:
            errors.append(f"{evidence_type} evidence must include parent_evidence_id for traceability")
    
    # All evidence should have architecture/QA references (if applicable)
    if evidence_type == 'build-initiation':
        instruction = evidence.get('instruction_received', {})
        if 'architecture_reference' not in instruction:
            errors.append("Build initiation must include architecture_reference")
        if 'qa_suite_location' not in instruction:
            errors.append("Build initiation must include qa_suite_location")
    
    if errors:
        return {'valid': False, 'errors': errors}
    else:
        return {'valid': True, 'errors': []}
```

**Action on Violation:**
- REJECT evidence
- Require traceability metadata to be added
- Log gap in governance memory

**Compliance Controls:**
- ISO 27001:A.12.4.1 - Event logging
- NIST 800-53:AU-3 - Content of Audit Records
- COBIT:MEA03.01 - Identify and collect monitoring data

---

### 3.4 Timestamp Validation (MANDATORY)

**Rule:** All timestamps MUST be ISO 8601 format and chronologically consistent.

**Implementation:**
```python
from datetime import datetime
import re

def validate_timestamps(evidence, evidence_type):
    """
    Validate timestamp format and chronological consistency.
    
    Args:
        evidence: Evidence object
        evidence_type: Type of evidence
    
    Returns:
        dict: {valid: bool, errors: list}
    """
    errors = []
    iso8601_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{3})?Z$'
    
    # Extract timestamps based on evidence type
    timestamps = {}
    if 'timestamp_started' in evidence:
        timestamps['started'] = evidence['timestamp_started']
    if 'timestamp_completed' in evidence:
        timestamps['completed'] = evidence['timestamp_completed']
    if 'validation_timestamp' in evidence:
        timestamps['validation'] = evidence['validation_timestamp']
    
    # Validate format
    for key, timestamp in timestamps.items():
        if not re.match(iso8601_pattern, timestamp):
            errors.append(f"Timestamp '{key}' is not in ISO 8601 format: {timestamp}")
    
    # Validate chronological order (started < completed)
    if 'started' in timestamps and 'completed' in timestamps:
        try:
            start = datetime.fromisoformat(timestamps['started'].replace('Z', '+00:00'))
            end = datetime.fromisoformat(timestamps['completed'].replace('Z', '+00:00'))
            if start >= end:
                errors.append(f"timestamp_started must be before timestamp_completed")
        except ValueError as e:
            errors.append(f"Invalid timestamp format: {e}")
    
    if errors:
        return {'valid': False, 'errors': errors}
    else:
        return {'valid': True, 'errors': []}
```

**Action on Violation:**
- REJECT evidence
- Require valid ISO 8601 timestamps
- Log timestamp violation

**Compliance Controls:**
- ISO 27001:A.12.4.4 - Clock synchronization
- NIST 800-53:AU-8 - Time Stamps
- COBIT:DSS05.03 - Manage endpoint security

---

### 3.5 Completeness Validation (MANDATORY)

**Rule:** All required fields MUST be present with valid values.

**Implementation:**
```python
def validate_completeness(evidence, evidence_type):
    """
    Validate all required fields are present and non-empty.
    
    Args:
        evidence: Evidence object
        evidence_type: Type of evidence
    
    Returns:
        dict: {valid: bool, errors: list}
    """
    # Schema validation already checks required fields
    # This adds additional semantic checks
    
    errors = []
    
    # Check for empty strings in critical fields
    if evidence_type == 'build-initiation':
        if not evidence.get('task_id', '').strip():
            errors.append("task_id cannot be empty")
        if not evidence.get('evidence_location', '').strip():
            errors.append("evidence_location cannot be empty")
    
    # Check arrays are not empty where required
    if evidence_type == 'build-initiation':
        if len(evidence.get('expected_deliverables', [])) == 0:
            errors.append("expected_deliverables cannot be empty")
    
    if errors:
        return {'valid': False, 'errors': errors}
    else:
        return {'valid': True, 'errors': []}
```

**Action on Violation:**
- REJECT evidence
- List missing/invalid fields
- Require complete evidence

**Compliance Controls:**
- ISO 27001:A.18.2.3 - Technical compliance review
- NIST 800-53:CM-6 - Configuration Settings
- COBIT:MEA03.03 - Ensure compliance with external requirements

---

### 3.6 Compliance Mapping Validation (RECOMMENDED)

**Rule:** Evidence SHOULD include compliance_mappings for audit trail.

**Implementation:**
```python
def validate_compliance_mapping(evidence):
    """
    Validate compliance mappings are present.
    
    Args:
        evidence: Evidence object
    
    Returns:
        dict: {valid: bool, warnings: list}
    """
    warnings = []
    metadata = evidence.get('evidence_metadata', {})
    
    if 'compliance_mappings' not in metadata:
        warnings.append("Evidence does not include compliance_mappings (recommended)")
    elif len(metadata['compliance_mappings']) == 0:
        warnings.append("compliance_mappings array is empty (recommended to populate)")
    
    # This is a warning, not a rejection
    return {'valid': True, 'warnings': warnings}
```

**Action on Violation:**
- WARN (do not reject)
- Allow evidence to proceed
- Note gap in audit log
- Recommend adding mappings

**Compliance Controls:**
- ISO 27001:A.18.2.1 - Independent review of information security
- NIST 800-53:PL-2 - System Security Plan
- COBIT:APO11.06 - Manage quality

---

## 4. Governance Gate Implementation

### 4.1 Main Validation Function

```python
class GovernanceGate:
    """Governance Gate for evidence validation"""
    
    def __init__(self):
        self.schema_path = Path('foreman/evidence/EVIDENCE_SCHEMA_CANON.json')
        with open(self.schema_path) as f:
            self.canon = json.load(f)
    
    def validate_evidence(self, evidence, evidence_type):
        """
        Validate evidence through all governance gates.
        
        Args:
            evidence: Evidence object to validate
            evidence_type: Type of evidence
        
        Returns:
            dict: {
                valid: bool,
                errors: list,
                warnings: list,
                validation_results: dict
            }
        """
        all_errors = []
        all_warnings = []
        results = {}
        
        # 1. Schema Conformance (MANDATORY)
        schema_result = self.validate_schema_conformance(evidence, evidence_type)
        results['schema_conformance'] = schema_result
        if not schema_result['valid']:
            all_errors.extend(schema_result['errors'])
        
        # 2. Immutability (MANDATORY)
        immutability_result = self.verify_immutability(evidence)
        results['immutability'] = immutability_result
        if not immutability_result['valid']:
            all_errors.extend(immutability_result['errors'])
        
        # 3. Traceability (MANDATORY)
        traceability_result = self.validate_traceability(evidence, evidence_type)
        results['traceability'] = traceability_result
        if not traceability_result['valid']:
            all_errors.extend(traceability_result['errors'])
        
        # 4. Timestamps (MANDATORY)
        timestamp_result = self.validate_timestamps(evidence, evidence_type)
        results['timestamps'] = timestamp_result
        if not timestamp_result['valid']:
            all_errors.extend(timestamp_result['errors'])
        
        # 5. Completeness (MANDATORY)
        completeness_result = self.validate_completeness(evidence, evidence_type)
        results['completeness'] = completeness_result
        if not completeness_result['valid']:
            all_errors.extend(completeness_result['errors'])
        
        # 6. Compliance Mapping (RECOMMENDED)
        compliance_result = self.validate_compliance_mapping(evidence)
        results['compliance_mapping'] = compliance_result
        if 'warnings' in compliance_result:
            all_warnings.extend(compliance_result['warnings'])
        
        # Overall result
        overall_valid = len(all_errors) == 0
        
        return {
            'valid': overall_valid,
            'errors': all_errors,
            'warnings': all_warnings,
            'validation_results': results,
            'evidence_type': evidence_type,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
    
    # Individual validation methods would be implemented here
    # (as shown in sections 3.1 - 3.6 above)
```

### 4.2 Usage Example

```python
# Initialize Governance Gate
gate = GovernanceGate()

# Load evidence
with open('foreman/evidence/builds/task-001/build-initiation.json') as f:
    evidence = json.load(f)

# Validate through gate
result = gate.validate_evidence(evidence, evidence_type='build-initiation')

if result['valid']:
    print("✅ Evidence ACCEPTED by Governance Gate")
    print(f"Warnings: {result['warnings']}")
else:
    print("❌ Evidence REJECTED by Governance Gate")
    print(f"Errors: {result['errors']}")
```

---

## 5. Audit Replay Support

### 5.1 Replay Engine

The Governance Gate enables audit replay by ensuring evidence structure is complete.

```python
class AuditReplayEngine:
    """Engine for replaying builds from evidence trail"""
    
    def replay_build(self, task_id):
        """
        Replay build process from evidence trail.
        
        Args:
            task_id: Task identifier
        
        Returns:
            dict: {
                success: bool,
                states: list,
                final_state: dict,
                errors: list
            }
        """
        evidence_dir = Path(f'foreman/evidence/builds/{task_id}')
        
        # Check evidence directory exists
        if not evidence_dir.exists():
            return {
                'success': False,
                'errors': [f'Evidence directory not found: {evidence_dir}']
            }
        
        # Load evidence chain
        chain = self.load_evidence_chain(evidence_dir)
        
        if 'errors' in chain:
            return {
                'success': False,
                'errors': chain['errors']
            }
        
        # Replay states
        states = []
        current_state = {}
        
        # 1. Build initiation
        initiation = chain['build-initiation']
        current_state = {
            'task_id': task_id,
            'qa_status': initiation['qa_summary'],
            'stage': 'initiated'
        }
        states.append(current_state.copy())
        
        # 2. Validation
        validation = chain['validation-results']
        current_state['stage'] = 'validated'
        current_state['validation_decision'] = validation['decision']
        states.append(current_state.copy())
        
        # 3. Iterations
        for iteration in chain['iterations']:
            current_state['qa_status'] = iteration['qa_status_after']
            current_state['iteration'] = iteration['iteration_number']
            current_state['stage'] = 'building'
            states.append(current_state.copy())
        
        # 4. Final validation
        if 'final-validation' in chain:
            final = chain['final-validation']
            current_state['stage'] = 'completed'
            current_state['final_status'] = final['overall_status']
            states.append(current_state.copy())
        
        return {
            'success': True,
            'states': states,
            'final_state': current_state,
            'evidence_chain': chain
        }
    
    def load_evidence_chain(self, evidence_dir):
        """Load all evidence files for a build"""
        chain = {}
        errors = []
        
        # Required files
        required = ['build-initiation.json', 'validation-results.json']
        
        for filename in required:
            filepath = evidence_dir / filename
            if not filepath.exists():
                errors.append(f'Missing required evidence: {filename}')
            else:
                with open(filepath) as f:
                    evidence_type = filename.replace('.json', '')
                    chain[evidence_type] = json.load(f)
        
        # Load iterations
        iterations_dir = evidence_dir / 'iterations'
        if iterations_dir.exists():
            iteration_files = sorted(iterations_dir.glob('iteration-*.json'))
            chain['iterations'] = []
            for filepath in iteration_files:
                with open(filepath) as f:
                    chain['iterations'].append(json.load(f))
        
        # Load final validation (optional for incomplete builds)
        final_path = evidence_dir / 'final-validation.json'
        if final_path.exists():
            with open(final_path) as f:
                chain['final-validation'] = json.load(f)
        
        if errors:
            return {'errors': errors}
        else:
            return chain
```

---

## 6. Integration Points

### 6.1 Build Process Integration

**When:** Evidence is generated during build process

**Action:**
1. Evidence generator creates evidence object
2. Evidence object passed to Governance Gate
3. Gate validates evidence
4. If valid: Evidence written to file system
5. If invalid: Evidence rejected, errors returned to builder

### 6.2 Compliance Reporting Integration

**When:** Compliance reports are generated

**Action:**
1. Compliance engine queries evidence
2. Evidence must have passed Governance Gate
3. Compliance mappings extracted from evidence_metadata
4. Controls marked as satisfied based on evidence

### 6.3 Audit Integration

**When:** Auditor requests evidence

**Action:**
1. Audit Replay Engine loads evidence chain
2. Replays build process from evidence
3. Verifies final state matches recorded state
4. Reports any discrepancies

---

## 7. Error Handling

### 7.1 Validation Errors

**Format:**
```json
{
  "valid": false,
  "errors": [
    {
      "rule": "schema_conformance",
      "field": "evidence_metadata.immutable",
      "message": "Evidence metadata does not mark evidence as immutable",
      "severity": "MANDATORY"
    }
  ]
}
```

### 7.2 Rejection Actions

When evidence is rejected:
1. Log to governance memory with `evidence-rejection` tag
2. Return detailed errors to evidence generator
3. Do NOT write evidence to file system
4. Escalate if repeated rejections occur

---

## 8. Testing

### 8.1 Test Coverage Requirements

All validation rules must have:
- ✅ Test for valid evidence (should pass)
- ✅ Test for invalid evidence (should fail)
- ✅ Test for edge cases
- ✅ Test for error message clarity

### 8.2 Test Files

- `tests/wave0_minimum_red/test_evidence_schema_validation.py`
- `tests/wave0_minimum_red/test_evidence_integrity.py`

---

## 9. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-16 | Initial Governance Gate specification for Issue B3 |

---

## 10. References

- `foreman/evidence/EVIDENCE_SCHEMA_CANON.json` - Canonical schemas
- `foreman/evidence/TEST_EVIDENCE_CONTROL_MAPPING.md` - Evidence-control mappings
- `foreman/architecture/FOREMAN_EVIDENCE_ARCHITECTURE_v1.0.md` - Evidence architecture
- `BUILD_PHILOSOPHY.md` - Section XII: Evidence Requirements

---

*END OF GOVERNANCE GATE SPECIFICATION*
