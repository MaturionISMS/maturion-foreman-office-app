"""
QA-426 to QA-435: System Optimizations Phase 1 Tests

Architectural Reference: Wave 2 System Optimizations Phase 1 Specification
QA Range: QA-426 to QA-435
Component: System Optimizations - Caching and Query Optimization

State: GREEN (Implemented by api-builder in Subwave 2.3)
Build-to-Green Status: COMPLETE
"""

import pytest
from typing import Dict, Any
import time

# Import cache module
from runtime.cache import CacheManager, CacheConfig, CacheStatistics

# Import query module
from runtime.query import (
    QueryAnalyzer,
    QueryProfile,
    QueryOptimizer,
    QueryPlan,
    QueryMonitor,
    QueryMetrics
)


class TestCachingImplementation:
    """Tests for Caching Implementation (QA-426 to QA-430)"""
    
    def test_qa_426_cache_layer_initialization(self):
        """
        QA-426: Cache layer initialization
        
        Verify:
        - Cache creation succeeds
        - Configuration loaded correctly
        - Readiness confirmation provided
        - Cache service available
        
        Status: GREEN - Implemented
        """
        # Create cache with default configuration
        cache = CacheManager()
        
        # Verify cache creation succeeded
        assert cache is not None
        
        # Verify configuration loaded correctly
        config = cache.get_config()
        assert config is not None
        assert config.default_ttl > 0
        assert config.max_size > 0
        
        # Verify readiness confirmation
        assert cache.is_ready() is True
        
        # Verify cache service available
        test_key = cache.generate_key("test")
        assert cache.set(test_key, "test_value") is True
    
    def test_qa_427_cache_key_generation(self):
        """
        QA-427: Cache key generation
        
        Verify:
        - Key uniqueness for different inputs
        - Collision handling mechanism
        - Consistency across requests
        - Key format standardization
        
        Status: GREEN - Implemented
        """
        cache = CacheManager()
        
        # Verify key uniqueness for different inputs
        key1 = cache.generate_key("input1")
        key2 = cache.generate_key("input2")
        assert key1 != key2
        
        # Verify collision handling mechanism (SHA-256 hash)
        assert len(key1) > 0
        assert "cache:" in key1
        
        # Verify consistency across requests
        key1_repeat = cache.generate_key("input1")
        assert key1 == key1_repeat
        
        # Verify key format standardization
        assert key1.startswith("cache:")
        
        # Verify with kwargs
        key3 = cache.generate_key(user="john", action="login")
        key4 = cache.generate_key(user="jane", action="login")
        assert key3 != key4
    
    def test_qa_428_cache_hit_miss_handling(self):
        """
        QA-428: Cache hit/miss handling
        
        Verify:
        - Cache hit returns cached data
        - Cache miss fetches fresh data
        - Metrics tracking for hits/misses
        - Proper data freshness handling
        
        Status: GREEN - Implemented
        """
        cache = CacheManager()
        
        # Test cache miss
        key = cache.generate_key("test_data")
        result = cache.get(key)
        assert result is None  # Cache miss
        
        # Set value
        test_value = {"data": "test"}
        cache.set(key, test_value)
        
        # Test cache hit
        result = cache.get(key)
        assert result is not None
        assert result == test_value
        
        # Verify metrics tracking
        stats = cache.get_statistics()
        assert stats['hits'] > 0
        assert stats['misses'] > 0
        
        # Test TTL expiration (data freshness)
        short_ttl_key = cache.generate_key("short_ttl")
        cache.set(short_ttl_key, "expires_soon", ttl=1)
        assert cache.get(short_ttl_key) == "expires_soon"
        
        time.sleep(1.1)  # Wait for TTL to expire
        assert cache.get(short_ttl_key) is None  # Should be expired
    
    def test_qa_429_cache_invalidation_logic(self):
        """
        QA-429: Cache invalidation logic
        
        Verify:
        - TTL expiration handling
        - Manual invalidation support
        - Cascade invalidation for dependencies
        - Invalidation event logging
        
        Status: GREEN - Implemented
        """
        cache = CacheManager()
        
        # Test manual invalidation
        key = cache.generate_key("manual_test")
        cache.set(key, "test_value")
        assert cache.get(key) == "test_value"
        
        result = cache.invalidate(key)
        assert result is True
        assert cache.get(key) is None
        
        # Test cascade invalidation (pattern-based)
        cache.set("cache:user:123:profile", "profile_data")
        cache.set("cache:user:123:settings", "settings_data")
        cache.set("cache:user:456:profile", "other_profile")
        
        # Invalidate all user 123 cache entries
        invalidated = cache.invalidate_pattern("user:123")
        assert invalidated == 2
        assert cache.get("cache:user:123:profile") is None
        assert cache.get("cache:user:123:settings") is None
        assert cache.get("cache:user:456:profile") == "other_profile"
        
        # Verify invalidation event logging in statistics
        stats = cache.get_statistics()
        assert stats['invalidations'] > 0
    
    def test_qa_430_cache_statistics_tracking(self):
        """
        QA-430: Cache statistics tracking
        
        Verify:
        - Hit rate calculation
        - Miss rate calculation
        - Eviction metrics collection
        - Performance statistics reporting
        
        Status: GREEN - Implemented
        """
        cache = CacheManager(CacheConfig(max_size=5))
        
        # Generate some cache activity
        keys = []
        for i in range(3):
            key = cache.generate_key(f"item_{i}")
            keys.append(key)
            cache.set(key, f"value_{i}")
        
        # Create hits and misses
        cache.get(keys[0])  # Hit
        cache.get(keys[1])  # Hit
        cache.get(cache.generate_key("nonexistent"))  # Miss
        
        # Get statistics
        stats = cache.get_statistics()
        
        # Verify hit rate calculation
        assert 'hit_rate' in stats
        assert stats['hit_rate'] > 0
        assert 0 <= stats['hit_rate'] <= 1
        
        # Verify miss rate calculation
        assert 'miss_rate' in stats
        assert stats['miss_rate'] > 0
        assert 0 <= stats['miss_rate'] <= 1
        
        # Verify hit_rate + miss_rate = 1.0
        assert abs((stats['hit_rate'] + stats['miss_rate']) - 1.0) < 0.01
        
        # Test eviction metrics by filling cache beyond max_size
        for i in range(3, 8):  # Add 5 more items to force evictions
            key = cache.generate_key(f"item_{i}")
            cache.set(key, f"value_{i}")
        
        stats = cache.get_statistics()
        
        # Verify eviction metrics collection
        assert 'evictions' in stats
        assert stats['evictions'] > 0
        
        # Verify performance statistics reporting
        assert 'total_operations' in stats
        assert 'current_size' in stats
        assert 'utilization' in stats
        assert stats['current_size'] <= stats['max_size']


