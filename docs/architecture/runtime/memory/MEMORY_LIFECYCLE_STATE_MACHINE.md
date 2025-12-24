# FM Runtime Memory Lifecycle State Machine Architecture

**Document Type:** Architecture Specification  
**Version:** 1.0.0  
**Status:** Draft  
**Owner:** Maturion Foreman  
**Created:** 2025-12-24

---

## 1. Purpose

This document defines the **runtime architecture** for implementing the memory lifecycle contract in the FM (Foreman Maturion) application. It specifies the state machine, components, transitions, and failure handling mechanisms that govern how memory moves from initialization through load, validation, and usable states at runtime.

This is an **architecture and specification document only** - no implementation is included.

---

## 2. Scope

This architecture applies to:

- **FM Runtime Agent** - Active monitoring and platform intelligence
- **Memory Fabric** - Unified, persistent, version-controlled memory system
- **All agents** (Foreman, builders, platform) that interact with memory at runtime

This architecture is **separate from but aligned with**:
- Build-time memory behavior (see `foreman/behaviours/memory-rules.md`)
- Memory ingestion specification (see `foreman/runtime-memory-ingestion.md`)
- Memory model and privacy guardrails (canonical versions in maturion-foreman-governance)

---

## 3. Memory Lifecycle States

The memory lifecycle consists of **5 primary states**:

### 3.1 State: UNINITIALIZED

**Description:** Memory fabric has not been detected or validated.

**Entry Conditions:**
- Application startup before memory check
- New repository without memory structure
- Memory directory deleted or corrupted

**Allowed Actions:**
- Detect memory fabric presence
- Initiate health check
- Trigger auto-initialization if missing

**Exit Conditions:**
- Memory directory structure detected → Move to LOADING
- Auto-initialization completed → Move to LOADING
- Fatal error (cannot initialize) → Move to FAILED

**Runtime Behavior:**
- ❌ All agent reasoning blocked
- ❌ All builds blocked
- ❌ All memory reads/writes blocked
- ✅ System health checks allowed (for diagnosis)

---

### 3.2 State: LOADING

**Description:** Memory fabric is being loaded from storage into runtime cache.

**Entry Conditions:**
- UNINITIALIZED → Memory structure detected
- DEGRADED → Attempting recovery
- Runtime restart/redeploy

**Responsibilities:**
1. **Load memory schema** (`memory/schema/memory-entry.json`)
2. **Load scope directories** (`global/`, `foreman/`, `platform/`, `runtime/`)
3. **Parse and index entries** by scope, tags, importance
4. **Build search indices** for fast filtering
5. **Cache critical memories** in working memory

**Allowed Actions:**
- Read memory files from disk/git
- Parse JSON entries
- Validate file structure (not content yet)
- Build in-memory indices

**Exit Conditions:**
- All required scopes loaded successfully → Move to VALIDATING
- Partial load (degraded mode eligible) → Move to DEGRADED
- Critical load failure → Move to FAILED

**Timeout:** 30 seconds (configurable)

**Runtime Behavior:**
- ❌ Agent reasoning blocked
- ❌ Builds blocked
- ❌ Memory writes blocked
- ✅ Health checks continue
- ✅ Loading progress reported to monitoring

---

### 3.3 State: VALIDATING

**Description:** Memory entries are being validated against schema and governance rules.

**Entry Conditions:**
- LOADING → All files loaded successfully

**Validation Checks:**

1. **Schema Compliance**
   - All entries conform to `memory-entry.json` schema
   - Required fields present: `id`, `timestamp`, `scope`, `title`, `summary`, `importance`, `tags`
   - Field types correct
   - Tag format valid

2. **Scope Integrity**
   - Entries in correct scope directories
   - No cross-scope contamination
   - Scope values match directory location

3. **Privacy Compliance**
   - No PII in memory entries
   - No tenant-specific identifiable data
   - No secrets or credentials
   - Compliance with privacy guardrails

4. **Temporal Consistency**
   - Timestamps realistic (not future-dated)
   - Date-based collection files ordered correctly
   - No duplicate IDs

5. **Reference Integrity**
   - Cross-references to valid entries
   - No orphaned references
   - Module references valid

