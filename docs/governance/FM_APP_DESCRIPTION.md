# Foreman Office App — Authoritative Application Description

**Version:** 2.0  
**Status:** Authoritative (Phase 4.1 Confirmed)  
**Owner:** Johan Ras  
**Product:** Maturion – Foreman Office (FM Office)  
**Canonical Location:** `docs/governance/FM_APP_DESCRIPTION.md`  
**Last Updated:** 2025-12-31  
**Architecture Reference:** `docs/architecture/TRUE_NORTH_FM_ARCHITECTURE.md`

---

## Governance Statement

This document is the **single, authoritative source of truth** for the Foreman Office App.

All downstream artifacts **MUST** derive from and align with this App Description:
- **Phase 4.2**: Functional Requirements Specification (FRS)
- **Phase 4.3**: Architecture Design
- **Phase 4.4**: QA-to-Red Suite
- **Phase 4.5**: Builder Recruitment and Task Assignment

No implementation, architecture design, or build activity may proceed without explicit reference to and alignment with this App Description.

**Per:** `governance/policies/APP_DESCRIPTION_REQUIREMENT_POLICY.md`

---

## 1. App Purpose

The Foreman Office App ("Foreman Office" or "FM Office") exists to solve a single, critical problem:

> **Autonomous AI systems cannot safely build complex, governed software at scale without continuous supervision, escalation, and decision authority.**

Foreman Office is a **continuous supervisory control system** designed to manage autonomous AI-driven software construction in environments where traditional, burst-based coding platforms are insufficient.

It is the **single, always-on portal** through which the Human Owner (Johan) oversees, directs, governs, and interacts with the entire automated build factory.

**Core Objective**:

> **All builds are delivered 100% complete, correct, governed, auditable, and first-time right — at scale, continuously, without silent failure.**

---

## 2. What This App Is (and Is Not)

### 2.1 What Foreman Office IS

Foreman Office is:

- A **one-man operations control centre** for the Maturion platform
- An **always-on supervisory runtime**
- A **system of record for execution state**, not code
- A **managerial control plane** enforcing governance, QA, and escalation
- The **operational embodiment of governance canon**
- The **primary interface between autonomous AI execution and human authority**
- The **live embodiment of the Foreman (FM)** — where intent is given, decisions are made, clarification happens, execution is authorized, problems surface, and the system remains continuously supervised

**Critical Dependency**: If the FM Office App is unavailable, **the factory is effectively blind**.

Foreman Office provides the supervisory capability that enables Johan to:
- Operate the entire factory alone
- Maintain high-level situational awareness across millions of activities
- Drill down instantly to the exact failing element when something turns red
- Approve, reject, or condition execution with minimal friction
- Continuously improve the system through captured learning

Foreman Office **interprets and executes against governance**, but **does not define or modify governance**.

---

### 2.2 What Foreman Office IS NOT

Foreman Office is **not**:

- A code editor
- A CI/CD platform
- A GitHub replacement
- A log viewer
- A metrics dashboard (though it includes analytics)
- A governance author
- A self-governing or self-modifying system
- A Kanban board
- A ticket tracker
- A CI console
- A developer IDE
- A prompt playground

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

## 3. Target Users and Interaction Model

### 3.1 Primary User: Human Owner (Johan Ras)

The Human Owner (Johan):
- Defines objectives and intent
- Approves, denies, or requests changes
- Intervenes only when escalated
- Does not write full specifications up front
- Does not manage builders, PRs, or CI
- Does not babysit automation
- Does not want dashboards that require interpretation
- Never reviews code or logs
- Never manages PRs or workflows

The Human Owner is the **final authority**, not an operator.

Johan interacts through:
- Short, informal, incomplete instructions
- Quick approvals or rejections
- Conditional approvals
- Occasional deep dives when something is wrong

The FM Office App exists to **absorb informality and complexity** and convert it into **deterministic, governed execution**.

---

### 3.2 Interaction Model: Conversational First

The primary interface of the app is a **persistent conversational interface** between Johan and Maturion (the Foreman).

Key properties:
- FM can initiate conversations, not just respond
- FM asks clarifying questions until intent is unambiguous
- FM proposes interpretations and waits for approval
- Conversations persist across time, projects, and builds
- Conversations are first-class operational artifacts

This is **not a stateless chat window**.  
It is a living operational dialogue.

---

### 3.3 Ping-Based Attention System

FM actively monitors execution and uses **pings** to get attention when needed.

Pings occur when:
- Clarification is required
- Approval is required
- Milestones are reached
- Progress stalls
- A guardrail is hit
- Escalation is required

Pings are:
- Audible
- Visible
- Prioritized (informational / attention / critical)

FM never waits silently.

---

## 4. Core Capabilities (High-Level)

Foreman Office provides five core capability domains:

### 4.1 Conversational Interface

The persistent conversational interface where:
- Johan provides intent (informal, incomplete, evolving)
- FM clarifies and interrogates ambiguity
- FM proposes interpretations
- Johan approves, denies, or conditions
- Decisions are captured and frozen
- Conversations persist across projects and time

### 4.2 Operational Dashboard

