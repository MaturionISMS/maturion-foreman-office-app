"""
QA-147 to QA-157: Global Memory Manager Tests

Tests for the Cross-Cutting Components - Global Memory Manager.

Architectural Reference:
- Component: CROSS-01 Memory Manager
- Location: FM_ARCHITECTURE_SPEC_V2_WIRING_COMPLETE.md
- QA Range: QA-147 to QA-157 (11 QA components)

Expected State: RED (intentionally failing until implementation exists)
"""

import pytest
from datetime import datetime
import json


@pytest.mark.cross_cutting
@pytest.mark.wave1_0
class TestGlobalMemoryManager:
    """Test suite for Global Memory Manager component (QA-147 to QA-157)"""
    
    def test_qa_147_initialize_memory_fabric(
        self,
        test_organisation_id,
        mock_memory_fabric,
        create_qa_evidence
    ):
        """
        QA-147: Initialize memory fabric
        
        Verify:
        - Directory structure creation
        - Schema validation
        - Seed data loading
        
        Expected: FAIL - No memory fabric initialization implemented yet
        """
        from foreman.cross_cutting.memory_manager import GlobalMemoryManager
        from foreman.cross_cutting.memory_schema import MemorySchemaValidator
        
        manager = GlobalMemoryManager(
            organisation_id=test_organisation_id,
            memory_path=mock_memory_fabric
        )
        
        # Initialize memory fabric
        result = manager.initialize_fabric()
        
        # Verify directory structure
        assert (mock_memory_fabric / "global").exists(), \
            "Global memory directory must be created"
        assert (mock_memory_fabric / "scoped").exists(), \
            "Scoped memory directory must be created"
        assert (mock_memory_fabric / "proposals").exists(), \
            "Proposals directory must be created"
        assert (mock_memory_fabric / "archive").exists(), \
            "Archive directory must be created"
        
        # Verify schema validation
        validator = MemorySchemaValidator()
        schema_valid = validator.validate_fabric_structure(mock_memory_fabric)
        
        assert schema_valid == True, \
            "Memory fabric structure must pass schema validation"
        
        # Verify seed data
        seed_file = mock_memory_fabric / "global" / "seed.json"
        assert seed_file.exists(), \
            "Seed data must be loaded"
        
        seed_data = json.loads(seed_file.read_text())
        assert "version" in seed_data, \
            "Seed data must include version"
        assert "created_at" in seed_data, \
            "Seed data must include creation timestamp"
        
        # Create evidence artifact
        evidence = create_qa_evidence(
            "QA-147",
            "PASS",
            {
                "fabric_initialized": result["success"],
                "directories_created": result["directories_created"],
                "schema_valid": schema_valid
            }
        )
    
    def test_qa_148_read_memory_entries(
        self,
        test_organisation_id,
        mock_memory_fabric,
        create_qa_evidence
    ):
        """
        QA-148: Read memory entries
        
        Verify:
        - Query by key
        - Query by category
        - Full-text search
        
        Expected: FAIL - No memory reading implemented yet
        """
        from foreman.cross_cutting.memory_manager import GlobalMemoryManager
        
        manager = GlobalMemoryManager(
            organisation_id=test_organisation_id,
            memory_path=mock_memory_fabric
        )
        manager.initialize_fabric()
        
        # Write test memories
        manager.write_memory(
            key="build_philosophy",
            category="governance",
            content="One-Time Build Correctness is paramount",
            organisation_id=test_organisation_id
        )
        
        manager.write_memory(
            key="qa_standards",
            category="governance",
            content="Zero Test Debt policy is enforced",
            organisation_id=test_organisation_id
        )
        
        manager.write_memory(
            key="architecture_pattern",
            category="architecture",
            content="Components must have explicit contracts",
            organisation_id=test_organisation_id
        )
        
        # Test query by key
        result = manager.read_memory(key="build_philosophy")
        
        assert result is not None, \
            "Memory read by key must return result"
        assert result["content"] == "One-Time Build Correctness is paramount", \
            "Memory content must match"
        assert result["category"] == "governance", \
            "Memory category must match"
        
        # Test query by category
        governance_memories = manager.read_by_category(category="governance")
        
        assert len(governance_memories) == 2, \
            "Should find 2 governance memories"
        assert all(m["category"] == "governance" for m in governance_memories), \
            "All results must be from governance category"
        
        # Test full-text search
        search_results = manager.search_memory(query="Test Debt")
        
        assert len(search_results) > 0, \
            "Full-text search should find matching memories"
        assert any("Test Debt" in r["content"] for r in search_results), \
            "Search results must contain query text"
        
        # Create evidence artifact
        evidence = create_qa_evidence(
            "QA-148",
            "PASS",
            {
                "read_by_key_successful": result is not None,
                "category_query_count": len(governance_memories),
                "search_results_count": len(search_results)
            }
        )
    
    def test_qa_149_generate_memory_write_proposal(
        self,
        test_organisation_id,
        test_user_id,
        create_qa_evidence
    ):
        """
        QA-149: Generate memory write proposal
        
        Verify:
        - Proposal format
        - Rationale capture
        - Provenance tracking
        
        Expected: FAIL - No memory write proposals implemented yet
        """
        from foreman.cross_cutting.memory_manager import GlobalMemoryManager
        from foreman.cross_cutting.memory_proposal import MemoryWriteProposal
        
        manager = GlobalMemoryManager(organisation_id=test_organisation_id)
        
        # Generate write proposal
        proposal = manager.create_write_proposal(
            key="new_governance_rule",
            category="governance",
            content="All builders must validate before merge",
            rationale="Prevents broken builds from reaching main branch",
            author=test_user_id,
            source="governance_review_2026_01"
        )
        
        # Verify proposal format
        assert isinstance(proposal, MemoryWriteProposal), \
            "Proposal must be MemoryWriteProposal instance"
        
        assert proposal.proposal_id is not None, \
            "Proposal must have unique ID"
        assert proposal.status == "PENDING", \
            "New proposal must have PENDING status"
        
        # Verify rationale capture
        assert proposal.rationale == "Prevents broken builds from reaching main branch", \
            "Proposal must capture rationale"
        assert len(proposal.rationale) > 0, \
            "Rationale must not be empty"
        
        # Verify provenance tracking
        assert proposal.author == test_user_id, \
            "Proposal must track author"
        assert proposal.source == "governance_review_2026_01", \
            "Proposal must track source"
        assert proposal.created_at is not None, \
            "Proposal must track creation timestamp"
        
        # Verify proposal can be serialized
        proposal_dict = proposal.to_dict()
        assert "proposal_id" in proposal_dict, \
            "Serialized proposal must include ID"
        assert "content" in proposal_dict, \
            "Serialized proposal must include content"
        assert "rationale" in proposal_dict, \
            "Serialized proposal must include rationale"
        
        # Create evidence artifact
        evidence = create_qa_evidence(
            "QA-149",
            "PASS",
            {
                "proposal_id": proposal.proposal_id,
                "proposal_status": proposal.status,
                "rationale_captured": len(proposal.rationale) > 0
            }
        )
    
    def test_qa_150_execute_approved_write(
        self,
        test_organisation_id,
        test_user_id,
        mock_memory_fabric,
        create_qa_evidence
    ):
        """
        QA-150: Execute approved write
        
        Verify:
        - Write only on approval
        - Immutability after write
        - Audit log entry
        
        Expected: FAIL - No approved write execution implemented yet
        """
        from foreman.cross_cutting.memory_manager import GlobalMemoryManager
        
        manager = GlobalMemoryManager(
            organisation_id=test_organisation_id,
            memory_path=mock_memory_fabric
        )
        manager.initialize_fabric()
        
        # Create proposal
        proposal = manager.create_write_proposal(
            key="approved_rule",
            category="governance",
            content="Critical rule requiring approval",
            rationale="Ensures governance integrity",
            author=test_user_id
        )
        
        # Attempt write without approval - should fail
        try:
            manager.execute_write(proposal_id=proposal.proposal_id)
            assert False, "Write without approval should be rejected"
        except Exception as e:
            assert "not approved" in str(e).lower() or "pending" in str(e).lower(), \
                "Rejection should clearly state approval required"
        
        # Approve proposal
        manager.approve_proposal(
            proposal_id=proposal.proposal_id,
            approver=test_user_id
        )
        
        # Execute approved write
        result = manager.execute_write(proposal_id=proposal.proposal_id)
        
        assert result["success"] == True, \
            "Approved write must succeed"
        assert result["memory_key"] == "approved_rule", \
            "Result must confirm memory key"
        
        # Verify write occurred
        memory = manager.read_memory(key="approved_rule")
        assert memory is not None, \
            "Memory must exist after approved write"
        assert memory["content"] == "Critical rule requiring approval", \
            "Memory content must match proposal"
        
        # Test immutability - attempt to modify
        try:
            manager.update_memory(
                key="approved_rule",
                content="Modified content"
            )
            assert False, "Memory modification should be prevented"
        except Exception as e:
            assert "immutable" in str(e).lower(), \
                "Immutability violation must be clearly stated"
        
        # Verify audit log
        audit_entries = manager.get_audit_log(key="approved_rule")
        assert len(audit_entries) > 0, \
            "Approved write must create audit log entry"
        
        audit_entry = audit_entries[0]
        assert audit_entry["action"] == "WRITE", \
            "Audit entry must record WRITE action"
        assert audit_entry["proposal_id"] == proposal.proposal_id, \
            "Audit entry must reference proposal"
        assert audit_entry["approver"] == test_user_id, \
            "Audit entry must record approver"
        
        # Create evidence artifact
        evidence = create_qa_evidence(
            "QA-150",
            "PASS",
            {
                "approval_enforced": True,
                "write_successful": result["success"],
                "immutability_enforced": True,
                "audit_logged": len(audit_entries) > 0
            }
        )
    
    def test_qa_151_memory_versioning(
        self,
        test_organisation_id,
        mock_memory_fabric,
        create_qa_evidence
    ):
        """
        QA-151: Memory versioning
        
        Verify:
        - Version tracking
        - History preservation
        - Rollback capability
        
        Expected: FAIL - No memory versioning implemented yet
        """
        from foreman.cross_cutting.memory_manager import GlobalMemoryManager
        
        manager = GlobalMemoryManager(
            organisation_id=test_organisation_id,
            memory_path=mock_memory_fabric
        )
        manager.initialize_fabric()
        
        # Create initial memory (version 1)
        manager.write_memory(
            key="versioned_rule",
            category="governance",
            content="Initial version of rule",
            organisation_id=test_organisation_id,
            version=1
        )
        
        # Update memory (version 2)
        manager.write_memory_version(
            key="versioned_rule",
            content="Updated version of rule",
            organisation_id=test_organisation_id,
            previous_version=1
        )
        
        # Update again (version 3)
        manager.write_memory_version(
            key="versioned_rule",
            content="Third version of rule",
            organisation_id=test_organisation_id,
            previous_version=2
        )
        
        # Verify version tracking
        current = manager.read_memory(key="versioned_rule")
        assert current["version"] == 3, \
            "Current version should be 3"
        assert current["content"] == "Third version of rule", \
            "Current content should match latest version"
        
        # Verify history preservation
        history = manager.get_memory_history(key="versioned_rule")
        
        assert len(history) == 3, \
            "History should include all 3 versions"
        assert history[0]["version"] == 1, \
            "History should start with version 1"
        assert history[2]["version"] == 3, \
            "History should end with version 3"
        
        # Verify all versions are preserved
        version_1 = manager.read_memory(key="versioned_rule", version=1)
        assert version_1["content"] == "Initial version of rule", \
            "Version 1 content must be preserved"
        
        version_2 = manager.read_memory(key="versioned_rule", version=2)
        assert version_2["content"] == "Updated version of rule", \
            "Version 2 content must be preserved"
        
        # Test rollback capability
        rollback_result = manager.rollback_memory(
            key="versioned_rule",
            to_version=1
        )
        
        assert rollback_result["success"] == True, \
            "Rollback must succeed"
        
        current_after_rollback = manager.read_memory(key="versioned_rule")
        assert current_after_rollback["content"] == "Initial version of rule", \
            "Content should match rollback target"
        assert current_after_rollback["version"] > 3, \
            "Rollback should create new version (not overwrite)"
        
        # Create evidence artifact
        evidence = create_qa_evidence(
            "QA-151",
            "PASS",
            {
                "versions_tracked": len(history),
                "history_preserved": True,
                "rollback_successful": rollback_result["success"]
            }
        )
    
    def test_qa_152_memory_manager_failure_modes(
        self,
        test_organisation_id,
        mock_memory_fabric,
        create_qa_evidence
    ):
        """
        QA-152: Memory Manager failure modes
        
        Verify:
        - Fabric corruption detection/recovery
        - Write proposal rejection handling
        
        Expected: FAIL - No failure mode handling implemented yet
        """
        from foreman.cross_cutting.memory_manager import GlobalMemoryManager
        from foreman.cross_cutting.memory_exceptions import (
            FabricCorruptionError,
            ProposalRejectedError
        )
        
        manager = GlobalMemoryManager(
            organisation_id=test_organisation_id,
            memory_path=mock_memory_fabric
        )
        manager.initialize_fabric()
        
        # Test fabric corruption detection
        try:
            # Simulate corruption by writing invalid JSON
            corrupted_file = mock_memory_fabric / "global" / "corrupted.json"
            corrupted_file.write_text("{ invalid json")
            
            # Attempt to read corrupted memory
            manager.read_memory(key="corrupted")
            
            # Should detect corruption
            assert False, "Corrupted memory should raise FabricCorruptionError"
        except FabricCorruptionError as e:
            # Verify corruption is detected
            assert "corruption" in str(e).lower(), \
                "Error must indicate corruption"
            
            # Verify recovery mechanism
            recovery_result = manager.recover_from_corruption(
                key="corrupted"
            )
            assert recovery_result["recovered"] == True or recovery_result["quarantined"] == True, \
                "Corruption should be recoverable or quarantined"
        
        # Test write proposal rejection
        try:
            # Create proposal
            proposal = manager.create_write_proposal(
                key="rejected_rule",
                category="governance",
                content="Rule to be rejected",
                rationale="Test rejection handling",
                author="test-user"
            )
            
            # Reject proposal
            manager.reject_proposal(
                proposal_id=proposal.proposal_id,
                rejector="admin",
                reason="Does not meet governance standards"
            )
            
            # Attempt to execute rejected proposal
            manager.execute_write(proposal_id=proposal.proposal_id)
            
            # Should not reach here
            assert False, "Rejected proposal execution should raise ProposalRejectedError"
        except ProposalRejectedError as e:
            # Verify rejection is handled
            assert "rejected" in str(e).lower(), \
                "Error must indicate rejection"
            assert hasattr(e, 'reason'), \
                "Rejection error should include reason"
            assert e.reason == "Does not meet governance standards", \
                "Rejection reason must be preserved"
        
        # Verify manager remains operational after failures
        manager.write_memory(
            key="recovery_test",
            category="test",
            content="Manager operational after failures",
            organisation_id=test_organisation_id
        )
        
        recovery_memory = manager.read_memory(key="recovery_test")
        assert recovery_memory is not None, \
            "Manager should remain operational after handling failures"
        
        # Create evidence artifact
        evidence = create_qa_evidence(
            "QA-152",
            "PASS",
            {
                "corruption_detected": True,
                "corruption_handled": True,
                "rejection_handled": True,
                "manager_recovery": True
            }
        )
    
    def test_qa_153_memory_consistency_validation(
        self,
        test_organisation_id,
        mock_memory_fabric,
        create_qa_evidence
    ):
        """
        QA-153: Memory consistency validation (Additional coverage for QA-147 to QA-157)
        
        Verify:
        - Cross-reference validation
        - Consistency checks
        - Conflict detection
        
        Expected: FAIL - No consistency validation implemented yet
        """
        from foreman.cross_cutting.memory_manager import GlobalMemoryManager
        from foreman.cross_cutting.memory_validator import MemoryConsistencyValidator
        
        manager = GlobalMemoryManager(
            organisation_id=test_organisation_id,
            memory_path=mock_memory_fabric
        )
        manager.initialize_fabric()
        validator = MemoryConsistencyValidator(manager)
        
        # Write related memories
        manager.write_memory(
            key="rule_a",
            category="governance",
            content="Rule A requires condition X",
            organisation_id=test_organisation_id,
            references=["rule_b"]
        )
        
        manager.write_memory(
            key="rule_b",
            category="governance",
            content="Rule B provides condition X",
            organisation_id=test_organisation_id
        )
        
        # Validate consistency
        validation_result = validator.validate_consistency()
        
        assert validation_result["consistent"] == True, \
            "Related memories should be consistent"
        assert len(validation_result["issues"]) == 0, \
            "No consistency issues should be found"
        
        # Test conflict detection - write conflicting memory
        manager.write_memory(
            key="rule_c",
            category="governance",
            content="Rule C contradicts condition X",
            organisation_id=test_organisation_id,
            conflicts_with=["rule_a", "rule_b"]
        )
        
        # Validate again
        validation_result = validator.validate_consistency()
        
        assert len(validation_result["conflicts"]) > 0, \
            "Conflict should be detected"
        
        conflict = validation_result["conflicts"][0]
        assert "rule_c" in conflict["involved_keys"], \
            "Conflict should reference rule_c"
        assert conflict["severity"] in ["HIGH", "MEDIUM", "LOW"], \
            "Conflict must have severity rating"
        
        # Create evidence artifact
        evidence = create_qa_evidence(
            "QA-153",
            "PASS",
            {
                "consistency_validated": True,
                "conflicts_detected": len(validation_result["conflicts"]),
                "validation_performed": True
            }
        )
    
    def test_qa_154_memory_isolation(
        self,
        test_organisation_id,
        mock_memory_fabric,
        create_qa_evidence
    ):
        """
        QA-154: Memory isolation (organisation_id boundary enforcement)
        
        Verify:
        - Tenant isolation is enforced
        - Cross-tenant access is prevented
        - Organisation_id is always required
        
        Expected: FAIL - No tenant isolation implemented yet
        """
        from foreman.cross_cutting.memory_manager import GlobalMemoryManager
        
        org1_id = test_organisation_id
        org2_id = "test-org-002"
        
        manager1 = GlobalMemoryManager(
            organisation_id=org1_id,
            memory_path=mock_memory_fabric
        )
        manager1.initialize_fabric()
        
        manager2 = GlobalMemoryManager(
            organisation_id=org2_id,
            memory_path=mock_memory_fabric
        )
        
        # Write memory for org1
        manager1.write_memory(
            key="org1_secret",
            category="sensitive",
            content="Org 1 confidential data",
            organisation_id=org1_id
        )
        
        # Write memory for org2
        manager2.write_memory(
            key="org2_secret",
            category="sensitive",
            content="Org 2 confidential data",
            organisation_id=org2_id
        )
        
        # Verify org1 can read its own memory
        org1_memory = manager1.read_memory(key="org1_secret")
        assert org1_memory is not None, \
            "Organisation should be able to read its own memory"
        assert org1_memory["content"] == "Org 1 confidential data", \
            "Content should match"
        
        # Verify org1 CANNOT read org2's memory
        try:
            org2_from_org1 = manager1.read_memory(key="org2_secret")
            # If returned, should be None or error
            assert org2_from_org1 is None, \
                "Organisation should not access another org's memory"
        except PermissionError:
            # This is the expected behavior
            pass
        
        # Verify org2 can read its own memory
        org2_memory = manager2.read_memory(key="org2_secret")
        assert org2_memory is not None, \
            "Organisation should be able to read its own memory"
        
        # Verify org2 CANNOT read org1's memory
        try:
            org1_from_org2 = manager2.read_memory(key="org1_secret")
            assert org1_from_org2 is None, \
                "Organisation should not access another org's memory"
        except PermissionError:
            # This is the expected behavior
            pass
        
        # Create evidence artifact
        evidence = create_qa_evidence(
            "QA-154",
            "PASS",
            {
                "tenant_isolation_enforced": True,
                "cross_tenant_access_prevented": True,
                "organisation_id_required": True
            }
        )
    
    # QA-155 to QA-157 would continue with additional memory manager edge cases
