# Cross-Module Relationships Guide – Maturion ISMS

**Version**: 1.0  
**Date**: 2025-12-04  
**Status**: Active  
**Build Wave**: 1.2

---

## 1. Purpose

This document defines **cross-module relationship patterns** for the Maturion ISMS ecosystem.

It establishes:
- How modules reference each other's entities
- Integration table patterns
- Event-driven communication
- Data consistency strategies
- Referential integrity approaches

---

## 2. Relationship Principles

### 2.1 Loose Coupling

**Avoid direct foreign keys across modules**:
- ❌ Don't: `threat.vulnerability_id → vulnerability.id`
- ✅ Do: Store reference as UUID with event-based sync

**Why?**
- Modules should be independently deployable
- Schema changes in one module shouldn't break others
- Allows for module-specific scaling and optimization

### 2.2 Event-Driven Integration

**Use event log for cross-module communication**:

```sql
-- Example: Threat references Vulnerability
-- Instead of FK, publish event when relationship is created

INSERT INTO event_log (
  organisation_id,
  event_type,
  source_module,
  source_entity_type,
  source_entity_id,
  target_module,
  target_entity_type,
  target_entity_id,
  payload
) VALUES (
  :org_id,
  'threat_vulnerability_linked',
  'threat',
  'threat',
  :threat_id,
  'vulnerability',
  'vulnerability',
  :vulnerability_id,
  jsonb_build_object('link_type', 'exploits')
);
```

### 2.3 Integration Tables

**For many-to-many relationships across modules**:

```sql
-- Integration table pattern
CREATE TABLE threat_vulnerability_link (
  id UUID PRIMARY KEY DEFAULT generate_uuidv7(),
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  
  -- Threat reference (no FK constraint across modules)
  threat_id UUID NOT NULL,
  threat_title TEXT, -- Denormalized for performance
  
  -- Vulnerability reference (no FK constraint across modules)
  vulnerability_id UUID NOT NULL,
  vulnerability_title TEXT, -- Denormalized for performance
  
  -- Relationship metadata
  link_type TEXT NOT NULL, -- 'exploits', 'mitigates', etc.
  confidence_level TEXT, -- 'high', 'medium', 'low'
  
  -- Standard audit fields
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_by UUID NOT NULL REFERENCES users(id),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_by UUID REFERENCES users(id),
  deleted_at TIMESTAMPTZ NULL,
  deleted_by UUID REFERENCES users(id),
  
  UNIQUE(organisation_id, threat_id, vulnerability_id)
);

CREATE INDEX idx_threat_vuln_link_threat ON threat_vulnerability_link(organisation_id, threat_id);
CREATE INDEX idx_threat_vuln_link_vuln ON threat_vulnerability_link(organisation_id, vulnerability_id);
```

---

## 3. Cross-Module Relationship Patterns

### 3.1 PIT ↔ WRAC

**Project personnel assignments** (PIT references WRAC personnel):

```sql
-- PIT: project_personnel (integration table)
CREATE TABLE project_personnel (
  id UUID PRIMARY KEY DEFAULT generate_uuidv7(),
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  
  -- Project reference (within PIT module)
  project_id UUID NOT NULL REFERENCES project(id),
  
  -- Personnel reference (from WRAC module, no FK constraint)
  personnel_id UUID NOT NULL,
  personnel_name TEXT NOT NULL, -- Denormalized
  personnel_email TEXT,
  
  -- Assignment details
  role TEXT NOT NULL, -- 'project_manager', 'team_member', 'stakeholder'
  allocation_percentage NUMERIC(5,2), -- % of time allocated
  start_date DATE,
  end_date DATE,
  
  -- Standard audit fields
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_by UUID NOT NULL REFERENCES users(id),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_by UUID REFERENCES users(id),
  deleted_at TIMESTAMPTZ NULL,
  
  UNIQUE(organisation_id, project_id, personnel_id)
);

CREATE INDEX idx_project_personnel_project ON project_personnel(organisation_id, project_id);
CREATE INDEX idx_project_personnel_person ON project_personnel(organisation_id, personnel_id);
```

