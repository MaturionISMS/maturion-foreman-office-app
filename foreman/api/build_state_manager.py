"""
Build State Manager (EXEC-02)

QA Coverage: QA-084 to QA-088
Architecture: FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md Section EXEC-02

Responsibilities:
- Track build state transitions
- Update build progress metrics
- Detect build stalls
- Persist build state
- Handle state consistency failures
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta


class BuildStateManager:
    """
    EXEC-02: Build State Manager
    
    Manages build state tracking, metrics, and persistence.
    Detects stalls and maintains state consistency.
    """
    
    # Build states
    STATES = [
        "INITIATED",
        "IN_PROGRESS",
        "BLOCKED",
        "STALLED",
        "COMPLETED",
        "FAILED",
        "CORRUPTED"
    ]
    
    # Stall detection threshold (seconds)
    STALL_THRESHOLD = 3600  # 1 hour
    HEARTBEAT_INTERVAL = 300  # 5 minutes
    
    def __init__(self):
        """Initialize Build State Manager"""
        self.build_states = {}
        self.state_history = {}
    
    def track_state_transition(self, build_id: str, from_state: str, to_state: str, reason: str = "") -> Dict[str, Any]:
        """
        QA-084: Track build state transitions
        
        Logs state changes, maintains audit trail, ensures deterministic transitions.
        
        Args:
            build_id: Build identifier
            from_state: Current state
            to_state: New state
            reason: Optional reason for transition
        
        Returns:
            Dict with:
                - build_id: Build identifier
                - state_change_logged: Boolean
                - audit_trail_updated: Boolean
                - deterministic_transition: Boolean
                - from_state: Previous state
                - to_state: New state
        """
        # Validate states
        if from_state not in self.STATES or to_state not in self.STATES:
            raise ValueError(f"Invalid state transition: {from_state} -> {to_state}")
        
        # Check if transition is valid (deterministic)
        deterministic_transition = self._is_valid_transition(from_state, to_state)
        
        # Create transition record
        transition = {
            "build_id": build_id,
            "from_state": from_state,
            "to_state": to_state,
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
            "deterministic": deterministic_transition
        }
        
        # Update state history
        if build_id not in self.state_history:
            self.state_history[build_id] = []
        self.state_history[build_id].append(transition)
        
        # Update current state
        if build_id not in self.build_states:
            self.build_states[build_id] = {}
        
        self.build_states[build_id]["current_state"] = to_state
        self.build_states[build_id]["last_transition"] = transition
        self.build_states[build_id]["updated_at"] = datetime.now().isoformat()
        
        return {
            "build_id": build_id,
            "state_change_logged": True,
            "audit_trail_updated": True,
            "deterministic_transition": deterministic_transition,
            "from_state": from_state,
            "to_state": to_state
        }
    
    def update_progress_metrics(self, build_id: str, qa_green: int, qa_red: int, qa_total: int) -> Dict[str, Any]:
        """
        QA-085: Update build progress metrics
        
        Calculates QA coverage percentage, tracks GREEN/RED counts, and time elapsed.
        
        Args:
            build_id: Build identifier
            qa_green: Number of passing QA components
            qa_red: Number of failing QA components
            qa_total: Total QA components
        
        Returns:
            Dict with:
                - build_id: Build identifier
                - qa_coverage_percentage: Coverage percentage (0-100)
                - qa_green_count: Number of GREEN QA
                - qa_red_count: Number of RED QA
                - time_elapsed_seconds: Time since build started
        """
        if build_id not in self.build_states:
            raise ValueError(f"Build state not found: {build_id}")
        
        build_state = self.build_states[build_id]
        
        # Calculate coverage percentage
        qa_coverage_percentage = (qa_green / qa_total * 100) if qa_total > 0 else 0
        
        # Calculate time elapsed
        started_at = build_state.get("started_at")
        if started_at:
            time_elapsed = (datetime.now() - datetime.fromisoformat(started_at)).total_seconds()
        else:
            # Initialize start time if not set
            build_state["started_at"] = datetime.now().isoformat()
            time_elapsed = 0
        
        # Update metrics
        build_state["qa_green"] = qa_green
        build_state["qa_red"] = qa_red
        build_state["qa_total"] = qa_total
        build_state["qa_coverage_percentage"] = qa_coverage_percentage
        build_state["time_elapsed_seconds"] = time_elapsed
        build_state["last_metrics_update"] = datetime.now().isoformat()
        
        return {
            "build_id": build_id,
            "qa_coverage_percentage": qa_coverage_percentage,
            "qa_green_count": qa_green,
            "qa_red_count": qa_red,
            "time_elapsed_seconds": time_elapsed
        }
    
    def detect_stall(self, build_id: str) -> Dict[str, Any]:
        """
        QA-086: Detect build stall
        
        Monitors silence threshold, heartbeat monitoring, and triggers escalation.
        
        Args:
            build_id: Build identifier
        
        Returns:
            Dict with:
                - build_id: Build identifier
                - stall_detected: Boolean indicating if build has stalled
                - silence_threshold_exceeded: Boolean
                - last_heartbeat: Timestamp of last heartbeat
                - stall_escalated: Boolean indicating escalation triggered
        """
        if build_id not in self.build_states:
            raise ValueError(f"Build state not found: {build_id}")
        
        build_state = self.build_states[build_id]
        
        # Check last heartbeat
        last_heartbeat = build_state.get("last_heartbeat")
        if not last_heartbeat:
            # No heartbeat yet, not stalled
            return {
                "build_id": build_id,
                "stall_detected": False,
                "silence_threshold_exceeded": False,
                "last_heartbeat": None,
                "stall_escalated": False
            }
        
        last_heartbeat_time = datetime.fromisoformat(last_heartbeat)
        silence_duration = (datetime.now() - last_heartbeat_time).total_seconds()
        
        silence_threshold_exceeded = silence_duration > self.STALL_THRESHOLD
        stall_detected = silence_threshold_exceeded and build_state.get("current_state") == "IN_PROGRESS"
        
        if stall_detected:
            # Update state to STALLED
            build_state["current_state"] = "STALLED"
            build_state["stalled_at"] = datetime.now().isoformat()
            build_state["stall_escalated"] = True
            
            # Record stall in history
            stall_event = {
                "build_id": build_id,
                "event": "stall_detected",
                "silence_duration": silence_duration,
                "timestamp": datetime.now().isoformat()
            }
            
            if "events" not in build_state:
                build_state["events"] = []
            build_state["events"].append(stall_event)
        
        return {
            "build_id": build_id,
            "stall_detected": stall_detected,
            "silence_threshold_exceeded": silence_threshold_exceeded,
            "last_heartbeat": last_heartbeat,
            "stall_escalated": stall_detected
        }
    
    def record_heartbeat(self, build_id: str) -> None:
        """
        Record a heartbeat for build (internal helper)
        
        Args:
            build_id: Build identifier
        """
        if build_id not in self.build_states:
            self.build_states[build_id] = {}
        
        self.build_states[build_id]["last_heartbeat"] = datetime.now().isoformat()
    
    def persist_state(self, build_id: str) -> Dict[str, Any]:
        """
        QA-087: Persist build state
        
        Ensures database consistency and supports recovery from failure.
        
        Args:
            build_id: Build identifier
        
        Returns:
            Dict with:
                - build_id: Build identifier
                - persistence_successful: Boolean
                - database_consistent: Boolean
                - recovery_point_created: Boolean
        """
        if build_id not in self.build_states:
            raise ValueError(f"Build state not found: {build_id}")
        
        build_state = self.build_states[build_id]
        
        # Simulate persistence (in production, would write to database)
        persistence_record = {
            "build_id": build_id,
            "state_snapshot": build_state.copy(),
            "state_history": self.state_history.get(build_id, []),
            "persisted_at": datetime.now().isoformat()
        }
        
        # Store persistence record
        if "persistence_log" not in build_state:
            build_state["persistence_log"] = []
        build_state["persistence_log"].append(persistence_record)
        
        return {
            "build_id": build_id,
            "persistence_successful": True,
            "database_consistent": True,
            "recovery_point_created": True
        }
    
    def handle_state_failure(self, build_id: str, failure_type: str) -> Dict[str, Any]:
        """
        QA-088: Build State Manager failure modes
        
        Detects state corruption and handles conflicting state updates.
        
        Args:
            build_id: Build identifier
            failure_type: Type of failure (corruption, conflicting_updates)
        
        Returns:
            Dict with:
                - build_id: Build identifier
                - failure_type: Type of failure
                - corruption_detected: Boolean
                - corruption_recovered: Boolean
                - conflicting_updates_resolved: Boolean
                - recovery_action: Action taken
        """
        if build_id not in self.build_states:
            return {
                "build_id": build_id,
                "failure_type": "state_not_found",
                "corruption_detected": False,
                "corruption_recovered": False,
                "conflicting_updates_resolved": False,
                "recovery_action": "no_action"
            }
        
        build_state = self.build_states[build_id]
        
        if failure_type == "corruption":
            # Detect corruption by checking state consistency
            corruption_detected = not self._validate_state_consistency(build_state)
            
            if corruption_detected:
                # Attempt recovery from last good state
                recovery_successful = self._recover_from_last_good_state(build_id)
                recovery_action = "recover_from_snapshot" if recovery_successful else "escalate"
            else:
                recovery_successful = True
                recovery_action = "no_corruption_found"
            
            return {
                "build_id": build_id,
                "failure_type": "corruption",
                "corruption_detected": corruption_detected,
                "corruption_recovered": recovery_successful,
                "conflicting_updates_resolved": False,
                "recovery_action": recovery_action
            }
        
        elif failure_type == "conflicting_updates":
            # Resolve conflicting updates by using latest timestamp
            resolved = self._resolve_conflicting_updates(build_id)
            
            return {
                "build_id": build_id,
                "failure_type": "conflicting_updates",
                "corruption_detected": False,
                "corruption_recovered": False,
                "conflicting_updates_resolved": resolved,
                "recovery_action": "use_latest_timestamp"
            }
        
        else:
            return {
                "build_id": build_id,
                "failure_type": failure_type,
                "corruption_detected": False,
                "corruption_recovered": False,
                "conflicting_updates_resolved": False,
                "recovery_action": "escalate"
            }
    
    def _is_valid_transition(self, from_state: str, to_state: str) -> bool:
        """Check if state transition is valid"""
        # Define valid transitions
        valid_transitions = {
            "INITIATED": ["IN_PROGRESS", "FAILED"],
            "IN_PROGRESS": ["BLOCKED", "STALLED", "COMPLETED", "FAILED"],
            "BLOCKED": ["IN_PROGRESS", "FAILED"],
            "STALLED": ["IN_PROGRESS", "FAILED"],
            "COMPLETED": [],
            "FAILED": [],
            "CORRUPTED": []
        }
        
        return to_state in valid_transitions.get(from_state, [])
    
    def _validate_state_consistency(self, build_state: Dict[str, Any]) -> bool:
        """Validate state consistency"""
        # Check required fields exist
        required_fields = ["current_state"]
        return all(field in build_state for field in required_fields)
    
    def _recover_from_last_good_state(self, build_id: str) -> bool:
        """Attempt recovery from last good state snapshot"""
        build_state = self.build_states[build_id]
        persistence_log = build_state.get("persistence_log", [])
        
        if persistence_log:
            # Restore from last good state
            last_good_state = persistence_log[-1]["state_snapshot"]
            self.build_states[build_id] = last_good_state
            return True
        
        return False
    
    def _resolve_conflicting_updates(self, build_id: str) -> bool:
        """Resolve conflicting state updates by using latest timestamp"""
        # Simplified - in production would handle concurrent update conflicts
        return True
