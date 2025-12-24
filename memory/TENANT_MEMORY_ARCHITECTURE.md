# Tenant Memory Architecture (Design-Only, NOT ACTIVATED)

**STATUS: DESIGN ONLY — NOT ACTIVE — NOT ENABLED — NOT PERSISTENT**

---

## ⚠️ CRITICAL NOTICE

This document defines the **architectural design** for tenant-specific memory in the Maturion ISMS ecosystem.

**THIS DESIGN IS NOT ACTIVATED.**

- ❌ No runtime persistence
- ❌ No tenant memory writes
- ❌ No cross-tenant access
- ❌ No production enablement
- ✅ Design and simulation only
- ✅ Safe for testing during build
- ✅ Deletable per tenant
- ✅ Resettable at any time

---

## Purpose

Define the tenant-specific memory architecture required for ISMS at go-live, while keeping it completely inactive during development and build phases.

This enables:
- Safe testing and simulation during build
- Architecture validation without risk
- Clear boundaries and isolation rules
- Governance retention of activation authority

---

## Context

### Why Tenant Memory is Required

At ISMS go-live, tenant-specific memory will be required for:

1. **Tenant-Specific Configuration Memory**
   - Custom compliance frameworks
   - Organization-specific policies
   - Approval workflows
   - Risk assessment criteria

2. **Tenant-Specific Operational Memory**
   - Incident response patterns (anonymized)
   - Audit preparation lessons
   - Compliance validation outcomes
   - Performance optimization insights

3. **Tenant-Specific Learning Memory**
   - Usage patterns (privacy-preserving)
   - Feature adoption feedback
   - User workflow improvements
   - Admin intelligence insights

### Why It Must NOT Be Activated Now

During build and development:
- Risk of premature data persistence
- Complexity of tenant isolation testing
- Governance validation not yet complete
- Production-grade security not yet audited
- Could introduce unintended data leakage

**Solution: Design now, activate later, under governance control.**

---

## Tenant Memory Boundaries

### Scope Definition

Tenant memory operates within a **strict isolation boundary**:

```
Tenant Memory Boundary:
┌────────────────────────────────────────────┐
│ Tenant: org-uuid-xxxx                      │
│ ┌────────────────────────────────────────┐ │
│ │ Tenant Memory Fabric                   │ │
│ │ - Configuration memory                 │ │
│ │ - Operational memory (anonymized)      │ │
│ │ - Learning memory (privacy-preserving) │ │
│ │ - Admin insights                       │ │
│ └────────────────────────────────────────┘ │
│                                            │
│ ISOLATION ENFORCED:                        │
│ - No cross-tenant reads                    │
│ - No cross-tenant writes                   │
│ - No cross-tenant references               │
│ - Encrypted at rest                        │
│ - Tenant-key encryption                    │
└────────────────────────────────────────────┘
```

### Tenant Memory Scopes

Tenant memory extends the existing memory scope model:

| Scope | Description | Activation Status |
|-------|-------------|-------------------|
| `global` | Platform-wide, all tenants | ✅ Active (read-only) |
| `foreman` | Build-time governance | ✅ Active (limited write) |
| `platform` | Runtime platform events | ✅ Active (read-only) |
| `tenant:{org_id}` | Tenant-specific memory | ❌ **NOT ACTIVE** |

### Tenant Memory Structure

```
memory/
├── global/              # Active - platform-wide memory
├── foreman/             # Active - build-time memory
├── platform/            # Active - runtime platform memory
└── tenant/              # NOT ACTIVE - tenant-specific memory
    ├── NOT_ACTIVE.md    # Explicit deactivation marker
    ├── SIMULATION_MODE.md
    └── {org_id}/        # Per-tenant directories (simulated)
        ├── config/      # Tenant configuration memory
        ├── operational/ # Operational patterns (anonymized)
        ├── learning/    # Learning insights (privacy-safe)
        └── metadata.json
```

---

## Isolation Rules

### Rule 1: Absolute Tenant Isolation

**Requirement:**
- Each tenant's memory MUST be completely isolated from all other tenants.

**Enforcement (when activated):**
- Database: Row-level security with `organisation_id` filter
- File system: Separate directories per `org_id`
- API: Middleware enforces tenant context from authentication
- Memory loading: Always filtered by authenticated tenant ID
- No cross-tenant queries permitted under any circumstance

**Current Status:**
- ❌ Not enforced (not activated)
- ✅ Architecture documented
- ✅ Validation checklist created

