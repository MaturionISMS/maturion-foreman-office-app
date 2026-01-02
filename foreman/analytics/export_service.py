"""
Metrics Export Service.
QA Coverage: QA-140
"""

from pathlib import Path
import json
import csv
from typing import Any

import sys
sys.path.insert(0, '/home/runner/work/maturion-foreman-office-app/maturion-foreman-office-app')


class MetricsExporter:
    """Exports metrics to various formats."""
    
    def export_to_csv(self, organisation_id: str, output_path: Path, time_period: str):
        """Export metrics to CSV format. QA-140"""
        from foreman.analytics.metrics_engine import _metrics_data
        
        metrics = _metrics_data.get(organisation_id, [])
        
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["metric", "value", "timestamp"])
            
            for metric in metrics:
                writer.writerow([
                    metric.get("metric"),
                    metric.get("value"),
                    metric.get("timestamp", "").isoformat() if hasattr(metric.get("timestamp", ""), "isoformat") else str(metric.get("timestamp", ""))
                ])
    
    def export_to_json(self, organisation_id: str, output_path: Path, time_period: str):
        """Export metrics to JSON format. QA-140"""
        from foreman.analytics.metrics_engine import _metrics_data
        
        metrics = _metrics_data.get(organisation_id, [])
        
        export_data = {
            "metrics": [
                {
                    "metric_name": m.get("metric"),
                    "value": m.get("value"),
                    "timestamp": m.get("timestamp", "").isoformat() if hasattr(m.get("timestamp", ""), "isoformat") else str(m.get("timestamp", "")),
                    "organisation_id": organisation_id
                }
                for m in metrics
            ]
        }
        
        with open(output_path, 'w') as jsonfile:
            json.dump(export_data, jsonfile, indent=2)
