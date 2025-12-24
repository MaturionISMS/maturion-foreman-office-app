# FM Runtime Memory Observability Architecture

**Document Type:** Architecture Specification  
**Version:** 1.0.0  
**Status:** Draft  
**Owner:** Maturion Foreman  
**Created:** 2025-12-24

---

## 1. Purpose

This document defines the **runtime observability architecture** for the Memory Fabric in the FM (Foreman Maturion) application. It specifies how memory state, access patterns, and audit trails are exposed for visibility, monitoring, and governance compliance.

**Observability Goals:**
- **Visibility** - Foreman, Watchdog, and Johan can see memory health and state
- **Auditability** - All memory access is logged and traceable
- **Debugging** - Diagnose memory-related issues quickly
- **Compliance** - Demonstrate governance adherence for audits
- **Performance Monitoring** - Track memory fabric performance and health

**Critical Constraint:** Observability must **not** enable introspection that violates agent autonomy or privacy boundaries.

This is an **architecture and specification document only** - no implementation is included.

---

## 2. Scope

This architecture applies to:

- **Memory Fabric Observability Layer** - Exposes memory state and audit trails
- **Foreman Dashboard** - Build-time memory visibility
- **Watchdog Dashboard** - Runtime memory monitoring
- **Johan Dashboard** - Complete system oversight
- **Audit Query Surfaces** - Compliance and forensic analysis

This architecture is **separate from but aligned with**:
- Memory lifecycle state machine (see `MEMORY_LIFECYCLE_STATE_MACHINE.md`)
- CHP memory integration (see `CHP_MEMORY_INTEGRATION_ARCHITECTURE.md`)
- Memory behavior rules (see `foreman/behaviours/memory-rules.md`)

---

## 3. Observability Principles

### 3.1 What is Visible

**Visible (Exposed for Observability):**
- ✅ Memory fabric health state (UNINITIALIZED, LOADING, VALIDATING, USABLE, DEGRADED, FAILED)
- ✅ State transition history (when, from, to, reason)
- ✅ Memory access patterns (who, what scopes, when, why)
- ✅ Validation outcomes (pass/fail, error types, counts)
- ✅ Performance metrics (load time, query latency, cache hit rate)
- ✅ Audit trails (immutable log of all memory operations)
- ✅ Privacy compliance status (PII scan results, violations detected)
- ✅ Aggregated statistics (entries per scope, tags, importance distribution)

**Not Visible (Privacy and Security Protected):**
- ❌ Raw memory entry content (entries contain governance rules, but full text not exposed via observability layer for tampering protection)
- ❌ Tenant-specific operational data (if stored in `runtime` or `platform` scopes)
- ❌ Agent reasoning internals (observability does not peer into agent decision-making, only memory access)
- ❌ Secrets, credentials, or PII (never stored in memory, but observability must enforce this boundary)

---

### 3.2 Who Can See What

| Stakeholder | Visibility Scope | Use Case |
|-------------|------------------|----------|
| **Johan (Owner)** | Full visibility | System oversight, governance compliance, forensic analysis |
| **Foreman (Build-Time)** | Memory health, agent access patterns, validation outcomes | Ensure memory available before builds, detect agent misbehavior |
| **Watchdog (Runtime)** | Memory health, state transitions, performance metrics | Monitor for degradation, alert on failures, track recovery |
| **Builder Agents** | Own access history only (read-only) | Self-awareness ("Did I load correct context?") |
| **CHP** | Own access history + proposal audit trail | Self-monitoring ("Are my proposals informed?") |
| **Compliance Auditors** | Audit trails (read-only, time-bounded) | Demonstrate governance compliance, investigate incidents |

---

## 4. Observable Surfaces

### 4.1 Memory Health Status API

**Purpose:** Real-time snapshot of memory fabric health.

**Endpoint:** `GET /api/internal/memory/health`

**Response Structure:**

