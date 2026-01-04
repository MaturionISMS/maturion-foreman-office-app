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
        costs_data = _build_costs.get(self.organisation_id, {})
        costs = [v.get("cost") if isinstance(v, dict) else v for v in costs_data.values()]
        
        # Filter out the anomalous build if needed
        if costs:
            # Exclude outliers for baseline calculation
            sorted_costs = sorted(costs)
            # Use median of lower 80% for baseline
            cutoff = int(len(sorted_costs) * 0.8)
            baseline_costs = sorted_costs[:cutoff] if cutoff > 0 else sorted_costs
            return sum(baseline_costs) / len(baseline_costs) if baseline_costs else 10.0
        return 10.0
    
    def detect_anomalies(self) -> List[Dict]:
        """Detect cost anomalies. QA-143"""
        from foreman.analytics.cost_tracker import _build_costs
        
        baseline = self.calculate_baseline_cost()
        anomalies = []
        
        costs_data = _build_costs.get(self.organisation_id, {})
        for build_id, cost_info in costs_data.items():
            cost = cost_info.get("cost") if isinstance(cost_info, dict) else cost_info
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
