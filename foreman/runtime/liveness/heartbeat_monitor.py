"""
Heartbeat Monitor - generates regular heartbeat signals.

Implements continuous heartbeat generation to prove liveness.
"""

import threading
import time
from datetime import datetime
from typing import List, Dict, Any


class HeartbeatMonitor:
    """
    Monitors system liveness through periodic heartbeat signals.
    
    Responsibilities:
    - Generate heartbeat signals at regular intervals
    - Track heartbeat history
    - Provide liveness proof
    """
    
    def __init__(self, interval_seconds: int = 5):
        """
        Initialize HeartbeatMonitor.
        
        Args:
            interval_seconds: Time between heartbeats in seconds
        """
        self.interval_seconds = interval_seconds
        self._heartbeats: List[Dict[str, Any]] = []
        self._running = False
        self._thread: threading.Thread = None
    
    def start(self) -> None:
        """Start generating heartbeats."""
        if self._running:
            return
        
        self._running = True
        self._thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self._thread.start()
    
    def stop(self) -> None:
        """Stop generating heartbeats."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)
    
    def get_heartbeats(self) -> List[Dict[str, Any]]:
        """
        Get all recorded heartbeats.
        
        Returns:
            List of heartbeat records
        """
        return self._heartbeats.copy()
    
    def get_latest_heartbeat(self) -> Dict[str, Any]:
        """
        Get the most recent heartbeat.
        
        Returns:
            Latest heartbeat record or None
        """
        return self._heartbeats[-1] if self._heartbeats else None
    
    def _heartbeat_loop(self) -> None:
        """Internal loop that generates heartbeats."""
        while self._running:
            self._generate_heartbeat()
            time.sleep(self.interval_seconds)
    
    def _generate_heartbeat(self) -> None:
        """Generate a single heartbeat."""
        heartbeat = {
            'timestamp': datetime.utcnow().isoformat(),
            'status': 'alive',
            'interval': self.interval_seconds
        }
        self._heartbeats.append(heartbeat)
