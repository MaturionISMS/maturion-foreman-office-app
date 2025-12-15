"""
Stall Detector - detects when system has stalled.

Implements stall detection based on heartbeat monitoring.
"""

import threading
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any


class StallDetector:
    """
    Detects system stalls by monitoring heartbeat activity.
    
    Responsibilities:
    - Monitor heartbeat freshness
    - Detect stalls when heartbeat stops
    - Classify stall types
    """
    
    def __init__(self, heartbeat_monitor, timeout_seconds: int = 10):
        """
        Initialize StallDetector.
        
        Args:
            heartbeat_monitor: HeartbeatMonitor instance to monitor
            timeout_seconds: Seconds without heartbeat before declaring stall
        """
        self.heartbeat_monitor = heartbeat_monitor
        self.timeout_seconds = timeout_seconds
        self._running = False
        self._thread: threading.Thread = None
        self._stalled = False
        self._stall_info: Optional[Dict[str, Any]] = None
    
    def start(self) -> None:
        """Start monitoring for stalls."""
        if self._running:
            return
        
        self._running = True
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()
    
    def stop(self) -> None:
        """Stop monitoring."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)
    
    def is_stalled(self) -> bool:
        """
        Check if system is currently stalled.
        
        Returns:
            True if stalled, False otherwise
        """
        return self._stalled
    
    def get_stall_info(self) -> Optional[Dict[str, Any]]:
        """
        Get information about the current stall.
        
        Returns:
            Stall info dict or None if not stalled
        """
        return self._stall_info
    
    def _monitor_loop(self) -> None:
        """Internal loop that monitors for stalls."""
        while self._running:
            self._check_for_stall()
            time.sleep(1)  # Check every second
    
    def _check_for_stall(self) -> None:
        """Check if a stall has occurred."""
        latest_heartbeat = self.heartbeat_monitor.get_latest_heartbeat()
        
        if not latest_heartbeat:
            # No heartbeats yet, not stalled
            self._stalled = False
            self._stall_info = None
            return
        
        # Check age of latest heartbeat
        heartbeat_time = datetime.fromisoformat(latest_heartbeat['timestamp'])
        age = datetime.utcnow() - heartbeat_time
        
        if age.total_seconds() > self.timeout_seconds:
            # Stall detected
            self._stalled = True
            stall_duration = age.total_seconds()
            
            # Classify stall type
            if stall_duration < self.timeout_seconds * 2:
                stall_type = 'soft_stall'
            elif stall_duration < self.timeout_seconds * 4:
                stall_type = 'hard_stall'
            else:
                stall_type = 'deadlock'
            
            self._stall_info = {
                'type': stall_type,
                'duration_seconds': stall_duration,
                'last_heartbeat': latest_heartbeat['timestamp'],
                'detected_at': datetime.utcnow().isoformat()
            }
        else:
            # No stall
            self._stalled = False
            self._stall_info = None