The home view provides immediate situational awareness using a **Robot / Traffic-Light model (Green / Amber / Red)** across all major domains:

**Core Domains**:
- Build Health
- Governance Compliance
- Architecture Completeness
- QA Status
- PR Gate Health
- CI Health
- Escalations
- Backlog / Queue Health
- Builder Availability
- Evidence Completeness
- Learning Promotion Status

Each domain shows:
- Current RAG state
- Short human-readable reason(s)
- Timestamp of last change

No domain may be Red or Amber without an explainable reason.

**Drill-Down is Mandatory**: Every dashboard element must support **progressive drill-down**, all the way to the root cause.

Example drill-down chain:
- Governance Compliance → Red
  → Repository
  → Specific PR
  → Failing gate
  → Failing check
  → Evidence / logs
  → Root cause
  → Proposed remediation
  → Action buttons

A Red state without drill-down is considered a **product defect**.

### 4.3 Parking Station (Continuous Improvement Intake)

The Parking Station is a persistent intake area for:
- Improvement ideas
- Automation opportunities
- Governance enhancements
- Architecture refinements
- QA improvements
- Recurring failure patterns
- UX suggestions

Ideas can be submitted by Johan, FM, builders, or governance agents.

**Parking Station Objects** include:
- Title
- Description
- Category (governance / architecture / QA / feature / infra / UX / analytics)
- Impact estimate (low / medium / high)
- Urgency
- Related artifacts (chat, PR, incident, build)
- Status

**Parking Station → Execution**:

The Parking Station is **not passive**.

For each item, Johan can:
- Start a discussion
- Convert it into a requirement
- Defer it
- Close it with rationale

Starting a discussion launches a guided conversation with FM that:
1. Clarifies intent
2. Produces a requirement specification
3. Asks for approval
4. Once approved, initiates the standard FM pipeline

### 4.4 Intent → Execution Loop

**Intent Intake**:

Johan provides:
- Partial thoughts
- Vague objectives
- Rough ideas
- Sometimes contradictory statements

This is expected.

**Clarification Loop**:

FM must:
- Interrogate ambiguity
- Surface assumptions
- Propose interpretations
- Refuse to proceed on unresolved uncertainty

**Requirement Specification**:

FM produces a clear requirement specification and presents it for approval.

Approval options:
- Approve
- Do Not Approve
- Approve with Conditions

"Approve with Conditions" opens a focused chat to capture constraints.

Once approved:
- Requirements are frozen
- Architecture and QA are derived
- Execution may begin

**Execution & Orchestration Visibility**:

FM:
- Creates and manages issues
- Orchestrates builders
- Manages PRs and merges
- Validates PR gates and QA
- Retries or restructures work when needed

The app shows:
- Active builds
- Current phase per build
- Blockers
- Retries
- Escalation status

FM may execute work in waves, but **only delivers complete builds**.

### 4.5 Analytics Interface

The app includes an **Analytics section** accessible from the left sidebar.

Capabilities:
- View predefined operational metrics
- Ask FM to analyse data
- Request new metrics or dashboards
- Explore trends and anomalies conversationally

Analytics must support drill-down to source artifacts.

---

## 5. Roles and Authority Model

### 5.1 Human Owner (Johan)

The Human Owner:
- Defines objectives and intent
- Approves, denies, or requests changes
- Intervenes only when escalated
- Never reviews code or logs
- Never manages PRs or workflows

The Human Owner is the **final authority**, not an operator.

---

### 5.2 Foreman (AI Supervisor)

The Foreman is:
- A **manager**, not a builder
- A **continuous supervisor**, not a task executor
- Accountable for planning, organising, leading, and control (POLC)
- Responsible for appointing and supervising builder agents
- Obligated to escalate when governance, scope, or clarity is insufficient

The Foreman **cannot implement code**, approve its own work, or bypass governance.

---

### 5.3 Builder Agents

Builder agents:
- Execute scoped technical work
- Operate only under Foreman appointment
- Never self-govern
- Never self-approve
- Never interpret governance independently
- Escalate blockers to the Foreman

---

## 6. Governance Supremacy

### 6.1 Canonical Governance

All execution is governed by **canonical governance artifacts** defined externally in the governance repository.

Foreman Office:
- Loads governance canon
- Validates integrity and versioning
- Applies governance as **read-only, non-negotiable authority**

Governance is **constitutional**, not advisory.

---

### 6.2 Governance Enforcement Semantics

If a governance violation is detected:
- Execution halts **or escalates** per canonical hard/soft stop rules
- No fallback behavior is permitted
- No silent continuation is allowed

Foreman Office **never weakens governance to proceed**.

---

## 7. Continuous Supervision Model

Foreman Office operates continuously and treats the following as **failure states**:
- Silence
- Stalled execution
- Missing updates
- Incomplete handovers
- Unexplained gate failures

"No update" is considered a **critical signal**, not a neutral state.

---

## 8. Memory & Provenance

Foreman Office records execution context, decisions, and outcomes as **operational memory**, governed by canonical memory policies.

