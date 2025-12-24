# FM Watchdog Runtime

**Status**: W-F1 Implementation  
**Type**: Read-Only, Non-Authoritative  
**Last Updated**: 2025-12-24

---

## Purpose

Independent watchdog runtime for FM application. Strictly read-only, report-and-escalate only.

**What it does:**
- ✅ Reads alerts from alert store
- ✅ Filters alerts by criteria
- ✅ Generates status reports
- ✅ Identifies alerts requiring escalation
- ✅ Reports to human oversight

**What it does NOT do:**
- ❌ Write or modify alerts
- ❌ Interpret policy
- ❌ Perform remediation
- ❌ Make autonomous decisions
- ❌ Silent failures (all errors escalated)

---

## Architecture

```
fm/runtime/watchdog/
├── __init__.py              # Module exports
├── alert_reader.py          # Read-only alert reader
├── escalation_reporter.py   # Escalation reporter
└── README.md               # This file
```

---

## Components

### AlertReader

Read-only alert reader that:
- Reads alerts from `maturion-isms/runtime/watchdog/watchdog-alerts.json`
- Enforces tenant isolation via `organisation_id`
- Filters by severity, type, status
- Provides alert summaries
- **Never writes or modifies alerts**

### EscalationReporter

Escalation reporter that:
- Identifies alerts requiring human attention
- Generates escalation reports
- Logs escalation events
- Reports to human oversight
- **Never modifies alerts or performs remediation**

---

## Tenant Isolation

All operations respect tenant isolation:

```python
# Read alerts for specific organisation only
reader = AlertReader()
alerts = reader.read_alerts(organisation_id="org-123")

# Generate escalation report for specific organisation
reporter = EscalationReporter()
report = reporter.generate_escalation_report(alerts, organisation_id="org-123")
```

If `organisation_id` is `None`, operates in platform-wide mode (for platform-level alerts only).

---

## Usage Examples

### Read Active Alerts

```python
from fm.runtime.watchdog import AlertReader

reader = AlertReader()

# Get all active alerts for organisation
alerts = reader.get_active_alerts(organisation_id="org-123")

# Get critical alerts only
critical = reader.get_critical_alerts(organisation_id="org-123")

# Get alerts by type
compliance_alerts = reader.get_alerts_by_type(
    "compliance_drift",
    organisation_id="org-123"
)
```

### Generate Escalation Report

```python
from fm.runtime.watchdog import AlertReader, EscalationReporter

reader = AlertReader()
reporter = EscalationReporter()

# Read alerts
alerts = reader.read_alerts(organisation_id="org-123")

# Generate escalation report
report = reporter.generate_escalation_report(
    alerts,
    organisation_id="org-123"
)

# Log escalations
reporter.log_escalation(report, destination="human_oversight")
```

### Get Alert Summary

```python
from fm.runtime.watchdog import AlertReader

reader = AlertReader()

# Get summary of all alerts
summary = reader.get_alert_summary(organisation_id="org-123")

print(f"Total alerts: {summary['total_alerts']}")
print(f"Active alerts: {summary['active_alerts']}")
print(f"By severity: {summary['by_severity']}")
```

---

## Error Handling

**No silent failures.** All errors are raised and escalated:

- `FileNotFoundError`: Alert store not found
- `ValueError`: Invalid alert store format
- `RuntimeError`: Unexpected errors

Watchdog runtime never swallows errors. If something fails, it escalates.

---

## Integration

Watchdog runtime integrates with:

- **Alert Store**: Reads from `maturion-isms/runtime/watchdog/watchdog-alerts.json`
- **Foreman Runtime**: Part of FM operational runtime
- **Human Oversight**: Escalates to human via logs and reports

It does NOT integrate with:
- Policy engines (no interpretation)
- Remediation systems (no auto-fix)
- Alert writers (read-only)

---

## Governance

This implementation follows:

- `governance/specs/watchdog-standard-spec.md`
- `governance/specs/compliance-watchdog-spec.md`
- `foreman/privacy-guardrails.md` (tenant isolation)
- `foreman/memory-model.md` (read-only operations)

---

## Testing

Tests located in: `tests/test_watchdog_runtime.py`

Run tests:
```bash
pytest tests/test_watchdog_runtime.py -v
```

---

## References

- **Issue**: W-F1 - Implement Independent Watchdog Runtime
- **Governance Specs**:
  - `governance/specs/watchdog-standard-spec.md`
  - `governance/specs/compliance-watchdog-spec.md`
- **Alert Schema**: `maturion-isms/runtime/watchdog/watchdog-alerts.json`
- **Privacy**: `foreman/privacy-guardrails.md`

---

*FM Watchdog Runtime - Read-Only, Report-and-Escalate Only*