```json
{
  "timestamp": "2025-12-24T15:00:00Z",
  "state": "USABLE",
  "stateEnteredAt": "2025-12-24T13:00:00Z",
  "stateDurationSec": 7200,
  "lastTransition": {
    "from": "VALIDATING",
    "to": "USABLE",
    "at": "2025-12-24T13:00:00Z",
    "reason": "All validation checks passed",
    "durationInPreviousStateSec": 45
  },
  "scopes": {
    "global": {
      "status": "available",
      "entryCount": 123,
      "lastUpdated": "2025-12-24T12:00:00Z"
    },
    "foreman": {
      "status": "available",
      "entryCount": 456,
      "lastUpdated": "2025-12-24T14:30:00Z"
    },
    "platform": {
      "status": "available",
      "entryCount": 789,
      "lastUpdated": "2025-12-24T14:45:00Z"
    },
    "runtime": {
      "status": "available",
      "entryCount": 234,
      "lastUpdated": "2025-12-24T14:50:00Z"
    },
    "experience": {
      "status": "available",
      "entryCount": 67,
      "lastUpdated": "2025-12-20T10:00:00Z"
    }
  },
  "metrics": {
    "loadTimeSec": 12,
    "validationTimeSec": 45,
    "totalEntries": 1669,
    "validationErrors": 0,
    "validationWarnings": 2,
    "privacyViolations": 0,
    "cacheHitRate": 0.92,
    "avgQueryLatencyMs": 85
  },
  "degradations": [],
  "alerts": [],
  "recommendations": []
}
```

**Access Control:**
- **Johan:** Full access
- **Foreman, Watchdog:** Read-only access
- **Builder Agents:** No direct access (receive health status via agent initialization)

**Refresh Rate:** Real-time (updated on state transitions, cached for 5 seconds between transitions)

---

### 4.2 State Transition History API

**Purpose:** Track memory lifecycle state changes over time.

**Endpoint:** `GET /api/internal/memory/lifecycle/history?since={ISO_TIMESTAMP}&limit={N}`

**Response Structure:**

```json
{
  "timestamp": "2025-12-24T15:00:00Z",
  "requestedSince": "2025-12-20T00:00:00Z",
  "transitionCount": 8,
  "transitions": [
    {
      "timestamp": "2025-12-24T13:00:00Z",
      "fromState": "VALIDATING",
      "toState": "USABLE",
      "reason": "All validation checks passed",
      "durationInPreviousStateSec": 45,
      "triggeredBy": "memory_lifecycle_manager",
      "affectedScopes": ["global", "foreman", "platform", "runtime", "experience"]
    },
    {
      "timestamp": "2025-12-24T12:59:15Z",
      "fromState": "LOADING",
      "toState": "VALIDATING",
      "reason": "All scopes loaded successfully",
      "durationInPreviousStateSec": 12,
      "triggeredBy": "memory_lifecycle_manager",
      "affectedScopes": ["global", "foreman", "platform", "runtime", "experience"]
    },
    {
      "timestamp": "2025-12-24T12:59:03Z",
      "fromState": "UNINITIALIZED",
      "toState": "LOADING",
      "reason": "Memory fabric detected, initiating load",
      "durationInPreviousStateSec": 3,
      "triggeredBy": "application_startup",
      "affectedScopes": []
    }
  ],
  "statistics": {
    "avgTransitionDurationSec": 20,
    "mostFrequentTransition": "USABLE -> VALIDATING (periodic revalidation)",
    "longestStateDurationSec": 86400,
    "longestState": "USABLE"
  }
}
```

**Access Control:**
- **Johan:** Full history
- **Foreman, Watchdog:** Last 30 days
- **Builder Agents:** No access

**Retention:** 90 days (rolling window)

---

### 4.3 Memory Access Audit API

**Purpose:** Track who accessed memory, when, and why.

**Endpoint:** `GET /api/internal/memory/audit/access?actor={ACTOR}&since={ISO_TIMESTAMP}&limit={N}`

