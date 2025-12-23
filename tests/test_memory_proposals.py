"""
Test Memory Write Proposals

Tests for:
- Proposal submission functionality
- Proposal storage (separate from memory fabric)
- Governance review path visibility
- Memory fabric remains unchanged
- No auto-approval enforcement

These tests validate that the Memory Write Proposal mechanism
correctly implements governance requirements for controlled memory writes.

Governance Authority:
- /memory/AUTHORITY/MEMORY_WRITE_POLICY.md
- /memory/AUTHORITY/LESSONS_TO_CANON_WORKFLOW.md
- /memory/schema/memory-proposal.json
"""

import pytest
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from python_agent.memory_proposal_client import (
    submit_memory_proposal,
    list_memory_proposals,
    get_proposal,
    get_proposal_status,
    MemoryProposalClient
)
from python_agent.memory_client import load_memory


@pytest.mark.memory
class TestProposalSubmission:
    """Test proposal submission functionality"""
    
    def test_can_submit_memory_proposal(self):
        """
        Test that memory proposals can be submitted successfully.
        
        Expected: Proposal is created and returns proposal ID
        """
        proposal_id = submit_memory_proposal(
            proposed_by='test-agent',
            proposed_memory={
                'scope': 'runtime',
                'title': 'Test Pattern Detected',
                'summary': 'This is a test pattern for automated testing purposes',
                'importance': 'high',
                'tags': ['test', 'pattern', 'runtime']
            },
            rationale='This is a test rationale that is sufficiently long to meet the minimum requirement of 50 characters'
        )
        
        assert proposal_id is not None, \
            "Proposal submission must return a proposal ID"
        assert proposal_id.startswith('prop-'), \
            "Proposal ID must follow prop-YYYY-MM-DD-NNN format"
    
    def test_proposal_requires_rationale(self):
        """
        Test that proposals require a rationale.
        
        Expected: ValueError if rationale is missing or too short
        """
        with pytest.raises(ValueError, match='rationale'):
            submit_memory_proposal(
                proposed_by='test-agent',
                proposed_memory={
                    'scope': 'runtime',
                    'title': 'Test Pattern',
                    'summary': 'Test summary',
                    'importance': 'high',
                    'tags': ['test']
                },
                rationale='Too short'
            )
    
    def test_proposal_requires_proposed_by(self):
        """
        Test that proposals require proposed_by field.
        
        Expected: ValueError if proposed_by is missing
        """
        with pytest.raises(ValueError, match='proposed_by'):
            submit_memory_proposal(
                proposed_by='',
                proposed_memory={
                    'scope': 'runtime',
                    'title': 'Test Pattern',
                    'summary': 'Test summary',
                    'importance': 'high',
                    'tags': ['test']
                },
                rationale='This is a sufficient rationale for testing purposes that meets requirements'
            )
    
    def test_proposal_requires_complete_memory_entry(self):
        """
        Test that proposals require complete memory entry fields.
        
        Expected: ValueError if required fields are missing
        """
        with pytest.raises(ValueError):
            submit_memory_proposal(
                proposed_by='test-agent',
                proposed_memory={
                    'scope': 'runtime',
                    'title': 'Test Pattern'
                    # Missing summary, importance, tags
                },
                rationale='This is a sufficient rationale for testing purposes that meets requirements'
            )


