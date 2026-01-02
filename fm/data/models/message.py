"""
Message data model.

Architecture Component: CONV-02 Message Handler
QA Coverage: QA-006 to QA-010
Architecture Reference: FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md (Section 3.2)

Data Contract:
- Entity: Message
- Operations: CREATE, READ, UPDATE
- Fields: messageId, conversationId, senderId, content, type, state, createdAt, deliveredAt, readAt
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum

from fm.data.models.base import TenantIsolatedModel


class MessageType(enum.Enum):
    """
    Message type classification.
    
    Types:
    - USER: Message from user (Johan)
    - FM: Message from Foreman
    """
    USER = "user"
    FM = "fm"


class MessageState(enum.Enum):
    """
    Message delivery states.
    
    State Transitions:
    - PENDING: Message created, not yet delivered
    - DELIVERED: Message delivered to recipient
    - READ: Message read by recipient
    """
    PENDING = "pending"
    DELIVERED = "delivered"
    READ = "read"


class Message(TenantIsolatedModel):
    """
    Message entity for handling conversation messages.
    
    Privacy Requirements:
    - Tenant isolation: organisation_id (inherited from TenantIsolatedModel)
    - Audit trail: created_at, updated_at, delivered_at, read_at
    
    State Management:
    - State transitions: PENDING → DELIVERED → READ
    - Timestamps track each transition
    
    Validation:
    - Content cannot be empty (enforced in application layer)
    - Conversation must exist (foreign key constraint)
    - Sender ID must be valid
    
    Relationships:
    - Many-to-one with Conversation (message belongs to conversation)
    """
    __tablename__ = 'messages'
    
    # Primary key
    id = Column(String(255), primary_key=True)
    
    # Foreign keys
    conversation_id = Column(String(255), ForeignKey('conversations.id'), nullable=False, index=True)
    
    # Message metadata
    sender_id = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=False)
    type = Column(SQLEnum(MessageType), nullable=False)
    
    # State management
    state = Column(SQLEnum(MessageState), nullable=False, default=MessageState.PENDING)
    
    # State transition timestamps
    delivered_at = Column(DateTime, nullable=True)
    read_at = Column(DateTime, nullable=True)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    
    def __repr__(self):
        return f"<Message(id={self.id}, conversation_id={self.conversation_id}, type={self.type.value}, state={self.state.value})>"
    
    @staticmethod
    def validate_content(content: str) -> None:
        """
        Validate message content.
        
        QA: QA-009 (Message validation - empty content rejection)
        
        Args:
            content: Message content to validate
            
        Raises:
            ValueError: If content is empty or invalid
        """
        if not content or not content.strip():
            raise ValueError("Message content cannot be empty")
        
        if len(content) > 10000:
            raise ValueError("Message content exceeds maximum length (10000 characters)")
    
    def deliver(self) -> None:
        """
        Mark message as delivered.
        
        QA: QA-007 (Deliver message with routing and timestamp)
        
        Raises:
            ValueError: If message already delivered
        """
        if self.state != MessageState.PENDING:
            raise ValueError(f"Message {self.id} is not in PENDING state (current state: {self.state.value})")
        
        self.state = MessageState.DELIVERED
        self.delivered_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def mark_read(self, read_by: str) -> None:
        """
        Mark message as read.
        
        QA: QA-008 (Mark message read with state update and audit log)
        
        Args:
            read_by: User ID who read the message
            
        Raises:
            ValueError: If message not delivered yet
        """
        if self.state != MessageState.DELIVERED:
            raise ValueError(f"Message {self.id} is not in DELIVERED state (current state: {self.state.value})")
        
        self.state = MessageState.READ
        self.read_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
