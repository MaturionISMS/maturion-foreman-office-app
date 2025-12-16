"""
Pytest configuration for Wave 0 minimum RED tests.

Provides fixtures and setup/teardown for test isolation.
"""

import pytest


@pytest.fixture(autouse=True)
def clear_global_registries():
    """
    Clear all global registries before each test to ensure test isolation.
    
    This fixture automatically runs before each test in this directory.
    """
    # Import all global registries
    from foreman.domain import task, program, wave, blocker
    from foreman.runtime import notification_manager
    
    # Clear all registries
    task._task_registry.clear()
    program._program_registry.clear()
    wave._wave_registry.clear()
    blocker._blocker_registry.clear()
    blocker._task_blockers_index.clear()
    notification_manager._notification_registry.clear()
    
    yield  # Test runs here
    
    # Cleanup after test (optional, but good practice)
    task._task_registry.clear()
    program._program_registry.clear()
    wave._wave_registry.clear()
    blocker._blocker_registry.clear()
    blocker._task_blockers_index.clear()
    notification_manager._notification_registry.clear()
