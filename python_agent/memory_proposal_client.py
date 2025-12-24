"""
Maturion Foreman - Memory Proposal Client (Python)

This module provides memory write proposal functionality for Python agents.

**GOVERNANCE AUTHORITY:**
- /memory/AUTHORITY/MEMORY_WRITE_POLICY.md
- /memory/AUTHORITY/LESSONS_TO_CANON_WORKFLOW.md

**KEY PRINCIPLE:**
Proposals are NON-BINDING. They do NOT change memory fabric until approved.

Usage:
```python
from python_agent.memory_proposal_client import submit_memory_proposal, list_memory_proposals

# Submit a proposal (does NOT write to memory)
proposal_id = submit_memory_proposal(
    proposed_by='runtime-agent',
    proposed_memory={
        'scope': 'runtime',
        'title': 'Auto-fix Pattern Detected',
        'summary': 'Pattern for handling database timeouts',
        'importance': 'high',
        'tags': ['runtime', 'auto-fix', 'pattern']
    },
    rationale='This pattern successfully resolved 5 incidents'
)

# List pending proposals
pending = list_memory_proposals(status='pending')
```
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class MemoryProposalClient:
    """Client for memory write proposals"""
    
    def __init__(self, memory_root: Optional[str] = None):
        """
        Initialize memory proposal client
        
        Args:
            memory_root: Root directory for memory fabric (default: ./memory)
        """
        if memory_root is None:
            memory_root = os.path.join(os.getcwd(), 'memory')
        
        self.memory_root = memory_root
        self.proposals_root = os.path.join(memory_root, 'proposals')
        self.schema_path = os.path.join(memory_root, 'schema', 'memory-proposal.json')
    
    def submit_memory_proposal(
        self,
        proposed_by: str,
        proposed_memory: Dict[str, Any],
        rationale: str,
        evidence_count: Optional[int] = None,
        first_observed: Optional[str] = None,
        last_observed: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Submit a memory write proposal
        
        This submits a proposal for governance review.
        It does NOT write to the memory fabric.
        
        Args:
            proposed_by: Agent submitting the proposal
            proposed_memory: Memory entry being proposed
            rationale: Detailed justification (min 50 chars)
            evidence_count: Number of supporting observations
            first_observed: When pattern was first observed (ISO8601)
            last_observed: When pattern was last observed (ISO8601)
            metadata: Additional metadata
        
        Returns:
            Proposal ID
        
        Raises:
            ValueError: If validation fails
        """
        # Validate required fields
        if not proposed_by:
            raise ValueError('proposed_by is required')
        
        if not proposed_memory:
            raise ValueError('proposed_memory is required')
        
        if not rationale or len(rationale) < 50:
            raise ValueError('rationale is required and must be at least 50 characters')
        
        # Validate proposed memory has required fields
        required_fields = ['scope', 'title', 'summary', 'importance', 'tags']
        for field in required_fields:
            if field not in proposed_memory:
                raise ValueError(f'proposed_memory must have {field}')
        
        # Generate proposal ID
        timestamp = datetime.utcnow().isoformat() + 'Z'
        date_str = timestamp.split('T')[0]
        proposal_id = self._generate_proposal_id(date_str)
        
        # Create proposal object
        proposal = {
            'proposal_id': proposal_id,
            'proposed_by': proposed_by,
            'proposed_at': timestamp,
            'status': 'pending',
            'proposed_memory': proposed_memory,
            'rationale': rationale,
            'review_notes': []
        }
        
        # Add optional fields
        if evidence_count is not None:
            proposal['evidence_count'] = evidence_count
        if first_observed:
            proposal['first_observed'] = first_observed
        if last_observed:
            proposal['last_observed'] = last_observed
        if metadata:
            proposal['metadata'] = metadata
        
        # Validate proposal
        self._validate_proposal(proposal)
        
        # Write proposal to pending directory
        self._write_proposal(proposal, 'pending')
        
        return proposal_id
    
    def list_memory_proposals(
        self,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        List memory proposals by status
        
        Args:
            status: Filter by status ('pending', 'under_review', 'approved', 'rejected')
                   If None, returns all proposals
        
        Returns:
            List of proposals
        """
        proposals = []
        
        # Determine which directories to read
        if status:
            status_dirs = [status]
        else:
            status_dirs = ['pending', 'under_review', 'approved', 'rejected']
        
        for status_dir in status_dirs:
            dir_path = os.path.join(self.proposals_root, status_dir)
            
            if not os.path.exists(dir_path):
                continue
            
            try:
                files = os.listdir(dir_path)
            except OSError:
                continue
            
            for file in files:
                if not file.endswith('.json'):
                    continue
                if file == '.gitkeep':
                    continue
                
                file_path = os.path.join(dir_path, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        proposal = json.load(f)
                        proposals.append(proposal)
                except (OSError, json.JSONDecodeError) as e:
                    print(f"Warning: Could not load proposal file {file_path}: {e}")
        
        # Sort by proposed_at (newest first)
        proposals.sort(key=lambda p: p.get('proposed_at', ''), reverse=True)
        
        return proposals
    
    def get_proposal(self, proposal_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific proposal by ID
        
        Args:
            proposal_id: Proposal ID
        
        Returns:
            Proposal dict or None if not found
        """
        status_dirs = ['pending', 'under_review', 'approved', 'rejected']
        
        for status_dir in status_dirs:
            file_path = os.path.join(self.proposals_root, status_dir, f'{proposal_id}.json')
            
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except (OSError, json.JSONDecodeError):
                    continue
        
        return None
    
    def get_proposal_status(self, proposal_id: str) -> Optional[str]:
        """
        Get proposal status
        
        Args:
            proposal_id: Proposal ID
        
        Returns:
            Status string or None if not found
        """
        proposal = self.get_proposal(proposal_id)
        return proposal.get('status') if proposal else None
    
    def proposals_directory_exists(self) -> bool:
        """Check if proposals directory exists"""
        return os.path.exists(self.proposals_root)
    
    def initialize_proposals_directory(self) -> None:
        """Initialize proposals directory structure"""
        status_dirs = ['pending', 'under_review', 'approved', 'rejected']
        
        for status_dir in status_dirs:
            dir_path = os.path.join(self.proposals_root, status_dir)
            os.makedirs(dir_path, exist_ok=True)
    
    def _generate_proposal_id(self, date_str: str) -> str:
        """
        Generate unique proposal ID
        
        Args:
            date_str: Date string (YYYY-MM-DD)
        
        Returns:
            Proposal ID (prop-YYYY-MM-DD-NNN)
        """
        # Find highest existing number for this date
        max_num = 0
        pending_dir = os.path.join(self.proposals_root, 'pending')
        
        if os.path.exists(pending_dir):
            try:
                files = os.listdir(pending_dir)
                prefix = f'prop-{date_str}-'
                
                for file in files:
                    if file.startswith(prefix) and file.endswith('.json'):
                        try:
                            num_str = file[len(prefix):-5]  # Remove prefix and .json
                            num = int(num_str)
                            if num > max_num:
                                max_num = num
                        except ValueError:
                            continue
            except OSError:
                pass
        
        # Generate next ID
        next_num = max_num + 1
        return f'prop-{date_str}-{next_num:03d}'
    
    def _validate_proposal(self, proposal: Dict[str, Any]) -> None:
        """
        Validate proposal against basic rules
        
        Args:
            proposal: Proposal dict
        
        Raises:
            ValueError: If validation fails
        """
        # Check for forbidden content (basic PII check)
        content_to_check = json.dumps(proposal).lower()
        
        forbidden_patterns = [
            'email@',
            '@gmail',
            '@outlook',
            'password',
            'secret_key',
            'api_key',
            'organisation_id',
            'user_id'
        ]
        
        for pattern in forbidden_patterns:
            if pattern.lower() in content_to_check:
                raise ValueError(f'Proposal may contain forbidden content: {pattern}')
        
        # Check rationale length
        if len(proposal['rationale']) < 50:
            raise ValueError('Rationale must be at least 50 characters')
    
    def _write_proposal(self, proposal: Dict[str, Any], status: str) -> None:
        """
        Write proposal to file
        
        Args:
            proposal: Proposal dict
            status: Status directory ('pending', 'under_review', etc.)
        """
        status_dir = os.path.join(self.proposals_root, status)
        os.makedirs(status_dir, exist_ok=True)
        
        file_path = os.path.join(status_dir, f"{proposal['proposal_id']}.json")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(proposal, f, indent=2)


# Convenience functions

def submit_memory_proposal(
    proposed_by: str,
    proposed_memory: Dict[str, Any],
    rationale: str,
    evidence_count: Optional[int] = None,
    first_observed: Optional[str] = None,
    last_observed: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
    memory_root: Optional[str] = None
) -> str:
    """
    Submit a memory write proposal (convenience function)
    
    Args:
        proposed_by: Agent submitting the proposal
        proposed_memory: Memory entry being proposed
        rationale: Detailed justification (min 50 chars)
        evidence_count: Number of supporting observations
        first_observed: When pattern was first observed (ISO8601)
        last_observed: When pattern was last observed (ISO8601)
        metadata: Additional metadata
        memory_root: Root directory for memory fabric
    
    Returns:
        Proposal ID
    """
    client = MemoryProposalClient(memory_root)
    return client.submit_memory_proposal(
        proposed_by=proposed_by,
        proposed_memory=proposed_memory,
        rationale=rationale,
        evidence_count=evidence_count,
        first_observed=first_observed,
        last_observed=last_observed,
        metadata=metadata
    )


def list_memory_proposals(
    status: Optional[str] = None,
    memory_root: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    List memory proposals (convenience function)
    
    Args:
        status: Filter by status ('pending', 'under_review', 'approved', 'rejected')
        memory_root: Root directory for memory fabric
    
    Returns:
        List of proposals
    """
    client = MemoryProposalClient(memory_root)
    return client.list_memory_proposals(status)


def get_proposal(
    proposal_id: str,
    memory_root: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Get a specific proposal (convenience function)
    
    Args:
        proposal_id: Proposal ID
        memory_root: Root directory for memory fabric
    
    Returns:
        Proposal dict or None
    """
    client = MemoryProposalClient(memory_root)
    return client.get_proposal(proposal_id)


def get_proposal_status(
    proposal_id: str,
    memory_root: Optional[str] = None
) -> Optional[str]:
    """
    Get proposal status (convenience function)
    
    Args:
        proposal_id: Proposal ID
        memory_root: Root directory for memory fabric
    
    Returns:
        Status string or None
    """
    client = MemoryProposalClient(memory_root)
    return client.get_proposal_status(proposal_id)