### Rule 2: Privacy-Preserving Memory Only

**Requirement:**
- Tenant memory MUST NOT contain PII or sensitive user data.

**Allowed:**
- ✅ Anonymized patterns
- ✅ Aggregate statistics (min 10 users)
- ✅ Configuration preferences
- ✅ Non-identifiable workflow insights

**Prohibited:**
- ❌ User names, emails, IDs
- ❌ Individual user actions
- ❌ Raw audit logs with PII
- ❌ Specific document contents
- ❌ Financial data
- ❌ Health information

**Current Status:**
- ❌ Not enforced (not activated)
- ✅ Privacy rules documented
- ✅ Validation schema defined

### Rule 3: No Cross-Tenant References

**Requirement:**
- Tenant memory entries MUST NOT reference other tenants.

**Enforcement:**
- Memory validation rejects entries with cross-tenant links
- No `tenant:{other_org_id}` references in memory
- No comparative analytics across tenants
- No "similar to tenant X" patterns

**Current Status:**
- ❌ Not enforced (not activated)
- ✅ Validation rules documented

### Rule 4: Tenant-Owned Deletion

**Requirement:**
- Tenants MUST be able to delete their memory completely.

**Capabilities (when activated):**
- One-command memory deletion per tenant
- Cascading deletion of all tenant memory entries
- Audit log of deletion (no recovery)
- GDPR-compliant "right to be forgotten"

**Current Status:**
- ❌ Not implemented (not activated)
- ✅ Deletion script designed (not active)
- ✅ Reset procedure documented

---

## Access Mediation Model

### Access Control Layers

```
Request Flow (when activated):
┌─────────────────────────────────────────────┐
│ 1. Authentication Layer                     │
│    - Verify user identity                   │
│    - Extract organisation_id from token     │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│ 2. Tenant Context Layer                     │
│    - Validate tenant access                 │
│    - Inject tenant context into request     │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│ 3. Memory Access Mediation                  │
│    - Filter by tenant scope                 │
│    - Enforce isolation rules                │
│    - Validate no cross-tenant access        │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│ 4. Memory Fabric                            │
│    - Load tenant-specific memory            │
│    - Return only tenant's data              │
└─────────────────────────────────────────────┘
```

### API Mediation (Design)

**Endpoint Design (not implemented):**

```typescript
// Load tenant memory (requires authentication)
GET /api/memory/tenant
Authorization: Bearer {tenant_jwt}

Response:
{
  "tenant_id": "org-uuid-xxxx",
  "memories": [...],  // Only this tenant's memories
  "count": 42,
  "scope": "tenant:org-uuid-xxxx"
}

// Write tenant memory (requires authentication + permission)
POST /api/memory/tenant
Authorization: Bearer {tenant_jwt}
Body: { memory_entry }

Response:
{
  "tenant_id": "org-uuid-xxxx",
  "memory_id": "mem-tenant-yyyy",
  "status": "created"
}
```

**Security Controls:**
- JWT must contain `organisation_id`
- Middleware validates tenant context
- Memory operations scoped to authenticated tenant only
- No wildcard or cross-tenant queries allowed
- Audit log for all tenant memory access

**Current Status:**
- ❌ Not implemented (not activated)
- ✅ API design documented
- ✅ Security controls defined

---

## Simulation and Reset Strategy

### Simulation Mode

**Purpose:** Allow testing of tenant memory architecture without activation.

**Characteristics:**
- Memory operations return simulated data
- No persistent writes
- Safe for development and testing
- Resettable at any time
- Clearly marked as simulation

**Implementation (not active):**

```typescript
// Simulation flag in memory client
const memoryClient = createMemoryClient({
  mode: 'simulation',  // or 'production'
  tenant: 'org-test-xxxx'
});

// All operations return simulated data
const memories = await memoryClient.loadTenantMemory();
// Returns: Sample tenant memories (non-persistent)
```

**Simulation Data Sources:**
- Static JSON fixtures in `/memory/tenant/simulation/`
- Generated on-the-fly with consistent UUIDs
- No database interaction
- No file system writes

**Current Status:**
- ❌ Not implemented (not activated)
- ✅ Simulation strategy documented
- ✅ Test fixtures designed

### Reset Procedures

**Development Reset:**

```bash
# Reset all tenant memory (simulation only)
python3 scripts/reset-tenant-memory.py --mode simulation --all

# Reset specific tenant (simulation only)
python3 scripts/reset-tenant-memory.py --mode simulation --tenant org-uuid-xxxx
```

