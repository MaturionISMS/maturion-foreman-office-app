"""
Tests for FM Watchdog Runtime.

Tests the read-only, non-authoritative watchdog runtime implementation.
Validates constraints:
- Read-only operations
- No policy interpretation
- No remediation
- Tenant isolation
- Error escalation (no silent failures)
"""

import pytest
import json
import tempfile
from pathlib import Path
from datetime import datetime

from fm.runtime.watchdog import AlertReader, EscalationReporter


# Test fixtures

@pytest.fixture
def sample_alerts():
    """Sample alert data for testing."""
    return {
        "metadata": {
            "version": "1.0",
            "generated_at": "2025-12-24T00:00:00Z",
            "alert_retention_days": 90
        },
        "alerts": [
            {
                "alert_id": "alert-001",
                "alert_type": "compliance_drift",
                "severity": "critical",
                "status": "new",
                "triggered_at": "2025-12-24T00:00:00Z",
                "watchdog_source": "compliance_watchdog",
                "organisation_id": "org-123",
                "alert_title": "Compliance drift detected",
                "alert_description": "Module X has drifted from compliance baseline",
                "recommended_action": "Review compliance status",
                "escalation": {
                    "escalated": False
                },
                "module": "module-x",
                "component": "api"
            },
            {
                "alert_id": "alert-002",
                "alert_type": "security_anomaly",
                "severity": "high",
                "status": "new",
                "triggered_at": "2025-12-24T01:00:00Z",
                "watchdog_source": "security_monitor",
                "organisation_id": "org-123",
                "alert_title": "Suspicious access pattern",
                "alert_description": "Unusual API access pattern detected",
                "recommended_action": "Investigate access logs",
                "escalation": {
                    "escalated": False
                },
                "module": "module-y",
                "component": "api"
            },
            {
                "alert_id": "alert-003",
                "alert_type": "performance_degradation",
                "severity": "medium",
                "status": "acknowledged",
                "triggered_at": "2025-12-23T00:00:00Z",
                "watchdog_source": "performance_monitor",
                "organisation_id": "org-456",
                "alert_title": "API response time elevated",
                "alert_description": "API response time 20% above baseline",
                "recommended_action": "Monitor performance metrics",
                "escalation": {
                    "escalated": False
                },
                "module": "module-z",
                "component": "api"
            },
            {
                "alert_id": "alert-004",
                "alert_type": "compliance_drift",
                "severity": "low",
                "status": "resolved",
                "triggered_at": "2025-12-22T00:00:00Z",
                "resolved_at": "2025-12-23T00:00:00Z",
                "watchdog_source": "compliance_watchdog",
                "organisation_id": "org-123",
                "alert_title": "Minor configuration drift",
                "alert_description": "Non-critical configuration drift resolved",
                "recommended_action": "No action required",
                "escalation": {
                    "escalated": False
                },
                "resolution_notes": "Configuration updated",
                "module": "module-x",
                "component": "ui"
            }
        ],
        "summary": {
            "total_alerts": 4,
            "active_alerts": 3
        }
    }


@pytest.fixture
def alert_store_file(sample_alerts, tmp_path):
    """Create temporary alert store file."""
    alert_file = tmp_path / "watchdog-alerts.json"
    with open(alert_file, 'w') as f:
        json.dump(sample_alerts, f)
    return alert_file


# AlertReader tests

