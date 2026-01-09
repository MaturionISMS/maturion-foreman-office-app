"""
Service Communicator

Purpose: Service discovery, request/response, retry logic, health checking, and security
Authority: Wave 2.0 Subwave 2.9 - Deep Integration Phase 1 (QA-471 to QA-475)
Tenant Isolation: All operations scoped by organisation_id
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
import time
import hashlib


class ServiceState(Enum):
    """Service operational states"""
    UNKNOWN = "unknown"
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    OFFLINE = "offline"


class SecurityLevel(Enum):
    """Security levels for service communication"""
    NONE = "none"
    BASIC = "basic"
    ENCRYPTED = "encrypted"
    MUTUAL_TLS = "mutual_tls"


@dataclass
class ServiceEndpoint:
    """Service endpoint information"""
    service_id: str
    service_name: str
    host: str
    port: int
    protocol: str = "http"
    version: str = "1.0"
    state: ServiceState = ServiceState.UNKNOWN
    last_health_check: Optional[datetime] = None
    
    def get_url(self) -> str:
        """Get full URL for the service"""
        return f"{self.protocol}://{self.host}:{self.port}"


@dataclass
class ServiceRequest:
    """Service request"""
    request_id: str
    source_service: str
    target_service: str
    method: str
    endpoint: str
    payload: Dict[str, Any]
    timestamp: datetime
    organisation_id: str
    security_level: SecurityLevel = SecurityLevel.BASIC
    timeout_seconds: int = 30
    
    def is_expired(self) -> bool:
        """Check if request has exceeded timeout"""
        elapsed = (datetime.now(timezone.utc) - self.timestamp).total_seconds()
        return elapsed > self.timeout_seconds


@dataclass
class ServiceResponse:
    """Service response"""
    request_id: str
    status_code: int
    payload: Dict[str, Any]
    timestamp: datetime
    response_time_ms: float
    organisation_id: str
    
    def is_successful(self) -> bool:
        """Check if response indicates success"""
        return 200 <= self.status_code < 300


@dataclass
class RetryPolicy:
    """Retry policy for failed requests"""
    max_retries: int = 3
    initial_delay_seconds: float = 1.0
    max_delay_seconds: float = 30.0
    exponential_backoff: bool = True
    retry_on_status_codes: List[int] = field(default_factory=lambda: [500, 502, 503, 504])
    
    def get_delay(self, attempt: int) -> float:
        """Calculate delay for a given retry attempt"""
        if self.exponential_backoff:
            delay = self.initial_delay_seconds * (2 ** (attempt - 1))
            return min(delay, self.max_delay_seconds)
        return self.initial_delay_seconds
    
    def should_retry(self, status_code: int, attempt: int) -> bool:
        """Check if request should be retried"""
        return (
            attempt < self.max_retries and
            status_code in self.retry_on_status_codes
        )


@dataclass
class HealthCheckResult:
    """Result of a service health check"""
    service_id: str
    state: ServiceState
    timestamp: datetime
    response_time_ms: float
    details: Dict[str, Any] = field(default_factory=dict)
    
    def is_healthy(self) -> bool:
        """Check if service is healthy"""
        return self.state == ServiceState.HEALTHY


@dataclass
class SecurityContext:
    """Security context for service communication"""
    organisation_id: str
    security_level: SecurityLevel
    api_key: Optional[str] = None
    token: Optional[str] = None
    certificate_hash: Optional[str] = None
    
    def validate(self) -> bool:
        """Validate security context"""
        if self.security_level == SecurityLevel.NONE:
            return True
        elif self.security_level == SecurityLevel.BASIC:
            return self.api_key is not None
        elif self.security_level == SecurityLevel.ENCRYPTED:
            return self.token is not None
        elif self.security_level == SecurityLevel.MUTUAL_TLS:
            return self.certificate_hash is not None
        return False


class ServiceCommunicator:
    """
    Manages service-to-service communication including discovery, request/response,
    retry logic, health checking, and security
    """
    
    def __init__(self):
        self.service_registry: Dict[str, Dict[str, ServiceEndpoint]] = {}  # org_id -> {service_id -> endpoint}
        self.requests: Dict[str, List[ServiceRequest]] = {}  # org_id -> requests
        self.responses: Dict[str, List[ServiceResponse]] = {}  # org_id -> responses
        self.health_checks: Dict[str, Dict[str, HealthCheckResult]] = {}  # org_id -> {service_id -> result}
        self.retry_policies: Dict[str, RetryPolicy] = {}  # org_id -> policy
        self.security_contexts: Dict[str, SecurityContext] = {}  # org_id -> context
        self.next_request_id = 1
    
    # QA-471: Service Discovery
    def register_service(
        self,
        organisation_id: str,
        service_id: str,
        service_name: str,
        host: str,
        port: int,
        protocol: str = "http",
        version: str = "1.0"
    ) -> ServiceEndpoint:
        """
        Register a service for discovery
        
        Args:
            organisation_id: Tenant identifier for isolation
            service_id: Unique service identifier
            service_name: Human-readable service name
            host: Service host address
            port: Service port number
            protocol: Communication protocol (http, https, grpc)
            version: Service version
            
        Returns:
            ServiceEndpoint with registration details
        """
        endpoint = ServiceEndpoint(
            service_id=service_id,
            service_name=service_name,
            host=host,
            port=port,
            protocol=protocol,
            version=version,
            state=ServiceState.UNKNOWN
        )
        
        if organisation_id not in self.service_registry:
            self.service_registry[organisation_id] = {}
        
        self.service_registry[organisation_id][service_id] = endpoint
        
        return endpoint
    
    def discover_service(
        self,
        organisation_id: str,
        service_id: str
    ) -> Optional[ServiceEndpoint]:
        """
        Discover a registered service
        
        Args:
            organisation_id: Tenant identifier
            service_id: Service to discover
            
        Returns:
            ServiceEndpoint if found, None otherwise
        """
        if organisation_id in self.service_registry:
            return self.service_registry[organisation_id].get(service_id)
        return None
    
    def list_services(
        self,
        organisation_id: str,
        state_filter: Optional[ServiceState] = None
    ) -> List[ServiceEndpoint]:
        """List all registered services, optionally filtered by state"""
        services = self.service_registry.get(organisation_id, {}).values()
        
        if state_filter:
            return [s for s in services if s.state == state_filter]
        
        return list(services)
    
    # QA-472: Request/Response Handling
    def send_request(
        self,
        organisation_id: str,
        source_service: str,
        target_service: str,
        method: str,
        endpoint: str,
        payload: Dict[str, Any],
        timeout_seconds: int = 30
    ) -> ServiceResponse:
        """
        Send a request to a service
        
        Args:
            organisation_id: Tenant identifier for isolation
            source_service: Service making the request
            target_service: Service receiving the request
            method: HTTP method (GET, POST, etc.)
            endpoint: Endpoint path
            payload: Request data
            timeout_seconds: Request timeout
            
        Returns:
            ServiceResponse with result
        """
        request_id = f"req_{self.next_request_id}_{organisation_id}"
        self.next_request_id += 1
        
        # Get security context
        security_level = SecurityLevel.BASIC
        if organisation_id in self.security_contexts:
            security_level = self.security_contexts[organisation_id].security_level
        
        request = ServiceRequest(
            request_id=request_id,
            source_service=source_service,
            target_service=target_service,
            method=method,
            endpoint=endpoint,
            payload=payload,
            timestamp=datetime.now(timezone.utc),
            organisation_id=organisation_id,
            security_level=security_level,
            timeout_seconds=timeout_seconds
        )
        
        # Store request
        if organisation_id not in self.requests:
            self.requests[organisation_id] = []
        self.requests[organisation_id].append(request)
        
        # Simulate request processing
        start_time = time.time()
        
        # Check if service exists
        target_endpoint = self.discover_service(organisation_id, target_service)
        if not target_endpoint:
            response = ServiceResponse(
                request_id=request_id,
                status_code=404,
                payload={"error": "Service not found"},
                timestamp=datetime.now(timezone.utc),
                response_time_ms=(time.time() - start_time) * 1000,
                organisation_id=organisation_id
            )
        else:
            # Simulate successful response
            response = ServiceResponse(
                request_id=request_id,
                status_code=200,
                payload={"success": True, "data": "Response data"},
                timestamp=datetime.now(timezone.utc),
                response_time_ms=(time.time() - start_time) * 1000,
                organisation_id=organisation_id
            )
        
        # Store response
        if organisation_id not in self.responses:
            self.responses[organisation_id] = []
        self.responses[organisation_id].append(response)
        
        return response
    
    def get_response(
        self,
        organisation_id: str,
        request_id: str
    ) -> Optional[ServiceResponse]:
        """Get response for a specific request"""
        responses = self.responses.get(organisation_id, [])
        for response in responses:
            if response.request_id == request_id:
                return response
        return None
    
    # QA-473: Retry Logic
    def send_request_with_retry(
        self,
        organisation_id: str,
        source_service: str,
        target_service: str,
        method: str,
        endpoint: str,
        payload: Dict[str, Any],
        retry_policy: Optional[RetryPolicy] = None
    ) -> ServiceResponse:
        """
        Send request with automatic retry on failure
        
        Args:
            organisation_id: Tenant identifier for isolation
            source_service: Service making the request
            target_service: Service receiving the request
            method: HTTP method
            endpoint: Endpoint path
            payload: Request data
            retry_policy: Optional retry policy (uses default if not provided)
            
        Returns:
            ServiceResponse with result after retries
        """
        if retry_policy is None:
            retry_policy = self.retry_policies.get(organisation_id, RetryPolicy())
        
        attempt = 0
        last_response = None
        
        while attempt <= retry_policy.max_retries:
            attempt += 1
            
            # Send request
            response = self.send_request(
                organisation_id=organisation_id,
                source_service=source_service,
                target_service=target_service,
                method=method,
                endpoint=endpoint,
                payload=payload
            )
            
            last_response = response
            
            # Check if successful
            if response.is_successful():
                return response
            
            # Check if should retry
            if not retry_policy.should_retry(response.status_code, attempt):
                break
            
            # Calculate delay before retry
            if attempt <= retry_policy.max_retries:
                delay = retry_policy.get_delay(attempt)
                time.sleep(delay)
        
        return last_response
    
    def set_retry_policy(
        self,
        organisation_id: str,
        policy: RetryPolicy
    ) -> None:
        """Set retry policy for a tenant"""
        self.retry_policies[organisation_id] = policy
    
    def get_retry_policy(
        self,
        organisation_id: str
    ) -> RetryPolicy:
        """Get retry policy for a tenant"""
        return self.retry_policies.get(organisation_id, RetryPolicy())
    
    # QA-474: Health Checking
    def perform_health_check(
        self,
        organisation_id: str,
        service_id: str
    ) -> HealthCheckResult:
        """
        Perform health check on a service
        
        Args:
            organisation_id: Tenant identifier for isolation
            service_id: Service to check
            
        Returns:
            HealthCheckResult with status
        """
        start_time = time.time()
        
        endpoint = self.discover_service(organisation_id, service_id)
        
        if not endpoint:
            result = HealthCheckResult(
                service_id=service_id,
                state=ServiceState.OFFLINE,
                timestamp=datetime.now(timezone.utc),
                response_time_ms=(time.time() - start_time) * 1000,
                details={"error": "Service not registered"}
            )
        else:
            # Simulate health check (in real implementation, would make actual HTTP request)
            response_time_ms = (time.time() - start_time) * 1000
            
            # Determine health based on response time
            if response_time_ms < 100:
                state = ServiceState.HEALTHY
            elif response_time_ms < 500:
                state = ServiceState.DEGRADED
            else:
                state = ServiceState.UNHEALTHY
            
            result = HealthCheckResult(
                service_id=service_id,
                state=state,
                timestamp=datetime.now(timezone.utc),
                response_time_ms=response_time_ms,
                details={"url": endpoint.get_url()}
            )
            
            # Update endpoint state
            endpoint.state = state
            endpoint.last_health_check = result.timestamp
        
        # Store health check result
        if organisation_id not in self.health_checks:
            self.health_checks[organisation_id] = {}
        self.health_checks[organisation_id][service_id] = result
        
        return result
    
    def get_health_status(
        self,
        organisation_id: str,
        service_id: str
    ) -> Optional[HealthCheckResult]:
        """Get most recent health check result for a service"""
        if organisation_id in self.health_checks:
            return self.health_checks[organisation_id].get(service_id)
        return None
    
    def is_service_healthy(
        self,
        organisation_id: str,
        service_id: str
    ) -> bool:
        """Check if a service is currently healthy"""
        result = self.get_health_status(organisation_id, service_id)
        return result is not None and result.is_healthy()
    
    # QA-475: Communication Security
    def configure_security(
        self,
        organisation_id: str,
        security_level: SecurityLevel,
        api_key: Optional[str] = None,
        token: Optional[str] = None,
        certificate: Optional[str] = None
    ) -> SecurityContext:
        """
        Configure security for service communication
        
        Args:
            organisation_id: Tenant identifier for isolation
            security_level: Level of security to apply
            api_key: API key for basic security
            token: Token for encrypted security
            certificate: Certificate for mutual TLS
            
        Returns:
            SecurityContext with configuration
        """
        certificate_hash = None
        if certificate:
            certificate_hash = hashlib.sha256(certificate.encode()).hexdigest()
        
        context = SecurityContext(
            organisation_id=organisation_id,
            security_level=security_level,
            api_key=api_key,
            token=token,
            certificate_hash=certificate_hash
        )
        
        self.security_contexts[organisation_id] = context
        
        return context
    
    def validate_security(
        self,
        organisation_id: str
    ) -> bool:
        """
        Validate security configuration
        
        Returns:
            True if security is properly configured
        """
        if organisation_id in self.security_contexts:
            return self.security_contexts[organisation_id].validate()
        return False
    
    def get_security_level(
        self,
        organisation_id: str
    ) -> SecurityLevel:
        """Get current security level for a tenant"""
        if organisation_id in self.security_contexts:
            return self.security_contexts[organisation_id].security_level
        return SecurityLevel.NONE
    
    def encrypt_payload(
        self,
        organisation_id: str,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Encrypt payload based on security level
        
        Args:
            organisation_id: Tenant identifier
            payload: Data to encrypt
            
        Returns:
            Encrypted payload (in real implementation)
        """
        context = self.security_contexts.get(organisation_id)
        
        if not context or context.security_level == SecurityLevel.NONE:
            return payload
        
        # In real implementation, would perform actual encryption
        # For now, just wrap payload to indicate encryption
        return {
            "encrypted": True,
            "security_level": context.security_level.value,
            "data": payload  # Would be encrypted in real implementation
        }
    
    def decrypt_payload(
        self,
        organisation_id: str,
        encrypted_payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Decrypt payload based on security level
        
        Args:
            organisation_id: Tenant identifier
            encrypted_payload: Encrypted data
            
        Returns:
            Decrypted payload
        """
        if not encrypted_payload.get("encrypted"):
            return encrypted_payload
        
        # In real implementation, would perform actual decryption
        return encrypted_payload.get("data", {})
