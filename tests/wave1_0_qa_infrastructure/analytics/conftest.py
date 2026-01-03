"""
Pytest configuration for Analytics subsystem tests.

Provides test isolation for analytics tests.
"""

import pytest


@pytest.fixture(autouse=True)
def clear_analytics_state():
    """
    Clear all analytics module state before and after each test.
    
    This ensures test isolation by resetting all module-level storage.
    """
    # Import all analytics modules that have clear_all()
    from foreman.analytics import usage_analyzer, data_source
    from foreman.analytics import cost_tracker, token_counter, anomaly_detector, cost_reporter
    from foreman.analytics import alert_manager, metrics_engine, storage
    
    # Clear before test
    usage_analyzer.clear_all()
    data_source.clear_all()
    cost_tracker.clear_all()
    if hasattr(token_counter, 'clear_all'):
        token_counter.clear_all()
    if hasattr(anomaly_detector, 'clear_all'):
        anomaly_detector.clear_all()
    if hasattr(cost_reporter, 'clear_all'):
        cost_reporter.clear_all()
    
    # Clear module-level dicts directly
    alert_manager._thresholds = {}
    alert_manager._alerts = {}
    metrics_engine._cache = {}
    storage._history = {}
    
    yield
    
    # Clear after test
    usage_analyzer.clear_all()
    data_source.clear_all()
    cost_tracker.clear_all()
    if hasattr(token_counter, 'clear_all'):
        token_counter.clear_all()
    if hasattr(anomaly_detector, 'clear_all'):
        anomaly_detector.clear_all()
    if hasattr(cost_reporter, 'clear_all'):
        cost_reporter.clear_all()
        
    alert_manager._thresholds = {}
    alert_manager._alerts = {}
    metrics_engine._cache = {}
    storage._history = {}