**Production Reset (future, when activated):**

```bash
# Requires explicit confirmation
python3 scripts/reset-tenant-memory.py --mode production --tenant org-uuid-xxxx --confirm

# Audit log generated
# GDPR compliance verified
# No recovery possible
```

**Reset Capabilities:**
- Delete all tenant memory entries
- Clear tenant metadata
- Regenerate tenant memory structure
- Audit log capture
- Confirmation required

**Current Status:**
- ❌ Scripts not active
- ✅ Reset procedures documented
- ✅ Audit requirements defined

---

## Kill-Switch Design

### Purpose

Provide immediate deactivation of tenant memory if issues arise.

### Kill-Switch Mechanism

**Kill-Switch File:** `/memory/tenant/KILL_SWITCH_ACTIVE`

**When Kill-Switch is Active:**
- All tenant memory reads return empty
- All tenant memory writes fail silently (logged)
- System continues to function with global memory only
- Admin dashboard shows kill-switch status
- Escalation to governance required

**Activation:**

```bash
# Activate kill-switch (immediate effect)
touch /memory/tenant/KILL_SWITCH_ACTIVE

# Deactivate kill-switch (after governance approval)
rm /memory/tenant/KILL_SWITCH_ACTIVE
```

**Runtime Check:**

```typescript
// Memory client checks kill-switch before every operation
async loadTenantMemory(tenantId: string) {
  if (await isKillSwitchActive()) {
    console.warn('Tenant memory kill-switch active, returning empty');
    return [];
  }
  // Continue with normal loading...
}
```

**Kill-Switch Scenarios:**
- Security vulnerability discovered
- Cross-tenant data leak detected
- Privacy violation suspected
- Compliance audit failure
- Performance degradation
- Emergency governance decision

**Current Status:**
- ❌ Not implemented (not activated)
- ✅ Kill-switch design documented
- ✅ Activation procedure defined

---

## Activation Authority and Governance

### Activation is Governance-Controlled

**Authority:** Johan Ras (Governance) ONLY

**Pre-Activation Requirements:**

- [ ] Security audit completed and passed
- [ ] Privacy impact assessment approved
- [ ] Tenant isolation tested and verified
- [ ] Compliance validation completed
- [ ] Performance benchmarks met
- [ ] Monitoring and alerting configured
- [ ] Kill-switch tested and operational
- [ ] Deletion procedures tested
- [ ] GDPR compliance verified
- [ ] Governance approval documented

**Activation Procedure (future):**

1. Governance reviews activation checklist
2. Security audit results reviewed
3. Privacy assessment approved
4. Governance issues activation command
5. Tenant memory enabled in production
6. Monitoring begins immediately
7. First-week audit scheduled

**Current Status:**
- ❌ Activation checklist not complete
- ❌ Tenant memory NOT ACTIVATED
- ✅ Activation requirements documented
- ✅ Governance approval process defined

---

## Testing Strategy (Simulation Only)

### Test Scenarios

**Test 1: Tenant Isolation**
- Create memory for Tenant A
- Attempt to read as Tenant B
- Verify empty result
- Status: ❌ Not implemented (not activated)

**Test 2: Privacy Enforcement**
- Attempt to write PII to tenant memory
- Verify rejection
- Verify validation error
- Status: ❌ Not implemented (not activated)

**Test 3: Kill-Switch**
- Activate kill-switch
- Attempt tenant memory operations
- Verify operations fail safely
- Verify system continues with global memory
- Status: ❌ Not implemented (not activated)

**Test 4: Tenant Deletion**
- Create tenant memory
- Execute deletion procedure
- Verify complete removal
- Verify audit log created
- Status: ❌ Not implemented (not activated)

**Test 5: Simulation Mode**
- Enable simulation mode
- Perform memory operations
- Verify no persistence
- Verify reset works
- Status: ❌ Not implemented (not activated)

### Test Execution

**Current Status:**
- All tests are simulated only
- No production data used
- No persistent writes
- Safe for development

---

## Compliance and Privacy

### GDPR Compliance

**Right to Access:**
- Tenant can export all their memory
- JSON format
- Complete and transparent

**Right to Deletion:**
- One-command deletion
- Cascading and complete
- Audit trail maintained
- No recovery

**Right to Portability:**
- Export in machine-readable format
- Import to new tenant (if needed)
- Standard JSON schema

**Privacy by Design:**
- No PII in memory entries
- Anonymized patterns only
- Aggregate statistics (min 10 users)
- Privacy-preserving by default