**Allowed Actions:**
- Validate entries against schema
- Check privacy compliance
- Verify temporal consistency
- Log validation warnings/errors

**Exit Conditions:**
- All validations pass → Move to USABLE
- Critical validations fail, but degraded mode possible → Move to DEGRADED
- Critical validations fail, degraded mode not possible → Move to FAILED

**Timeout:** 60 seconds (configurable)

**Runtime Behavior:**
- ❌ Agent reasoning blocked (still loading)
- ❌ Builds blocked
- ❌ Memory writes blocked (read-only validation)
- ✅ Health checks continue
- ✅ Validation progress reported

---

### 3.4 State: USABLE

**Description:** Memory fabric is fully loaded, validated, and operational.

**Entry Conditions:**
- VALIDATING → All validation checks passed
- DEGRADED → Recovery successful, all checks now pass

**Guarantees:**
- All memory scopes available
- All entries schema-compliant
- Privacy guardrails enforced
- Search indices built and ready
- Write operations safe

**Allowed Actions:**
- ✅ Read memory (all scopes, tags, importance levels)
- ✅ Write memory (with validation)
- ✅ Agent reasoning and builds (memory context loaded)
- ✅ Memory queries and filters
- ✅ Health monitoring continues

**Exit Conditions:**
- Memory corruption detected → Move to VALIDATING (revalidate)
- Partial failure (e.g., scope unavailable) → Move to DEGRADED
- Critical failure → Move to FAILED

**Runtime Behavior:**
- ✅ **Full operational mode**
- All agents may proceed with memory-dependent actions
- Foreman may accept builds and dispatch tasks
- Runtime agent may process monitoring events

**Health Monitoring:**
- Continuous validation of new writes
- Periodic revalidation of existing entries (configurable)
- Anomaly detection (unexpected schema changes, corruption)

---

### 3.5 State: DEGRADED

**Description:** Memory fabric is partially operational. Some scopes or entries unavailable, but critical functionality preserved.

**Entry Conditions:**
- LOADING → Partial load failure (non-critical scope missing)
- VALIDATING → Non-critical validation failures
- USABLE → Partial corruption detected

**Degraded Mode Eligibility:**

**Allowed Degradation Scenarios:**
1. **Non-critical scope missing** (e.g., `runtime/` missing, but `global/` and `foreman/` available)
2. **Validation warnings** (non-blocking issues like future timestamps within tolerance)
3. **Performance degradation** (slow reads, but still functional)

**NOT Allowed (Must Fail):**
1. **Critical scope missing** (`global/` or `foreman/` unavailable)
2. **Schema corruption** (cannot parse entries)
3. **Privacy violations** (PII detected)

**Degraded Capabilities:**
- ✅ Read from available scopes
- ✅ Limited agent reasoning (with warnings)
- ⚠️ Builds allowed with explicit approval (Foreman must acknowledge degraded state)
- ⚠️ Memory writes validated extra strictly
- ❌ No auto-fix actions (too risky without full context)

**Exit Conditions:**
- Recovery successful (missing scope restored, validation passes) → Move to USABLE
- Recovery failed or new critical failure → Move to FAILED

**Timeout:** 5 minutes (attempt recovery, then decide)

**Runtime Behavior:**
- ⚠️ **Limited operational mode**
- Foreman warned: "Memory degraded, proceed with caution"
- Johan notified: "Memory fabric degraded, recovery in progress"
- All actions logged at elevated level (audit trail)

---

### 3.6 State: FAILED

**Description:** Memory fabric is non-operational. Critical failure prevents safe operation.

**Entry Conditions:**
- LOADING → Critical load failure (e.g., `global/` missing)
- VALIDATING → Critical validation failure (e.g., schema corruption, PII detected)
- DEGRADED → Recovery failed or timeout exceeded
- USABLE → Catastrophic corruption detected

**Failure Modes:**

#### **Hard Stop (Immediate Halt)**

Trigger conditions:
1. **Critical scope missing** - `global/` or `foreman/` directories not found
2. **Schema corruption** - Cannot parse or validate memory entries
3. **Privacy violation** - PII, secrets, or tenant data detected in memory
4. **Security breach** - Unauthorized memory modification detected

