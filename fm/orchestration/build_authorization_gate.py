"""
Build Authorization Gate Validator

Implements the Build Authorization Gate validation logic as defined in:
governance/build/BUILD_AUTHORIZATION_GATE.md

This module validates all 8 mandatory preconditions before a build can proceed.
"""

import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional


class GateResult(Enum):
    """Binary gate resolution states"""
    PASS = "PASS"
    FAIL = "FAIL"


class PreconditionStatus(Enum):
    """Status of individual preconditions"""
    SATISFIED = "SATISFIED"
    FAILED = "FAILED"
    NOT_EVALUATED = "NOT_EVALUATED"


@dataclass
class PreconditionResult:
    """Result of a single precondition check"""
    name: str
    status: PreconditionStatus
    message: str
    evidence_paths: List[str]
    blocking_conditions: List[str]


@dataclass
class BuildAuthorizationResult:
    """Complete Build Authorization Gate validation result"""
    build_id: str
    gate_result: GateResult
    timestamp: str
    precondition_results: List[PreconditionResult]
    summary: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'build_id': self.build_id,
            'gate_result': self.gate_result.value,
            'timestamp': self.timestamp,
            'precondition_results': [
                {
                    'name': pr.name,
                    'status': pr.status.value,
                    'message': pr.message,
                    'evidence_paths': pr.evidence_paths,
                    'blocking_conditions': pr.blocking_conditions
                }
                for pr in self.precondition_results
            ],
            'summary': self.summary
        }


