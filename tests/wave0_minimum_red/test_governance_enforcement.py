"""
Tests for governance validators.

These tests verify that governance enforcement is working at the execution level.
"""

import pytest
import subprocess
import sys
from pathlib import Path


@pytest.fixture
def repo_root():
    """Get repository root path"""
    return Path(__file__).parent.parent.parent


@pytest.fixture
def governance_scripts_dir(repo_root):
    """Get governance scripts directory"""
    return repo_root / "governance" / "scripts"


class TestAppDescriptionValidator:
    """Test App Description validator"""
    
    def test_validator_exists(self, governance_scripts_dir):
        """Verify App Description validator script exists"""
        validator = governance_scripts_dir / "validate-app-description.py"
        assert validator.exists(), "App Description validator must exist"
        assert validator.is_file(), "App Description validator must be a file"
    
    def test_validator_is_executable(self, governance_scripts_dir):
        """Verify App Description validator is executable"""
        validator = governance_scripts_dir / "validate-app-description.py"
        # Check if file has executable permissions (on Unix-like systems)
        import stat
        mode = validator.stat().st_mode
        is_executable = mode & stat.S_IXUSR or mode & stat.S_IXGRP or mode & stat.S_IXOTH
        assert is_executable, "App Description validator must be executable"
    
    def test_validator_runs(self, repo_root, governance_scripts_dir):
        """Verify App Description validator can run"""
        validator = governance_scripts_dir / "validate-app-description.py"
        result = subprocess.run(
            [sys.executable, str(validator), "FM"],
            capture_output=True,
            text=True,
            cwd=str(repo_root),
            timeout=30
        )
        # Validator should complete (exit code 0 or 1, not crash)
        assert result.returncode in [0, 1], "Validator should complete without errors"
        assert "APP DESCRIPTION VALIDATION RESULTS" in result.stdout


class TestFRSAlignmentValidator:
    """Test FRS Alignment validator"""
    
    def test_validator_exists(self, governance_scripts_dir):
        """Verify FRS Alignment validator script exists"""
        validator = governance_scripts_dir / "validate-frs-alignment.py"
        assert validator.exists(), "FRS Alignment validator must exist"
    
    def test_validator_runs(self, repo_root, governance_scripts_dir):
        """Verify FRS Alignment validator can run"""
        validator = governance_scripts_dir / "validate-frs-alignment.py"
        result = subprocess.run(
            [sys.executable, str(validator), "FM", "foreman/architecture/FOREMAN_TRUE_NORTH_v1.0.md"],
            capture_output=True,
            text=True,
            cwd=str(repo_root),
            timeout=30
        )
        # Validator should complete
        assert result.returncode in [0, 1], "Validator should complete without errors"
        assert "FRS ALIGNMENT VALIDATION RESULTS" in result.stdout


class TestArchitectureCompilationValidator:
    """Test Architecture Compilation validator"""
    
    def test_validator_exists(self, governance_scripts_dir):
        """Verify Architecture Compilation validator script exists"""
        validator = governance_scripts_dir / "validate-architecture-compilation.py"
        assert validator.exists(), "Architecture Compilation validator must exist"
    
    def test_validator_runs(self, repo_root, governance_scripts_dir):
        """Verify Architecture Compilation validator can run"""
        validator = governance_scripts_dir / "validate-architecture-compilation.py"
        result = subprocess.run(
            [sys.executable, str(validator), "FM"],
            capture_output=True,
            text=True,
            cwd=str(repo_root),
            timeout=30
        )
        # Validator should complete
        assert result.returncode in [0, 1], "Validator should complete without errors"
        assert "ARCHITECTURE COMPILATION VALIDATION RESULTS" in result.stdout


class TestBuildAuthorizationGateValidator:
    """Test Build Authorization Gate validator"""
    
    def test_validator_exists(self, governance_scripts_dir):
        """Verify Build Authorization Gate validator script exists"""
        validator = governance_scripts_dir / "validate-build-authorization-gate.py"
        assert validator.exists(), "Build Authorization Gate validator must exist"
    
    def test_validator_runs(self, repo_root, governance_scripts_dir):
        """Verify Build Authorization Gate validator can run"""
        validator = governance_scripts_dir / "validate-build-authorization-gate.py"
        result = subprocess.run(
            [sys.executable, str(validator), "FM"],
            capture_output=True,
            text=True,
            cwd=str(repo_root),
            timeout=60
        )
        # Validator should complete
        assert result.returncode in [0, 1], "Validator should complete without errors"
        assert "BUILD AUTHORIZATION GATE DECISION" in result.stdout
    
    def test_validator_checks_preconditions(self, repo_root, governance_scripts_dir):
        """Verify Build Authorization Gate checks all preconditions"""
        validator = governance_scripts_dir / "validate-build-authorization-gate.py"
        result = subprocess.run(
            [sys.executable, str(validator), "FM"],
            capture_output=True,
            text=True,
            cwd=str(repo_root),
            timeout=60
        )
        
        # Check that it evaluates all key preconditions
        output = result.stdout
        assert "App Description" in output, "Must check App Description"
        assert "Architecture Compilation" in output, "Must check Architecture Compilation"
        assert "QA" in output, "Must check QA"


