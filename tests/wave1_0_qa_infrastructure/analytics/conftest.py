"""
Pytest configuration for Analytics subsystem tests.

Provides test isolation for analytics tests.
"""

import pytest
import importlib
import sys


@pytest.fixture(autouse=True, scope="function")
def clear_analytics_state():
    """
    Clear all analytics module state before and after each test.
    
    This ensures test isolation by resetting all module-level storage.
    """
    # Force reload all analytics modules to pick up code changes
    analytics_modules = [
        'foreman.analytics.metrics_engine',
        'foreman.analytics.usage_analyzer',
        'foreman.analytics.data_source',
        'foreman.analytics.cost_tracker',
        'foreman.analytics.metrics_calculator',
    ]
    
    for module_name in analytics_modules:
        if module_name in sys.modules:
            importlib.reload(sys.modules[module_name])
    
    # Import all analytics modules that have clear_all()
    from foreman.analytics import usage_analyzer, data_source
    from foreman.analytics import cost_tracker, token_counter, anomaly_detector, cost_reporter
    from foreman.analytics import alert_manager, metrics_engine, storage
    
    # Clear before test
    usage_analyzer.clear_all()
    data_source.clear_all()
    cost_tracker.clear_all()
    metrics_engine.clear_all()  # This also clears data_source._metrics_data
    if hasattr(token_counter, 'clear_all'):
        token_counter.clear_all()
    if hasattr(anomaly_detector, 'clear_all'):
        anomaly_detector.clear_all()
    if hasattr(cost_reporter, 'clear_all'):
        cost_reporter.clear_all()
    
    # Clear module-level dicts directly
    alert_manager._thresholds.clear()
    alert_manager._alerts.clear()
    storage._history.clear()
    
    yield
    
    # Clear after test
    usage_analyzer.clear_all()
    data_source.clear_all()
    cost_tracker.clear_all()
    metrics_engine.clear_all()
    if hasattr(token_counter, 'clear_all'):
        token_counter.clear_all()
    if hasattr(anomaly_detector, 'clear_all'):
        anomaly_detector.clear_all()
    if hasattr(cost_reporter, 'clear_all'):
        cost_reporter.clear_all()
        
    alert_manager._thresholds.clear()
    alert_manager._alerts.clear()
    storage._history.clear()
