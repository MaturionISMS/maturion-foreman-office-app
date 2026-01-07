"""
Test Category 2: Governance Supremacy

Tests for:
- Architecture freeze enforcement
- QA bypass prevention

These tests validate that governance rules are enforced absolutely,
with no exceptions or bypasses.

Expected: All tests RED (failing) until implementation exists.
"""

import pytest
from pathlib import Path


@pytest.mark.governance
@pytest.mark.wave0
class TestArchitectureFreezeEnforcement:
    """Test architecture freeze enforcement during build"""
    
    def test_architecture_cannot_be_modified_during_build(self):
        """
        Test that architecture files cannot be modified once build starts.
        
        Expected to FAIL: No architecture freeze enforcement implemented yet.
        """
        from foreman.governance.architecture_freeze import ArchitectureFreezeManager
        from foreman.governance.build_state import BuildStateManager
        
        freeze_manager = ArchitectureFreezeManager()
        build_state = BuildStateManager()
        
        # Define architecture path
        arch_path = Path("foreman/architecture/test-module-architecture.md")
        
        # Start build - this should freeze architecture
        build_state.start_build(architecture_path=arch_path)
        
        # Attempt to modify architecture should be blocked
        with pytest.raises(Exception) as exc_info:
            freeze_manager.modify_architecture(arch_path, "new content")
        
        assert "Architecture is frozen" in str(exc_info.value), \
            "Modification attempt must be blocked with clear error message"
        
        build_state.complete_build()
    
    def test_architecture_freeze_applies_to_all_related_files(self):
        """
        Test that architecture freeze applies to all related architectural files.
        
        Expected to FAIL: No comprehensive freeze system implemented yet.
        """
        from foreman.governance.architecture_freeze import ArchitectureFreezeManager
        from foreman.governance.build_state import BuildStateManager
        
        freeze_manager = ArchitectureFreezeManager()
        build_state = BuildStateManager()
        
        # Define related architecture files
        main_arch = Path("foreman/architecture/module-architecture.md")
        true_north = Path("foreman/architecture/module-true-north.md")
        integration = Path("foreman/architecture/module-integrations.md")
        
        # Start build
        build_state.start_build(
            architecture_path=main_arch,
            related_paths=[true_north, integration]
        )
        
        # All related files should be frozen
        for path in [main_arch, true_north, integration]:
            with pytest.raises(Exception) as exc_info:
                freeze_manager.modify_architecture(path, "new content")
            
            assert "frozen" in str(exc_info.value).lower(), \
                f"All related architecture files must be frozen: {path}"
        
        build_state.complete_build()
    
    def test_architecture_freeze_released_after_build_completion(self):
        """
        Test that architecture freeze is released after build completes.
        
        Expected to FAIL: No freeze lifecycle management implemented yet.
        """
        from foreman.governance.architecture_freeze import ArchitectureFreezeManager
        from foreman.governance.build_state import BuildStateManager
        
        freeze_manager = ArchitectureFreezeManager()
        build_state = BuildStateManager()
        
        arch_path = Path("foreman/architecture/test-module-architecture.md")
        
        # Start and complete build
        build_state.start_build(architecture_path=arch_path)
        build_state.complete_build()
        
        # Architecture should now be modifiable
        try:
            freeze_manager.modify_architecture(arch_path, "new content")
            modification_allowed = True
        except Exception:
            modification_allowed = False
        
        assert modification_allowed, \
            "Architecture must be modifiable after build completes"
    
    def test_architecture_freeze_logs_violation_attempts(self):
        """
        Test that attempts to violate architecture freeze are logged.
        
        Expected to FAIL: No violation logging implemented yet.
        """
        from foreman.governance.architecture_freeze import ArchitectureFreezeManager
        from foreman.governance.build_state import BuildStateManager
        
        freeze_manager = ArchitectureFreezeManager()
        build_state = BuildStateManager()
        
        arch_path = Path("foreman/architecture/test-module-architecture.md")
        
        # Start build
        build_state.start_build(architecture_path=arch_path)
        
        # Attempt modification
        try:
            freeze_manager.modify_architecture(arch_path, "new content")
        except Exception:
            pass  # Expected to fail
        
        # Check violation log
        violations = freeze_manager.get_violation_log()
        
        assert len(violations) > 0, "Violation attempts must be logged"
        assert violations[0]['file_path'] == str(arch_path), \
            "Violation log must include file path"
        assert violations[0]['attempted_action'] == 'modify', \
            "Violation log must include attempted action"
        assert 'timestamp' in violations[0], \
            "Violation log must include timestamp"
        
        build_state.complete_build()
    
    def test_architecture_freeze_blocks_cs2_without_approval(self):
        """
        Test that CS2 (Change Sequence 2) modifications require explicit approval.
        
        Expected to FAIL: No CS2 approval workflow implemented yet.
        """
        from foreman.governance.architecture_freeze import ArchitectureFreezeManager
        from foreman.governance.build_state import BuildStateManager
        from foreman.governance.cs2_approval import CS2ApprovalManager
        
        freeze_manager = ArchitectureFreezeManager()
        build_state = BuildStateManager()
        cs2_manager = CS2ApprovalManager()
        
        arch_path = Path("foreman/architecture/test-module-architecture.md")
        
        # Start build
        build_state.start_build(architecture_path=arch_path)
        
        # CS2 request without approval should be blocked
        cs2_request_id = cs2_manager.request_architecture_change(
            architecture_path=arch_path,
            reason="Critical bug fix needed",
            requester="builder-agent"
        )
        
        assert cs2_manager.get_approval_status(cs2_request_id) == "pending", \
            "CS2 request should be pending approval"
        
        with pytest.raises(Exception) as exc_info:
            freeze_manager.modify_architecture(
                arch_path, 
                "new content",
                cs2_request_id=cs2_request_id
            )
        
        assert "not approved" in str(exc_info.value).lower(), \
            "CS2 modification without approval must be blocked"
        
        build_state.complete_build()