**Response Structure:**

```json
{
  "timestamp": "2025-12-24T15:00:00Z",
  "requestedActor": "CHP",
  "requestedSince": "2025-12-24T00:00:00Z",
  "accessCount": 45,
  "accesses": [
    {
      "timestamp": "2025-12-24T14:30:00Z",
      "actor": "CHP",
      "actorType": "cognitive_hygiene_protocol",
      "action": "read_memory",
      "scopesAccessed": ["global", "foreman"],
      "tagsQueried": ["architecture", "governance"],
      "importanceMin": "high",
      "entriesReturned": 15,
      "queryLatencyMs": 120,
      "reason": "Analyzing agent deviation from module boundary rules",
      "sessionId": "chp-session-789",
      "sourceIP": "10.0.1.5",
      "authorized": true
    },
    {
      "timestamp": "2025-12-24T14:00:00Z",
      "actor": "ui-builder",
      "actorType": "builder_agent",
      "action": "read_memory",
      "scopesAccessed": ["global"],
      "tagsQueried": ["ui", "patterns"],
      "importanceMin": "medium",
      "entriesReturned": 8,
      "queryLatencyMs": 95,
      "reason": "Loading UI component patterns before task execution",
      "sessionId": "ui-builder-session-456",
      "sourceIP": "10.0.2.10",
      "authorized": true
    }
  ],
  "statistics": {
    "totalAccesses": 45,
    "byActor": {
      "CHP": 12,
      "Foreman": 18,
      "ui-builder": 8,
      "api-builder": 7
    },
    "byScope": {
      "global": 40,
      "foreman": 25,
      "experience": 5
    },
    "unauthorizedAttempts": 0,
    "avgQueryLatencyMs": 105
  }
}
```

**Access Control:**
- **Johan:** Full audit trail (all actors, all time)
- **Foreman:** All builder agent accesses + CHP accesses
- **Watchdog:** All accesses (monitoring for anomalies)
- **Builder Agents:** Own accesses only (self-awareness)
- **CHP:** Own accesses only

**Retention:** 7 years (compliance requirement)

**Immutability:** Audit logs are append-only, tamper-proof (cryptographic hash chain)

---

### 4.4 Memory Write Audit API

**Purpose:** Track memory entry creation and modification.

**Endpoint:** `GET /api/internal/memory/audit/write?actor={ACTOR}&scope={SCOPE}&since={ISO_TIMESTAMP}&limit={N}`

**Response Structure:**

```json
{
  "timestamp": "2025-12-24T15:00:00Z",
  "requestedActor": "Foreman",
  "requestedScope": "foreman",
  "requestedSince": "2025-12-24T00:00:00Z",
  "writeCount": 12,
  "writes": [
    {
      "timestamp": "2025-12-24T14:00:00Z",
      "actor": "Foreman",
      "action": "write_memory",
      "scope": "foreman",
      "entryId": "foreman-2025-12-24-001234",
      "title": "Module Boundary Decision: Asset Module API Layer",
      "importance": "high",
      "tags": ["architecture", "decision", "module", "asset"],
      "validationStatus": "passed",
      "privacyCheckStatus": "passed",
      "writeLatencyMs": 45,
      "reason": "Approved UI Builder proposal to use API layer for Asset data access",
      "sessionId": "foreman-session-123",
      "sourceIP": "10.0.1.1",
      "authorized": true
    }
  ],
  "statistics": {
    "totalWrites": 12,
    "byScope": {
      "foreman": 8,
      "experience": 4
    },
    "byImportance": {
      "critical": 1,
      "high": 5,
      "medium": 6,
      "low": 0
    },
    "validationFailures": 0,
    "privacyViolations": 0,
    "avgWriteLatencyMs": 50
  }
}
```

