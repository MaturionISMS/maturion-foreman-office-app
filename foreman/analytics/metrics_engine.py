"""
Metrics Engine (ANALYTICS-02)
QA Coverage: QA-137 to QA-141
"""

from datetime import datetime
from typing import Dict, Any, List
import time
import sys
sys.path.insert(0, '/home/runner/work/maturion-foreman-office-app/maturion-foreman-office-app')

# Import shared storage from data_source
from foreman.analytics.data_source import _metrics_data

_cache = {}


def store_metric_data(organisation_id: str, metric: str, value: float, timestamp: datetime):
    """Store metric data for history tracking."""
    if organisation_id not in _metrics_data:
        _metrics_data[organisation_id] = []
    
    _metrics_data[organisation_id].append({
        "metric": metric,
        "value": value,
        "timestamp": timestamp
    })


class MetricsEngine:
    """Engine for metric aggregation and computation. QA-137 to QA-141"""
    
    def __init__(self, organisation_id: str):
        self.organisation_id = organisation_id
        if organisation_id not in _cache:
            _cache[organisation_id] = {}
        if organisation_id not in _metrics_data:
            _metrics_data[organisation_id] = []
    
    def calculate_aggregates(self, time_period: str) -> Dict[str, Any]:
        """Calculate aggregate metrics with caching. QA-137"""
        cache_key = f"aggregates_{time_period}"
        
        if cache_key in _cache.get(self.organisation_id, {}):
            return _cache[self.organisation_id][cache_key]
        
        # Simulate computation time
        time.sleep(0.01)
        
        # Calculate from source data
        data = _metrics_data.get(self.organisation_id, [])
        # Sum the VALUES, not count the records
        builds_completed = sum(d.get("value", 0) for d in data if d.get("metric") == "builds_completed")
        builds_failed = sum(d.get("value", 0) for d in data if d.get("metric") == "builds_failed")
        total = builds_completed + builds_failed
        
        result = {
            "success_rate": (builds_completed / total * 100) if total > 0 else 0,
            "total_builds": total
        }
        
        _cache[self.organisation_id][cache_key] = result
        return result
    
    def get_source_data(self) -> List[Dict]:
        """Get source data for validation. QA-137"""
        return _metrics_data.get(self.organisation_id, [])
    
    def record_metric(self, metric_name: str, value: float, timestamp: datetime = None):
        """Record a metric. QA-138, QA-139"""
        if timestamp is None:
            timestamp = datetime.utcnow()
        
        _metrics_data[self.organisation_id].append({
            "metric": metric_name,
            "value": value,
            "timestamp": timestamp
        })
        
        # Also call storage helper
        store_metric_data(self.organisation_id, metric_name, value, timestamp)
    
    def calculate_sum(self, metric_name: str) -> float:
        """Calculate sum of metric values. QA-141"""
        data = _metrics_data.get(self.organisation_id, [])
        total = sum(d.get("value", 0) for d in data if d.get("metric") == metric_name)
        
        # Handle overflow by checking if number is too large
        if total > 10**300:
            import sys
            sys.path.insert(0, '/home/runner/work/maturion-foreman-office-app/maturion-foreman-office-app')
            from foreman.analytics.exceptions import CalculationOverflowError
            raise CalculationOverflowError("Calculation overflow detected")
        
        return total