**Current Status:**
- ❌ GDPR features not implemented (not activated)
- ✅ GDPR requirements documented
- ✅ Compliance design validated

---

## Integration with Existing Memory Fabric

### Current Memory Fabric (Active)

```
memory/
├── schema/
│   └── memory-entry.json      # Memory entry schema (active)
├── global/                     # Global memory (active, read-only)
├── foreman/                    # Foreman memory (active, limited write)
└── platform/                   # Platform memory (active, read-only)
```

### Extended Memory Fabric (Design)

```
memory/
├── schema/
│   ├── memory-entry.json      # Extended to support tenant scope
│   └── tenant-memory.json     # Tenant-specific schema (design only)
├── global/                     # Global memory (active)
├── foreman/                    # Foreman memory (active)
├── platform/                   # Platform memory (active)
└── tenant/                     # ❌ NOT ACTIVE
    ├── NOT_ACTIVE.md           # Deactivation marker
    ├── KILL_SWITCH_ACTIVE      # Kill-switch file (if active)
    ├── simulation/             # Simulation fixtures
    └── {org_id}/               # Per-tenant directories (not created)
```

### Schema Extension (Design Only)

**Current `memory-entry.json` scope values:**
```json
{
  "scope": {
    "allowed_values": [
      "global",
      "foreman",
      "isms",
      "partpulse",
      "runtime"
    ]
  }
}
```

**Extended scope values (design only):**
```json
{
  "scope": {
    "allowed_values": [
      "global",
      "foreman",
      "isms",
      "partpulse",
      "runtime",
      "tenant:{org_id}"    // ← New, not active
    ]
  }
}
```

**Current Status:**
- ❌ Schema not modified
- ✅ Extension design documented
- ✅ Backward compatibility ensured

---

## Implementation Phases (Future)

### Phase 1: Design and Simulation (Current)

- ✅ Architecture documented
- ✅ Isolation rules defined
- ✅ Simulation strategy created
- ✅ Kill-switch designed
- ❌ NOT ACTIVATED

### Phase 2: Security and Privacy Audit (Future)

- Security audit
- Privacy impact assessment
- Compliance validation
- Governance approval

### Phase 3: Implementation (Future, Post-Approval)

- Implement tenant memory persistence
- Implement access mediation
- Implement kill-switch runtime checks
- Implement deletion procedures

### Phase 4: Testing and Validation (Future)

- Tenant isolation testing
- Privacy enforcement testing
- Kill-switch testing
- Performance testing

### Phase 5: Production Activation (Future)

- Governance approval
- Production deployment
- Monitoring activation
- First-week audit

**Current Phase: Phase 1 (Design Only)**

---

## Explicit Deactivation Statement

### 🔴 TENANT MEMORY IS NOT ACTIVE

This document is a **design specification only**.

**Tenant memory is explicitly NOT:**
- ❌ Implemented in runtime code
- ❌ Persisting data to disk or database
- ❌ Accessible via APIs
- ❌ Enabled in any environment
- ❌ Processing real tenant data

**This design:**
- ✅ Can be tested in simulation mode
- ✅ Can be validated for correctness
- ✅ Can be reviewed for compliance
- ✅ Will be activated ONLY after governance approval

**Activation is governance-controlled and requires explicit approval.**

---

## References

- **Memory Schema:** `/memory/schema/memory-entry.json`
- **Global Memory Runtime:** `/GLOBAL_MEMORY_RUNTIME_README.md`
- **Memory Wave 2 Overview:** `/MEMORY_WAVE_2_README.md`
- **Privacy Guardrails:** `/foreman/privacy-guardrails.md` (relocated to governance repo)
- **Memory Model:** `/foreman/memory-model.md` (relocated to governance repo)
- **Authority Policy:** `/memory/AUTHORITY/MEMORY_WRITE_POLICY.md`

---

## Compliance Statement

This design:

✅ Respects privacy guardrails  
✅ Enforces strict tenant isolation  
✅ Provides GDPR-compliant deletion  
✅ Includes kill-switch for emergency deactivation  
✅ Maintains governance approval authority  
✅ Documents simulation and testing strategy  
✅ Explicitly states: **NOT ACTIVE**  

**No tenant memory is activated or persisted by this design.**

---

**End of Tenant Memory Architecture Design**

**STATUS: DESIGN ONLY — NOT ACTIVE — NOT ENABLED — NOT PERSISTENT**