**Access Control:**
- **Johan:** Full write audit (all actors, all scopes)
- **Foreman:** Writes to `foreman`, `experience` scopes (own writes + approved writes)
- **Watchdog:** All writes (monitoring for anomalies)
- **Builder Agents:** Own writes only

**Retention:** 7 years (compliance requirement)

---

### 4.5 Privacy Compliance Report API

**Purpose:** Demonstrate privacy guardrail enforcement.

**Endpoint:** `GET /api/internal/memory/compliance/privacy?since={ISO_TIMESTAMP}`

**Response Structure:**

```json
{
  "timestamp": "2025-12-24T15:00:00Z",
  "reportPeriod": "2025-12-20T00:00:00Z to 2025-12-24T15:00:00Z",
  "scansConducted": 1234,
  "scansScheduled": 1234,
  "complianceRate": 1.0,
  "violations": {
    "totalViolations": 0,
    "byType": {
      "pii_detected": 0,
      "secrets_detected": 0,
      "tenant_data_detected": 0,
      "cross_tenant_reference": 0
    }
  },
  "scans": [
    {
      "timestamp": "2025-12-24T14:30:00Z",
      "scanType": "write_validation",
      "scope": "foreman",
      "entryId": "foreman-2025-12-24-001234",
      "piiDetected": false,
      "secretsDetected": false,
      "tenantDataDetected": false,
      "scanDurationMs": 25,
      "outcome": "passed"
    }
  ],
  "alerts": [],
  "recommendations": []
}
```

**Access Control:**
- **Johan:** Full compliance report
- **Foreman:** Read-only access (ensure compliance before builds)
- **Compliance Auditors:** Read-only access (time-bounded, authorized by Johan)

**Retention:** 7 years (compliance requirement)

---

### 4.6 Performance Metrics API

**Purpose:** Monitor memory fabric performance and detect degradation.

**Endpoint:** `GET /api/internal/memory/metrics/performance?since={ISO_TIMESTAMP}&interval={INTERVAL}`

**Response Structure:**

```json
{
  "timestamp": "2025-12-24T15:00:00Z",
  "reportPeriod": "2025-12-24T00:00:00Z to 2025-12-24T15:00:00Z",
  "interval": "1h",
  "dataPoints": [
    {
      "timestamp": "2025-12-24T14:00:00Z",
      "metrics": {
        "loadTimeSec": 12,
        "validationTimeSec": 45,
        "avgQueryLatencyMs": 85,
        "p50QueryLatencyMs": 75,
        "p95QueryLatencyMs": 150,
        "p99QueryLatencyMs": 200,
        "cacheHitRate": 0.92,
        "cacheSize": 1024,
        "memoryUsageMB": 256,
        "queriesPerSec": 12,
        "writesPerSec": 0.5
      },
      "state": "USABLE",
      "alerts": []
    }
  ],
  "thresholds": {
    "loadTimeSec": 30,
    "validationTimeSec": 60,
    "avgQueryLatencyMs": 200,
    "cacheHitRate": 0.85
  },
  "alerts": [],
  "recommendations": []
}
```

**Access Control:**
- **Johan:** Full metrics history
- **Foreman, Watchdog:** Last 30 days
- **Builder Agents:** No access

**Retention:** 90 days (rolling window)

---

## 5. Dashboard Views

### 5.1 Foreman Dashboard - Memory Status Panel

**Purpose:** Enable Foreman to ensure memory is ready before accepting builds.

**Displayed Information:**
- Current memory state (USABLE, DEGRADED, FAILED)
- State duration (how long in current state)
- Last state transition (when, from, to, reason)
- Scope availability (which scopes are available)
- Recent agent memory accesses (last 10)
- Validation status (last validation outcome)
- Privacy compliance status (any violations detected)

**Alerts Shown:**
- ⚠️ "Memory DEGRADED: `experience` scope unavailable"
- 🚨 "Memory FAILED: Critical scope missing, builds blocked"
- ✅ "Memory USABLE: All scopes available, validation passed"