**Behavior:**
- ❌ All agent reasoning halted
- ❌ All builds blocked
- ❌ All memory reads/writes blocked
- ❌ Runtime agent in safe mode (monitoring only, no actions)
- 🚨 **Escalation to Johan** - Immediate notification with diagnostic context

#### **Degrade (Partial Operation)**

Trigger conditions:
1. **Non-critical scope missing** - `runtime/` or `platform/` unavailable
2. **Performance issues** - Slow reads, high latency (still functional)
3. **Validation warnings** - Non-blocking issues

**Behavior:**
- ⚠️ Limited operation (degraded mode, see State 3.5)
- ⚠️ Elevated logging and monitoring
- 📢 Notification to Johan - "Memory degraded, monitoring for recovery"

**Recovery Actions:**

1. **Automated Recovery** (if safe):
   - Re-initialize missing scopes
   - Re-validate entries
   - Rebuild indices
   - Retry load

2. **Manual Intervention Required**:
   - Privacy violations → Manual audit required
   - Schema corruption → Manual repair required
   - Security breach → Manual investigation required

**Exit Conditions:**
- Manual recovery completed → Move to LOADING (restart cycle)
- Auto-recovery successful → Move to LOADING
- No recovery possible → Remain in FAILED (awaiting intervention)

**Runtime Behavior:**
- 🚨 **Emergency mode**
- System operates in minimal safe mode
- No memory-dependent actions allowed
- Health checks continue (for diagnostics)
- All actions logged for post-mortem

---

## 4. State Transition Diagram

```
┌─────────────────┐
│  UNINITIALIZED  │ (Startup / No memory detected)
└────────┬────────┘
         │ Detect/Initialize
         ▼
┌─────────────────┐
│     LOADING     │ (Loading files, parsing, indexing)
└────────┬────────┘
         │ Load complete
         ▼
┌─────────────────┐
│   VALIDATING    │ (Schema, privacy, integrity checks)
└────┬────────┬───┘
     │        │
     │ Pass   │ Partial fail
     ▼        ▼
┌─────────┐  ┌─────────────┐
│ USABLE  │  │  DEGRADED   │ (Limited operation)
└────┬────┘  └─────┬───────┘
     │             │
     │ Corruption  │ Recovery or fail
     ▼             ▼
┌──────────────────────────┐
│        FAILED            │ (Hard stop or degrade)
└──────────────────────────┘
          │
          │ Manual/Auto recovery
          ▼
     (Back to LOADING)
```

---

## 5. Runtime Components

### 5.1 Memory Lifecycle Manager

**Responsibility:** Orchestrates state transitions and enforces lifecycle rules.

**Key Functions:**
- `initialize()` - Detect and initialize memory fabric
- `load()` - Load memory entries from storage
- `validate()` - Validate entries against schema and governance
- `setState(newState)` - Transition to new state with logging
- `getState()` - Return current state
- `healthCheck()` - Return lifecycle health status

**Interfaces:**
- Consumed by: Foreman, Runtime Agent, Builder Agents
- Consumes: Memory Store, Schema Validator, Privacy Checker

---

### 5.2 Memory Store

**Responsibility:** Persistent storage and retrieval of memory entries.

**Key Functions:**
- `loadScope(scopeName)` - Load all entries from a scope directory
- `writeEntry(entry)` - Write new memory entry (with validation)
- `queryEntries(scopes, tags, importanceMin)` - Filter and return entries
- `rebuildIndex()` - Rebuild search indices

**Storage Layers:**
- **Primary:** Git-versioned JSON files (`memory/{scope}/{date}.json`)
- **Cache:** In-memory index for fast queries (Redis/Memcached)
- **Archive:** Compressed long-term storage (optional)

**Interfaces:**
- Consumed by: Memory Lifecycle Manager
- Consumes: File system, Git, Cache layer

---

### 5.3 Schema Validator

**Responsibility:** Validate memory entries against JSON schema.

**Key Functions:**
- `validateEntry(entry)` - Validate single entry against schema
- `validateScope(scopeEntries)` - Validate all entries in scope
- `getSchemaVersion()` - Return current schema version

