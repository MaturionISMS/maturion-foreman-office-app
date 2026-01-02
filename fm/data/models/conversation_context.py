"""
ConversationContext data model.

Architecture Component: CONV-03 FM Conversation Initiator
QA Coverage: QA-011 to QA-013
Architecture Reference: FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md (Section 3.3)

Data Contract:
- Entity: ConversationContext
- Operations: CREATE
- Fields: id, conversationId, contextType, contextData, createdAt
"""

from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
import json

from fm.data.models.base import TenantIsolatedModel


class ConversationContext(TenantIsolatedModel):
    """
    ConversationContext entity for attaching context to FM-initiated conversations.
    
    Privacy Requirements:
    - Tenant isolation: organisation_id (inherited from TenantIsolatedModel)
    - Audit trail: created_at, updated_at
    
    Context Types:
    - ESCALATION: Escalation context (component, error, retry count)
    - BUILD: Build context (build ID, phase, status)
    - EVIDENCE: Evidence linking (QA component, test results)
    - URGENT: Urgent notification context
    
    Data Storage:
    - context_data stored as JSON for flexibility
    - Immutable after creation (no UPDATE operations)
    
    Relationships:
    - Many-to-one with Conversation (context belongs to conversation)
    """
    __tablename__ = 'conversation_contexts'
    
    # Primary key
    id = Column(String(255), primary_key=True)
    
    # Foreign keys
    conversation_id = Column(String(255), ForeignKey('conversations.id'), nullable=False, index=True)
    
    # Context metadata
    context_type = Column(String(100), nullable=False, index=True)
    _context_data = Column("context_data", Text, nullable=False)
    
    @property
    def context_data(self):
        """Get context_data as Python dict."""
        try:
            return json.loads(self._context_data) if self._context_data else {}
        except json.JSONDecodeError:
            return {}
    
    @context_data.setter
    def context_data(self, value):
        """Set context_data from Python dict."""
        self._context_data = json.dumps(value) if value else "{}"
    
    # Priority flag (for urgent conversations)
    priority = Column(String(50), nullable=False, default="normal")
    
    # Relationships
    conversation = relationship("Conversation", back_populates="contexts")
    
    def __repr__(self):
        return f"<ConversationContext(id={self.id}, conversation_id={self.conversation_id}, context_type={self.context_type}, priority={self.priority})>"
    
    @staticmethod
    def validate_context_type(context_type: str) -> None:
        """
        Validate context type.
        
        QA: QA-012 (Attach context validation)
        
        Args:
            context_type: Context type to validate
            
        Raises:
            ValueError: If context type is invalid
        """
        valid_types = ["escalation", "build", "evidence", "urgent", "general"]
        if context_type.lower() not in valid_types:
            raise ValueError(f"Invalid context type: {context_type}. Must be one of: {', '.join(valid_types)}")
    
    @staticmethod
    def validate_priority(priority: str) -> None:
        """
        Validate priority level.
        
        QA: QA-013 (FM urgent conversation with priority flag)
        
        Args:
            priority: Priority level to validate
            
        Raises:
            ValueError: If priority is invalid
        """
        valid_priorities = ["normal", "high", "urgent"]
        if priority.lower() not in valid_priorities:
            raise ValueError(f"Invalid priority: {priority}. Must be one of: {', '.join(valid_priorities)}")
