# Runtime Transition Plan

## Purpose

Describe how control and knowledge move between:

- Build-time Foreman
- Run-time Maturion
- Back to Foreman for the next version

Without losing context and without exposing tenant data.

---

## 1. Phases

1. **Build Phase**
   - Foreman owns architecture, QA, and governance.
   - Builders produce a new platform version.

2. **Handover to Runtime**
   - Foreman signs off on build.
   - Maturion is initialised with governance knowledge + allowed runtime memory structures.

3. **Runtime Phase**
   - Maturion operates as platform agent.
   - Records behaviour events, incidents, lessons (meta only).

4. **Return to Foreman**
   - Runtime exports allowed meta-knowledge.
   - Foreman reinitialises with this data and prepares the next upgrade.

---

## 2. Artefacts Moved Back to Foreman

- Aggregated runtime snapshots
- Behaviour event summaries
- Incident and risk records
- Aggregated user feedback categories
- Performance and drift trends

Schema references:

- `upgrade/runtime-export-spec.md`
- `upgrade/foreman-import-spec.md`
- `ai-memory/*`

---

## 3. Guardrails

- No tenant-specific data crosses the boundary.
- Export must pass compliance and QA checks.
- Each transition is logged in the change log.

See `transition/continuity-protocol.md` for the full protocol.
