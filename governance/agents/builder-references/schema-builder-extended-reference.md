# Schema Builder Extended Reference

**Purpose**: Extended documentation for Schema Builder contract  
**Authority**: `.github/agents/schema-builder.md`  
**Status**: Reference Material  
**Last Updated**: 2026-01-07

This document contains detailed examples, extended narratives, and supporting material for the Schema Builder contract. The core contract file contains essential doctrine and obligations. This reference provides context and illustration.

---

## Detailed Appointment Acknowledgment Example

When appointed by FM, Schema Builder provides complete acknowledgment with verification of:
- Frozen database schema specifications
- QA-to-Red tests for schema validation
- Migration strategy defined
- Data model requirements clear
- Tenant isolation requirements
- Memory fabric status

---

## BL-018/BL-019 Schema Builder Scenarios

### Scenario 1: Missing Entity Relationships

Builder appointed to implement User entity, but architecture doesn't define relationships with Organization and Role entities.

**Correct Response**: STOP, declare BLOCKED, document missing relationship specifications, escalate to FM per BL-018 awareness.

### Scenario 2: Migration Test Mismatch

Architecture specifies PostgreSQL schema, but QA-to-Red tests check MySQL-specific features.

**Correct Response**: STOP, declare BLOCKED, document database mismatch, escalate per BL-019 awareness.

---

## Code Checking Process for Schema Implementation

### Schema-Specific Checks

1. **Schema Correctness**: Do tables/columns match specifications?
2. **Constraints**: Are foreign keys, indexes, unique constraints correct?
3. **Migrations**: Are migrations idempotent and reversible?
4. **Tenant Isolation**: Is organization_id present where required?
5. **Data Types**: Are data types appropriate and efficient?

**Example Walkthrough**: Implementation of Dashboard schema
- Verify table structure matches architecture ✅
- Verify foreign keys correct ✅
- Verify indexes on query columns ✅
- Verify organization_id present ✅
- Verify migration can rollback ✅
- Run QA-to-Red tests (RED → GREEN) ✅

---

## Enhancement Capture Examples for Schema Builder

### Example 1: Index Optimization
```
ENHANCEMENT PROPOSAL (PARKED)

Title: Composite Index for Common Query Pattern
Context: Queries often filter by organization_id AND created_at. A composite index would 
improve query performance.

Proposal: Add composite index (organization_id, created_at) to dashboard table

Benefit: Reduces query time from ~50ms to ~5ms for dashboard list queries

Status: PARKED — NOT AUTHORIZED FOR EXECUTION
Routing: → Foreman App Parking Station
```

### Example 2: Data Model Enhancement
```
ENHANCEMENT PROPOSAL (PARKED)

Title: Soft Delete Pattern
Context: Current schema uses hard deletes. Soft deletes would enable data recovery and 
audit trails.

Proposal: Add deleted_at column to key tables, update queries to filter WHERE deleted_at IS NULL

Benefit: Enables data recovery, improves audit capability, prevents accidental data loss

Status: PARKED — NOT AUTHORIZED FOR EXECUTION
Routing: → Foreman App Parking Station
```

---

**End of Extended Reference**