@pytest.mark.memory
class TestProposalStorage:
    """Test proposal storage mechanism"""
    
    def test_proposals_stored_separately_from_memory(self):
        """
        Test that proposals are stored separately from memory fabric.
        
        Expected: Proposals go to /memory/proposals/, not /memory/{scope}/
        """
        proposal_id = submit_memory_proposal(
            proposed_by='test-agent',
            proposed_memory={
                'scope': 'runtime',
                'title': 'Separation Test Pattern',
                'summary': 'Testing that proposals are stored separately from memory',
                'importance': 'high',
                'tags': ['test', 'separation']
            },
            rationale='This tests that proposals are stored in the proposals directory and not in the memory fabric itself'
        )
        
        # Check proposal exists in proposals/pending/
        proposals_dir = os.path.join(project_root, 'memory', 'proposals', 'pending')
        proposal_file = os.path.join(proposals_dir, f'{proposal_id}.json')
        
        assert os.path.exists(proposal_file), \
            f"Proposal should exist in proposals/pending/ directory: {proposal_file}"
        
        # Check proposal does NOT exist in memory/runtime/
        runtime_dir = os.path.join(project_root, 'memory', 'runtime')
        if os.path.exists(runtime_dir):
            runtime_files = os.listdir(runtime_dir)
            proposal_in_runtime = any(proposal_id in f for f in runtime_files)
            assert not proposal_in_runtime, \
                "Proposal should NOT exist in memory/runtime/ directory"
    
    def test_proposals_have_pending_status(self):
        """
        Test that new proposals have 'pending' status.
        
        Expected: Status is 'pending' after submission
        """
        proposal_id = submit_memory_proposal(
            proposed_by='test-agent',
            proposed_memory={
                'scope': 'foreman',
                'title': 'Status Test Pattern',
                'summary': 'Testing that proposals start with pending status',
                'importance': 'high',
                'tags': ['test', 'status']
            },
            rationale='This tests that newly submitted proposals automatically receive pending status'
        )
        
        status = get_proposal_status(proposal_id)
        assert status == 'pending', \
            "New proposals must have 'pending' status"
    
    def test_can_retrieve_submitted_proposal(self):
        """
        Test that submitted proposals can be retrieved.
        
        Expected: Proposal can be fetched by ID
        """
        proposal_id = submit_memory_proposal(
            proposed_by='test-agent',
            proposed_memory={
                'scope': 'platform',
                'title': 'Retrieval Test Pattern',
                'summary': 'Testing that proposals can be retrieved after submission',
                'importance': 'critical',
                'tags': ['test', 'retrieval']
            },
            rationale='This tests that proposals can be successfully retrieved using their ID after submission'
        )
        
        proposal = get_proposal(proposal_id)
        
        assert proposal is not None, \
            "Proposal must be retrievable by ID"
        assert proposal['proposal_id'] == proposal_id, \
            "Retrieved proposal must match submitted proposal ID"
        assert proposal['status'] == 'pending', \
            "Retrieved proposal must have correct status"


@pytest.mark.memory
class TestMemoryFabricIsolation:
    """Test that proposals do NOT affect memory fabric"""
    
    def test_memory_fabric_unchanged_by_proposals(self):
        """
        Test that memory fabric is unchanged after proposal submission.
        
        Expected: Memory entries remain the same before and after proposal
        """
        # Load memory before proposal
        memories_before = load_memory(
            scopes=['runtime'],
            tags=None,
            importance_min='low'
        )
        count_before = len(memories_before)
        
        # Submit proposal
        submit_memory_proposal(
            proposed_by='test-agent',
            proposed_memory={
                'scope': 'runtime',
                'title': 'Isolation Test Pattern',
                'summary': 'Testing that proposals do not modify the memory fabric',
                'importance': 'high',
                'tags': ['test', 'isolation']
            },
            rationale='This tests that submitting a proposal does not add entries to the memory fabric'
        )
        
        # Load memory after proposal
        memories_after = load_memory(
            scopes=['runtime'],
            tags=None,
            importance_min='low'
        )
        count_after = len(memories_after)
        
        assert count_before == count_after, \
            "Memory fabric must remain unchanged after proposal submission"
    
    def test_proposal_does_not_create_memory_entry(self):
        """
        Test that proposal submission does NOT create memory entry.
        
        Expected: No new memory entry with proposal content
        """
        test_title = 'Unique Test Title For Verification 12345'
        
        # Submit proposal with unique title
        submit_memory_proposal(
            proposed_by='test-agent',
            proposed_memory={
                'scope': 'runtime',
                'title': test_title,
                'summary': 'Testing that this does not become a memory entry immediately',
                'importance': 'high',
                'tags': ['test', 'unique']
            },
            rationale='This tests that proposal submission does not directly create memory entries'
        )
        
        # Search for this title in memory
        memories = load_memory(
            scopes=['runtime'],
            tags=None,
            importance_min='low'
        )
        
        matching_memories = [m for m in memories if m.get('title') == test_title]
        
        assert len(matching_memories) == 0, \
            "Proposal content must NOT appear in memory fabric"


