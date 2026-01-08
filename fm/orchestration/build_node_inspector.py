"""
Build Node Inspector

Provides inspection and drill-down capabilities for build nodes.
Implements the BUILD_NODE_INSPECTION_MODEL.md (G-C9) specification.

Core Principle: "No status without explanation"
Every status, state, or indicator must be fully explainable through inspection.
"""

import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime, timezone
import json

logger = logging.getLogger(__name__)


class BuildNodeInspector:
    """
    Inspector for build tree nodes (Program, Wave, Task).
    
    Provides read-only inspection and drill-down capabilities.
    Enforces the principle: "No status without explanation."
    """
    
    def __init__(self, repo_root: Path):
        """
        Initialize the build node inspector.
        
        Args:
            repo_root: Root directory of the repository
        """
        self.repo_root = repo_root
        self.architecture_dir = repo_root / "architecture"
        self.governance_dir = repo_root / "governance"
        
    def inspect_node(
        self,
        node_type: str,
        node_id: str,
        depth: int = 3,
        include_children: bool = False
    ) -> Dict[str, Any]:
        """
        Inspect a build node and return comprehensive information.
        
        Args:
            node_type: Type of node ('program', 'wave', 'sub-wave', 'task')
            node_id: Unique identifier for the node
            depth: Inspection depth level (1-5)
            include_children: Whether to include child nodes
            
        Returns:
            Dictionary containing inspection data
        """
        logger.info(f"Inspecting {node_type} node: {node_id} (depth={depth})")
        
        # Validate inputs
        if node_type not in ['program', 'wave', 'sub-wave', 'task']:
            raise ValueError(f"Invalid node_type: {node_type}")
        
        if depth not in range(1, 6):
            raise ValueError(f"Invalid depth: {depth}. Must be 1-5")
        
        # Build inspection data based on depth
        inspection_data = {
            "node_id": node_id,
            "node_type": node_type,
            "last_inspected_at": datetime.now(timezone.utc).isoformat() + "Z"
        }
        
        # Level 1: Quick Status View (always included)
        inspection_data.update(self._get_quick_status(node_type, node_id))
        
        # Level 2: State Explanation
        if depth >= 2:
            inspection_data["current_state"] = self._get_state_explanation(node_type, node_id)
        
        # Level 3: Evidence & Requirements
        if depth >= 3:
            inspection_data["governing_checks"] = self._get_governing_checks(node_type, node_id)
            inspection_data["requirements"] = self._get_requirements(node_type, node_id)
            inspection_data["evidence"] = self._get_evidence(node_type, node_id)
            inspection_data["evidence_summary"] = self._get_evidence_summary(
                inspection_data["evidence"]
            )
        
        # Level 4: Decisions & Audit Trail
        if depth >= 4:
            inspection_data["decisions"] = self._get_decisions(node_type, node_id)
            inspection_data["audit_reports"] = self._get_audit_reports(node_type, node_id)
            inspection_data["surveys"] = self._get_surveys(node_type, node_id)
        
        # Level 5: Blockers & STOP Conditions
        if depth >= 5:
            inspection_data["blockers"] = self._get_blockers(node_type, node_id)
            inspection_data["blocker_resolution_paths"] = self._get_resolution_paths(
                inspection_data["blockers"]
            )
            inspection_data["stop_conditions"] = self._get_stop_conditions(node_type, node_id)
        
        # Include children if requested
        if include_children:
            inspection_data["children"] = self._get_children(node_type, node_id)
        
        return inspection_data
    
    def _get_quick_status(self, node_type: str, node_id: str) -> Dict[str, Any]:
        """Get Level 1: Quick status view"""
        # TODO: Load from actual build tree data
        # For now, return mock data structure
        return {
            "name": f"Sample {node_type.title()}: {node_id}",
            "description": f"Description for {node_id}",
            "created_at": "2025-12-29T08:00:00Z",
            "updated_at": "2025-12-29T12:00:00Z"
        }
    
    def _get_state_explanation(self, node_type: str, node_id: str) -> Dict[str, Any]:
        """Get Level 2: State explanation"""
        # TODO: Load from actual build tree data
        return {
            "execution_state": "IN_PROGRESS",
            "execution_state_reason": "Builder is actively implementing components",
            "execution_state_since": "2025-12-29T10:00:00Z",
            
            "activation_state": "ACTIVE",
            "activation_state_reason": "Approved and assigned to builder",
            "activation_state_since": "2025-12-29T09:15:00Z",
            
            "status": "GREEN",
            "status_reason": "On track, no blockers, QA plan ready",
            "status_contributing_factors": [
                {
                    "factor_type": "evidence_complete",
                    "description": "Architecture complete",
                    "severity": "MAJOR",
                    "contributing_to": "GREEN"
                },
                {
                    "factor_type": "qa_ready",
                    "description": "QA suite in RED status",
                    "severity": "MAJOR",
                    "contributing_to": "GREEN"
                },
                {
                    "factor_type": "no_blockers",
                    "description": "No active blockers",
                    "severity": "MAJOR",
                    "contributing_to": "GREEN"
                }
            ],
            
            "completion_percentage": 0,
            "completion_calculation": "Binary: 0% until complete, then 100%",
            "completion_is_authoritative": False
        }
    
    def _get_governing_checks(self, node_type: str, node_id: str) -> List[Dict[str, Any]]:
        """Get governing checks applicable to this node"""
        # TODO: Load from actual governance data
        return [
            {
                "check_id": "arch-completeness",
                "check_name": "Architecture Completeness Check",
                "check_type": "architecture",
                "description": "Verify architecture document is 100% complete",
                "required": True,
                "status": "PASS",
                "last_checked_at": "2025-12-29T09:00:00Z"
            },
            {
                "check_id": "qa-coverage",
                "check_name": "QA Coverage Check",
                "check_type": "qa",
                "description": "Verify QA test coverage meets minimum requirements",
                "required": True,
                "status": "PASS",
                "last_checked_at": "2025-12-29T09:05:00Z"
            },
            {
                "check_id": "zero-test-debt",
                "check_name": "Zero Test Debt Check",
                "check_type": "qa",
                "description": "Verify no skipped or incomplete tests",
                "required": True,
                "status": "PASS",
                "last_checked_at": "2025-12-29T09:05:00Z"
            }
        ]
    
    def _get_requirements(self, node_type: str, node_id: str) -> List[Dict[str, Any]]:
        """Get requirements applicable to this node"""
        # TODO: Load from actual requirements data
        return [
            {
                "requirement_id": "req-arch-doc",
                "requirement_name": "Architecture Document Exists",
                "requirement_type": "architecture",
                "description": "Architecture document must exist and be validated",
                "mandatory": True,
                "satisfied": True,
                "satisfied_at": "2025-12-29T08:30:00Z",
                "satisfied_by": "Foreman"
            },
            {
                "requirement_id": "req-qa-pass",
                "requirement_name": "QA Suite 100% Pass",
                "requirement_type": "qa",
                "description": "QA test suite must show 100% pass rate",
                "mandatory": True,
                "satisfied": True,
                "satisfied_at": "2025-12-29T09:00:00Z",
                "satisfied_by": "qa-builder"
            },
            {
                "requirement_id": "req-zero-debt",
                "requirement_name": "Zero Test Debt",
                "requirement_type": "qa",
                "description": "No skipped or incomplete tests allowed",
                "mandatory": True,
                "satisfied": True,
                "satisfied_at": "2025-12-29T09:00:00Z",
                "satisfied_by": "qa-builder"
            },
            {
                "requirement_id": "req-pr-merged",
                "requirement_name": "PR Merged",
                "requirement_type": "evidence",
                "description": "Pull request must be merged to main branch",
                "mandatory": True,
                "satisfied": False,
                "unsatisfied_reason": "Task still in progress"
            },
            {
                "requirement_id": "req-foreman-signoff",
                "requirement_name": "Foreman Sign-off",
                "requirement_type": "approval",
                "description": "Foreman must validate evidence and approve completion",
                "mandatory": True,
                "satisfied": False,
                "unsatisfied_reason": "Awaiting task completion"
            }
        ]
    
    def _get_evidence(self, node_type: str, node_id: str) -> List[Dict[str, Any]]:
        """Get evidence artifacts for this node"""
        # TODO: Load from actual evidence data
        return [
            {
                "id": "ev-arch-001",
                "category": "ARCHITECTURE",
                "artifact_type": "markdown",
                "artifact_location": f"/architecture/{node_id}-spec.md",
                "artifact_description": "Architecture specification document",
                "validated": True,
                "validated_at": "2025-12-29T08:30:00Z",
                "validated_by": "Foreman",
                "validation_notes": "Complete and meets all requirements"
            },
            {
                "id": "ev-qa-001",
                "category": "QA",
                "artifact_type": "test_results",
                "artifact_location": f"/tests/{node_id}/results.json",
                "artifact_description": "QA test execution results",
                "validated": True,
                "validated_at": "2025-12-29T09:00:00Z",
                "validated_by": "qa-builder",
                "validation_notes": "15/15 tests passing, 100% coverage"
            },
            {
                "id": "ev-build-001",
                "category": "BUILD",
                "artifact_type": "pr",
                "artifact_location": "https://github.com/MaturionISMS/repo/pull/145",
                "artifact_description": "Pull request for task implementation",
                "validated": False,
                "validation_notes": "Pending: Task in progress"
            },
            {
                "id": "ev-completion-001",
                "category": "COMPLETION",
                "artifact_type": "report",
                "artifact_location": f"/foreman/evidence/{node_id}-validation.md",
                "artifact_description": "Evidence validation report by Foreman",
                "validated": False,
                "validation_notes": "Pending: Awaiting task completion"
            }
        ]
    
    def _get_evidence_summary(self, evidence: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Summarize evidence artifacts"""
        by_category = {"ARCHITECTURE": 0, "QA": 0, "BUILD": 0, "COMPLETION": 0}
        validated_count = 0
        
        for ev in evidence:
            category = ev.get("category", "")
            if category in by_category:
                by_category[category] += 1
            if ev.get("validated", False):
                validated_count += 1
        
        return {
            "total_evidence_items": len(evidence),
            "validated_items": validated_count,
            "pending_items": len(evidence) - validated_count,
            "by_category": by_category
        }
    
    def _get_decisions(self, node_type: str, node_id: str) -> List[Dict[str, Any]]:
        """Get decisions related to this node"""
        # TODO: Load from actual decision data
        return [
            {
                "decision_id": "dec-001",
                "decision_type": "approval",
                "decision_summary": "Approval to proceed with task",
                "decision_rationale": "Architecture complete, QA plan validated, resources available",
                "decision_authority": "Johan",
                "decided_at": "2025-12-29T09:00:00Z",
                "related_node_id": node_id
            },
            {
                "decision_id": "dec-002",
                "decision_type": "authorization",
                "decision_summary": "Builder assignment: ui-builder",
                "decision_rationale": "Task scope matches UI builder expertise",
                "decision_authority": "Foreman",
                "decided_at": "2025-12-29T09:15:00Z",
                "related_node_id": node_id
            }
        ]
    
    def _get_audit_reports(self, node_type: str, node_id: str) -> List[Dict[str, Any]]:
        """Get audit reports related to this node"""
        # TODO: Load from actual audit data
        return [
            {
                "report_id": "audit-001",
                "report_type": "evidence_validation",
                "report_title": "Evidence Validation Report",
                "report_location": f"/foreman/evidence/{node_id}-validation.md",
                "created_at": "2025-12-29T09:10:00Z",
                "created_by": "Foreman",
                "findings_summary": "All evidence validated, no issues found"
            }
        ]
    
    def _get_surveys(self, node_type: str, node_id: str) -> List[Dict[str, Any]]:
        """Get surveys related to this node"""
        # TODO: Load from actual survey data
        return []
    
    def _get_blockers(self, node_type: str, node_id: str) -> List[Dict[str, Any]]:
        """Get active blockers for this node"""
        # TODO: Load from actual blocker data
        return []
    
    def _get_resolution_paths(self, blockers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get resolution paths for blockers"""
        # TODO: Generate resolution paths based on blockers
        return []
    
    def _get_stop_conditions(self, node_type: str, node_id: str) -> List[Dict[str, Any]]:
        """Get active STOP conditions for this node"""
        # TODO: Load from actual STOP condition data
        return []
    
    def _get_children(self, node_type: str, node_id: str) -> List[Dict[str, Any]]:
        """Get child nodes"""
        # TODO: Load from actual build tree data
        return []
    
    def log_inspection(
        self,
        node_id: str,
        node_type: str,
        inspected_by: str,
        inspection_depth: int,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> None:
        """
        Log an inspection access for audit trail.
        
        Args:
            node_id: Node being inspected
            node_type: Type of node
            inspected_by: User or system performing inspection
            inspection_depth: Depth level of inspection
            ip_address: Optional IP address
            user_agent: Optional user agent string
        """
        log_entry = {
            "log_id": f"inspect-{datetime.now(timezone.utc).timestamp()}",
            "node_id": node_id,
            "node_type": node_type,
            "inspected_by": inspected_by,
            "inspected_at": datetime.now(timezone.utc).isoformat() + "Z",
            "inspection_depth": inspection_depth,
            "ip_address": ip_address,
            "user_agent": user_agent
        }
        
        logger.info(f"Inspection audit log: {json.dumps(log_entry)}")
        
        # TODO: Write to persistent audit log storage


def create_inspector(repo_root: Path = None) -> BuildNodeInspector:
    """
    Factory function to create a BuildNodeInspector instance.
    
    Args:
        repo_root: Root directory of the repository (optional)
        
    Returns:
        BuildNodeInspector instance
    """
    if repo_root is None:
        repo_root = Path(__file__).parent.parent.parent
    
    return BuildNodeInspector(repo_root=repo_root)
