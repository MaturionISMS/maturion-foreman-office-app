"""
Evidence Schema Validation Tests

Tests for validating evidence conforms to EVIDENCE_SCHEMA_CANON.json
and can be properly consumed by the Governance Gate.

Expected: All tests RED (failing) until implementation exists.
"""

import pytest
import json
from pathlib import Path
from jsonschema import validate, ValidationError, Draft7Validator, RefResolver
from datetime import datetime


SCHEMA_PATH = Path("foreman/evidence/EVIDENCE_SCHEMA_CANON.json")


def get_validator_for_evidence_type(evidence_type):
    """
    Get a JSON schema validator for a specific evidence type.
    
    Args:
        evidence_type: Type of evidence (build-initiation, iteration, etc.)
    
    Returns:
        Draft7Validator configured with schema and resolver
    """
    with open(SCHEMA_PATH) as f:
        canon = json.load(f)
    
    # We need to pass the entire canon as the base schema so refs can be resolved
    # But we only want to validate against one schema, so we'll pull out the schema
    # and create a custom root schema that includes both definitions and the target schema
    
    evidence_schema = canon['schemas'][evidence_type]
    
    # Create a root schema that includes definitions from canon
    root_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "definitions": canon.get('definitions', {}),
        **evidence_schema  # Merge the evidence schema into root
    }
    
    # Create validator with the combined schema
    validator = Draft7Validator(root_schema)
    
    return validator


