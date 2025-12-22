# FM Office App — Product Description (Authoritative)

**Status:** Authoritative v1  
**Owner:** Johan Ras  
**Product:** Maturion – Foreman Office (FM Office)

---

## 1. What This App Is

The **FM Office App** is a **one-man operations control centre** for the Maturion platform.

It is the **single, always-on portal** through which Johan oversees, directs, governs, and interacts with the entire automated build factory: governance, agents, builders, CI, PRs, QA, incidents, learning, analytics, and future platform operations.

This app is **not a dashboard** and **not a reporting tool**.

It is the **live embodiment of the Foreman (FM)** — the place where intent is given, decisions are made, clarification happens, execution is authorized, problems surface, and the system remains continuously supervised.

If the FM exists, this app exists.  
If this app is unavailable, **the factory is effectively blind**.

---

## 2. Core Purpose

The FM Office App exists to ensure that:

> **All builds are delivered 100% complete, correct, governed, auditable, and first-time right — at scale, continuously, without silent failure.**

The app enables Johan to:
- operate the entire factory alone
- maintain high-level situational awareness across millions of activities
- drill down instantly to the exact failing element when something turns red
- approve, reject, or condition execution with minimal friction
- continuously improve the system through captured learning

---

## 3. Primary User

### Johan Ras (Owner / Authority)

Johan:
- does not write full specifications up front
- does not manage builders, PRs, or CI
- does not babysit automation
- does not want dashboards that require interpretation

Johan interacts through:
- short, informal, incomplete instructions
- quick approvals or rejections
- conditional approvals
- occasional deep dives when something is wrong

The FM Office App exists to **absorb informality and complexity** and convert it into **deterministic, governed execution**.

---

## 4. Interaction Model (Foundational)

### 4.1 Conversational First

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

### 4.2 Ping-Based Attention System

FM actively monitors execution and uses **pings** to get attention when needed.

Pings occur when:
- clarification is required
- approval is required
- milestones are reached
- progress stalls
- a guardrail is hit
- escalation is required

Pings are:
- audible
- visible
- prioritized (informational / attention / critical)

FM never waits silently.

---

## 5. One-Man Operations Control Centre

### 5.1 Operational Dashboard (Home View)

The home view of the FM Office App is an **operations control dashboard** that provides immediate situational awareness.

It uses a **Robot / Traffic-Light model (Green / Amber / Red)** across all major domains.

#### Core Domains (v1)

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

---

### 5.2 Drill-Down Is Mandatory

Every dashboard element must support **progressive drill-down**, all the way to the root cause.

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

---

## 6. Parking Station (Continuous Improvement Intake)

The FM Office App includes a **Parking Station**.

This is a persistent intake area for:
- improvement ideas
- automation opportunities
- governance enhancements
- architecture refinements
- QA improvements
- recurring failure patterns
- UX suggestions

Ideas can be submitted by:
- Johan
- FM
- builders
- governance agents

---

### 6.1 Parking Station Objects

Each Parking Station item includes:
- title
- description
- category (governance / architecture / QA / feature / infra / UX / analytics)
- impact estimate (low / medium / high)
- urgency
- related artifacts (chat, PR, incident, build)
- status

---

### 6.2 Parking Station → Execution

The Parking Station is **not passive**.

For each item, Johan can:
- start a discussion
- convert it into a requirement
- defer it
- close it with rationale

Starting a discussion launches a guided conversation with FM that:
1. clarifies intent
2. produces a requirement specification
3. asks for approval
4. once approved, initiates the standard FM pipeline

---

## 7. Intent → Execution Loop

### 7.1 Intent Intake

Johan provides:
- partial thoughts
- vague objectives
- rough ideas
- sometimes contradictory statements

This is expected.

---

### 7.2 Clarification Loop

FM must:
- interrogate ambiguity
- surface assumptions
- propose interpretations
- refuse to proceed on unresolved uncertainty

---

### 7.3 Requirement Specification

FM produces a clear requirement specification and presents it for approval.

Approval options:
- Approve  
- Do Not Approve  
- Approve with Conditions  

“Approve with Conditions” opens a focused chat to capture constraints.

Once approved:
- requirements are frozen
- architecture and QA are derived
- execution may begin

---

## 8. Execution & Orchestration Visibility

FM:
- creates and manages issues
- orchestrates builders
- manages PRs and merges
- validates PR gates and QA
- retries or restructures work when needed

The app shows:
- active builds
- current phase per build
- blockers
- retries
- escalation status

FM may execute work in waves, but **only delivers complete builds**.

---

## 9. Analytics Interface

The app includes an **Analytics section** accessible from the left sidebar.

Capabilities:
- view predefined operational metrics
- ask FM to analyse data
- request new metrics or dashboards
- explore trends and anomalies conversationally

Analytics must support drill-down to source artifacts.

---

## 10. Chat UX Details

- FM messages and Johan messages are visually distinct
- Left/right alignment with role colouring
- Role badges
- Persistent history
- Searchable
- Linkable to builds, PRs, incidents, parking items

---

## 11. Message Inbox & Quick Actions

A sidebar **Messages / Requests** view shows:
- all outstanding FM requests
- pending approvals
- unresolved escalations

Each item supports **one-click actions**:
- Approve
- Do Not Approve
- Approve with Conditions

This enables full factory control from desktop or mobile.

---

## 12. Scale & Performance Assumptions

The app must assume:
- millions of transactions
- thousands of concurrent activities
- long-running builds
- continuous operation

The UI must prioritize:
- signal over noise
- summarization over raw data
- drill-down on demand

---

## 13. What This App Is Not

- Not a Kanban board  
- Not a ticket tracker  
- Not a CI console  
- Not a developer IDE  
- Not a prompt playground  

---

## 14. Success Definition

The FM Office App is successful if:
- Johan can run the entire factory alone
- Red states surface immediately and are explainable
- Decisions require minimal friction
- Builds complete first time
- Learning compounds across projects
- The system feels alive, attentive, and trustworthy

---

## 15. Final Principle

> **The FM Office App is the bridge between human intent and autonomous execution.  
> It exists so complexity is governed, not managed.**
