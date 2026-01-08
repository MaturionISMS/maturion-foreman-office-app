"""
Trend Analyzer for Advanced Analytics Phase 2.

QA Coverage: QA-446 to QA-450
Provides trend calculation, visualization, forecasting, anomaly detection, and comparison.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from statistics import mean, stdev
import sys
sys.path.insert(0, '/home/runner/work/maturion-foreman-office-app/maturion-foreman-office-app')

# Shared storage for trend data
_trend_data = {}


def clear_all():
    """Clear all trend analyzer state for testing."""
    global _trend_data
    _trend_data = {}


class TrendAnalyzer:
    """Analyzes trends in metrics and data over time. QA-446 to QA-450"""
    
    def __init__(self, organisation_id: str):
        """
        Initialize trend analyzer for organisation.
        
        Args:
            organisation_id: Organisation ID for tenant isolation
        """
        self.organisation_id = organisation_id
        if organisation_id not in _trend_data:
            _trend_data[organisation_id] = {}
    
    def calculate_trend(self, metric_name: str, data_points: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate trend from data points. QA-446
        
        Args:
            metric_name: Name of the metric to analyze
            data_points: List of data points with 'timestamp' and 'value'
        
        Returns:
            Trend analysis with direction, slope, and confidence
        """
        if not data_points:
            return {
                "direction": "stable",
                "slope": 0.0,
                "confidence": 0.0,
                "data_point_count": 0
            }
        
        # Sort by timestamp
        sorted_points = sorted(data_points, key=lambda x: x.get('timestamp', ''))
        values = [p.get('value', 0) for p in sorted_points]
        
        # Calculate simple linear trend
        n = len(values)
        if n < 2:
            return {
                "direction": "stable",
                "slope": 0.0,
                "confidence": 0.5,
                "data_point_count": n
            }
        
        # Simple linear regression
        x = list(range(n))
        x_mean = mean(x)
        y_mean = mean(values)
        
        numerator = sum((x[i] - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        slope = numerator / denominator if denominator != 0 else 0.0
        
        # Determine direction and confidence
        direction = "increasing" if slope > 0.1 else "decreasing" if slope < -0.1 else "stable"
        confidence = min(abs(slope) * 10, 1.0)  # Normalize confidence to 0-1
        
        # Store trend data
        trend_id = f"{metric_name}_{datetime.now().timestamp()}"
        _trend_data[self.organisation_id][trend_id] = {
            "metric_name": metric_name,
            "direction": direction,
            "slope": slope,
            "confidence": confidence,
            "data_point_count": n,
            "calculated_at": datetime.now().isoformat()
        }
        
        return {
            "direction": direction,
            "slope": slope,
            "confidence": confidence,
            "data_point_count": n
        }
    
    def prepare_visualization_data(self, metric_name: str, data_points: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Prepare data for trend visualization. QA-447
        
        Args:
            metric_name: Name of the metric
            data_points: List of data points
        
        Returns:
            Visualization-ready data with series, axes, and formatting
        """
        if not data_points:
            return {
                "series": [],
                "x_axis": {"label": "Time", "values": []},
                "y_axis": {"label": metric_name, "values": []},
                "chart_type": "line"
            }
        
        sorted_points = sorted(data_points, key=lambda x: x.get('timestamp', ''))
        
        return {
            "series": [
                {
                    "name": metric_name,
                    "data": [p.get('value', 0) for p in sorted_points]
                }
            ],
            "x_axis": {
                "label": "Time",
                "values": [p.get('timestamp', '') for p in sorted_points]
            },
            "y_axis": {
                "label": metric_name,
                "values": [p.get('value', 0) for p in sorted_points]
            },
            "chart_type": "line"
        }
    
    def forecast_trend(self, metric_name: str, data_points: List[Dict[str, Any]], periods: int) -> Dict[str, Any]:
        """
        Forecast future trend values. QA-448
        
        Args:
            metric_name: Name of the metric
            data_points: Historical data points
            periods: Number of future periods to forecast
        
        Returns:
            Forecast with predicted values and confidence intervals
        """
        if not data_points or periods <= 0:
            return {
                "forecast_values": [],
                "confidence_interval": {"lower": [], "upper": []},
                "accuracy_estimate": 0.0
            }
        
        # Calculate trend first
        trend = self.calculate_trend(metric_name, data_points)
        slope = trend["slope"]
        
        # Get last value
        sorted_points = sorted(data_points, key=lambda x: x.get('timestamp', ''))
        last_value = sorted_points[-1].get('value', 0)
        
        # Generate forecast
        forecast_values = []
        for i in range(1, periods + 1):
            predicted_value = last_value + (slope * i)
            forecast_values.append(predicted_value)
        
        # Simple confidence intervals (±10% for demonstration)
        confidence_margin = 0.1
        confidence_interval = {
            "lower": [v * (1 - confidence_margin) for v in forecast_values],
            "upper": [v * (1 + confidence_margin) for v in forecast_values]
        }
        
        return {
            "forecast_values": forecast_values,
            "confidence_interval": confidence_interval,
            "accuracy_estimate": trend["confidence"]
        }
    
    def detect_anomalies(self, metric_name: str, data_points: List[Dict[str, Any]], sensitivity: float = 2.0) -> List[Dict[str, Any]]:
        """
        Detect anomalies in trend data. QA-449
        
        Args:
            metric_name: Name of the metric
            data_points: Data points to analyze
            sensitivity: Standard deviations for anomaly threshold
        
        Returns:
            List of detected anomalies with timestamps and values
        """
        if not data_points or len(data_points) < 3:
            return []
        
        values = [p.get('value', 0) for p in data_points]
        value_mean = mean(values)
        
        # Calculate standard deviation, but handle case where all values are identical
        try:
            value_std = stdev(values) if len(values) > 1 else 0
        except:
            value_std = 0
        
        if value_std == 0:
            # If std is 0, use a percentage-based threshold instead
            threshold = abs(value_mean) * 0.5  # 50% deviation from mean
            if threshold == 0:
                return []
        else:
            threshold = sensitivity * value_std
        
        anomalies = []
        
        for point in data_points:
            value = point.get('value', 0)
            deviation = abs(value - value_mean)
            
            if deviation > threshold:
                anomalies.append({
                    "timestamp": point.get('timestamp', ''),
                    "value": value,
                    "deviation": deviation,
                    "severity": "high" if deviation > threshold * 1.5 else "medium"
                })
        
        return anomalies
    
    def compare_trends(self, metric_name_1: str, data_points_1: List[Dict[str, Any]], 
                      metric_name_2: str, data_points_2: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compare two trends. QA-450
        
        Args:
            metric_name_1: Name of first metric
            data_points_1: Data points for first metric
            metric_name_2: Name of second metric
            data_points_2: Data points for second metric
        
        Returns:
            Comparison analysis with correlation and divergence
        """
        trend_1 = self.calculate_trend(metric_name_1, data_points_1)
        trend_2 = self.calculate_trend(metric_name_2, data_points_2)
        
        # Calculate correlation (simplified)
        values_1 = [p.get('value', 0) for p in data_points_1]
        values_2 = [p.get('value', 0) for p in data_points_2]
        
        # Ensure same length for correlation
        min_len = min(len(values_1), len(values_2))
        if min_len == 0:
            correlation = 0.0
        else:
            values_1 = values_1[:min_len]
            values_2 = values_2[:min_len]
            
            if len(values_1) < 2:
                correlation = 0.0
            else:
                mean_1 = mean(values_1)
                mean_2 = mean(values_2)
                std_1 = stdev(values_1) if len(values_1) > 1 else 0
                std_2 = stdev(values_2) if len(values_2) > 1 else 0
                
                if std_1 == 0 or std_2 == 0:
                    correlation = 0.0
                else:
                    covariance = sum((values_1[i] - mean_1) * (values_2[i] - mean_2) for i in range(min_len)) / min_len
                    correlation = covariance / (std_1 * std_2)
        
        # Calculate divergence (difference in slopes)
        divergence = abs(trend_1["slope"] - trend_2["slope"])
        
        return {
            "trend_1": trend_1,
            "trend_2": trend_2,
            "correlation": correlation,
            "divergence": divergence,
            "relationship": "correlated" if abs(correlation) > 0.7 else "divergent" if divergence > 0.5 else "independent"
        }