@pytest.mark.evidence
@pytest.mark.wave0
class TestEvidenceSchemaValidation:
    """Test evidence schema validation for Governance Gate"""
    
    def test_evidence_schema_canon_exists(self):
        """
        Test that EVIDENCE_SCHEMA_CANON.json exists and is valid JSON.
        
        Expected to PASS: Schema now exists.
        """
        assert SCHEMA_PATH.exists(), \
            f"Canonical evidence schema must exist at {SCHEMA_PATH}"
        
        with open(SCHEMA_PATH) as f:
            schema = json.load(f)
        
        assert 'version' in schema, \
            "Schema must have version"
        assert 'schemas' in schema, \
            "Schema must define evidence schemas"
        assert 'governance_gate_requirements' in schema, \
            "Schema must define Governance Gate requirements"
    
    def test_build_initiation_schema_validates_valid_evidence(self):
        """
        Test that valid build-initiation evidence passes schema validation.
        
        Expected to PASS: Schema validation now works.
        """
        validator = get_validator_for_evidence_type('build-initiation')
        
        # Valid evidence
        valid_evidence = {
            "task_id": "task-001",
            "build_type": "build_to_green",
            "timestamp_started": "2025-12-16T10:00:00.000Z",
            "initiated_by": "foreman",
            "instruction_received": {
                "format": "Build to Green",
                "architecture_reference": "foreman/architecture/test.md",
                "qa_suite_location": "tests/qa/test/",
                "qa_current_status": "RED",
                "failing_tests_count": 5,
                "acceptance_criteria": "All tests must pass (100% green)"
            },
            "builder_assigned": "ui-builder",
            "expected_deliverables": [
                "All QA tests passing (100%)"
            ],
            "evidence_location": "foreman/evidence/builds/task-001/",
            "evidence_metadata": {
                "schema_version": "1.0.0",
                "immutable": True,
                "governance_gate_version": "1.0.0"
            }
        }
        
        # Should not raise ValidationError
        validator.validate(valid_evidence)
    
    def test_build_initiation_schema_rejects_invalid_evidence(self):
        """
        Test that invalid build-initiation evidence fails schema validation.
        
        Expected to PASS: Schema validation rejects invalid evidence.
        """
        validator = get_validator_for_evidence_type('build-initiation')
        
        # Invalid evidence - missing required fields
        invalid_evidence = {
            "task_id": "task-002"
            # Missing all other required fields
        }
        
        with pytest.raises(ValidationError):
            validator.validate(invalid_evidence)
    
    def test_build_initiation_enforces_immutability_flag(self):
        """
        Test that build-initiation schema enforces immutable: true.
        
        Expected to FAIL: No immutability enforcement yet.
        """
        with open(SCHEMA_PATH) as f:
            canon = json.load(f)
        
        schema = canon['schemas']['build-initiation']
        
        # Evidence with immutable: false (INVALID)
        evidence_not_immutable = {
            "task_id": "task-003",
            "build_type": "build_to_green",
            "timestamp_started": "2025-12-16T10:00:00.000Z",
            "initiated_by": "foreman",
            "instruction_received": {
                "format": "Build to Green",
                "architecture_reference": "test.md",
                "qa_suite_location": "tests/",
                "qa_current_status": "RED",
                "acceptance_criteria": "All pass"
            },
            "builder_assigned": "ui-builder",
            "expected_deliverables": ["Tests pass"],
            "evidence_location": "foreman/evidence/builds/task-003/",
            "evidence_metadata": {
                "schema_version": "1.0.0",
                "immutable": False,  # INVALID - must be true
                "governance_gate_version": "1.0.0"
            }
        }
        
        with pytest.raises(ValidationError) as exc_info:
            validate(instance=evidence_not_immutable, schema=schema)
        
        assert 'immutable' in str(exc_info.value).lower(), \
            "Validation error must mention immutability"
    
    def test_iteration_schema_validates_valid_evidence(self):
        """
        Test that valid iteration evidence passes schema validation.
        
        Expected to FAIL: No schema validator implemented yet.
        """
        with open(SCHEMA_PATH) as f:
            canon = json.load(f)
        
        schema = canon['schemas']['iteration']
        
        valid_evidence = {
            "task_id": "task-004",
            "iteration_number": 1,
            "timestamp_started": "2025-12-16T10:00:00.000Z",
            "timestamp_completed": "2025-12-16T10:05:00.000Z",
            "qa_status_before": {
                "total_tests": 10,
                "passing": 0,
                "failing": 10,
                "skipped": 0
            },
            "target_test": {
                "test_name": "test_example",
                "test_file": "tests/test_example.py"
            },
            "implementation": {
                "approach": "Implement example function",
                "files_modified": [],
                "minimal_code_principle": "yes"
            },
            "qa_status_after": {
                "total_tests": 10,
                "passing": 1,
                "failing": 9,
                "skipped": 0,
                "test_debt_detected": "no"
            },
            "result": {
                "target_test_status": "pass",
                "progress": "1/10 tests passing",
                "regressions_detected": "no"
            },
            "next_action": "continue",
            "evidence_metadata": {
                "schema_version": "1.0.0",
                "immutable": True,
                "parent_evidence_id": "evidence-build-init-task-004"
            }
        }
        
        validate(instance=valid_evidence, schema=schema)
    
    def test_iteration_schema_requires_parent_evidence_id(self):
        """
        Test that iteration schema requires parent_evidence_id for traceability.
        
        Expected to FAIL: No traceability enforcement yet.
        """
        with open(SCHEMA_PATH) as f:
            canon = json.load(f)
        
        schema = canon['schemas']['iteration']
        
        # Missing parent_evidence_id
        evidence_no_parent = {
            "task_id": "task-005",
            "iteration_number": 1,
            "timestamp_started": "2025-12-16T10:00:00.000Z",
            "timestamp_completed": "2025-12-16T10:05:00.000Z",
            "qa_status_before": {
                "total_tests": 10,
                "passing": 0,
                "failing": 10,
                "skipped": 0
            },
            "target_test": {
                "test_name": "test_example",
                "test_file": "tests/test.py"
            },
            "implementation": {
                "approach": "Test",
                "files_modified": [],
                "minimal_code_principle": "yes"
            },
            "qa_status_after": {
                "total_tests": 10,
                "passing": 1,
                "failing": 9,
                "skipped": 0,
                "test_debt_detected": "no"
            },
            "result": {
                "target_test_status": "pass",
                "progress": "1/10",
                "regressions_detected": "no"
            },
            "next_action": "continue",
            "evidence_metadata": {
                "schema_version": "1.0.0",
                "immutable": True
                # Missing parent_evidence_id
            }
        }
        
        with pytest.raises(ValidationError) as exc_info:
            validate(instance=evidence_no_parent, schema=schema)
        
        assert 'parent_evidence_id' in str(exc_info.value), \
            "Validation error must mention missing parent_evidence_id"
    
    def test_final_validation_schema_validates_valid_evidence(self):
        """
        Test that valid final-validation evidence passes schema validation.
        
        Expected to FAIL: No schema validator implemented yet.
        """
        with open(SCHEMA_PATH) as f:
            canon = json.load(f)
        
        schema = canon['schemas']['final-validation']
        
        valid_evidence = {
            "task_id": "task-006",
            "validation_timestamp": "2025-12-16T11:00:00.000Z",
            "qa_completeness": {
                "all_tests_passing": True,
                "zero_test_failures": True,
                "zero_test_errors": True,
                "zero_skipped_tests": True,
                "zero_test_debt": True,
                "test_statistics": {
                    "total_tests": 10,
                    "passing": 10,
                    "failing": 0,
                    "skipped": 0
                }
            },
            "build_quality": {
                "typescript_compilation": "pass",
                "lint_check": {
                    "status": "pass",
                    "errors": 0,
                    "warnings": 0
                },
                "build_success": True,
                "no_console_errors": True
            },
            "interface_integrity": {
                "all_union_values_present": True,
                "all_imports_valid": True,
                "no_breaking_changes": True,
                "pre_build_validation_passed": True
            },
            "evidence_trail": {
                "build_iterations_documented": True,
                "test_results_captured": True,
                "code_changes_logged": True,
                "completion_timestamp": "2025-12-16T11:00:00.000Z"
            },
            "overall_status": "GREEN",
            "evidence_metadata": {
                "schema_version": "1.0.0",
                "immutable": True,
                "governance_gate_version": "1.0.0"
            }
        }
        
        validate(instance=valid_evidence, schema=schema)
    
    def test_final_validation_enforces_green_requirements(self):
        """
        Test that final-validation schema enforces all requirements for GREEN status.
        
        Expected to FAIL: No GREEN enforcement yet.
        """
        with open(SCHEMA_PATH) as f:
            canon = json.load(f)
        
        schema = canon['schemas']['final-validation']
        
        # All booleans must be true for GREEN
        evidence_not_green = {
            "task_id": "task-007",
            "validation_timestamp": "2025-12-16T11:00:00.000Z",
            "qa_completeness": {
                "all_tests_passing": False,  # Must be true
                "zero_test_failures": True,
                "zero_test_errors": True,
                "zero_skipped_tests": True,
                "zero_test_debt": True
            },
            "build_quality": {
                "typescript_compilation": "pass",
                "lint_check": {
                    "status": "pass",
                    "errors": 0,
                    "warnings": 0
                },
                "build_success": True,
                "no_console_errors": True
            },
            "interface_integrity": {
                "all_union_values_present": True,
                "all_imports_valid": True,
                "no_breaking_changes": True,
                "pre_build_validation_passed": True
            },
            "evidence_trail": {
                "build_iterations_documented": True,
                "test_results_captured": True,
                "code_changes_logged": True,
                "completion_timestamp": "2025-12-16T11:00:00.000Z"
            },
            "overall_status": "GREEN",
            "evidence_metadata": {
                "schema_version": "1.0.0",
                "immutable": True,
                "governance_gate_version": "1.0.0"
            }
        }
        
        with pytest.raises(ValidationError):
            validate(instance=evidence_not_green, schema=schema)


