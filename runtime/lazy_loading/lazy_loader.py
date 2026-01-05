"""
Lazy Loader

Provides lazy loading functionality for efficient data loading including
initialization, data fetch, and error handling.
"""

import time
from typing import Any, Optional, Dict, Callable
from dataclasses import dataclass, field
from threading import Lock


@dataclass
class LazyLoadConfig:
    """Lazy loading configuration settings"""
    cache_loaded: bool = True  # Cache loaded data
    retry_on_error: bool = True  # Retry on load errors
    max_retries: int = 3  # Maximum retry attempts
    retry_delay: float = 1.0  # Delay between retries in seconds
    load_timeout: int = 30  # Load timeout in seconds
    
    def validate(self) -> bool:
        """Validate lazy load configuration"""
        return (
            self.max_retries >= 0 and
            self.retry_delay >= 0 and
            self.load_timeout > 0
        )


@dataclass
class LazyLoadable:
    """
    Lazy loadable data container
    
    Represents data that can be loaded on demand with lazy loading semantics.
    """
    key: str
    loader: Callable[[], Any]  # Function to load data
    loaded: bool = False
    data: Any = None
    last_loaded: Optional[float] = None
    load_count: int = 0
    error_count: int = 0
    organisation_id: Optional[str] = None  # Tenant isolation
    
    def mark_loaded(self, data: Any) -> None:
        """Mark data as loaded"""
        self.loaded = True
        self.data = data
        self.last_loaded = time.time()
        self.load_count += 1
    
    def mark_error(self) -> None:
        """Mark load error"""
        self.error_count += 1
    
    def reset(self) -> None:
        """Reset loadable state"""
        self.loaded = False
        self.data = None
        self.last_loaded = None


