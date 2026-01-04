"""
Cross-Cutting Components for Foreman Office App

Provides infrastructure components used across the entire application.

Components:
- Memory Manager (CROSS-01): Global memory fabric management
- Authority Manager (CROSS-02): Role and permission enforcement
- Notification Service (CROSS-03): Multi-channel notification routing
- Evidence Store (CROSS-04): Evidence artifact management
- Audit Logger (CROSS-05): Immutable audit trail
- Watchdog Observer (CROSS-06): System health monitoring

Architectural Reference: FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md Section 16
QA Coverage: QA-147 to QA-199 (53 QA components)
"""

__all__ = [
    'memory_manager',
    'authority_manager',
    'notification_service',
    'evidence_store',
    'audit_logger',
    'watchdog_observer'
]

# Registry for test state management
_registries = {}

def clear_all():
    """Clear all cross-cutting state for testing."""
    global _registries
    _registries = {}
    
    # Import and clear each module's state
    try:
        from foreman.cross_cutting import memory_manager, audit_logger, system_health_watchdog
        memory_manager.clear_all()
        audit_logger.clear_all()
        system_health_watchdog.clear_all()
    except Exception:
        pass  # Ignore import errors during test setup
