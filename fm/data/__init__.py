"""
Foreman Office Data Layer

This module provides the database schema and data models for the
Conversational Interface subsystem (CONV-01 through CONV-04).

Architecture Reference: FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md
QA Coverage: QA-001 to QA-018
"""

from fm.data.models import (
    Base,
    DatabaseConfig,
    init_database,
    get_database,
    Conversation,
    ConversationState,
    Message,
    MessageType,
    MessageState,
    ConversationContext,
    ClarificationSession,
    ClarificationState,
)

__all__ = [
    'Base',
    'DatabaseConfig',
    'init_database',
    'get_database',
    'Conversation',
    'ConversationState',
    'Message',
    'MessageType',
    'MessageState',
    'ConversationContext',
    'ClarificationSession',
    'ClarificationState',
]
