# Agent Boundary Checklist

**Purpose**: Verify agent boundary compliance before submitting PR

**Constitutional Authority**: `governance/alignment/AGENT_SCOPED_QA_BOUNDARIES.md`

---

## Pre-PR Agent Boundary Verification

Before submitting your PR, verify ALL of the following:

### Builder QA Execution

- [ ] **Builder QA executed by correct builder agent**
  - UI changes → ui-builder executes UI QA
  - API changes → api-builder executes API QA
  - Schema changes → schema-builder executes schema QA
  - Integration changes → integration-builder executes integration QA
  - QA infrastructure → qa-builder executes QA-of-QA

- [ ] **No cross-agent QA execution**
  - Did NOT run QA that belongs to another builder
  - Did NOT run governance QA (belongs to governance agent)
  - Did NOT run FM QA (belongs to FM agent)

### Governance QA Boundaries

- [ ] **No governance QA in builder scope**
  - Did NOT validate governance artifacts (governance agent responsibility)
  - Did NOT check compliance rules (governance agent responsibility)
  - Did NOT verify canonical governance consumption (governance agent responsibility)

### FM QA Boundaries

- [ ] **No FM QA in builder scope**
  - Did NOT validate FM architecture (FM agent responsibility)
  - Did NOT check FM platform readiness (FM agent responsibility)
  - Did NOT verify FM orchestration logic (FM agent responsibility)

### Agent Attribution

- [ ] **Agent ID present in all artifacts**
  - Builder QA Report includes correct `agent_id` field
  - Evidence artifacts reference executing agent
  - No artifacts missing agent attribution

- [ ] **Agent ID matches builder responsibility**
  - `agent_id` matches the builder responsible for this work
  - No mismatched agent IDs
  - No generic or placeholder agent IDs

---

## Violation Detection

If any checklist item is NOT checked, you have an **agent boundary violation**.

### What to Do

1. **STOP** - Do not submit PR
2. **Review** - Identify which QA was executed by wrong agent
3. **Correct** - Re-run QA with correct agent
4. **Verify** - Re-check this checklist
5. **Only then submit PR**

---

## Catastrophic Violation Categories

The following are **CATASTROPHIC** violations and MUST be escalated:

- ❌ Builder executed governance QA
- ❌ Builder executed FM QA
- ❌ Multiple agents executed same QA
- ❌ Agent attribution missing entirely

**Escalation**: If any catastrophic violation detected, escalate to Foreman immediately. Do NOT attempt to fix without guidance.

---

## References

- **Canonical Agent Boundaries**: `governance/alignment/AGENT_SCOPED_QA_BOUNDARIES.md`
- **PR Gate Requirements**: `governance/alignment/PR_GATE_REQUIREMENTS_CANON.md`
- **Agent Boundary Gate**: `.github/workflows/agent-boundary-gate.yml`

---

**Version**: 1.0.0  
**Last Updated**: 2025-12-30