@pytest.mark.governance
@pytest.mark.wave0
class TestQABypassPrevention:
    """Test QA bypass prevention mechanisms"""
    
    def test_cannot_mark_task_complete_with_failing_tests(self):
        """
        Test that tasks cannot be marked complete if QA tests are failing.
        
        Expected to FAIL: No QA enforcement implemented yet.
        """
        from foreman.governance.qa_enforcement import QAEnforcementManager
        from foreman.governance.task_completion import TaskCompletionValidator
        
        qa_enforcer = QAEnforcementManager()
        task_validator = TaskCompletionValidator(qa_enforcer=qa_enforcer)
        
        # Simulate task with failing tests
        task_id = "task-001"
        qa_results = {
            'total_tests': 10,
            'passing_tests': 8,
            'failing_tests': 2,
            'status': 'RED'
        }
        
        # Attempt to complete task should be blocked
        with pytest.raises(Exception) as exc_info:
            task_validator.validate_completion(task_id, qa_results)
        
        assert "QA tests failing" in str(exc_info.value), \
            "Task completion must be blocked when tests are failing"
        assert "100% pass required" in str(exc_info.value), \
            "Error must explicitly state 100% pass requirement"
    
    def test_99_percent_pass_rate_is_failure(self):
        """
        Test that 99% pass rate is treated as complete failure (GSR enforcement).
        
        Expected to FAIL: No strict QA enforcement implemented yet.
        """
        from foreman.governance.qa_enforcement import QAEnforcementManager
        from foreman.governance.task_completion import TaskCompletionValidator
        
        qa_enforcer = QAEnforcementManager()
        task_validator = TaskCompletionValidator(qa_enforcer=qa_enforcer)
        
        # 99% pass rate (301/303 tests passing)
        task_id = "task-002"
        qa_results = {
            'total_tests': 303,
            'passing_tests': 301,
            'failing_tests': 2,
            'status': 'RED',
            'pass_rate': 0.993  # 99.3%
        }
        
        # Must be blocked despite high pass rate
        with pytest.raises(Exception) as exc_info:
            task_validator.validate_completion(task_id, qa_results)
        
        assert "100%" in str(exc_info.value), \
            "Error must emphasize 100% requirement"
        assert "2 tests failing" in str(exc_info.value) or "2 failing" in str(exc_info.value), \
            "Error must state exact number of failing tests"
    
    def test_cannot_skip_qa_validation_step(self):
        """
        Test that QA validation cannot be skipped in task completion workflow.
        
        Expected to FAIL: No mandatory QA validation implemented yet.
        """
        from foreman.governance.task_completion import TaskCompletionValidator
        
        task_validator = TaskCompletionValidator()
        
        task_id = "task-003"
        
        # Attempt to complete without QA results should be blocked
        with pytest.raises(Exception) as exc_info:
            task_validator.validate_completion(task_id, qa_results=None)
        
        assert "QA validation required" in str(exc_info.value), \
            "Completion without QA must be explicitly blocked"
    
    def test_test_debt_blocks_completion(self):
        """
        Test that any test debt (skipped tests, TODOs) blocks task completion.
        
        Expected to FAIL: No test debt detection implemented yet.
        """
        from foreman.governance.qa_enforcement import QAEnforcementManager
        from foreman.governance.task_completion import TaskCompletionValidator
        
        qa_enforcer = QAEnforcementManager()
        task_validator = TaskCompletionValidator(qa_enforcer=qa_enforcer)
        
        task_id = "task-004"
        
        # All tests passing but has test debt
        qa_results = {
            'total_tests': 10,
            'passing_tests': 10,
            'failing_tests': 0,
            'skipped_tests': 2,  # Test debt!
            'status': 'GREEN',
            'test_debt': True
        }
        
        # Must be blocked due to test debt
        with pytest.raises(Exception) as exc_info:
            task_validator.validate_completion(task_id, qa_results)
        
        assert "test debt" in str(exc_info.value).lower(), \
            "Error must explicitly mention test debt"
        assert "skipped" in str(exc_info.value).lower() or "2" in str(exc_info.value), \
            "Error must identify the test debt type"
    
    def test_qa_bypass_attempts_are_logged_to_governance_memory(self):
        """
        Test that attempts to bypass QA are logged to governance memory.
        
        Expected to FAIL: No governance memory logging implemented yet.
        """
        from foreman.governance.qa_enforcement import QAEnforcementManager
        from foreman.governance.task_completion import TaskCompletionValidator
        from foreman.governance.memory import GovernanceMemoryLogger
        
        qa_enforcer = QAEnforcementManager()
        task_validator = TaskCompletionValidator(qa_enforcer=qa_enforcer)
        memory_logger = GovernanceMemoryLogger()
        
        task_id = "task-005"
        
        # Attempt completion with failing tests
        qa_results = {
            'total_tests': 10,
            'passing_tests': 7,
            'failing_tests': 3,
            'status': 'RED'
        }
        
        try:
            task_validator.validate_completion(task_id, qa_results)
        except Exception:
            pass  # Expected to fail
        
        # Check governance memory
        memory_entries = memory_logger.query(
            scope='governance',
            tags=['qa-bypass-attempt']
        )
        
        assert len(memory_entries) > 0, \
            "QA bypass attempts must be logged to governance memory"
        assert memory_entries[0]['task_id'] == task_id, \
            "Memory entry must include task ID"
        assert memory_entries[0]['failing_tests'] == 3, \
            "Memory entry must include number of failing tests"
    
    def test_qa_enforcement_applies_to_all_builder_types(self):
        """
        Test that QA enforcement applies equally to all builder types.
        
        Expected to FAIL: No universal QA enforcement implemented yet.
        """
        from foreman.governance.qa_enforcement import QAEnforcementManager
        from foreman.governance.task_completion import TaskCompletionValidator
        
        qa_enforcer = QAEnforcementManager()
        task_validator = TaskCompletionValidator(qa_enforcer=qa_enforcer)
        
        # Test with different builder types
        builder_types = ['ui-builder', 'api-builder', 'schema-builder', 'integration-builder']
        
        qa_results = {
            'total_tests': 10,
            'passing_tests': 9,
            'failing_tests': 1,
            'status': 'RED'
        }
        
        for builder_type in builder_types:
            task_id = f"task-{builder_type}"
            
            with pytest.raises(Exception) as exc_info:
                task_validator.validate_completion(
                    task_id, 
                    qa_results,
                    builder_type=builder_type
                )
            
            # All should be blocked equally
            assert "100% pass required" in str(exc_info.value) or "QA" in str(exc_info.value), \
                f"QA enforcement must apply to {builder_type}"