class BuildAuthorizationGate:
    """
    Build Authorization Gate validator
    
    Validates all 8 mandatory preconditions:
    1. App Description Exists and Is Authoritative
    2. Architecture Compilation Contract = PASS
    3. QA Derivation & Coverage Rules = PASS
    4. FL/CI Learning Integration = COMPLETE
    5. Deployment and Runtime Validation = COMPLETE
    6. Governance Checklist = PASS
    7. Scope Freeze = CONFIRMED
    8. Zero Test Debt = CONFIRMED
    """
    
    def __init__(self, repo_root: Optional[Path] = None):
        """
        Initialize the gate validator
        
        Args:
            repo_root: Root directory of the repository. Defaults to current directory.
        """
        self.repo_root = repo_root or Path.cwd()
    
    def validate(self, build_id: str) -> BuildAuthorizationResult:
        """
        Validate all preconditions for the given build
        
        Args:
            build_id: Unique identifier for the build
            
        Returns:
            BuildAuthorizationResult with PASS/FAIL determination
        """
        precondition_results = []
        
        # Validate all 8 preconditions
        precondition_results.append(self._validate_precondition_1(build_id))
        precondition_results.append(self._validate_precondition_2(build_id))
        precondition_results.append(self._validate_precondition_3(build_id))
        precondition_results.append(self._validate_precondition_4(build_id))
        precondition_results.append(self._validate_precondition_5(build_id))
        precondition_results.append(self._validate_precondition_6(build_id))
        precondition_results.append(self._validate_precondition_7(build_id))
        precondition_results.append(self._validate_precondition_8(build_id))
        
        # Determine gate result: ALL must be SATISFIED for PASS
        all_satisfied = all(
            pr.status == PreconditionStatus.SATISFIED
            for pr in precondition_results
        )
        
        gate_result = GateResult.PASS if all_satisfied else GateResult.FAIL
        
        # Generate summary
        satisfied_count = sum(
            1 for pr in precondition_results
            if pr.status == PreconditionStatus.SATISFIED
        )
        summary = (
            f"Build Authorization Gate: {gate_result.value}\n"
            f"Preconditions: {satisfied_count}/8 satisfied\n"
        )
        
        if gate_result == GateResult.FAIL:
            failed = [pr.name for pr in precondition_results
                     if pr.status == PreconditionStatus.FAILED]
            summary += f"Failed preconditions: {', '.join(failed)}"
        else:
            summary += "All preconditions satisfied. Build may proceed."
        
        return BuildAuthorizationResult(
            build_id=build_id,
            gate_result=gate_result,
            timestamp=datetime.utcnow().isoformat() + 'Z',
            precondition_results=precondition_results,
            summary=summary
        )
    
    def _validate_precondition_1(self, build_id: str) -> PreconditionResult:
        """Precondition 1: App Description Exists and Is Authoritative"""
        evidence_dir = self.repo_root / "architecture" / "builds" / build_id
        evidence_paths = []
        blocking_conditions = []
        
        # Check for app description validation evidence
        app_desc_validation = evidence_dir / "app-description-validation.md"
        if app_desc_validation.exists():
            evidence_paths.append(str(app_desc_validation))
        else:
            blocking_conditions.append("App Description validation evidence missing")
        
        # Check for FRS alignment checklist
        frs_alignment = evidence_dir / "app-description-frs-alignment-checklist-result.md"
        if frs_alignment.exists():
            evidence_paths.append(str(frs_alignment))
        else:
            blocking_conditions.append("App Description → FRS Alignment Checklist result missing")
        
        # Check main app description file
        app_desc_file = self.repo_root / "APP_DESCRIPTION.md"
        if app_desc_file.exists():
            content = app_desc_file.read_text()
            if "Authoritative" in content or "Approved" in content:
                evidence_paths.append(str(app_desc_file))
            else:
                blocking_conditions.append("App Description not marked as Authoritative")
        else:
            blocking_conditions.append("APP_DESCRIPTION.md not found")
        
        status = (PreconditionStatus.SATISFIED if not blocking_conditions
                 else PreconditionStatus.FAILED)
        
        return PreconditionResult(
            name="App Description Exists and Is Authoritative",
            status=status,
            message="App Description must exist, be authoritative, and be explicitly referenced by Requirements Specification",
            evidence_paths=evidence_paths,
            blocking_conditions=blocking_conditions
        )
    
    def _validate_precondition_2(self, build_id: str) -> PreconditionResult:
        """Precondition 2: Architecture Compilation Contract = PASS"""
        evidence_dir = self.repo_root / "architecture" / "builds" / build_id
        evidence_paths = []
        blocking_conditions = []
        
        validation_file = evidence_dir / "validation.md"
        if validation_file.exists():
            content = validation_file.read_text()
            if "PASS" in content:
                evidence_paths.append(str(validation_file))
            else:
                blocking_conditions.append("Architecture Compilation Contract did not resolve to PASS")
        else:
            blocking_conditions.append("Architecture validation evidence missing")
        
        flci_plan = evidence_dir / "flci-prevention-plan.md"
        if flci_plan.exists():
            evidence_paths.append(str(flci_plan))
        else:
            blocking_conditions.append("FL/CI prevention plan missing")
        
        status = (PreconditionStatus.SATISFIED if not blocking_conditions
                 else PreconditionStatus.FAILED)
        
        return PreconditionResult(
            name="Architecture Compilation Contract = PASS",
            status=status,
            message="Architecture must be complete, frozen, and validated",
            evidence_paths=evidence_paths,
            blocking_conditions=blocking_conditions
        )
    
    def _validate_precondition_3(self, build_id: str) -> PreconditionResult:
        """Precondition 3: QA Derivation & Coverage Rules = PASS"""
        evidence_dir = self.repo_root / "architecture" / "builds" / build_id / "qa-evidence"
        evidence_paths = []
        blocking_conditions = []
        
        coverage_report = evidence_dir / "coverage-report.md"
        if coverage_report.exists():
            content = coverage_report.read_text()
            if "100%" in content:
                evidence_paths.append(str(coverage_report))
            else:
                blocking_conditions.append("QA coverage < 100%")
        else:
            blocking_conditions.append("QA coverage report missing")
        
        test_execution = evidence_dir / "test-execution-report.md"
        if test_execution.exists():
            content = test_execution.read_text()
            if "GREEN" in content and "RED" not in content:
                evidence_paths.append(str(test_execution))
            else:
                blocking_conditions.append("Tests are not all GREEN")
        else:
            blocking_conditions.append("Test execution report missing")
        
        flci_coverage = self.repo_root / "architecture" / "builds" / build_id / "flci-coverage-report.md"
        if flci_coverage.exists():
            evidence_paths.append(str(flci_coverage))
        else:
            blocking_conditions.append("FL/CI coverage report missing")
        
        status = (PreconditionStatus.SATISFIED if not blocking_conditions
                 else PreconditionStatus.FAILED)
        
        return PreconditionResult(
            name="QA Derivation & Coverage Rules = PASS",
            status=status,
            message="QA must be fully derived, implemented, and GREEN",
            evidence_paths=evidence_paths,
            blocking_conditions=blocking_conditions
        )
    
    def _validate_precondition_4(self, build_id: str) -> PreconditionResult:
        """Precondition 4: FL/CI Learning Integration = COMPLETE"""
        evidence_dir = self.repo_root / "architecture" / "builds" / build_id
        evidence_paths = []
        blocking_conditions = []
        
        flci_plan = evidence_dir / "flci-prevention-plan.md"
        if flci_plan.exists():
            evidence_paths.append(str(flci_plan))
        else:
            blocking_conditions.append("FL/CI prevention plan missing")
        
        flci_coverage = evidence_dir / "flci-coverage-report.md"
        if flci_coverage.exists():
            evidence_paths.append(str(flci_coverage))
        else:
            blocking_conditions.append("FL/CI coverage report missing")
        
        # Check for non-testable risks documentation
        non_testable = evidence_dir / "non-testable-risks.md"
        if non_testable.exists():
            content = non_testable.read_text()
            if "risk acceptance" not in content.lower():
                blocking_conditions.append("Non-testable risks lack risk acceptance documentation")
            else:
                evidence_paths.append(str(non_testable))
        
        status = (PreconditionStatus.SATISFIED if not blocking_conditions
                 else PreconditionStatus.FAILED)
        
        return PreconditionResult(
            name="FL/CI Learning Integration = COMPLETE",
            status=status,
            message="All applicable historical failure classes must be addressed",
            evidence_paths=evidence_paths,
            blocking_conditions=blocking_conditions
        )
    
    def _validate_precondition_5(self, build_id: str) -> PreconditionResult:
        """Precondition 5: Deployment and Runtime Validation = COMPLETE"""
        evidence_dir = self.repo_root / "architecture" / "builds" / build_id
        evidence_paths = []
        blocking_conditions = []
        
        # Look for deployment validation evidence
        deployment_tests = evidence_dir / "deployment-test-results.md"
        deployment_risks = evidence_dir / "non-testable-deployment-risks.md"
        
        if not deployment_tests.exists() and not deployment_risks.exists():
            blocking_conditions.append("No deployment validation evidence found")
        else:
            if deployment_tests.exists():
                evidence_paths.append(str(deployment_tests))
            if deployment_risks.exists():
                evidence_paths.append(str(deployment_risks))
        
        # Check for migration validation if applicable
        migration_tests = evidence_dir / "migration-test-results.md"
        if migration_tests.exists():
            evidence_paths.append(str(migration_tests))
        
        # Check for environment compatibility matrix
        env_compat = evidence_dir / "environment-compatibility-matrix.md"
        if env_compat.exists():
            evidence_paths.append(str(env_compat))
        else:
            blocking_conditions.append("Environment compatibility matrix missing")
        
        status = (PreconditionStatus.SATISFIED if not blocking_conditions
                 else PreconditionStatus.FAILED)
        
        return PreconditionResult(
            name="Deployment and Runtime Validation = COMPLETE",
            status=status,
            message="Deployment and runtime behavior must be validated",
            evidence_paths=evidence_paths,
            blocking_conditions=blocking_conditions
        )
    
    def _validate_precondition_6(self, build_id: str) -> PreconditionResult:
        """Precondition 6: Governance Checklist = PASS"""
        evidence_dir = self.repo_root / "architecture" / "builds" / build_id
        evidence_paths = []
        blocking_conditions = []
        
        checklist_file = evidence_dir / "architecture-validation-checklist.md"
        if checklist_file.exists():
            content = checklist_file.read_text()
            # Look for completed checklist markers
            if "- [x]" in content.lower() or "- [✓]" in content:
                # Check for incomplete items
                if "- [ ]" in content:
                    blocking_conditions.append("Checklist contains incomplete items")
                else:
                    evidence_paths.append(str(checklist_file))
            else:
                blocking_conditions.append("Checklist not completed")
        else:
            blocking_conditions.append("Architecture Validation Checklist missing")
        
        status = (PreconditionStatus.SATISFIED if not blocking_conditions
                 else PreconditionStatus.FAILED)
        
        return PreconditionResult(
            name="Governance Checklist = PASS",
            status=status,
            message="All governance checklist items must be satisfied",
            evidence_paths=evidence_paths,
            blocking_conditions=blocking_conditions
        )
    
    def _validate_precondition_7(self, build_id: str) -> PreconditionResult:
        """Precondition 7: Scope Freeze = CONFIRMED"""
        evidence_dir = self.repo_root / "architecture" / "builds" / build_id
        evidence_paths = []
        blocking_conditions = []
        
        freeze_file = evidence_dir / "freeze-timestamp.txt"
        if freeze_file.exists():
            evidence_paths.append(str(freeze_file))
        else:
            blocking_conditions.append("Freeze timestamp missing")
        
        # Check for immutability markers in architecture artifacts
        arch_dir = self.repo_root / "architecture" / "builds" / build_id
        if arch_dir.exists():
            immutable_marker = arch_dir / "IMMUTABLE"
            if immutable_marker.exists():
                evidence_paths.append(str(immutable_marker))
            else:
                blocking_conditions.append("Architecture not marked immutable")
        else:
            blocking_conditions.append("Architecture artifacts directory not found")
        
        status = (PreconditionStatus.SATISFIED if not blocking_conditions
                 else PreconditionStatus.FAILED)
        
        return PreconditionResult(
            name="Scope Freeze = CONFIRMED",
            status=status,
            message="Architecture and requirements must be frozen",
            evidence_paths=evidence_paths,
            blocking_conditions=blocking_conditions
        )
    
    def _validate_precondition_8(self, build_id: str) -> PreconditionResult:
        """Precondition 8: Zero Test Debt = CONFIRMED"""
        evidence_dir = self.repo_root / "architecture" / "builds" / build_id
        evidence_paths = []
        blocking_conditions = []
        
        test_debt_report = evidence_dir / "test-debt-scan-report.md"
        if test_debt_report.exists():
            content = test_debt_report.read_text()
            if "ZERO" in content or "0 debt" in content:
                evidence_paths.append(str(test_debt_report))
            else:
                blocking_conditions.append("Test debt detected")
        else:
            blocking_conditions.append("Test debt scan report missing")
        
        status = (PreconditionStatus.SATISFIED if not blocking_conditions
                 else PreconditionStatus.FAILED)
        
        return PreconditionResult(
            name="Zero Test Debt = CONFIRMED",
            status=status,
            message="No test debt permitted",
            evidence_paths=evidence_paths,
            blocking_conditions=blocking_conditions
        )
    
    def generate_evidence_package(self, result: BuildAuthorizationResult) -> str:
        """
        Generate evidence package for build authorization
        
        Args:
            result: The authorization result to document
            
        Returns:
            Path to the generated evidence package directory
        """
        evidence_dir = (
            self.repo_root / "architecture" / "builds" / 
            result.build_id / "authorization-evidence"
        )
        evidence_dir.mkdir(parents=True, exist_ok=True)
        
        # Write gate validation report
        report_path = evidence_dir / "gate-validation-report.md"
        with open(report_path, 'w') as f:
            f.write(f"# Build Authorization Gate Validation Report\n\n")
            f.write(f"**Build ID**: {result.build_id}\n")
            f.write(f"**Timestamp**: {result.timestamp}\n")
            f.write(f"**Gate Result**: {result.gate_result.value}\n\n")
            f.write(f"## Summary\n\n{result.summary}\n\n")
            f.write(f"## Precondition Results\n\n")
            
            for i, pr in enumerate(result.precondition_results, 1):
                f.write(f"### {i}. {pr.name}\n\n")
                f.write(f"**Status**: {pr.status.value}\n\n")
                f.write(f"**Requirement**: {pr.message}\n\n")
                
                if pr.evidence_paths:
                    f.write(f"**Evidence**:\n")
                    for path in pr.evidence_paths:
                        f.write(f"- `{path}`\n")
                    f.write("\n")
                
                if pr.blocking_conditions:
                    f.write(f"**Blocking Conditions**:\n")
                    for condition in pr.blocking_conditions:
                        f.write(f"- {condition}\n")
                    f.write("\n")
        
        # Write authorization decision
        decision_path = evidence_dir / "authorization-decision.md"
        with open(decision_path, 'w') as f:
            f.write(f"# Build Authorization Decision\n\n")
            f.write(f"**Build ID**: {result.build_id}\n")
            f.write(f"**Decision**: {result.gate_result.value}\n")
            f.write(f"**Timestamp**: {result.timestamp}\n\n")
            f.write(f"## Justification\n\n{result.summary}\n\n")
            
            if result.gate_result == GateResult.PASS:
                # Write authorization timestamp
                timestamp_path = evidence_dir / "authorization-timestamp.txt"
                with open(timestamp_path, 'w') as ts:
                    ts.write(result.timestamp)
            else:
                # Write blocker report
                blocker_path = evidence_dir / "blocker-report.md"
                with open(blocker_path, 'w') as b:
                    b.write(f"# Build Authorization Blockers\n\n")
                    b.write(f"**Build ID**: {result.build_id}\n")
                    b.write(f"**Timestamp**: {result.timestamp}\n\n")
                    b.write(f"## Blocking Preconditions\n\n")
                    
                    for pr in result.precondition_results:
                        if pr.status == PreconditionStatus.FAILED:
                            b.write(f"### {pr.name}\n\n")
                            for condition in pr.blocking_conditions:
                                b.write(f"- {condition}\n")
                            b.write("\n")
        
        # Write JSON version for machine consumption
        json_path = evidence_dir / "gate-validation-result.json"
        with open(json_path, 'w') as f:
            json.dump(result.to_dict(), f, indent=2)
        
        return str(evidence_dir)
