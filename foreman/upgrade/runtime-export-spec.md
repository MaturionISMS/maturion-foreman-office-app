# Runtime Export Specification

## Purpose

Define what runtime artefacts can be exported from Maturion to Foreman and in what format.

**Privacy Rule**: Exports are strictly meta-level. No tenant PII, no raw user content.

---

## 1. Exportable Artefacts

### 1.1 Runtime State Snapshot
- Platform version
- Environment map snapshot
- Active modules and their health states
- Aggregated error rates by module
- Performance metrics (P50, P95, P99) by module

### 1.2 Behaviour Event Summary
- Total events by category
- Critical events with summaries (no tenant data)
- Incident summaries per `incident-detection-spec.md`
- Risk entries per `runtime-risk-model-spec.md`

### 1.3 AI Behaviour Metrics
- Model families in use
- Drift event summaries
- Aggregated quality scores
- Safety event counts by category

### 1.4 User Feedback Aggregates
- Feedback volume by module
- Top feedback categories
- Aggregated satisfaction scores
- Feature request themes (no identifiable details)

### 1.5 Compliance & Watchdog State
- Active watchdog rules
- Compliance violations by standard
- Mitigation states
- Audit trail summaries (meta only)

---

## 2. Export Format

All exports use JSON format with the following structure:

```json
{
  "export_metadata": {
    "export_id": "uuid",
    "exported_at": "ISO 8601 timestamp",
    "platform_version": "semver",
    "export_type": "runtime_snapshot",
    "time_period": {
      "start": "ISO 8601",
      "end": "ISO 8601"
    }
  },
  "privacy_validation": {
    "no_pii_confirmed": true,
    "no_tenant_data_confirmed": true,
    "validated_by": "export_validator",
    "validated_at": "ISO 8601"
  },
  "data": {
    "runtime_state": {},
    "behaviour_events": [],
    "ai_metrics": {},
    "user_feedback_aggregates": {},
    "compliance_state": {}
  }
}
```

---

## 3. Validation Rules

Before export:

- [ ] No tenant names, IDs, or identifiable information
- [ ] No user names, emails, or credentials
- [ ] No raw text from conversations
- [ ] All counts and metrics are aggregated
- [ ] Export schema validated
- [ ] Privacy guardrails check passed

---

## 4. Storage & Access

- Exports stored in secure Foreman workspace
- Retention: last 5 exports (aligned with version retention)
- Access restricted to Foreman and authorized human admin
- Exports are versioned and linked to platform version
