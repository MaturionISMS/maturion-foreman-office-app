"""
Test suite for Wave 1.0.4 API Builder - Execution Orchestration Subsystem

QA Coverage: QA-078 to QA-092 (15 QA components)
Architecture: FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md
Builder: api-builder
"""

import pytest
from datetime import datetime, timedelta
from foreman.api.build_orchestrator import BuildOrchestrator
from foreman.api.build_state_manager import BuildStateManager
from foreman.api.build_progress_tracker import BuildProgressTracker


class TestBuildOrchestrator:
    """Tests for EXEC-01: Build Orchestrator (QA-078 to QA-083)"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.orchestrator = BuildOrchestrator()
    
    def test_qa_078_initiate_build(self):
        """
        QA-078: Initiate build from approved requirement
        Verifies build entity creation, architecture linking, wave planning
        """
        result = self.orchestrator.initiate_build(
            "req_123",
            "FM_ARCHITECTURE_SPEC_V2"
        )
        
        assert result["build_id"] is not None
        assert result["build_entity_created"] is True
        assert result["architecture_linked"] is True
        assert result["wave_planning_complete"] is True
        assert len(result["waves"]) > 0
        
        # Verify build entity
        build = self.orchestrator.builds[result["build_id"]]
        assert build["requirement_id"] == "req_123"
        assert build["architecture_ref"] == "FM_ARCHITECTURE_SPEC_V2"
        assert build["state"] == "INITIATED"
    
    def test_qa_079_assign_builder_to_qa_range(self):
        """
        QA-079: Assign builder to QA range
        Verifies range calculation, builder selection, task creation
        """
        # First initiate a build
        build = self.orchestrator.initiate_build("req_123", "arch_v2")
        build_id = build["build_id"]
        
        # Assign builder to QA range (QA-058 to QA-092 for api-builder)
        result = self.orchestrator.assign_builder(
            build_id,
            58,  # qa_start
            92,  # qa_end
            "api-builder"
        )
        
        assert result["build_id"] == build_id
        assert result["task_id"] is not None
        assert result["qa_range_calculated"] is True
        assert result["qa_start"] == 58
        assert result["qa_end"] == 92
        assert result["builder_selected"] == "api-builder"
        assert result["task_created"] is True
        
        # Verify task
        task = self.orchestrator.builder_assignments[result["task_id"]]
        assert task["qa_count"] == 35  # 92 - 58 + 1
        assert task["state"] == "ASSIGNED"
    
    def test_qa_080_monitor_build_progress(self):
        """
        QA-080: Monitor build progress
        Verifies QA status tracking, progress percentage, stall detection
        """
        build = self.orchestrator.initiate_build("req_123", "arch_v2")
        build_id = build["build_id"]
        
        # Assign task
        self.orchestrator.assign_builder(build_id, 1, 10, "schema-builder")
        
        # Update some progress
        self.orchestrator.builds[build_id]["qa_green"] = 5
        
        # Monitor progress
        result = self.orchestrator.monitor_progress(build_id)
        
        assert result["build_id"] == build_id
        assert result["qa_status_tracked"] is True
        assert result["progress_percentage"] == 50.0  # 5/10 * 100
        assert result["qa_green"] == 5
        assert result["qa_red"] == 0
        assert "stall_detected" in result
    
    def test_qa_081_handle_build_blocking(self):
        """
        QA-081: Handle build blocking
        Verifies blocker creation, escalation, build pause
        """
        build = self.orchestrator.initiate_build("req_123", "arch_v2")
        build_id = build["build_id"]
        
        # Handle blocking
        result = self.orchestrator.handle_blocking(
            build_id,
            "Missing architecture specification for component X",
            {"component": "X", "severity": "high"}
        )
        
        assert result["build_id"] == build_id
        assert result["blocker_id"] is not None
        assert result["blocker_created"] is True
        assert result["escalation_triggered"] is True
        assert result["build_paused"] is True
        
        # Verify build state
        build_entity = self.orchestrator.builds[build_id]
        assert build_entity["state"] == "BLOCKED"
    
    def test_qa_082_complete_build_success(self):
        """
        QA-082: Complete build - success case
        Verifies 100% QA GREEN validation, completion evidence, deliverable
        """
        build = self.orchestrator.initiate_build("req_123", "arch_v2")
        build_id = build["build_id"]
        
        # Assign and complete all QA
        self.orchestrator.assign_builder(build_id, 1, 10, "schema-builder")
        self.orchestrator.builds[build_id]["qa_green"] = 10  # All GREEN
        
        # Complete build
        result = self.orchestrator.complete_build(build_id)
        
        assert result["build_id"] == build_id
        assert result["qa_green_validated"] is True
        assert result["completion_evidence_generated"] is True
        assert result["deliverable_created"] is True
        assert result["completion_status"] == "COMPLETE"
        
        # Verify build state
        build_entity = self.orchestrator.builds[build_id]
        assert build_entity["state"] == "COMPLETED"
    
    def test_qa_082_complete_build_incomplete(self):
        """
        QA-082: Complete build - incomplete case
        Verifies validation fails if not 100% GREEN
        """
        build = self.orchestrator.initiate_build("req_123", "arch_v2")
        build_id = build["build_id"]
        
        # Assign but not all GREEN
        self.orchestrator.assign_builder(build_id, 1, 10, "schema-builder")
        self.orchestrator.builds[build_id]["qa_green"] = 8  # Only 8/10 GREEN
        
        # Try to complete
        result = self.orchestrator.complete_build(build_id)
        
        assert result["qa_green_validated"] is False
        assert result["completion_status"] == "INCOMPLETE"
        assert "reason" in result
    
    def test_qa_083_handle_builder_unavailable(self):
        """
        QA-083: Build Orchestrator failure modes - builder unavailable
        """
        build = self.orchestrator.initiate_build("req_123", "arch_v2")
        build_id = build["build_id"]
        
        result = self.orchestrator.handle_orchestration_failure(
            build_id,
            "builder_unavailable"
        )
        
        assert result["build_id"] == build_id
        assert result["failure_type"] == "builder_unavailable"
        assert result["failure_handled"] is True
        assert result["recovery_action"] == "retry_with_different_builder"
        assert result["corruption_detected"] is False
    
    def test_qa_083_handle_orchestration_corruption(self):
        """
        QA-083: Build Orchestrator failure modes - corruption detection
        """
        build = self.orchestrator.initiate_build("req_123", "arch_v2")
        build_id = build["build_id"]
        
        result = self.orchestrator.handle_orchestration_failure(
            build_id,
            "corruption"
        )
        
        assert result["failure_type"] == "corruption"
        assert result["corruption_detected"] is True
        assert result["recovery_action"] == "escalate_and_halt"
        
        # Verify build marked as corrupted
        build_entity = self.orchestrator.builds[build_id]
        assert build_entity["state"] == "CORRUPTED"


class TestBuildStateManager:
    """Tests for EXEC-02: Build State Manager (QA-084 to QA-088)"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.manager = BuildStateManager()
    
    def test_qa_084_track_state_transition(self):
        """
        QA-084: Track build state transitions
        Verifies state change logged, audit trail, deterministic transitions
        """
        result = self.manager.track_state_transition(
            "build_123",
            "INITIATED",
            "IN_PROGRESS",
            "Builder started work"
        )
        
        assert result["build_id"] == "build_123"
        assert result["state_change_logged"] is True
        assert result["audit_trail_updated"] is True
        assert result["deterministic_transition"] is True
        assert result["from_state"] == "INITIATED"
        assert result["to_state"] == "IN_PROGRESS"
        
        # Verify history
        history = self.manager.state_history["build_123"]
        assert len(history) == 1
        assert history[0]["reason"] == "Builder started work"
    
    def test_qa_084_invalid_state_transition(self):
        """QA-084: Detect invalid state transitions"""
        # Try invalid transition (COMPLETED -> IN_PROGRESS)
        result = self.manager.track_state_transition(
            "build_123",
            "COMPLETED",
            "IN_PROGRESS"
        )
        
        # Should still track but mark as non-deterministic
        assert result["deterministic_transition"] is False
    
    def test_qa_085_update_progress_metrics(self):
        """
        QA-085: Update build progress metrics
        Verifies QA coverage percentage, GREEN/RED counts, time elapsed
        """
        # Initialize build state
        self.manager.build_states["build_123"] = {
            "started_at": datetime.now().isoformat()
        }
        
        result = self.manager.update_progress_metrics(
            "build_123",
            qa_green=15,
            qa_red=5,
            qa_total=35
        )
        
        assert result["build_id"] == "build_123"
        assert result["qa_coverage_percentage"] == pytest.approx(42.86, rel=0.1)  # 15/35
        assert result["qa_green_count"] == 15
        assert result["qa_red_count"] == 5
        assert result["time_elapsed_seconds"] >= 0
    
    def test_qa_086_detect_stall_no_heartbeat(self):
        """
        QA-086: Detect build stall - no heartbeat yet
        """
        self.manager.build_states["build_123"] = {
            "current_state": "IN_PROGRESS"
        }
        
        result = self.manager.detect_stall("build_123")
        
        assert result["build_id"] == "build_123"
        assert result["stall_detected"] is False
        assert result["silence_threshold_exceeded"] is False
        assert result["last_heartbeat"] is None
    
    def test_qa_086_detect_stall_threshold_exceeded(self):
        """
        QA-086: Detect build stall - threshold exceeded
        """
        # Set up old heartbeat
        old_time = (datetime.now() - timedelta(hours=2)).isoformat()
        self.manager.build_states["build_123"] = {
            "current_state": "IN_PROGRESS",
            "last_heartbeat": old_time
        }
        
        result = self.manager.detect_stall("build_123")
        
        assert result["build_id"] == "build_123"
        assert result["stall_detected"] is True
        assert result["silence_threshold_exceeded"] is True
        assert result["stall_escalated"] is True
        
        # Verify state updated
        build_state = self.manager.build_states["build_123"]
        assert build_state["current_state"] == "STALLED"
    
    def test_qa_087_persist_build_state(self):
        """
        QA-087: Persist build state
        Verifies database consistency, recovery point creation
        """
        self.manager.build_states["build_123"] = {
            "current_state": "IN_PROGRESS",
            "qa_green": 10
        }
        
        result = self.manager.persist_state("build_123")
        
        assert result["build_id"] == "build_123"
        assert result["persistence_successful"] is True
        assert result["database_consistent"] is True
        assert result["recovery_point_created"] is True
        
        # Verify persistence log
        build_state = self.manager.build_states["build_123"]
        assert "persistence_log" in build_state
        assert len(build_state["persistence_log"]) > 0
    
    def test_qa_088_handle_state_corruption(self):
        """
        QA-088: Build State Manager failure modes - corruption
        """
        # Set up build state with persistence history
        self.manager.build_states["build_123"] = {
            "current_state": "IN_PROGRESS",
            "persistence_log": [
                {
                    "state_snapshot": {"current_state": "INITIATED"},
                    "persisted_at": datetime.now().isoformat()
                }
            ]
        }
        
        result = self.manager.handle_state_failure(
            "build_123",
            "corruption"
        )
        
        assert result["build_id"] == "build_123"
        assert result["failure_type"] == "corruption"
        assert "corruption_detected" in result
        assert "corruption_recovered" in result
        assert result["recovery_action"] in ["recover_from_snapshot", "no_corruption_found"]
    
    def test_qa_088_handle_conflicting_updates(self):
        """
        QA-088: Build State Manager failure modes - conflicting updates
        """
        self.manager.build_states["build_123"] = {
            "current_state": "IN_PROGRESS"
        }
        
        result = self.manager.handle_state_failure(
            "build_123",
            "conflicting_updates"
        )
        
        assert result["build_id"] == "build_123"
        assert result["failure_type"] == "conflicting_updates"
        assert result["conflicting_updates_resolved"] is True
        assert result["recovery_action"] == "use_latest_timestamp"


