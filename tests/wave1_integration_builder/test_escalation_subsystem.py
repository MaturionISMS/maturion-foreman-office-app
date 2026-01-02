"""
Wave 1 Integration Builder Tests - Escalation Subsystem
QA-093 to QA-116: Escalation & Supervision Components

Tests for:
- ESC-01: Ping Generator (QA-093 to QA-096)
- ESC-02: Escalation Manager (QA-097 to QA-104)
- ESC-03: Silence Detector (QA-105 to QA-109)
- ESC-04: Message Inbox Controller (QA-110 to QA-116) - UI tests (already exist)
"""

import pytest
from datetime import datetime, timedelta
from foreman.escalation import PingGenerator, EscalationManager, SilenceDetector


class TestPingGenerator:
    """Tests for ESC-01: Ping Generator (QA-093 to QA-096)"""
    
    @pytest.fixture
    def ping_generator(self):
        return PingGenerator()
    
    def test_qa_093_generate_ping_for_attention_required(self, ping_generator):
        """
        QA-093: Generate ping for attention required.
        
        Verify ping creation, context attachment, priority assignment.
        """
        # Generate ping with context
        context = {
            'component': 'BuildOrchestrator',
            'issue': 'Stalled build',
            'build_id': 'build-123'
        }
        
        ping = ping_generator.generate_ping(context, priority="high")
        
        # Verify ping creation
        assert ping is not None
        assert ping.ping_id is not None
        assert ping.context == context
        assert ping.priority == "high"
        assert ping.status == "sent"
        assert isinstance(ping.created_at, datetime)
        
        # Verify context attachment
        assert 'component' in ping.context
        assert 'issue' in ping.context
        assert 'build_id' in ping.context
        
        # Verify priority assignment
        assert ping.priority in ["normal", "high", "urgent", "critical"]
    
    def test_qa_094_route_ping_to_notification_service(self, ping_generator):
        """
        QA-094: Route ping to notification service.
        
        Verify delivery trigger and acknowledgment tracking.
        """
        # Create ping
        ping = ping_generator.generate_ping({'test': 'context'}, priority="normal")
        
        # Route ping
        result = ping_generator.route_ping(ping.ping_id)
        
        # Verify delivery trigger
        assert result['delivery_trigger'] is True
        assert result['status'] == 'delivered'
        
        # Verify acknowledgment tracking
        assert result['acknowledgment_tracking'] is True
        assert 'delivered_at' in result
    
    def test_qa_095_track_ping_lifecycle(self, ping_generator):
        """
        QA-095: Track ping lifecycle.
        
        Verify sent/delivered/acknowledged states and timeout detection.
        """
        # Create and route ping
        ping = ping_generator.generate_ping({'test': 'lifecycle'}, priority="normal")
        ping_generator.route_ping(ping.ping_id)
        
        # Track lifecycle
        lifecycle = ping_generator.track_lifecycle(ping.ping_id)
        
        # Verify states
        assert lifecycle['status'] in ['sent', 'delivered', 'acknowledged', 'timeout']
        assert lifecycle['ping_id'] == ping.ping_id
        assert 'created_at' in lifecycle
        assert 'delivered_at' in lifecycle
        
        # Acknowledge ping
        ping_generator.acknowledge_ping(ping.ping_id)
        lifecycle_after = ping_generator.track_lifecycle(ping.ping_id)
        assert lifecycle_after['status'] == 'acknowledged'
        assert lifecycle_after['acknowledged_at'] is not None
        
        # Verify timeout detection (would require time manipulation in real test)
        assert 'is_timeout' in lifecycle
    
    def test_qa_096_ping_generator_failure_modes(self, ping_generator):
        """
        QA-096: Ping Generator failure modes.
        
        Test delivery failure retry/escalation and duplicate ping prevention.
        """
        # Test duplicate prevention
        context = {'unique': 'test'}
        ping1 = ping_generator.generate_ping(context, priority="normal")
        
        with pytest.raises(ValueError, match="Duplicate ping detected"):
            ping2 = ping_generator.generate_ping(context, priority="normal")
        
        # Test delivery failure handling
        ping3 = ping_generator.generate_ping({'different': 'context'}, priority="normal")
        
        # Simulate retries
        failure_result = ping_generator.handle_failure_modes(
            'delivery_failure',
            ping_id=ping3.ping_id
        )
        
        assert 'status' in failure_result
        assert failure_result['status'] in ['retry', 'escalated', 'error']