**Actions Available:**
- 🔄 "Re-validate memory fabric" (trigger manual revalidation)
- 🔍 "View full health report" (link to detailed health API)
- 📊 "View access audit" (link to audit API filtered to current build session)

**Refresh Rate:** Real-time (WebSocket or polling every 5 seconds)

---

### 5.2 Watchdog Dashboard - Memory Health Monitor

**Purpose:** Enable Watchdog to monitor memory fabric health during runtime.

**Displayed Information:**
- Real-time memory state (with state transition timeline)
- Performance metrics (load time, query latency, cache hit rate)
- Access patterns (queries per minute, writes per minute)
- Privacy compliance status (scan results, violations)
- State transition history (last 24 hours)
- Anomaly alerts (unexpected state transitions, performance degradation)

**Charts/Graphs:**
- **State Timeline:** Visual timeline of state transitions over last 24h
- **Query Latency Graph:** Line chart showing query latency trends
- **Access Heatmap:** Which scopes are accessed most frequently
- **Error Rate Graph:** Validation errors, privacy violations over time

**Alerts Shown:**
- 🚨 "Memory transitioned to FAILED: Privacy violation detected"
- ⚠️ "Memory query latency exceeds threshold: avg 250ms (threshold 200ms)"
- ℹ️ "Memory state stable: USABLE for 72 hours"

**Actions Available:**
- 🔄 "Trigger recovery" (attempt auto-recovery if DEGRADED or FAILED)
- 🔍 "View audit trail" (link to full audit API)
- 📊 "Export performance report" (download metrics as CSV/JSON)

**Refresh Rate:** Real-time (WebSocket)

---

### 5.3 Johan Dashboard - Complete Memory Oversight

**Purpose:** Provide Johan with full visibility into memory fabric state and governance.

**Displayed Information:**
- All information from Foreman and Watchdog dashboards
- Full audit trail (all actors, all scopes, all time)
- Write history (who wrote what, when, why)
- Privacy compliance report (detailed scan results)
- CHP proposal audit (proposals generated, approved, rejected)
- Agent access patterns (which agents access memory most frequently)
- Governance enforcement status (compliance with memory behavior rules)

**Advanced Queries:**
- "Show all memory accesses by CHP in last 7 days"
- "Show all writes to `foreman` scope by Foreman"
- "Show all privacy violations detected (historical)"
- "Show memory state transitions correlated with build failures"

**Alerts Shown:**
- All alerts from Foreman and Watchdog dashboards
- Additional forensic alerts: "Unauthorized access attempt detected"
- Governance alerts: "Agent violated memory behavior rules"

**Actions Available:**
- All actions from Foreman and Watchdog dashboards
- 🔧 "Manually repair memory fabric" (advanced admin action)
- 🔍 "Forensic audit mode" (enable detailed logging for investigation)
- 📋 "Generate compliance report" (export for auditors)

**Refresh Rate:** Real-time (WebSocket)

---

## 6. Query Surfaces (Conceptual)

### 6.1 SQL-Like Query Interface (Conceptual)

**Purpose:** Enable flexible queries for forensic analysis and compliance audits.

**Example Queries:**

```sql
-- Find all memory accesses by CHP in last 7 days
SELECT * FROM memory_audit_access
WHERE actor = 'CHP'
AND timestamp >= NOW() - INTERVAL '7 days'
ORDER BY timestamp DESC;

-- Find all writes to foreman scope with high importance
SELECT * FROM memory_audit_write
WHERE scope = 'foreman'
AND importance IN ('high', 'critical')
ORDER BY timestamp DESC;

-- Find all state transitions to FAILED state
SELECT * FROM memory_state_transitions
WHERE toState = 'FAILED'
ORDER BY timestamp DESC;

-- Find all privacy violations (historical)
SELECT * FROM memory_privacy_scans
WHERE piiDetected = true OR secretsDetected = true
ORDER BY timestamp DESC;

-- Correlate memory state with build outcomes
SELECT st.timestamp, st.toState, b.buildId, b.outcome
FROM memory_state_transitions st
JOIN builds b ON b.timestamp BETWEEN st.timestamp AND st.timestamp + INTERVAL '1 hour'
WHERE st.toState IN ('DEGRADED', 'FAILED')
ORDER BY st.timestamp DESC;
```

