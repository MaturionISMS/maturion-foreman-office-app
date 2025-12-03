================================================================================
MATURION FOREMAN - BUILDER AGENT REGISTRY REPORT
================================================================================

SUMMARY
--------------------------------------------------------------------------------
Total Agents Registered: 5
Specification Files Found: 5
Validation Checks: 19
Errors: 0
Warnings: 0

REGISTERED AGENTS
--------------------------------------------------------------------------------

[ui-builder]
  Responsibilities: UI components, layouts, wizards
  Forbidden: backend logic, cross-module logic
  Capabilities: ui, frontend, components, styling
  Read Access: foreman/*
  Write Access: apps/*/frontend/*

[api-builder]
  Responsibilities: API endpoints, handlers
  Forbidden: UI, global state
  Capabilities: api, backend, logic, routes
  Read Access: foreman/*
  Write Access: apps/*/backend/*

[schema-builder]
  Responsibilities: database schemas, models
  Forbidden: UI, integration routing
  Capabilities: schema, models, migrations
  Read Access: foreman/*
  Write Access: apps/*/data/*

[integration-builder]
  Responsibilities: module integrations
  Forbidden: UI, schemas
  Capabilities: integration, inter-module, events
  Read Access: foreman/*
  Write Access: apps/*/integration/*

[qa-builder]
  Responsibilities: QA tests, coverage
  Forbidden: architecture, governance
  Capabilities: testing, coverage, qa-of-qa
  Read Access: foreman/*
  Write Access: apps/*/qa/*

VALIDATION RESULTS
--------------------------------------------------------------------------------
✓ Successfully loaded builder-manifest.json: builder-manifest.json
✓ Successfully loaded builder-capability-map.json: builder-capability-map.json
✓ Successfully loaded builder-permission-policy.json: builder-permission-policy.json
✓ Discovered 5 builder specification files
✓ Spec file validated for 'qa-builder'
✓ Spec file validated for 'api-builder'
✓ Spec file validated for 'integration-builder'
✓ Spec file validated for 'schema-builder'
✓ Spec file validated for 'ui-builder'
✓ Capability alignment validated for 'qa-builder': 3 capabilities
✓ Capability alignment validated for 'api-builder': 4 capabilities
✓ Capability alignment validated for 'ui-builder': 4 capabilities
✓ Capability alignment validated for 'integration-builder': 3 capabilities
✓ Capability alignment validated for 'schema-builder': 3 capabilities
✓ Permission alignment validated for 'qa-builder': 1 read, 1 write
✓ Permission alignment validated for 'api-builder': 1 read, 1 write
✓ Permission alignment validated for 'ui-builder': 1 read, 1 write
✓ Permission alignment validated for 'integration-builder': 1 read, 1 write
✓ Permission alignment validated for 'schema-builder': 1 read, 1 write

STATUS
--------------------------------------------------------------------------------
✓ SUCCESS: All builder agents initialized and validated successfully
================================================================================