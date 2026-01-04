"""
Escalation & Supervision Subsystem

Components:
- ESC-01: Ping Generator (QA-093 to QA-096)
- ESC-02: Escalation Manager (QA-097 to QA-104)
- ESC-03: Silence Detector (QA-105 to QA-109)
- ESC-04: Message Inbox Controller (QA-110 to QA-116) - UI component

This module provides escalation mechanisms for attention-required situations,
supervision of system health, and silence detection for stalled processes.
"""

from .ping_generator import PingGenerator
from .escalation_manager import EscalationManager
from .silence_detector import SilenceDetector

__all__ = ['PingGenerator', 'EscalationManager', 'SilenceDetector']
