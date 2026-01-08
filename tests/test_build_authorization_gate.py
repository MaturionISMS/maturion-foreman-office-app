"""
Tests for Build Authorization Gate

Tests the Build Authorization Gate validator logic including:
- Individual precondition validation
- Gate resolution (PASS/FAIL)
- Evidence package generation
"""

import pytest
import json
from pathlib import Path
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'fm' / 'orchestration'))

from build_authorization_gate import (
    BuildAuthorizationGate,
    BuildAuthorizationResult,
    GateResult,
    PreconditionStatus
)


@pytest.fixture
def temp_repo_structure(tmp_path):
    """Create a temporary repository structure for testing"""
    # Create base directories
    arch_dir = tmp_path / "architecture" / "builds" / "test-build-001"
    arch_dir.mkdir(parents=True)
    
    qa_dir = arch_dir / "qa-evidence"
    qa_dir.mkdir(parents=True)
    
    # Create APP_DESCRIPTION.md
    app_desc = tmp_path / "APP_DESCRIPTION.md"
    app_desc.write_text("# Test App\nStatus: Authoritative")
    
    return tmp_path


@pytest.fixture
def gate_validator(temp_repo_structure):
    """Create a BuildAuthorizationGate instance with temp repo"""
    return BuildAuthorizationGate(repo_root=temp_repo_structure)


class TestBuildAuthorizationGate:
    """Test suite for Build Authorization Gate"""
    
    def test_gate_initialization(self, gate_validator, temp_repo_structure):
        """Test that gate validator initializes correctly"""
        assert gate_validator.repo_root == temp_repo_structure
    
    def test_validate_precondition_1_pass(self, gate_validator, temp_repo_structure):
        """Test Precondition 1 passes with valid evidence"""
        build_id = "test-build-001"
        evidence_dir = temp_repo_structure / "architecture" / "builds" / build_id
        
        # Create required evidence
        (evidence_dir / "app-description-validation.md").write_text("Validated")
        (evidence_dir / "app-description-frs-alignment-checklist-result.md").write_text("PASS")
        
        result = gate_validator._validate_precondition_1(build_id)
        
        assert result.status == PreconditionStatus.SATISFIED
        assert len(result.evidence_paths) >= 2
        assert len(result.blocking_conditions) == 0
    
    def test_validate_precondition_1_fail_missing_evidence(self, gate_validator):
        """Test Precondition 1 fails with missing evidence"""
        build_id = "test-build-001"
        
        result = gate_validator._validate_precondition_1(build_id)
        
        assert result.status == PreconditionStatus.FAILED
        assert len(result.blocking_conditions) > 0
        assert any("missing" in bc.lower() for bc in result.blocking_conditions)
    
    def test_validate_precondition_2_pass(self, gate_validator, temp_repo_structure):
        """Test Precondition 2 passes with valid evidence"""
        build_id = "test-build-001"
        evidence_dir = temp_repo_structure / "architecture" / "builds" / build_id
        
        (evidence_dir / "validation.md").write_text("Architecture Compilation: PASS")
        (evidence_dir / "flci-prevention-plan.md").write_text("FL/CI Prevention Plan")
        
        result = gate_validator._validate_precondition_2(build_id)
        
        assert result.status == PreconditionStatus.SATISFIED
        assert len(result.evidence_paths) == 2
    
    def test_validate_precondition_3_pass(self, gate_validator, temp_repo_structure):
        """Test Precondition 3 passes with full QA coverage"""
        build_id = "test-build-001"
        qa_dir = temp_repo_structure / "architecture" / "builds" / build_id / "qa-evidence"
        
        (qa_dir / "coverage-report.md").write_text("Coverage: 100%")
        (qa_dir / "test-execution-report.md").write_text("All tests: GREEN")
        
        flci_dir = temp_repo_structure / "architecture" / "builds" / build_id
        (flci_dir / "flci-coverage-report.md").write_text("FL/CI Coverage Complete")
        
        result = gate_validator._validate_precondition_3(build_id)
        
        assert result.status == PreconditionStatus.SATISFIED
        assert len(result.evidence_paths) == 3
    
    def test_validate_precondition_8_pass(self, gate_validator, temp_repo_structure):
        """Test Precondition 8 passes with zero test debt"""
        build_id = "test-build-001"
        evidence_dir = temp_repo_structure / "architecture" / "builds" / build_id
        
        (evidence_dir / "test-debt-scan-report.md").write_text("Test Debt: ZERO")
        
        result = gate_validator._validate_precondition_8(build_id)
        
        assert result.status == PreconditionStatus.SATISFIED
        assert len(result.blocking_conditions) == 0
    
    def test_validate_precondition_8_fail_with_debt(self, gate_validator, temp_repo_structure):
        """Test Precondition 8 fails when test debt exists"""
        build_id = "test-build-001"
        evidence_dir = temp_repo_structure / "architecture" / "builds" / build_id
        
        (evidence_dir / "test-debt-scan-report.md").write_text("Test Debt: 5 skipped tests")
        
        result = gate_validator._validate_precondition_8(build_id)
        
        assert result.status == PreconditionStatus.FAILED
        assert "Test debt detected" in result.blocking_conditions
    
    def test_validate_all_preconditions_fail(self, gate_validator):
        """Test complete validation fails when preconditions not met"""
        build_id = "test-build-001"
        
        result = gate_validator.validate(build_id)
        
        assert result.gate_result == GateResult.FAIL
        assert result.build_id == build_id
        assert len(result.precondition_results) == 8
        assert all(pr.status == PreconditionStatus.FAILED for pr in result.precondition_results)
    
    def test_validate_all_preconditions_pass(self, gate_validator, temp_repo_structure):
        """Test complete validation passes when all preconditions met"""
        build_id = "test-build-001"
        evidence_dir = temp_repo_structure / "architecture" / "builds" / build_id
        qa_dir = evidence_dir / "qa-evidence"
        
        # Create all required evidence for all preconditions
        (evidence_dir / "app-description-validation.md").write_text("Valid")
        (evidence_dir / "app-description-frs-alignment-checklist-result.md").write_text("PASS")
        (evidence_dir / "validation.md").write_text("PASS")
        (evidence_dir / "flci-prevention-plan.md").write_text("Complete")
        (qa_dir / "coverage-report.md").write_text("100%")
        (qa_dir / "test-execution-report.md").write_text("GREEN")
        (evidence_dir / "flci-coverage-report.md").write_text("Complete")
        (evidence_dir / "environment-compatibility-matrix.md").write_text("Valid")
        (evidence_dir / "deployment-test-results.md").write_text("Valid")
        (evidence_dir / "architecture-validation-checklist.md").write_text("- [x] All items")
        (evidence_dir / "freeze-timestamp.txt").write_text(datetime.now(UTC).isoformat())
        (evidence_dir / "IMMUTABLE").write_text("")
        (evidence_dir / "test-debt-scan-report.md").write_text("ZERO")
        
        result = gate_validator.validate(build_id)
        
        assert result.gate_result == GateResult.PASS
        assert result.build_id == build_id
        assert len(result.precondition_results) == 8
        assert all(pr.status == PreconditionStatus.SATISFIED for pr in result.precondition_results)
    
    def test_generate_evidence_package(self, gate_validator, temp_repo_structure):
        """Test evidence package generation"""
        build_id = "test-build-001"
        
        result = gate_validator.validate(build_id)
        evidence_path = gate_validator.generate_evidence_package(result)
        
        evidence_dir = Path(evidence_path)
        assert evidence_dir.exists()
        assert (evidence_dir / "gate-validation-report.md").exists()
        assert (evidence_dir / "authorization-decision.md").exists()
        assert (evidence_dir / "gate-validation-result.json").exists()
        
        # Check JSON structure
        with open(evidence_dir / "gate-validation-result.json") as f:
            json_data = json.load(f)
        
        assert json_data['build_id'] == build_id
        assert json_data['gate_result'] in ['PASS', 'FAIL']
        assert 'precondition_results' in json_data
        assert len(json_data['precondition_results']) == 8
    
    def test_to_dict_conversion(self, gate_validator):
        """Test BuildAuthorizationResult to_dict conversion"""
        build_id = "test-build-001"
        result = gate_validator.validate(build_id)
        
        result_dict = result.to_dict()
        
        assert isinstance(result_dict, dict)
        assert result_dict['build_id'] == build_id
        assert 'gate_result' in result_dict
        assert 'timestamp' in result_dict
        assert 'precondition_results' in result_dict
        assert isinstance(result_dict['precondition_results'], list)


