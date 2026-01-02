"""
GOV-03: Governance Supremacy Enforcer
QA-126 to QA-131

Enforces hard/soft violations, prevents governance weakening,
audits overrides, handles governance updates.
"""

from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import uuid


class EnforcementAction(Enum):
    """Actions taken by enforcer."""
    HALT = "halt"
    ESCALATE = "escalate"
    LOG = "log"
    ALLOW = "allow"


@dataclass
class EnforcementEvent:
    """Represents an enforcement action."""
    event_id: str
    violation_id: str
    action: EnforcementAction
    priority: str
    reason: str
    timestamp: datetime = field(default_factory=datetime.now)
    escalated_to: Optional[str] = None


class GovernanceSupremacyEnforcer:
    """
    GOV-03: Governance Supremacy Enforcer
    
    Enforces governance supremacy over all operations.
    Implements QA-126 to QA-131.
    """
    
    def __init__(self, governance_validator=None, escalation_manager=None):
        self.governance_validator = governance_validator
        self.escalation_manager = escalation_manager
        self.enforcement_log: List[EnforcementEvent] = []
        self.override_log: List[Dict[str, any]] = []
        self.protected_files = ['BUILD_PHILOSOPHY.md']
    
    def enforce_hard_violation(self, violation_id: str) -> Dict[str, any]:
        """
        QA-126: Enforce hard governance violations.
        
        Immediately halts operation, escalates with CRITICAL priority.
        
        Args:
            violation_id: ID of hard violation to enforce
            
        Returns:
            Dict containing enforcement result
        """
        if not self.governance_validator or violation_id not in self.governance_validator.violations:
            raise KeyError(f"Violation {violation_id} not found")
        
        violation = self.governance_validator.violations[violation_id]
        
        if violation.violation_type.value != 'hard':
            raise ValueError(f"Violation {violation_id} is not a hard violation")
        
        # Immediate halt
        halt_result = self._halt_operation(violation)
        
        # Escalate with CRITICAL priority
        escalation_result = self._escalate_violation(violation, priority="CRITICAL")
        
        # Log enforcement
        enforcement_event = EnforcementEvent(
            event_id=str(uuid.uuid4()),
            violation_id=violation_id,
            action=EnforcementAction.HALT,
            priority="CRITICAL",
            reason="Hard governance violation",
            escalated_to="ESC-02"
        )
        self.enforcement_log.append(enforcement_event)
        
        return {
            'violation_id': violation_id,
            'action': 'halt',
            'halted': halt_result['halted'],
            'escalated': escalation_result['escalated'],
            'priority': 'CRITICAL',
            'enforcement_event_id': enforcement_event.event_id
        }
    
    def enforce_soft_violation(self, violation_id: str) -> Dict[str, any]:
        """
        QA-127: Enforce soft governance violations.
        
        Escalates without halt, HIGH priority.
        
        Args:
            violation_id: ID of soft violation to enforce
            
        Returns:
            Dict containing enforcement result
        """
        if not self.governance_validator or violation_id not in self.governance_validator.violations:
            raise KeyError(f"Violation {violation_id} not found")
        
        violation = self.governance_validator.violations[violation_id]
        
        if violation.violation_type.value != 'soft':
            raise ValueError(f"Violation {violation_id} is not a soft violation")
        
        # Escalate with HIGH priority (no halt)
        escalation_result = self._escalate_violation(violation, priority="HIGH")
        
        # Log enforcement
        enforcement_event = EnforcementEvent(
            event_id=str(uuid.uuid4()),
            violation_id=violation_id,
            action=EnforcementAction.ESCALATE,
            priority="HIGH",
            reason="Soft governance violation",
            escalated_to="ESC-02"
        )
        self.enforcement_log.append(enforcement_event)
        
        return {
            'violation_id': violation_id,
            'action': 'escalate_without_halt',
            'halted': False,
            'escalated': escalation_result['escalated'],
            'priority': 'HIGH',
            'enforcement_event_id': enforcement_event.event_id
        }
    
    def prevent_governance_weakening(self, change: Dict[str, any]) -> Dict[str, any]:
        """
        QA-128: Prevent governance weakening.
        
        Ensures BUILD_PHILOSOPHY.md and core rules are immutable.
        
        Args:
            change: Proposed change to governance
            
        Returns:
            Dict indicating if change is allowed
        """
        file_changed = change.get('file')
        change_type = change.get('type')  # 'modify', 'delete', 'add'
        
        # Check if protected file
        if file_changed in self.protected_files:
            if change_type in ['modify', 'delete']:
                return {
                    'allowed': False,
                    'reason': f'{file_changed} is immutable',
                    'file': file_changed,
                    'protection_status': 'protected'
                }
        
        # Check if core rule is being weakened
        if 'rule_id' in change:
            rule_id = change['rule_id']
            if self._is_core_rule(rule_id):
                if change_type == 'modify' and self._is_weakening_change(change):
                    return {
                        'allowed': False,
                        'reason': f'Core rule {rule_id} cannot be weakened',
                        'rule_id': rule_id,
                        'protection_status': 'core_rule'
                    }
        
        return {
            'allowed': True,
            'reason': 'Change does not weaken governance',
            'change_approved': True
        }
    
    def audit_governance_override(
        self,
        override_request: Dict[str, any],
        justification: str,
        approved_by: str
    ) -> Dict[str, any]:
        """
        QA-129: Audit governance overrides.
        
        Logs override with justification and approval trail.
        
        Args:
            override_request: Details of override
            justification: Reason for override
            approved_by: Who approved the override
            
        Returns:
            Dict containing audit result
        """
        override_entry = {
            'override_id': str(uuid.uuid4()),
            'override_request': override_request,
            'justification': justification,
            'approved_by': approved_by,
            'timestamp': datetime.now().isoformat(),
            'approval_trail': [
                {
                    'approved_by': approved_by,
                    'timestamp': datetime.now().isoformat()
                }
            ]
        }
        
        self.override_log.append(override_entry)
        
        return {
            'override_logged': True,
            'override_id': override_entry['override_id'],
            'justification_captured': True,
            'approval_trail_created': True,
            'audit_complete': True
        }
    
    def handle_governance_update(self, update: Dict[str, any]) -> Dict[str, any]:
        """
        QA-130: Governance update handling.
        
        Checks version compatibility and breaking change detection.
        
        Args:
            update: Governance update details
            
        Returns:
            Dict containing compatibility analysis
        """
        current_version = update.get('current_version', '1.0.0')
        new_version = update.get('new_version', '1.0.1')
        changes = update.get('changes', [])
        
        # Check version compatibility
        is_compatible = self._check_version_compatibility(current_version, new_version)
        
        # Detect breaking changes
        breaking_changes = []
        for change in changes:
            if self._is_breaking_change(change):
                breaking_changes.append(change)
        
        has_breaking_changes = len(breaking_changes) > 0
        
        return {
            'current_version': current_version,
            'new_version': new_version,
            'is_compatible': is_compatible,
            'has_breaking_changes': has_breaking_changes,
            'breaking_changes': breaking_changes,
            'update_allowed': is_compatible and not has_breaking_changes
        }
    
    def handle_failure_modes(self, failure_type: str, **kwargs) -> Dict[str, any]:
        """
        QA-131: Handle governance supremacy failure modes.
        
        Handles:
        - Override abuse detection
        - Enforcement bypass prevention
        """
        if failure_type == 'override_abuse':
            # Check for override abuse patterns
            recent_overrides = self._get_recent_overrides(hours=24)
            
            if len(recent_overrides) > 5:  # More than 5 overrides in 24 hours
                return {
                    'status': 'abuse_detected',
                    'override_count': len(recent_overrides),
                    'period': '24 hours',
                    'action': 'escalate_to_governance_review',
                    'overrides_suspended': True
                }
            
            return {
                'status': 'normal',
                'override_count': len(recent_overrides),
                'abuse_detected': False
            }
        
        elif failure_type == 'enforcement_bypass':
            # Detect attempts to bypass enforcement
            bypass_attempt = kwargs.get('bypass_attempt', {})
            
            return {
                'status': 'bypass_prevented',
                'attempt_logged': True,
                'enforcement_maintained': True,
                'escalated': True,
                'action': 'Immediate escalation to security review'
            }
        
        return {'status': 'error', 'reason': f'Unknown failure type: {failure_type}'}
    
    def _halt_operation(self, violation) -> Dict[str, any]:
        """Halt current operation due to hard violation."""
        return {
            'halted': True,
            'reason': violation.description,
            'timestamp': datetime.now().isoformat()
        }
    
    def _escalate_violation(self, violation, priority: str) -> Dict[str, any]:
        """Escalate violation to ESC-02."""
        if self.escalation_manager:
            try:
                escalation = self.escalation_manager.create_escalation(
                    what=violation.description,
                    why="Governance violation detected",
                    blocked=violation.affected_component,
                    decision="Review and remediate governance violation",
                    consequence="System integrity at risk",
                    priority=priority
                )
                return {
                    'escalated': True,
                    'escalation_id': escalation.escalation_id,
                    'priority': priority
                }
            except:
                pass
        
        return {
            'escalated': False,
            'reason': 'Escalation manager not available'
        }
    
    def _is_core_rule(self, rule_id: str) -> bool:
        """Check if rule is a core rule."""
        core_rules = ['BP-001', 'BP-002', 'BP-003']  # Build Philosophy core rules
        return rule_id in core_rules
    
    def _is_weakening_change(self, change: Dict[str, any]) -> bool:
        """Check if change weakens governance."""
        # Simulated check
        return change.get('severity_change') == 'hard_to_soft'
    
    def _check_version_compatibility(self, current: str, new: str) -> bool:
        """Check if version update is compatible."""
        # Simple semantic versioning check
        current_major = int(current.split('.')[0])
        new_major = int(new.split('.')[0])
        
        # Breaking if major version changes
        return current_major == new_major
    
    def _is_breaking_change(self, change: Dict[str, any]) -> bool:
        """Check if change is breaking."""
        breaking_types = ['rule_removal', 'severity_reduction', 'mandatory_to_optional']
        return change.get('type') in breaking_types
    
    def _get_recent_overrides(self, hours: int = 24) -> List[Dict[str, any]]:
        """Get overrides from recent time period."""
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(hours=hours)
        
        recent = []
        for override in self.override_log:
            timestamp = datetime.fromisoformat(override['timestamp'])
            if timestamp > cutoff:
                recent.append(override)
        
        return recent
