# COURSE_CRAFTER_DATABASE_SCHEMA_v1.0.md

## Course Crafter - Database Schema
**Version**: 1.0  
**Date**: 2025-12-04

## Schema Overview
All tables follow naming convention: `course_crafter_*`

All tables include:
- `organisation_id UUID NOT NULL REFERENCES organisations(id)`
- `created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()`
- `updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()`
- `created_by UUID NOT NULL REFERENCES auth.users(id)`
- `updated_by UUID NOT NULL REFERENCES auth.users(id)`

## Core Tables
[Entity tables to be defined - following RLS pattern]

## Row Level Security (RLS)
All tables have RLS enabled with policies:
- SELECT: WHERE organisation_id = auth.current_organisation_id()
- INSERT: WITH CHECK organisation_id = auth.current_organisation_id()
- UPDATE: USING organisation_id = auth.current_organisation_id()
- DELETE: USING organisation_id = auth.current_organisation_id()

## Indexes
- Primary keys on all tables
- Index on organisation_id for all tables
- Composite indexes for common queries

## Triggers
- Auto-update `updated_at` timestamp on UPDATE
- Auto-set `updated_by` to auth.uid() on UPDATE

## Data Integrity
- Foreign keys for referential integrity
- Check constraints for validation
- Unique constraints where applicable
- CASCADE delete for tenant data

*Generated for Build Wave 0.1 - Architecture Completion Sprint*
