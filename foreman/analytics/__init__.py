"""
Analytics Subsystem for Foreman Office App

Provides usage analytics, metrics tracking, cost analysis, and performance reporting.

Components:
- Usage Analyzer (ANALYTICS-01): Dashboard metrics and rendering
- Metrics Engine (ANALYTICS-02): Metric aggregation and alerting  
- Cost Tracker (ANALYTICS-03): AI usage cost tracking and anomaly detection

Architectural Reference: FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md Section 16.3
QA Coverage: QA-132 to QA-146 (15 QA components)
"""

__all__ = [
    'usage_analyzer',
    'metrics_engine',
    'cost_tracker'
]

# Registry for test state management
_registries = {}

def clear_all():
    """Clear all analytics state for testing."""
    global _registries
    _registries = {}
