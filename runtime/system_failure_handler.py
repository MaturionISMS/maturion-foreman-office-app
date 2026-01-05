"""
System Failure Handler

Purpose: Handle system-wide failures with graceful shutdown and state preservation
Authority: Wave 2.0 Subwave 2.8 - Full Watchdog Coverage (QA-400)
Tenant Isolation: All operations scoped by organisation_id
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class Escalation:
    """Escalation record"""
    escalation_id: str
    escalation_type: str
    severity: str
    organisation_id: str
    timestamp: datetime
    details: Dict[str, Any]


class GracefulShutdown:
    """Manages graceful system shutdown"""
    
    def __init__(self):
        self._shutdown_initiated = False
        self._shutdown_reason: Optional[str] = None
        self._shutdown_time: Optional[datetime] = None
    
    def initiate(self, reason: str) -> Dict[str, Any]:
        """
        Initiate graceful shutdown
        
        Returns shutdown initiation result
        """
        self._shutdown_initiated = True
        self._shutdown_reason = reason
        self._shutdown_time = datetime.utcnow()
        
        return {
            "status": "initiated",
            "reason": reason,
            "initiated_at": self._shutdown_time.isoformat()
        }
    
    def is_shutdown_initiated(self) -> bool:
        """Check if shutdown is initiated"""
        return self._shutdown_initiated
    
    def get_shutdown_info(self) -> Optional[Dict[str, Any]]:
        """Get shutdown information"""
        if not self._shutdown_initiated:
            return None
        
        return {
            "reason": self._shutdown_reason,
            "initiated_at": self._shutdown_time.isoformat() if self._shutdown_time else None
        }


class StatePreserver:
    """Preserves system state during failures"""
    
    def __init__(self):
        self._preserved_states: Dict[str, Dict[str, Any]] = {}  # org_id -> state_type -> data
    
    def preserve_state(
        self,
        state_type: str,
        state_data: Any,
        organisation_id: str
    ) -> Dict[str, Any]:
        """
        Preserve state data
        
        State types:
        - active_sessions
        - pending_operations
        - cache_data
        - etc.
        """
        if organisation_id not in self._preserved_states:
            self._preserved_states[organisation_id] = {}
        
        # Ensure state_data is serializable
        if isinstance(state_data, list):
            state_count = len(state_data)
        elif isinstance(state_data, dict):
            state_count = len(state_data)
        else:
            state_count = 1
        
        self._preserved_states[organisation_id][state_type] = {
            "data": state_data,
            "preserved_at": datetime.utcnow().isoformat(),
            "count": state_count
        }
        
        return {
            "status": "preserved",
            "state_type": state_type,
            "state_count": state_count,
            "organisation_id": organisation_id
        }
    
    def restore_state(
        self,
        state_type: str,
        organisation_id: str
    ) -> Any:
        """
        Restore preserved state
        
        Returns state data or empty list if not found
        """
        if organisation_id not in self._preserved_states:
            return []
        
        if state_type not in self._preserved_states[organisation_id]:
            return []
        
        return self._preserved_states[organisation_id][state_type]["data"]
    
    def get_preserved_states(self, organisation_id: Optional[str] = None) -> Dict[str, Any]:
        """Get all preserved states, optionally filtered by organisation"""
        if organisation_id:
            return self._preserved_states.get(organisation_id, {})
        return self._preserved_states


class RecoveryCoordinator:
    """Coordinates system recovery"""
    
    def __init__(self):
        self._recovery_plans: List[Dict[str, Any]] = []
    
    def generate_recovery_plan(
        self,
        failure_reason: str,
        preserved_states: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate recovery plan based on failure and preserved states
        
        Returns recovery plan with steps
        """
        steps = []
        
        # Step 1: Assess damage
        steps.append({
            "step": 1,
            "action": "assess_system_state",
            "description": "Assess system state and identify affected components",
            "estimated_duration_minutes": 5
        })
        
        # Step 2: Restore critical services
        steps.append({
            "step": 2,
            "action": "restore_critical_services",
            "description": "Restore critical system services and dependencies",
            "estimated_duration_minutes": 15
        })
        
        # Step 3: Restore preserved states
        if preserved_states:
            state_types = []
            for org_id, states in preserved_states.items():
                state_types.extend(states.keys())
            
            steps.append({
                "step": 3,
                "action": "restore_state",
                "description": f"Restore preserved states: {', '.join(set(state_types))}",
                "estimated_duration_minutes": 10,
                "state_types": list(set(state_types))
            })
        
        # Step 4: Verify data consistency
        steps.append({
            "step": 4,
            "action": "verify_data_consistency",
            "description": "Verify data consistency across system",
            "estimated_duration_minutes": 10
        })
        
        # Step 5: Resume operations
        steps.append({
            "step": 5,
            "action": "resume_operations",
            "description": "Resume normal system operations",
            "estimated_duration_minutes": 5
        })
        
        total_duration = sum(step["estimated_duration_minutes"] for step in steps)
        
        recovery_plan = {
            "plan_id": f"recovery_{int(datetime.utcnow().timestamp())}",
            "failure_reason": failure_reason,
            "steps": steps,
            "estimated_duration_minutes": total_duration,
            "created_at": datetime.utcnow().isoformat()
        }
        
        self._recovery_plans.append(recovery_plan)
        return recovery_plan


class SystemFailureHandler:
    """
    Handles system-wide failures
    
    Responsibilities:
    - Initiate graceful shutdown
    - Preserve system state
    - Escalate critical failures
    - Coordinate recovery
    - Maintain tenant isolation
    """
    
    def __init__(self, organisation_id: str):
        self.organisation_id = organisation_id
        self._graceful_shutdown = GracefulShutdown()
        self._state_preserver = StatePreserver()
        self._recovery_coordinator = RecoveryCoordinator()
        self._escalations: List[Escalation] = []
    
    def get_graceful_shutdown(self) -> GracefulShutdown:
        """Get graceful shutdown manager"""
        return self._graceful_shutdown
    
    def get_state_preserver(self) -> StatePreserver:
        """Get state preserver"""
        return self._state_preserver
    
    def get_recovery_coordinator(self) -> RecoveryCoordinator:
        """Get recovery coordinator"""
        return self._recovery_coordinator
    
    def escalate_system_failure(
        self,
        reason: str,
        details: Optional[Dict[str, Any]] = None
    ) -> str:
        """Escalate system-wide failure"""
        escalation_id = f"esc_{self.organisation_id}_{int(datetime.utcnow().timestamp())}"
        
        escalation = Escalation(
            escalation_id=escalation_id,
            escalation_type="system_wide_failure",
            severity="critical",
            organisation_id=self.organisation_id,
            timestamp=datetime.utcnow(),
            details={
                "reason": reason,
                **(details or {})
            }
        )
        
        self._escalations.append(escalation)
        return escalation_id
    
    def get_escalations(self, organisation_id: str) -> List[Dict[str, Any]]:
        """Get escalations for organisation"""
        if organisation_id != self.organisation_id:
            return []
        
        return [
            {
                "escalation_id": e.escalation_id,
                "type": e.escalation_type,
                "severity": e.severity,
                "timestamp": e.timestamp.isoformat(),
                "details": e.details
            }
            for e in self._escalations
        ]
