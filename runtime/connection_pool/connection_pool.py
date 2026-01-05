"""
Connection Pool Manager

Provides connection pooling functionality including initialization,
connection acquisition and return, and pool management.
"""

import time
import uuid
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime
from threading import Lock


@dataclass
class ConnectionPoolConfig:
    """Connection pool configuration settings"""
    min_size: int = 5  # Minimum number of connections in pool
    max_size: int = 20  # Maximum number of connections in pool
    connection_timeout: int = 30  # Connection timeout in seconds
    idle_timeout: int = 300  # Idle connection timeout in seconds (5 minutes)
    max_lifetime: int = 3600  # Maximum connection lifetime in seconds (1 hour)
    
    def validate(self) -> bool:
        """Validate pool configuration"""
        return (
            self.min_size > 0 and
            self.max_size >= self.min_size and
            self.connection_timeout > 0 and
            self.idle_timeout > 0 and
            self.max_lifetime > 0
        )


@dataclass
class Connection:
    """Represents a single connection in the pool"""
    connection_id: str
    created_at: float
    last_used: float = field(default_factory=time.time)
    in_use: bool = False
    use_count: int = 0
    organisation_id: Optional[str] = None  # Tenant isolation
    
    def is_expired(self, max_lifetime: int) -> bool:
        """Check if connection has exceeded maximum lifetime"""
        return time.time() > (self.created_at + max_lifetime)
    
    def is_idle_expired(self, idle_timeout: int) -> bool:
        """Check if connection has been idle too long"""
        if self.in_use:
            return False
        return time.time() > (self.last_used + idle_timeout)
    
    def acquire(self, organisation_id: Optional[str] = None) -> None:
        """Mark connection as in use"""
        self.in_use = True
        self.last_used = time.time()
        self.use_count += 1
        self.organisation_id = organisation_id
    
    def release(self) -> None:
        """Mark connection as available"""
        self.in_use = False
        self.last_used = time.time()
        self.organisation_id = None


