"""
Pool Statistics

Provides statistics collection and reporting for connection pools.
"""

from typing import Dict, Any, List
from dataclasses import dataclass
import time


@dataclass
class PoolStatistics:
    """
    Pool Statistics Container
    
    Stores and provides access to pool statistics including:
    - Connection metrics (acquisitions, releases, creations, destructions)
    - Performance metrics (timeouts, errors)
    - Utilization metrics
    - Historical trends
    """
    
    def __init__(self):
        """Initialize statistics container"""
        self._snapshots: List[Dict[str, Any]] = []
    
    def record_snapshot(self, stats: Dict[str, Any]) -> None:
        """
        Record a statistics snapshot
        
        Args:
            stats: Statistics dictionary from connection pool
        """
        snapshot = {
            **stats,
            'timestamp': time.time()
        }
        self._snapshots.append(snapshot)
    
    def get_latest(self) -> Dict[str, Any]:
        """Get latest statistics snapshot"""
        if not self._snapshots:
            return {}
        return self._snapshots[-1]
    
    def get_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get statistics history
        
        Args:
            limit: Maximum number of snapshots to return
        
        Returns:
            List of recent statistics snapshots
        """
        return self._snapshots[-limit:]
    
    def get_trend_analysis(self) -> Dict[str, Any]:
        """
        Analyze trends in pool statistics
        
        Returns:
            Dictionary with trend analysis
        """
        if len(self._snapshots) < 2:
            return {
                'trend': 'insufficient_data',
                'snapshots_available': len(self._snapshots)
            }
        
        # Compare recent vs. older snapshots
        recent_window = self._snapshots[-5:] if len(self._snapshots) >= 5 else self._snapshots
        older_window = self._snapshots[:5] if len(self._snapshots) >= 10 else self._snapshots[:len(self._snapshots)//2]
        
        # Calculate averages
        recent_utilization = sum(s.get('utilization', 0) for s in recent_window) / len(recent_window)
        older_utilization = sum(s.get('utilization', 0) for s in older_window) / len(older_window)
        
        recent_timeouts = sum(s.get('timeouts', 0) for s in recent_window) / len(recent_window)
        older_timeouts = sum(s.get('timeouts', 0) for s in older_window) / len(older_window)
        
        # Determine trend
        if recent_utilization > older_utilization * 1.2:
            trend = 'increasing_load'
        elif recent_utilization < older_utilization * 0.8:
            trend = 'decreasing_load'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'recent_utilization': recent_utilization,
            'older_utilization': older_utilization,
            'recent_timeouts': recent_timeouts,
            'older_timeouts': older_timeouts,
            'utilization_change': recent_utilization - older_utilization,
            'timeout_change': recent_timeouts - older_timeouts
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics summary
        
        Returns:
            Dictionary with aggregated statistics
        """
        if not self._snapshots:
            return {
                'total_snapshots': 0,
                'average_utilization': 0.0,
                'peak_utilization': 0.0,
                'total_acquisitions': 0,
                'total_releases': 0,
                'total_timeouts': 0,
                'total_errors': 0
            }
        
        latest = self._snapshots[-1]
        
        # Calculate averages from recent snapshots
        recent = self._snapshots[-10:]
        avg_utilization = sum(s.get('utilization', 0) for s in recent) / len(recent)
        peak_utilization = max(s.get('utilization', 0) for s in recent)
        
        return {
            'total_snapshots': len(self._snapshots),
            'average_utilization': avg_utilization,
            'peak_utilization': peak_utilization,
            'current_size': latest.get('current_size', 0),
            'available': latest.get('available', 0),
            'in_use': latest.get('in_use', 0),
            'total_acquisitions': latest.get('acquisitions', 0),
            'total_releases': latest.get('releases', 0),
            'total_creations': latest.get('creations', 0),
            'total_destructions': latest.get('destructions', 0),
            'total_timeouts': latest.get('timeouts', 0),
            'total_errors': latest.get('errors', 0)
        }
    
    def clear(self) -> None:
        """Clear all statistics history"""
        self._snapshots.clear()