**Access Control:**
- **Johan:** Full query access
- **Compliance Auditors:** Read-only, time-bounded queries (authorized by Johan)
- **Foreman, Watchdog:** Predefined queries only (no arbitrary SQL)

---

### 6.2 GraphQL Query Interface (Conceptual)

**Purpose:** Enable flexible, type-safe queries for dashboards and integrations.

**Example Query:**

```graphql
query MemoryHealthOverview {
  memoryHealth {
    state
    stateEnteredAt
    stateDurationSec
    lastTransition {
      from
      to
      at
      reason
    }
    scopes {
      name
      status
      entryCount
      lastUpdated
    }
    metrics {
      loadTimeSec
      validationTimeSec
      avgQueryLatencyMs
      cacheHitRate
    }
    alerts {
      severity
      message
      timestamp
    }
  }
}

query MemoryAccessAudit($actor: String!, $since: DateTime!) {
  memoryAccessAudit(actor: $actor, since: $since) {
    accesses {
      timestamp
      actor
      action
      scopesAccessed
      tagsQueried
      entriesReturned
      reason
      authorized
    }
    statistics {
      totalAccesses
      byScope
      unauthorizedAttempts
    }
  }
}
```

**Access Control:** Same as SQL-like interface

---

## 7. Data Retention Constraints

### 7.1 Operational Data

| Data Type | Retention Period | Rationale |
|-----------|------------------|-----------|
| Memory health status | 90 days | Performance trending, incident analysis |
| State transition history | 90 days | Debugging, pattern analysis |
| Performance metrics | 90 days | Trend analysis, capacity planning |

**After Retention Period:** Data aggregated into monthly summaries, then archived.

---

### 7.2 Audit Data

| Data Type | Retention Period | Rationale |
|-----------|------------------|-----------|
| Access audit logs | 7 years | Compliance requirement (ISO 27001, POPIA) |
| Write audit logs | 7 years | Compliance requirement (ISO 27001, POPIA) |
| Privacy compliance scans | 7 years | Compliance requirement (GDPR, POPIA) |

**After Retention Period:** Data moved to cold storage (compressed, encrypted).

---

### 7.3 Aggregated Statistics

| Data Type | Retention Period | Rationale |
|-----------|------------------|-----------|
| Monthly performance summaries | Indefinite | Long-term trend analysis |
| Annual compliance reports | Indefinite | Historical compliance records |

---

## 8. Escalation Linkage (Alerts Reference Evidence)

### 8.1 Escalation Event Structure

Every escalation from memory fabric to Foreman, Watchdog, or Johan includes:

```json
{
  "escalationId": "ESC-2025-001234",
  "timestamp": "2025-12-24T16:00:00Z",
  "severity": "high",
  "source": "memory_lifecycle_manager",
  "eventType": "memory_state_failed",
  "title": "Memory fabric entered FAILED state: Critical scope missing",
  "description": "Memory lifecycle manager detected missing `global` scope during validation. All operations blocked.",
  "evidence": {
    "stateTransition": {
      "from": "VALIDATING",
      "to": "FAILED",
      "at": "2025-12-24T16:00:00Z",
      "reason": "Critical scope missing: global"
    },
    "scopeStatus": {
      "global": "missing",
      "foreman": "available",
      "platform": "available",
      "runtime": "available"
    },
    "auditTrail": {
      "lastAccessToGlobal": "2025-12-24T15:00:00Z",
      "lastWriteToGlobal": "2025-12-24T14:00:00Z"
    },
    "diagnosticLinks": [
      "/api/internal/memory/health",
      "/api/internal/memory/lifecycle/history?since=2025-12-24T15:00:00Z",
      "/api/internal/memory/audit/access?scope=global&since=2025-12-24T14:00:00Z"
    ]
  },
  "recommendedActions": [
    "Check for accidental deletion of `memory/global/` directory",
    "Restore from Git history if deleted",
    "Re-initialize memory fabric if restoration fails"
  ],
  "escalationTarget": "Johan",
  "escalationChannel": "email",
  "urgency": "immediate"
}
```

