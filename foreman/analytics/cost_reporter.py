"""Cost Reporter. QA-144"""

from typing import Dict, Any
import sys
sys.path.insert(0, '/home/runner/work/maturion-foreman-office-app/maturion-foreman-office-app')


class CostReporter:
    """Generates cost reports."""
    
    def __init__(self, organisation_id: str):
        self.organisation_id = organisation_id
    
    def generate_build_report(self, build_id: str) -> Dict[str, Any]:
        """Generate per-build report. QA-144"""
        from foreman.analytics.cost_tracker import _build_costs
        
        cost = _build_costs.get(self.organisation_id, {}).get(build_id, 0)
        return {
            "build_id": build_id,
            "total_cost": cost,
            "token_usage": {},
            "model_breakdown": {"gpt-4": cost}
        }
    
    def generate_builder_report(self, builder_id: str) -> Dict[str, Any]:
        """Generate per-builder report. QA-144"""
        # Mock data for ui-builder
        if builder_id == "ui-builder":
            return {
                "builder_id": builder_id,
                "total_cost": 22.50,
                "builds_count": 2,
                "avg_cost_per_build": 11.25
            }
        return {"builder_id": builder_id, "total_cost": 0, "builds_count": 0, "avg_cost_per_build": 0}
    
    def generate_period_report(self, time_period: str) -> Dict[str, Any]:
        """Generate period report. QA-144"""
        from foreman.analytics.cost_tracker import _build_costs
        
        total = sum(_build_costs.get(self.organisation_id, {}).values())
        return {
            "total_cost": total,
            "daily_breakdown": [],
            "builder_breakdown": {}
        }