**Validation Rules:**
- Required fields present
- Field types correct
- Tag format valid (`[a-z0-9_-]+`)
- Importance level valid (`low`, `medium`, `high`, `critical`)
- Scope matches directory location

**Interfaces:**
- Consumed by: Memory Lifecycle Manager, Memory Store
- Consumes: Schema definition (`memory/schema/memory-entry.json`)

---

### 5.4 Privacy Checker

**Responsibility:** Enforce privacy guardrails on memory entries.

**Key Functions:**
- `scanForPII(entry)` - Detect PII in memory content
- `scanForSecrets(entry)` - Detect credentials, API keys, secrets
- `scanForTenantData(entry)` - Detect tenant-specific identifiable data
- `reportViolation(entry, violationType)` - Log and escalate privacy violation

**Detection Techniques:**
- Regex patterns (email, phone, credit card)
- Named entity recognition (person names, organizations)
- Keyword blocklists (API keys, passwords, tokens)
- Cross-reference with tenant data (no tenant IDs, org names)

**Interfaces:**
- Consumed by: Memory Lifecycle Manager, Memory Store (on write)
- Consumes: Privacy guardrails policy, blocklists

---

### 5.5 Health Monitor

**Responsibility:** Continuous monitoring of memory fabric health.

**Key Functions:**
- `checkLifecycleState()` - Monitor state transitions
- `checkLoadTime()` - Monitor load performance
- `checkValidationErrors()` - Track validation failures
- `checkPrivacyViolations()` - Monitor for privacy breaches
- `alertOnAnomaly(anomalyType)` - Escalate health issues

**Metrics Tracked:**
- Load time (target: <30s)
- Validation time (target: <60s)
- Validation error rate (target: <1%)
- Privacy violation count (target: 0)
- State transition frequency (detect thrashing)

**Interfaces:**
- Consumed by: Foreman, Watchdog, Runtime Agent
- Consumes: Memory Lifecycle Manager, Telemetry system

---

## 6. Failure Mode Handling

### 6.1 Hard Stop Scenarios

**When to Hard Stop:**

1. **Critical Scope Missing**
   - `global/` or `foreman/` directory not found
   - **Why:** Cannot proceed without governance and architecture memory
   - **Action:** Block all operations, escalate to Johan

2. **Schema Corruption**
   - Cannot parse memory entries
   - Schema version mismatch
   - **Why:** Cannot trust data integrity
   - **Action:** Block all operations, require manual repair

3. **Privacy Violation**
   - PII detected in memory entries
   - Secrets or credentials found
   - **Why:** Governance violation, legal risk
   - **Action:** Block all operations, require manual audit

4. **Security Breach**
   - Unauthorized memory modification
   - Tampering detected
   - **Why:** Integrity compromised
   - **Action:** Block all operations, forensic investigation

**Hard Stop Procedure:**
1. Immediately transition to FAILED state
2. Log full diagnostic context
3. Escalate to Johan with:
   - Failure mode
   - Affected scopes/entries
   - Recommended recovery action
   - Time-bound urgency
4. Block all memory-dependent actions
5. Await manual intervention

---

### 6.2 Degraded Mode Scenarios

**When to Degrade (Instead of Stop):**

1. **Non-Critical Scope Missing**
   - `runtime/` or `platform/` directory missing
   - **Why:** Core governance still intact
   - **Action:** Operate with warnings, attempt recovery

2. **Performance Degradation**
   - Load time exceeds threshold (>30s)
   - High query latency
   - **Why:** Still functional, just slow
   - **Action:** Operate with elevated monitoring

3. **Validation Warnings**
   - Non-blocking issues (e.g., missing optional fields)
   - Future timestamps within tolerance
   - **Why:** Not critical, still safe
   - **Action:** Log warnings, proceed

4. **Partial Index Corruption**
   - Search index rebuild required
   - **Why:** Can rebuild, underlying data intact
   - **Action:** Operate with degraded query performance

