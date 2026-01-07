"""
ClarificationSession data model.

Architecture Component: CONV-04 Clarification Engine
QA Coverage: QA-014 to QA-018
Architecture Reference: FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md (Section 3.4)

Data Contract:
- Entity: Clarification
- Operations: CREATE, READ, UPDATE
- Fields: clarificationId, messageId, questions, responses, state, resolvedAt
"""

from datetime import datetime, timezone
from typing import Optional, List, Dict
from sqlalchemy import Column, String, DateTime, Float, Integer, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.mutable import MutableList
import enum
import json

from fm.data.models.base import TenantIsolatedModel


class ClarificationState(enum.Enum):
    """
    Clarification session states.
    
    State Transitions:
    - DETECTING: Analyzing for ambiguity
    - ACTIVE: Clarification in progress
    - RESOLVED: Sufficient clarification received
    - STALLED: Exceeded iteration limit
    """
    DETECTING = "detecting"
    ACTIVE = "active"
    RESOLVED = "resolved"
    STALLED = "stalled"


class ClarificationSession(TenantIsolatedModel):
    """
    ClarificationSession entity for managing clarification loops.
    
    Privacy Requirements:
    - Tenant isolation: organisation_id (inherited from TenantIsolatedModel)
    - Audit trail: created_at, updated_at, resolved_at
    
    Ambiguity Detection:
    - ambiguity_score: Confidence score (0.0 to 1.0)
    - ambiguity_type: Type of ambiguity detected
    
    Clarification Loop Management:
    - iteration_count: Number of clarification rounds
    - max_iterations: Maximum allowed iterations (default: 3)
    - questions: List of clarification questions asked
    - responses: User responses to questions
    
    State Management:
    - State transitions tracked via 'state' field
    - Escalation trigger when iteration_count exceeds max_iterations
    
    Relationships:
    - Many-to-one with Conversation (session belongs to conversation)
    """
    __tablename__ = 'clarification_sessions'
    
    # Primary key
    id = Column(String(255), primary_key=True)
    
    # Foreign keys
    conversation_id = Column(String(255), ForeignKey('conversations.id'), nullable=False, index=True)
    message_id = Column(String(255), nullable=False, index=True)
    
    # Ambiguity detection
    ambiguity_score = Column(Float, nullable=False)
    ambiguity_type = Column(String(100), nullable=True)
    
    # Clarification loop management
    iteration_count = Column(Integer, nullable=False, default=0)
    max_iterations = Column(Integer, nullable=False, default=3)
    
    # Clarification data (stored as Text with JSON serialization)
    _questions = Column("questions", Text, nullable=False, default="[]")
    _responses = Column("responses", Text, nullable=False, default="[]")
    
    @property
    def questions(self) -> List[Dict]:
        """Get questions as Python list."""
        try:
            return json.loads(self._questions) if self._questions else []
        except json.JSONDecodeError:
            return []
    
    @questions.setter
    def questions(self, value: List[Dict]):
        """Set questions from Python list."""
        self._questions = json.dumps(value) if value else "[]"
    
    @property
    def responses(self) -> List[Dict]:
        """Get responses as Python list."""
        try:
            return json.loads(self._responses) if self._responses else []
        except json.JSONDecodeError:
            return []
    
    @responses.setter
    def responses(self, value: List[Dict]):
        """Set responses from Python list."""
        self._responses = json.dumps(value) if value else "[]"
    
    # State management
    state = Column(SQLEnum(ClarificationState), nullable=False, default=ClarificationState.DETECTING)
    resolved_at = Column(DateTime, nullable=True)
    stalled_at = Column(DateTime, nullable=True)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="clarification_sessions")
    
    def __repr__(self):
        return f"<ClarificationSession(id={self.id}, conversation_id={self.conversation_id}, state={self.state.value}, iteration_count={self.iteration_count})>"
    
    @staticmethod
    def validate_ambiguity_score(score: float) -> None:
        """
        Validate ambiguity confidence score.
        
        QA: QA-014 (Detect ambiguity with confidence scoring)
        
        Args:
            score: Confidence score to validate
            
        Raises:
            ValueError: If score is out of range
        """
        if not 0.0 <= score <= 1.0:
            raise ValueError(f"Ambiguity score must be between 0.0 and 1.0, got {score}")
    
    def add_clarification_round(self, questions: List[str], response: Optional[str] = None) -> None:
        """
        Add a clarification round (question and optionally response).
        
        QA: QA-015 (Generate clarifying questions)
        QA: QA-016 (Resolve clarification)
        QA: QA-017 (Clarification loop limits)
        
        Args:
            questions: List of clarification questions
            response: User response (if provided)
            
        Raises:
            ValueError: If max iterations exceeded
        """
        if self.iteration_count >= self.max_iterations:
            self.state = ClarificationState.STALLED
            self.stalled_at = datetime.now(timezone.utc).replace(tzinfo=None)
            raise ValueError(f"Clarification session {self.id} exceeded max iterations ({self.max_iterations})")
        
        self.iteration_count += 1
        
        # Store questions
        current_questions = self.questions if isinstance(self.questions, list) else []
        current_questions.append({
            "iteration": self.iteration_count,
            "questions": questions,
            "timestamp": datetime.now(timezone.utc).replace(tzinfo=None).isoformat()
        })
        self.questions = current_questions
        
        # Store response if provided
        if response:
            current_responses = self.responses if isinstance(self.responses, list) else []
            current_responses.append({
                "iteration": self.iteration_count,
                "response": response,
                "timestamp": datetime.now(timezone.utc).replace(tzinfo=None).isoformat()
            })
            self.responses = current_responses
        
        self.state = ClarificationState.ACTIVE
        self.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
    
    def resolve(self, resolved_intent: Dict) -> None:
        """
        Resolve clarification session with final intent.
        
        QA: QA-016 (Resolve clarification with sufficient information check)
        
        Args:
            resolved_intent: Final resolved intent data
        """
        self.state = ClarificationState.RESOLVED
        self.resolved_at = datetime.now(timezone.utc).replace(tzinfo=None)
        self.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
        
        # Store resolved intent in responses
        current_responses = self.responses if isinstance(self.responses, list) else []
        current_responses.append({
            "iteration": "final",
            "resolved_intent": resolved_intent,
            "timestamp": datetime.now(timezone.utc).replace(tzinfo=None).isoformat()
        })
        self.responses = current_responses
    
    def check_stalled(self) -> bool:
        """
        Check if clarification session is stalled (exceeded iterations).
        
        QA: QA-017 (Clarification loop limits - escalation after N loops)
        
        Returns:
            True if stalled, False otherwise
        """
        if self.iteration_count >= self.max_iterations and self.state != ClarificationState.RESOLVED:
            if self.state != ClarificationState.STALLED:
                self.state = ClarificationState.STALLED
                self.stalled_at = datetime.now(timezone.utc).replace(tzinfo=None)
                self.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
            return True
        return False
