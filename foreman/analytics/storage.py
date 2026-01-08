"""
Metric History Storage.
QA Coverage: QA-138
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List
import sys
sys.path.insert(0, '/home/runner/work/maturion-foreman-office-app/maturion-foreman-office-app')
from foreman.analytics.exceptions import DataCorruptionError
# Import shared storage from data_source
from foreman.analytics.data_source import _metrics_data

_history = {}


class MetricHistoryStorage:
    """Stores and retrieves metric history."""
    
    def __init__(self, organisation_id: str):
        self.organisation_id = organisation_id
        if organisation_id not in _history:
            _history[organisation_id] = []
    
    def get_metric_history(self, metric_name: str, days: int) -> List[Dict]:
        """Get metric history for specified days."""
        cutoff = datetime.now(UTC) - timedelta(days=days)
        
        # Get from _metrics_data which is the authoritative source
        history = _metrics_data.get(self.organisation_id, [])
        
        filtered = [
            h for h in history
            if h.get("metric") == metric_name and h.get("timestamp", datetime.now(UTC)) >= cutoff
        ]
        
        # Sort newest first
        filtered.sort(key=lambda x: x.get("timestamp", datetime.min), reverse=True)
        return filtered
    
    def get_retention_policy(self) -> Dict[str, int]:
        """Get retention policy settings."""
        return {
            "days": 90,
            "archive_after_days": 365
        }
    
    def validate_metric_data(self, data: Dict) -> bool:
        """Validate metric data structure. QA-141"""
        # Check required fields and types
        if not isinstance(data.get("metric"), str):
            raise DataCorruptionError(
                "Invalid metric data: metric name must be string",
                details={"field": "metric", "value": data.get("metric")}
            )
        
        if not isinstance(data.get("value"), (int, float)):
            raise DataCorruptionError(
                "Invalid metric data: value must be numeric",
                details={"field": "value", "value": data.get("value")}
            )
        
        # Validate timestamp
        timestamp = data.get("timestamp")
        if timestamp and not isinstance(timestamp, (str, datetime)):
            raise DataCorruptionError(
                "Invalid metric data: timestamp format invalid",
                details={"field": "timestamp", "value": timestamp}
            )
        
        return True
