# Johan’s Foreman Office  
## Application Description (Wave 0 – Authoritative)

---

## 1. Purpose

Johan’s Foreman Office is an **always-on supervisory application** designed to plan, govern, monitor, and control AI-assisted software execution.

It exists to solve a proven problem:

> Burst-based AI platforms (e.g. GitHub agents) are excellent executors, but **cannot function as continuous supervisors**.

Foreman Office provides the missing layer:
- persistent awareness
- planning and control (POLC)
- governance enforcement
- execution visibility
- human-in-the-loop oversight without micromanagement

This application is the **brain and cockpit** of the Maturion build system.

---

## 2. What This Application Is (and Is Not)

### 2.1 This Application IS
- An **always-on AI supervisor**
- A **program and wave orchestrator**
- A **governance enforcement engine**
- A **live execution cockpit** for the human governor
- The foundational runtime for **PIT (Project Implementation Tracker)**

### 2.2 This Application IS NOT
- A CI/CD system
- A GitHub replacement
- A passive dashboard
- A one-off execution script
- A chat-only interface

GitHub remains the **system of record for code**.  
Foreman Office is the **system of record for execution state and control**.

---

## 3. Primary Roles

### 3.1 Johan (Human Governor)
- Defines intent (“Build this”, “Implement Annex 1”)
- Reviews plans before execution
- Monitors live progress
- Intervenes only at governance or decision points
- Verifies outcomes via UI and evidence, not source code

### 3.2 Foreman (AI Supervisor)
- Always-on
- Plans execution (POLC – Planning)
- Supervises execution (POLC – Leading)
- Monitors and corrects execution (POLC – Control)
- Enforces governance rules
- Coordinates builders
- Reports continuously

### 3.3 Builder Agents (Executors)
- Stateless or semi-stateless
- Execute clearly bounded tasks
- Must obey a strict builder contract
- Never bypass governance or QA
- Never report directly to Johan

---

## 4. Core Concepts

### 4.1 Programs, Waves, and Tasks
Execution is structured as:
- **Program** (e.g. “Annex 1”)
- **Waves** (ordered, dependency-aware)
- **Tasks** (atomic build units)

Each level tracks:
- state
- progress percentage
- evidence
- blockers (classified)

---

### 4.2 Governance Supremacy
Governance rules override:
- speed
- convenience
- automation
- autonomy

If governance is violated, execution **halts automatically**.

Mandatory principles include:
- Governance Supremacy Rule (GSR)
- One-Prompt One-Job Doctrine (OPOJD)
- One-Time Build / True North
- Architecture → Red QA → Build to Green
- Zero Test Debt

---

### 4.3 Continuous Supervision (Non-Negotiable)
Foreman Office must:
- never sleep
- maintain execution context across sessions
- know what is happening *right now*
- detect stalls without human prompting

“No update” is treated as a failure state.

---

## 5. Foreman ↔ Johan Interaction Model

The application must provide a **live, project-specific interaction surface** that allows Foreman to:

- present plans for approval
- request decisions
- report progress
- escalate blockers
- provide summaries with evidence

This interaction **must not depend on GitHub comments**.

---

## 6. Monitoring & Visibility Requirements

At any moment, Johan must be able to see:
- what program is active
- which wave is executing
- which tasks are running
- last heartbeat per builder
- current blockers and classification
- pending decisions
- provenance (who did what, with which model)

---

## 7. Builder Orchestration

Foreman Office decides:
- which builder backend to use
- when to escalate models
- how to recover from stalled execution

Builder backends may include:
- local/manual builder (human acting as agent)
- hosted runtime (e.g. Render)
- burst platforms (e.g. Copilot)

Builder behavior is governed by a **strict builder contract**.

---

## 8. Provenance & Auditability

For every action, the system records:
- actor (Foreman / Builder)
- backend used
- model used (best-effort disclosure)
- escalation rationale
- evidence artifacts

This data is required for:
- audits
- learning
- PIT integration
- governance verification

---

## 9. Relationship to PIT (Project Implementation Tracker)

Foreman Office is designed so that:
- PIT emerges naturally from execution telemetry
- no retrofit is required later

All programs, waves, tasks, heartbeats, and evidence must be PIT-compatible from day one.

---

## 10. Out of Scope (Wave 0)

The following are explicitly out of scope for this wave:
- full PIT UI
- autonomous mega-batch execution
- billing or user management
- external integrations

---

## 11. Success Criteria

This application is successful when:
- Johan is never blind to execution state
- execution does not silently stall
- governance is enforced without micromanagement
- builders can fail without collapsing the program
- large backlogs can be executed safely in batches

---

## 12. Authority

This document is the **authoritative point of departure**.

No architecture, QA, or code may be produced that contradicts this description.