class TestGateResolution:
    """Test gate resolution logic"""
    
    def test_gate_fails_with_one_failed_precondition(self, gate_validator, temp_repo_structure):
        """Test that gate fails if even one precondition fails"""
        build_id = "test-build-001"
        evidence_dir = temp_repo_structure / "architecture" / "builds" / build_id
        qa_dir = evidence_dir / "qa-evidence"
        
        # Create evidence for 7 preconditions (missing one)
        (evidence_dir / "app-description-validation.md").write_text("Valid")
        (evidence_dir / "app-description-frs-alignment-checklist-result.md").write_text("PASS")
        (evidence_dir / "validation.md").write_text("PASS")
        (evidence_dir / "flci-prevention-plan.md").write_text("Complete")
        (qa_dir / "coverage-report.md").write_text("100%")
        (qa_dir / "test-execution-report.md").write_text("GREEN")
        (evidence_dir / "flci-coverage-report.md").write_text("Complete")
        (evidence_dir / "environment-compatibility-matrix.md").write_text("Valid")
        (evidence_dir / "deployment-test-results.md").write_text("Valid")
        (evidence_dir / "architecture-validation-checklist.md").write_text("- [x] All")
        (evidence_dir / "freeze-timestamp.txt").write_text(datetime.now(UTC).isoformat())
        (evidence_dir / "IMMUTABLE").write_text("")
        # Missing test-debt-scan-report.md - this should cause failure
        
        result = gate_validator.validate(build_id)
        
        assert result.gate_result == GateResult.FAIL
        failed_preconditions = [pr for pr in result.precondition_results
                               if pr.status == PreconditionStatus.FAILED]
        assert len(failed_preconditions) >= 1
    
    def test_gate_summary_format(self, gate_validator):
        """Test that gate summary is properly formatted"""
        build_id = "test-build-001"
        result = gate_validator.validate(build_id)
        
        assert result.summary is not None
        assert build_id in result.summary or "Build Authorization Gate" in result.summary
        assert result.gate_result.value in result.summary


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
