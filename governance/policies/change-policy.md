# Change Management Policy

## Purpose

Define mandatory rules for all changes affecting:

- Architecture
- Code
- AI routing/behaviour
- Configuration
- Compliance/QA logic

---

## Principles

1. **Risk-aware** – every change has an explicit risk assessment.
2. **Test-first** – all changes must be validated in the test environment.
3. **Rollback-ready** – every change has a viable rollback plan.
4. **Traceable** – changes are recorded in `change-log-schema.json`.
5. **Segregation of Duties** – builder agents implement; Foreman governs.

---

## Scope

- Applies to all Maturion ISMS modules.
- Applies to both Foreman and runtime Maturion adjustments.
- Includes configuration changes in external systems if they influence behaviour.
