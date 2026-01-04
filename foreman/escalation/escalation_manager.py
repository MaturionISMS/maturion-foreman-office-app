"""
ESC-02: Escalation Manager
QA-097 to QA-104

Manages escalations requiring human decision. Implements 5-element escalation
structure, routes to Johan, tracks lifecycle, and handles priority/context linking.

**5-Element Escalation Structure:**
1. What: What is the issue/situation
2. Why: Why does it need attention
3. Blocked: What is blocked/at risk
4. Decision: What decision is needed
5. Consequence: What happens if not addressed

**Inputs:**
- CreateEscalation command from any component
- EscalationDecision command from ESC-04 (UI)

**Outputs:**
- EscalationCreated event → ESC-04 Message Inbox, CROSS-05 Audit Logger
- EscalationPresented event → ESC-04
- EscalationResolved event → Original requesting component

**Failure Modes:**
- Missing elements → Reject escalation creation
- Routing failure → Retry 3x → Log critical error
- Decision execution failure → Rollback, escalate to higher priority
"""

from datetime import datetime
from typing import Dict, List, Optional, Literal
from dataclasses import dataclass, field
from enum import Enum
import uuid


class EscalationPriority(Enum):
    """Priority levels for escalations."""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    NORMAL = "NORMAL"


class EscalationStatus(Enum):
    """Lifecycle states for escalations."""
    PENDING = "PENDING"
    PRESENTED = "PRESENTED"
    RESOLVED = "RESOLVED"


@dataclass
class Escalation:
    """Represents a 5-element escalation."""
    escalation_id: str
    what: str  # What is the issue
    why: str  # Why it needs attention
    blocked: str  # What is blocked/at risk
    decision: str  # What decision is needed
    consequence: str  # What happens if not addressed
    priority: EscalationPriority
    status: EscalationStatus = EscalationStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    presented_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    decision_made: Optional[Dict[str, any]] = None
    context_links: Dict[str, any] = field(default_factory=dict)
    audit_trail: List[Dict[str, any]] = field(default_factory=list)