**Event-based sync**:
- When personnel details change in WRAC → publish event
- PIT listens for event → updates denormalized fields

### 3.2 Threat ↔ Vulnerability

**Threat-Vulnerability relationships** (many-to-many):

```sql
-- Integration table (could live in either module or shared schema)
CREATE TABLE threat_vulnerability_link (
  id UUID PRIMARY KEY DEFAULT generate_uuidv7(),
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  
  threat_id UUID NOT NULL,
  threat_title TEXT,
  vulnerability_id UUID NOT NULL,
  vulnerability_title TEXT,
  
  link_type TEXT NOT NULL, -- 'exploits', 'targets'
  severity TEXT, -- Combined severity assessment
  
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_by UUID NOT NULL REFERENCES users(id),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_by UUID REFERENCES users(id),
  deleted_at TIMESTAMPTZ NULL,
  
  UNIQUE(organisation_id, threat_id, vulnerability_id)
);
```

### 3.3 ERM ↔ Risk Assessment

**Enterprise risks linked to risk assessments**:

```sql
-- ERM: risk_assessment_link (integration table)
CREATE TABLE risk_assessment_link (
  id UUID PRIMARY KEY DEFAULT generate_uuidv7(),
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  
  -- Enterprise risk (within ERM module)
  enterprise_risk_id UUID NOT NULL REFERENCES risk(id),
  
  -- Risk assessment (from Risk Assessment module, no FK)
  risk_assessment_id UUID NOT NULL,
  risk_assessment_title TEXT,
  
  -- Link metadata
  assessment_type TEXT, -- 'initial', 'follow_up', 'annual_review'
  assessment_date DATE,
  
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_by UUID NOT NULL REFERENCES users(id),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_by UUID REFERENCES users(id),
  deleted_at TIMESTAMPTZ NULL,
  
  UNIQUE(organisation_id, enterprise_risk_id, risk_assessment_id)
);
```

### 3.4 Course Crafter ↔ Skills Portal

**Training courses linked to skills development**:

```sql
-- Skills Portal: course_enrollment (integration table)
CREATE TABLE course_enrollment (
  id UUID PRIMARY KEY DEFAULT generate_uuidv7(),
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  
  -- User (from WRAC/Skills Portal)
  user_id UUID NOT NULL REFERENCES users(id),
  
  -- Course (from Course Crafter module, no FK)
  course_id UUID NOT NULL,
  course_title TEXT NOT NULL,
  course_version TEXT,
  
  -- Enrollment details
  enrolled_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  score NUMERIC(5,2),
  status TEXT NOT NULL DEFAULT 'enrolled', -- enrolled, in_progress, completed, failed
  
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_by UUID NOT NULL REFERENCES users(id),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_by UUID REFERENCES users(id),
  deleted_at TIMESTAMPTZ NULL,
  
  UNIQUE(organisation_id, user_id, course_id)
);
```

---

## 4. Referential Integrity Strategies

### 4.1 Application-Level Validation

**Always validate referenced IDs exist before creating links**:

```typescript
// Before linking threat to vulnerability
const vulnerability = await getVulnerability(vulnerabilityId, organisationId);
if (!vulnerability) {
  throw new Error('Vulnerability not found');
}

// Create link
await createThreatVulnerabilityLink({
  threatId,
  vulnerabilityId,
  vulnerabilityTitle: vulnerability.title, // Denormalize
  organisationId
});
```

### 4.2 Eventual Consistency

**Accept eventual consistency for denormalized fields**:

