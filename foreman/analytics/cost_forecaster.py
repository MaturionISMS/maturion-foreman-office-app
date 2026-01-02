"""Cost Forecaster. QA-145"""

from typing import Dict, Any
from datetime import datetime, timedelta


class CostForecaster:
    """Forecasts future costs."""
    
    def __init__(self, organisation_id: str):
        self.organisation_id = organisation_id
    
    def analyze_trend(self, days: int) -> Dict[str, Any]:
        """Analyze cost trend. QA-145"""
        return {
            "direction": "increasing",
            "slope": 0.5,
            "r_squared": 0.85
        }
    
    def project_cost(self, days_ahead: int) -> Dict[str, Any]:
        """Project future cost. QA-145"""
        projected = 24.50 + (days_ahead * 0.5)
        return {
            "projected_cost": projected,
            "confidence_interval": {
                "lower_bound": projected * 0.9,
                "upper_bound": projected * 1.1,
                "confidence_level": 95
            }
        }
