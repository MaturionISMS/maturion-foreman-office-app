"""
Cache Statistics Tracking

Provides detailed cache statistics collection and reporting.
"""

from typing import Dict, Any, List
from dataclasses import dataclass, field
import time


@dataclass
class CacheStatistics:
    """
    Cache Statistics Tracker
    
    Provides comprehensive statistics including:
    - Hit rate calculation
    - Miss rate calculation
    - Eviction metrics collection
    - Performance statistics reporting
    """
    
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    invalidations: int = 0
    total_operations: int = 0
    start_time: float = field(default_factory=time.time)
    
    def record_hit(self) -> None:
        """Record a cache hit"""
        self.hits += 1
        self.total_operations += 1
    
    def record_miss(self) -> None:
        """Record a cache miss"""
        self.misses += 1
        self.total_operations += 1
    
    def record_eviction(self) -> None:
        """Record a cache eviction"""
        self.evictions += 1
    
    def record_invalidation(self) -> None:
        """Record a cache invalidation"""
        self.invalidations += 1
    
    def get_hit_rate(self) -> float:
        """Calculate hit rate as percentage"""
        total_requests = self.hits + self.misses
        if total_requests == 0:
            return 0.0
        return self.hits / total_requests
    
    def get_miss_rate(self) -> float:
        """Calculate miss rate as percentage"""
        total_requests = self.hits + self.misses
        if total_requests == 0:
            return 0.0
        return self.misses / total_requests
    
    def get_uptime(self) -> float:
        """Get uptime in seconds"""
        return time.time() - self.start_time
    
    def get_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive statistics report
        
        Returns:
            Dictionary with all statistics and calculated metrics
        """
        return {
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': self.get_hit_rate(),
            'miss_rate': self.get_miss_rate(),
            'evictions': self.evictions,
            'invalidations': self.invalidations,
            'total_operations': self.total_operations,
            'uptime_seconds': self.get_uptime()
        }
    
    def reset(self) -> None:
        """Reset all statistics"""
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.invalidations = 0
        self.total_operations = 0
        self.start_time = time.time()