**Degraded Mode Procedure:**
1. Transition to DEGRADED state
2. Log degradation reason
3. Notify Foreman and Johan
4. Enable elevated monitoring
5. Attempt auto-recovery (if safe)
6. Allow limited operations with explicit warnings

---

### 6.3 Recovery Strategies

#### **Automatic Recovery**

1. **Re-initialize Missing Scopes**
   - Create directory structure
   - Copy seed memories from Foreman repo
   - Validate initialization

2. **Rebuild Indices**
   - Parse all entries
   - Rebuild search index
   - Validate integrity

3. **Reload Memory Fabric**
   - Clear cache
   - Re-read from disk
   - Re-validate

#### **Manual Recovery**

1. **Privacy Violation**
   - Audit all entries
   - Remove violating content
   - Re-validate

2. **Schema Corruption**
   - Restore from Git history
   - Manually repair entries
   - Re-validate

3. **Security Breach**
   - Forensic analysis
   - Identify and remove tampered entries
   - Restore from trusted backup

---

## 7. Transition Observability Points

### 7.1 Observable Events

Every state transition MUST emit an observable event:

| Event Type | Trigger | Data Included |
|------------|---------|---------------|
| `memory.lifecycle.uninitialized` | Enter UNINITIALIZED | Reason, detection method |
| `memory.lifecycle.loading.start` | Enter LOADING | Scopes to load, timeout |
| `memory.lifecycle.loading.progress` | During LOADING | Scopes loaded, remaining |
| `memory.lifecycle.loading.complete` | Exit LOADING | Load time, entries loaded |
| `memory.lifecycle.validating.start` | Enter VALIDATING | Validation checks planned |
| `memory.lifecycle.validating.progress` | During VALIDATING | Checks completed, remaining |
| `memory.lifecycle.validating.complete` | Exit VALIDATING | Validation time, pass/fail |
| `memory.lifecycle.usable` | Enter USABLE | Total entries, scopes available |
| `memory.lifecycle.degraded` | Enter DEGRADED | Degradation reason, affected scopes |
| `memory.lifecycle.failed` | Enter FAILED | Failure mode, recovery required |
| `memory.lifecycle.recovery.attempt` | Recovery start | Recovery strategy |
| `memory.lifecycle.recovery.success` | Recovery success | Time to recover |
| `memory.lifecycle.recovery.failed` | Recovery failure | Failure reason |

---

### 7.2 Event Consumers

**Foreman (Build-Time):**
- Monitors: `memory.lifecycle.usable`, `memory.lifecycle.degraded`, `memory.lifecycle.failed`
- Actions: Block builds if not USABLE, warn if DEGRADED, escalate if FAILED

**Watchdog (Runtime):**
- Monitors: All lifecycle events
- Actions: Alert on DEGRADED or FAILED, track recovery time, escalate if recovery fails

**Johan Dashboard:**
- Monitors: All lifecycle events
- Display: Real-time state, transition history, health metrics

**Telemetry System:**
- Monitors: All lifecycle events
- Storage: Time-series data for trend analysis

---

### 7.3 Observability Interfaces

#### **Health Check Endpoint** (Conceptual)

```typescript
GET /api/internal/memory/health

Response:
{
  "state": "USABLE",
  "stateEnteredAt": "2025-12-24T13:00:00Z",
  "stateDurationSec": 3600,
  "lastTransition": {
    "from": "VALIDATING",
    "to": "USABLE",
    "at": "2025-12-24T13:00:00Z",
    "reason": "All validation checks passed"
  },
  "scopes": {
    "global": "available",
    "foreman": "available",
    "platform": "available",
    "runtime": "available"
  },
  "metrics": {
    "loadTimeSec": 12,
    "validationTimeSec": 45,
    "totalEntries": 1234,
    "validationErrors": 0,
    "privacyViolations": 0
  },
  "degradations": [],
  "recommendations": []
}
```

#### **State History Endpoint** (Conceptual)

