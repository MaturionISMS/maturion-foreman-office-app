"""
Data models for Foreman Office Conversational Interface subsystem.

Architecture Reference: FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md
QA Coverage: QA-001 to QA-018

Models:
- Conversation: CONV-01 Conversation Manager (QA-001 to QA-005)
- Message: CONV-02 Message Handler (QA-006 to QA-010)
- ConversationContext: CONV-03 FM Conversation Initiator (QA-011 to QA-013)
- ClarificationSession: CONV-04 Clarification Engine (QA-014 to QA-018)
"""

from fm.data.models.base import (
    Base,
    TenantIsolatedModel,
    DatabaseConfig,
    init_database,
    get_database,
)
from fm.data.models.conversation import Conversation, ConversationState
from fm.data.models.message import Message, MessageType, MessageState
from fm.data.models.conversation_context import ConversationContext
from fm.data.models.clarification_session import ClarificationSession, ClarificationState

__all__ = [
    # Base classes
    'Base',
    'TenantIsolatedModel',
    'DatabaseConfig',
    'init_database',
    'get_database',
    # Models
    'Conversation',
    'ConversationState',
    'Message',
    'MessageType',
    'MessageState',
    'ConversationContext',
    'ClarificationSession',
    'ClarificationState',
]