class LazyLoader:
    """
    Lazy Loader
    
    Provides comprehensive lazy loading functionality including:
    - Lazy initialization of data structures
    - On-demand data fetching
    - Error handling with retry logic
    - Load caching
    - Performance tracking
    """
    
    def __init__(self, config: Optional[LazyLoadConfig] = None):
        """
        Initialize lazy loader
        
        Args:
            config: Lazy load configuration (uses defaults if not provided)
        """
        self.config = config or LazyLoadConfig()
        if not self.config.validate():
            raise ValueError("Invalid lazy load configuration")
        
        self._loadables: Dict[str, LazyLoadable] = {}
        self._lock = Lock()
        self._ready = False
        self._stats = {
            'loads': 0,
            'cache_hits': 0,
            'errors': 0,
            'retries': 0
        }
        self._initialize()
    
    def _initialize(self) -> None:
        """Initialize lazy loader"""
        self._loadables.clear()
        self._ready = True
    
    def is_ready(self) -> bool:
        """Check if loader is ready"""
        return self._ready
    
    def get_config(self) -> LazyLoadConfig:
        """Get current configuration"""
        return self.config
    
    def register(
        self, 
        key: str, 
        loader: Callable[[], Any], 
        organisation_id: Optional[str] = None
    ) -> None:
        """
        Register a lazy loadable
        
        Args:
            key: Unique identifier for the loadable
            loader: Function to call to load data
            organisation_id: Tenant identifier for isolation
        """
        with self._lock:
            if key in self._loadables:
                raise ValueError(f"Loadable already registered: {key}")
            
            loadable = LazyLoadable(
                key=key,
                loader=loader,
                organisation_id=organisation_id
            )
            self._loadables[key] = loadable
    
    def load(self, key: str, force_reload: bool = False) -> Any:
        """
        Load data for a lazy loadable
        
        Implements:
        - Cache checking (if not force_reload)
        - Data loading via loader function
        - Error handling with retry logic
        - Performance tracking
        
        Args:
            key: Loadable identifier
            force_reload: Force reload even if cached
        
        Returns:
            Loaded data
        
        Raises:
            KeyError: If key not registered
            RuntimeError: If load fails after retries
        """
        with self._lock:
            if key not in self._loadables:
                raise KeyError(f"Loadable not registered: {key}")
            
            loadable = self._loadables[key]
            
            # Check if already loaded and caching enabled
            if not force_reload and loadable.loaded and self.config.cache_loaded:
                self._stats['cache_hits'] += 1
                return loadable.data
        
        # Load data (outside lock to allow concurrent loads of different keys)
        data = self._load_with_retry(loadable)
        
        with self._lock:
            loadable.mark_loaded(data)
            self._stats['loads'] += 1
        
        return data
    
    def _load_with_retry(self, loadable: LazyLoadable) -> Any:
        """
        Load data with retry logic
        
        Args:
            loadable: Loadable to load
        
        Returns:
            Loaded data
        
        Raises:
            RuntimeError: If all retries fail
        """
        last_error = None
        max_attempts = self.config.max_retries + 1 if self.config.retry_on_error else 1
        
        for attempt in range(max_attempts):
            try:
                # Call loader function with timeout
                start_time = time.time()
                data = loadable.loader()
                
                # Check timeout
                if time.time() - start_time > self.config.load_timeout:
                    raise TimeoutError(f"Load timeout exceeded: {self.config.load_timeout}s")
                
                return data
            
            except Exception as e:
                last_error = e
                loadable.mark_error()
                self._stats['errors'] += 1
                
                # If not last attempt and retry enabled, wait and retry
                if attempt < max_attempts - 1 and self.config.retry_on_error:
                    self._stats['retries'] += 1
                    time.sleep(self.config.retry_delay * (attempt + 1))  # Exponential backoff
                    continue
                
                # All retries failed
                break
        
        raise RuntimeError(f"Failed to load data for {loadable.key} after {max_attempts} attempts: {last_error}")
    
    def is_loaded(self, key: str) -> bool:
        """
        Check if data is loaded
        
        Args:
            key: Loadable identifier
        
        Returns:
            True if loaded, False otherwise
        """
        with self._lock:
            if key not in self._loadables:
                return False
            return self._loadables[key].loaded
    
    def get_if_loaded(self, key: str) -> Optional[Any]:
        """
        Get data if already loaded (without triggering load)
        
        Args:
            key: Loadable identifier
        
        Returns:
            Data if loaded, None otherwise
        """
        with self._lock:
            if key not in self._loadables:
                return None
            
            loadable = self._loadables[key]
            if loadable.loaded:
                return loadable.data
            return None
    
    def unload(self, key: str) -> bool:
        """
        Unload data (reset loadable)
        
        Args:
            key: Loadable identifier
        
        Returns:
            True if unloaded, False if not found
        """
        with self._lock:
            if key not in self._loadables:
                return False
            
            loadable = self._loadables[key]
            loadable.reset()
            return True
    
    def unregister(self, key: str) -> bool:
        """
        Unregister a loadable
        
        Args:
            key: Loadable identifier
        
        Returns:
            True if unregistered, False if not found
        """
        with self._lock:
            if key not in self._loadables:
                return False
            
            del self._loadables[key]
            return True
    
    def get_loadable_info(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a loadable
        
        Args:
            key: Loadable identifier
        
        Returns:
            Dictionary with loadable info
        """
        with self._lock:
            if key not in self._loadables:
                return None
            
            loadable = self._loadables[key]
            return {
                'key': loadable.key,
                'loaded': loadable.loaded,
                'last_loaded': loadable.last_loaded,
                'load_count': loadable.load_count,
                'error_count': loadable.error_count,
                'organisation_id': loadable.organisation_id
            }
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get loader statistics
        
        Returns:
        - Load count
        - Cache hit count
        - Error count
        - Retry count
        - Registered loadables count
        """
        with self._lock:
            return {
                'loads': self._stats['loads'],
                'cache_hits': self._stats['cache_hits'],
                'errors': self._stats['errors'],
                'retries': self._stats['retries'],
                'registered': len(self._loadables),
                'loaded': sum(1 for l in self._loadables.values() if l.loaded),
                'cache_hit_rate': (
                    self._stats['cache_hits'] / (self._stats['loads'] + self._stats['cache_hits'])
                    if (self._stats['loads'] + self._stats['cache_hits']) > 0
                    else 0.0
                )
            }
    
    def clear_cache(self) -> int:
        """
        Clear all loaded data (unload all)
        
        Returns:
            Number of loadables cleared
        """
        with self._lock:
            count = 0
            for loadable in self._loadables.values():
                if loadable.loaded:
                    loadable.reset()
                    count += 1
            return count
