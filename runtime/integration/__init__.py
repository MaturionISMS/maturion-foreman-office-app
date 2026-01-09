"""
Runtime Integration Module

Purpose: Deep cross-module integrations for Wave 2.9
Authority: Wave 2.0 Subwave 2.9 - Deep Integration Phase 1 (QA-461 to QA-475)
Tenant Isolation: All operations scoped by organisation_id
"""

from .cross_subsystem_integrator import CrossSubsystemIntegrator
from .event_bus import EventBus
from .service_communicator import ServiceCommunicator

__all__ = [
    'CrossSubsystemIntegrator',
    'EventBus',
    'ServiceCommunicator',
]
