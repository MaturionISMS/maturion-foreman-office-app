"""
Blocker domain model.

Implements the Blocker entity representing obstacles preventing progress.
"""

from enum import Enum
from typing import Optional, Dict
from datetime import datetime


class BlockerStatus(Enum):
    """Blocker status enumeration."""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class BlockerClassification(Enum):
    """Blocker classification enumeration."""
    ARCHITECTURE_ISSUE = "architecture_issue"
    QA_ISSUE = "qa_issue"
    BUILDER_FAILURE = "builder_failure"
    DEPENDENCY_ISSUE = "dependency_issue"
    GOVERNANCE_VIOLATION = "governance_violation"
    OTHER = "other"


# Global blocker registry for automatic lookup
_blocker_registry: Dict[str, 'Blocker'] = {}
_task_blockers_index: Dict[str, list] = {}


class Blocker:
    """
    Blocker entity representing an obstacle preventing task completion.
    
    Blockers are created when tasks fail or cannot proceed.
    """
    
    def __init__(
        self,
        id: str,
        task_id: str,
        reason: str,
        classification: Optional[BlockerClassification] = None
    ):
        """
        Initialize a new Blocker.
        
        Args:
            id: Unique blocker identifier
            task_id: ID of the blocked task
            reason: Description of why the task is blocked
            classification: Optional classification of blocker type
        """
        self.id = id
        self.task_id = task_id
        self.reason = reason
        self.classification = classification or BlockerClassification.OTHER
        
        # State management - use string for easier test comparison
        self.status = "open"  # or "in_progress", "resolved", "closed"
        
        # Metadata
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.resolved_at: Optional[datetime] = None
        self.resolution: Optional[str] = None
        
        # Auto-register in global registry
        _blocker_registry[self.id] = self
        if task_id not in _task_blockers_index:
            _task_blockers_index[task_id] = []
        _task_blockers_index[task_id].append(self.id)
    
    def __repr__(self):
        return f"Blocker(id={self.id}, task_id={self.task_id}, status={self.status})"
    
    @classmethod
    def get_by_id(cls, blocker_id: str) -> Optional['Blocker']:
        """
        Get a blocker by ID from global registry.
        
        Args:
            blocker_id: Blocker ID to look up
            
        Returns:
            Blocker if found, None otherwise
        """
        return _blocker_registry.get(blocker_id)
    
    @classmethod
    def get_blockers_for_task(cls, task_id: str) -> list:
        """
        Get all blockers for a specific task from global registry.
        
        Args:
            task_id: Task ID
            
        Returns:
            List of Blocker objects
        """
        blocker_ids = _task_blockers_index.get(task_id, [])
        return [_blocker_registry[bid] for bid in blocker_ids if bid in _blocker_registry]