---

### 8.2 Evidence Types

| Escalation Type | Evidence Included |
|-----------------|-------------------|
| Memory state FAILED | State transition history, scope status, last access/write audit |
| Privacy violation detected | Privacy scan results, violating entry details, actor audit trail |
| Unauthorized access attempt | Access audit log, actor details, attempted scopes, authorization failure reason |
| Performance degradation | Performance metrics over time, threshold breach details, affected operations |
| Validation failure | Validation errors, affected entries, schema version, suggested fixes |

---

### 8.3 Diagnostic Link Structure

All escalations include direct links to:
1. **Health API** - Current memory state
2. **State History API** - Recent state transitions
3. **Audit API** - Relevant access/write logs
4. **Performance API** - Recent performance metrics

**Example Diagnostic Link:**
```
https://foreman-dashboard.example.com/memory/diagnostics?escalationId=ESC-2025-001234
```

This link pre-filters all observability surfaces to show only data relevant to the escalation.

---

## 9. Integration with Existing Specifications

This architecture integrates with:

### 9.1 Memory Lifecycle State Machine
- **Source:** `MEMORY_LIFECYCLE_STATE_MACHINE.md`
- **Alignment:** Observability exposes all lifecycle states and transitions defined in state machine

### 9.2 CHP Memory Integration
- **Source:** `CHP_MEMORY_INTEGRATION_ARCHITECTURE.md`
- **Alignment:** CHP memory reads are audited and visible via access audit API, CHP proposals visible in Johan dashboard

### 9.3 Memory Behavior Rules
- **Source:** `foreman/behaviours/memory-rules.md`
- **Alignment:** Observability enables enforcement monitoring (e.g., detect agents that skip memory load)

### 9.4 Privacy Guardrails (Canonical)
- **Source:** `maturion-foreman-governance/governance/policies/privacy-guardrails.md`
- **Alignment:** Privacy compliance report API demonstrates guardrail enforcement

---

## 10. Non-Functional Requirements

### 10.1 Performance

- **Health API Latency:** <100ms
- **Audit Query Latency:** <500ms for last 30 days, <2s for full history
- **Dashboard Refresh Rate:** Real-time (WebSocket) or 5-second polling
- **Query Throughput:** Support 100+ queries/sec (dashboards, monitoring)

### 10.2 Reliability

- **Observability Uptime:** 99.9% (independent of memory fabric state)
- **Audit Log Durability:** 100% (no audit data loss)
- **Dashboard Availability:** 99.5% (degraded mode if memory FAILED, but observability still operational)

### 10.3 Security

- **Access Control Enforcement:** 100% (stakeholders see only authorized data)
- **Audit Immutability:** 100% (append-only, tamper-proof)
- **PII Protection:** Zero PII in observability data (even if accidentally stored in memory, observability layer filters it)

---

## 11. Privacy and Security Constraints

### 11.1 What Observability Must NOT Expose

**Protected Content:**
- ❌ Full text of memory entries (entries may contain governance rules, but observability returns only metadata for security)
- ❌ Tenant-specific identifiers (organisation_id, user_id) in aggregated statistics
- ❌ Raw tenant operational data (even if accidentally stored in `runtime` or `platform` scopes)
- ❌ Agent reasoning internals (observability does not introspect agent decision-making)
- ❌ Secrets, credentials, or API keys (never stored, but observability must enforce boundary)

---

### 11.2 Defense-in-Depth Filtering

