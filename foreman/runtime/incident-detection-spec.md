# Incident Detection Specification

## Purpose

Describe how behaviour events are escalated into **incidents** and how severity is determined.

---

## 1. Incident Triggers

Incidents can start from:

- Behaviour log patterns
- Watchdog rule violations
- Compliance engine alerts
- Manual admin reports

---

## 2. Incident Structure

- `incident_id`
- `detected_at`
- `first_seen_event_ids`
- `severity` – `CRITICAL | HIGH | MEDIUM | LOW`
- `status` – `OPEN | INVESTIGATING | MITIGATED | CLOSED`
- `module_ids` – affected modules
- `environments` – envs involved
- `root_cause_hypothesis`
- `temporary_mitigations`
- `permanent_fixes_ref` – references into change records

The canonical schema is defined in `foreman/ai-memory/historical-issues-schema.json`.

---

## 3. Severity Guidelines

- **CRITICAL** – security breach, data integrity loss, or platform-wide outage.
- **HIGH** – major functional degradation or near-miss security issues.
- **MEDIUM** – limited module impact; does not threaten global platform.
- **LOW** – minor issues with clear workaround.

---

## 4. Integration

- Incidents feed:
  - Risk model updates
  - Upgrade insights
  - Architectural lessons
  - Change requests (new tasks for Foreman/builders)
