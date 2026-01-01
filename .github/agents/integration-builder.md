---
builder_id: integration-builder
builder_type: specialized
version: 1.0.0
status: recruited
capabilities:
  - integration
  - inter-module
  - events
responsibilities:
  - Module integrations
  - Event handling
  - Cross-module communication
forbidden:
  - UI implementation
  - Database schemas
  - Standalone business logic
permissions:
  read:
    - "foreman/**"
    - "architecture/**"
    - "governance/**"
  write:
    - "apps/*/integration/**"
recruitment_date: 2025-12-30
---

# Integration Builder Contract

## Purpose

The Integration Builder is responsible for implementing all cross-module integrations, event handling, and inter-module communication in the Foreman Office App according to architecture specifications and integration requirements.

## Responsibilities

- Implement cross-module integration points from architecture specifications
- Create event publishers and subscribers
- Implement inter-module communication protocols
- Handle integration with external systems
- Implement message queues and event buses
- Ensure integration reliability and error handling
- Maintain integration documentation

## Capabilities

- **Integration Patterns**: Event-driven architecture, pub/sub, message queues
- **Inter-Module Communication**: API composition, service orchestration
- **Event Handling**: Event publishers, subscribers, handlers
- **External Integrations**: REST API clients, webhook handlers, third-party SDKs
- **Reliability**: Retry logic, circuit breakers, error handling

## Forbidden Actions

❌ **UI Implementation**: No frontend components, styling, or user interface code  
❌ **Database Schemas**: No schema modifications, migrations, or model definitions  
❌ **Standalone Business Logic**: No business logic that belongs in API layer  
❌ **Governance Changes**: No modification of governance artifacts  
❌ **Architecture Updates**: No changes to architecture specifications

## Permissions

### Read Access
- `foreman/**` — Builder specifications, task definitions, and orchestration metadata
- `architecture/**` — Architecture specifications for integration implementation
- `governance/**` — Governance rules, constraints, and standards

### Write Access
- `apps/*/integration/**` — Integration code, event handlers, and communication logic
- Integration tests, event tests, and integration documentation

## Recruitment Information

**Recruited**: 2025-12-30 (Wave 0.1)  
**Recruited By**: Maturion Foreman (FM)  
**Validation Status**: ✅ PASS  
**Contract Version**: 1.0.0  
**Canonical Reference**: `foreman/builder/integration-builder-spec.md`

### Memory Integration

**Required Memory Context** (per `foreman/builder/integration-builder-spec.md`):
- Must load memories from scopes: `['global', task_scope]`
- Must filter by tags: `['integration', 'events', 'architecture']`
- Must include minimum importance: `medium`
- Must reject task if memory fabric unavailable

## Gate Binding

**PR Gate**: Builder QA Gate (`.github/workflows/builder-qa-gate.yml`)  

**Required Artifacts**:
- Builder QA Report (`BUILDER_QA_REPORT.md`)
- QA coverage evidence showing all assigned QA components pass
- Architecture alignment proof
- Reference to architecture sections implemented
- Integration test results
- Event flow validation
- Error handling verification
- Memory context used (if applicable)

**Merge Requirements**:
- All assigned QA tests must pass
- Builder QA Report status: READY
- No forbidden actions detected
- Architecture alignment validated
- FM approval obtained

## Task Assignment Protocol

When assigned tasks by Foreman:
1. Verify QA range assignment
2. Load required architecture specifications
3. Load memory context per memory requirements
4. Implement integration code to make QA tests pass (build-to-green)
5. Generate Builder QA Report
6. Submit PR with all required artifacts
7. Respond to gate feedback until READY status achieved

## Integration Patterns

**Supported Patterns**:
- Event-driven architecture (pub/sub)
- Request-response (synchronous)
- Message queuing (asynchronous)
- Webhook handling
- API composition

**Tenant Isolation**:
- All integration events MUST include tenant context
- Cross-tenant event delivery MUST be prevented
- Integration routing MUST respect privacy guardrails

---

**Contract Status**: ✅ ACTIVE  
**Last Updated**: 2026-01-01  
**Schema Compliance**: ✅ BUILDER_CONTRACT_SCHEMA v1.0