class TestEscalationManager:
    """Tests for ESC-02: Escalation Manager (QA-097 to QA-104)"""
    
    @pytest.fixture
    def escalation_manager(self):
        return EscalationManager()
    
    def test_qa_097_create_escalation_with_5_elements(self, escalation_manager):
        """
        QA-097: Create escalation with 5 elements.
        
        Verify all 5 elements present: what/why/blocked/decision/consequence.
        """
        # Create escalation with all 5 elements
        escalation = escalation_manager.create_escalation(
            what="Build failed after 3 attempts",
            why="Architecture specification incomplete",
            blocked="Module implementation",
            decision="Should we complete architecture or proceed with partial spec?",
            consequence="Module will be hollow and fail QA",
            priority="HIGH"
        )
        
        # Verify all 5 elements present
        assert escalation.what == "Build failed after 3 attempts"
        assert escalation.why == "Architecture specification incomplete"
        assert escalation.blocked == "Module implementation"
        assert escalation.decision == "Should we complete architecture or proceed with partial spec?"
        assert escalation.consequence == "Module will be hollow and fail QA"
        
        # Verify missing elements are rejected
        with pytest.raises(ValueError, match="Missing required escalation elements"):
            escalation_manager.create_escalation(
                what="Something",
                why="",  # Missing
                blocked="Something",
                decision="Something",
                consequence="Something"
            )
    
    def test_qa_098_route_escalation_to_johan(self, escalation_manager):
        """
        QA-098: Route escalation to Johan.
        
        Verify inbox placement, notification, UI rendering.
        """
        # Create escalation
        escalation = escalation_manager.create_escalation(
            what="Test",
            why="Test",
            blocked="Test",
            decision="Test",
            consequence="Test",
            priority="NORMAL"
        )
        
        # Route to Johan
        result = escalation_manager.route_to_johan(escalation.escalation_id)
        
        # Verify inbox placement
        assert result['inbox_placed'] is True
        
        # Verify notification sent
        assert result['notification_sent'] is True
        
        # Verify UI rendering triggered
        assert result['ui_rendering_triggered'] is True
        assert 'presented_at' in result
    
    def test_qa_099_present_escalation_in_ui(self, escalation_manager):
        """
        QA-099: Present escalation in UI.
        
        Verify 5-element display, action buttons, context linking.
        """
        # Create escalation with context
        escalation = escalation_manager.create_escalation(
            what="Test",
            why="Test",
            blocked="Test",
            decision="Test",
            consequence="Test",
            priority="HIGH",
            context_links={'build_id': 'build-456'}
        )
        
        # Get UI presentation
        ui_data = escalation_manager.present_in_ui(escalation.escalation_id)
        
        # Verify 5-element display
        assert 'five_elements' in ui_data
        assert ui_data['five_elements']['what'] == "Test"
        assert ui_data['five_elements']['why'] == "Test"
        assert ui_data['five_elements']['blocked'] == "Test"
        assert ui_data['five_elements']['decision'] == "Test"
        assert ui_data['five_elements']['consequence'] == "Test"
        
        # Verify action buttons
        assert 'action_buttons' in ui_data
        assert 'approve' in ui_data['action_buttons']
        assert 'reject' in ui_data['action_buttons']
        
        # Verify context linking
        assert 'context_links' in ui_data
        assert ui_data['context_links']['build_id'] == 'build-456'
    
    def test_qa_100_handle_escalation_decision(self, escalation_manager):
        """
        QA-100: Handle escalation decision.
        
        Verify decision capture, execution trigger, resolution logging.
        """
        # Create and route escalation
        escalation = escalation_manager.create_escalation(
            what="Test",
            why="Test",
            blocked="Test",
            decision="Test",
            consequence="Test"
        )
        escalation_manager.route_to_johan(escalation.escalation_id)
        
        # Handle decision
        result = escalation_manager.handle_decision(
            escalation.escalation_id,
            decision="approve",
            decision_data={'approved_by': 'Johan'}
        )
        
        # Verify decision captured
        assert result['decision_captured'] is True
        
        # Verify execution triggered
        assert result['execution_triggered'] is True
        assert 'execution_result' in result
        
        # Verify resolution logged
        assert result['resolution_logged'] is True
        assert 'resolved_at' in result
    
    def test_qa_101_track_escalation_lifecycle(self, escalation_manager):
        """
        QA-101: Track escalation lifecycle.
        
        Verify Pending/Presented/Resolved states and audit trail.
        """
        # Create escalation
        escalation = escalation_manager.create_escalation(
            what="Test",
            why="Test",
            blocked="Test",
            decision="Test",
            consequence="Test"
        )
        
        # Track initial state
        lifecycle = escalation_manager.track_lifecycle(escalation.escalation_id)
        assert lifecycle['status'] == 'Pending'
        assert lifecycle['current_state']['Pending'] is True
        
        # Route escalation
        escalation_manager.route_to_johan(escalation.escalation_id)
        lifecycle = escalation_manager.track_lifecycle(escalation.escalation_id)
        assert lifecycle['status'] == 'Presented'
        assert lifecycle['current_state']['Presented'] is True
        
        # Resolve escalation
        escalation_manager.handle_decision(escalation.escalation_id, "approve")
        lifecycle = escalation_manager.track_lifecycle(escalation.escalation_id)
        assert lifecycle['status'] == 'Resolved'
        assert lifecycle['current_state']['Resolved'] is True
        
        # Verify audit trail
        assert 'audit_trail' in lifecycle
        assert len(lifecycle['audit_trail']) > 0
    
    def test_qa_102_escalation_priority_handling(self, escalation_manager):
        """
        QA-102: Escalation priority handling.
        
        Verify CRITICAL, HIGH, NORMAL routing.
        """
        # Test each priority level
        for priority in ['CRITICAL', 'HIGH', 'NORMAL']:
            escalation = escalation_manager.create_escalation(
                what="Test",
                why="Test",
                blocked="Test",
                decision="Test",
                consequence="Test",
                priority=priority
            )
            
            # Get routing info
            routing = escalation_manager.handle_priority_routing(escalation.escalation_id)
            
            assert routing['priority'] == priority
            assert 'routing' in routing
            
            if priority == 'CRITICAL':
                assert 'email' in routing['routing']['notification_channels']
                assert 'sms' in routing['routing']['notification_channels']
            elif priority == 'HIGH':
                assert 'email' in routing['routing']['notification_channels']
            else:  # NORMAL
                assert routing['routing']['notification_channels'] == ['inbox']
    
    def test_qa_103_escalation_context_linking(self, escalation_manager):
        """
        QA-103: Escalation context linking.
        
        Verify build linking, conversation linking, evidence linking.
        """
        # Create escalation
        escalation = escalation_manager.create_escalation(
            what="Test",
            why="Test",
            blocked="Test",
            decision="Test",
            consequence="Test"
        )
        
        # Link context
        result = escalation_manager.link_context(
            escalation.escalation_id,
            build_id="build-789",
            conversation_id="conv-123",
            evidence_ids=["evidence-1", "evidence-2"]
        )
        
        # Verify all linking types
        assert result['build_linked'] is True
        assert result['conversation_linked'] is True
        assert result['evidence_linked'] is True
        
        assert result['context_links']['build_id'] == "build-789"
        assert result['context_links']['conversation_id'] == "conv-123"
        assert "evidence-1" in result['context_links']['evidence_ids']
    
    def test_qa_104_escalation_manager_failure_modes(self, escalation_manager):
        """
        QA-104: Escalation Manager failure modes.
        
        Test missing elements detection, routing failure, decision execution failure.
        """
        # Test missing elements detection (already tested in QA-097)
        with pytest.raises(ValueError):
            escalation_manager.create_escalation(
                what="",  # Missing
                why="Test",
                blocked="Test",
                decision="Test",
                consequence="Test"
            )
        
        # Test routing failure with invalid ID
        with pytest.raises(KeyError):
            escalation_manager.route_to_johan("invalid-id")
        
        # Test decision execution failure with invalid ID
        with pytest.raises(KeyError):
            escalation_manager.handle_decision("invalid-id", "approve")