@pytest.mark.memory
class TestGovernanceReviewPath:
    """Test governance review path visibility"""
    
    def test_can_list_pending_proposals(self):
        """
        Test that pending proposals are visible for review.
        
        Expected: Pending proposals can be listed
        """
        # Submit a proposal
        proposal_id = submit_memory_proposal(
            proposed_by='test-agent',
            proposed_memory={
                'scope': 'foreman',
                'title': 'Review Path Test',
                'summary': 'Testing that proposals are visible for governance review',
                'importance': 'high',
                'tags': ['test', 'review']
            },
            rationale='This tests that pending proposals can be listed and are visible for human review'
        )
        
        # List pending proposals
        pending = list_memory_proposals(status='pending')
        
        assert len(pending) > 0, \
            "Must be able to list pending proposals"
        
        proposal_ids = [p['proposal_id'] for p in pending]
        assert proposal_id in proposal_ids, \
            "Submitted proposal must appear in pending list"
    
    def test_proposals_contain_review_metadata(self):
        """
        Test that proposals contain metadata for review.
        
        Expected: Proposals have proposed_by, proposed_at, rationale
        """
        proposal_id = submit_memory_proposal(
            proposed_by='test-agent',
            proposed_memory={
                'scope': 'runtime',
                'title': 'Metadata Test',
                'summary': 'Testing that proposals have sufficient metadata for review',
                'importance': 'high',
                'tags': ['test', 'metadata']
            },
            rationale='This tests that proposals include all necessary metadata for governance review'
        )
        
        proposal = get_proposal(proposal_id)
        
        assert 'proposed_by' in proposal, \
            "Proposal must include proposed_by"
        assert 'proposed_at' in proposal, \
            "Proposal must include proposed_at timestamp"
        assert 'rationale' in proposal, \
            "Proposal must include rationale"
        assert 'status' in proposal, \
            "Proposal must include status"


@pytest.mark.memory
class TestNoAutoApproval:
    """Test that auto-approval is prevented"""
    
    def test_proposals_not_auto_approved(self):
        """
        Test that proposals are never auto-approved.
        
        Expected: All proposals remain 'pending' after submission
        """
        # Submit multiple proposals
        proposal_ids = []
        for i in range(3):
            proposal_id = submit_memory_proposal(
                proposed_by='test-agent',
                proposed_memory={
                    'scope': 'runtime',
                    'title': f'Auto-Approval Test {i}',
                    'summary': f'Testing auto-approval prevention, iteration {i}',
                    'importance': 'high',
                    'tags': ['test', 'auto-approval']
                },
                rationale='This tests that proposals are not automatically approved and require explicit human review'
            )
            proposal_ids.append(proposal_id)
        
        # Check all remain pending
        for proposal_id in proposal_ids:
            status = get_proposal_status(proposal_id)
            assert status == 'pending', \
                f"Proposal {proposal_id} must remain 'pending', not auto-approved"
    
    def test_no_automatic_memory_creation(self):
        """
        Test that memory entries are NOT automatically created.
        
        Expected: High importance proposals do not auto-create memory
        """
        # Count runtime memories before
        memories_before = load_memory(scopes=['runtime'], tags=None, importance_min='low')
        count_before = len(memories_before)
        
        # Submit high importance proposal
        submit_memory_proposal(
            proposed_by='test-agent',
            proposed_memory={
                'scope': 'runtime',
                'title': 'Critical Auto-Creation Test',
                'summary': 'Testing that even critical proposals do not auto-create memory',
                'importance': 'critical',
                'tags': ['test', 'critical']
            },
            rationale='This tests that even critical importance proposals require explicit approval'
        )
        
        # Count runtime memories after
        memories_after = load_memory(scopes=['runtime'], tags=None, importance_min='low')
        count_after = len(memories_after)
        
        assert count_before == count_after, \
            "Memory must not be auto-created for high/critical proposals"


@pytest.mark.memory
class TestProposalValidation:
    """Test proposal validation rules"""
    
    def test_proposal_rejects_potential_pii(self):
        """
        Test that proposals reject content with potential PII.
        
        Expected: ValueError for forbidden patterns
        """
        # Test email pattern
        with pytest.raises(ValueError, match='forbidden content'):
            submit_memory_proposal(
                proposed_by='test-agent',
                proposed_memory={
                    'scope': 'runtime',
                    'title': 'PII Test',
                    'summary': 'Contact user at test.email@example.com for more info',
                    'importance': 'high',
                    'tags': ['test']
                },
                rationale='This should be rejected due to email pattern in summary field'
            )
    
    def test_proposal_validates_required_fields(self):
        """
        Test that proposals validate required fields.
        
        Expected: Clear error messages for missing fields
        """
        with pytest.raises(ValueError):
            submit_memory_proposal(
                proposed_by='test-agent',
                proposed_memory={
                    'scope': 'runtime'
                    # Missing title, summary, importance, tags
                },
                rationale='This tests validation of required fields in proposed memory entry'
            )