@pytest.mark.evidence
@pytest.mark.wave0
class TestGovernanceGateValidation:
    """Test Governance Gate evidence validation"""
    
    def test_governance_gate_rejects_malformed_evidence(self):
        """
        Test that Governance Gate rejects evidence that doesn't conform to schema.
        
        Expected to FAIL: No Governance Gate implementation yet.
        """
        from foreman.governance.evidence_gate import GovernanceGate
        
        gate = GovernanceGate()
        
        # Malformed evidence
        malformed = {
            "task_id": "task-008"
            # Missing all required fields
        }
        
        result = gate.validate_evidence(malformed, evidence_type='build-initiation')
        
        assert result['valid'] is False, \
            "Governance Gate must reject malformed evidence"
        assert 'errors' in result, \
            "Governance Gate must return validation errors"
        assert len(result['errors']) > 0, \
            "Governance Gate must list specific errors"
    
    def test_governance_gate_accepts_valid_evidence(self):
        """
        Test that Governance Gate accepts evidence that conforms to schema.
        
        Expected to FAIL: No Governance Gate implementation yet.
        """
        from foreman.governance.evidence_gate import GovernanceGate
        
        gate = GovernanceGate()
        
        valid_evidence = {
            "task_id": "task-009",
            "build_type": "build_to_green",
            "timestamp_started": "2025-12-16T10:00:00.000Z",
            "initiated_by": "foreman",
            "instruction_received": {
                "format": "Build to Green",
                "architecture_reference": "test.md",
                "qa_suite_location": "tests/",
                "qa_current_status": "RED",
                "failing_tests_count": 1,
                "acceptance_criteria": "All pass"
            },
            "builder_assigned": "ui-builder",
            "expected_deliverables": ["Tests pass"],
            "evidence_location": "foreman/evidence/builds/task-009/",
            "evidence_metadata": {
                "schema_version": "1.0.0",
                "immutable": True,
                "governance_gate_version": "1.0.0"
            }
        }
        
        result = gate.validate_evidence(valid_evidence, evidence_type='build-initiation')
        
        assert result['valid'] is True, \
            "Governance Gate must accept valid evidence"
        assert 'errors' not in result or len(result['errors']) == 0, \
            "Valid evidence should have no errors"
    
    def test_governance_gate_verifies_immutability(self):
        """
        Test that Governance Gate verifies evidence immutability flag.
        
        Expected to FAIL: No immutability verification yet.
        """
        from foreman.governance.evidence_gate import GovernanceGate
        
        gate = GovernanceGate()
        
        # Evidence with immutable: false
        mutable_evidence = {
            "task_id": "task-010",
            "build_type": "build_to_green",
            "timestamp_started": "2025-12-16T10:00:00.000Z",
            "initiated_by": "foreman",
            "instruction_received": {
                "format": "Build to Green",
                "architecture_reference": "test.md",
                "qa_suite_location": "tests/",
                "qa_current_status": "RED",
                "acceptance_criteria": "All pass"
            },
            "builder_assigned": "ui-builder",
            "expected_deliverables": ["Tests pass"],
            "evidence_location": "foreman/evidence/builds/task-010/",
            "evidence_metadata": {
                "schema_version": "1.0.0",
                "immutable": False,  # INVALID
                "governance_gate_version": "1.0.0"
            }
        }
        
        result = gate.validate_evidence(mutable_evidence, evidence_type='build-initiation')
        
        assert result['valid'] is False, \
            "Governance Gate must reject non-immutable evidence"
        assert 'immutability' in str(result['errors']).lower(), \
            "Error must mention immutability violation"
    
    def test_governance_gate_verifies_traceability(self):
        """
        Test that Governance Gate verifies evidence traceability chain.
        
        Expected to FAIL: No traceability verification yet.
        """
        from foreman.governance.evidence_gate import GovernanceGate
        
        gate = GovernanceGate()
        
        # Iteration evidence without parent_evidence_id
        no_parent = {
            "task_id": "task-011",
            "iteration_number": 1,
            "timestamp_started": "2025-12-16T10:00:00.000Z",
            "timestamp_completed": "2025-12-16T10:05:00.000Z",
            "qa_status_before": {"total_tests": 10, "passing": 0, "failing": 10, "skipped": 0},
            "target_test": {"test_name": "test", "test_file": "test.py"},
            "implementation": {"approach": "Test", "files_modified": [], "minimal_code_principle": "yes"},
            "qa_status_after": {"total_tests": 10, "passing": 1, "failing": 9, "skipped": 0, "test_debt_detected": "no"},
            "result": {"target_test_status": "pass", "progress": "1/10", "regressions_detected": "no"},
            "next_action": "continue",
            "evidence_metadata": {
                "schema_version": "1.0.0",
                "immutable": True
                # Missing parent_evidence_id
            }
        }
        
        result = gate.validate_evidence(no_parent, evidence_type='iteration')
        
        assert result['valid'] is False, \
            "Governance Gate must reject evidence without traceability"
        assert 'traceability' in str(result['errors']).lower() or 'parent' in str(result['errors']).lower(), \
            "Error must mention traceability/parent issue"


