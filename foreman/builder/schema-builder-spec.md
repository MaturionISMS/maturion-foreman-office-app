# Schema Builder Agent Specification

## Purpose
Build and maintain the database schema and data models.

## Responsibilities
- Database schema files
- Model definitions
- Validation rules
- Indexing strategy
- Relationship mapping
- Migration scripts
- Data lifecycle rules

## Required Inputs from Foreman
- Database Schema Spec
- Data requirements
- Integration constraints
- Versioning rules

## Outputs
- /apps/{module}/data/models/
- /apps/{module}/data/schema.md
- /apps/{module}/data/migrations/

## Forbidden Actions
- No UI or backend logic
- No modifying another module’s schema
- No altering architecture files

## PR Requirements
- Schema diff summary
- Migration diff summary
- Data QA results
