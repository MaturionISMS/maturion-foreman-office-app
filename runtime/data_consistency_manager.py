"""
Data Consistency Manager

Purpose: Detect and reconcile data consistency failures
Authority: Wave 2.0 Subwave 2.8 - Full Watchdog Coverage (QA-399)
Tenant Isolation: All operations scoped by organisation_id
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timezone


class ConsistencyStatus(Enum):
    """Data consistency status"""
    CONSISTENT = "consistent"
    INCONSISTENT = "inconsistent"
    UNKNOWN = "unknown"


@dataclass
class Escalation:
    """Escalation record"""
    escalation_id: str
    escalation_type: str
    organisation_id: str
    timestamp: datetime
    details: Dict[str, Any]


class ConsistencyValidator:
    """Validates data consistency between sources"""
    
    def __init__(self):
        self._validation_history: List[Dict[str, Any]] = []
    
    def validate_consistency(
        self,
        source: Dict[str, Any],
        target: Dict[str, Any],
        record_id: str
    ) -> Dict[str, Any]:
        """
        Validate consistency between source and target data
        
        Returns consistency check result with differences
        """
        differences = {}
        
        # Check each field
        all_keys = set(source.keys()) | set(target.keys())
        
        for key in all_keys:
            source_value = source.get(key)
            target_value = target.get(key)
            
            if source_value != target_value:
                differences[key] = {
                    "source": source_value,
                    "target": target_value
                }
        
        status = ConsistencyStatus.CONSISTENT if not differences else ConsistencyStatus.INCONSISTENT
        
        result = {
            "status": status,
            "record_id": record_id,
            "differences": differences,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        self._validation_history.append(result)
        return result


class ReconciliationEngine:
    """Reconciles inconsistent data"""
    
    def __init__(self):
        self._reconciliation_history: List[Dict[str, Any]] = []
    
    def reconcile(
        self,
        source: Dict[str, Any],
        target: Dict[str, Any],
        record_id: str,
        strategy: str = "source_wins"
    ) -> Dict[str, Any]:
        """
        Reconcile inconsistent data using specified strategy
        
        Strategies:
        - source_wins: Source data takes precedence
        - target_wins: Target data takes precedence
        - latest_wins: Most recent timestamp wins
        - merge: Attempt to merge fields intelligently
        """
        
        # Check for irreconcilable conflicts
        # Same version but different data = conflict
        if (source.get("version") == target.get("version") and
            source.get("version") is not None and
            source.get("updated_at") == target.get("updated_at")):
            
            # Check if data is actually different
            differences = {}
            for key in source.keys():
                if key not in ["version", "updated_at", "record_id"] and source.get(key) != target.get(key):
                    differences[key] = {
                        "source": source.get(key),
                        "target": target.get(key)
                    }
            
            if differences:
                return {
                    "status": "failed",
                    "reason": "irreconcilable_conflict",
                    "record_id": record_id,
                    "conflicts": differences
                }
        
        resolved_data = {}
        
        if strategy == "source_wins":
            resolved_data = source.copy()
        elif strategy == "target_wins":
            resolved_data = target.copy()
        elif strategy == "latest_wins":
            # Compare timestamps
            source_time = source.get("updated_at", "")
            target_time = target.get("updated_at", "")
            resolved_data = source.copy() if source_time > target_time else target.copy()
        elif strategy == "merge":
            # Merge fields, preferring newer version
            resolved_data = target.copy()
            source_version = source.get("version", 0)
            target_version = target.get("version", 0)
            
            if source_version > target_version:
                resolved_data.update(source)
        else:
            resolved_data = source.copy()
        
        result = {
            "status": "reconciled",
            "record_id": record_id,
            "resolved_data": resolved_data,
            "strategy": strategy,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        self._reconciliation_history.append(result)
        return result


class DataConsistencyManager:
    """
    Manages data consistency validation and reconciliation
    
    Responsibilities:
    - Validate data consistency between sources
    - Detect inconsistencies
    - Reconcile inconsistent data
    - Escalate reconciliation failures
    - Maintain tenant isolation
    """
    
    def __init__(self, organisation_id: str):
        self.organisation_id = organisation_id
        self._validator = ConsistencyValidator()
        self._reconciliation_engine = ReconciliationEngine()
        self._escalations: List[Escalation] = []
    
    def get_validator(self) -> ConsistencyValidator:
        """Get consistency validator"""
        return self._validator
    
    def get_reconciliation_engine(self) -> ReconciliationEngine:
        """Get reconciliation engine"""
        return self._reconciliation_engine
    
    def escalate_reconciliation_failure(
        self,
        record_id: str,
        reason: str,
        details: Optional[Dict[str, Any]] = None
    ) -> str:
        """Escalate a reconciliation failure"""
        escalation_id = f"esc_{self.organisation_id}_{int(datetime.now(timezone.utc).timestamp())}"
        
        escalation = Escalation(
            escalation_id=escalation_id,
            escalation_type="data_consistency_failure",
            organisation_id=self.organisation_id,
            timestamp=datetime.now(timezone.utc),
            details={
                "record_id": record_id,
                "reason": reason,
                **(details or {})
            }
        )
        
        self._escalations.append(escalation)
        return escalation_id
    
    def get_escalations(self, organisation_id: str) -> List[Dict[str, Any]]:
        """Get escalations for organisation"""
        if organisation_id != self.organisation_id:
            return []
        
        return [
            {
                "escalation_id": e.escalation_id,
                "type": e.escalation_type,
                "timestamp": e.timestamp.isoformat(),
                "details": e.details
            }
            for e in self._escalations
        ]
