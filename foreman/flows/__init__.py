"""
Flow Orchestration for Foreman Office App

Provides end-to-end flow coordination for major user journeys.

Flows:
- Intent to Build Flow (FLOW-01): From user intent to build completion
- Build Lifecycle Flow (FLOW-02): Build execution orchestration
- Escalation Flow (FLOW-03): Escalation handling and resolution

Architectural Reference: FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md Section 14
QA Coverage: QA-200 to QA-210 (11 QA components)
"""

__all__ = [
    'intent_to_build',
    'build_lifecycle',
    'escalation_flow'
]

# Registry for test state management
_registries = {}

def clear_all():
    """Clear all flow state for testing."""
    global _registries
    _registries = {}
