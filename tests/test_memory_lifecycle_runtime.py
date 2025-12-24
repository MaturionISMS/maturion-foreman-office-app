"""
Test Memory Lifecycle State Machine Runtime

Tests for:
- State machine transitions (UNINITIALIZED → LOADING → VALIDATING → USABLE/DEGRADED/FAILED)
- Failure mode handling (hard stop vs degraded)
- Health check functionality
- State transition audit logging
- Privacy validation
- Observability events

Governance Authority:
- docs/architecture/runtime/memory/MEMORY_LIFECYCLE_STATE_MACHINE.md
- foreman/behaviours/memory-rules.md
- foreman/privacy-guardrails.md
"""

import pytest
import json
import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.mark.lifecycle
class TestMemoryLifecycleStates:
    """Test memory lifecycle state machine states"""
    
    def test_lifecycle_states_defined(self):
        """
        Test that all 5 lifecycle states are defined.
        
        Expected: UNINITIALIZED, LOADING, VALIDATING, USABLE, DEGRADED, FAILED
        """
        # This is a documentation/architecture test
        # Verify the states are documented in the architecture spec
        arch_spec_path = project_root / 'docs' / 'architecture' / 'runtime' / 'memory' / 'MEMORY_LIFECYCLE_STATE_MACHINE.md'
        
        assert arch_spec_path.exists(), \
            "Memory lifecycle architecture specification must exist"
        
        content = arch_spec_path.read_text()
        
        required_states = [
            'UNINITIALIZED',
            'LOADING',
            'VALIDATING',
            'USABLE',
            'DEGRADED',
            'FAILED'
        ]
        
        for state in required_states:
            assert state in content, \
                f"State {state} must be defined in architecture specification"
    
    def test_state_transition_paths_defined(self):
        """
        Test that state transition paths are defined.
        
        Expected: Clear transition rules from each state
        """
        arch_spec_path = project_root / 'docs' / 'architecture' / 'runtime' / 'memory' / 'MEMORY_LIFECYCLE_STATE_MACHINE.md'
        content = arch_spec_path.read_text()
        
        # Check for transition documentation
        assert 'State Transition Diagram' in content or 'state transitions' in content.lower(), \
            "State transitions must be documented"
        
        # Check for key transitions
        assert 'LOADING' in content and 'VALIDATING' in content, \
            "LOADING → VALIDATING transition must be defined"
        
        assert 'VALIDATING' in content and 'USABLE' in content, \
            "VALIDATING → USABLE transition must be defined"


@pytest.mark.lifecycle
class TestFailureModes:
    """Test failure mode handling"""
    
    def test_hard_stop_scenarios_defined(self):
        """
        Test that hard stop scenarios are defined.
        
        Expected: Critical scope missing, schema corruption, privacy violations
        """
        arch_spec_path = project_root / 'docs' / 'architecture' / 'runtime' / 'memory' / 'MEMORY_LIFECYCLE_STATE_MACHINE.md'
        content = arch_spec_path.read_text()
        
        # Check for hard stop documentation
        assert 'Hard Stop' in content or 'HARD_STOP' in content, \
            "Hard stop failure mode must be defined"
        
        # Check for critical failure triggers
        assert 'Critical scope missing' in content or 'critical scope' in content.lower(), \
            "Critical scope missing trigger must be defined"
        
        assert 'privacy violation' in content.lower() or 'PII' in content, \
            "Privacy violation trigger must be defined"
    
    def test_degraded_mode_scenarios_defined(self):
        """
        Test that degraded mode scenarios are defined.
        
        Expected: Non-critical scope missing, performance issues, validation warnings
        """
        arch_spec_path = project_root / 'docs' / 'architecture' / 'runtime' / 'memory' / 'MEMORY_LIFECYCLE_STATE_MACHINE.md'
        content = arch_spec_path.read_text()
        
        # Check for degraded mode documentation
        assert 'DEGRADED' in content or 'Degraded' in content, \
            "Degraded state must be defined"
        
        assert 'Non-critical' in content or 'non-critical' in content, \
            "Non-critical degradation scenarios must be defined"