class TestQueryOptimization:
    """Tests for Query Optimization (QA-431 to QA-435)"""
    
    def test_qa_431_query_analysis_and_profiling(self):
        """
        QA-431: Query analysis and profiling
        
        Verify:
        - Slow query detection
        - Query logging mechanism
        - Performance alerting
        - Query pattern analysis
        
        Status: GREEN - Implemented
        """
        analyzer = QueryAnalyzer(slow_query_threshold=0.5)
        
        # Test slow query detection
        slow_query = "SELECT * FROM large_table WHERE complex_condition"
        profile = analyzer.analyze_query(slow_query, execution_time=1.5)
        
        assert profile.is_slow is True
        assert profile.execution_time == 1.5
        
        # Test fast query
        fast_query = "SELECT id FROM users WHERE id = 1"
        profile2 = analyzer.analyze_query(fast_query, execution_time=0.1)
        assert profile2.is_slow is False
        
        # Verify query logging mechanism
        log = analyzer.get_log()
        assert len(log) == 2
        assert log[0].query == slow_query
        
        # Verify performance alerting
        alerts = analyzer.get_alerts()
        assert len(alerts) > 0
        assert alerts[0]['type'] == 'slow_query'
        
        # Verify query pattern analysis
        analyzer.analyze_query("SELECT * FROM table1", 0.2)
        analyzer.analyze_query("INSERT INTO table1 VALUES (1)", 0.1)
        analyzer.analyze_query("UPDATE table1 SET x=1", 0.3)
        
        patterns = analyzer.get_query_patterns()
        assert 'SELECT' in patterns
        assert 'INSERT' in patterns
        assert 'UPDATE' in patterns
        assert patterns['SELECT'] >= 2
    
    def test_qa_432_query_plan_optimization(self):
        """
        QA-432: Query plan optimization
        
        Verify:
        - Index usage optimization
        - Join optimization logic
        - Query plan caching
        - Execution plan analysis
        
        Status: GREEN - Implemented
        """
        optimizer = QueryOptimizer()
        
        # Test basic optimization
        query = "SELECT * FROM users WHERE email = 'test@example.com'"
        available_indexes = ['EMAIL', 'USER_ID', 'CREATED_AT']
        
        plan = optimizer.optimize_query(query, available_indexes)
        
        # Verify plan created
        assert plan is not None
        assert plan.query == query
        assert plan.plan_id is not None
        
        # Verify index usage optimization
        assert 'EMAIL' in plan.indexes_used
        assert 'index_selection' in plan.optimization_applied
        
        # Test join optimization logic
        join_query = "SELECT * FROM users INNER JOIN orders ON users.id = orders.user_id"
        join_plan = optimizer.optimize_query(join_query)
        
        assert join_plan.join_type is not None
        assert 'join_optimization' in join_plan.optimization_applied
        
        # Verify query plan caching
        cached_plan = optimizer.optimize_query(query, available_indexes)
        assert cached_plan.is_cached is True
        assert cached_plan.plan_id == plan.plan_id
        
        # Verify cache size
        assert optimizer.get_cache_size() >= 2
        
        # Verify execution plan analysis (cost estimation)
        assert plan.estimated_cost > 0
    
    def test_qa_433_index_usage_optimization(self):
        """
        QA-433: Index usage optimization
        
        Verify:
        - Optimal index selection
        - Coverage analysis
        - Efficiency metrics
        - Index recommendation logic
        
        Status: GREEN - Implemented
        """
        optimizer = QueryOptimizer()
        
        # Test optimal index selection
        query = "SELECT * FROM users WHERE email = 'test@example.com' AND status = 'active'"
        available_indexes = ['EMAIL', 'STATUS', 'CREATED_AT', 'USER_ID']
        
        plan = optimizer.optimize_query(query, available_indexes)
        
        # Verify optimal index selection
        assert len(plan.indexes_used) > 0
        assert 'EMAIL' in plan.indexes_used or 'STATUS' in plan.indexes_used
        
        # Test coverage analysis
        # Indexes mentioned in query should be selected
        query2 = "SELECT * FROM orders WHERE USER_ID = 123"
        plan2 = optimizer.optimize_query(query2, available_indexes)
        assert 'USER_ID' in plan2.indexes_used
        
        # Test efficiency metrics (cost estimation)
        simple_query = "SELECT id FROM users WHERE id = 1"
        complex_query = "SELECT * FROM users JOIN orders ON users.id = orders.user_id WHERE users.email LIKE '%@example.com'"
        
        simple_plan = optimizer.optimize_query(simple_query)
        complex_plan = optimizer.optimize_query(complex_query)
        
        assert complex_plan.estimated_cost > simple_plan.estimated_cost
        
        # Test index recommendation logic
        optimizer.recommend_index('users', 'email')
        optimizer.recommend_index('users', 'status')
        optimizer.recommend_index('orders', 'user_id')
        
        recommendations = optimizer.get_index_recommendations()
        assert 'users' in recommendations
        assert 'orders' in recommendations
        assert len(recommendations['users']) >= 2
    
    def test_qa_434_query_result_caching(self):
        """
        QA-434: Query result caching
        
        Verify:
        - Cache integration with queries
        - Invalidation on data change
        - Data consistency maintained
        - Cache key generation for queries
        
        Status: GREEN - Implemented
        """
        # Integration test: using both cache and query optimizer
        cache = CacheManager()
        optimizer = QueryOptimizer()
        
        # Test cache integration with queries
        query = "SELECT * FROM users WHERE id = 123"
        
        # Generate cache key for query
        cache_key = cache.generate_key(query)
        
        # Simulate query execution and caching result
        query_result = {"id": 123, "name": "John Doe", "email": "john@example.com"}
        cache.set(cache_key, query_result)
        
        # Verify cached result retrieval
        cached_result = cache.get(cache_key)
        assert cached_result == query_result
        
        # Test invalidation on data change
        # Simulate data change by invalidating cache
        cache.invalidate(cache_key)
        assert cache.get(cache_key) is None
        
        # Test data consistency with pattern-based invalidation
        # Use custom keys with patterns for testing
        user_key_1 = "cache:query:users:1"
        user_key_2 = "cache:query:users:2"
        order_key = "cache:query:orders:1"
        
        cache.set(user_key_1, {"id": 1})
        cache.set(user_key_2, {"id": 2})
        cache.set(order_key, {"order_id": 1})
        
        # Invalidate all user queries using pattern
        invalidated = cache.invalidate_pattern("users")
        assert invalidated == 2
        
        # Verify user caches are gone
        assert cache.get(user_key_1) is None
        assert cache.get(user_key_2) is None
        
        # Verify orders cache still exists
        assert cache.get(order_key) == {"order_id": 1}
        
        # Test cache key generation consistency for queries
        key1 = cache.generate_key(query)
        key2 = cache.generate_key(query)
        assert key1 == key2
    
    def test_qa_435_query_performance_monitoring(self):
        """
        QA-435: Query performance monitoring
        
        Verify:
        - Execution time tracking
        - Query count metrics
        - Alert threshold monitoring
        - Performance trend analysis
        
        Status: GREEN - Implemented
        """
        monitor = QueryMonitor(alert_threshold=1.0)
        
        # Test execution time tracking
        query_id = "query_001"
        metrics = monitor.track_query(query_id, execution_time=0.5)
        
        assert metrics is not None
        assert metrics.query_id == query_id
        assert metrics.execution_time == 0.5
        
        # Test query count metrics
        monitor.track_query(query_id, execution_time=0.6)
        monitor.track_query(query_id, execution_time=0.7)
        
        updated_metrics = monitor.get_metrics(query_id)
        assert updated_metrics.query_count == 3
        
        # Test alert threshold monitoring
        slow_query_id = "slow_query"
        monitor.track_query(slow_query_id, execution_time=2.5)  # Exceeds threshold
        
        alerts = monitor.get_alerts()
        assert len(alerts) > 0
        assert alerts[0]['type'] == 'slow_query'
        assert alerts[0]['query_id'] == slow_query_id
        
        # Test performance statistics
        stats = monitor.get_statistics()
        assert 'total_queries' in stats
        assert 'average_time' in stats
        assert stats['total_queries'] >= 4
        
        # Test performance trend analysis
        # Add more queries to establish a trend
        for i in range(20):
            monitor.track_query(f"query_{i}", execution_time=0.3 + (i * 0.01))
        
        trend = monitor.get_trend_analysis(window_size=10)
        assert 'trend' in trend
        assert trend['trend'] in ['stable', 'improving', 'degrading']
        assert 'average_recent' in trend
        assert 'average_overall' in trend
