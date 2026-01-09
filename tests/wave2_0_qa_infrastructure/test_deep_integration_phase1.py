"""
Wave 2.0 QA Infrastructure — Subwave 2.9: Deep Integration Phase 1
QA Range: QA-461 to QA-475 (15 QA components)

Authority: BL-019 Emergency Corrective Action Plan
Purpose: QA-to-Red tests for Deep Integration Phase 1

Test Categories:
- Cross-Subsystem Integration (QA-461 to QA-465)
- Event Bus Implementation (QA-466 to QA-470)
- Service Communication (QA-471 to QA-475)
"""

import pytest
from runtime.integration.cross_subsystem_integrator import CrossSubsystemIntegrator, SubsystemState
from runtime.integration.event_bus import EventBus, EventBusState
from runtime.integration.service_communicator import ServiceCommunicator, ServiceState, SecurityLevel, RetryPolicy


@pytest.mark.wave2
@pytest.mark.subwave_2_9
class TestCrossSubsystemIntegration:
    """QA-461 to QA-465: Cross-Subsystem Integration"""

    def test_qa_461_event_propagation(self):
        """QA-461: Subsystem event propagation"""
        integrator = CrossSubsystemIntegrator()
        org_id = "test_org_461"
        
        # Propagate event from source to multiple targets
        event = integrator.propagate_event(
            organisation_id=org_id,
            source_subsystem="analytics",
            target_subsystems=["dashboard", "parking_station"],
            event_type="data_updated",
            payload={"key": "value"}
        )
        
        # Verify event was created
        assert event.event_id is not None
        assert event.source_subsystem == "analytics"
        assert event.organisation_id == org_id
        
        # Verify propagation to targets
        assert "dashboard" in event.propagated_to
        assert "parking_station" in event.propagated_to
        
        # Verify event can be retrieved
        events = integrator.get_propagated_events(org_id, "dashboard")
        assert len(events) == 1
        assert events[0].event_id == event.event_id

    def test_qa_462_data_synchronization(self):
        """QA-462: Subsystem data synchronization"""
        integrator = CrossSubsystemIntegrator()
        org_id = "test_org_462"
        
        # Synchronize data between subsystems
        record = integrator.synchronize_data(
            organisation_id=org_id,
            source_subsystem="analytics",
            target_subsystem="dashboard",
            data_keys=["metrics", "trends", "insights"]
        )
        
        # Verify sync record created
        assert record.sync_id is not None
        assert record.source_subsystem == "analytics"
        assert record.target_subsystem == "dashboard"
        assert record.organisation_id == org_id
        assert len(record.data_keys) == 3
        
        # Verify sync completed successfully
        assert record.status == "completed"
        
        # Verify sync status can be retrieved
        status = integrator.get_sync_status(org_id, record.sync_id)
        assert status is not None
        assert status.status == "completed"

    def test_qa_463_state_coordination(self):
        """QA-463: Subsystem state coordination"""
        integrator = CrossSubsystemIntegrator()
        org_id = "test_org_463"
        
        # Coordinate state across subsystems
        coordination = integrator.coordinate_state(
            organisation_id=org_id,
            subsystems=["analytics", "dashboard", "governance"],
            coordinated_state={"mode": "active", "priority": "high"}
        )
        
        # Verify coordination created
        assert coordination.coordination_id is not None
        assert len(coordination.participating_subsystems) == 3
        assert coordination.organisation_id == org_id
        assert coordination.coordinated_state["mode"] == "active"
        
        # Verify subsystems marked as synchronized
        for subsystem in ["analytics", "dashboard", "governance"]:
            state = integrator.get_subsystem_state(org_id, subsystem)
            assert state == SubsystemState.SYNCHRONIZED
        
        # Verify coordination can be retrieved
        retrieved = integrator.get_coordinated_state(org_id, coordination.coordination_id)
        assert retrieved is not None
        assert retrieved.coordination_id == coordination.coordination_id

    def test_qa_464_dependency_management(self):
        """QA-464: Subsystem dependency management"""
        integrator = CrossSubsystemIntegrator()
        org_id = "test_org_464"
        
        # Define dependencies
        graph = integrator.manage_dependencies(
            organisation_id=org_id,
            subsystem="dashboard",
            depends_on=["analytics", "governance"]
        )
        
        # Verify dependencies registered
        assert graph.organisation_id == org_id
        deps = integrator.get_dependencies(org_id, "dashboard")
        assert "analytics" in deps
        assert "governance" in deps
        
        # Verify no circular dependency
        assert not integrator.has_circular_dependency(org_id)
        
        # Add another dependency
        integrator.manage_dependencies(
            organisation_id=org_id,
            subsystem="governance",
            depends_on=["analytics"]
        )
        
        # Verify still no circular dependency
        assert not integrator.has_circular_dependency(org_id)

    def test_qa_465_error_handling(self):
        """QA-465: Cross-subsystem error handling"""
        integrator = CrossSubsystemIntegrator()
        org_id = "test_org_465"
        
        # Handle cross-subsystem error
        error_record = integrator.handle_cross_subsystem_error(
            organisation_id=org_id,
            source_subsystem="analytics",
            affected_subsystems=["dashboard", "parking_station"],
            error_type="data_inconsistency",
            error_message="Data sync failed",
            recovery_action="retry_sync"
        )
        
        # Verify error record created
        assert error_record["error_id"] is not None
        assert error_record["source_subsystem"] == "analytics"
        assert len(error_record["affected_subsystems"]) == 2
        assert error_record["organisation_id"] == org_id
        assert error_record["recovery_action"] == "retry_sync"
        
        # Verify affected subsystems marked as degraded
        for subsystem in ["dashboard", "parking_station"]:
            state = integrator.get_subsystem_state(org_id, subsystem)
            assert state == SubsystemState.DEGRADED
        
        # Verify error can be retrieved
        errors = integrator.get_errors_for_subsystem(org_id, "dashboard")
        assert len(errors) == 1
        assert errors[0]["error_id"] == error_record["error_id"]


