"""
Wave domain model.

Implements the Wave entity representing an execution phase.
"""

from enum import Enum
from typing import Optional, List, Dict
from datetime import datetime


class WaveState(Enum):
    """Wave state enumeration."""
    PLANNED = "planned"
    IN_PROGRESS = "in-progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"


# Global wave registry
_wave_registry: Dict[str, 'Wave'] = {}


class Wave:
    """
    Wave entity representing an ordered execution phase.
    
    A wave contains tasks and has dependencies on other waves.
    """
    
    def __init__(
        self,
        id: str,
        program_id: str,
        name: Optional[str] = None,
        sequence_number: Optional[int] = None,
        dependencies: Optional[List[str]] = None
    ):
        """
        Initialize a new Wave.
        
        Args:
            id: Unique wave identifier
            program_id: ID of the parent program
            name: Optional human-readable wave name
            sequence_number: Optional sequence number within program
            dependencies: Optional list of prerequisite wave IDs
        """
        self.id = id
        self.program_id = program_id
        self.name = name or f"Wave {sequence_number or 'Unnamed'}"
        self.sequence_number = sequence_number
        self.dependencies = dependencies or []
        
        # State management
        self.state = WaveState.PLANNED
        self.progress_percentage = 0.0
        
        # Metadata
        self.created_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)
        
        # Auto-register
        _wave_registry[self.id] = self
    
    def __repr__(self):
        return f"Wave(id={self.id}, name={self.name}, state={self.state.value})"
    
    @classmethod
    def get_by_id(cls, wave_id: str) -> Optional['Wave']:
        """Get a wave by ID from global registry."""
        return _wave_registry.get(wave_id)
