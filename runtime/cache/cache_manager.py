"""
Cache Manager

Provides core caching functionality including initialization, key generation,
cache operations, and invalidation logic.
"""

import hashlib
import json
import time
from typing import Any, Dict, Optional, List
from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class CacheConfig:
    """Cache configuration settings"""
    default_ttl: int = 3600  # Default TTL in seconds (1 hour)
    max_size: int = 1000  # Maximum number of cached items
    enable_stats: bool = True  # Enable statistics tracking
    
    def validate(self) -> bool:
        """Validate cache configuration"""
        return (
            self.default_ttl > 0 and
            self.max_size > 0 and
            isinstance(self.enable_stats, bool)
        )


@dataclass
class CacheEntry:
    """Represents a single cache entry"""
    key: str
    value: Any
    created_at: float
    ttl: int
    access_count: int = 0
    last_accessed: float = field(default_factory=time.time)
    
    def is_expired(self) -> bool:
        """Check if cache entry has expired"""
        return time.time() > (self.created_at + self.ttl)
    
    def touch(self) -> None:
        """Update last accessed time and increment access count"""
        self.last_accessed = time.time()
        self.access_count += 1


class CacheManager:
    """
    Cache Manager
    
    Provides comprehensive caching functionality including:
    - Cache initialization and configuration
    - Cache key generation with collision handling
    - Cache hit/miss handling
    - TTL-based and manual cache invalidation
    - Cache statistics tracking
    """
    
    def __init__(self, config: Optional[CacheConfig] = None):
        """
        Initialize cache manager
        
        Args:
            config: Cache configuration (uses defaults if not provided)
        """
        self.config = config or CacheConfig()
        if not self.config.validate():
            raise ValueError("Invalid cache configuration")
        
        self._cache: Dict[str, CacheEntry] = {}
        self._ready = False
        self._stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'invalidations': 0,
            'total_operations': 0
        }
        self._initialize()
    
    def _initialize(self) -> None:
        """Initialize cache layer"""
        self._cache.clear()
        self._stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'invalidations': 0,
            'total_operations': 0
        }
        self._ready = True
    
    def is_ready(self) -> bool:
        """Check if cache is ready for operations"""
        return self._ready
    
    def get_config(self) -> CacheConfig:
        """Get current cache configuration"""
        return self.config
    
    def generate_key(self, *args, **kwargs) -> str:
        """
        Generate unique cache key from inputs
        
        Provides:
        - Uniqueness for different inputs
        - Collision handling via SHA-256
        - Consistency across requests
        - Standardized key format
        
        Args:
            *args: Positional arguments to include in key
            **kwargs: Keyword arguments to include in key
        
        Returns:
            Standardized cache key string
        """
        # Create deterministic representation of inputs
        key_data = {
            'args': args,
            'kwargs': sorted(kwargs.items())
        }
        
        # Serialize to JSON for consistent ordering
        key_string = json.dumps(key_data, sort_keys=True, default=str)
        
        # Hash for collision handling and consistent length
        key_hash = hashlib.sha256(key_string.encode()).hexdigest()
        
        # Format: cache:hash
        return f"cache:{key_hash}"
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache
        
        Handles:
        - Cache hit: returns cached data
        - Cache miss: returns None
        - Automatic TTL expiration
        - Metrics tracking
        
        Args:
            key: Cache key
        
        Returns:
            Cached value or None if not found/expired
        """
        self._stats['total_operations'] += 1
        
        if key not in self._cache:
            self._stats['misses'] += 1
            return None
        
        entry = self._cache[key]
        
        # Check TTL expiration
        if entry.is_expired():
            self._invalidate_key(key)
            self._stats['misses'] += 1
            return None
        
        # Cache hit
        entry.touch()
        self._stats['hits'] += 1
        return entry.value
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Set value in cache
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (uses config default if not provided)
        
        Returns:
            True if successful
        """
        # Enforce max size by evicting oldest entry
        if len(self._cache) >= self.config.max_size and key not in self._cache:
            self._evict_oldest()
        
        # Create cache entry
        entry = CacheEntry(
            key=key,
            value=value,
            created_at=time.time(),
            ttl=ttl or self.config.default_ttl
        )
        
        self._cache[key] = entry
        self._stats['total_operations'] += 1
        return True
    
    def invalidate(self, key: str) -> bool:
        """
        Manually invalidate cache entry
        
        Args:
            key: Cache key to invalidate
        
        Returns:
            True if entry was invalidated, False if not found
        """
        if key in self._cache:
            self._invalidate_key(key)
            self._stats['invalidations'] += 1
            return True
        return False
    
    def invalidate_pattern(self, pattern: str) -> int:
        """
        Invalidate all keys matching pattern
        
        Supports cascade invalidation for dependencies
        
        Args:
            pattern: Pattern to match (simple substring match)
        
        Returns:
            Number of keys invalidated
        """
        keys_to_invalidate = [
            key for key in self._cache.keys()
            if pattern in key
        ]
        
        for key in keys_to_invalidate:
            self._invalidate_key(key)
            self._stats['invalidations'] += 1
        
        return len(keys_to_invalidate)
    
    def _invalidate_key(self, key: str) -> None:
        """Internal method to remove key from cache"""
        if key in self._cache:
            del self._cache[key]
    
    def _evict_oldest(self) -> None:
        """Evict oldest cache entry based on last accessed time"""
        if not self._cache:
            return
        
        oldest_key = min(
            self._cache.keys(),
            key=lambda k: self._cache[k].last_accessed
        )
        
        self._invalidate_key(oldest_key)
        self._stats['evictions'] += 1
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get cache statistics
        
        Returns:
        - Hit rate calculation
        - Miss rate calculation
        - Eviction metrics
        - Performance statistics
        """
        total_requests = self._stats['hits'] + self._stats['misses']
        
        stats = {
            'hits': self._stats['hits'],
            'misses': self._stats['misses'],
            'hit_rate': self._stats['hits'] / total_requests if total_requests > 0 else 0.0,
            'miss_rate': self._stats['misses'] / total_requests if total_requests > 0 else 0.0,
            'evictions': self._stats['evictions'],
            'invalidations': self._stats['invalidations'],
            'total_operations': self._stats['total_operations'],
            'current_size': len(self._cache),
            'max_size': self.config.max_size,
            'utilization': len(self._cache) / self.config.max_size if self.config.max_size > 0 else 0.0
        }
        
        return stats
    
    def clear(self) -> None:
        """Clear all cache entries"""
        self._cache.clear()