```sql
-- When vulnerability title changes, publish event
INSERT INTO event_log (
  organisation_id,
  event_type,
  source_module,
  source_entity_id,
  payload
) VALUES (
  :org_id,
  'vulnerability_updated',
  'vulnerability',
  :vulnerability_id,
  jsonb_build_object('title', :new_title)
);

-- Threat module listens and updates denormalized fields
UPDATE threat_vulnerability_link
SET vulnerability_title = :new_title,
    updated_at = NOW()
WHERE vulnerability_id = :vulnerability_id
  AND organisation_id = :org_id;
```

### 4.3 Cascade Delete Handling

**Soft delete cascades via events**:

```sql
-- When vulnerability is soft deleted, publish event
INSERT INTO event_log (
  organisation_id,
  event_type,
  source_module,
  source_entity_id
) VALUES (
  :org_id,
  'vulnerability_deleted',
  'vulnerability',
  :vulnerability_id
);

-- Threat module listens and soft deletes links
UPDATE threat_vulnerability_link
SET deleted_at = NOW(),
    deleted_by = :system_user_id
WHERE vulnerability_id = :vulnerability_id
  AND organisation_id = :org_id
  AND deleted_at IS NULL;
```

---

## 5. Event Log Integration

### 5.1 Publishing Events

```sql
-- Publish cross-module event
INSERT INTO event_log (
  organisation_id,
  event_type,
  source_module,
  source_entity_type,
  source_entity_id,
  target_module,
  target_entity_type,
  target_entity_id,
  payload
) VALUES (
  :org_id,
  :event_type,
  :source_module,
  :source_entity_type,
  :source_entity_id,
  :target_module,
  :target_entity_type,
  :target_entity_id,
  :payload_jsonb
);
```

### 5.2 Consuming Events

```sql
-- Get unprocessed events for this module
SELECT 
  id,
  event_type,
  source_module,
  source_entity_id,
  payload
FROM event_log
WHERE organisation_id = :org_id
  AND (target_module = :this_module OR target_module IS NULL)
  AND processed_at IS NULL
ORDER BY timestamp ASC
LIMIT 100;

-- Mark event as processed
UPDATE event_log
SET processed_at = NOW()
WHERE id = :event_id;
```

### 5.3 Event Types

**Standard cross-module events**:
- `entity_created`
- `entity_updated`
- `entity_deleted`
- `entity_linked`
- `entity_unlinked`
- `entity_status_changed`
- `entity_approved`
- `entity_archived`

**Event payload structure**:

```json
{
  "entity_id": "01234567-89ab-7def-0123-456789abcdef",
  "entity_type": "vulnerability",
  "changes": {
    "title": "New Title",
    "severity": "high"
  },
  "metadata": {
    "triggered_by": "user_id",
    "reason": "Manual update"
  }
}
```

---

## 6. Denormalization Patterns

### 6.1 When to Denormalize

✅ **Denormalize when**:
- Read performance is critical
- Data is displayed frequently (e.g., titles in lists)
- Joins across modules are expensive
- Data changes infrequently

❌ **Don't denormalize when**:
- Data changes very frequently
- Storage cost is high
- Consistency is critical (financial data, etc.)

### 6.2 Denormalization Example

```sql
-- Store commonly accessed fields from referenced entity
CREATE TABLE risk_control_link (
  id UUID PRIMARY KEY DEFAULT generate_uuidv7(),
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  
  risk_id UUID NOT NULL REFERENCES risk(id),
  
  -- Control reference (from separate module)
  control_id UUID NOT NULL,
  
  -- Denormalized fields for performance
  control_title TEXT NOT NULL,
  control_type TEXT,
  control_status TEXT,
  
  -- Last sync timestamp
  last_synced_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_by UUID NOT NULL REFERENCES users(id),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_by UUID REFERENCES users(id),
  deleted_at TIMESTAMPTZ NULL
);
```

### 6.3 Sync Strategy

