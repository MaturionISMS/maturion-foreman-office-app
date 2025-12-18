# AI Drift Monitor Specification

## Purpose

Detect when AI behaviour changes in ways that may:

- Reduce quality,
- Violate expectations,
- Or threaten compliance / security.

Drift monitoring is based on **patterns and aggregates**, never raw conversations.

---

## 1. Drift Types

1. **Model Configuration Drift**
   - Underlying model family or version changes
   - Routing policy changes
2. **Behaviour Drift**
   - Increased refusal rate or over-compliance
   - Increased hallucination indicators (contradict known architecture/QA specs)
3. **Safety Drift**
   - More frequent triggering of safety/guardrail blocks
   - New categories of unsafe attempts

---

## 2. Signals

- Longitudinal sampling of:
  - Response types by category
  - QA evaluation scores
  - Safety block events
- Comparison against:
  - Baselines stored in `foreman/ai-memory/reasoning-patterns-schema.json`
  - Architecture rules in SRMF and module True North docs

---

## 3. Drift Classification

- **Benign Drift** – harmless and neutral or positive
- **Watch Drift** – unusual, monitor for some time
- **Actionable Drift** – requires architecture/QA review
- **Critical Drift** – requires immediate rollback or reconfiguration

Each drift item is summarised and stored via the runtime knowledge schemas.

---

## 4. Integration

- Generates upgrade candidates into `upgrade/upgrade-insights-schema.json`
- Feeds architectural lessons into `ai-memory/architectural-lessons.md`
- Triggers QA-of-QA review for affected modules
