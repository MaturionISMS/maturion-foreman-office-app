"""
Pytest configuration and fixtures for Wave 2.0 QA infrastructure.

Provides shared fixtures and configuration for Wave 2 tests.
"""

import pytest
from typing import Dict, Any


@pytest.fixture
def ui_test_context() -> Dict[str, Any]:
    """
    Provides UI test context for Wave 2 UI tests.
    
    Returns:
        Dictionary with test context including organization_id for tenant isolation.
    """
    return {
        "organisation_id": "test-org-wave-2",
        "user_id": "test-user-1",
        "session_id": "test-session-1"
    }


@pytest.fixture
def dashboard_enhanced_context(ui_test_context) -> Dict[str, Any]:
    """
    Provides enhanced dashboard test context.
    
    Returns:
        Dictionary with dashboard-specific test context.
    """
    return {
        **ui_test_context,
        "dashboard_id": "enhanced-dashboard-1",
        "view_type": "enhanced"
    }
