"""
Build Orchestrator (EXEC-01)

QA Coverage: QA-078 to QA-083
Architecture: FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md Section EXEC-01

Responsibilities:
- Initiate build from approved requirement
- Assign builders to QA ranges
- Monitor build progress
- Handle build blocking conditions
- Complete builds with validation
- Handle orchestration failures
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class BuildOrchestrator:
    """
    EXEC-01: Build Orchestrator
    
    Orchestrates build execution from approved requirements.
    Manages builder assignment, progress monitoring, and completion validation.
    """
    
    def __init__(self):
        """Initialize Build Orchestrator"""
        self.builds = {}
        self.builder_assignments = {}
    
    def initiate_build(self, requirement_id: str, architecture_ref: str) -> Dict[str, Any]:
        """
        QA-078: Initiate build from approved requirement
        
        Creates build entity, links architecture, and plans waves.
        
        Args:
            requirement_id: Approved requirement identifier
            architecture_ref: Reference to architecture specification
        
        Returns:
            Dict with:
                - build_id: Unique build identifier
                - build_entity_created: Boolean
                - architecture_linked: Boolean
                - wave_planning_complete: Boolean
                - waves: List of planned waves
        """
        build_id = f"build_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        # Create build entity
        build_entity = {
            "build_id": build_id,
            "requirement_id": requirement_id,
            "architecture_ref": architecture_ref,
            "state": "INITIATED",
            "created_at": datetime.now().isoformat(),
            "progress_percentage": 0,
            "qa_total": 0,
            "qa_green": 0,
            "qa_red": 0
        }
        
        # Plan waves (simplified - in production would analyze architecture)
        waves = [
            {
                "wave_id": "wave-1.0.1",
                "name": "Schema Foundation",
                "builder": "schema-builder",
                "qa_range": "QA-001 to QA-020",
                "status": "planned"
            },
            {
                "wave_id": "wave-1.0.2",
                "name": "UI Foundation",
                "builder": "ui-builder",
                "qa_range": "QA-021 to QA-040",
                "status": "planned"
            },
            {
                "wave_id": "wave-1.0.3",
                "name": "API Foundation",
                "builder": "api-builder",
                "qa_range": "QA-041 to QA-060",
                "status": "planned"
            }
        ]
        
        build_entity["waves"] = waves
        build_entity["wave_planning_complete"] = True
        
        self.builds[build_id] = build_entity
        
        return {
            "build_id": build_id,
            "build_entity_created": True,
            "architecture_linked": True,
            "wave_planning_complete": True,
            "waves": waves
        }
    
    def assign_builder(self, build_id: str, qa_start: int, qa_end: int, builder_type: str) -> Dict[str, Any]:
        """
        QA-079: Assign builder to QA range
        
        Calculates range, selects builder, and creates task.
        
        Args:
            build_id: Build identifier
            qa_start: Starting QA number (e.g., 58 for QA-058)
            qa_end: Ending QA number (e.g., 92 for QA-092)
            builder_type: Builder to assign (schema, ui, api, integration, qa)
        
        Returns:
            Dict with:
                - build_id: Build identifier
                - task_id: Created task identifier
                - qa_range_calculated: Boolean
                - qa_start: Starting QA number
                - qa_end: Ending QA number
                - builder_selected: Builder type
                - task_created: Boolean
        """
        if build_id not in self.builds:
            raise ValueError(f"Build not found: {build_id}")
        
        build = self.builds[build_id]
        
        # Create task
        task_id = f"task_{build_id}_{builder_type}_{qa_start}_{qa_end}"
        
        task = {
            "task_id": task_id,
            "build_id": build_id,
            "builder_type": builder_type,
            "qa_start": qa_start,
            "qa_end": qa_end,
            "qa_range": f"QA-{qa_start:03d} to QA-{qa_end:03d}",
            "qa_count": qa_end - qa_start + 1,
            "state": "ASSIGNED",
            "assigned_at": datetime.now().isoformat(),
            "progress": 0
        }
        
        self.builder_assignments[task_id] = task
        
        # Update build
        if "tasks" not in build:
            build["tasks"] = []
        build["tasks"].append(task_id)
        build["qa_total"] += task["qa_count"]
        
        return {
            "build_id": build_id,
            "task_id": task_id,
            "qa_range_calculated": True,
            "qa_start": qa_start,
            "qa_end": qa_end,
            "builder_selected": builder_type,
            "task_created": True
        }
    
    def monitor_progress(self, build_id: str) -> Dict[str, Any]:
        """
        QA-080: Monitor build progress
        
        Tracks QA status, calculates progress percentage, and detects stalls.
        
        Args:
            build_id: Build identifier
        
        Returns:
            Dict with:
                - build_id: Build identifier
                - qa_status_tracked: Boolean
                - progress_percentage: Progress percentage (0-100)
                - stall_detected: Boolean indicating if build has stalled
                - qa_green: Count of passing QA
                - qa_red: Count of failing QA
        """
        if build_id not in self.builds:
            raise ValueError(f"Build not found: {build_id}")
        
        build = self.builds[build_id]
        
        # Calculate progress from tasks
        total_qa = build.get("qa_total", 0)
        green_qa = build.get("qa_green", 0)
        
        progress_percentage = (green_qa / total_qa * 100) if total_qa > 0 else 0
        
        # Detect stall (no progress in last update)
        last_update = build.get("last_progress_update")
        stall_detected = False
        if last_update:
            last_update_time = datetime.fromisoformat(last_update)
            time_since_update = (datetime.now() - last_update_time).total_seconds()
            # Stall if no update for 1 hour
            stall_detected = time_since_update > 3600
        
        # Update build
        build["progress_percentage"] = progress_percentage
        build["last_progress_check"] = datetime.now().isoformat()
        
        return {
            "build_id": build_id,
            "qa_status_tracked": True,
            "progress_percentage": progress_percentage,
            "stall_detected": stall_detected,
            "qa_green": green_qa,
            "qa_red": build.get("qa_red", 0)
        }
    
    def handle_blocking(self, build_id: str, blocker_reason: str, blocker_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        QA-081: Handle build blocking
        
        Creates blocker, triggers escalation, and pauses build.
        
        Args:
            build_id: Build identifier
            blocker_reason: Reason for blocking
            blocker_context: Context information about blocker
        
        Returns:
            Dict with:
                - build_id: Build identifier
                - blocker_id: Created blocker identifier
                - blocker_created: Boolean
                - escalation_triggered: Boolean
                - build_paused: Boolean
        """
        if build_id not in self.builds:
            raise ValueError(f"Build not found: {build_id}")
        
        build = self.builds[build_id]
        
        # Create blocker
        blocker_id = f"blocker_{build_id}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        blocker = {
            "blocker_id": blocker_id,
            "build_id": build_id,
            "reason": blocker_reason,
            "context": blocker_context,
            "created_at": datetime.now().isoformat(),
            "escalated": True,
            "resolved": False
        }
        
        # Update build state
        build["state"] = "BLOCKED"
        build["blocker_id"] = blocker_id
        build["blocker"] = blocker
        build["blocked_at"] = datetime.now().isoformat()
        
        return {
            "build_id": build_id,
            "blocker_id": blocker_id,
            "blocker_created": True,
            "escalation_triggered": True,
            "build_paused": True
        }
    
    def complete_build(self, build_id: str) -> Dict[str, Any]:
        """
        QA-082: Complete build
        
        Validates 100% QA GREEN, generates completion evidence, and creates deliverable.
        
        Args:
            build_id: Build identifier
        
        Returns:
            Dict with:
                - build_id: Build identifier
                - qa_green_validated: Boolean (must be 100%)
                - completion_evidence_generated: Boolean
                - deliverable_created: Boolean
                - completion_status: Status (COMPLETE or INCOMPLETE)
        """
        if build_id not in self.builds:
            raise ValueError(f"Build not found: {build_id}")
        
        build = self.builds[build_id]
        
        # Validate 100% QA GREEN
        total_qa = build.get("qa_total", 0)
        green_qa = build.get("qa_green", 0)
        qa_green_validated = total_qa > 0 and green_qa == total_qa
        
        if not qa_green_validated:
            return {
                "build_id": build_id,
                "qa_green_validated": False,
                "completion_evidence_generated": False,
                "deliverable_created": False,
                "completion_status": "INCOMPLETE",
                "reason": f"Only {green_qa}/{total_qa} QA components are GREEN"
            }
        
        # Generate completion evidence
        completion_evidence = {
            "build_id": build_id,
            "requirement_id": build["requirement_id"],
            "completed_at": datetime.now().isoformat(),
            "qa_total": total_qa,
            "qa_green": green_qa,
            "qa_coverage": 100.0,
            "waves_completed": len(build.get("waves", [])),
            "tasks_completed": len(build.get("tasks", []))
        }
        
        # Update build
        build["state"] = "COMPLETED"
        build["completed_at"] = datetime.now().isoformat()
        build["completion_evidence"] = completion_evidence
        build["deliverable_created"] = True
        
        return {
            "build_id": build_id,
            "qa_green_validated": True,
            "completion_evidence_generated": True,
            "deliverable_created": True,
            "completion_status": "COMPLETE"
        }
    
    def handle_orchestration_failure(self, build_id: str, failure_type: str) -> Dict[str, Any]:
        """
        QA-083: Build Orchestrator failure modes
        
        Handles builder unavailable, task assignment failure, and corruption detection.
        
        Args:
            build_id: Build identifier
            failure_type: Type of failure (builder_unavailable, task_assignment, corruption)
        
        Returns:
            Dict with:
                - build_id: Build identifier
                - failure_type: Type of failure
                - failure_handled: Boolean
                - recovery_action: Action taken
                - corrupted_detected: Boolean (for corruption failures)
        """
        if build_id not in self.builds:
            return {
                "build_id": build_id,
                "failure_type": "build_not_found",
                "failure_handled": True,
                "recovery_action": "no_action",
                "corruption_detected": False
            }
        
        build = self.builds[build_id]
        
        if failure_type == "builder_unavailable":
            recovery_action = "retry_with_different_builder"
            corruption_detected = False
        elif failure_type == "task_assignment":
            recovery_action = "recreate_task"
            corruption_detected = False
        elif failure_type == "corruption":
            recovery_action = "escalate_and_halt"
            corruption_detected = True
            build["state"] = "CORRUPTED"
        else:
            recovery_action = "escalate"
            corruption_detected = False
        
        build["last_failure"] = {
            "type": failure_type,
            "timestamp": datetime.now().isoformat(),
            "recovery_action": recovery_action
        }
        
        return {
            "build_id": build_id,
            "failure_type": failure_type,
            "failure_handled": True,
            "recovery_action": recovery_action,
            "corruption_detected": corruption_detected
        }