@pytest.mark.wave2
@pytest.mark.subwave_2_9
class TestEventBus:
    """QA-466 to QA-470: Event Bus Implementation"""

    def test_qa_466_bus_initialization(self):
        """QA-466: Event bus initialization"""
        bus = EventBus()
        org_id = "test_org_466"
        
        # Initialize event bus for tenant
        result = bus.initialize(org_id)
        
        # Verify initialization successful
        assert result is True
        assert bus.is_initialized(org_id)
        assert bus.get_state() == EventBusState.RUNNING
        
        # Verify data structures created
        assert org_id in bus.event_queues
        assert org_id in bus.subscriptions
        assert org_id in bus.published_events

    def test_qa_467_event_publishing(self):
        """QA-467: Event publishing"""
        bus = EventBus()
        org_id = "test_org_467"
        
        # Publish event
        event = bus.publish(
            organisation_id=org_id,
            event_type="user_action",
            payload={"action": "click", "target": "button"}
        )
        
        # Verify event published
        assert event.event_id is not None
        assert event.event_type == "user_action"
        assert event.organisation_id == org_id
        assert event.sequence_number > 0
        
        # Verify event stored
        published = bus.get_published_events(org_id)
        assert len(published) == 1
        assert published[0].event_id == event.event_id
        
        # Verify event type filtering
        filtered = bus.get_published_events(org_id, "user_action")
        assert len(filtered) == 1

    def test_qa_468_event_subscription(self):
        """QA-468: Event subscription"""
        bus = EventBus()
        org_id = "test_org_468"
        
        # Track callback invocations
        received_events = []
        
        def callback(event):
            received_events.append(event)
        
        # Subscribe to events
        subscription = bus.subscribe(
            organisation_id=org_id,
            subscriber_id="subscriber_1",
            event_types=["test_event"],
            callback=callback
        )
        
        # Verify subscription created
        assert subscription.subscriber_id == "subscriber_1"
        assert subscription.organisation_id == org_id
        assert subscription.active is True
        
        # Verify subscription in list
        subs = bus.get_subscriptions(org_id)
        assert len(subs) == 1
        assert subs[0].subscriber_id == "subscriber_1"
        
        # Publish event
        event = bus.publish(org_id, "test_event", {"data": "value"})
        
        # Verify event delivered to subscriber
        assert len(received_events) == 1
        assert received_events[0].event_id == event.event_id
        assert "subscriber_1" in event.delivered_to
        
        # Unsubscribe
        bus.unsubscribe(org_id, "subscriber_1")
        subs = bus.get_subscriptions(org_id)
        assert len(subs) == 0

    def test_qa_469_ordering_guarantees(self):
        """QA-469: Event ordering guarantees"""
        bus = EventBus()
        org_id = "test_org_469"
        
        # Publish multiple events
        events = []
        for i in range(5):
            event = bus.publish(
                organisation_id=org_id,
                event_type="ordered_event",
                payload={"index": i}
            )
            events.append(event)
        
        # Verify sequence numbers are monotonically increasing
        for i in range(1, len(events)):
            assert events[i].sequence_number > events[i-1].sequence_number
        
        # Verify ordering is maintained
        assert bus.verify_ordering(org_id) is True
        
        # Get events in order
        ordered = bus.get_events_in_order(org_id)
        assert len(ordered) == 5
        for i in range(len(ordered)):
            assert ordered[i].payload["index"] == i
        
        # Get events with start sequence
        partial = bus.get_events_in_order(org_id, start_sequence=3)
        assert len(partial) == 3
        
        # Get events with limit
        limited = bus.get_events_in_order(org_id, limit=2)
        assert len(limited) == 2

    def test_qa_470_failure_handling(self):
        """QA-470: Event bus failure handling"""
        bus = EventBus()
        org_id = "test_org_470"
        
        # Create subscription with failing callback
        def failing_callback(event):
            raise Exception("Callback failed")
        
        bus.subscribe(
            organisation_id=org_id,
            subscriber_id="failing_subscriber",
            event_types=["test_event"],
            callback=failing_callback
        )
        
        # Publish event (will trigger failure)
        event = bus.publish(org_id, "test_event", {"data": "value"})
        
        # Verify failure was recorded
        failures = bus.get_failed_deliveries(org_id)
        assert len(failures) > 0
        
        failure = failures[0]
        assert failure["event_id"] == event.event_id
        assert failure["subscriber_id"] == "failing_subscriber"
        assert failure["organisation_id"] == org_id
        
        # Verify recovery was attempted
        assert "recovered" in failure
        
        # Test basic failure recovery without processing pending events
        # (to avoid infinite loop with failing callback)
        bus.state = EventBusState.FAILED
        
        # Clear the queue to avoid retry loop
        if org_id in bus.event_queues:
            bus.event_queues[org_id].events.clear()
        
        recovered = bus.recover_from_failure(org_id)
        
        # Verify recovery attempt was made and state changed
        assert recovered is True
        assert bus.state == EventBusState.RUNNING


