"""
Alert Reader - Read-only watchdog alert reader.

This module reads watchdog alerts from the maturion-isms runtime alert store.
It is strictly read-only and does NOT:
- Write or modify alerts
- Interpret policy
- Perform remediation
- Make autonomous decisions

All it does:
- Read alerts
- Filter by criteria
- Report status
- Escalate when required
"""

import json
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime


logger = logging.getLogger(__name__)


class AlertReader:
    """
    Read-only alert reader for watchdog runtime.
    
    Responsibilities:
    - Read alerts from alert store (read-only)
    - Filter alerts by criteria
    - Provide alert summary
    - Enforce tenant isolation
    
    Does NOT:
    - Write or modify alerts
    - Interpret policy
    - Perform remediation
    - Make decisions
    """
    
    def __init__(self, alert_store_path: Optional[str] = None):
        """
        Initialize AlertReader.
        
        Args:
            alert_store_path: Path to alert store JSON file
                             Defaults to maturion-isms/runtime/watchdog/watchdog-alerts.json
        """
        if alert_store_path is None:
            # Default to known alert store location
            base_path = Path(__file__).parent.parent.parent.parent
            alert_store_path = base_path / "maturion-isms" / "runtime" / "watchdog" / "watchdog-alerts.json"
        
        self.alert_store_path = Path(alert_store_path)
        logger.info(f"AlertReader initialized with alert store: {self.alert_store_path}")
    
    def read_alerts(self, organisation_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Read alerts from the alert store.
        
        This is a READ-ONLY operation. No writes, no modifications.
        
        Args:
            organisation_id: Optional organisation ID for tenant isolation
                           If provided, only returns alerts for that organisation
                           
        Returns:
            List of alert dictionaries
            
        Raises:
            FileNotFoundError: If alert store not found (escalated, not silent)
            ValueError: If alert store is invalid (escalated, not silent)
        """
        try:
            if not self.alert_store_path.exists():
                error_msg = f"Alert store not found: {self.alert_store_path}"
                logger.error(error_msg)
                raise FileNotFoundError(error_msg)
            
            with open(self.alert_store_path, 'r') as f:
                data = json.load(f)
            
            # Validate basic structure
            if not isinstance(data, dict):
                raise ValueError("Alert store must be a JSON object")
            
            alerts = data.get('alerts', [])
            
            # Tenant isolation: filter by organisation_id if provided
            if organisation_id is not None:
                alerts = [
                    alert for alert in alerts
                    if alert.get('organisation_id') == organisation_id
                ]
                logger.info(f"Filtered to {len(alerts)} alerts for organisation {organisation_id}")
            else:
                logger.info(f"Read {len(alerts)} alerts (no tenant filter)")
            
            return alerts
            
        except FileNotFoundError:
            # Re-raise - this is an escalation, not a silent failure
            raise
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON in alert store: {e}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error reading alerts: {e}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
    
    def get_active_alerts(self, organisation_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get only active (unresolved) alerts.
        
        Active means status is NOT 'resolved' or 'false_positive'.
        
        Args:
            organisation_id: Optional organisation ID for tenant isolation
            
        Returns:
            List of active alert dictionaries
        """
        alerts = self.read_alerts(organisation_id=organisation_id)
        
        active_alerts = [
            alert for alert in alerts
            if alert.get('status') not in ['resolved', 'false_positive']
        ]
        
        logger.info(f"Found {len(active_alerts)} active alerts")
        return active_alerts
    
    def get_critical_alerts(self, organisation_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get critical severity alerts.
        
        Args:
            organisation_id: Optional organisation ID for tenant isolation
            
        Returns:
            List of critical alert dictionaries
        """
        alerts = self.read_alerts(organisation_id=organisation_id)
        
        critical_alerts = [
            alert for alert in alerts
            if alert.get('severity') == 'critical'
        ]
        
        logger.info(f"Found {len(critical_alerts)} critical alerts")
        return critical_alerts
    
    def get_alerts_by_type(
        self,
        alert_type: str,
        organisation_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get alerts by type.
        
        Args:
            alert_type: Alert type to filter by (e.g., 'compliance_drift')
            organisation_id: Optional organisation ID for tenant isolation
            
        Returns:
            List of matching alert dictionaries
        """
        alerts = self.read_alerts(organisation_id=organisation_id)
        
        filtered_alerts = [
            alert for alert in alerts
            if alert.get('alert_type') == alert_type
        ]
        
        logger.info(f"Found {len(filtered_alerts)} alerts of type {alert_type}")
        return filtered_alerts
    
    def get_alert_summary(self, organisation_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get summary of alert status.
        
        Provides counts by severity, type, and status.
        
        Args:
            organisation_id: Optional organisation ID for tenant isolation
            
        Returns:
            Dictionary with alert summary statistics
        """
        alerts = self.read_alerts(organisation_id=organisation_id)
        
        summary = {
            'total_alerts': len(alerts),
            'active_alerts': len([a for a in alerts if a.get('status') not in ['resolved', 'false_positive']]),
            'by_severity': {},
            'by_type': {},
            'by_status': {},
            'escalated_count': len([a for a in alerts if a.get('escalation', {}).get('escalated', False)]),
            'organisation_id': organisation_id,
            'generated_at': datetime.utcnow().isoformat()
        }
        
        # Count by severity
        for alert in alerts:
            severity = alert.get('severity', 'unknown')
            summary['by_severity'][severity] = summary['by_severity'].get(severity, 0) + 1
        
        # Count by type
        for alert in alerts:
            alert_type = alert.get('alert_type', 'unknown')
            summary['by_type'][alert_type] = summary['by_type'].get(alert_type, 0) + 1
        
        # Count by status
        for alert in alerts:
            status = alert.get('status', 'unknown')
            summary['by_status'][status] = summary['by_status'].get(status, 0) + 1
        
        logger.info(f"Generated alert summary: {summary['total_alerts']} total, {summary['active_alerts']} active")
        return summary
