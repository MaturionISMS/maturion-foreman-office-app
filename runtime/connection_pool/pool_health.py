"""
Pool Health Monitor

Provides health monitoring for connection pools including health checks,
status tracking, and alerting.
"""

import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum


class HealthStatus(Enum):
    """Health status enumeration"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class HealthCheckResult:
    """Result of a health check"""
    status: HealthStatus
    timestamp: float
    details: Dict[str, Any]
    message: str


class PoolHealthMonitor:
    """
    Pool Health Monitor
    
    Provides comprehensive health monitoring for connection pools including:
    - Health status tracking
    - Pool utilization monitoring
    - Connection timeout tracking
    - Degradation detection
    - Health alerts
    """
    
    def __init__(self, unhealthy_threshold: float = 0.9, degraded_threshold: float = 0.7):
        """
        Initialize health monitor
        
        Args:
            unhealthy_threshold: Pool utilization threshold for unhealthy status (0.0-1.0)
            degraded_threshold: Pool utilization threshold for degraded status (0.0-1.0)
        """
        self.unhealthy_threshold = unhealthy_threshold
        self.degraded_threshold = degraded_threshold
        self._health_history: List[HealthCheckResult] = []
        self._alerts: List[Dict[str, Any]] = []
    
    def check_health(self, pool_stats: Dict[str, Any]) -> HealthCheckResult:
        """
        Check pool health based on statistics
        
        Args:
            pool_stats: Pool statistics dictionary
        
        Returns:
            HealthCheckResult with status and details
        """
        utilization = pool_stats.get('utilization', 0.0)
        timeouts = pool_stats.get('timeouts', 0)
        errors = pool_stats.get('errors', 0)
        current_size = pool_stats.get('current_size', 0)
        min_size = pool_stats.get('min_size', 0)
        
        # Determine health status
        if utilization >= self.unhealthy_threshold:
            status = HealthStatus.UNHEALTHY
            message = f"Pool utilization critically high: {utilization:.1%}"
        elif utilization >= self.degraded_threshold:
            status = HealthStatus.DEGRADED
            message = f"Pool utilization elevated: {utilization:.1%}"
        elif timeouts > 0:
            status = HealthStatus.DEGRADED
            message = f"Pool experiencing timeouts: {timeouts}"
        elif errors > 0:
            status = HealthStatus.DEGRADED
            message = f"Pool experiencing errors: {errors}"
        elif current_size < min_size:
            status = HealthStatus.DEGRADED
            message = f"Pool below minimum size: {current_size} < {min_size}"
        else:
            status = HealthStatus.HEALTHY
            message = "Pool operating normally"
        
        # Create health check result
        result = HealthCheckResult(
            status=status,
            timestamp=time.time(),
            details={
                'utilization': utilization,
                'timeouts': timeouts,
                'errors': errors,
                'current_size': current_size,
                'min_size': min_size,
                'max_size': pool_stats.get('max_size', 0),
                'available': pool_stats.get('available', 0),
                'in_use': pool_stats.get('in_use', 0)
            },
            message=message
        )
        
        # Record in history
        self._health_history.append(result)
        
        # Generate alerts for unhealthy or degraded status
        if status in [HealthStatus.UNHEALTHY, HealthStatus.DEGRADED]:
            self._generate_alert(result)
        
        return result
    
    def _generate_alert(self, result: HealthCheckResult) -> None:
        """Generate health alert"""
        alert = {
            'type': 'health_alert',
            'status': result.status.value,
            'message': result.message,
            'timestamp': result.timestamp,
            'details': result.details
        }
        self._alerts.append(alert)
    
    def get_current_status(self) -> Optional[HealthStatus]:
        """Get current health status"""
        if not self._health_history:
            return HealthStatus.UNKNOWN
        return self._health_history[-1].status
    
    def get_health_history(self, limit: int = 10) -> List[HealthCheckResult]:
        """
        Get recent health check history
        
        Args:
            limit: Maximum number of recent checks to return
        
        Returns:
            List of recent health check results
        """
        return self._health_history[-limit:]
    
    def get_alerts(self) -> List[Dict[str, Any]]:
        """Get all health alerts"""
        return self._alerts.copy()
    
    def clear_alerts(self) -> None:
        """Clear all health alerts"""
        self._alerts.clear()
    
    def get_health_summary(self) -> Dict[str, Any]:
        """
        Get health summary statistics
        
        Returns:
            Dictionary with health metrics and trends
        """
        if not self._health_history:
            return {
                'current_status': HealthStatus.UNKNOWN.value,
                'total_checks': 0,
                'healthy_count': 0,
                'degraded_count': 0,
                'unhealthy_count': 0,
                'alert_count': len(self._alerts)
            }
        
        recent_checks = self._health_history[-10:]
        
        healthy_count = sum(1 for c in recent_checks if c.status == HealthStatus.HEALTHY)
        degraded_count = sum(1 for c in recent_checks if c.status == HealthStatus.DEGRADED)
        unhealthy_count = sum(1 for c in recent_checks if c.status == HealthStatus.UNHEALTHY)
        
        return {
            'current_status': self._health_history[-1].status.value,
            'total_checks': len(self._health_history),
            'recent_healthy_count': healthy_count,
            'recent_degraded_count': degraded_count,
            'recent_unhealthy_count': unhealthy_count,
            'alert_count': len(self._alerts),
            'health_percentage': healthy_count / len(recent_checks) if recent_checks else 0.0
        }
