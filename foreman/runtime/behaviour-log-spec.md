# Behaviour Log Specification

## Purpose

Define how runtime behaviour events are captured in a **privacy-preserving**, meta-level form so they can:

- Feed risk management,
- Drive upgrades,
- Support incident analysis,
- And generate long-term lessons.

No tenant-identifying fields are allowed.

---

## 1. Event Structure

Each event must have:

- `event_id` – unique meta identifier
- `timestamp` – ISO 8601
- `environment_id` – matches `environment-map.json`
- `module_id` – e.g. `ERM`, `RISK_ASSESSMENT`, `THREAT`
- `category` – e.g. `health_check`, `ai_drift`, `compliance_alert`, `user_feedback_aggregate`
- `severity` – `INFO | NOTICE | WARNING | ERROR | CRITICAL`
- `summary` – short plain-language description
- `details_ref` – optional reference to an internal log, never raw content
- `related_risks` – references to risk IDs in `runtime-risk-model-spec.md`
- `version_tag` – platform/app version

---

## 2. Privacy Rules

- No user names, tenant names, email addresses, or free-text fields that could contain secrets.
- Event payloads are **labels and counts**, not raw text.

---

## 3. Storage & Access

- Behaviour events can be aggregated for:
  - Upgrade insights (`upgrade-insights-schema.json`)
  - Historical issues (`historical-issues-schema.json`)
  - Architectural lessons (`architectural-lessons.md`)

- Granular raw logs stay outside Foreman; only structured summaries enter the memory spine.

---

## 4. QA-of-QA

Foreman must ensure that:

- Behaviour events cannot bypass privacy guardrails.
- Every CRITICAL event is either:
  - Linked to an incident record, or
  - Explicitly classified as false positive with justification.
