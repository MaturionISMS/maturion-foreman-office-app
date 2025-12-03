# Copilot Instructions for Maturion Foreman

## Repository Overview

This repository defines and governs **Maturion Foreman**, the permanent AI Foreman and Platform Agent for the Maturion ISMS ecosystem.

- This repo is about **governance, architecture rules, QA, compliance, and orchestration**.
- It is **not** where application code for ISMS modules is implemented.
- All changes here affect how the Foreman thinks, governs, and coordinates builder agents.

---

## Foreman Identity

**Name:** Maturion Foreman  
**Role:** Governance, architecture enforcement, QA-of-QA, compliance oversight, and AI orchestration hub  
**Scope:**  
- Supervises builder agents (UI, API, schema, integration, QA)  
- Enforces architecture, QA, and compliance standards  
- Coordinates build sequencing  
- Monitors platform health (at runtime)  
- Manages innovation, surveys, and admin intelligence

> 🔴 **Important:**  
> Maturion Foreman is a **governance agent, not a builder**.  
> He does **not** write production module code in this repository.

For full identity details, see:  
- `foreman/identity.md`  
- `foreman/roles-and-duties.md`  

---

## Core Principles (Build Philosophy)

When Copilot assists in this repo, it MUST respect the **Maturion Build Philosophy**:

1. **One-Time Build Correctness**  
   - Design governance, architecture, QA, and compliance so that builds are correct the first time.

2. **Zero Regression**  
   - Never break existing rules, specs, or governance logic that already work.

3. **Full Architectural Alignment**  
   - All changes must align with:
     - SRMF Master Build Reference  
     - Integrated ISMS Architecture  
     - Module True North documents  

4. **Zero Loss of Context**  
   - Never discard, overwrite, or “simplify away” important governance details.  
   - Preserve rationales, decisions, and coverage.

5. **Zero Ambiguity**  
   - Governance rules must be explicit and machine-checkable.  
   - Avoid vague text that cannot be enforced.

---

## Privacy & Memory Guardrails

This repo encodes strong privacy and isolation guarantees.

Copilot must respect:

- `foreman/memory-model.md`  
- `foreman/privacy-guardrails.md`  

Rules:

- Always assume **strict tenant isolation**.  
- Never design or suggest cross-tenant data sharing.  
- All runtime operations must include an `organisation_id` or equivalent isolation key.  
- Any new governance logic must respect the memory and privacy model.

---

## Governance, QA, and Compliance

Key governance specs live under `foreman/`:

- Architecture & Standards  
  - `foreman/minimum-architecture-template.md`  
  - `foreman/architecture-validation-checklist.md`  
  - `foreman/architecture-naming-conventions.md`  
  - `foreman/architecture-folder-structure.md`  
  - `foreman/versioning-rules.md`  

- QA & QA-of-QA  
  - `foreman/qa-governance.md`  
  - `foreman/qa-minimum-coverage-requirements.md`  
  - `foreman/qa-of-qa.md`  
  - `foreman/platform/qa-dashboard-spec.md`  
  - `foreman/platform/governance-qa-dashboard-spec.md`  

- Compliance  
  - `foreman/compliance/compliance-reference-map.md`  
  - `foreman/compliance/compliance-control-library.json`  
  - `foreman/compliance/compliance-qa-spec.md`  
  - `foreman/compliance/compliance-watchdog-spec.md`  
  - `foreman/compliance/compliance-dashboard-spec.md`  

When modifying or adding anything in these areas, Copilot must:

- Keep existing structure and intent intact.  
- Extend, not replace, established rules.  
- Ensure all new rules are testable and enforceable.  

---

## Builder Agents & Their Boundaries

Foreman orchestrates 5 builder agents:

- `ui-builder` – UI components and frontend code  
- `api-builder` – API routes and backend logic  
- `schema-builder` – database schema and models  
- `integration-builder` – inter-module and external integrations  
- `qa-builder` – tests, coverage, and QA-of-QA reports  

Specifications:

- `foreman/builder/ui-builder-spec.md`  
- `foreman/builder/api-builder-spec.md`  
- `foreman/builder/schema-builder-spec.md`  
- `foreman/builder/integration-builder-spec.md`  
- `foreman/builder/qa-builder-spec.md`  
- `foreman/builder/builder-collaboration-rules.md`  
- `foreman/builder/builder-capability-map.json`  
- `foreman/builder/builder-permission-policy.json`  

Copilot must **NOT**:

- Turn Foreman into a builder.  
- Blur boundaries between builder agents.  
- Grant builders permissions beyond what `builder-permission-policy.json` defines.  

---

## When Working on Issues in This Repo

Before proposing changes, Copilot should:

1. **Understand Foreman’s Role**
   - Read:  
     - `foreman/identity.md`  
     - `foreman/roles-and-duties.md`  
     - `foreman/runtime-agent-plan.md`  

2. **Respect Command Grammar**
   - Use `foreman/command-grammar.md` to understand how Johan and agents communicate.

3. **Respect Governance & Standards**
   - Align with:  
     - `foreman/minimum-architecture-template.md`  
     - `foreman/architecture-validation-checklist.md`  
     - `foreman/qa-governance.md`  
     - `foreman/compliance-qa-spec.md`  

4. **Avoid Modifying Core Identity & Guardrail Files**  
   Do **not** change these unless explicitly instructed in the issue:
   - `foreman/identity.md`  
   - `foreman/memory-model.md`  
   - `foreman/privacy-guardrails.md`  
   - `foreman/command-grammar.md`  
   - `foreman/roles-and-duties.md`  

5. **Prefer Adding New Specs Over Overwriting Old Ones**
   - If a new behaviour is needed, introduce a new spec or section rather than rewriting foundational documents.

6. **Always Consider Multi-Module Impact**
   - Any change can affect:
     - Architecture indexing  
     - Compliance coverage  
     - QA dashboards  
     - Builder orchestration  

---

## Working with Validation & Indexing Tools

This repo contains internal tools that Foreman uses:

- `validate-repository.py`  
- `index-isms-architecture.py`  
- `activate-compliance-engine.py`  
- `init_builders.py`  

Copilot may:

- Improve robustness (logging, error handling, clarity)
- Extend validation checks safely
- Update documentation around how they’re run

Copilot must NOT:

- Remove existing checks that enforce governance/standards  
- Bypass validation logic to “make things pass”  

---

## Documentation Expectations

When Copilot changes or adds behaviour:

- Update or create relevant `*_REPORT.md` and `*_SUMMARY.md` files.
- Ensure new specs are referenced in:
  - `OPERATIONAL_STATUS_REPORT.md`  
  - README files where relevant.  

All changes should support:

- Transparency  
- Auditability  
- Governance traceability  

---

## Summary for Copilot

- Treat this repo as **the brain and rulebook** of Maturion Foreman.  
- Foreman **governs** builders, he does **not** build modules here.  
- Respect privacy, tenant isolation, and compliance at all times.  
- Maintain strict architecture, QA, and compliance standards.  
- Extend governance with clarity and structure, never weaken it.  
- Always think:  
  > “Will this change help Maturion enforce One-Time Build Correctness and Zero Regression across the entire ISMS ecosystem?”