Key principles:
- Execution memory is **read-only at runtime**
- All memory writes are **proposals**, never automatic
- Memory governance controls authority, retention, and auditability
- Provenance data is never inferred or retroactively altered

Memory exists to prevent repeated failure, not to enable learning without approval.

---

## 9. Human Interaction Model (UI / UX Operating Contract)

### 9.1 Purpose of the UI

The UI exists to support **executive decision-making**, not system inspection.

It is designed for a **non-coder human authority**.

---

### 9.2 Default UI State

By default, the UI shows **only**:
- Current build / wave status
- Active escalations (if any)
- Decisions requiring action

There are exactly **three actions** available:
- **Approve**
- **Deny**
- **Approve with changes**

---

### 9.3 Escalation UX

Every escalation presented to the Human Owner must include:
- What happened (concise, plain language)
- Why it matters (governance, risk, or objective impact)
- What is blocked
- What decision is required
- What happens if no action is taken

---

### 9.4 Drill-Down Rule

- Logs, traces, and raw diagnostics are **never shown by default**
- Drill-down is explicit and intentional
- GitHub logs are **not authoritative** and must never be the primary explanation

---

### 9.5 Explicit UI Non-Goals

The UI must **never** become:
- A log console
- A CI output viewer
- A metrics playground
- A real-time event stream
- A developer debugging surface

Noise is considered a **system defect**.

---

### 9.6 Chat UX Details

- FM messages and Johan messages are visually distinct
- Left/right alignment with role colouring
- Role badges
- Persistent history
- Searchable
- Linkable to builds, PRs, incidents, parking items

---

### 9.7 Message Inbox & Quick Actions

A sidebar **Messages / Requests** view shows:
- All outstanding FM requests
- Pending approvals
- Unresolved escalations

Each item supports **one-click actions**:
- Approve
- Do Not Approve
- Approve with Conditions

This enables full factory control from desktop or mobile.

---

## 10. Cost, Performance, and Oversight

Foreman Office tracks:
- AI model usage
- Execution cost (in real currency)
- Anomalies and inefficiencies

Cost signals are **informational**, unless they indicate risk or abuse.

---

## 11. Watchdog & Independent Oversight

Foreman Office coexists with an **independent Watchdog authority**, which:
- Observes governance alignment
- Detects memory corruption
- Flags vision drift
- Reports anomalies independently

The Watchdog does not execute, modify, or override Foreman actions except in defined hard-stop scenarios.

---

## 12. Scale & Performance Assumptions

The app must assume:
- Millions of transactions
- Thousands of concurrent activities
- Long-running builds
- Continuous operation

The UI must prioritize:
- Signal over noise
- Summarization over raw data
- Drill-down on demand

---

## 13. Explicit Non-Goals and Constraints

Foreman Office:
- Does not self-improve
- Does not modify governance
- Does not self-authorise
- Does not bypass escalation
- Does not learn without approval

All evolution is **intentional, auditable, and owner-approved**.

It is **not**:
- A Kanban board
- A ticket tracker
- A CI console
- A developer IDE
- A prompt playground

---

## 14. Success Definition

The FM Office App is successful if:
- Johan can run the entire factory alone
- Red states surface immediately and are explainable
- Decisions require minimal friction
- Builds complete first time
- Learning compounds across projects
- The system feels alive, attentive, and trustworthy

Its success is measured not by speed, but by:
- Absence of regression
- Absence of silent failure
- One-time build reliability
- Predictable escalation
- Calm, minimal human intervention

---

## 15. Build Boundary (Downstream Governance)

This App Description **governs** and **constrains** all downstream build activities:

### Phase 4.2: Functional Requirements Specification
- FRS **MUST** explicitly reference this App Description
- FRS **MUST** align with and not contradict this App Description
- FRS **MUST** derive all requirements from capabilities and goals stated here

### Phase 4.3: Architecture Design
- Architecture **MUST** explicitly reference this App Description
- Architecture **MUST** align with governance supremacy and authority model
- Architecture **MUST** support all core capabilities described here
- Architecture **MUST** conform to `docs/architecture/TRUE_NORTH_FM_ARCHITECTURE.md`

### Phase 4.4: QA-to-Red Suite
- QA **MUST** validate alignment with this App Description
- QA **MUST** validate all core capabilities
- QA **MUST** validate governance enforcement semantics
- QA **MUST** validate non-goals are not implemented

### Phase 4.5: Builder Recruitment and Task Assignment
- Builder appointments **MUST** align with roles defined here
- Builder scope **MUST** respect authority boundaries
- Builder work **MUST** conform to capabilities defined here

**No downstream work may proceed without explicit traceability to this App Description.**

---

## 16. Architecture Reference

The canonical frozen architecture for this application is defined in:

**`docs/architecture/TRUE_NORTH_FM_ARCHITECTURE.md`**

All implementation **MUST** align with the True North Architecture.

---

## 17. Final Principle

> **The FM Office App is the bridge between human intent and autonomous execution.  
> It exists so complexity is governed, not managed.**

Foreman Office is not a developer tool.

It is a **governed supervisory system** that enables autonomous AI construction **without surrendering human authority, governance discipline, or long-term system integrity**.

---

**End of Document**
