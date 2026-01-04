"""
Analytics UI Renderer (part of ANALYTICS-01)

Renders analytics sections and handles failure modes for UI display.

QA Coverage: QA-132, QA-136 (rendering and failure modes)
"""

from typing import Dict, Any
import sys
sys.path.insert(0, '/home/runner/work/maturion-foreman-office-app/maturion-foreman-office-app')
from foreman.analytics.exceptions import DataLoadError, CalculationError


class AnalyticsRenderer:
    """
    Renders analytics data for UI display.
    
    QA-132: Renders analytics section
    QA-136: Error UX rendering
    """
    
    def render_analytics_section(self, analytics_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Render analytics section from summary data.
        
        Returns structured data for UI rendering including charts and selectors.
        """
        rendered = {
            "builder_activations": analytics_data.get("builder_activations", 0),
            "intent_submissions": analytics_data.get("intent_submissions", 0),
            "build_executions": analytics_data.get("build_executions", 0),
            "charts": [
                {
                    "type": "line",
                    "title": "Build Trend",
                    "data": []
                }
            ],
            "time_period_selector": analytics_data.get("time_period_selector", {})
        }
        
        return rendered
    
    def render_error_state(self, error: DataLoadError) -> Dict[str, Any]:
        """
        Render error UI for data load failures.
        
        QA-136: Data load failure UX
        """
        return {
            "error_message": "Unable to load analytics data. Please try again.",
            "retry_button": True,
            "technical_details": str(error)
        }
    
    def render_calculation_error(self, error: CalculationError) -> Dict[str, Any]:
        """
        Render error UI for calculation failures.
        
        QA-136: Calculation error handling
        """
        return {
            "error_message": "Error calculating metrics. Data may be incomplete.",
            "retry_button": True,
            "technical_details": str(error)
        }
