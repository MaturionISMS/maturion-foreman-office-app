"""
Wave 2.0 QA Infrastructure — Subwave 2.7: Governance Advanced (Security)
QA Range: QA-386 to QA-390 (5 QA components)

Authority: WAVE_2_ROLLOUT_PLAN.md Section II, Subwave 2.7
Purpose: QA-to-Red tests for Security Failure Modes

Test Categories:
- Security Failure Modes (QA-386 to QA-390)

State: RED → GREEN (Build-to-Green in progress)
Build-to-Green Status: IN PROGRESS
"""

import pytest
from typing import Dict, Any, List
from datetime import datetime, UTC

# Import security failure handler module
from fm.runtime.security_failure_handler import (
    SecurityFailureHandler,
    SecurityEvent,
    SecurityEventType,
    SecurityAction,
    AuditLogger,
    IntegrityChecker
)


@pytest.mark.wave2
@pytest.mark.subwave_2_7
class TestSecurityFailureModes:
    """QA-386 to QA-390: Security Failure Modes"""

    @pytest.fixture
    def security_handler(self, test_organisation_id):
        """Initialize security failure handler with test context."""
        return SecurityFailureHandler(organisation_id=test_organisation_id)

    @pytest.fixture
    def audit_logger(self, test_organisation_id):
        """Initialize audit logger for security events."""
        return AuditLogger(organisation_id=test_organisation_id)

    @pytest.fixture
    def integrity_checker(self, test_organisation_id):
        """Initialize integrity checker for data validation."""
        return IntegrityChecker(organisation_id=test_organisation_id)

    def test_qa_386_unauthorized_access_attempt(
        self, security_handler, test_organisation_id
    ):
        """
        QA-386: Unauthorized access attempt
        
        Verify:
        - Detection of unauthorized access
        - Access blocking
        - Audit log entry
        - Escalation triggered
        
        Tenant isolation: organisation_id required
        """
        # Arrange: Create unauthorized access event
        access_event = SecurityEvent(
            event_type=SecurityEventType.UNAUTHORIZED_ACCESS,
            user_id="unauthorized-user-001",
            resource="protected-resource",
            organisation_id=test_organisation_id,
            timestamp=datetime.now(UTC)
        )

        # Act: Process unauthorized access attempt
        result = security_handler.handle_event(access_event)

        # Assert: Detection
        assert result.detected is True, "Unauthorized access must be detected"
        
        # Assert: Blocking
        assert result.blocked is True, "Unauthorized access must be blocked"
        assert result.action == SecurityAction.BLOCK, "Action must be BLOCK"
        
        # Assert: Audit log (use handler's internal audit logger)
        audit_entries = security_handler._audit_logger.get_entries(
            event_type=SecurityEventType.UNAUTHORIZED_ACCESS,
            organisation_id=test_organisation_id
        )
        assert len(audit_entries) > 0, "Audit log must contain entry"
        assert audit_entries[0].event_type == SecurityEventType.UNAUTHORIZED_ACCESS
        
        # Assert: Escalation
        assert result.escalated is True, "Unauthorized access must trigger escalation"
        assert result.escalation_reason is not None, "Escalation must have reason"

    def test_qa_387_authority_escalation_abuse(
        self, security_handler, test_organisation_id
    ):
        """
        QA-387: Authority escalation abuse
        
        Verify:
        - Detection of authority escalation abuse
        - Escalation blocking
        - Audit log entry
        - Escalation triggered
        
        Tenant isolation: organisation_id required
        """
        # Arrange: Create authority escalation event
        escalation_event = SecurityEvent(
            event_type=SecurityEventType.AUTHORITY_ESCALATION_ABUSE,
            user_id="user-002",
            attempted_role="admin",
            current_role="builder",
            organisation_id=test_organisation_id,
            timestamp=datetime.now(UTC)
        )

        # Act: Process escalation abuse attempt
        result = security_handler.handle_event(escalation_event)

        # Assert: Detection
        assert result.detected is True, "Authority escalation must be detected"
        
        # Assert: Blocking
        assert result.blocked is True, "Authority escalation must be blocked"
        assert result.action == SecurityAction.BLOCK, "Action must be BLOCK"
        
        # Assert: Audit log (use handler's internal audit logger)
        audit_entries = security_handler._audit_logger.get_entries(
            event_type=SecurityEventType.AUTHORITY_ESCALATION_ABUSE,
            organisation_id=test_organisation_id
        )
        assert len(audit_entries) > 0, "Audit log must contain entry"
        
        # Assert: Escalation
        assert result.escalated is True, "Authority escalation abuse must trigger escalation"

    def test_qa_388_data_tampering_attempt(
        self, security_handler, integrity_checker, test_organisation_id
    ):
        """
        QA-388: Data tampering attempt
        
        Verify:
        - Integrity checks detect tampering
        - Tampering detection
        - Escalation triggered
        
        Tenant isolation: organisation_id required
        """
        # Arrange: Create data with valid integrity
        original_data = {
            "id": "data-001",
            "content": "original content",
            "organisation_id": test_organisation_id
        }
        integrity_hash = integrity_checker.compute_hash(original_data)
        
        # Arrange: Tamper with data
        tampered_data = {
            "id": "data-001",
            "content": "tampered content",
            "organisation_id": test_organisation_id
        }

        # Act: Validate tampered data
        tampering_event = SecurityEvent(
            event_type=SecurityEventType.DATA_TAMPERING,
            data=tampered_data,
            expected_hash=integrity_hash,
            organisation_id=test_organisation_id,
            timestamp=datetime.now(UTC)
        )
        result = security_handler.handle_event(tampering_event)

        # Assert: Integrity check detects tampering
        is_valid = integrity_checker.validate(tampered_data, integrity_hash)
        assert is_valid is False, "Integrity check must detect tampering"
        
        # Assert: Detection
        assert result.detected is True, "Data tampering must be detected"
        
        # Assert: Escalation
        assert result.escalated is True, "Data tampering must trigger escalation"
        
        # Assert: Audit log (use handler's internal audit logger)
        audit_entries = security_handler._audit_logger.get_entries(
            event_type=SecurityEventType.DATA_TAMPERING,
            organisation_id=test_organisation_id
        )
        assert len(audit_entries) > 0, "Audit log must contain tampering entry"

    def test_qa_389_governance_bypass_attempt(
        self, security_handler, test_organisation_id
    ):
        """
        QA-389: Governance bypass attempt
        
        Verify:
        - Detection of governance bypass
        - Bypass blocking
        - Audit log entry
        - Escalation triggered
        
        Tenant isolation: organisation_id required
        """
        # Arrange: Create governance bypass event
        bypass_event = SecurityEvent(
            event_type=SecurityEventType.GOVERNANCE_BYPASS,
            user_id="user-003",
            bypassed_rule="BUILD_PHILOSOPHY.md Section III",
            action_attempted="skip_test",
            organisation_id=test_organisation_id,
            timestamp=datetime.now(UTC)
        )

        # Act: Process bypass attempt
        result = security_handler.handle_event(bypass_event)

        # Assert: Detection
        assert result.detected is True, "Governance bypass must be detected"
        
        # Assert: Blocking
        assert result.blocked is True, "Governance bypass must be blocked"
        assert result.action == SecurityAction.BLOCK, "Action must be BLOCK"
        
        # Assert: Audit log (use handler's internal audit logger)
        audit_entries = security_handler._audit_logger.get_entries(
            event_type=SecurityEventType.GOVERNANCE_BYPASS,
            organisation_id=test_organisation_id
        )
        assert len(audit_entries) > 0, "Audit log must contain bypass attempt"
        
        # Assert: Escalation
        assert result.escalated is True, "Governance bypass must trigger escalation"
        assert "BUILD_PHILOSOPHY" in result.escalation_reason

    def test_qa_390_memory_fabric_unauthorized_write(
        self, security_handler, test_organisation_id
    ):
        """
        QA-390: Memory fabric unauthorized write
        
        Verify:
        - Prevention of unauthorized writes
        - Detection of unauthorized write attempts
        - Escalation triggered
        
        Tenant isolation: organisation_id required
        """
        # Arrange: Create memory write event without authorization
        memory_write_event = SecurityEvent(
            event_type=SecurityEventType.MEMORY_FABRIC_UNAUTHORIZED_WRITE,
            user_id="unauthorized-writer-001",
            memory_scope="restricted-scope",
            write_attempted=True,
            organisation_id=test_organisation_id,
            timestamp=datetime.now(UTC)
        )

        # Act: Process unauthorized write attempt
        result = security_handler.handle_event(memory_write_event)

        # Assert: Prevention
        assert result.prevented is True, "Unauthorized write must be prevented"
        assert result.action == SecurityAction.PREVENT, "Action must be PREVENT"
        
        # Assert: Detection
        assert result.detected is True, "Unauthorized write must be detected"
        
        # Assert: Escalation
        assert result.escalated is True, "Unauthorized write must trigger escalation"
        
        # Assert: Audit log (use handler's internal audit logger)
        audit_entries = security_handler._audit_logger.get_entries(
            event_type=SecurityEventType.MEMORY_FABRIC_UNAUTHORIZED_WRITE,
            organisation_id=test_organisation_id
        )
        assert len(audit_entries) > 0, "Audit log must contain write attempt"
        assert audit_entries[0].write_prevented is True
