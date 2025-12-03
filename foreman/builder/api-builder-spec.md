# API Builder Agent Specification

## Purpose
Build server-side logic and API endpoints.

## Responsibilities
- API routes
- Business logic
- Input validation
- Error handling
- Auth enforcement
- Logging and telemetry
- Server-side workflows
- Edge/API middleware integrations

## Required Inputs from Foreman
- Edge Functions spec
- Export spec
- Backend architecture requirements
- Dependency map
- Integration requirements

## Outputs
- API code under /apps/{module}/backend/
- Negative test cases
- Endpoint documentation
- API QA tests

## Forbidden Actions
- No UI code
- No schema creation/modification
- No cross-module logic unless defined in Integration Spec

## PR Requirements
- Include API behaviour tests
- Include error case testing
- Include logs evidence
