"""
Watchdog Runtime Module.

Independent, read-only watchdog runtime for FM application.

Constraints (MANDATORY):
- ❌ No writes to alerts or system state
- ❌ No policy interpretation or decision-making
- ❌ No automatic remediation
- ❌ No silent failures - all errors escalated
- ✅ Report only - read and report alert status
- ✅ Escalate only - forward to human oversight

This module implements W-F1: Independent Watchdog Runtime (Read-Only, Non-Authoritative)
"""

from .alert_reader import AlertReader
from .escalation_reporter import EscalationReporter

__all__ = ['AlertReader', 'EscalationReporter']
