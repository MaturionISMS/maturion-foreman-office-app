"""
Lazy Consistency Manager

Provides consistency management for lazy loaded data including
consistency checks, validation, and synchronization.
"""

import time
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum


class ConsistencyStatus(Enum):
    """Consistency status enumeration"""
    CONSISTENT = "consistent"
    INCONSISTENT = "inconsistent"
    STALE = "stale"
    UNKNOWN = "unknown"


@dataclass
class ConsistencyCheck:
    """Result of a consistency check"""
    key: str
    status: ConsistencyStatus
    timestamp: float
    details: Dict[str, Any]
    message: str


class LazyConsistencyManager:
    """
    Lazy Consistency Manager
    
    Provides comprehensive consistency management including:
    - Consistency validation
    - Staleness detection
    - Synchronization tracking
    - Consistency alerts
    - Version management
    """
    
    def __init__(self, stale_threshold: int = 300):
        """
        Initialize consistency manager
        
        Args:
            stale_threshold: Time in seconds before data is considered stale
        """
        self.stale_threshold = stale_threshold
        self._consistency_checks: Dict[str, List[ConsistencyCheck]] = {}
        self._versions: Dict[str, int] = {}
        self._last_validated: Dict[str, float] = {}
        self._alerts: List[Dict[str, Any]] = []
    
    def check_consistency(
        self, 
        key: str, 
        last_loaded: Optional[float],
        validator: Optional[Callable[[], bool]] = None
    ) -> ConsistencyCheck:
        """
        Check data consistency
        
        Args:
            key: Loadable identifier
            last_loaded: Timestamp when data was last loaded
            validator: Optional validation function
        
        Returns:
            ConsistencyCheck result
        """
        current_time = time.time()
        
        # Check staleness
        if last_loaded is None:
            status = ConsistencyStatus.UNKNOWN
            message = "Data never loaded"
        elif current_time - last_loaded > self.stale_threshold:
            status = ConsistencyStatus.STALE
            message = f"Data is stale (loaded {int(current_time - last_loaded)}s ago)"
        elif validator is not None:
            # Run custom validator
            try:
                if validator():
                    status = ConsistencyStatus.CONSISTENT
                    message = "Data is consistent"
                else:
                    status = ConsistencyStatus.INCONSISTENT
                    message = "Data failed validation"
            except Exception as e:
                status = ConsistencyStatus.INCONSISTENT
                message = f"Validation error: {str(e)}"
        else:
            status = ConsistencyStatus.CONSISTENT
            message = "Data is consistent"
        
        # Create consistency check result
        check = ConsistencyCheck(
            key=key,
            status=status,
            timestamp=current_time,
            details={
                'last_loaded': last_loaded,
                'age_seconds': current_time - last_loaded if last_loaded else None,
                'stale_threshold': self.stale_threshold,
                'version': self._versions.get(key, 0)
            },
            message=message
        )
        
        # Record check
        if key not in self._consistency_checks:
            self._consistency_checks[key] = []
        self._consistency_checks[key].append(check)
        
        # Update last validated timestamp
        self._last_validated[key] = current_time
        
        # Generate alert for inconsistencies
        if status in [ConsistencyStatus.INCONSISTENT, ConsistencyStatus.STALE]:
            self._generate_alert(check)
        
        return check
    
    def _generate_alert(self, check: ConsistencyCheck) -> None:
        """Generate consistency alert"""
        alert = {
            'type': 'consistency_alert',
            'key': check.key,
            'status': check.status.value,
            'message': check.message,
            'timestamp': check.timestamp,
            'details': check.details
        }
        self._alerts.append(alert)
    
    def mark_version(self, key: str, version: Optional[int] = None) -> int:
        """
        Mark data version
        
        Args:
            key: Loadable identifier
            version: Version number (auto-increments if not provided)
        
        Returns:
            Version number
        """
        if version is not None:
            self._versions[key] = version
        else:
            self._versions[key] = self._versions.get(key, 0) + 1
        
        return self._versions[key]
    
    def get_version(self, key: str) -> int:
        """
        Get current version
        
        Args:
            key: Loadable identifier
        
        Returns:
            Current version number (0 if never versioned)
        """
        return self._versions.get(key, 0)
    
    def invalidate(self, key: str) -> bool:
        """
        Mark data as invalid/stale
        
        Args:
            key: Loadable identifier
        
        Returns:
            True if invalidated, False if not tracked
        """
        if key not in self._last_validated:
            return False
        
        # Set last validated to very old timestamp
        self._last_validated[key] = 0
        return True
    
    def get_consistency_status(self, key: str) -> ConsistencyStatus:
        """
        Get current consistency status
        
        Args:
            key: Loadable identifier
        
        Returns:
            Current consistency status
        """
        if key not in self._consistency_checks or not self._consistency_checks[key]:
            return ConsistencyStatus.UNKNOWN
        
        return self._consistency_checks[key][-1].status
    
    def get_consistency_history(self, key: str, limit: int = 10) -> List[ConsistencyCheck]:
        """
        Get consistency check history
        
        Args:
            key: Loadable identifier
            limit: Maximum number of checks to return
        
        Returns:
            List of recent consistency checks
        """
        if key not in self._consistency_checks:
            return []
        
        return self._consistency_checks[key][-limit:]
    
    def get_alerts(self) -> List[Dict[str, Any]]:
        """Get all consistency alerts"""
        return self._alerts.copy()
    
    def clear_alerts(self) -> None:
        """Clear all alerts"""
        self._alerts.clear()
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get consistency statistics
        
        Returns:
        - Total checks
        - Consistent count
        - Inconsistent count
        - Stale count
        - Alert count
        """
        all_checks = []
        for checks in self._consistency_checks.values():
            all_checks.extend(checks)
        
        if not all_checks:
            return {
                'total_checks': 0,
                'consistent_count': 0,
                'inconsistent_count': 0,
                'stale_count': 0,
                'unknown_count': 0,
                'alert_count': len(self._alerts),
                'tracked_keys': 0
            }
        
        consistent = sum(1 for c in all_checks if c.status == ConsistencyStatus.CONSISTENT)
        inconsistent = sum(1 for c in all_checks if c.status == ConsistencyStatus.INCONSISTENT)
        stale = sum(1 for c in all_checks if c.status == ConsistencyStatus.STALE)
        unknown = sum(1 for c in all_checks if c.status == ConsistencyStatus.UNKNOWN)
        
        return {
            'total_checks': len(all_checks),
            'consistent_count': consistent,
            'inconsistent_count': inconsistent,
            'stale_count': stale,
            'unknown_count': unknown,
            'alert_count': len(self._alerts),
            'tracked_keys': len(self._consistency_checks),
            'consistency_rate': consistent / len(all_checks) if all_checks else 0.0
        }
    
    def clear_history(self, key: Optional[str] = None) -> None:
        """
        Clear consistency history
        
        Args:
            key: Specific key to clear (clears all if None)
        """
        if key is not None:
            if key in self._consistency_checks:
                self._consistency_checks[key].clear()
        else:
            self._consistency_checks.clear()
