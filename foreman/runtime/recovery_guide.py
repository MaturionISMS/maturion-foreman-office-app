"""
Recovery Guide - provides recovery paths for different failure types.

Implements failure classification and recovery documentation.
"""

from typing import Dict, List, Optional, Any


class RecoveryGuide:
    """
    Provides recovery paths for different failure types.
    
    Responsibilities:
    - Failure type classification
    - Recovery path documentation
    - Recovery step guidance
    """
    
    # Recovery paths for known failure types
    RECOVERY_PATHS = {
        'architecture_mismatch': {
            'name': 'Architecture-QA Mismatch',
            'steps': [
                'Review architecture document for completeness',
                'Review QA test suite for coverage',
                'Identify mismatched requirements',
                'Update architecture or QA as appropriate (with CS2 approval if needed)',
                'Re-validate architecture completeness',
                'Retry build'
            ],
            'requires_approval': True,
            'escalation_target': 'foreman'
        },
        'test_failure': {
            'name': 'Test Failure',
            'steps': [
                'Review failing test assertions',
                'Check implementation against architecture',
                'Verify test expectations are correct',
                'Fix implementation or escalate if test is incorrect',
                'Re-run tests'
            ],
            'requires_approval': False,
            'escalation_target': None
        },
        'builder_stall': {
            'name': 'Builder Stall',
            'steps': [
                'Check builder heartbeat status',
                'Review builder logs',
                'Classify stall type (soft/hard/deadlock)',
                'Apply appropriate recovery strategy',
                'Monitor recovery progress'
            ],
            'requires_approval': False,
            'escalation_target': 'foreman'
        },
        'governance_violation': {
            'name': 'Governance Violation',
            'steps': [
                'Identify violated governance rule',
                'Document violation details',
                'Halt all related work immediately',
                'Escalate to Foreman',
                'Wait for governance decision',
                'Apply corrective action'
            ],
            'requires_approval': True,
            'escalation_target': 'foreman'
        }
    }
    
    def __init__(self):
        """Initialize RecoveryGuide."""
        pass
    
    def get_recovery_path(self, failure_type: str) -> Optional[Dict[str, Any]]:
        """
        Get recovery path for a failure type.
        
        Args:
            failure_type: Type of failure
            
        Returns:
            Recovery path dictionary or None if not found
        """
        return self.RECOVERY_PATHS.get(failure_type)
    
    def list_failure_types(self) -> List[str]:
        """
        List all known failure types.
        
        Returns:
            List of failure type identifiers
        """
        return list(self.RECOVERY_PATHS.keys())
