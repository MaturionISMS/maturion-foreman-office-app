"""
Program Manager - manages programs and their lifecycle.

Implements program status tracking and aggregation.
"""

from typing import Dict, List, Optional, Any

from foreman.domain.program import Program, ProgramState
from foreman.domain.wave import Wave
from foreman.domain.task import Task, TaskState


class ProgramManager:
    """
    Manages programs and their status.
    
    Responsibilities:
    - Program status aggregation
    - Progress tracking
    - Failure detection
    """
    
    def __init__(self):
        """Initialize ProgramManager."""
        self._programs: Dict[str, Program] = {}
        self._waves: Dict[str, Wave] = {}
        self._tasks: Dict[str, Task] = {}
        
        # Indices
        self._program_waves: Dict[str, List[str]] = {}  # program_id -> wave_ids
        self._wave_tasks: Dict[str, List[str]] = {}  # wave_id -> task_ids
    
    def register_program(self, program: Program) -> None:
        """Register a program."""
        self._programs[program.id] = program
        self._program_waves[program.id] = []
    
    def register_wave(self, wave: Wave) -> None:
        """Register a wave."""
        self._waves[wave.id] = wave
        self._wave_tasks[wave.id] = []
        
        if wave.program_id in self._program_waves:
            self._program_waves[wave.program_id].append(wave.id)
    
    def register_task(self, task: Task) -> None:
        """Register a task."""
        self._tasks[task.id] = task
        
        if task.wave_id and task.wave_id in self._wave_tasks:
            self._wave_tasks[task.wave_id].append(task.id)
    
    def get_program_status(self, program_id: str) -> Dict[str, Any]:
        """
        Get aggregated status for a program.
        
        Args:
            program_id: ID of program
            
        Returns:
            Dictionary with program status information
        """
        # Check local registry first, then global
        program = self._programs.get(program_id)
        if not program:
            program = Program.get_by_id(program_id)
        
        if not program:
            return {}
        
        # Get all waves for this program
        wave_ids = self._program_waves.get(program_id, [])
        if not wave_ids:
            # Check for waves in global registry
            from foreman.domain.wave import _wave_registry
            wave_ids = [wid for wid, w in _wave_registry.items() if w.program_id == program_id]
        
        # Get all tasks for these waves
        all_tasks = []
        for wave_id in wave_ids:
            task_ids = self._wave_tasks.get(wave_id, [])
            if not task_ids:
                # Check for tasks in global registry
                from foreman.domain.task import _task_registry
                task_ids = [tid for tid, t in _task_registry.items() if t.wave_id == wave_id]
            
            for task_id in task_ids:
                task = self._tasks.get(task_id)
                if not task:
                    task = Task.get_by_id(task_id)
                if task:
                    all_tasks.append(task)
        
        # Count task states
        failed_tasks = [t for t in all_tasks if t.state == TaskState.FAILED]
        completed_tasks = [t for t in all_tasks if t.state == TaskState.COMPLETED]
        
        return {
            'program_id': program_id,
            'state': program.state.value,
            'has_failures': len(failed_tasks) > 0,
            'failed_tasks': len(failed_tasks),
            'failed_task_ids': [t.id for t in failed_tasks],
            'completed_tasks': len(completed_tasks),
            'total_tasks': len(all_tasks),
            'progress_percentage': program.progress_percentage
        }