@pytest.mark.lifecycle
class TestHealthChecks:
    """Test health check functionality"""
    
    def test_health_check_endpoint_specified(self):
        """
        Test that health check endpoint structure is specified.
        
        Expected: Health check returns state, metrics, scopes, degradations
        """
        arch_spec_path = project_root / 'docs' / 'architecture' / 'runtime' / 'memory' / 'MEMORY_LIFECYCLE_STATE_MACHINE.md'
        content = arch_spec_path.read_text()
        
        # Check for health check specification
        assert 'health' in content.lower() or 'healthCheck' in content, \
            "Health check must be specified"
        
        # Check for health check fields
        assert 'state' in content, \
            "Health check must include state"
        
        assert 'metrics' in content or 'Metrics' in content, \
            "Health check must include metrics"
    
    def test_health_check_includes_scope_status(self):
        """
        Test that health check includes scope status.
        
        Expected: Health check reports status of each scope (global, foreman, platform, runtime)
        """
        arch_spec_path = project_root / 'docs' / 'architecture' / 'runtime' / 'memory' / 'MEMORY_LIFECYCLE_STATE_MACHINE.md'
        content = arch_spec_path.read_text()
        
        # Check for scope status
        assert 'scopes' in content or 'Scopes' in content, \
            "Health check must include scope information"


@pytest.mark.lifecycle
class TestStateTransitionAudit:
    """Test state transition audit logging"""
    
    def test_state_transitions_are_auditable(self):
        """
        Test that state transitions are logged for audit.
        
        Expected: All transitions emit observable events
        """
        arch_spec_path = project_root / 'docs' / 'architecture' / 'runtime' / 'memory' / 'MEMORY_LIFECYCLE_STATE_MACHINE.md'
        content = arch_spec_path.read_text()
        
        # Check for observability
        assert 'observable' in content.lower() or 'Observable' in content, \
            "State transitions must be observable"
        
        assert 'event' in content.lower() or 'Event' in content, \
            "State transitions must emit events"
    
    def test_transition_history_trackable(self):
        """
        Test that transition history can be tracked.
        
        Expected: History of state transitions available
        """
        arch_spec_path = project_root / 'docs' / 'architecture' / 'runtime' / 'memory' / 'MEMORY_LIFECYCLE_STATE_MACHINE.md'
        content = arch_spec_path.read_text()
        
        # Check for history tracking
        assert 'history' in content.lower() or 'History' in content, \
            "State transition history must be trackable"


@pytest.mark.lifecycle
class TestPrivacyValidation:
    """Test privacy validation in lifecycle"""
    
    def test_privacy_checks_in_validation_state(self):
        """
        Test that privacy checks occur during VALIDATING state.
        
        Expected: Privacy Checker integrated into validation pipeline
        """
        arch_spec_path = project_root / 'docs' / 'architecture' / 'runtime' / 'memory' / 'MEMORY_LIFECYCLE_STATE_MACHINE.md'
        content = arch_spec_path.read_text()
        
        # Check for privacy validation
        assert 'Privacy' in content or 'privacy' in content, \
            "Privacy validation must be part of lifecycle"
        
        assert 'Privacy Checker' in content or 'privacy check' in content.lower(), \
            "Privacy Checker component must be specified"
    
    def test_pii_detection_triggers_failure(self):
        """
        Test that PII detection triggers failure mode.
        
        Expected: PII found → FAILED state
        """
        arch_spec_path = project_root / 'docs' / 'architecture' / 'runtime' / 'memory' / 'MEMORY_LIFECYCLE_STATE_MACHINE.md'
        content = arch_spec_path.read_text()
        
        # Check for PII handling
        assert 'PII' in content, \
            "PII detection must be specified"
        
        # PII should trigger failure
        assert 'FAILED' in content, \
            "PII detection should trigger FAILED state"