**Observability Layer Filters:**
1. **PII Filter** - Redact any detected PII in observability responses (email, phone, names)
2. **Tenant Isolation Filter** - Anonymize tenant identifiers in cross-tenant aggregations
3. **Secret Scanner** - Redact any detected secrets (API keys, passwords, tokens)
4. **Metadata-Only Mode** - Return entry metadata (id, timestamp, scope, tags) without full content

**Example:**
```json
// Memory entry (stored):
{
  "id": "foreman-2025-12-24-001234",
  "timestamp": "2025-12-24T14:00:00Z",
  "scope": "foreman",
  "title": "Module Boundary Decision",
  "summary": "Approved API layer for Asset module...",
  "importance": "high",
  "tags": ["architecture", "decision"]
}

// Observability response (metadata only):
{
  "entryId": "foreman-2025-12-24-001234",
  "timestamp": "2025-12-24T14:00:00Z",
  "scope": "foreman",
  "importance": "high",
  "tags": ["architecture", "decision"],
  "contentAvailable": false,
  "contentAccessRequiresAuthorization": true
}
```

---

## 12. Future Enhancements

### 12.1 Predictive Monitoring
- Machine learning models predict memory state transitions (e.g., "Memory likely to enter DEGRADED in next 2 hours based on access patterns")
- Proactive alerts before failures occur

### 12.2 Anomaly Detection
- Detect unusual access patterns (e.g., "CHP accessed memory 10x more than usual today")
- Detect unusual state transitions (e.g., "Memory transitioned to FAILED 5 times in 1 hour, investigate root cause")

### 12.3 Natural Language Queries
- Enable Johan to query observability in natural language: "Show me all memory failures in December 2025"
- AI-powered query translation to SQL/GraphQL

### 12.4 Cross-System Correlation
- Correlate memory state with build outcomes, deployment events, compliance incidents
- Root cause analysis: "Why did Build Wave 3 fail? Memory was DEGRADED at the time."

---

## 13. Summary

This architecture defines a **comprehensive, secure, and privacy-respecting** observability layer for the Memory Fabric.

**Key Principles:**
1. **Full Visibility** - All memory state, transitions, accesses, and writes are observable
2. **Strong Access Control** - Stakeholders see only what they're authorized to see
3. **Audit Everything** - All operations logged immutably for compliance
4. **Privacy Protection** - Observability filters PII, secrets, tenant data (defense-in-depth)
5. **Escalation Evidence** - All alerts link to diagnostic data for rapid resolution
6. **No Introspection** - Observability does not peer into agent reasoning, only memory access

**Observable Surfaces:**
- Health Status API
- State Transition History API
- Access Audit API
- Write Audit API
- Privacy Compliance Report API
- Performance Metrics API

**Dashboards:**
- Foreman Dashboard: Memory readiness for builds
- Watchdog Dashboard: Runtime health monitoring
- Johan Dashboard: Complete oversight and governance

**Data Retention:**
- Operational data: 90 days (then aggregated)
- Audit data: 7 years (compliance requirement)
- Aggregated statistics: Indefinite

This architecture enables **trustworthy, auditable, and governance-compliant** memory operations across the FM platform.

---

**Next Steps:**
1. Review and approve architecture
2. Implement observability APIs (health, audit, metrics)
3. Build dashboards (Foreman, Watchdog, Johan)
4. Integrate with escalation system
5. Deploy and monitor in production

---

**Version History:**
- v1.0.0 (2025-12-24): Initial architecture specification

**Related Documents:**
- `MEMORY_LIFECYCLE_STATE_MACHINE.md` - Memory lifecycle states and transitions
- `CHP_MEMORY_INTEGRATION_ARCHITECTURE.md` - CHP memory integration and proposals
- `foreman/behaviours/memory-rules.md` - Memory behavior requirements
- `foreman/runtime-memory-ingestion.md` - Runtime memory ingestion patterns
