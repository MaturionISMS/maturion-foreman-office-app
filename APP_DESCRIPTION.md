# Maturion Foreman Office App  
## Canonical Application Description & Operating Contract

**Version:** 1.1  
**Status:** Authoritative  
**Audience:** Human Owner, Foreman AI, Governance Agents, Builders  
**Scope:** Definition only — no execution or implementation implied  

---

## 1. Purpose

The Maturion Foreman Office App (“Foreman Office”) is a **continuous supervisory control system** designed to manage autonomous AI-driven software construction in environments where traditional, burst-based coding platforms are insufficient.

It exists to solve a single core problem:

> **Autonomous AI systems cannot safely build complex, governed software without continuous supervision, escalation, and decision authority.**

Foreman Office provides that supervision.

---

## 2. What This App Is (and Is Not)

### 2.1 What Foreman Office IS

Foreman Office is:

- An **always-on supervisory runtime**
- A **system of record for execution state**, not code
- A **managerial control plane** enforcing governance, QA, and escalation
- The **operational embodiment of governance canon**
- The **primary interface between autonomous AI execution and human authority**

Foreman Office **interprets and executes against governance**, but **does not define or modify governance**.

---

### 2.2 What Foreman Office IS NOT

Foreman Office is **not**:

- A code editor
- A CI/CD platform
- A GitHub replacement
- A log viewer
- A metrics dashboard
- A governance author
- A self-governing or self-modifying system

Foreman Office **never invents rules, relaxes governance, or bypasses controls**.

---

### 2.3 Platform-Wide Supervisory Role

Foreman Office is the **single, platform-wide supervisory and management authority** for all applications within the Maturion platform.

This means:

- All applications operate under governance interpreted and enforced by Foreman Office
- Escalation, exception handling, and owner decisions are centralised through Foreman Office
- Execution systems remain autonomous and decoupled
- No application embeds its own supervisory or governance authority

Foreman Office does **not** execute application logic, host runtimes, or replace application autonomy.  
It provides **coordination, governance enforcement, escalation, and oversight** across the platform.

---

## 3. Roles and Authority Model

### 3.1 Human Owner (Johan)

The Human Owner:

- Defines objectives and intent
- Approves, denies, or requests changes
- Intervenes only when escalated
- Never reviews code or logs
- Never manages PRs or workflows

The Human Owner is the **final authority**, not an operator.

---

### 3.2 Foreman (AI Supervisor)

The Foreman is:

- A **manager**, not a builder
- A **continuous supervisor**, not a task executor
- Accountable for planning, organising, leading, and control (POLC)
- Responsible for appointing and supervising builder agents
- Obligated to escalate when governance, scope, or clarity is insufficient

The Foreman **cannot implement code**, approve its own work, or bypass governance.

---

### 3.3 Builder Agents

Builder agents:

- Execute scoped technical work
- Operate only under Foreman appointment
- Never self-govern
- Never self-approve
- Never interpret governance independently
- Escalate blockers to the Foreman

---

## 4. Governance Supremacy

### 4.1 Canonical Governance

All execution is governed by **canonical governance artifacts** defined externally in the governance repository.

Foreman Office:

- Loads governance canon
- Validates integrity and versioning
- Applies governance as **read-only, non-negotiable authority**

Governance is **constitutional**, not advisory.

---

### 4.2 Governance Enforcement Semantics

If a governance violation is detected:

- Execution halts **or escalates** per canonical hard/soft stop rules
- No fallback behavior is permitted
- No silent continuation is allowed

Foreman Office **never weakens governance to proceed**.

---

## 5. Continuous Supervision Model

Foreman Office operates continuously and treats the following as **failure states**:

- Silence
- Stalled execution
- Missing updates
- Incomplete handovers
- Unexplained gate failures

“No update” is considered a **critical signal**, not a neutral state.

---

## 6. Memory & Provenance

Foreman Office records execution context, decisions, and outcomes as **operational memory**, governed by canonical memory policies.

Key principles:

- Execution memory is **read-only at runtime**
- All memory writes are **proposals**, never automatic
- Memory governance controls authority, retention, and auditability
- Provenance data is never inferred or retroactively altered

Memory exists to prevent repeated failure, not to enable learning without approval.

---

## 7. Human Interaction Model (UI / UX Operating Contract)

### 7.1 Purpose of the UI

The UI exists to support **executive decision-making**, not system inspection.

It is designed for a **non-coder human authority**.

---

### 7.2 Default UI State

By default, the UI shows **only**:

- Current build / wave status
- Active escalations (if any)
- Decisions requiring action

There are exactly **three actions** available:

- **Approve**
- **Deny**
- **Approve with changes**

---

### 7.3 Escalation UX

Every escalation presented to the Human Owner must include:

- What happened (concise, plain language)
- Why it matters (governance, risk, or objective impact)
- What is blocked
- What decision is required
- What happens if no action is taken

---

### 7.4 Drill-Down Rule

- Logs, traces, and raw diagnostics are **never shown by default**
- Drill-down is explicit and intentional
- GitHub logs are **not authoritative** and must never be the primary explanation

---

### 7.5 Explicit UI Non-Goals

The UI must **never** become:

- A log console
- A CI output viewer
- A metrics playground
- A real-time event stream
- A developer debugging surface

Noise is considered a **system defect**.

---

## 8. Cost, Performance, and Oversight

Foreman Office tracks:

- AI model usage
- Execution cost (in real currency)
- Anomalies and inefficiencies

Cost signals are **informational**, unless they indicate risk or abuse.

---

## 9. Watchdog & Independent Oversight

Foreman Office coexists with an **independent Watchdog authority**, which:

- Observes governance alignment
- Detects memory corruption
- Flags vision drift
- Reports anomalies independently

The Watchdog does not execute, modify, or override Foreman actions except in defined hard-stop scenarios.

---

## 10. Non-Goals and Explicit Constraints

Foreman Office:

- Does not self-improve
- Does not modify governance
- Does not self-authorise
- Does not bypass escalation
- Does not learn without approval

All evolution is **intentional, auditable, and owner-approved**.

---

## 11. Summary

Foreman Office is not a developer tool.

It is a **governed supervisory system** that enables autonomous AI construction **without surrendering human authority, governance discipline, or long-term system integrity**.

Its success is measured not by speed, but by:

- Absence of regression
- Absence of silent failure
- One-time build reliability
- Predictable escalation
- Calm, minimal human intervention

---

## 12. Architecture Reference

The canonical frozen architecture for this application is defined in:

**docs/architecture/TRUE_NORTH_FM_ARCHITECTURE.md**

All implementation MUST align with the True North Architecture.

---

**End of Document**
