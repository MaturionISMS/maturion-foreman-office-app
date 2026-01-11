# Canonical Schemas Reference

## Purpose

This document references all canonical governance schemas from the `maturion-foreman-governance` repository. Schemas are NOT copied to prevent drift; instead, this document provides authoritative references.

## Canonical Source

**Repository**: `maturion-foreman-governance`  
**Location**: `governance/schemas/`  
**URL**: `https://github.com/APGI-cmy/maturion-foreman-governance/tree/main/governance/schemas`

## Applicable Schemas

### Repository Initialization Evidence Schema
**File**: `REPOSITORY_INITIALIZATION_EVIDENCE.schema.md`  
**Version**: v1.0  
**Purpose**: Normative structure for repository initialization evidence artifacts  
**Location**: `https://github.com/APGI-cmy/maturion-foreman-governance/blob/main/governance/schemas/REPOSITORY_INITIALIZATION_EVIDENCE.schema.md`  
**Used In**: `.architecture/REPOSITORY_INITIALIZATION_EVIDENCE.md`

### .agent Contract Schema
**File**: `.agent.schema.md`  
**Version**: Current  
**Purpose**: Normative structure for repository-level .agent contracts  
**Location**: `https://github.com/APGI-cmy/maturion-foreman-governance/blob/main/governance/canon/.agent.schema.md`  
**Used In**: `.agent` (repository root)

### Code Review Closure Schema
**File**: `code-review-closure-schema.json`  
**Version**: Current  
**Purpose**: Structure for code review closure requirements  
**Location**: Local copy exists at `governance/schemas/code-review-closure-schema.json`  
**Used In**: Code review closure gate workflows

## Schema Synchronization

**Method**: Reference-based (schemas NOT copied)  
**Drift Prevention**: All schema references point to canonical source in governance repository  
**Version Tracking**: Schema versions tracked in `governance/alignment/GOVERNANCE_ALIGNMENT.md`

## Adding New Schema References

When a new canonical schema is used in this repository:

1. Add entry to this document with:
   - Schema name and file
   - Version number
   - Purpose
   - Canonical location URL
   - Where used in this repository

2. Update `governance/alignment/GOVERNANCE_ALIGNMENT.md` to reflect schema addition

3. Do NOT copy schema files (except where absolutely required for offline operation)

---

**Last Updated**: 2026-01-11  
**Maintained By**: Governance Liaison Agent  
**Governance Version**: 7dc8110
