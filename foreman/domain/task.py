"""
Task domain model and state machine.

Implements the Task entity with state transitions and lifecycle management.
"""

from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime


class TaskState(Enum):
    """Task state enumeration."""
    CREATED = "created"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


# Global task registry for automatic lookup
_task_registry: Dict[str, 'Task'] = {}


class Task:
    """
    Task entity representing a build task in the Foreman system.
    
    A task is a unit of work assigned to a builder agent with specific
    architecture and QA requirements.
    """
    
    def __init__(
        self,
        id: str,
        name: str,
        type: str,
        wave_id: Optional[str] = None,
        prerequisites: Optional[List[str]] = None,
        architecture_ref: Optional[str] = None,
        qa_suite_ref: Optional[str] = None
    ):
        """
        Initialize a new Task.
        
        Args:
            id: Unique task identifier
            name: Human-readable task name
            type: Type of task (ui-build, api-build, schema-build, etc.)
            wave_id: Optional wave this task belongs to
            prerequisites: Optional list of prerequisite task IDs
            architecture_ref: Optional path to architecture document
            qa_suite_ref: Optional path to QA suite
        """
        self.id = id
        self.name = name
        self.type = type
        self.wave_id = wave_id
        self.prerequisites = prerequisites or []
        self.architecture_ref = architecture_ref
        self.qa_suite_ref = qa_suite_ref
        
        # State management
        self.state = TaskState.CREATED
        self.assigned_builder_id: Optional[str] = None
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.failed_at: Optional[datetime] = None
        
        # Failure tracking
        self.failure_reason: Optional[str] = None
        self.diagnostics: Optional[Dict[str, Any]] = None
        
        # Metadata
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        
        # Auto-register in global registry
        _task_registry[self.id] = self
    
    def __repr__(self):
        return f"Task(id={self.id}, name={self.name}, state={self.state.value})"
    
    @classmethod
    def get_by_id(cls, task_id: str) -> Optional['Task']:
        """
        Get a task by ID from global registry.
        
        Args:
            task_id: Task ID to look up
            
        Returns:
            Task if found, None otherwise
        """
        return _task_registry.get(task_id)
