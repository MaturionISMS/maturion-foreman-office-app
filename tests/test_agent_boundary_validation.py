#!/usr/bin/env python3
"""
Comprehensive Test Suite for Agent QA Boundary Validation

Tests all valid and invalid QA report scenarios to ensure
the agent boundary enforcement is working correctly.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, Tuple

def run_validation(report_path: str, repo: str) -> Tuple[int, str]:
    """
    Run the validation script and return exit code and output.
    
    Returns:
        Tuple of (exit_code, output)
    """
    cmd = [
        'python3',
        'governance/scripts/validate_agent_boundaries.py',
        '--reports', report_path,
        '--current-repo', repo
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return -1, "Validation timed out"
    except Exception as e:
        return -2, f"Validation error: {e}"


def test_valid_builder_qa():
    """Test valid builder QA report"""
    print("Testing valid builder QA report...")
    
    report = {
        "qa_report_metadata": {
            "agent_type": "builder",
            "agent_id": "ui-builder",
            "agent_version": "1.0.0",
            "scope": "builder-qa",
            "repository": "MaturionISMS/isms-test-module",
            "timestamp": "2025-12-31T07:00:00Z"
        },
        "report_type": "BUILDER_QA_REPORT",
        "agent_id": "ui-builder",
        "timestamp": "2025-12-31T07:00:00Z",
        "qa_status": "READY",
        "evidence_chain": ["tests/ui/test-results.json"],
        "test_summary": {
            "total": 10,
            "passed": 10,
            "failed": 0,
            "skipped": 0
        },
        "gate_compliance": {
            "agent_boundary": "COMPLIANT",
            "architecture": "COMPLIANT",
            "governance": "COMPLIANT",
            "build_to_green": "COMPLIANT"
        },
        "immutable": True,
        "qa_details": {
            "test_framework": "jest",
            "coverage_percentage": 95.0,
            "test_duration_seconds": 30.5
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='-qa-report.json', delete=False) as f:
        json.dump(report, f)
        f.flush()
        exit_code, output = run_validation(f.name, "MaturionISMS/isms-test-module")
        Path(f.name).unlink()
    
    if exit_code == 0 and "ALL AGENT BOUNDARIES RESPECTED" in output:
        print("  ✅ PASS: Valid builder QA report accepted")
        assert True
    else:
        print(f"  ❌ FAIL: Valid builder QA report rejected (exit code: {exit_code})")
        print(f"  Output: {output}")
        assert False, "Valid builder QA report was rejected"


def test_valid_fm_qa():
    """Test valid FM QA report"""
    print("Testing valid FM QA report...")
    
    report = {
        "qa_report_metadata": {
            "agent_type": "fm",
            "agent_id": "fm-builder",
            "agent_version": "1.0.0",
            "scope": "fm-qa",
            "repository": "maturion-foreman-office-app",
            "timestamp": "2025-12-31T07:00:00Z"
        },
        "report_type": "FM_QA_REPORT",
        "agent_id": "fm-builder",
        "timestamp": "2025-12-31T07:00:00Z",
        "qa_status": "READY",
        "evidence_chain": ["tests/fm/orchestration-results.json"],
        "test_summary": {
            "total": 20,
            "passed": 20,
            "failed": 0,
            "skipped": 0
        },
        "gate_compliance": {
            "agent_boundary": "COMPLIANT",
            "architecture": "COMPLIANT",
            "governance": "COMPLIANT",
            "orchestration": "COMPLIANT"
        },
        "immutable": True,
        "fm_specific": {
            "orchestration_tests": 8,
            "dashboard_tests": 5,
            "enforcement_tests": 4,
            "integration_tests": 3
        },
        "qa_details": {
            "test_framework": "pytest",
            "coverage_percentage": 92.0,
            "test_duration_seconds": 45.2
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='-qa-report.json', delete=False) as f:
        json.dump(report, f)
        f.flush()
        exit_code, output = run_validation(f.name, "MaturionISMS/maturion-foreman-office-app")
        Path(f.name).unlink()
    
    if exit_code == 0 and "ALL AGENT BOUNDARIES RESPECTED" in output:
        print("  ✅ PASS: Valid FM QA report accepted")
        assert True
    else:
        print(f"  ❌ FAIL: Valid FM QA report rejected (exit code: {exit_code})")
        print(f"  Output: {output}")
        assert False, "Valid FM QA report was rejected"


def test_valid_governance_qa():
    """Test valid Governance QA report"""
    print("Testing valid Governance QA report...")
    
    report = {
        "qa_report_metadata": {
            "agent_type": "governance",
            "agent_id": "governance-administrator",
            "agent_version": "1.0.0",
            "scope": "governance-qa",
            "repository": "maturion-foreman-governance",
            "timestamp": "2025-12-31T07:00:00Z"
        },
        "report_type": "GOVERNANCE_QA_REPORT",
        "agent_id": "governance-administrator",
        "timestamp": "2025-12-31T07:00:00Z",
        "qa_status": "READY",
        "evidence_chain": ["governance/compliance-check-results.json"],
        "compliance_summary": {
            "total_checks": 15,
            "passed": 15,
            "failed": 0,
            "warnings": 0
        },
        "gate_compliance": {
            "agent_boundary": "COMPLIANT",
            "canonical_alignment": "COMPLIANT",
            "governance_rules": "COMPLIANT",
            "constitutional_compliance": "COMPLIANT"
        },
        "immutable": True,
        "governance_specific": {
            "policy_violations": [],
            "constitutional_violations": [],
            "canonical_drift_detected": False,
            "governance_artifacts_validated": 25
        },
        "qa_details": {
            "validation_framework": "governance-validator",
            "validation_duration_seconds": 60.5
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='-qa-report.json', delete=False) as f:
        json.dump(report, f)
        f.flush()
        exit_code, output = run_validation(f.name, "MaturionISMS/maturion-foreman-governance")
        Path(f.name).unlink()
    
    if exit_code == 0 and "ALL AGENT BOUNDARIES RESPECTED" in output:
        print("  ✅ PASS: Valid Governance QA report accepted")
        assert True
    else:
        print(f"  ❌ FAIL: Valid Governance QA report rejected (exit code: {exit_code})")
        print(f"  Output: {output}")
        assert False, "Valid Governance QA report was rejected"


def test_cross_agent_violation_builder_to_governance():
    """Test violation: Builder agent executing Governance QA"""
    print("Testing violation: Builder executing Governance QA...")
    
    report = {
        "qa_report_metadata": {
            "agent_type": "builder",
            "agent_id": "ui-builder",
            "agent_version": "1.0.0",
            "scope": "governance-qa",  # VIOLATION: Builder executing Governance QA
            "repository": "MaturionISMS/isms-test-module",
            "timestamp": "2025-12-31T07:00:00Z"
        },
        "report_type": "GOVERNANCE_QA_REPORT",
        "agent_id": "ui-builder",
        "timestamp": "2025-12-31T07:00:00Z",
        "qa_status": "READY",
        "evidence_chain": ["fake"],
        "compliance_summary": {
            "total_checks": 5,
            "passed": 5,
            "failed": 0,
            "warnings": 0
        },
        "gate_compliance": {
            "agent_boundary": "COMPLIANT",
            "canonical_alignment": "COMPLIANT",
            "governance_rules": "COMPLIANT"
        },
        "immutable": True
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='-qa-report.json', delete=False) as f:
        json.dump(report, f)
        f.flush()
        exit_code, output = run_validation(f.name, "MaturionISMS/isms-test-module")
        Path(f.name).unlink()
    
    if exit_code == 1 and "CROSS_AGENT_QA_EXECUTION" in output and "CATASTROPHIC" in output:
        print("  ✅ PASS: Violation correctly detected and blocked")
        assert True
    else:
        print(f"  ❌ FAIL: Violation not detected (exit code: {exit_code})")
        print(f"  Output: {output}")
        assert False, "Builder→Governance violation was not detected"


def test_cross_agent_violation_fm_to_builder():
    """Test violation: FM agent executing Builder QA"""
    print("Testing violation: FM executing Builder QA...")
    
    report = {
        "qa_report_metadata": {
            "agent_type": "fm",
            "agent_id": "fm-builder",
            "agent_version": "1.0.0",
            "scope": "builder-qa",  # VIOLATION: FM executing Builder QA
            "repository": "maturion-foreman-office-app",
            "timestamp": "2025-12-31T07:00:00Z"
        },
        "report_type": "BUILDER_QA_REPORT",
        "agent_id": "fm-builder",
        "timestamp": "2025-12-31T07:00:00Z",
        "qa_status": "READY",
        "evidence_chain": ["fake"],
        "test_summary": {
            "total": 10,
            "passed": 10,
            "failed": 0,
            "skipped": 0
        },
        "gate_compliance": {
            "agent_boundary": "COMPLIANT",
            "architecture": "COMPLIANT",
            "governance": "COMPLIANT"
        },
        "immutable": True
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='-qa-report.json', delete=False) as f:
        json.dump(report, f)
        f.flush()
        exit_code, output = run_validation(f.name, "MaturionISMS/maturion-foreman-office-app")
        Path(f.name).unlink()
    
    if exit_code == 1 and "CROSS_AGENT_QA_EXECUTION" in output and "CATASTROPHIC" in output:
        print("  ✅ PASS: Violation correctly detected and blocked")
        assert True
    else:
        print(f"  ❌ FAIL: Violation not detected (exit code: {exit_code})")
        print(f"  Output: {output}")
        assert False, "FM→Builder violation was not detected"


def test_missing_metadata():
    """Test missing qa_report_metadata section"""
    print("Testing missing qa_report_metadata...")
    
    report = {
        "report_type": "BUILDER_QA_REPORT",
        "agent_id": "ui-builder",
        "timestamp": "2025-12-31T07:00:00Z",
        "qa_status": "READY",
        "evidence_chain": ["fake"],
        "test_summary": {
            "total": 10,
            "passed": 10,
            "failed": 0,
            "skipped": 0
        },
        "gate_compliance": {
            "agent_boundary": "COMPLIANT",
            "architecture": "COMPLIANT",
            "governance": "COMPLIANT"
        },
        "immutable": True
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='-qa-report.json', delete=False) as f:
        json.dump(report, f)
        f.flush()
        exit_code, output = run_validation(f.name, "MaturionISMS/isms-test-module")
        Path(f.name).unlink()
    
    if exit_code == 1 and "MISSING_AGENT_ATTRIBUTION" in output:
        print("  ✅ PASS: Missing metadata correctly detected")
        assert True
    else:
        print(f"  ❌ FAIL: Missing metadata not detected (exit code: {exit_code})")
        print(f"  Output: {output}")
        assert False, "Missing metadata was not detected"


def test_no_reports():
    """Test when no QA reports are present"""
    print("Testing no QA reports scenario...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        exit_code, output = run_validation(tmpdir, "MaturionISMS/test-repo")
    
    if exit_code == 0 and "No QA report files found" in output:
        print("  ✅ PASS: No reports handled correctly (non-blocking)")
        assert True
    else:
        print(f"  ❌ FAIL: No reports scenario failed (exit code: {exit_code})")
        print(f"  Output: {output}")
        assert False, "No reports scenario was not handled correctly"


def main():
    """Run all tests"""
    print("=" * 70)
    print("AGENT QA BOUNDARY VALIDATION - COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    print()
    
    tests = [
        ("Valid Builder QA", test_valid_builder_qa),
        ("Valid FM QA", test_valid_fm_qa),
        ("Valid Governance QA", test_valid_governance_qa),
        ("Cross-Agent Violation: Builder→Governance", test_cross_agent_violation_builder_to_governance),
        ("Cross-Agent Violation: FM→Builder", test_cross_agent_violation_fm_to_builder),
        ("Missing Metadata", test_missing_metadata),
        ("No Reports", test_no_reports),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"  ❌ FAIL: Test raised exception: {e}")
            results.append((name, False))
        print()
    
    # Summary
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    failed = sum(1 for _, result in results if not result)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print()
    print(f"Total Tests: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print()
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED")
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        return 1


if __name__ == '__main__':
    sys.exit(main())
