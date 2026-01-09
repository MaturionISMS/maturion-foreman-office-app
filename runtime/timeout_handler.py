"""
Timeout Handler

Purpose: Handle operation timeouts with graceful degradation and recovery
Authority: Wave 2.0 Subwave 2.11 - Complex Failure Modes Phase 1 (QA-246 to QA-250)
QA Coverage: QA-246 to QA-250
Tenant Isolation: All operations scoped by organisation_id

Timeout Handling:
- QA-246: Intent rework timeout (CLARIFIED → RECEIVED with context preservation)
- QA-247: Requirement spec approval timeout (DRAFT → PENDING_APPROVAL)
- QA-248: Requirement approval decision timeout (PENDING_APPROVAL → APPROVED)
- QA-249: Requirement rejection timeout (PENDING_APPROVAL → REJECTED)
- QA-250: Conditional approval timeout (PENDING_APPROVAL → CONDITIONAL)
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
import threading
import time


class TimeoutAction(Enum):
    """Actions to take when timeout occurs"""
    ESCALATE = "escalate"  # Escalate to human
    RETRY = "retry"  # Retry operation
    FAIL_GRACEFULLY = "fail_gracefully"  # Fail with cleanup
    USE_DEFAULT = "use_default"  # Use default value/behavior
    EXTEND = "extend"  # Extend timeout


class TimeoutState(Enum):
    """Timeout monitoring states"""
    ACTIVE = "active"
    TRIGGERED = "triggered"
    HANDLED = "handled"
    CANCELLED = "cancelled"


@dataclass
class TimeoutConfig:
    """Timeout configuration"""
    operation_id: str
    timeout_seconds: int
    action: TimeoutAction
    default_value: Optional[Any] = None
    max_extensions: int = 2
    extension_count: int = 0
    callback: Optional[Callable] = None


@dataclass
class TimeoutRecord:
    """Record of timeout event"""
    operation_id: str
    operation_type: str
    organisation_id: str
    timeout_seconds: int
    started_at: datetime
    triggered_at: Optional[datetime] = None
    handled_at: Optional[datetime] = None
    state: TimeoutState = TimeoutState.ACTIVE
    action_taken: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)
    audit_trail: List[Dict[str, Any]] = field(default_factory=list)


class TimeoutHandler:
    """
    Handles operation timeouts with graceful degradation
    
    Implements QA-246 to QA-250:
    - Intent rework with context preservation
    - Requirement state transition timeouts
    - Timeout escalation and recovery
    - Iteration tracking for rework
    - Conditional timeout handling
    """
    
    def __init__(self, organisation_id: str):
        """
        Initialize timeout handler
        
        Args:
            organisation_id: Organisation ID for tenant isolation
        """
        self.organisation_id = organisation_id
        self._timeouts: Dict[str, TimeoutRecord] = {}
        self._configs: Dict[str, TimeoutConfig] = {}
        self._timeout_history: List[TimeoutRecord] = []
        self._monitoring_threads: Dict[str, threading.Thread] = {}
        self._stop_monitoring = threading.Event()
        
    def start_timeout_monitoring(
        self,
        operation_id: str,
        operation_type: str,
        timeout_seconds: int,
        action: TimeoutAction = TimeoutAction.ESCALATE,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        QA-246, QA-247: Start monitoring operation timeout
        
        For QA-246 (Intent rework): Monitors CLARIFIED → RECEIVED transition
        For QA-247 (Requirement approval): Monitors DRAFT → PENDING_APPROVAL transition
        
        Args:
            operation_id: Operation identifier
            operation_type: Type of operation (e.g., 'intent_rework', 'requirement_approval')
            timeout_seconds: Timeout duration in seconds
            action: Action to take on timeout
            context: Operation context (including state, iteration count, etc.)
            
        Returns:
            Dict with:
                - operation_id: Operation identifier
                - monitoring_started: Boolean
                - timeout_seconds: Configured timeout
                - expires_at: ISO timestamp of expiration
        """
        # Create timeout record
        record = TimeoutRecord(
            operation_id=operation_id,
            operation_type=operation_type,
            organisation_id=self.organisation_id,
            timeout_seconds=timeout_seconds,
            started_at=datetime.now(timezone.utc),
            context=context or {}
        )
        
        # Create config
        config = TimeoutConfig(
            operation_id=operation_id,
            timeout_seconds=timeout_seconds,
            action=action
        )
        
        # Store
        self._timeouts[operation_id] = record
        self._configs[operation_id] = config
        
        # Start monitoring thread
        monitor_thread = threading.Thread(
            target=self._monitor_timeout,
            args=(operation_id,),
            daemon=True
        )
        self._monitoring_threads[operation_id] = monitor_thread
        monitor_thread.start()
        
        # Audit trail
        record.audit_trail.append({
            "action": "monitoring_started",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "timeout_seconds": timeout_seconds,
            "action_on_timeout": action.value
        })
        
        expires_at = record.started_at + timedelta(seconds=timeout_seconds)
        
        return {
            "operation_id": operation_id,
            "monitoring_started": True,
            "timeout_seconds": timeout_seconds,
            "expires_at": expires_at.isoformat(),
            "organisation_id": self.organisation_id
        }
    
    def handle_state_transition_timeout(
        self,
        operation_id: str,
        from_state: str,
        to_state: str,
        entity_type: str,
        entity_id: str,
        preserve_context: bool = True
    ) -> Dict[str, Any]:
        """
        QA-246, QA-248, QA-249, QA-250: Handle state transition timeout
        
        - QA-246: CLARIFIED → RECEIVED (rework with context preservation)
        - QA-248: PENDING_APPROVAL → APPROVED (approval decision)
        - QA-249: PENDING_APPROVAL → REJECTED (rejection decision)
        - QA-250: PENDING_APPROVAL → CONDITIONAL (conditional approval)
        
        Args:
            operation_id: Operation identifier
            from_state: Source state
            to_state: Target state
            entity_type: Type of entity ('intent', 'requirement', etc.)
            entity_id: Entity identifier
            preserve_context: Whether to preserve context (for rework scenarios)
            
        Returns:
            Dict with:
                - timeout_handled: Boolean
                - context_preserved: Boolean (for QA-246)
                - iteration_tracked: Boolean (for rework)
                - escalation_triggered: Boolean
                - recovery_action: Action taken
        """
        if operation_id not in self._timeouts:
            return {
                "timeout_handled": False,
                "error": "Operation not found"
            }
        
        record = self._timeouts[operation_id]
        config = self._configs[operation_id]
        
        # Mark as triggered
        record.state = TimeoutState.TRIGGERED
        record.triggered_at = datetime.now(timezone.utc)
        
        # Determine action based on config and context
        action_result = self._execute_timeout_action(
            config,
            record,
            from_state,
            to_state,
            entity_type,
            entity_id
        )
        
        # Track iteration for rework scenarios (QA-246)
        iteration_tracked = False
        if to_state == "RECEIVED" and from_state == "CLARIFIED":
            iteration_tracked = self._track_rework_iteration(
                entity_id,
                record.context
            )
        
        # Preserve context if requested (critical for QA-246)
        context_preserved = False
        if preserve_context:
            context_preserved = self._preserve_operation_context(
                operation_id,
                record.context
            )
        
        # Mark as handled
        record.state = TimeoutState.HANDLED
        record.handled_at = datetime.now(timezone.utc)
        record.action_taken = action_result["action"]
        
        # Audit trail
        record.audit_trail.append({
            "action": "timeout_handled",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "from_state": from_state,
            "to_state": to_state,
            "action_taken": action_result["action"],
            "context_preserved": context_preserved,
            "iteration_tracked": iteration_tracked
        })
        
        return {
            "timeout_handled": True,
            "context_preserved": context_preserved,
            "iteration_tracked": iteration_tracked,
            "escalation_triggered": action_result["escalated"],
            "recovery_action": action_result["action"],
            "operation_id": operation_id,
            "organisation_id": self.organisation_id
        }
    
    def extend_timeout(
        self,
        operation_id: str,
        additional_seconds: int
    ) -> Dict[str, Any]:
        """
        Extend timeout for an operation
        
        Args:
            operation_id: Operation identifier
            additional_seconds: Additional time to add
            
        Returns:
            Dict with extension result
        """
        if operation_id not in self._timeouts:
            return {
                "extended": False,
                "error": "Operation not found"
            }
        
        record = self._timeouts[operation_id]
        config = self._configs[operation_id]
        
        # Check if extension allowed
        if config.extension_count >= config.max_extensions:
            return {
                "extended": False,
                "error": "Max extensions reached",
                "max_extensions": config.max_extensions
            }
        
        # Extend timeout
        config.timeout_seconds += additional_seconds
        config.extension_count += 1
        
        # Audit trail
        record.audit_trail.append({
            "action": "timeout_extended",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "additional_seconds": additional_seconds,
            "new_timeout": config.timeout_seconds,
            "extension_count": config.extension_count
        })
        
        new_expires_at = record.started_at + timedelta(seconds=config.timeout_seconds)
        
        return {
            "extended": True,
            "additional_seconds": additional_seconds,
            "new_timeout": config.timeout_seconds,
            "extension_count": config.extension_count,
            "max_extensions": config.max_extensions,
            "new_expires_at": new_expires_at.isoformat()
        }
    
    def cancel_timeout_monitoring(self, operation_id: str) -> Dict[str, Any]:
        """
        Cancel timeout monitoring (operation completed successfully)
        
        Args:
            operation_id: Operation identifier
            
        Returns:
            Dict with cancellation result
        """
        if operation_id not in self._timeouts:
            return {
                "cancelled": False,
                "error": "Operation not found"
            }
        
        record = self._timeouts[operation_id]
        record.state = TimeoutState.CANCELLED
        
        # Stop monitoring thread
        if operation_id in self._monitoring_threads:
            # Thread will exit on next check
            pass
        
        # Move to history
        self._timeout_history.append(record)
        del self._timeouts[operation_id]
        del self._configs[operation_id]
        
        # Audit trail
        record.audit_trail.append({
            "action": "monitoring_cancelled",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "reason": "operation_completed"
        })
        
        return {
            "cancelled": True,
            "operation_id": operation_id,
            "duration_seconds": (
                (datetime.now(timezone.utc) - record.started_at).total_seconds()
            )
        }
    
    def get_timeout_status(self, operation_id: str) -> Optional[Dict[str, Any]]:
        """
        Get current timeout status
        
        Args:
            operation_id: Operation identifier
            
        Returns:
            Dict with timeout status or None if not found
        """
        if operation_id in self._timeouts:
            record = self._timeouts[operation_id]
            config = self._configs[operation_id]
            
            elapsed = (datetime.now(timezone.utc) - record.started_at).total_seconds()
            remaining = max(0, config.timeout_seconds - elapsed)
            
            return {
                "operation_id": operation_id,
                "state": record.state.value,
                "elapsed_seconds": elapsed,
                "remaining_seconds": remaining,
                "timeout_seconds": config.timeout_seconds,
                "extensions_used": config.extension_count,
                "max_extensions": config.max_extensions,
                "organisation_id": record.organisation_id
            }
        
        # Check history
        for record in self._timeout_history:
            if record.operation_id == operation_id:
                return {
                    "operation_id": operation_id,
                    "state": record.state.value,
                    "completed": True,
                    "organisation_id": record.organisation_id
                }
        
        return None
    
    # Private helper methods
    
    def _monitor_timeout(self, operation_id: str):
        """Monitor timeout in background thread"""
        
        if operation_id not in self._configs:
            return
        
        config = self._configs[operation_id]
        
        # Wait for timeout
        elapsed = 0
        check_interval = 1  # Check every second
        
        while elapsed < config.timeout_seconds:
            if self._stop_monitoring.is_set():
                return
            
            # Check if operation cancelled or completed
            if operation_id not in self._timeouts:
                return
            
            if self._timeouts[operation_id].state != TimeoutState.ACTIVE:
                return
            
            time.sleep(check_interval)
            elapsed += check_interval
        
        # Timeout occurred
        if operation_id in self._timeouts:
            record = self._timeouts[operation_id]
            if record.state == TimeoutState.ACTIVE:
                self._trigger_timeout(operation_id)
    
    def _trigger_timeout(self, operation_id: str):
        """Trigger timeout handling"""
        
        if operation_id not in self._timeouts:
            return
        
        record = self._timeouts[operation_id]
        config = self._configs[operation_id]
        
        # Execute callback if provided
        if config.callback:
            try:
                config.callback(operation_id)
            except Exception as e:
                record.audit_trail.append({
                    "action": "callback_failed",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "error": str(e)
                })
    
    def _execute_timeout_action(
        self,
        config: TimeoutConfig,
        record: TimeoutRecord,
        from_state: str,
        to_state: str,
        entity_type: str,
        entity_id: str
    ) -> Dict[str, Any]:
        """Execute configured timeout action"""
        
        if config.action == TimeoutAction.ESCALATE:
            # Escalate to human for decision
            return {
                "action": "escalated",
                "escalated": True,
                "details": f"Timeout on {entity_type} {entity_id} transition {from_state} → {to_state}"
            }
        
        elif config.action == TimeoutAction.RETRY:
            # Retry the operation
            return {
                "action": "retry",
                "escalated": False,
                "details": "Operation will be retried"
            }
        
        elif config.action == TimeoutAction.FAIL_GRACEFULLY:
            # Fail with cleanup
            return {
                "action": "failed_gracefully",
                "escalated": False,
                "details": "Operation failed with cleanup"
            }
        
        elif config.action == TimeoutAction.USE_DEFAULT:
            # Use default behavior
            return {
                "action": "default_used",
                "escalated": False,
                "default_value": config.default_value
            }
        
        elif config.action == TimeoutAction.EXTEND:
            # Auto-extend if allowed
            if config.extension_count < config.max_extensions:
                config.timeout_seconds += 60  # Add 1 minute
                config.extension_count += 1
                return {
                    "action": "extended",
                    "escalated": False,
                    "new_timeout": config.timeout_seconds
                }
        
        # Default: escalate
        return {
            "action": "escalated",
            "escalated": True
        }
    
    def _track_rework_iteration(
        self,
        entity_id: str,
        context: Dict[str, Any]
    ) -> bool:
        """Track rework iteration count"""
        
        if "iteration_count" not in context:
            context["iteration_count"] = 1
        else:
            context["iteration_count"] += 1
        
        context["last_rework_at"] = datetime.now(timezone.utc).isoformat()
        
        return True
    
    def _preserve_operation_context(
        self,
        operation_id: str,
        context: Dict[str, Any]
    ) -> bool:
        """Preserve operation context for recovery"""
        
        # Context is already stored in the record
        # This method ensures it's marked as preserved
        context["preserved_at"] = datetime.now(timezone.utc).isoformat()
        context["preserved"] = True
        
        return True
    
    def shutdown(self):
        """Shutdown timeout handler and stop all monitoring"""
        self._stop_monitoring.set()
        
        # Wait for threads to finish
        for thread in self._monitoring_threads.values():
            if thread.is_alive():
                thread.join(timeout=5)
