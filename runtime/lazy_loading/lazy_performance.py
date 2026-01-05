"""
Lazy Performance Monitor

Provides performance monitoring for lazy loading operations including
timing, metrics collection, and performance analysis.
"""

import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class PerformanceMetrics:
    """Performance metrics for a lazy load operation"""
    key: str
    load_time: float
    timestamp: float
    cache_hit: bool
    success: bool
    error: Optional[str] = None


class LazyPerformanceMonitor:
    """
    Lazy Performance Monitor
    
    Provides comprehensive performance monitoring including:
    - Load time tracking
    - Cache hit/miss metrics
    - Performance statistics
    - Trend analysis
    - Performance alerts
    """
    
    def __init__(self, slow_load_threshold: float = 1.0):
        """
        Initialize performance monitor
        
        Args:
            slow_load_threshold: Threshold in seconds for slow load alerts
        """
        self.slow_load_threshold = slow_load_threshold
        self._metrics: List[PerformanceMetrics] = []
        self._alerts: List[Dict[str, Any]] = []
    
    def record_load(
        self, 
        key: str, 
        load_time: float, 
        cache_hit: bool = False,
        success: bool = True,
        error: Optional[str] = None
    ) -> PerformanceMetrics:
        """
        Record a load operation
        
        Args:
            key: Loadable identifier
            load_time: Time taken to load in seconds
            cache_hit: Whether this was a cache hit
            success: Whether load was successful
            error: Error message if failed
        
        Returns:
            PerformanceMetrics object
        """
        metrics = PerformanceMetrics(
            key=key,
            load_time=load_time,
            timestamp=time.time(),
            cache_hit=cache_hit,
            success=success,
            error=error
        )
        
        self._metrics.append(metrics)
        
        # Generate alert for slow loads
        if not cache_hit and load_time > self.slow_load_threshold:
            self._generate_alert(metrics)
        
        return metrics
    
    def _generate_alert(self, metrics: PerformanceMetrics) -> None:
        """Generate performance alert"""
        alert = {
            'type': 'slow_load',
            'key': metrics.key,
            'load_time': metrics.load_time,
            'threshold': self.slow_load_threshold,
            'timestamp': metrics.timestamp
        }
        self._alerts.append(alert)
    
    def get_metrics_for_key(self, key: str) -> List[PerformanceMetrics]:
        """
        Get all metrics for a specific key
        
        Args:
            key: Loadable identifier
        
        Returns:
            List of metrics for the key
        """
        return [m for m in self._metrics if m.key == key]
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get performance statistics
        
        Returns:
        - Total loads
        - Cache hits
        - Average load time
        - Min/max load time
        - Success rate
        - Alert count
        """
        if not self._metrics:
            return {
                'total_loads': 0,
                'cache_hits': 0,
                'average_load_time': 0.0,
                'min_load_time': 0.0,
                'max_load_time': 0.0,
                'success_rate': 0.0,
                'alert_count': 0
            }
        
        actual_loads = [m for m in self._metrics if not m.cache_hit]
        cache_hits = [m for m in self._metrics if m.cache_hit]
        successful = [m for m in self._metrics if m.success]
        
        load_times = [m.load_time for m in actual_loads]
        
        return {
            'total_loads': len(actual_loads),
            'cache_hits': len(cache_hits),
            'average_load_time': sum(load_times) / len(load_times) if load_times else 0.0,
            'min_load_time': min(load_times) if load_times else 0.0,
            'max_load_time': max(load_times) if load_times else 0.0,
            'success_rate': len(successful) / len(self._metrics) if self._metrics else 0.0,
            'alert_count': len(self._alerts),
            'cache_hit_rate': len(cache_hits) / len(self._metrics) if self._metrics else 0.0
        }
    
    def get_alerts(self) -> List[Dict[str, Any]]:
        """Get all performance alerts"""
        return self._alerts.copy()
    
    def clear_alerts(self) -> None:
        """Clear all alerts"""
        self._alerts.clear()
    
    def get_trend_analysis(self, window_size: int = 10) -> Dict[str, Any]:
        """
        Analyze performance trends
        
        Args:
            window_size: Number of recent operations to analyze
        
        Returns:
            Dictionary with trend analysis
        """
        if len(self._metrics) < 2:
            return {
                'trend': 'insufficient_data',
                'metrics_available': len(self._metrics)
            }
        
        # Get recent and older windows
        recent = self._metrics[-window_size:] if len(self._metrics) >= window_size else self._metrics
        older = self._metrics[:window_size] if len(self._metrics) >= window_size * 2 else self._metrics[:len(self._metrics)//2]
        
        # Filter out cache hits for performance comparison
        recent_loads = [m for m in recent if not m.cache_hit]
        older_loads = [m for m in older if not m.cache_hit]
        
        if not recent_loads or not older_loads:
            return {
                'trend': 'insufficient_data',
                'metrics_available': len(self._metrics)
            }
        
        # Calculate averages
        recent_avg = sum(m.load_time for m in recent_loads) / len(recent_loads)
        older_avg = sum(m.load_time for m in older_loads) / len(older_loads)
        
        # Determine trend
        if recent_avg > older_avg * 1.2:
            trend = 'degrading'
        elif recent_avg < older_avg * 0.8:
            trend = 'improving'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'recent_average': recent_avg,
            'older_average': older_avg,
            'performance_change': recent_avg - older_avg,
            'recent_samples': len(recent_loads),
            'older_samples': len(older_loads)
        }
    
    def clear_history(self) -> None:
        """Clear all metrics history"""
        self._metrics.clear()