```sql
-- Periodic sync job (or event-based)
UPDATE risk_control_link rcl
SET control_title = c.title,
    control_type = c.type,
    control_status = c.status,
    last_synced_at = NOW()
FROM control c
WHERE rcl.control_id = c.id
  AND rcl.organisation_id = c.organisation_id
  AND rcl.deleted_at IS NULL
  AND c.deleted_at IS NULL
  AND rcl.last_synced_at < c.updated_at; -- Only if control was updated
```

---

## 7. Query Patterns

### 7.1 Get Linked Entities

```sql
-- Get all vulnerabilities linked to a threat
SELECT 
  tvl.id AS link_id,
  tvl.vulnerability_id,
  tvl.vulnerability_title,
  tvl.link_type,
  tvl.created_at
FROM threat_vulnerability_link tvl
WHERE tvl.threat_id = :threat_id
  AND tvl.organisation_id = :org_id
  AND tvl.deleted_at IS NULL
ORDER BY tvl.created_at DESC;
```

### 7.2 Get Entity with Related Counts

```sql
-- Get threat with count of linked vulnerabilities
SELECT 
  t.*,
  COUNT(tvl.id) AS vulnerability_count
FROM threat t
LEFT JOIN threat_vulnerability_link tvl 
  ON tvl.threat_id = t.id 
  AND tvl.organisation_id = t.organisation_id
  AND tvl.deleted_at IS NULL
WHERE t.organisation_id = :org_id
  AND t.deleted_at IS NULL
GROUP BY t.id;
```

---

## 8. Consistency Guarantees

### 8.1 Within Module

- ✅ Strong consistency (ACID transactions)
- ✅ Foreign key constraints enforced
- ✅ Immediate referential integrity

### 8.2 Across Modules

- ⚠️ Eventual consistency (event-driven)
- ⚠️ No database-level FK constraints
- ⚠️ Application-level validation required
- ⚠️ Denormalized data may be stale (but sync'ed regularly)

### 8.3 Trade-offs

**Benefits**:
- Module independence
- Independent scaling
- Deployment flexibility
- No cross-module schema locks

**Costs**:
- Eventual consistency
- More complex error handling
- Application-level integrity checks

---

## 9. Testing Cross-Module Relationships

### 9.1 Integration Tests

```typescript
describe('Threat-Vulnerability Link', () => {
  it('should create link when both entities exist', async () => {
    const threat = await createThreat({ title: 'Test Threat' });
    const vulnerability = await createVulnerability({ title: 'Test Vuln' });
    
    const link = await linkThreatToVulnerability(threat.id, vulnerability.id);
    
    expect(link.threat_id).toBe(threat.id);
    expect(link.vulnerability_id).toBe(vulnerability.id);
    expect(link.vulnerability_title).toBe('Test Vuln'); // Denormalized
  });
  
  it('should fail when vulnerability does not exist', async () => {
    const threat = await createThreat({ title: 'Test Threat' });
    const fakeVulnId = '00000000-0000-0000-0000-000000000000';
    
    await expect(linkThreatToVulnerability(threat.id, fakeVulnId))
      .rejects.toThrow('Vulnerability not found');
  });
  
  it('should update denormalized fields when vulnerability changes', async () => {
    const link = await createThreatVulnerabilityLink();
    
    await updateVulnerability(link.vulnerability_id, { title: 'New Title' });
    await processEvents(); // Process event queue
    
    const updatedLink = await getLink(link.id);
    expect(updatedLink.vulnerability_title).toBe('New Title');
  });
});
```

---

## 10. Conclusion

Cross-module relationships in Maturion ISMS are designed for:

- ✅ Module independence
- ✅ Loose coupling
- ✅ Event-driven integration
- ✅ Eventual consistency
- ✅ Performance optimization
- ✅ Scalability

**Key Patterns**:
1. No direct FK constraints across modules
2. Integration tables for many-to-many relationships
3. Denormalize frequently accessed fields
4. Event-driven sync for consistency
5. Application-level validation

---

**Prepared by**: Maturion Foreman  
**Build Wave**: 1.2  
**Date**: 2025-12-04