class ConnectionPool:
    """
    Connection Pool Manager
    
    Provides comprehensive connection pooling functionality including:
    - Pool initialization with min/max size configuration
    - Connection acquisition with timeout handling
    - Connection return and cleanup
    - Connection lifecycle management
    - Health monitoring integration
    - Statistics tracking
    """
    
    def __init__(self, config: Optional[ConnectionPoolConfig] = None):
        """
        Initialize connection pool
        
        Args:
            config: Pool configuration (uses defaults if not provided)
        """
        self.config = config or ConnectionPoolConfig()
        if not self.config.validate():
            raise ValueError("Invalid connection pool configuration")
        
        self._connections: Dict[str, Connection] = {}
        self._lock = Lock()
        self._ready = False
        self._stats = {
            'acquisitions': 0,
            'releases': 0,
            'creations': 0,
            'destructions': 0,
            'timeouts': 0,
            'errors': 0
        }
        self._initialize()
    
    def _initialize(self) -> None:
        """Initialize connection pool with minimum connections"""
        with self._lock:
            # Create minimum number of connections
            for _ in range(self.config.min_size):
                connection = self._create_connection()
                self._connections[connection.connection_id] = connection
                self._stats['creations'] += 1
            
            self._ready = True
    
    def _create_connection(self) -> Connection:
        """Create a new connection"""
        connection_id = str(uuid.uuid4())
        return Connection(
            connection_id=connection_id,
            created_at=time.time()
        )
    
    def is_ready(self) -> bool:
        """Check if pool is ready for operations"""
        return self._ready
    
    def get_config(self) -> ConnectionPoolConfig:
        """Get current pool configuration"""
        return self.config
    
    def acquire(self, organisation_id: Optional[str] = None, timeout: Optional[int] = None) -> Optional[Connection]:
        """
        Acquire connection from pool
        
        Args:
            organisation_id: Tenant identifier for isolation
            timeout: Acquisition timeout in seconds (uses config default if not provided)
        
        Returns:
            Connection if available, None if timeout or pool exhausted
        """
        timeout = timeout or self.config.connection_timeout
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            with self._lock:
                # First pass: clean up expired connections
                expired_ids = []
                for conn_id, conn in self._connections.items():
                    if not conn.in_use:
                        if conn.is_expired(self.config.max_lifetime) or conn.is_idle_expired(self.config.idle_timeout):
                            expired_ids.append(conn_id)
                
                for conn_id in expired_ids:
                    self._destroy_connection(conn_id)
                
                # Second pass: find available connection
                for conn in self._connections.values():
                    if not conn.in_use:
                        # Acquire connection
                        conn.acquire(organisation_id)
                        self._stats['acquisitions'] += 1
                        return conn
                
                # No available connections, try to create new one if under max size
                if len(self._connections) < self.config.max_size:
                    new_conn = self._create_connection()
                    self._connections[new_conn.connection_id] = new_conn
                    self._stats['creations'] += 1
                    new_conn.acquire(organisation_id)
                    self._stats['acquisitions'] += 1
                    return new_conn
            
            # Wait a bit before retrying
            time.sleep(0.1)
        
        # Timeout
        self._stats['timeouts'] += 1
        return None
    
    def release(self, connection: Connection) -> bool:
        """
        Return connection to pool
        
        Args:
            connection: Connection to return
        
        Returns:
            True if successful, False if connection not found
        """
        with self._lock:
            if connection.connection_id not in self._connections:
                return False
            
            conn = self._connections[connection.connection_id]
            
            # Check if connection should be destroyed (expired or excess)
            if conn.is_expired(self.config.max_lifetime):
                self._destroy_connection(conn.connection_id)
                return True
            
            # If we have more than min connections and this one is old, destroy it
            if len(self._connections) > self.config.min_size:
                if conn.is_idle_expired(self.config.idle_timeout):
                    self._destroy_connection(conn.connection_id)
                    return True
            
            # Release connection back to pool
            conn.release()
            self._stats['releases'] += 1
            return True
    
    def _destroy_connection(self, connection_id: str) -> None:
        """Destroy a connection (internal method)"""
        if connection_id in self._connections:
            del self._connections[connection_id]
            self._stats['destructions'] += 1
    
    def get_pool_size(self) -> int:
        """Get current pool size"""
        with self._lock:
            return len(self._connections)
    
    def get_available_count(self) -> int:
        """Get number of available connections"""
        with self._lock:
            return sum(1 for conn in self._connections.values() if not conn.in_use)
    
    def get_in_use_count(self) -> int:
        """Get number of connections in use"""
        with self._lock:
            return sum(1 for conn in self._connections.values() if conn.in_use)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get pool statistics
        
        Returns:
        - Acquisition count
        - Release count
        - Creation count
        - Destruction count
        - Timeout count
        - Error count
        - Current pool metrics
        """
        with self._lock:
            # Calculate counts directly instead of calling methods (to avoid deadlock)
            available = sum(1 for conn in self._connections.values() if not conn.in_use)
            in_use = sum(1 for conn in self._connections.values() if conn.in_use)
            current_size = len(self._connections)
            
            stats = {
                'acquisitions': self._stats['acquisitions'],
                'releases': self._stats['releases'],
                'creations': self._stats['creations'],
                'destructions': self._stats['destructions'],
                'timeouts': self._stats['timeouts'],
                'errors': self._stats['errors'],
                'current_size': current_size,
                'available': available,
                'in_use': in_use,
                'min_size': self.config.min_size,
                'max_size': self.config.max_size,
                'utilization': in_use / current_size if current_size > 0 else 0.0
            }
            return stats
    
    def cleanup_expired(self) -> int:
        """
        Clean up expired connections
        
        Returns:
            Number of connections cleaned up
        """
        with self._lock:
            expired_ids = [
                conn_id for conn_id, conn in self._connections.items()
                if not conn.in_use and (
                    conn.is_expired(self.config.max_lifetime) or
                    conn.is_idle_expired(self.config.idle_timeout)
                )
            ]
            
            # Don't destroy if it would bring us below min_size
            safe_to_destroy = max(0, len(self._connections) - len(expired_ids) - self.config.min_size)
            expired_ids = expired_ids[:safe_to_destroy]
            
            for conn_id in expired_ids:
                self._destroy_connection(conn_id)
            
            return len(expired_ids)
    
    def shutdown(self) -> None:
        """Shutdown pool and destroy all connections"""
        with self._lock:
            for conn_id in list(self._connections.keys()):
                self._destroy_connection(conn_id)
            self._ready = False