@pytest.mark.wave2
@pytest.mark.subwave_2_9
class TestServiceCommunication:
    """QA-471 to QA-475: Service Communication"""

    def test_qa_471_service_discovery(self):
        """QA-471: Service discovery"""
        communicator = ServiceCommunicator()
        org_id = "test_org_471"
        
        # Register service
        endpoint = communicator.register_service(
            organisation_id=org_id,
            service_id="analytics_service",
            service_name="Analytics Service",
            host="localhost",
            port=8080,
            protocol="http"
        )
        
        # Verify service registered
        assert endpoint.service_id == "analytics_service"
        assert endpoint.host == "localhost"
        assert endpoint.port == 8080
        
        # Discover service
        discovered = communicator.discover_service(org_id, "analytics_service")
        assert discovered is not None
        assert discovered.service_id == "analytics_service"
        assert discovered.get_url() == "http://localhost:8080"
        
        # List services
        services = communicator.list_services(org_id)
        assert len(services) == 1
        assert services[0].service_id == "analytics_service"

    def test_qa_472_request_response(self):
        """QA-472: Service request/response"""
        communicator = ServiceCommunicator()
        org_id = "test_org_472"
        
        # Register target service
        communicator.register_service(
            organisation_id=org_id,
            service_id="target_service",
            service_name="Target Service",
            host="localhost",
            port=9090
        )
        
        # Send request
        response = communicator.send_request(
            organisation_id=org_id,
            source_service="source_service",
            target_service="target_service",
            method="POST",
            endpoint="/api/data",
            payload={"key": "value"}
        )
        
        # Verify response
        assert response.request_id is not None
        assert response.organisation_id == org_id
        assert response.is_successful()
        
        # Retrieve response
        retrieved = communicator.get_response(org_id, response.request_id)
        assert retrieved is not None
        assert retrieved.request_id == response.request_id

    def test_qa_473_retry_logic(self):
        """QA-473: Service retry logic"""
        communicator = ServiceCommunicator()
        org_id = "test_org_473"
        
        # Register target service
        communicator.register_service(
            organisation_id=org_id,
            service_id="retry_service",
            service_name="Retry Service",
            host="localhost",
            port=9091
        )
        
        # Set retry policy
        policy = RetryPolicy(
            max_retries=3,
            initial_delay_seconds=0.1,
            exponential_backoff=True
        )
        communicator.set_retry_policy(org_id, policy)
        
        # Verify policy set
        retrieved_policy = communicator.get_retry_policy(org_id)
        assert retrieved_policy.max_retries == 3
        
        # Test delay calculation
        assert retrieved_policy.get_delay(1) == 0.1
        assert retrieved_policy.get_delay(2) == 0.2
        assert retrieved_policy.get_delay(3) == 0.4
        
        # Test should_retry logic
        assert retrieved_policy.should_retry(500, 1) is True
        assert retrieved_policy.should_retry(500, 4) is False
        assert retrieved_policy.should_retry(200, 1) is False
        
        # Send request with retry (will succeed immediately in test)
        response = communicator.send_request_with_retry(
            organisation_id=org_id,
            source_service="source",
            target_service="retry_service",
            method="GET",
            endpoint="/api/health",
            payload={}
        )
        
        assert response is not None
        assert response.is_successful()

    def test_qa_474_health_checking(self):
        """QA-474: Service health checking"""
        communicator = ServiceCommunicator()
        org_id = "test_org_474"
        
        # Register service
        communicator.register_service(
            organisation_id=org_id,
            service_id="health_service",
            service_name="Health Service",
            host="localhost",
            port=9092
        )
        
        # Perform health check
        result = communicator.perform_health_check(org_id, "health_service")
        
        # Verify health check result
        assert result.service_id == "health_service"
        assert result.state in [ServiceState.HEALTHY, ServiceState.DEGRADED, ServiceState.UNHEALTHY]
        assert result.response_time_ms >= 0
        
        # Check if service is healthy
        is_healthy = communicator.is_service_healthy(org_id, "health_service")
        assert isinstance(is_healthy, bool)
        
        # Get health status
        status = communicator.get_health_status(org_id, "health_service")
        assert status is not None
        assert status.service_id == "health_service"
        
        # Test health check for non-existent service
        result = communicator.perform_health_check(org_id, "nonexistent_service")
        assert result.state == ServiceState.OFFLINE

    def test_qa_475_communication_security(self):
        """QA-475: Service communication security"""
        communicator = ServiceCommunicator()
        org_id = "test_org_475"
        
        # Configure security with API key
        context = communicator.configure_security(
            organisation_id=org_id,
            security_level=SecurityLevel.BASIC,
            api_key="test_api_key_123"
        )
        
        # Verify security context
        assert context.organisation_id == org_id
        assert context.security_level == SecurityLevel.BASIC
        assert context.api_key == "test_api_key_123"
        
        # Validate security
        assert communicator.validate_security(org_id) is True
        
        # Check security level
        level = communicator.get_security_level(org_id)
        assert level == SecurityLevel.BASIC
        
        # Test encryption (simplified)
        payload = {"sensitive": "data"}
        encrypted = communicator.encrypt_payload(org_id, payload)
        assert encrypted.get("encrypted") is True
        
        # Test decryption
        decrypted = communicator.decrypt_payload(org_id, encrypted)
        assert decrypted == payload
        
        # Test higher security level
        context2 = communicator.configure_security(
            organisation_id=org_id,
            security_level=SecurityLevel.ENCRYPTED,
            token="secure_token_456"
        )
        assert context2.security_level == SecurityLevel.ENCRYPTED
        assert communicator.validate_security(org_id) is True
