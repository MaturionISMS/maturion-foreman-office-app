"""
Conversation data model.

Architecture Component: CONV-01 Conversation Manager
QA Coverage: QA-001 to QA-005
Architecture Reference: FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md (Section 3.1)

Data Contract:
- Entity: Conversation
- Operations: CREATE, READ, UPDATE
- Fields: conversationId, userId, state, createdAt, archivedAt, resumedAt
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, DateTime, Integer, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum

from fm.data.models.base import TenantIsolatedModel


class ConversationState(enum.Enum):
    """
    Conversation lifecycle states.
    
    State Transitions:
    - ACTIVE: New conversation, currently in use
    - ARCHIVED: User archived conversation (with reason)
    - RESUMED: Previously archived conversation reactivated
    """
    ACTIVE = "active"
    ARCHIVED = "archived"
    RESUMED = "resumed"


class Conversation(TenantIsolatedModel):
    """
    Conversation entity for managing conversation lifecycle.
    
    Privacy Requirements:
    - Tenant isolation: organisation_id (inherited from TenantIsolatedModel)
    - Audit trail: created_at, updated_at, archived_at, resumed_at
    
    State Management:
    - State transitions tracked via 'state' field
    - Archive reason captured in 'archived_reason'
    - Timestamps: created_at, archived_at, resumed_at
    
    Relationships:
    - One-to-many with Message (conversation can have multiple messages)
    - One-to-many with ConversationContext (conversation can have multiple contexts)
    - One-to-many with ClarificationSession (conversation can have multiple clarification sessions)
    """
    __tablename__ = 'conversations'
    
    # Primary key
    id = Column(String(255), primary_key=True)
    
    # Foreign keys
    user_id = Column(String(255), nullable=False, index=True)
    
    # State management
    state = Column(SQLEnum(ConversationState), nullable=False, default=ConversationState.ACTIVE)
    archived_reason = Column(String(1000), nullable=True)
    
    # State transition timestamps
    archived_at = Column(DateTime, nullable=True)
    resumed_at = Column(DateTime, nullable=True)
    
    # Message tracking
    last_message_at = Column(DateTime, nullable=True)
    message_count = Column(Integer, nullable=False, default=0)
    
    # Relationships
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    contexts = relationship("ConversationContext", back_populates="conversation", cascade="all, delete-orphan")
    clarification_sessions = relationship("ClarificationSession", back_populates="conversation", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Conversation(id={self.id}, user_id={self.user_id}, state={self.state.value}, organisation_id={self.organisation_id})>"
    
    def archive(self, reason: str) -> None:
        """
        Archive the conversation with a reason.
        
        QA: QA-003 (Archive conversation)
        
        Args:
            reason: Reason for archiving
            
        Raises:
            ValueError: If conversation already archived
        """
        if self.state == ConversationState.ARCHIVED:
            raise ValueError(f"Conversation {self.id} is already archived")
        
        self.state = ConversationState.ARCHIVED
        self.archived_reason = reason
        self.archived_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def resume(self) -> None:
        """
        Resume an archived conversation.
        
        QA: QA-004 (Resume conversation)
        
        Raises:
            ValueError: If conversation not archived
        """
        if self.state != ConversationState.ARCHIVED:
            raise ValueError(f"Conversation {self.id} is not archived (current state: {self.state.value})")
        
        self.state = ConversationState.RESUMED
        self.resumed_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def update_message_stats(self) -> None:
        """
        Update message statistics after a new message.
        
        QA: QA-002 (Retrieve conversation with message loading)
        """
        self.message_count = len(self.messages)
        if self.messages:
            self.last_message_at = max(msg.created_at for msg in self.messages)
        self.updated_at = datetime.utcnow()