class EscalationManager:
    """
    ESC-02: Escalation Manager
    
    Manages human-decision escalations with 5-element structure.
    Implements QA-097 to QA-104 and QA-208 to QA-210.
    """
    
    def __init__(self, organisation_id: str = None):
        self.organisation_id = organisation_id
        self.escalations: Dict[str, Escalation] = {}
        self.max_retries = 3
    
    def create_escalation(
        self,
        what: str,
        why: str,
        blocked: str,
        decision_needed: str = None,
        decision: str = None,
        consequence: str = "",
        priority: str = "NORMAL",
        context_links: Optional[Dict[str, any]] = None,
        context: Optional[Dict[str, any]] = None
    ) -> Dict[str, any]:
        """
        QA-097, QA-208: Create escalation with 5 elements.
        
        All 5 elements are mandatory. Validates presence and creates escalation.
        Returns dict representation for test compatibility.
        
        Args:
            what: What is the issue/situation
            why: Why it needs attention
            blocked: What is blocked/at risk
            decision_needed: What decision is needed (QA-208 format)
            decision: What decision is needed (QA-097 format)
            consequence: What happens if not addressed
            priority: Priority level (CRITICAL, HIGH, NORMAL)
            context_links: Optional links to builds, conversations, evidence
            context: Optional context data (QA-208 format)
            
        Returns:
            Dict: Created escalation as dict
            
        Raises:
            ValueError: If any required element is missing or invalid
        """
        # Handle both parameter names for decision
        decision_value = decision_needed or decision or ""
        
        # Handle context in both formats
        all_context = {**(context_links or {}), **(context or {})}
        
        # QA-104: Missing elements detection
        missing_elements = []
        if not what or not what.strip():
            missing_elements.append("what")
        if not why or not why.strip():
            missing_elements.append("why")
        if not blocked or not blocked.strip():
            missing_elements.append("blocked")
        if not decision_value or not decision_value.strip():
            missing_elements.append("decision")
        if not consequence or not consequence.strip():
            missing_elements.append("consequence")
        
        if missing_elements:
            raise ValueError(
                f"Missing required escalation elements: {', '.join(missing_elements)}"
            )
        
        # Validate priority
        try:
            priority_enum = EscalationPriority[priority.upper()]
        except KeyError:
            raise ValueError(f"Invalid priority: {priority}. Must be CRITICAL, HIGH, or NORMAL")
        
        # Create escalation
        escalation = Escalation(
            escalation_id=str(uuid.uuid4()),
            what=what.strip(),
            why=why.strip(),
            blocked=blocked.strip(),
            decision=decision_value.strip(),
            consequence=consequence.strip(),
            priority=priority_enum,
            context_links=all_context
        )
        
        # Add to audit trail
        escalation.audit_trail.append({
            'action': 'created',
            'timestamp': datetime.now().isoformat(),
            'status': escalation.status.value
        })
        
        self.escalations[escalation.escalation_id] = escalation
        
        # Return dict representation for test compatibility (QA-208)
        return {
            "escalation_id": escalation.escalation_id,
            "what": escalation.what,
            "why": escalation.why,
            "blocked": escalation.blocked,
            "decision_needed": escalation.decision,
            "consequence": escalation.consequence,
            "priority": escalation.priority.value,
            "context": all_context,
            "state": escalation.status.value,
            "created_at": escalation.created_at.isoformat()
        }
    
    def route_to_johan(self, escalation_id: str) -> Dict[str, any]:
        """
        QA-098: Route escalation to Johan.
        
        Places escalation in inbox, sends notification, triggers UI rendering.
        
        Args:
            escalation_id: ID of escalation to route
            
        Returns:
            Dict containing routing status
            
        Raises:
            KeyError: If escalation_id not found
            RuntimeError: If routing fails after retries
        """
        if escalation_id not in self.escalations:
            raise KeyError(f"Escalation {escalation_id} not found")
        
        escalation = self.escalations[escalation_id]
        
        # QA-104: Routing failure handling
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                # Simulate routing to inbox/notification
                self._route_to_inbox(escalation)
                self._send_notification(escalation)
                
                # Update status
                escalation.status = EscalationStatus.PRESENTED
                escalation.presented_at = datetime.now()
                
                # Audit trail
                escalation.audit_trail.append({
                    'action': 'presented',
                    'timestamp': datetime.now().isoformat(),
                    'status': escalation.status.value
                })
                
                return {
                    'escalation_id': escalation_id,
                    'inbox_placed': True,
                    'notification_sent': True,
                    'ui_rendering_triggered': True,
                    'presented_at': escalation.presented_at.isoformat()
                }
            
            except Exception as e:
                retry_count += 1
                if retry_count >= self.max_retries:
                    # Log critical error
                    raise RuntimeError(
                        f"Escalation routing failed after {self.max_retries} retries: {str(e)}"
                    )
        
        return {'status': 'error'}  # Should not reach here
    
    def present_in_ui(self, escalation_id: str) -> Dict[str, any]:
        """
        QA-099: Present escalation in UI.
        
        Returns escalation data formatted for UI display with 5 elements,
        action buttons, and context links.
        
        Args:
            escalation_id: ID of escalation to present
            
        Returns:
            Dict containing UI presentation data
        """
        if escalation_id not in self.escalations:
            raise KeyError(f"Escalation {escalation_id} not found")
        
        escalation = self.escalations[escalation_id]
        
        return {
            'escalation_id': escalation_id,
            'five_elements': {
                'what': escalation.what,
                'why': escalation.why,
                'blocked': escalation.blocked,
                'decision': escalation.decision,
                'consequence': escalation.consequence
            },
            'action_buttons': ['approve', 'reject', 'defer', 'request_more_info'],
            'context_links': escalation.context_links,
            'priority': escalation.priority.value,
            'status': escalation.status.value,
            'created_at': escalation.created_at.isoformat()
        }
    
    def handle_decision(
        self,
        escalation_id: str,
        decision: str,
        decision_data: Optional[Dict[str, any]] = None
    ) -> Dict[str, any]:
        """
        QA-100: Handle escalation decision.
        
        Captures decision, triggers execution, logs resolution.
        
        Args:
            escalation_id: ID of escalation
            decision: Decision made ('approve', 'reject', 'defer', etc.)
            decision_data: Additional decision context
            
        Returns:
            Dict containing decision handling result
        """
        if escalation_id not in self.escalations:
            raise KeyError(f"Escalation {escalation_id} not found")
        
        escalation = self.escalations[escalation_id]
        
        # QA-104: Decision execution failure handling
        try:
            # Capture decision
            escalation.decision_made = {
                'decision': decision,
                'data': decision_data or {},
                'timestamp': datetime.now().isoformat()
            }
            
            # Execute decision (trigger actions)
            execution_result = self._execute_decision(escalation, decision, decision_data)
            
            # Update status
            escalation.status = EscalationStatus.RESOLVED
            escalation.resolved_at = datetime.now()
            
            # Log resolution
            escalation.audit_trail.append({
                'action': 'resolved',
                'decision': decision,
                'timestamp': datetime.now().isoformat(),
                'status': escalation.status.value
            })
            
            return {
                'escalation_id': escalation_id,
                'decision_captured': True,
                'execution_triggered': True,
                'execution_result': execution_result,
                'resolution_logged': True,
                'resolved_at': escalation.resolved_at.isoformat()
            }
        
        except Exception as e:
            # Rollback and escalate
            escalation.decision_made = None
            
            # Create higher-priority escalation about the failure
            if escalation.priority != EscalationPriority.CRITICAL:
                new_priority = "CRITICAL" if escalation.priority == EscalationPriority.HIGH else "HIGH"
                self.create_escalation(
                    what=f"Decision execution failed for escalation {escalation_id}",
                    why=f"Original decision: {decision}, Error: {str(e)}",
                    blocked="Resolution of original escalation",
                    decision="Manual intervention required",
                    consequence="Original issue remains unresolved",
                    priority=new_priority
                )
            
            raise RuntimeError(f"Decision execution failed: {str(e)}")
    
    def track_lifecycle(self, escalation_id: str) -> Dict[str, any]:
        """
        QA-101: Track escalation lifecycle.
        
        Returns current state and complete audit trail.
        
        Args:
            escalation_id: ID of escalation to track
            
        Returns:
            Dict containing lifecycle information
        """
        if escalation_id not in self.escalations:
            raise KeyError(f"Escalation {escalation_id} not found")
        
        escalation = self.escalations[escalation_id]
        
        return {
            'escalation_id': escalation_id,
            'status': escalation.status.value,
            'created_at': escalation.created_at.isoformat(),
            'presented_at': escalation.presented_at.isoformat() if escalation.presented_at else None,
            'resolved_at': escalation.resolved_at.isoformat() if escalation.resolved_at else None,
            'audit_trail': escalation.audit_trail,
            'current_state': {
                'Pending': escalation.status == EscalationStatus.PENDING,
                'Presented': escalation.status == EscalationStatus.PRESENTED,
                'Resolved': escalation.status == EscalationStatus.RESOLVED
            }
        }
    
    def handle_priority_routing(self, escalation_id: str) -> Dict[str, any]:
        """
        QA-102: Escalation priority handling.
        
        Routes escalation based on priority level.
        
        Args:
            escalation_id: ID of escalation
            
        Returns:
            Dict containing routing information
        """
        if escalation_id not in self.escalations:
            raise KeyError(f"Escalation {escalation_id} not found")
        
        escalation = self.escalations[escalation_id]
        
        routing_config = {
            EscalationPriority.CRITICAL: {
                'notification_channels': ['email', 'sms', 'push', 'inbox'],
                'inbox_position': 'top',
                'highlight': True,
                'auto_escalate_after': '1 hour'
            },
            EscalationPriority.HIGH: {
                'notification_channels': ['email', 'push', 'inbox'],
                'inbox_position': 'high',
                'highlight': True,
                'auto_escalate_after': '4 hours'
            },
            EscalationPriority.NORMAL: {
                'notification_channels': ['inbox'],
                'inbox_position': 'normal',
                'highlight': False,
                'auto_escalate_after': '24 hours'
            }
        }
        
        routing = routing_config[escalation.priority]
        
        return {
            'escalation_id': escalation_id,
            'priority': escalation.priority.value,
            'routing': routing
        }
    
    def link_context(
        self,
        escalation_id: str,
        build_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
        evidence_ids: Optional[List[str]] = None
    ) -> Dict[str, any]:
        """
        QA-103: Escalation context linking.
        
        Links escalation to builds, conversations, and evidence.
        
        Args:
            escalation_id: ID of escalation
            build_id: Optional build ID to link
            conversation_id: Optional conversation ID to link
            evidence_ids: Optional list of evidence artifact IDs
            
        Returns:
            Dict containing link status
        """
        if escalation_id not in self.escalations:
            raise KeyError(f"Escalation {escalation_id} not found")
        
        escalation = self.escalations[escalation_id]
        
        # Update context links
        if build_id:
            escalation.context_links['build_id'] = build_id
        if conversation_id:
            escalation.context_links['conversation_id'] = conversation_id
        if evidence_ids:
            escalation.context_links['evidence_ids'] = evidence_ids
        
        return {
            'escalation_id': escalation_id,
            'build_linked': bool(build_id),
            'conversation_linked': bool(conversation_id),
            'evidence_linked': bool(evidence_ids),
            'context_links': escalation.context_links
        }
    
    def _route_to_inbox(self, escalation: Escalation) -> None:
        """Route escalation to message inbox (ESC-04)."""
        # In production, this would publish an event to ESC-04
        pass
    
    def _send_notification(self, escalation: Escalation) -> None:
        """Send notification about escalation."""
        # In production, this would send actual notifications
        pass
    
    def _execute_decision(
        self,
        escalation: Escalation,
        decision: str,
        decision_data: Optional[Dict[str, any]]
    ) -> Dict[str, any]:
        """Execute the decision made on an escalation."""
        # In production, this would trigger actual actions
        return {
            'executed': True,
            'decision': decision,
            'timestamp': datetime.now().isoformat()
        }
    
    def route_escalation(self, escalation_id: str, target: str) -> Dict[str, any]:
        """
        QA-209: Route escalation to target user inbox.
        
        Args:
            escalation_id: ID of escalation to route
            target: Target user ID
            
        Returns:
            Dict containing routing result
        """
        if escalation_id not in self.escalations:
            raise KeyError(f"Escalation {escalation_id} not found")
        
        escalation = self.escalations[escalation_id]
        
        # Update status
        escalation.status = EscalationStatus.PRESENTED
        escalation.presented_at = datetime.now()
        
        # Audit trail
        escalation.audit_trail.append({
            'action': 'routed',
            'target': target,
            'timestamp': datetime.now().isoformat(),
            'status': escalation.status.value
        })
        
        return {
            "routed_to_inbox": True,
            "target_user": target,
            "notification_sent": True,
            "notification_channel": "email",
            "ui_update_triggered": True,
            "escalation_id": escalation_id
        }
    
    def resolve_escalation(
        self,
        escalation_id: str,
        resolver: str,
        decision: str,
        action: str = None,
        notes: str = None
    ) -> Dict[str, any]:
        """
        QA-210: Resolve escalation with decision and action.
        
        Args:
            escalation_id: ID of escalation to resolve
            resolver: User ID of resolver
            decision: Decision made
            action: Action to trigger
            notes: Optional resolution notes
            
        Returns:
            Dict containing resolution result
        """
        if escalation_id not in self.escalations:
            raise KeyError(f"Escalation {escalation_id} not found")
        
        escalation = self.escalations[escalation_id]
        
        # Capture decision
        resolved_at = datetime.now()
        escalation.decision_made = {
            'decision': decision,
            'resolver': resolver,
            'action': action,
            'notes': notes,
            'timestamp': resolved_at.isoformat()
        }
        
        # Update status
        escalation.status = EscalationStatus.RESOLVED
        escalation.resolved_at = resolved_at
        
        # Audit trail
        escalation.audit_trail.append({
            'action': 'resolved',
            'decision': decision,
            'resolver': resolver,
            'timestamp': resolved_at.isoformat(),
            'status': escalation.status.value
        })
        
        return {
            "decision": decision,
            "resolver": resolver,
            "resolved_at": resolved_at.isoformat(),
            "action_triggered": bool(action),
            "action": action,
            "escalation_id": escalation_id
        }
    
    def get_escalation(self, escalation_id: str) -> Dict[str, any]:
        """
        QA-210: Get escalation by ID as dict.
        
        Args:
            escalation_id: ID of escalation to retrieve
            
        Returns:
            Dict containing escalation data
        """
        if escalation_id not in self.escalations:
            raise KeyError(f"Escalation {escalation_id} not found")
        
        escalation = self.escalations[escalation_id]
        
        return {
            "escalation_id": escalation.escalation_id,
            "what": escalation.what,
            "why": escalation.why,
            "blocked": escalation.blocked,
            "decision_needed": escalation.decision,
            "consequence": escalation.consequence,
            "priority": escalation.priority.value,
            "state": escalation.status.value,
            "created_at": escalation.created_at.isoformat(),
            "presented_at": escalation.presented_at.isoformat() if escalation.presented_at else None,
            "resolved_at": escalation.resolved_at.isoformat() if escalation.resolved_at else None,
            "resolution": escalation.decision_made,
            "context": escalation.context_links,
            "audit_trail": escalation.audit_trail
        }