class TestBuildProgressTracker:
    """Tests for EXEC-03: Build Progress Tracker (QA-089 to QA-092)"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.tracker = BuildProgressTracker()
        
        # Set up sample progress data
        self.tracker.build_progress_cache["build_123"] = {
            "state": "IN_PROGRESS",
            "progress_percentage": 65.0,
            "qa_total": 35,
            "qa_green": 23,
            "qa_red": 5,
            "requirement_id": "req_123",
            "architecture_ref": "FM_ARCH_V2",
            "requirement_title": "User Dashboard Feature",
            "waves": [
                {
                    "wave_id": "wave-1.0.1",
                    "name": "Foundation",
                    "builder": "schema-builder",
                    "qa_range": "QA-001 to QA-020",
                    "status": "complete",
                    "progress_percentage": 100
                }
            ]
        }
    
    def test_qa_089_get_progress_data(self):
        """
        QA-089: Render build progress UI (API support)
        Verifies current state display, progress bar, QA status summary
        """
        result = self.tracker.get_progress_data("build_123")
        
        assert result["build_id"] == "build_123"
        assert "current_state_display" in result
        assert result["current_state_display"]["state"] == "IN_PROGRESS"
        assert "progress_bar_data" in result
        assert result["progress_bar_data"]["percentage"] == 65.0
        assert "qa_status_summary" in result
        assert result["qa_status_summary"]["total"] == 35
        assert result["qa_status_summary"]["green"] == 23
        assert result["qa_status_summary"]["red"] == 5
    
    def test_qa_090_get_build_details(self):
        """
        QA-090: Render build details (API support)
        Verifies architecture reference, requirement reference, wave breakdown
        """
        result = self.tracker.get_build_details("build_123")
        
        assert result["build_id"] == "build_123"
        assert "architecture_reference" in result
        assert result["architecture_reference"]["spec_id"] == "FM_ARCH_V2"
        assert "requirement_reference" in result
        assert result["requirement_reference"]["requirement_id"] == "req_123"
        assert "wave_breakdown" in result
        assert len(result["wave_breakdown"]) == 1
        assert result["wave_breakdown"][0]["wave_id"] == "wave-1.0.1"
    
    def test_qa_091_push_realtime_update(self):
        """
        QA-091: Real-time build updates (API support)
        Verifies WebSocket push, UI refresh, notification
        """
        # Subscribe a user
        self.tracker.subscribe_to_updates("build_123", "session_456")
        
        # Push update
        update_data = {
            "update_type": "progress",
            "qa_green": 25,
            "progress_percentage": 71.4
        }
        
        result = self.tracker.push_realtime_update("build_123", update_data)
        
        assert result["build_id"] == "build_123"
        assert result["websocket_pushed"] is True
        assert result["ui_refresh_triggered"] is True
        assert result["notification_sent"] is True
        assert result["subscribers_notified"] == 1
        
        # Verify cache updated
        cached = self.tracker.build_progress_cache["build_123"]
        assert cached["qa_green"] == 25
    
    def test_qa_092_handle_update_push_failure(self):
        """
        QA-092: Build Visibility failure modes - update push failure
        """
        result = self.tracker.handle_visibility_failure(
            "build_123",
            "update_push_failure"
        )
        
        assert result["build_id"] == "build_123"
        assert result["failure_type"] == "update_push_failure"
        assert result["update_push_failure_handled"] is True
        assert result["recovery_action"] == "retry_push"
        
        # Verify failed update logged
        cached = self.tracker.build_progress_cache["build_123"]
        assert "failed_updates" in cached
        assert len(cached["failed_updates"]) > 0
    
    def test_qa_092_handle_ui_desync(self):
        """
        QA-092: Build Visibility failure modes - UI desync detection/recovery
        """
        result = self.tracker.handle_visibility_failure(
            "build_123",
            "ui_desync"
        )
        
        assert result["build_id"] == "build_123"
        assert result["failure_type"] == "ui_desync"
        assert result["ui_desync_detected"] is True
        assert result["ui_desync_recovered"] is True
        assert result["recovery_action"] == "force_full_refresh"
        
        # Verify force refresh flag set
        cached = self.tracker.build_progress_cache["build_123"]
        assert cached["force_refresh"] is True


# Integration test to verify end-to-end flow
class TestIntegration:
    """Integration tests for complete API flow"""
    
    def test_complete_build_flow(self):
        """
        Integration test: Complete flow from build initiation to completion
        """
        orchestrator = BuildOrchestrator()
        state_manager = BuildStateManager()
        tracker = BuildProgressTracker()
        
        # 1. Initiate build
        build = orchestrator.initiate_build("req_123", "arch_v2")
        build_id = build["build_id"]
        
        # 2. Track state transition
        state_manager.track_state_transition(
            build_id,
            "INITIATED",
            "IN_PROGRESS"
        )
        
        # 3. Assign builder
        orchestrator.assign_builder(build_id, 1, 35, "api-builder")
        
        # 4. Update progress
        state_manager.update_progress_metrics(
            build_id,
            qa_green=35,
            qa_red=0,
            qa_total=35
        )
        
        # 5. Update tracker cache
        tracker.update_progress_cache(build_id, {
            "state": "IN_PROGRESS",
            "progress_percentage": 100.0,
            "qa_total": 35,
            "qa_green": 35,
            "qa_red": 0
        })
        
        # 6. Complete build
        orchestrator.builds[build_id]["qa_green"] = 35
        completion = orchestrator.complete_build(build_id)
        
        # Verify complete flow
        assert completion["completion_status"] == "COMPLETE"
        assert completion["qa_green_validated"] is True
        
        # Verify state
        assert state_manager.state_history[build_id][0]["to_state"] == "IN_PROGRESS"
        
        # Verify tracker has data
        progress_data = tracker.get_progress_data(build_id)
        assert progress_data["progress_bar_data"]["percentage"] == 100.0