```typescript
GET /api/internal/memory/lifecycle/history?since=2025-12-20

Response:
{
  "transitions": [
    {
      "timestamp": "2025-12-24T13:00:00Z",
      "fromState": "VALIDATING",
      "toState": "USABLE",
      "reason": "All validation checks passed",
      "durationInPreviousStateSec": 45
    },
    {
      "timestamp": "2025-12-24T12:59:15Z",
      "fromState": "LOADING",
      "toState": "VALIDATING",
      "reason": "All scopes loaded successfully",
      "durationInPreviousStateSec": 12
    }
  ]
}
```

---

## 8. Integration with Existing Specifications

This architecture integrates with:

### 8.1 Memory Model (Canonical)
- **Source:** `maturion-foreman-governance/governance/policies/memory-model.md`
- **Alignment:** Lifecycle states enforce memory model guarantees (tenant isolation, privacy)

### 8.2 Memory Behavior Rules
- **Source:** `foreman/behaviours/memory-rules.md`
- **Alignment:** USABLE state enables "Memory Before Action" requirement

### 8.3 Runtime Memory Ingestion
- **Source:** `foreman/runtime-memory-ingestion.md`
- **Alignment:** Ingested data flows through validation pipeline (LOADING → VALIDATING → USABLE)

### 8.4 Privacy Guardrails (Canonical)
- **Source:** `maturion-foreman-governance/governance/policies/privacy-guardrails.md`
- **Alignment:** Privacy Checker enforces guardrails during VALIDATING state

---

## 9. Non-Functional Requirements

### 9.1 Performance

- **Load Time:** <30 seconds for typical memory fabric (1000-5000 entries)
- **Validation Time:** <60 seconds for full validation
- **State Transition Latency:** <1 second (excluding load/validation)
- **Query Latency:** <100ms for filtered memory queries (USABLE state)

### 9.2 Reliability

- **Availability:** 99.9% uptime for memory fabric (USABLE state)
- **Recovery Time:** <5 minutes for automatic recovery from DEGRADED
- **Data Integrity:** 100% (zero tolerance for corruption)

### 9.3 Security

- **Privacy Compliance:** 100% (zero PII, zero secrets in memory)
- **Audit Trail:** All state transitions logged with full context
- **Access Control:** Memory reads/writes require authentication and authorization

---

## 10. Future Enhancements

### 10.1 Advanced Validation
- Machine learning-based anomaly detection in memory content
- Cross-entry consistency validation (reference integrity)

### 10.2 Performance Optimization
- Lazy loading (load scopes on-demand)
- Incremental validation (validate only new/changed entries)
- Distributed caching (multi-node deployments)

### 10.3 Self-Healing
- Automatic recovery from transient failures
- Predictive maintenance (detect degradation before failure)

---

## 11. Summary

This architecture defines a **robust, observable, and governance-aligned** memory lifecycle state machine for FM runtime operation.

**Key Principles:**
1. **Safety First** - Hard stop on critical failures, degrade gracefully when safe
2. **Observability** - Every transition emitted as event, full audit trail
3. **Privacy Enforcement** - Privacy checks integrated into validation pipeline
4. **Recovery Orientation** - Automatic recovery where safe, manual where required
5. **Governance Alignment** - Enforces memory behavior rules and privacy guardrails

**States:** UNINITIALIZED → LOADING → VALIDATING → USABLE (or DEGRADED or FAILED)

**Failure Modes:** Hard stop (critical) vs. Degrade (non-critical)

**Observability:** Events, health checks, state history, telemetry integration

This architecture enables **trustworthy, auditable, and resilient** memory-dependent operations across the FM platform.

---

**Next Steps:**
1. Review and approve architecture
2. Implement Memory Lifecycle Manager component
3. Implement state machine logic and transitions
4. Add lifecycle observability to dashboards
5. Integrate with existing Foreman and Runtime Agent workflows

---

**Version History:**
- v1.0.0 (2025-12-24): Initial architecture specification

**Related Documents:**
- `foreman/behaviours/memory-rules.md` - Memory behavior requirements
- `foreman/runtime-memory-ingestion.md` - Runtime memory ingestion specification
- `docs/architecture/runtime/cognitive-hygiene/CHP_MEMORY_INTEGRATION_ARCHITECTURE.md` - CHP integration
- `docs/architecture/runtime/observability/MEMORY_OBSERVABILITY_ARCHITECTURE.md` - Observability details
