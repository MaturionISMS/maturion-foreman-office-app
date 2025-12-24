"""
Escalation Reporter - Report alerts requiring human intervention.

This module reports alerts that require escalation to human oversight.
It is strictly report-only and does NOT:
- Modify alerts
- Interpret policy
- Perform remediation
- Make autonomous decisions

All it does:
- Identify alerts requiring escalation
- Format escalation reports
- Log escalation events (read-only)
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime


logger = logging.getLogger(__name__)


class EscalationReporter:
    """
    Escalation reporter for watchdog runtime.
    
    Responsibilities:
    - Identify alerts requiring escalation
    - Format escalation reports
    - Log escalation events
    - Report to human oversight
    
    Does NOT:
    - Modify alerts
    - Interpret policy
    - Perform remediation
    - Make decisions
    """
    
    def __init__(self):
        """Initialize EscalationReporter."""
        logger.info("EscalationReporter initialized")
    
    def should_escalate(self, alert: Dict[str, Any]) -> bool:
        """
        Determine if an alert should be escalated.
        
        This is NOT policy interpretation - it simply checks existing
        escalation flags set by upstream systems.
        
        Escalation criteria (read from alert, not decided here):
        - Alert has escalation.escalated = true
        - Alert severity is 'critical'
        - Alert status is 'new' and severity is 'high'
        
        Args:
            alert: Alert dictionary
            
        Returns:
            True if alert should be escalated
        """
        # Check if already escalated (read flag, don't decide)
        if alert.get('escalation', {}).get('escalated', False):
            return True
        
        # Check severity (read severity, don't interpret)
        severity = alert.get('severity', '')
        status = alert.get('status', '')
        
        # Critical alerts always escalate
        if severity == 'critical':
            return True
        
        # New high-severity alerts escalate
        if severity == 'high' and status == 'new':
            return True
        
        return False
    
    def generate_escalation_report(
        self,
        alerts: List[Dict[str, Any]],
        organisation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate escalation report for alerts.
        
        This is a READ-ONLY operation. It reports status, does not change it.
        
        Args:
            alerts: List of alerts to report on
            organisation_id: Optional organisation ID for context
            
        Returns:
            Escalation report dictionary
        """
        escalation_alerts = [
            alert for alert in alerts
            if self.should_escalate(alert)
        ]
        
        report = {
            'report_type': 'watchdog_escalation',
            'generated_at': datetime.utcnow().isoformat(),
            'organisation_id': organisation_id,
            'total_alerts_reviewed': len(alerts),
            'escalation_count': len(escalation_alerts),
            'escalations': []
        }
        
        for alert in escalation_alerts:
            escalation = {
                'alert_id': alert.get('alert_id'),
                'alert_type': alert.get('alert_type'),
                'severity': alert.get('severity'),
                'status': alert.get('status'),
                'triggered_at': alert.get('triggered_at'),
                'alert_title': alert.get('alert_title'),
                'alert_description': alert.get('alert_description'),
                'recommended_action': alert.get('recommended_action'),
                'escalation_reason': self._get_escalation_reason(alert),
                'impact': alert.get('impact', {}),
                'module': alert.get('module'),
                'component': alert.get('component')
            }
            report['escalations'].append(escalation)
        
        logger.info(
            f"Generated escalation report: {len(escalation_alerts)} alerts "
            f"escalated out of {len(alerts)} reviewed"
        )
        
        return report
    
    def _get_escalation_reason(self, alert: Dict[str, Any]) -> str:
        """
        Get reason why alert is being escalated.
        
        This reads existing data, does not interpret policy.
        
        Args:
            alert: Alert dictionary
            
        Returns:
            Escalation reason string
        """
        # If already escalated, return existing reason
        if alert.get('escalation', {}).get('escalated', False):
            reason = alert.get('escalation', {}).get('escalation_reason', 'Already escalated')
            return reason
        
        # Otherwise, determine reason based on severity/status
        severity = alert.get('severity', '')
        status = alert.get('status', '')
        
        if severity == 'critical':
            return 'Critical severity - requires immediate human attention'
        
        if severity == 'high' and status == 'new':
            return 'New high-severity alert - requires human triage'
        
        return 'Escalation criteria met'
    
    def log_escalation(
        self,
        report: Dict[str, Any],
        destination: str = 'human_oversight'
    ) -> None:
        """
        Log escalation event.
        
        This is a READ-ONLY operation. It logs to application logs,
        does not modify alert store.
        
        Args:
            report: Escalation report to log
            destination: Where escalation is being sent (for logging only)
        """
        logger.warning(
            f"ESCALATION: {report['escalation_count']} alerts escalated "
            f"to {destination} for organisation {report.get('organisation_id', 'platform')}"
        )
        
        for escalation in report.get('escalations', []):
            logger.warning(
                f"  - Alert {escalation['alert_id']}: {escalation['alert_type']} "
                f"({escalation['severity']}) - {escalation['alert_title']}"
            )
    
    def get_escalation_summary(
        self,
        alerts: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Get summary of escalations.
        
        Args:
            alerts: List of alerts to analyze
            
        Returns:
            Escalation summary dictionary
        """
        escalation_alerts = [
            alert for alert in alerts
            if self.should_escalate(alert)
        ]
        
        summary = {
            'total_alerts': len(alerts),
            'requires_escalation': len(escalation_alerts),
            'by_severity': {},
            'by_type': {},
            'generated_at': datetime.utcnow().isoformat()
        }
        
        # Count escalations by severity
        for alert in escalation_alerts:
            severity = alert.get('severity', 'unknown')
            summary['by_severity'][severity] = summary['by_severity'].get(severity, 0) + 1
        
        # Count escalations by type
        for alert in escalation_alerts:
            alert_type = alert.get('alert_type', 'unknown')
            summary['by_type'][alert_type] = summary['by_type'].get(alert_type, 0) + 1
        
        return summary