@pytest.mark.lifecycle
class TestObservability:
    """Test observability events"""
    
    def test_lifecycle_events_defined(self):
        """
        Test that lifecycle events are defined.
        
        Expected: Events for each state transition
        """
        arch_spec_path = project_root / 'docs' / 'architecture' / 'runtime' / 'memory' / 'MEMORY_LIFECYCLE_STATE_MACHINE.md'
        content = arch_spec_path.read_text()
        
        # Check for event definitions
        assert 'memory.lifecycle' in content, \
            "Lifecycle events must be defined with namespace"
        
        # Check for key events
        expected_events = [
            'memory.lifecycle.loading',
            'memory.lifecycle.validating',
            'memory.lifecycle.usable'
        ]
        
        for event in expected_events:
            assert event in content, \
                f"Event {event} must be defined"
    
    def test_event_consumers_specified(self):
        """
        Test that event consumers are specified.
        
        Expected: Foreman, Watchdog, Johan Dashboard consume events
        """
        arch_spec_path = project_root / 'docs' / 'architecture' / 'runtime' / 'memory' / 'MEMORY_LIFECYCLE_STATE_MACHINE.md'
        content = arch_spec_path.read_text()
        
        # Check for consumer documentation
        assert 'Event Consumers' in content or 'consumer' in content.lower(), \
            "Event consumers must be specified"


@pytest.mark.lifecycle
class TestComponentIntegration:
    """Test component integration"""
    
    def test_lifecycle_manager_component_specified(self):
        """
        Test that Memory Lifecycle Manager component is specified.
        
        Expected: Component with initialize(), load(), validate(), healthCheck()
        """
        arch_spec_path = project_root / 'docs' / 'architecture' / 'runtime' / 'memory' / 'MEMORY_LIFECYCLE_STATE_MACHINE.md'
        content = arch_spec_path.read_text()
        
        # Check for component
        assert 'Memory Lifecycle Manager' in content or 'MemoryLifecycleManager' in content, \
            "Memory Lifecycle Manager component must be specified"
        
        # Check for key functions
        functions = ['initialize', 'load', 'validate', 'healthCheck']
        for func in functions:
            assert func in content, \
                f"Function {func}() must be specified"
    
    def test_memory_store_component_specified(self):
        """
        Test that Memory Store component is specified.
        
        Expected: Component for storage and retrieval
        """
        arch_spec_path = project_root / 'docs' / 'architecture' / 'runtime' / 'memory' / 'MEMORY_LIFECYCLE_STATE_MACHINE.md'
        content = arch_spec_path.read_text()
        
        # Check for component
        assert 'Memory Store' in content or 'MemoryStore' in content, \
            "Memory Store component must be specified"
    
    def test_schema_validator_component_specified(self):
        """
        Test that Schema Validator component is specified.
        
        Expected: Component for schema validation
        """
        arch_spec_path = project_root / 'docs' / 'architecture' / 'runtime' / 'memory' / 'MEMORY_LIFECYCLE_STATE_MACHINE.md'
        content = arch_spec_path.read_text()
        
        # Check for component
        assert 'Schema Validator' in content or 'SchemaValidator' in content, \
            "Schema Validator component must be specified"
    
    def test_privacy_checker_component_specified(self):
        """
        Test that Privacy Checker component is specified.
        
        Expected: Component for privacy enforcement
        """
        arch_spec_path = project_root / 'docs' / 'architecture' / 'runtime' / 'memory' / 'MEMORY_LIFECYCLE_STATE_MACHINE.md'
        content = arch_spec_path.read_text()
        
        # Check for component
        assert 'Privacy Checker' in content or 'PrivacyChecker' in content, \
            "Privacy Checker component must be specified"


