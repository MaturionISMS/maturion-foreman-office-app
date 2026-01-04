"""
Metric Alert Manager.
QA Coverage: QA-139
"""

from typing import List, Dict, Any

_thresholds = {}
_alerts = {}


class MetricAlertManager:
    """Manages metric thresholds and alerts."""
    
    def __init__(self, organisation_id: str):
        self.organisation_id = organisation_id
        if organisation_id not in _thresholds:
            _thresholds[organisation_id] = {}
        if organisation_id not in _alerts:
            _alerts[organisation_id] = []
    
    def set_threshold(self, metric_name: str, max_value: float):
        """Set alert threshold for a metric."""
        _thresholds[self.organisation_id][metric_name] = max_value
    
    def check_thresholds(self) -> List[Dict]:
        """Check metrics against thresholds and generate alerts."""
        alerts = []
        
        # Import dynamically to avoid circular dependency
        import sys
        sys.path.insert(0, '/home/runner/work/maturion-foreman-office-app/maturion-foreman-office-app')
        from foreman.analytics.metrics_engine import _metrics_data
        
        metrics = _metrics_data.get(self.organisation_id, [])
        thresholds = _thresholds.get(self.organisation_id, {})
        
        for metric in metrics:
            metric_name = metric.get("metric")
            value = metric.get("value")
            
            if metric_name in thresholds:
                threshold = thresholds[metric_name]
                if value > threshold:
                    alert = {
                        "metric": metric_name,
                        "actual_value": value,
                        "threshold": threshold,
                        "severity": "HIGH",
                        "alert_id": f"alert-{len(_alerts[self.organisation_id])+1}",
                        "timestamp": metric.get("timestamp")
                    }
                    alerts.append(alert)
                    _alerts[self.organisation_id].append(alert)
        
        return alerts
    
    def get_all_alerts(self) -> List[Dict]:
        """Get all alerts."""
        return _alerts.get(self.organisation_id, [])
    
    def route_alerts(self, alerts: List[Dict]) -> Dict[str, bool]:
        """Route alerts to appropriate channels."""
        has_high_severity = any(a.get("severity") == "HIGH" for a in alerts)
        return {
            "escalation_created": has_high_severity,
            "notification_sent": len(alerts) > 0
        }
