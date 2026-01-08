"""
Task Manager - manages task lifecycle and state transitions.

Implements task assignment, execution tracking, and completion validation.
"""

from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import uuid

from foreman.domain.task import Task, TaskState
from foreman.domain.blocker import Blocker, BlockerClassification


class TaskTransition:
    """Represents a state transition in task lifecycle."""
    
    def __init__(self, from_state: TaskState, to_state: TaskState, timestamp: datetime):
        self.from_state = from_state
        self.to_state = to_state
        self.timestamp = timestamp


class TaskManager:
    """
    Manages task lifecycle and state transitions.
    
    Responsibilities:
    - Task assignment to builders
    - State transition validation
    - Lifecycle tracking
    - Prerequisite validation
    """
    
    def __init__(self, blocker_manager=None, notification_manager=None):
        """Initialize TaskManager."""
        self._tasks: Dict[str, Task] = {}
        self._transition_logs: Dict[str, List[Dict[str, Any]]] = {}
        self._blocker_manager = blocker_manager
        self._notification_manager = notification_manager
    
    def create_task(self, task: Task) -> None:
        """
        Register a new task.
        
        Args:
            task: Task to register
        """
        self._tasks[task.id] = task
        self._transition_logs[task.id] = []
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Retrieve a task by ID.
        
        Args:
            task_id: ID of task to retrieve
            
        Returns:
            Task if found, None otherwise
        """
        return self._tasks.get(task_id)
    
    def assign_task(self, task_or_id: Union[str, Task], builder_id: str) -> None:
        """
        Assign a task to a builder.
        
        Args:
            task_or_id: Task object or task ID
            builder_id: ID of builder to assign to
            
        Raises:
            ValueError: If task not found or invalid state
        """
        # Handle both Task objects and task IDs
        if isinstance(task_or_id, Task):
            task = task_or_id
            # Auto-register if not already registered
            if task.id not in self._tasks:
                self.create_task(task)
            task_id = task.id
        else:
            task_id = task_or_id
            task = self._tasks.get(task_id)
            # If not in local registry, check global Task registry
            if not task:
                task = Task.get_by_id(task_id)
                if task:
                    # Import from global registry
                    self._tasks[task_id] = task
                    self._transition_logs[task_id] = []
                else:
                    raise ValueError(f"Task {task_id} not found. Task must be created first.")
        
        if task.state != TaskState.CREATED:
            raise ValueError(f"Invalid state transition: task must be in CREATED state, currently {task.state.value}")
        
        # Record transition
        self._log_transition(task_id, task.state, TaskState.ASSIGNED)
        
        # Update task
        task.state = TaskState.ASSIGNED
        task.assigned_builder_id = builder_id
        task.updated_at = datetime.now(UTC)
    
    def start_task(self, task_id: str) -> None:
        """
        Mark a task as started.
        
        Args:
            task_id: ID of task to start
            
        Raises:
            ValueError: If task not found or invalid state
        """
        task = self._tasks.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        if task.state != TaskState.ASSIGNED:
            raise ValueError(f"Invalid state transition: task must be ASSIGNED to start, currently {task.state.value}")
        
        # Check prerequisites
        if task.prerequisites:
            for prereq_id in task.prerequisites:
                prereq = self._tasks.get(prereq_id)
                if not prereq or prereq.state != TaskState.COMPLETED:
                    raise ValueError(f"Prerequisite {prereq_id} not completed")
        
        # Record transition
        self._log_transition(task_id, task.state, TaskState.IN_PROGRESS)
        
        # Update task
        task.state = TaskState.IN_PROGRESS
        task.started_at = datetime.now(UTC)
        task.updated_at = datetime.now(UTC)
    
    def complete_task(self, task_id: str, qa_results: Optional[Dict[str, Any]] = None) -> None:
        """
        Mark a task as completed.
        
        Args:
            task_id: ID of task to complete
            qa_results: Optional QA validation results
            
        Raises:
            ValueError: If task not found or invalid state
        """
        task = self._tasks.get(task_id)
        if not task:
            # Check global registry
            task = Task.get_by_id(task_id)
            if task:
                # Import from global registry
                self._tasks[task_id] = task
                self._transition_logs[task_id] = []
            else:
                raise ValueError(f"Task {task_id} not found")
        
        if task.state not in [TaskState.IN_PROGRESS, TaskState.ASSIGNED]:
            raise ValueError(f"Invalid state transition: cannot complete from {task.state.value}")
        
        # Record transition
        self._log_transition(task_id, task.state, TaskState.COMPLETED)
        
        # Update task
        task.state = TaskState.COMPLETED
        task.completed_at = datetime.now(UTC)
        task.updated_at = datetime.now(UTC)
    
    def fail_task(
        self,
        task_id: str,
        reason: str,
        qa_results: Optional[Dict[str, Any]] = None,
        diagnostics: Optional[Dict[str, Any]] = None,
        failure_type: Optional[str] = None
    ) -> None:
        """
        Mark a task as failed.
        
        Args:
            task_id: ID of task that failed
            reason: Reason for failure
            qa_results: Optional QA results
            diagnostics: Optional diagnostic information
            failure_type: Optional classification of failure
            
        Raises:
            ValueError: If task not found
        """
        task = self._tasks.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        # Record transition
        self._log_transition(task_id, task.state, TaskState.FAILED)
        
        # Update task
        task.state = TaskState.FAILED
        task.failure_reason = reason
        task.diagnostics = diagnostics
        task.failed_at = datetime.now(UTC)
        task.updated_at = datetime.now(UTC)
        
        # Automatically create blocker (blockers auto-register globally)
        blocker_id = f"blocker-{uuid.uuid4()}"
        classification = self._classify_failure(failure_type, reason)
        blocker = Blocker(
            id=blocker_id,
            task_id=task_id,
            reason=reason,
            classification=classification
        )
        # Blocker auto-registers itself, no need to call blocker_manager
        
        # If blocker_manager was explicitly provided, we can still notify it
        if self._blocker_manager:
            self._blocker_manager.create_blocker(blocker)
        
        # Send escalation notification to global registry
        from foreman.runtime.notification_manager import _notification_registry
        severity = 'critical' if 'critical' in reason.lower() else 'high'
        notification = {
            'recipient': 'foreman',
            'type': 'escalation',
            'task_id': task_id,
            'severity': severity,
            'message': f"Task {task_id} failed: {reason}",
            'timestamp': datetime.now(UTC).isoformat()
        }
        _notification_registry.append(notification)
        
        # Also notify via manager if one was provided
        if self._notification_manager:
            self._notification_manager.send_notification(
                recipient='foreman',
                type='escalation',
                task_id=task_id,
                severity=severity,
                message=f"Task {task_id} failed: {reason}"
            )
    
    def get_transition_log(self, task_id: str) -> List[Dict[str, Any]]:
        """
        Get state transition log for a task.
        
        Args:
            task_id: ID of task
            
        Returns:
            List of transition records
        """
        return self._transition_logs.get(task_id, [])
    
    def _log_transition(self, task_id: str, from_state: TaskState, to_state: TaskState) -> None:
        """
        Log a state transition.
        
        Args:
            task_id: ID of task
            from_state: Previous state
            to_state: New state
        """
        if task_id not in self._transition_logs:
            self._transition_logs[task_id] = []
        
        self._transition_logs[task_id].append({
            'from_state': from_state.value,
            'to_state': to_state.value,
            'timestamp': datetime.now(UTC).isoformat()
        })
    
    def _classify_failure(self, failure_type: Optional[str], reason: str) -> BlockerClassification:
        """
        Classify a failure into a blocker classification.
        
        Args:
            failure_type: Optional explicit failure type
            reason: Failure reason
            
        Returns:
            BlockerClassification
        """
        if failure_type == 'architecture_mismatch':
            return BlockerClassification.ARCHITECTURE_ISSUE
        elif 'qa' in reason.lower() or 'test' in reason.lower():
            return BlockerClassification.QA_ISSUE
        elif 'governance' in reason.lower():
            return BlockerClassification.GOVERNANCE_VIOLATION
        elif 'dependency' in reason.lower():
            return BlockerClassification.DEPENDENCY_ISSUE
        else:
            return BlockerClassification.OTHER
