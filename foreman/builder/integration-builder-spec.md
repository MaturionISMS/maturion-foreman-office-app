# Integration Builder Agent Specification

## Purpose
Build all cross-module and cross-system integrations.

## Responsibilities
- Integration endpoints
- Event-driven flows
- API inter-module links
- Webhooks
- Messaging channels

## Required Inputs from Foreman
- Module Integration Spec
- Platform Integration Map
- Architecture boundaries
- Allowed dependency graph

## Outputs
- Integration code under /apps/{module}/integration/
- Integration tests
- Dependency diagrams

## Forbidden Actions
- No schema creation
- No UI
- No business logic outside defined flows

## PR Requirements
- Full integration flow diagrams
- Integration test coverage
- Compliance with boundaries
