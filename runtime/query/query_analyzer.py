"""
Query Analyzer and Profiler

Provides query analysis, profiling, slow query detection, and pattern analysis.
"""

import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class QueryProfile:
    """Query execution profile"""
    query: str
    execution_time: float
    timestamp: float = field(default_factory=time.time)
    row_count: int = 0
    is_slow: bool = False
    pattern: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'query': self.query,
            'execution_time': self.execution_time,
            'timestamp': self.timestamp,
            'row_count': self.row_count,
            'is_slow': self.is_slow,
            'pattern': self.pattern
        }


class QueryAnalyzer:
    """
    Query Analyzer and Profiler
    
    Provides:
    - Slow query detection
    - Query logging mechanism
    - Performance alerting
    - Query pattern analysis
    """
    
    def __init__(self, slow_query_threshold: float = 1.0):
        """
        Initialize query analyzer
        
        Args:
            slow_query_threshold: Threshold in seconds for slow query detection
        """
        self.slow_query_threshold = slow_query_threshold
        self._query_log: List[QueryProfile] = []
        self._slow_queries: List[QueryProfile] = []
        self._patterns: Dict[str, int] = {}
        self._alerts: List[Dict[str, Any]] = []
    
    def analyze_query(self, query: str, execution_time: float, row_count: int = 0) -> QueryProfile:
        """
        Analyze a query execution
        
        Args:
            query: SQL query string
            execution_time: Query execution time in seconds
            row_count: Number of rows returned
        
        Returns:
            QueryProfile with analysis results
        """
        # Detect if query is slow
        is_slow = execution_time > self.slow_query_threshold
        
        # Extract query pattern (simplified - just get first word/command)
        pattern = self._extract_pattern(query)
        
        # Create profile
        profile = QueryProfile(
            query=query,
            execution_time=execution_time,
            row_count=row_count,
            is_slow=is_slow,
            pattern=pattern
        )
        
        # Log query
        self._query_log.append(profile)
        
        # Track slow queries
        if is_slow:
            self._slow_queries.append(profile)
            self._create_alert(profile)
        
        # Track patterns
        if pattern:
            self._patterns[pattern] = self._patterns.get(pattern, 0) + 1
        
        return profile
    
    def _extract_pattern(self, query: str) -> str:
        """Extract query pattern (command type)"""
        query_upper = query.strip().upper()
        if query_upper.startswith('SELECT'):
            return 'SELECT'
        elif query_upper.startswith('INSERT'):
            return 'INSERT'
        elif query_upper.startswith('UPDATE'):
            return 'UPDATE'
        elif query_upper.startswith('DELETE'):
            return 'DELETE'
        else:
            return 'OTHER'
    
    def _create_alert(self, profile: QueryProfile) -> None:
        """Create performance alert for slow query"""
        alert = {
            'type': 'slow_query',
            'timestamp': profile.timestamp,
            'query': profile.query,
            'execution_time': profile.execution_time,
            'threshold': self.slow_query_threshold
        }
        self._alerts.append(alert)
    
    def get_slow_queries(self) -> List[QueryProfile]:
        """Get all detected slow queries"""
        return self._slow_queries.copy()
    
    def get_query_patterns(self) -> Dict[str, int]:
        """Get query pattern statistics"""
        return self._patterns.copy()
    
    def get_alerts(self) -> List[Dict[str, Any]]:
        """Get performance alerts"""
        return self._alerts.copy()
    
    def get_log(self) -> List[QueryProfile]:
        """Get full query log"""
        return self._query_log.copy()
    
    def clear_log(self) -> None:
        """Clear query log and alerts"""
        self._query_log.clear()
        self._slow_queries.clear()
        self._alerts.clear()
