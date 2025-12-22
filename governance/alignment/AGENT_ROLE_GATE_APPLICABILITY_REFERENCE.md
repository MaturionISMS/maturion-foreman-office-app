# Agent Role Gate Applicability (Canonical Reference)

**Status**: Canonical Reference  
**Authority**: Corporate Governance Canon (`maturion-foreman-governance`)  
**FM Scope**: Enforcement-Only (No Modification)

---

## Purpose

This document references the **canonical** `AGENT_ROLE_GATE_APPLICABILITY.md` from the governance repository and ensures FM enforcement respects agent-role-based gate applicability.

---

## Canonical Source

**Repository**: `maturion-foreman-governance`  
**Document**: `AGENT_ROLE_GATE_APPLICABILITY.md`

This document is **authoritative** and defines which PR gates apply to which agent roles.

---

## Key Principle (Canonical)

> **Agent role determines gate applicability, not file paths.**

Gates must not infer applicability from changed files or paths. Agent role is the sole determinant.

---

## FM Enforcement Requirements

FM workflows **must**:

1. **Respect agent role** as provided in PR metadata, `.agent` file, or agent declaration
2. **Apply only applicable gates** for the declared agent role
3. **Skip non-applicable gates** without treating as failure
4. **Never infer role** from file paths, commit messages, or other heuristics

FM workflows **must not**:

- ❌ Enforce builder-only gates against governance/FM agents
- ❌ Infer agent role from changed paths
- ❌ Apply all gates universally regardless of role
- ❌ Require artifacts from non-applicable agent scopes

---

## Agent Role Declarations

FM recognizes the following agent role declarations (in order of precedence):

1. **Explicit PR label**: `agent-role:builder`, `agent-role:governance`, `agent-role:fm`
2. **`.agent` file** in repository root (parsed for `role` or `authority` field)
3. **PR title prefix**: `[Builder]`, `[Governance]`, `[FM]`
4. **Default**: If none present, default to repository owner role (FM for FM repo)

---

## Gate Applicability Matrix (Canonical Reference)

| Gate                          | Builder | Governance Admin | FM Agent |
|-------------------------------|---------|------------------|----------|
| Agent Boundary Enforcement    | ✅      | ✅               | ✅       |
| Builder QA Gate               | ✅      | ❌               | ❌       |
| Build-to-Green Enforcement    | ✅      | ❌               | ✅       |
| FM Architecture Gate          | ❌      | ❌               | ✅       |
| Governance Artifact Gate      | ❌      | ✅               | ❌       |

**Note**: This matrix is a simplified reference. Refer to canonical `AGENT_ROLE_GATE_APPLICABILITY.md` for complete rules.

---

## Predictability Invariant (Canonical)

> **If all checklist items for the active agent role are satisfied, the PR gate MUST pass.**

If a gate blocks compliant work:
- This is a **governance alignment defect**
- Document the mismatch with checklist citations
- Escalate (do not invent artifacts or expand scope)

---

## FM Implementation

FM workflows implement agent role detection via:

```yaml
# Workflow: Detect agent role
- name: Detect Agent Role
  id: agent-role
  run: |
    # Check for explicit PR label (highest precedence)
    if [[ "${{ github.event.pull_request.labels }}" =~ agent-role:([a-z]+) ]]; then
      ROLE="${BASH_REMATCH[1]}"
    # Check .agent file
    elif [ -f ".agent" ] && grep -q "role\|authority" ".agent"; then
      ROLE=$(grep -E "role|authority" .agent | head -1 | cut -d: -f2 | tr -d ' "')
    # Check PR title
    elif [[ "${{ github.event.pull_request.title }}" =~ ^\[(Builder|Governance|FM)\] ]]; then
      ROLE=$(echo "${BASH_REMATCH[1]}" | tr '[:upper:]' '[:lower:]')
    # Default to repo owner role
    else
      ROLE="fm"  # For FM repository
    fi
    
    echo "role=$ROLE" >> $GITHUB_OUTPUT
    echo "Detected agent role: $ROLE"
```

---

## Compliance Requirements

FM must ensure:

1. **All workflows** respect agent role applicability
2. **Non-applicable gates** skip gracefully (no failure)
3. **Applicable gates** enforce strictly
4. **No path-based inference** of agent role

---

## References

- **Canonical Document**: `maturion-foreman-governance/AGENT_ROLE_GATE_APPLICABILITY.md`
- **PR Gate Release Checklists**: 
  - `PR_GATE_RELEASE_CHECKLIST_BUILDER.md`
  - `PR_GATE_RELEASE_CHECKLIST_GOVERNANCE_ADMIN.md`
  - `PR_GATE_RELEASE_CHECKLIST_FM.md`
- **Two-Gatekeeper Model**: `governance/alignment/TWO_GATEKEEPER_MODEL.md`

---

**Last Updated**: 2025-12-22  
**Authority**: Corporate Governance Canon  
**FM Status**: Enforcement-Only (No Local Modification)