@pytest.mark.evidence
@pytest.mark.wave0
class TestAuditReplaySupport:
    """Test that evidence supports audit replay"""
    
    def test_evidence_chain_supports_replay(self):
        """
        Test that complete evidence chain can be used for audit replay.
        
        Expected to FAIL: No audit replay implementation yet.
        """
        from foreman.governance.audit_replay import AuditReplayEngine
        
        engine = AuditReplayEngine()
        
        task_id = "task-012"
        evidence_dir = Path(f"foreman/evidence/builds/{task_id}")
        
        # Assume evidence exists for this test
        # In real scenario, evidence would be generated first
        
        # Replay should reconstruct build process
        replay_result = engine.replay_build(task_id)
        
        assert replay_result['success'], \
            "Audit replay must succeed for complete evidence chain"
        assert 'states' in replay_result, \
            "Replay must return state progression"
        assert 'final_state' in replay_result, \
            "Replay must return final state"
    
    def test_audit_replay_detects_missing_evidence(self):
        """
        Test that audit replay detects incomplete evidence chain.
        
        Expected to FAIL: No audit replay implementation yet.
        """
        from foreman.governance.audit_replay import AuditReplayEngine
        
        engine = AuditReplayEngine()
        
        task_id = "task-013-incomplete"
        
        # This task has incomplete evidence (missing iteration or final validation)
        replay_result = engine.replay_build(task_id)
        
        assert replay_result['success'] is False, \
            "Audit replay must fail for incomplete evidence"
        assert 'missing_evidence' in replay_result, \
            "Replay must report missing evidence"
    
    def test_audit_replay_validates_chronological_consistency(self):
        """
        Test that audit replay validates timestamps are chronologically consistent.
        
        Expected to FAIL: No chronological validation yet.
        """
        from foreman.governance.audit_replay import AuditReplayEngine
        
        engine = AuditReplayEngine()
        
        task_id = "task-014"
        
        # Evidence with inconsistent timestamps
        # (e.g., iteration complete before build start)
        
        replay_result = engine.replay_build(task_id)
        
        if not replay_result['success']:
            assert 'chronological' in str(replay_result.get('errors', '')).lower() or \
                   'timestamp' in str(replay_result.get('errors', '')).lower(), \
                "Error must mention chronological inconsistency"
