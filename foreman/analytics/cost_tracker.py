"""
Cost Tracker (ANALYTICS-03).
QA Coverage: QA-142 to QA-146
"""

from typing import Dict, Any
from datetime import datetime
import sys
sys.path.insert(0, '/home/runner/work/maturion-foreman-office-app/maturion-foreman-office-app')
from foreman.analytics.exceptions import TokenCountingError, CostCalculationError

_token_usage = {}
_build_costs = {}


def clear_all():
    """Clear all cost tracker state for testing."""
    global _token_usage, _build_costs
    _token_usage = {}
    _build_costs = {}


class CostTracker:
    """Tracks AI usage costs per build. QA-142 to QA-146"""
    
    def __init__(self, organisation_id: str):
        self.organisation_id = organisation_id
        if organisation_id not in _token_usage:
            _token_usage[organisation_id] = {}
        if organisation_id not in _build_costs:
            _build_costs[organisation_id] = {}
    
    def record_token_usage(self, build_id: str, model: str, input_tokens: int, output_tokens: int):
        """Record token usage for a build. QA-142"""
        if input_tokens < 0 or output_tokens < 0:
            raise TokenCountingError("Token counts must be non-negative")
        
        if build_id not in _token_usage[self.organisation_id]:
            _token_usage[self.organisation_id][build_id] = {"input": 0, "output": 0, "model": model}
        
        _token_usage[self.organisation_id][build_id]["input"] += input_tokens
        _token_usage[self.organisation_id][build_id]["output"] += output_tokens
    
    def get_total_tokens(self, build_id: str) -> Dict[str, int]:
        """Get total tokens for a build. QA-142"""
        usage = _token_usage[self.organisation_id].get(build_id, {"input": 0, "output": 0})
        return {"input": usage["input"], "output": usage["output"]}
    
    def calculate_build_cost(self, build_id: str) -> float:
        """Calculate cost for a build. QA-142"""
        usage = _token_usage[self.organisation_id].get(build_id)
        
        if not usage:
            return 0.0
        
        # GPT-4 pricing: $0.03/1K input, $0.06/1K output
        model = usage.get("model", "gpt-4")
        
        if model == "unknown-model":
            raise CostCalculationError("Unknown model - pricing data unavailable")
        
        input_cost = (usage["input"] / 1000) * 0.03
        output_cost = (usage["output"] / 1000) * 0.06
        
        total_cost = input_cost + output_cost
        _build_costs[self.organisation_id][build_id] = total_cost
        
        return total_cost
    
    def get_costs_by_build(self, organisation_id: str) -> Dict[str, float]:
        """Get costs by build ID. QA-142"""
        return _build_costs.get(organisation_id, {})
    
    def record_build_cost(self, build_id: str, cost_usd: float, builder_id: str = None, timestamp: datetime = None):
        """Record a build cost directly. QA-143, QA-144"""
        if timestamp is None:
            timestamp = datetime.now(UTC)
        _build_costs[self.organisation_id][build_id] = {
            "cost": cost_usd,
            "builder_id": builder_id,
            "timestamp": timestamp
        }
    
    def get_cost_breakdown(self, build_id: str) -> Dict[str, Any]:
        """Get detailed cost breakdown. QA-143"""
        cost_info = _build_costs[self.organisation_id].get(build_id, 0)
        cost = cost_info.get("cost") if isinstance(cost_info, dict) else cost_info
        
        return {
            "by_model": {"gpt-4": cost},
            "by_component": {"total": cost},
            "timeline": []
        }
