"""
Metric History Storage.
QA Coverage: QA-138
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List

_history = {}


class MetricHistoryStorage:
    """Stores and retrieves metric history."""
    
    def __init__(self, organisation_id: str):
        self.organisation_id = organisation_id
        if organisation_id not in _history:
            _history[organisation_id] = []
    
    def get_metric_history(self, metric_name: str, days: int) -> List[Dict]:
        """Get metric history for specified days."""
        cutoff = datetime.utcnow() - timedelta(days=days)
        history = _history.get(self.organisation_id, [])
        
        filtered = [
            h for h in history
            if h.get("metric") == metric_name and h.get("timestamp", datetime.utcnow()) >= cutoff
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
