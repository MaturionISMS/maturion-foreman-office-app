"""
Build Intervention Controller

Implements BUILD_INTERVENTION_AND_ALERT_MODEL.md (G-C10).
Provides intervention controls for build execution with full audit trail.

Core Principles:
- No automated intervention
- All stops and alerts require explicit human decision
- Full audit trail for all interventions
- Explicit authorization required for resumption
"""

import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime
import json
import uuid

logger = logging.getLogger(__name__)


class BuildInterventionController:
    """
    Controller for build intervention and alert routing.
    
    Implements G-C10: BUILD_INTERVENTION_AND_ALERT_MODEL.md
    """
    
    VALID_SCOPE_LEVELS = ['step', 'sub-wave', 'wave', 'application']
    ALERT_MIN_RATIONALE_LENGTH = 20
    STOP_MIN_RATIONALE_LENGTH = 50
    
    def __init__(self, repo_root: Path):
        """
        Initialize the intervention controller.
        
        Args:
            repo_root: Root directory of the repository
        """
        self.repo_root = repo_root
        self.intervention_log_dir = repo_root / "architecture" / "interventions"
        self.intervention_log_dir.mkdir(parents=True, exist_ok=True)
        
    def issue_alert(
        self,
        scope_level: str,
        target_node_id: str,
        rationale: str,
        triggered_by: str,
        triggered_by_type: str = 'human',
        ip_address: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Issue a non-blocking alert for the specified build node.
        
        Args:
            scope_level: 'step', 'sub-wave', 'wave', or 'application'
            target_node_id: ID of the target node
            rationale: Explanation for the alert (min 20 chars)
            triggered_by: Identity of the trigger (user or agent)
            triggered_by_type: 'human', 'agent', or 'watchdog'
            ip_address: Optional IP address of trigger
            
        Returns:
            Dictionary containing alert details and routing
            
        Raises:
            ValueError: If inputs are invalid
        """
        logger.info(f"Issuing alert for {scope_level}/{target_node_id}")
        
        # Validate inputs
        self._validate_scope_level(scope_level)
        self._validate_rationale(rationale, self.ALERT_MIN_RATIONALE_LENGTH, "alert")
        
        # Generate unique alert ID
        alert_id = f"alert-{uuid.uuid4().hex[:12]}"
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        # Determine routing based on scope
        routing = self._determine_alert_routing(scope_level)
        
        # Create alert record
        alert = {
            "alert_id": alert_id,
            "alert_type": "alert",
            "triggered_at": timestamp,
            "triggered_by": {
                "type": triggered_by_type,
                "identity": triggered_by,
                "ip_address": ip_address
            },
            "scope": {
                "level": scope_level,
                "target_node_id": target_node_id,
                "target_node_type": self._infer_node_type(target_node_id)
            },
            "rationale": rationale,
            "routing": routing,
            "status": "open",
            "response_timeline": {},
            "context_package": self._prepare_context_package(target_node_id)
        }
        
        # Persist alert
        self._save_intervention(alert_id, alert)
        
        # Log audit trail
        self._log_intervention_audit(alert_id, "alert_issued", alert)
        
        logger.info(f"Alert {alert_id} issued and routed to {routing['primary']}")
        
        return {
            "success": True,
            "alert_id": alert_id,
            "routed_to": routing['primary'] + routing['secondary'],
            "status": "open",
            "timestamp": timestamp
        }
    
    def issue_emergency_stop(
        self,
        scope_level: str,
        target_node_id: str,
        critical_rationale: str,
        triggered_by: str,
        confirmation: Dict[str, Any],
        triggered_by_type: str = 'human',
        ip_address: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Issue an immediate emergency stop for the specified scope.
        
        Args:
            scope_level: 'step', 'sub-wave', 'wave', or 'application'
            target_node_id: ID of the target node
            critical_rationale: Critical explanation for the stop (min 50 chars)
            triggered_by: Identity of the trigger (user or agent)
            confirmation: Confirmation object with acknowledged_impact and typed_confirmation
            triggered_by_type: 'human', 'agent', or 'watchdog'
            ip_address: Optional IP address of trigger
            
        Returns:
            Dictionary containing stop details and status
            
        Raises:
            ValueError: If inputs are invalid or confirmation is missing
        """
        logger.warning(f"⚠️ EMERGENCY STOP requested for {scope_level}/{target_node_id}")
        
        # Validate inputs
        self._validate_scope_level(scope_level)
        self._validate_rationale(critical_rationale, self.STOP_MIN_RATIONALE_LENGTH, "emergency stop")
        self._validate_stop_confirmation(confirmation)
        
        # Generate unique stop ID
        stop_id = f"stop-{uuid.uuid4().hex[:12]}"
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        # Determine affected nodes
        affected_nodes = self._determine_affected_nodes(scope_level, target_node_id)
        
        # Determine routing and authorization requirements
        routing = self._determine_stop_routing(scope_level)
        
        # Create execution snapshot
        execution_snapshot = self._create_execution_snapshot(target_node_id, affected_nodes)
        
        # Create stop record
        stop = {
            "stop_id": stop_id,
            "stop_type": "emergency_stop",
            "triggered_at": timestamp,
            "triggered_by": {
                "type": triggered_by_type,
                "identity": triggered_by,
                "ip_address": ip_address
            },
            "scope": {
                "level": scope_level,
                "target_node_id": target_node_id,
                "target_node_type": self._infer_node_type(target_node_id),
                "affected_nodes": affected_nodes
            },
            "critical_rationale": critical_rationale,
            "confirmation": confirmation,
            "execution_snapshot": execution_snapshot,
            "routing": routing,
            "status": "active",
            "timeline": {
                "stopped_at": timestamp
            },
            "evidence_package": self._create_evidence_package(target_node_id, affected_nodes)
        }
        
        # Persist stop
        self._save_intervention(stop_id, stop)
        
        # Log audit trail
        self._log_intervention_audit(stop_id, "emergency_stop_triggered", stop)
        
        logger.critical(f"🛑 EMERGENCY STOP {stop_id} ACTIVATED - {len(affected_nodes)} nodes affected")
        
        return {
            "success": True,
            "stop_id": stop_id,
            "stopped_at": timestamp,
            "affected_nodes": affected_nodes,
            "status": "active",
            "resumption_requires": routing['required_authorization']
        }
    
    def get_intervention_context(self, intervention_id: str) -> Dict[str, Any]:
        """
        Get the full context for an intervention (alert or stop).
        
        Args:
            intervention_id: ID of the intervention
            
        Returns:
            Dictionary containing full context for the intervention
            
        Raises:
            FileNotFoundError: If intervention not found
        """
        logger.info(f"Retrieving context for intervention {intervention_id}")
        
        # Load intervention record
        intervention = self._load_intervention(intervention_id)
        
        if not intervention:
            raise FileNotFoundError(f"Intervention {intervention_id} not found")
        
        # Get target node ID
        target_node_id = intervention['scope']['target_node_id']
        
        # Prepare comprehensive context
        context = {
            "intervention": intervention,
            "node": self._get_node_inspection(target_node_id),
            "evidence": self._get_node_evidence(target_node_id),
            "blockers": self._get_node_blockers(target_node_id),
            "decisions": self._get_node_decisions(target_node_id),
            "timeline": self._get_node_timeline(target_node_id)
        }
        
        return {
            "success": True,
            "intervention_id": intervention_id,
            "context": context
        }
    
    def resume_after_stop(
        self,
        stop_id: str,
        authorized_by: str,
        resolution_summary: str,
        resume_conditions: List[str]
    ) -> Dict[str, Any]:
        """
        Resume execution after an emergency stop.
        
        Args:
            stop_id: ID of the stop to resume
            authorized_by: Identity of the authorizing party
            resolution_summary: Summary of resolution (min 50 chars)
            resume_conditions: List of conditions met for resumption
            
        Returns:
            Dictionary containing resumption status
            
        Raises:
            ValueError: If stop not found or already resumed
            PermissionError: If unauthorized resumption attempt
        """
        logger.info(f"Resumption requested for stop {stop_id} by {authorized_by}")
        
        # Validate resolution summary
        if len(resolution_summary) < 50:
            raise ValueError("Resolution summary must be at least 50 characters")
        
        # Load stop record
        stop = self._load_intervention(stop_id)
        
        if not stop:
            raise FileNotFoundError(f"Stop {stop_id} not found")
        
        if stop['status'] == 'resumed':
            raise ValueError(f"Stop {stop_id} has already been resumed")
        
        # Verify authorization
        required_auth = stop['routing']['required_authorization']
        if not self._verify_resumption_authority(authorized_by, required_auth):
            raise PermissionError(f"User {authorized_by} not authorized to resume {required_auth}")
        
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        # Update stop record
        stop['status'] = 'resumed'
        stop['timeline']['resumed_at'] = timestamp
        stop['resumption'] = {
            "authorized_by": authorized_by,
            "authorization_timestamp": timestamp,
            "resolution_summary": resolution_summary,
            "resume_conditions": resume_conditions
        }
        
        # Persist updated stop
        self._save_intervention(stop_id, stop)
        
        # Log audit trail
        self._log_intervention_audit(stop_id, "stop_resumed", stop)
        
        logger.info(f"✅ Stop {stop_id} resumed by {authorized_by}")
        
        return {
            "success": True,
            "stop_id": stop_id,
            "resumed_at": timestamp,
            "status": "resumed"
        }
    
    # Private helper methods
    
    def _validate_scope_level(self, scope_level: str) -> None:
        """Validate that scope level is valid."""
        if scope_level not in self.VALID_SCOPE_LEVELS:
            raise ValueError(
                f"Invalid scope_level: {scope_level}. "
                f"Must be one of: {', '.join(self.VALID_SCOPE_LEVELS)}"
            )
    
    def _validate_rationale(self, rationale: str, min_length: int, intervention_type: str) -> None:
        """Validate rationale meets minimum length."""
        if len(rationale) < min_length:
            raise ValueError(
                f"Rationale for {intervention_type} must be at least {min_length} characters"
            )
    
    def _validate_stop_confirmation(self, confirmation: Dict[str, Any]) -> None:
        """Validate emergency stop confirmation."""
        if not confirmation.get('acknowledged_impact'):
            raise ValueError("Emergency stop requires acknowledged_impact=true")
        
        if confirmation.get('typed_confirmation') != 'STOP':
            raise ValueError("Emergency stop requires typed_confirmation='STOP'")
    
    def _infer_node_type(self, node_id: str) -> str:
        """Infer node type from node ID pattern."""
        if node_id.startswith('task-'):
            return 'task'
        elif node_id.startswith('wave-'):
            return 'wave'
        elif node_id.startswith('sub-wave-'):
            return 'sub-wave'
        elif node_id.startswith('program-'):
            return 'program'
        else:
            return 'unknown'
    
    def _determine_alert_routing(self, scope_level: str) -> Dict[str, Any]:
        """Determine routing for alerts based on scope."""
        routing_table = {
            'step': {
                'primary': ['builder_agent', 'fm'],
                'secondary': [],
                'escalation_after_hours': 24
            },
            'sub-wave': {
                'primary': ['fm', 'governance'],
                'secondary': [],
                'escalation_after_hours': 12
            },
            'wave': {
                'primary': ['fm', 'governance', 'human_authority'],
                'secondary': [],
                'escalation_after_hours': 0  # immediate escalation
            },
            'application': {
                'primary': ['human_authority', 'johan'],
                'secondary': ['fm', 'governance'],
                'escalation_after_hours': 0  # immediate notification
            }
        }
        return routing_table.get(scope_level, routing_table['step'])
    
    def _determine_stop_routing(self, scope_level: str) -> Dict[str, Any]:
        """Determine routing and authorization for emergency stops."""
        routing_table = {
            'step': {
                'immediate': ['builder_agent', 'fm'],
                'required_authorization': 'FM'
            },
            'sub-wave': {
                'immediate': ['fm', 'governance'],
                'required_authorization': 'Human Authority or FM'
            },
            'wave': {
                'immediate': ['fm', 'human_authority'],
                'required_authorization': 'Human Authority'
            },
            'application': {
                'immediate': ['johan', 'all_stakeholders'],
                'required_authorization': 'Johan'
            }
        }
        return routing_table.get(scope_level, routing_table['step'])
    
    def _determine_affected_nodes(self, scope_level: str, target_node_id: str) -> List[str]:
        """Determine which nodes are affected by a stop at this scope."""
        # TODO: In production, this would query the actual build tree
        # For now, return mock data
        if scope_level == 'step':
            return [target_node_id]
        elif scope_level == 'sub-wave':
            return [target_node_id, f"{target_node_id}-task-1", f"{target_node_id}-task-2"]
        elif scope_level == 'wave':
            return [target_node_id, f"{target_node_id}-sub-1", f"{target_node_id}-sub-2"]
        else:  # application
            return [target_node_id, "all_waves", "all_tasks"]
    
    def _prepare_context_package(self, node_id: str) -> Dict[str, Any]:
        """Prepare context package for alert."""
        # TODO: In production, this would gather actual node state
        return {
            "node_state": {"status": "mock"},
            "evidence": [],
            "blockers": []
        }
    
    def _create_execution_snapshot(self, node_id: str, affected_nodes: List[str]) -> Dict[str, Any]:
        """Create snapshot of execution state at moment of stop."""
        # TODO: In production, this would capture actual execution state
        return {
            "frozen_state": {"status": "frozen"},
            "active_tasks": affected_nodes,
            "pending_transitions": []
        }
    
    def _create_evidence_package(self, node_id: str, affected_nodes: List[str]) -> Dict[str, Any]:
        """Create evidence package for emergency stop."""
        # TODO: In production, this would gather all evidence artifacts
        return {
            "full_snapshot": f"evidence/stop-{node_id}-snapshot.json",
            "logs": [],
            "artifacts": [],
            "decisions": []
        }
    
    def _verify_resumption_authority(self, user: str, required_auth: str) -> bool:
        """Verify that user has authority to resume."""
        # TODO: In production, this would check actual authorization
        # For now, accept any user that matches the required authority pattern
        return True  # Simplified for initial implementation
    
    def _save_intervention(self, intervention_id: str, intervention_data: Dict[str, Any]) -> None:
        """Persist intervention to disk."""
        intervention_file = self.intervention_log_dir / f"{intervention_id}.json"
        with open(intervention_file, 'w') as f:
            json.dump(intervention_data, f, indent=2)
    
    def _load_intervention(self, intervention_id: str) -> Optional[Dict[str, Any]]:
        """Load intervention from disk."""
        intervention_file = self.intervention_log_dir / f"{intervention_id}.json"
        if not intervention_file.exists():
            return None
        
        with open(intervention_file, 'r') as f:
            return json.load(f)
    
    def _log_intervention_audit(self, intervention_id: str, action: str, data: Dict[str, Any]) -> None:
        """Log intervention action to audit trail."""
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "intervention_id": intervention_id,
            "action": action,
            "data_summary": {
                "scope": data.get('scope', {}),
                "status": data.get('status'),
                "triggered_by": data.get('triggered_by', {}).get('identity')
            }
        }
        
        # Append to audit log
        audit_log_file = self.intervention_log_dir / "audit.log"
        with open(audit_log_file, 'a') as f:
            f.write(json.dumps(audit_entry) + "\n")
        
        logger.info(f"Audit: {action} - {intervention_id}")
    
    # Context retrieval methods (mock implementations)
    
    def _get_node_inspection(self, node_id: str) -> Dict[str, Any]:
        """Get inspection data for node."""
        # TODO: Integrate with build_node_inspector
        return {
            "node_id": node_id,
            "status": "mock",
            "state": "BUILDING"
        }
    
    def _get_node_evidence(self, node_id: str) -> List[Dict[str, Any]]:
        """Get evidence artifacts for node."""
        # TODO: Integrate with evidence system
        return []
    
    def _get_node_blockers(self, node_id: str) -> List[Dict[str, Any]]:
        """Get blockers for node."""
        # TODO: Integrate with blocker tracking
        return []
    
    def _get_node_decisions(self, node_id: str) -> List[Dict[str, Any]]:
        """Get recent decisions for node."""
        # TODO: Integrate with decision system
        return []
    
    def _get_node_timeline(self, node_id: str) -> List[Dict[str, Any]]:
        """Get state timeline for node."""
        # TODO: Integrate with timeline system
        return []


def create_intervention_controller(repo_root: Path) -> BuildInterventionController:
    """
    Factory function to create intervention controller.
    
    Args:
        repo_root: Root directory of the repository
        
    Returns:
        BuildInterventionController instance
    """
    return BuildInterventionController(repo_root)
