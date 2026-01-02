"""
GOV-02: Governance Validator
QA-121 to QA-125

Validates actions/artifacts against governance rules.
Detects violations, generates reports, logs validation events.
"""

from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class ViolationType(Enum):
    """Types of governance violations."""
    HARD = "hard"  # Must be fixed immediately
    SOFT = "soft"  # Should be fixed but not blocking


@dataclass
class Violation:
    """Represents a governance violation."""
    violation_id: str
    rule_id: str
    violation_type: ViolationType
    description: str
    affected_component: str
    remediation: str
    context: Dict[str, any]
    detected_at: datetime = field(default_factory=datetime.now)


class GovernanceValidator:
    """
    GOV-02: Governance Validator
    
    Validates against governance rules and detects violations.
    Implements QA-121 to QA-125.
    """
    
    def __init__(self, governance_loader=None):
        self.governance_loader = governance_loader
        self.validation_history: List[Dict[str, any]] = []
        self.violations: Dict[str, Violation] = {}
    
    def validate(self, artifact: Dict[str, any], rule_ids: Optional[List[str]] = None) -> Dict[str, any]:
        """
        QA-121: Validate against governance rules.
        
        Executes rules, detects violations, determines pass/fail.
        
        Args:
            artifact: Artifact to validate
            rule_ids: Optional specific rules to check (defaults to all)
            
        Returns:
            Dict containing validation result
        """
        import uuid
        
        violations_found: List[Violation] = []
        rules_checked = 0
        
        # Get rules to validate against
        if self.governance_loader:
            if rule_ids:
                rules = [self.governance_loader.get_rule(rid) for rid in rule_ids if self.governance_loader.get_rule(rid)]
            else:
                rules = list(self.governance_loader.rules.values())
        else:
            rules = []
        
        # Execute each rule
        for rule in rules:
            rules_checked += 1
            violation = self._execute_rule(rule, artifact)
            if violation:
                self.violations[violation.violation_id] = violation
                violations_found.append(violation)
        
        # Determine pass/fail
        passed = len(violations_found) == 0
        
        # Log validation
        validation_event = {
            'artifact': artifact.get('name', 'unknown'),
            'rules_checked': rules_checked,
            'violations_found': len(violations_found),
            'passed': passed,
            'timestamp': datetime.now().isoformat()
        }
        self.validation_history.append(validation_event)
        
        return {
            'passed': passed,
            'rules_checked': rules_checked,
            'violations': [self._serialize_violation(v) for v in violations_found],
            'validation_id': str(uuid.uuid4())
        }
    
    def detect_violations(self, artifact: Dict[str, any]) -> Dict[str, any]:
        """
        QA-122: Detect governance violations.
        
        Identifies hard and soft violations with context.
        
        Args:
            artifact: Artifact to check
            
        Returns:
            Dict containing detected violations
        """
        validation_result = self.validate(artifact)
        
        hard_violations = []
        soft_violations = []
        
        for violation_data in validation_result['violations']:
            if violation_data['type'] == 'hard':
                hard_violations.append(violation_data)
            else:
                soft_violations.append(violation_data)
        
        return {
            'hard_violations': hard_violations,
            'soft_violations': soft_violations,
            'hard_count': len(hard_violations),
            'soft_count': len(soft_violations),
            'total_violations': len(validation_result['violations'])
        }
    
    def generate_violation_report(self, violation_id: str) -> Dict[str, any]:
        """
        QA-123: Generate violation report.
        
        Creates detailed report with description, affected component, remediation.
        
        Args:
            violation_id: ID of violation to report
            
        Returns:
            Dict containing violation report
        """
        if violation_id not in self.violations:
            raise KeyError(f"Violation {violation_id} not found")
        
        violation = self.violations[violation_id]
        
        return {
            'violation_id': violation_id,
            'rule_id': violation.rule_id,
            'type': violation.violation_type.value,
            'description': violation.description,
            'affected_component': violation.affected_component,
            'remediation_guidance': violation.remediation,
            'context': violation.context,
            'detected_at': violation.detected_at.isoformat()
        }
    
    def log_validation_event(self, event: Dict[str, any]) -> Dict[str, any]:
        """
        QA-124: Log governance validation events.
        
        Creates audit trail of all validation activities.
        
        Args:
            event: Validation event to log
            
        Returns:
            Dict containing log status
        """
        log_entry = {
            **event,
            'logged_at': datetime.now().isoformat()
        }
        
        self.validation_history.append(log_entry)
        
        return {
            'logged': True,
            'audit_trail_size': len(self.validation_history),
            'logged_at': log_entry['logged_at']
        }
    
    def get_validation_history(self) -> List[Dict[str, any]]:
        """Get complete validation history."""
        return self.validation_history
    
    def handle_failure_modes(self, failure_type: str, **kwargs) -> Dict[str, any]:
        """
        QA-125: Handle governance validator failure modes.
        
        Handles:
        - Rule execution failure
        - False positive prevention
        """
        if failure_type == 'rule_execution_failure':
            rule_id = kwargs.get('rule_id')
            error = kwargs.get('error')
            
            return {
                'status': 'logged',
                'rule_id': rule_id,
                'error': str(error),
                'action': 'skip_rule_and_continue',
                'validation_continued': True
            }
        
        elif failure_type == 'false_positive':
            # Implement logic to detect and prevent false positives
            violation_id = kwargs.get('violation_id')
            
            if violation_id and violation_id in self.violations:
                violation = self.violations[violation_id]
                
                # Check if violation might be false positive
                is_false_positive = self._check_false_positive(violation)
                
                if is_false_positive:
                    # Remove from violations
                    del self.violations[violation_id]
                    
                    return {
                        'status': 'false_positive_detected',
                        'violation_id': violation_id,
                        'action': 'violation_removed'
                    }
            
            return {
                'status': 'checked',
                'is_false_positive': False
            }
        
        return {'status': 'error', 'reason': f'Unknown failure type: {failure_type}'}
    
    def _execute_rule(self, rule, artifact: Dict[str, any]) -> Optional[Violation]:
        """Execute a governance rule against an artifact."""
        import uuid
        
        # Simulated rule execution for testing
        # In production, this would execute actual rule logic
        
        # Example: check if artifact has required fields
        if rule.rule_id == 'BP-001':  # One-Time Build Correctness
            if artifact.get('build_attempts', 1) > 1:
                return Violation(
                    violation_id=str(uuid.uuid4()),
                    rule_id=rule.rule_id,
                    violation_type=ViolationType.HARD,
                    description="Build required multiple attempts",
                    affected_component=artifact.get('name', 'unknown'),
                    remediation="Ensure architecture is complete before building",
                    context=artifact
                )
        
        return None
    
    def _serialize_violation(self, violation: Violation) -> Dict[str, any]:
        """Serialize violation for reporting."""
        return {
            'violation_id': violation.violation_id,
            'rule_id': violation.rule_id,
            'type': violation.violation_type.value,
            'description': violation.description,
            'affected_component': violation.affected_component,
            'remediation': violation.remediation,
            'detected_at': violation.detected_at.isoformat()
        }
    
    def _check_false_positive(self, violation: Violation) -> bool:
        """Check if violation might be a false positive."""
        # Simulated false positive detection
        # In production, would have more sophisticated logic
        return False
