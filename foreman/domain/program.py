"""
Program domain model.

Implements the Program entity representing a high-level initiative.
"""

from enum import Enum
from typing import Optional, List, Dict
from datetime import datetime


class ProgramState(Enum):
    """Program state enumeration."""
    PLANNED = "planned"
    IN_PROGRESS = "in-progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"


# Global program registry
_program_registry: Dict[str, 'Program'] = {}


class Program:
    """
    Program entity representing a high-level initiative.
    
    A program contains waves and defines objectives and scope.
    """
    
    def __init__(
        self,
        id: str,
        name: str,
        description: Optional[str] = None,
        objectives: Optional[List[str]] = None
    ):
        """
        Initialize a new Program.
        
        Args:
            id: Unique program identifier
            name: Human-readable program name
            description: Optional program description
            objectives: Optional list of program objectives
        """
        self.id = id
        self.name = name
        self.description = description or ""
        self.objectives = objectives or []
        
        # State management
        self.state = ProgramState.PLANNED
        self.progress_percentage = 0.0
        
        # Metadata
        self.created_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)
        self.evidence_location: Optional[str] = None
        
        # Auto-register
        _program_registry[self.id] = self
    
    def __repr__(self):
        return f"Program(id={self.id}, name={self.name}, state={self.state.value})"
    
    @classmethod
    def get_by_id(cls, program_id: str) -> Optional['Program']:
        """Get a program by ID from global registry."""
        return _program_registry.get(program_id)
