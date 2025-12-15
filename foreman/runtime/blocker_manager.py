"""
Blocker Manager - manages blockers and obstacles.

Implements blocker creation, tracking, and resolution.
"""

from typing import Dict, List
from datetime import datetime

from foreman.domain.blocker import Blocker, BlockerStatus


class BlockerManager:
    """
    Manages blockers and obstacles preventing task progress.
    
    Responsibilities:
    - Blocker creation
    - Blocker tracking
    - Resolution management
    
    Note: Blockers auto-register globally when created, so this manager
    primarily provides convenience methods and can work with any Blocker
    regardless of which manager instance created it.
    """
    
    def __init__(self):
        """Initialize BlockerManager."""
        pass
    
    def create_blocker(self, blocker: Blocker) -> None:
        """
        Create a new blocker.
        
        Args:
            blocker: Blocker to create
            
        Note: Blocker automatically registers itself globally in __init__
        """
        # Blocker auto-registers, so just pass through
        pass
    
    def get_blocker(self, blocker_id: str) -> Blocker:
        """
        Get a blocker by ID.
        
        Args:
            blocker_id: ID of blocker
            
        Returns:
            Blocker instance or None
        """
        return Blocker.get_by_id(blocker_id)
    
    def get_blockers_for_task(self, task_id: str) -> List[Blocker]:
        """
        Get all blockers for a specific task.
        
        Args:
            task_id: ID of task
            
        Returns:
            List of blockers
        """
        return Blocker.get_blockers_for_task(task_id)
    
    def resolve_blocker(self, blocker_id: str, resolution: str) -> None:
        """
        Resolve a blocker.
        
        Args:
            blocker_id: ID of blocker to resolve
            resolution: Description of resolution
        """
        blocker = Blocker.get_by_id(blocker_id)
        if blocker:
            blocker.status = "resolved"
            blocker.resolution = resolution
            blocker.resolved_at = datetime.utcnow()
            blocker.updated_at = datetime.utcnow()