class TestAlertReader:
    """Tests for AlertReader (read-only alert reader)."""
    
    def test_init_with_custom_path(self, alert_store_file):
        """Test AlertReader initialization with custom path."""
        reader = AlertReader(alert_store_path=str(alert_store_file))
        assert reader.alert_store_path == Path(alert_store_file)
    
    def test_read_all_alerts(self, alert_store_file):
        """Test reading all alerts without filtering."""
        reader = AlertReader(alert_store_path=str(alert_store_file))
        alerts = reader.read_alerts()
        
        assert len(alerts) == 4
        assert all('alert_id' in alert for alert in alerts)
    
    def test_tenant_isolation(self, alert_store_file):
        """Test tenant isolation via organisation_id filtering."""
        reader = AlertReader(alert_store_path=str(alert_store_file))
        
        # Read alerts for org-123
        org_123_alerts = reader.read_alerts(organisation_id="org-123")
        assert len(org_123_alerts) == 3
        assert all(a['organisation_id'] == 'org-123' for a in org_123_alerts)
        
        # Read alerts for org-456
        org_456_alerts = reader.read_alerts(organisation_id="org-456")
        assert len(org_456_alerts) == 1
        assert all(a['organisation_id'] == 'org-456' for a in org_456_alerts)
    
    def test_get_active_alerts(self, alert_store_file):
        """Test filtering active (unresolved) alerts."""
        reader = AlertReader(alert_store_path=str(alert_store_file))
        active = reader.get_active_alerts(organisation_id="org-123")
        
        # Should exclude resolved alert
        assert len(active) == 2
        assert all(a['status'] not in ['resolved', 'false_positive'] for a in active)
    
    def test_get_critical_alerts(self, alert_store_file):
        """Test filtering critical severity alerts."""
        reader = AlertReader(alert_store_path=str(alert_store_file))
        critical = reader.get_critical_alerts(organisation_id="org-123")
        
        assert len(critical) == 1
        assert critical[0]['severity'] == 'critical'
        assert critical[0]['alert_id'] == 'alert-001'
    
    def test_get_alerts_by_type(self, alert_store_file):
        """Test filtering alerts by type."""
        reader = AlertReader(alert_store_path=str(alert_store_file))
        compliance = reader.get_alerts_by_type(
            "compliance_drift",
            organisation_id="org-123"
        )
        
        assert len(compliance) == 2
        assert all(a['alert_type'] == 'compliance_drift' for a in compliance)
    
    def test_get_alert_summary(self, alert_store_file):
        """Test generating alert summary."""
        reader = AlertReader(alert_store_path=str(alert_store_file))
        summary = reader.get_alert_summary(organisation_id="org-123")
        
        assert summary['total_alerts'] == 3
        assert summary['active_alerts'] == 2
        assert summary['organisation_id'] == "org-123"
        assert 'by_severity' in summary
        assert 'by_type' in summary
        assert 'by_status' in summary
        
        # Verify counts
        assert summary['by_severity']['critical'] == 1
        assert summary['by_severity']['high'] == 1
        assert summary['by_severity']['low'] == 1
    
    def test_file_not_found_raises_error(self, tmp_path):
        """Test that missing alert store raises FileNotFoundError."""
        non_existent = tmp_path / "does-not-exist.json"
        reader = AlertReader(alert_store_path=str(non_existent))
        
        with pytest.raises(FileNotFoundError):
            reader.read_alerts()
    
    def test_invalid_json_raises_error(self, tmp_path):
        """Test that invalid JSON raises ValueError."""
        invalid_file = tmp_path / "invalid.json"
        with open(invalid_file, 'w') as f:
            f.write("{ invalid json }")
        
        reader = AlertReader(alert_store_path=str(invalid_file))
        
        with pytest.raises(ValueError):
            reader.read_alerts()
    
    def test_read_only_no_modifications(self, alert_store_file):
        """Test that AlertReader never modifies alert store."""
        reader = AlertReader(alert_store_path=str(alert_store_file))
        
        # Read original content
        with open(alert_store_file, 'r') as f:
            original_content = f.read()
        
        # Perform multiple read operations
        reader.read_alerts()
        reader.get_active_alerts()
        reader.get_critical_alerts()
        reader.get_alert_summary()
        
        # Verify content unchanged
        with open(alert_store_file, 'r') as f:
            current_content = f.read()
        
        assert current_content == original_content


# EscalationReporter tests

