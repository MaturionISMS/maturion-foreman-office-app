# Runtime Risk Model Specification

## Purpose

Bridge the **live platform risks** to the SRMF/ERM risk constructs.

---

## 1. Risk Categories

- **Platform Availability**
- **Data Integrity**
- **Security & Privacy**
- **Compliance**
- **AI Behaviour**
- **User Experience / Adoption**

Each runtime risk:

- Links to ERM framework elements where applicable.
- References one or more behaviour events or incidents.

---

## 2. Risk Entry Fields

- `risk_id`
- `title`
- `category`
- `severity` – mapped to ERM scales
- `likelihood` – coarse rating (LOW/MEDIUM/HIGH)
- `impact` – coarse rating
- `current_controls` – high-level description
- `proposed_actions`
- `status` – `MONITORED | ACTION_REQUIRED | RESOLVED`

The structured storage format is described in `ai-memory/knowledge-base-schema.json`.

---

## 3. QA Rules

- Every CRITICAL incident must have at least one risk entry.
- Risks must use the same language and concepts as the ERM module True North documents.