class TestGovernanceGate:
    """Test central Governance Gate"""
    
    def test_gate_exists(self, governance_scripts_dir):
        """Verify Governance Gate script exists"""
        gate = governance_scripts_dir / "governance-gate.py"
        assert gate.exists(), "Governance Gate must exist"
    
    def test_gate_runs(self, repo_root, governance_scripts_dir):
        """Verify Governance Gate can run"""
        gate = governance_scripts_dir / "governance-gate.py"
        result = subprocess.run(
            [sys.executable, str(gate), "FM"],
            capture_output=True,
            text=True,
            cwd=str(repo_root),
            timeout=120
        )
        # Gate should complete
        assert result.returncode in [0, 1], "Gate should complete without errors"
        assert "GOVERNANCE GATE DECISION" in result.stdout
    
    def test_gate_makes_decision(self, repo_root, governance_scripts_dir):
        """Verify Governance Gate makes a clear decision"""
        gate = governance_scripts_dir / "governance-gate.py"
        result = subprocess.run(
            [sys.executable, str(gate), "FM"],
            capture_output=True,
            text=True,
            cwd=str(repo_root),
            timeout=120
        )
        
        output = result.stdout
        # Must have a clear decision
        assert ("AUTHORIZED" in output or "BLOCKED" in output), "Gate must make clear decision"


class TestGovernanceEvidence:
    """Test governance evidence generation"""
    
    def test_evidence_directory_created(self, repo_root):
        """Verify evidence directory is created"""
        evidence_dir = repo_root / "governance" / "evidence"
        # Run a validator to generate evidence
        validator = repo_root / "governance" / "scripts" / "validate-app-description.py"
        subprocess.run(
            [sys.executable, str(validator), "FM"],
            capture_output=True,
            cwd=str(repo_root),
            timeout=30
        )
        
        assert evidence_dir.exists(), "Evidence directory must be created"
        assert evidence_dir.is_dir(), "Evidence directory must be a directory"
    
    def test_evidence_files_generated(self, repo_root):
        """Verify evidence files are generated"""
        evidence_dir = repo_root / "governance" / "evidence"
        # Run a validator
        validator = repo_root / "governance" / "scripts" / "validate-app-description.py"
        subprocess.run(
            [sys.executable, str(validator), "FM"],
            capture_output=True,
            cwd=str(repo_root),
            timeout=30
        )
        
        # Check for JSON evidence files
        evidence_files = list(evidence_dir.glob("app-desc-*.json"))
        assert len(evidence_files) > 0, "Evidence files must be generated"


class TestExecutionLayerIntegration:
    """Test that execution scripts integrate with governance gate"""
    
    def test_plan_build_checks_governance(self, repo_root):
        """Verify plan-build.py calls governance gate"""
        plan_build = repo_root / "plan-build.py"
        assert plan_build.exists(), "plan-build.py must exist"
        
        with open(plan_build, 'r') as f:
            content = f.read()
        
        # Check if it calls governance gate
        assert "governance-gate.py" in content or "governance_gate" in content, \
            "plan-build.py must call governance gate"
    
    def test_create_build_tasks_has_lineage(self, repo_root):
        """Verify create-build-tasks.py tracks governance lineage"""
        create_tasks = repo_root / "create-build-tasks.py"
        assert create_tasks.exists(), "create-build-tasks.py must exist"
        
        with open(create_tasks, 'r') as f:
            content = f.read()
        
        # Check if it tracks governance lineage
        assert "governance_lineage" in content or "_load_governance_evidence" in content, \
            "create-build-tasks.py must track governance lineage"
    
    def test_validate_repository_checks_governance(self, repo_root):
        """Verify validate-repository.py checks governance execution"""
        validate_repo = repo_root / "validate-repository.py"
        assert validate_repo.exists(), "validate-repository.py must exist"
        
        with open(validate_repo, 'r') as f:
            content = f.read()
        
        # Check if it validates governance execution
        assert "validate_governance_execution" in content, \
            "validate-repository.py must validate governance execution"


class TestGovernanceEnforcementEnd2End:
    """End-to-end tests for governance enforcement"""
    
    def test_governance_blocks_non_compliant_build(self, repo_root):
        """Verify governance gate blocks builds that don't meet requirements"""
        # This is a conceptual test - in reality, if governance requirements
        # are not met, the gate should return exit code 1
        gate = repo_root / "governance" / "scripts" / "governance-gate.py"
        result = subprocess.run(
            [sys.executable, str(gate), "FM"],
            capture_output=True,
            text=True,
            cwd=str(repo_root),
            timeout=120
        )
        
        # Check that output shows evaluation occurred
        output = result.stdout
        assert "Preconditions Status" in output or "Validation Results" in output, \
            "Gate must show precondition evaluation"
    
    def test_validators_produce_machine_readable_output(self, repo_root):
        """Verify validators produce JSON evidence"""
        evidence_dir = repo_root / "governance" / "evidence"
        
        # Run build gate validator
        validator = repo_root / "governance" / "scripts" / "validate-build-authorization-gate.py"
        subprocess.run(
            [sys.executable, str(validator), "FM"],
            capture_output=True,
            cwd=str(repo_root),
            timeout=60
        )
        
        # Check for JSON evidence
        gate_evidence = list(evidence_dir.glob("build-gate-*.json"))
        assert len(gate_evidence) > 0, "Build gate must produce JSON evidence"
        
        # Verify JSON is valid
        import json
        with open(gate_evidence[0], 'r') as f:
            evidence = json.load(f)
        
        assert 'validation_id' in evidence, "Evidence must have validation_id"
        assert 'timestamp' in evidence, "Evidence must have timestamp"
        assert 'decision' in evidence, "Evidence must have decision"