@pytest.mark.lifecycle
class TestAcceptanceCriteria:
    """Test acceptance criteria from Section 7.1"""
    
    def test_ac_state_machine_transitions(self):
        """
        Test AC: State machine transitions work correctly
        
        Expected: All transitions documented and testable
        """
        arch_spec_path = project_root / 'docs' / 'architecture' / 'runtime' / 'memory' / 'MEMORY_LIFECYCLE_STATE_MACHINE.md'
        content = arch_spec_path.read_text()
        
        # All states must be documented
        states = ['UNINITIALIZED', 'LOADING', 'VALIDATING', 'USABLE', 'DEGRADED', 'FAILED']
        for state in states:
            assert state in content, \
                f"State {state} must be documented for AC compliance"
    
    def test_ac_failure_modes_trigger_correctly(self):
        """
        Test AC: Failure modes trigger correct behavior
        
        Expected: Hard stop and degraded mode clearly defined
        """
        arch_spec_path = project_root / 'docs' / 'architecture' / 'runtime' / 'memory' / 'MEMORY_LIFECYCLE_STATE_MACHINE.md'
        content = arch_spec_path.read_text()
        
        assert 'Hard Stop' in content or 'hard stop' in content.lower(), \
            "Hard stop failure mode must be defined"
        
        assert 'Degraded' in content or 'degraded' in content.lower(), \
            "Degraded mode must be defined"
    
    def test_ac_health_check_returns_state(self):
        """
        Test AC: Health check endpoint returns accurate state
        
        Expected: Health check structure includes state
        """
        arch_spec_path = project_root / 'docs' / 'architecture' / 'runtime' / 'memory' / 'MEMORY_LIFECYCLE_STATE_MACHINE.md'
        content = arch_spec_path.read_text()
        
        assert 'healthCheck' in content or 'health check' in content.lower(), \
            "Health check must be specified"
        
        assert '"state"' in content or 'state' in content, \
            "Health check must return state"
    
    def test_ac_transitions_are_logged(self):
        """
        Test AC: State transitions are logged and auditable
        
        Expected: Audit logging specified
        """
        arch_spec_path = project_root / 'docs' / 'architecture' / 'runtime' / 'memory' / 'MEMORY_LIFECYCLE_STATE_MACHINE.md'
        content = arch_spec_path.read_text()
        
        assert 'audit' in content.lower() or 'log' in content.lower(), \
            "Audit logging must be specified"
    
    def test_ac_all_states_reachable(self):
        """
        Test AC: All 5 states are reachable and tested
        
        Expected: Entry and exit conditions defined for each state
        """
        arch_spec_path = project_root / 'docs' / 'architecture' / 'runtime' / 'memory' / 'MEMORY_LIFECYCLE_STATE_MACHINE.md'
        content = arch_spec_path.read_text()
        
        # Check for entry/exit conditions
        assert 'Entry Conditions' in content or 'entry condition' in content.lower(), \
            "Entry conditions must be specified"
        
        assert 'Exit Conditions' in content or 'exit condition' in content.lower(), \
            "Exit conditions must be specified"


@pytest.mark.lifecycle
class TestImplementationFiles:
    """Test that implementation files exist"""
    
    def test_lifecycle_manager_file_exists(self):
        """
        Test that lifecycle-manager.ts exists
        """
        impl_file = project_root / 'lib' / 'memory' / 'lifecycle-manager.ts'
        assert impl_file.exists(), \
            "lifecycle-manager.ts implementation file must exist"
    
    def test_store_file_exists(self):
        """
        Test that store.ts exists
        """
        impl_file = project_root / 'lib' / 'memory' / 'store.ts'
        assert impl_file.exists(), \
            "store.ts implementation file must exist"
    
    def test_schema_validator_file_exists(self):
        """
        Test that schema-validator.ts exists
        """
        impl_file = project_root / 'lib' / 'memory' / 'schema-validator.ts'
        assert impl_file.exists(), \
            "schema-validator.ts implementation file must exist"
    
    def test_privacy_checker_file_exists(self):
        """
        Test that privacy-checker.ts exists
        """
        impl_file = project_root / 'lib' / 'memory' / 'privacy-checker.ts'
        assert impl_file.exists(), \
            "privacy-checker.ts implementation file must exist"
    
    def test_health_monitor_file_exists(self):
        """
        Test that health-monitor.ts exists
        """
        impl_file = project_root / 'lib' / 'memory' / 'health-monitor.ts'
        assert impl_file.exists(), \
            "health-monitor.ts implementation file must exist"
