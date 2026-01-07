# Integration Builder Extended Reference

**Purpose**: Extended documentation for Integration Builder contract  
**Authority**: `.github/agents/integration-builder.md`  
**Status**: Reference Material  
**Last Updated**: 2026-01-07

This document contains detailed examples, extended narratives, and supporting material for the Integration Builder contract. The core contract file contains essential doctrine and obligations. This reference provides context and illustration.

---

## Detailed Appointment Acknowledgment Example

When appointed by FM, Integration Builder provides complete acknowledgment with verification of:
- Frozen integration specifications
- QA-to-Red tests for integration points
- External service contracts defined
- Authentication/authorization requirements
- Error handling requirements
- Memory fabric status

---

## BL-018/BL-019 Integration Builder Scenarios

### Scenario 1: Missing External Service Specification

Builder appointed to integrate with Authentication Service, but architecture lacks service contract definition.

**Correct Response**: STOP, declare BLOCKED, document missing service contract, escalate to FM per BL-018 awareness.

### Scenario 2: Protocol Mismatch

Architecture specifies REST API integration, but QA-to-Red tests check for GraphQL queries.

**Correct Response**: STOP, declare BLOCKED, document protocol mismatch between architecture and tests, escalate per BL-019 awareness.

---

## Code Checking Process for Integration Implementation

### Integration-Specific Checks

1. **Protocol Correctness**: Does integration use correct protocol (REST/GraphQL/gRPC)?
2. **Error Handling**: Are network errors, timeouts, retries handled?
3. **Authentication**: Are credentials managed securely?
4. **Data Mapping**: Is data correctly transformed between systems?
5. **Idempotency**: Are operations idempotent where required?

**Example Walkthrough**: Implementation of External Auth Service integration
- Verify HTTP client configured correctly ✅
- Verify error handling comprehensive ✅
- Verify credentials from environment/vault ✅
- Verify request/response mapping correct ✅
- Verify retry logic in place ✅
- Run QA-to-Red tests (RED → GREEN) ✅

---

## Enhancement Capture Examples for Integration Builder

### Example 1: Circuit Breaker Pattern
```
ENHANCEMENT PROPOSAL (PARKED)

Title: Circuit Breaker for External Service Calls
Context: External service calls can fail repeatedly. Circuit breaker pattern would prevent 
cascading failures and improve resilience.

Proposal: Implement circuit breaker (using library like opossum) for external auth service calls

Benefit: Prevents cascading failures, improves system resilience, reduces unnecessary retries

Status: PARKED — NOT AUTHORIZED FOR EXECUTION
Routing: → Foreman App Parking Station
```

### Example 2: Response Caching
```
ENHANCEMENT PROPOSAL (PARKED)

Title: Cache External Service Responses
Context: Some external service responses are cacheable (user profiles, static data). 
Caching would reduce external calls and improve performance.

Proposal: Add Redis caching layer for cacheable external service responses

Benefit: Reduces external API calls by ~60%, improves response time, reduces costs

Status: PARKED — NOT AUTHORIZED FOR EXECUTION
Routing: → Foreman App Parking Station
```

---

**End of Extended Reference**