@pytest.mark.memory
class TestProposalDirectoryStructure:
    """Test proposal directory structure"""
    
    def test_proposals_directory_exists(self):
        """
        Test that proposals directory structure exists.
        
        Expected: /memory/proposals/{pending,under_review,approved,rejected}/
        """
        client = MemoryProposalClient()
        
        assert client.proposals_directory_exists(), \
            "Proposals directory must exist"
        
        # Check subdirectories
        for status_dir in ['pending', 'under_review', 'approved', 'rejected']:
            dir_path = os.path.join(client.proposals_root, status_dir)
            assert os.path.exists(dir_path), \
                f"Proposals subdirectory must exist: {status_dir}"
    
    def test_proposals_separate_from_memory_scopes(self):
        """
        Test that proposals directory is separate from memory scopes.
        
        Expected: /memory/proposals/ is not a scope directory
        """
        # Proposals should not be loadable as memory scope
        try:
            memories = load_memory(scopes=['proposals'], tags=None, importance_min='low')
            # Should return empty or raise error, not load proposals as memories
            assert len(memories) == 0, \
                "Proposals must not be loadable as memory scope"
        except Exception:
            # Also acceptable - scopes may be validated
            pass


@pytest.mark.memory
class TestProposalIntegration:
    """Test proposal integration with existing systems"""
    
    def test_proposal_schema_exists(self):
        """
        Test that proposal schema file exists.
        
        Expected: /memory/schema/memory-proposal.json exists
        """
        schema_path = os.path.join(project_root, 'memory', 'schema', 'memory-proposal.json')
        
        assert os.path.exists(schema_path), \
            "Proposal schema must exist at /memory/schema/memory-proposal.json"
        
        # Validate it's valid JSON
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        
        assert 'schema' in schema, \
            "Proposal schema must define schema structure"
    
    def test_governance_policy_exists(self):
        """
        Test that governance policy documents exist.
        
        Expected: MEMORY_WRITE_POLICY.md and LESSONS_TO_CANON_WORKFLOW.md exist
        """
        policy_path = os.path.join(
            project_root, 'memory', 'AUTHORITY', 'MEMORY_WRITE_POLICY.md'
        )
        workflow_path = os.path.join(
            project_root, 'memory', 'AUTHORITY', 'LESSONS_TO_CANON_WORKFLOW.md'
        )
        
        assert os.path.exists(policy_path), \
            "Memory write policy must exist"
        assert os.path.exists(workflow_path), \
            "Lessons to canon workflow must exist"
    
    def test_proposal_client_separate_from_memory_client(self):
        """
        Test that proposal client is separate from memory client.
        
        Expected: Proposal functions do not modify memory client behavior
        """
        # This is a structural test - ensure proposal client is separate module
        from python_agent import memory_proposal_client
        from python_agent import memory_client
        
        # Verify they are different modules
        assert memory_proposal_client != memory_client, \
            "Proposal client must be separate from memory client"
        
        # Verify proposal submission doesn't use memory append
        import inspect
        proposal_code = inspect.getsource(memory_proposal_client.submit_memory_proposal)
        
        # Should NOT call memory client's append_memory
        assert 'append_memory' not in proposal_code.lower(), \
            "Proposal submission must NOT call append_memory"


# Cleanup fixture
@pytest.fixture(autouse=True, scope='function')
def cleanup_test_proposals():
    """Clean up test proposals after each test"""
    yield
    
    # Clean up test proposals
    proposals_dir = os.path.join(project_root, 'memory', 'proposals', 'pending')
    if os.path.exists(proposals_dir):
        for file in os.listdir(proposals_dir):
            if file.startswith('prop-') and file.endswith('.json'):
                file_path = os.path.join(proposals_dir, file)
                try:
                    # Only delete test proposals
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        if data.get('proposed_by') == 'test-agent':
                            os.remove(file_path)
                except Exception:
                    pass
