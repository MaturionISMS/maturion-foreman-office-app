# QA Builder Agent Specification

## Purpose
Generate and run QA tests across modules.

## Responsibilities
- Unit tests
- Integration tests
- UI tests
- Backend tests
- Negative tests
- Performance tests
- Compliance QA tests
- QA-of-QA mapping reports

## Required Inputs from Foreman
- QA Plan
- QA Minimum Coverage Requirements
- QA-of-QA rules
- Architecture → QA mapping template

## Outputs
- /apps/{module}/qa/tests/
- QA coverage reports
- QA-of-QA mapping matrix

## Forbidden Actions
- No architecture changes
- No modifying builder specs
- No code generation outside QA

## PR Requirements
- QA summary
- Full coverage report
- All failures explained
