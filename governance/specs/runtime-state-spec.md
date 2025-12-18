# Runtime State Specification

## Purpose

Define what "runtime state" means for Maturion as a **platform agent** and how Foreman expects to consume that state for:

- Health monitoring
- Risk assessment
- Upgrade decisions
- Incident detection

This spec is meta-level only. It does **not** define how raw application data is stored.

---

## 1. Runtime State Layers

1. **Platform Health**
   - Availability per module (UP / DEGRADED / DOWN)
   - Latency bands (P50, P95, P99)
   - Error rate classes (client, server, integration)

2. **AI Behaviour State**
   - Model families in use (names only)
   - Routing rules currently active
   - Observed drift indicators (see `ai-drift-monitor-spec.md`)

3. **Compliance & Security State**
   - Watchdog alerts by severity (CRITICAL / HIGH / MEDIUM / LOW)
   - Compliance violations by standard
   - Active mitigations

4. **User Feedback & Usage**
   - Volume of AI interactions by module
   - Top categories of feedback (praise, confusion, missing feature, etc.)
   - Aggregated satisfaction scores (where available)

---

## 2. Expected Signals to Foreman

When Foreman re-enters build mode or runs governance checks, it expects:

- A **summarised runtime snapshot** in the format defined in
  `foreman/upgrade/runtime-export-spec.md`.
- No tenant identifiers, no content of user messages.
- Only **aggregated counts, trends, and category labels.**

---

## 3. Integration Points

- **Upgrade Cycle** → `foreman/upgrade/upgrade-cycle.md`
- **Runtime Knowledge** → `foreman/ai-memory/knowledge-base-schema.json`
- **Risk Model** → `foreman/runtime/runtime-risk-model-spec.md`
- **Compliance Engine** → `foreman/compliance/compliance-engine-initialization.md`

---

## 4. QA of Runtime State

Before a runtime snapshot is used by Foreman:

- [ ] Snapshot validated against export schema
- [ ] No tenant PII present
- [ ] All mandatory fields populated
- [ ] Trends computed over a defined time window
- [ ] Linked to the version identifier of the platform

Details of validation rules are in:

- `foreman/qa-governance.md`
- `foreman/qa-of-qa.md`
