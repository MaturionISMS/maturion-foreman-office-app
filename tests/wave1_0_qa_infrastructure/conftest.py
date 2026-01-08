"""
Pytest configuration for Wave 1.0 QA Infrastructure tests.

Provides fixtures and setup/teardown for test isolation.
"""

import pytest
import os
import json
from datetime import datetime, timezone
from pathlib import Path


@pytest.fixture
def evidence_dir():
    """
    Create evidence directory for QA artifacts.
    
    Returns path to evidence directory for this test run.
    """
    evidence_path = Path("evidence/wave-1.0/qa-builder")
    evidence_path.mkdir(parents=True, exist_ok=True)
    return evidence_path


@pytest.fixture
def test_organisation_id():
    """
    Provide test organisation ID for tenant isolation.
    
    All tests must use this ID to ensure proper tenant isolation.
    """
    return "test-org-001"


@pytest.fixture
def test_user_id():
    """
    Provide test user ID (Johan) for authority context.
    """
    return "johan-001"


@pytest.fixture
def test_fm_id():
    """
    Provide test FM ID for authority context.
    """
    return "fm-001"


@pytest.fixture
def mock_memory_fabric(tmp_path):
    """
    Create mock memory fabric for testing.
    
    Returns path to temporary memory fabric directory.
    """
    memory_path = tmp_path / "memory"
    memory_path.mkdir(parents=True, exist_ok=True)
    
    # Create basic memory structure
    (memory_path / "global").mkdir(exist_ok=True)
    (memory_path / "scoped").mkdir(exist_ok=True)
    (memory_path / "proposals").mkdir(exist_ok=True)
    
    return memory_path


@pytest.fixture
def mock_evidence_store(tmp_path):
    """
    Create mock evidence store for testing.
    
    Returns path to temporary evidence store directory.
    """
    evidence_path = tmp_path / "evidence"
    evidence_path.mkdir(parents=True, exist_ok=True)
    return evidence_path


@pytest.fixture
def create_qa_evidence():
    """
    Factory fixture to create QA evidence artifacts.
    
    Returns a function that creates evidence artifacts in JSON format.
    """
    def _create_evidence(qa_id: str, status: str, details: dict):
        evidence = {
            "qa_id": qa_id,
            "status": status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "details": details
        }
        return evidence
    
    return _create_evidence


@pytest.fixture(autouse=True)
def clear_test_state():
    """
    Clear test state before each test to ensure isolation.
    
    This fixture automatically runs before each test.
    """
    # Import registries if they exist
    try:
        from foreman.analytics import usage_analyzer, cost_tracker, performance_reporter
        usage_analyzer.clear_all()
        cost_tracker.clear_all()
        performance_reporter.clear_all()
    except ImportError:
        pass  # Components not implemented yet (expected in RED phase)
    
    try:
        from foreman.cross_cutting import memory_manager, authority_enforcer, audit_logger, system_health_watchdog
        memory_manager.clear_all()
        authority_enforcer.clear_all()
        audit_logger.clear_all()
        system_health_watchdog.clear_all()
    except ImportError:
        pass  # Components not implemented yet (expected in RED phase)
    
    yield  # Test runs here
    
    # Cleanup after test
    try:
        from foreman.analytics import usage_analyzer, cost_tracker, performance_reporter
        usage_analyzer.clear_all()
        cost_tracker.clear_all()
        performance_reporter.clear_all()
    except ImportError:
        pass
    
    try:
        from foreman.cross_cutting import memory_manager, authority_enforcer, audit_logger, system_health_watchdog
        memory_manager.clear_all()
        authority_enforcer.clear_all()
        audit_logger.clear_all()
        system_health_watchdog.clear_all()
    except ImportError:
        pass
