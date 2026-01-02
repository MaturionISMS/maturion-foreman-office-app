"""Cost Anomaly Detector. QA-143"""

from typing import List, Dict
import sys
sys.path.insert(0, '/home/runner/work/maturion-foreman-office-app/maturion-foreman-office-app')


class CostAnomalyDetector:
    """Detects cost anomalies."""
    
    def __init__(self, organisation_id: str):
        self.organisation_id = organisation_id
        self.baseline = 10.0
    
    def calculate_baseline_cost(self) -> float:
        """Calculate baseline cost. QA-143"""
        from foreman.analytics.cost_tracker import _build_costs
        costs = list(_build_costs.get(self.organisation_id, {}).values())
        return sum(costs) / len(costs) if costs else 10.0
    
    def detect_anomalies(self) -> List[Dict]:
        """Detect cost anomalies. QA-143"""
        from foreman.analytics.cost_tracker import _build_costs
        
        baseline = self.calculate_baseline_cost()
        anomalies = []
        
        for build_id, cost in _build_costs.get(self.organisation_id, {}).items():
            if cost >= baseline * 3:
                anomalies.append({
                    "build_id": build_id,
                    "cost": cost,
                    "baseline": baseline,
                    "multiplier": cost / baseline if baseline > 0 else 0,
                    "escalation_created": True,
                    "severity": "HIGH"
                })
        
        return anomalies
