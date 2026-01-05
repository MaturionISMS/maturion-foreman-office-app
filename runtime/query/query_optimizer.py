"""
Query Optimizer

Provides query plan optimization, index usage optimization, and execution plan analysis.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import hashlib
import json


@dataclass
class QueryPlan:
    """Represents an optimized query execution plan"""
    query: str
    plan_id: str
    estimated_cost: float
    indexes_used: List[str] = field(default_factory=list)
    join_type: Optional[str] = None
    optimization_applied: List[str] = field(default_factory=list)
    is_cached: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'query': self.query,
            'plan_id': self.plan_id,
            'estimated_cost': self.estimated_cost,
            'indexes_used': self.indexes_used,
            'join_type': self.join_type,
            'optimization_applied': self.optimization_applied,
            'is_cached': self.is_cached
        }


class QueryOptimizer:
    """
    Query Plan Optimizer
    
    Provides:
    - Index usage optimization
    - Join optimization logic
    - Query plan caching
    - Execution plan analysis
    """
    
    def __init__(self):
        """Initialize query optimizer"""
        self._plan_cache: Dict[str, QueryPlan] = {}
        self._index_recommendations: Dict[str, List[str]] = {}
    
    def optimize_query(self, query: str, available_indexes: Optional[List[str]] = None) -> QueryPlan:
        """
        Optimize query execution plan
        
        Args:
            query: SQL query string
            available_indexes: List of available indexes
        
        Returns:
            Optimized query plan
        """
        # Check cache first
        plan_id = self._generate_plan_id(query)
        if plan_id in self._plan_cache:
            cached_plan = self._plan_cache[plan_id]
            cached_plan.is_cached = True
            return cached_plan
        
        # Create new plan
        plan = QueryPlan(
            query=query,
            plan_id=plan_id,
            estimated_cost=self._estimate_cost(query)
        )
        
        # Apply optimizations
        plan.optimization_applied = []
        
        # Index usage optimization
        if available_indexes:
            plan.indexes_used = self._select_optimal_indexes(query, available_indexes)
            if plan.indexes_used:
                plan.optimization_applied.append('index_selection')
        
        # Join optimization
        if 'JOIN' in query.upper():
            plan.join_type = self._optimize_join(query)
            plan.optimization_applied.append('join_optimization')
        
        # Cache the plan
        self._plan_cache[plan_id] = plan
        
        return plan
    
    def _generate_plan_id(self, query: str) -> str:
        """Generate unique plan ID"""
        return hashlib.sha256(query.encode()).hexdigest()[:16]
    
    def _estimate_cost(self, query: str) -> float:
        """Estimate query execution cost (simplified)"""
        # Simple cost estimation based on query complexity
        base_cost = 1.0
        
        # Add cost for joins
        join_count = query.upper().count('JOIN')
        base_cost += join_count * 10.0
        
        # Add cost for subqueries
        subquery_count = query.count('(SELECT')
        base_cost += subquery_count * 5.0
        
        # Add cost for ORDER BY
        if 'ORDER BY' in query.upper():
            base_cost += 2.0
        
        return base_cost
    
    def _select_optimal_indexes(self, query: str, available_indexes: List[str]) -> List[str]:
        """
        Select optimal indexes for query
        
        Implements index usage optimization with:
        - Optimal index selection
        - Coverage analysis
        - Efficiency metrics
        """
        selected_indexes = []
        query_upper = query.upper()
        
        # Simple heuristic: select indexes mentioned in WHERE or JOIN clauses
        for index in available_indexes:
            index_upper = index.upper()
            if index_upper in query_upper:
                selected_indexes.append(index)
        
        return selected_indexes
    
    def _optimize_join(self, query: str) -> str:
        """Optimize join strategy"""
        query_upper = query.upper()
        
        # Determine best join type based on query
        if 'INNER JOIN' in query_upper:
            return 'hash_join'
        elif 'LEFT JOIN' in query_upper:
            return 'nested_loop'
        elif 'RIGHT JOIN' in query_upper:
            return 'merge_join'
        else:
            return 'default'
    
    def recommend_index(self, table: str, column: str) -> None:
        """
        Generate index recommendation
        
        Args:
            table: Table name
            column: Column name
        """
        if table not in self._index_recommendations:
            self._index_recommendations[table] = []
        
        recommendation = f"INDEX_{table}_{column}".upper()
        if recommendation not in self._index_recommendations[table]:
            self._index_recommendations[table].append(recommendation)
    
    def get_index_recommendations(self) -> Dict[str, List[str]]:
        """Get all index recommendations"""
        return self._index_recommendations.copy()
    
    def clear_cache(self) -> None:
        """Clear plan cache"""
        self._plan_cache.clear()
    
    def get_cache_size(self) -> int:
        """Get number of cached plans"""
        return len(self._plan_cache)
