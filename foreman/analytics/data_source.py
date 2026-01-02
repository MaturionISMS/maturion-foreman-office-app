"""
Data Source for Metrics Engine.
QA Coverage: QA-137
"""

from datetime import datetime

_metrics_data = {}


class MetricsDataSource:
    """Provides data source for metrics."""
    
    def __init__(self, organisation_id: str):
        self.organisation_id = organisation_id
        if self.organisation_id not in _metrics_data:
            _metrics_data[self.organisation_id] = []
    
    def add_metric(self, metric_name: str, value: float, timestamp: datetime):
        """Add a metric data point."""
        _metrics_data[self.organisation_id].append({
            "metric": metric_name,
            "value": value,
            "timestamp": timestamp
        })