class TestSilenceDetector:
    """Tests for ESC-03: Silence Detector (QA-105 to QA-109)"""
    
    @pytest.fixture
    def silence_detector(self):
        return SilenceDetector(silence_threshold_hours=0.001)  # 3.6 seconds for testing
    
    def test_qa_105_monitor_build_heartbeat(self, silence_detector):
        """
        QA-105: Monitor build heartbeat.
        
        Verify last update tracking, threshold comparison, silence detection.
        """
        # Start monitoring
        result = silence_detector.monitor_heartbeat("build-001")
        
        # Verify monitoring started
        assert result['status'] == 'monitoring_started'
        assert result['build_id'] == "build-001"
        assert 'last_update' in result
        assert 'threshold' in result
        assert result['silence_detected'] is False
        
        # Update heartbeat
        result2 = silence_detector.monitor_heartbeat("build-001", datetime.now())
        assert result2['silence_detected'] is False
    
    def test_qa_106_detect_silence(self, silence_detector):
        """
        QA-106: Detect silence.
        
        Verify 2-hour threshold, escalation trigger, silence context creation.
        """
        # Monitor build with old heartbeat
        old_time = datetime.now() - timedelta(hours=3)
        silence_detector.monitor_heartbeat("build-002", old_time)
        
        # Detect silence
        result = silence_detector.detect_silence("build-002")
        
        # Verify silence detected
        assert result['silence_detected'] is True
        assert result['elapsed_hours'] > silence_detector.silence_threshold.total_seconds() / 3600
        
        # Verify escalation triggered (for actual stalls)
        assert 'escalation_triggered' in result
        
        # Verify silence context
        if result['escalation_triggered']:
            assert 'escalation_context' in result
            assert result['escalation_context']['issue'] == 'BuildSilence'
    
    def test_qa_107_differentiate_silence_types(self, silence_detector):
        """
        QA-107: Differentiate silence types.
        
        Verify intentional pause vs actual stall, verify different handling.
        """
        # Test actual stall
        old_time = datetime.now() - timedelta(hours=3)
        silence_detector.monitor_heartbeat("build-003", old_time)
        
        result1 = silence_detector.differentiate_silence_type("build-003")
        assert result1['is_actual_stall'] is True
        assert result1['handling'] == 'escalate'
        
        # Test intentional pause
        silence_detector.pause_build("build-004", "Manual pause for review")
        silence_detector.monitor_heartbeat("build-004", old_time)
        
        result2 = silence_detector.differentiate_silence_type("build-004")
        assert result2['is_intentional_pause'] is True
        assert result2['handling'] == 'no_escalation'
        assert result2['pause_reason'] == "Manual pause for review"
    
    def test_qa_108_silence_recovery(self, silence_detector):
        """
        QA-108: Silence recovery.
        
        Verify heartbeat restoration and escalation closure.
        """
        # Create silent build
        old_time = datetime.now() - timedelta(hours=3)
        silence_detector.monitor_heartbeat("build-005", old_time)
        silence_detector.detect_silence("build-005")
        
        # Recover from silence
        result = silence_detector.handle_silence_recovery("build-005")
        
        # Verify heartbeat restored
        assert result['heartbeat_restored'] is True
        assert result['was_silent'] is True
        
        # Verify escalation closed
        assert 'escalation_closed' in result
        assert 'restored_at' in result
    
    def test_qa_109_silence_detector_failure_modes(self, silence_detector):
        """
        QA-109: Silence Detector failure modes.
        
        Test false positive prevention and heartbeat update failure.
        """
        # Test false positive prevention
        silence_detector.pause_build("build-006", "Intentional pause")
        
        result = silence_detector.handle_failure_modes(
            'false_positive',
            build_id="build-006"
        )
        
        assert result['status'] == 'false_positive_prevented'
        assert result['escalation_suppressed'] is True
        
        # Test heartbeat update failure
        result2 = silence_detector.handle_failure_modes(
            'heartbeat_update_failure',
            build_id="build-007",
            error="Network timeout"
        )
        
        assert result2['status'] == 'logged'
        assert result2['monitoring_continued'] is True


# Note: QA-110 to QA-116 (ESC-04: Message Inbox Controller) are UI tests
# and already exist in tests/wave1_ui/test_build_visibility_and_escalation_ui.py