class TestEscalationReporter:
    """Tests for EscalationReporter (escalation reporter)."""
    
    def test_init(self):
        """Test EscalationReporter initialization."""
        reporter = EscalationReporter()
        assert reporter is not None
    
    def test_should_escalate_critical(self):
        """Test that critical alerts should escalate."""
        reporter = EscalationReporter()
        alert = {
            'severity': 'critical',
            'status': 'new',
            'escalation': {'escalated': False}
        }
        
        assert reporter.should_escalate(alert) is True
    
    def test_should_escalate_high_new(self):
        """Test that new high-severity alerts should escalate."""
        reporter = EscalationReporter()
        alert = {
            'severity': 'high',
            'status': 'new',
            'escalation': {'escalated': False}
        }
        
        assert reporter.should_escalate(alert) is True
    
    def test_should_not_escalate_medium(self):
        """Test that medium alerts don't auto-escalate."""
        reporter = EscalationReporter()
        alert = {
            'severity': 'medium',
            'status': 'new',
            'escalation': {'escalated': False}
        }
        
        assert reporter.should_escalate(alert) is False
    
    def test_should_escalate_already_escalated(self):
        """Test that already escalated alerts are identified."""
        reporter = EscalationReporter()
        alert = {
            'severity': 'low',
            'status': 'acknowledged',
            'escalation': {'escalated': True}
        }
        
        assert reporter.should_escalate(alert) is True
    
    def test_generate_escalation_report(self, sample_alerts):
        """Test generating escalation report."""
        reporter = EscalationReporter()
        alerts = sample_alerts['alerts']
        
        report = reporter.generate_escalation_report(
            alerts,
            organisation_id="org-123"
        )
        
        assert report['report_type'] == 'watchdog_escalation'
        assert report['organisation_id'] == 'org-123'
        assert report['total_alerts_reviewed'] == 4
        assert report['escalation_count'] >= 1
        assert 'escalations' in report
        
        # Verify escalations have required fields
        for escalation in report['escalations']:
            assert 'alert_id' in escalation
            assert 'alert_type' in escalation
            assert 'severity' in escalation
            assert 'escalation_reason' in escalation
    
    def test_get_escalation_reason_critical(self):
        """Test escalation reason for critical alerts."""
        reporter = EscalationReporter()
        alert = {
            'severity': 'critical',
            'status': 'new',
            'escalation': {'escalated': False}
        }
        
        reason = reporter._get_escalation_reason(alert)
        assert 'Critical severity' in reason
    
    def test_get_escalation_reason_high_new(self):
        """Test escalation reason for new high-severity alerts."""
        reporter = EscalationReporter()
        alert = {
            'severity': 'high',
            'status': 'new',
            'escalation': {'escalated': False}
        }
        
        reason = reporter._get_escalation_reason(alert)
        assert 'high-severity' in reason
    
    def test_get_escalation_summary(self, sample_alerts):
        """Test generating escalation summary."""
        reporter = EscalationReporter()
        alerts = sample_alerts['alerts']
        
        summary = reporter.get_escalation_summary(alerts)
        
        assert summary['total_alerts'] == 4
        assert summary['requires_escalation'] >= 1
        assert 'by_severity' in summary
        assert 'by_type' in summary
    
    def test_log_escalation(self, sample_alerts, caplog):
        """Test logging escalation events."""
        reporter = EscalationReporter()
        alerts = sample_alerts['alerts']
        
        report = reporter.generate_escalation_report(alerts)
        reporter.log_escalation(report, destination="human_oversight")
        
        # Verify escalation was logged
        assert "ESCALATION" in caplog.text
    
    def test_no_modifications_to_alerts(self, sample_alerts):
        """Test that EscalationReporter never modifies alerts."""
        reporter = EscalationReporter()
        alerts = sample_alerts['alerts'].copy()
        
        # Store original alert data
        original_alerts = json.dumps(alerts, sort_keys=True)
        
        # Perform escalation operations
        reporter.generate_escalation_report(alerts)
        reporter.get_escalation_summary(alerts)
        
        # Verify alerts unchanged
        current_alerts = json.dumps(alerts, sort_keys=True)
        assert current_alerts == original_alerts


# Integration tests

class TestWatchdogRuntimeIntegration:
    """Integration tests for watchdog runtime."""
    
    def test_full_workflow(self, alert_store_file):
        """Test full watchdog runtime workflow."""
        # Step 1: Read alerts
        reader = AlertReader(alert_store_path=str(alert_store_file))
        alerts = reader.read_alerts(organisation_id="org-123")
        
        assert len(alerts) > 0
        
        # Step 2: Get summary
        summary = reader.get_alert_summary(organisation_id="org-123")
        
        assert summary['total_alerts'] == len(alerts)
        
        # Step 3: Generate escalation report
        reporter = EscalationReporter()
        report = reporter.generate_escalation_report(
            alerts,
            organisation_id="org-123"
        )
        
        assert report['organisation_id'] == 'org-123'
        assert report['escalation_count'] >= 0
        
        # Step 4: Log escalations
        reporter.log_escalation(report)
    
    def test_multi_tenant_isolation(self, alert_store_file):
        """Test that tenant isolation works across workflow."""
        reader = AlertReader(alert_store_path=str(alert_store_file))
        reporter = EscalationReporter()
        
        # Workflow for org-123
        alerts_123 = reader.read_alerts(organisation_id="org-123")
        report_123 = reporter.generate_escalation_report(
            alerts_123,
            organisation_id="org-123"
        )
        
        # Workflow for org-456
        alerts_456 = reader.read_alerts(organisation_id="org-456")
        report_456 = reporter.generate_escalation_report(
            alerts_456,
            organisation_id="org-456"
        )
        
        # Verify isolation
        assert report_123['organisation_id'] == 'org-123'
        assert report_456['organisation_id'] == 'org-456'
        assert report_123['total_alerts_reviewed'] != report_456['total_alerts_reviewed']
    
    def test_error_escalation_no_silent_failures(self, tmp_path):
        """Test that all errors are raised (no silent failures)."""
        non_existent = tmp_path / "missing.json"
        reader = AlertReader(alert_store_path=str(non_existent))
        
        # Missing file should raise, not fail silently
        with pytest.raises(FileNotFoundError):
            reader.read_alerts()
