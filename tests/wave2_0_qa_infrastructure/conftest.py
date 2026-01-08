"""
Pytest configuration for Wave 2.0 QA Infrastructure tests.

Provides fixtures and setup/teardown for test isolation.
"""

import pytest
import os
import json
from datetime import datetime
from pathlib import Path


@pytest.fixture
def evidence_dir():
    """
    Create evidence directory for Wave 2.0 QA artifacts.
    
    Returns path to evidence directory for this test run.
    """
    evidence_path = Path("evidence/wave-2.0/ui-builder/subwave-2.1")
    evidence_path.mkdir(parents=True, exist_ok=True)
    return evidence_path


@pytest.fixture
def test_organisation_id():
    """
    Provide test organisation ID for tenant isolation.
    
    All tests must use this ID to ensure proper tenant isolation.
    """
    return "test-org-wave2-001"


@pytest.fixture
def test_user_id():
    """
    Provide test user ID (Johan) for authority context.
    """
    return "johan-wave2-001"


@pytest.fixture
def test_fm_id():
    """
    Provide test FM ID for authority context.
    """
    return "fm-wave2-001"


@pytest.fixture
def ui_test_context(test_organisation_id, test_user_id):
    """
    Base UI test context with organisation_id for tenant isolation.
    """
    return {
        "organisation_id": test_organisation_id,
        "user_id": test_user_id,
        "session_id": "test-session-001",
        "tenant_isolation": True
    }


@pytest.fixture
def dashboard_enhanced_context(ui_test_context):
    """
    Dashboard-specific test context for enhanced features.
    """
    return {
        **ui_test_context,
        "dashboard_mode": "enhanced",
        "features_enabled": ["drill_down", "filtering", "realtime"]
    }


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
            "timestamp": datetime.now(UTC).isoformat(),
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
    # Clear any enhanced dashboard state
    try:
        from ui.dashboard import enhanced_dashboard
        enhanced_dashboard.clear_all()
    except (ImportError, AttributeError):
        pass  # Components not implemented yet (expected in RED phase)
    
    yield  # Test runs here
    
    # Cleanup after test
    try:
        from ui.dashboard import enhanced_dashboard
        enhanced_dashboard.clear_all()
    except (ImportError, AttributeError):
        pass
