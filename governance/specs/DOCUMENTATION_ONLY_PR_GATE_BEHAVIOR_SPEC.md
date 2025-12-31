# Documentation-Only PR Gate Behavior Specification

**Status**: Authoritative  
**Authority**: FM (Gate Release Authority)  
**Date**: 2025-12-31  
**Version**: 1.0.0

---

## I. Problem Statement

PR gate workflows report `action_required` status for documentation-only governance layer-down PRs, despite:
- No code changes
- No workflow modifications
- No readiness declaration
- All governance acceptance criteria being met

This creates ambiguity in gate semantics and blocks handover.

---

## II. Constitutional Authority

Per FM's role as gate-release authority, FM defines **deterministic behavior** for PR gates in scenarios not covered by canonical governance specifications.

This specification addresses the specific case of:
> Documentation-only governance PRs (including governance canon updates and layer-down evidence) that introduce **no code and no workflow changes**.

---

## III. Scope and Applicability

### In Scope
- Documentation-only PRs (markdown, text files, evidence artifacts)
- Governance layer-down PRs (no code, no implementation)
- Analysis and proposal PRs (no executable changes)

### Out of Scope
- PRs with code changes (even minor)
- PRs with workflow modifications
- PRs with schema/config changes
- PRs with test modifications

---

## IV. Canonical Gate Behavior Specification

### A. Documentation-Only PR Detection

A PR is classified as **documentation-only** if:

1. **All changed files** match these patterns:
   - `*.md` (Markdown documentation)
   - `*.txt` (Text files)
   - `*.json` (Evidence/governance artifacts in `governance/` or `foreman/evidence/`)
   - Files in `docs/`, `governance/`, `foreman/` directories

2. **No changed files** match these patterns:
   - `*.js`, `*.ts`, `*.jsx`, `*.tsx` (JavaScript/TypeScript code)
   - `*.py` (Python code)
   - `*.yml`, `*.yaml` in `.github/workflows/` (Workflow changes)
   - `*.json` in package configuration (e.g., `package.json`, `tsconfig.json`)
   - Test files in `tests/`, `__tests__/`, `*.test.*`, `*.spec.*`

3. **Detection Logic**:
```bash
# Get list of changed files in PR
CHANGED_FILES=$(git diff --name-only origin/main...HEAD)

# Check if any code/workflow files changed
if echo "$CHANGED_FILES" | grep -E '\.(js|ts|jsx|tsx|py)$|\.github/workflows/.*\.ya?ml$|package\.json$|tests/|__tests__/|\.test\.|\.spec\.'; then
  DOCUMENTATION_ONLY=false
else
  DOCUMENTATION_ONLY=true
fi
```

---

### B. Gate Behavior Matrix

For **documentation-only PRs**, gates behave as follows:

| Gate | Behavior | Outcome | Rationale |
|------|----------|---------|-----------|
| **Agent QA Boundary Enforcement** | Validate or Skip | ✅ GREEN | No QA reports = no boundary violations possible |
| **Build-to-Green Enforcement** | Validate or Skip | ✅ GREEN | No code changes = no test dodging possible |
| **Builder QA Gate** | Informational Skip | ℹ️ SKIP (Non-blocking) | No code to test = no QA report expected |
| **Governance Compliance Gate** | Validate or Skip | ✅ GREEN (if applicable role) | Validates governance artifacts if present |

---

### C. Outcome Classifications

#### 1. GREEN (Explicit Pass)

**Definition**: Gate validation executed and all checks passed.

**When to use**:
- Gate is applicable to agent role
- Gate validation logic executed
- All validation checks passed
- No violations detected

**GitHub Status**: `success`

**Example**:
```yaml
- name: Report Explicit GREEN
  run: |
    echo "✅ Gate PASSED - Explicit GREEN outcome"
    echo "All validation checks completed successfully"
    exit 0
```

---

#### 2. SKIP (Non-Applicable, Non-Blocking)

**Definition**: Gate is not applicable to this PR's agent role or context.

**When to use**:
- Gate applies to different agent role (e.g., Builder QA Gate for FM agent PR)
- Gate is context-specific and context doesn't match (e.g., no code changes for code-focused gate)
- Gate validation cannot execute due to lack of applicable artifacts

**GitHub Status**: `success` (with informational comment)

**Example**:
```yaml
- name: Report SKIP
  run: |
    echo "ℹ️ Gate SKIPPED - Not applicable to this PR"
    echo "Reason: Documentation-only PR, no code changes"
    echo "Status: Non-blocking"
    exit 0
```

---

#### 3. INFORMATIONAL (Advisory, Non-Blocking)

**Definition**: Gate provides information but does not block merge.

**When to use**:
- Gate detects conditions that don't warrant blocking
- Advisory checks for awareness only
- Non-critical violations that don't affect merge eligibility

**GitHub Status**: `success` (with informational comment)

**Example**:
```yaml
- name: Report INFORMATIONAL
  run: |
    echo "ℹ️ Gate completed with INFORMATIONAL status"
    echo "Advisory note: [details]"
    echo "Status: Non-blocking, informational only"
    exit 0
```

---

### D. Prohibited Outcomes

The following outcomes are **prohibited** for documentation-only PRs:

- ❌ `action_required` - Ambiguous, requires interpretation
- ❌ `failure` (unless true violation detected) - Blocks merge inappropriately  
- ❌ Undefined/implicit status - Creates unpredictability
- ❌ Context-dependent interpretation - Not deterministic

---

## V. Implementation Requirements

### A. Workflow Updates

Each PR gate workflow **MUST**:

1. **Detect documentation-only PRs** using canonical detection logic
2. **Branch behavior** based on detection:
   - If documentation-only AND no applicable artifacts → **SKIP**
   - If documentation-only AND applicable artifacts → **Validate and GREEN/FAIL**
   - If code changes present → **Normal validation logic**
3. **Report explicit outcome** in all cases (GREEN/SKIP/INFORMATIONAL/FAIL)
4. **Comment on PR** with clear outcome explanation
5. **Exit with success (0)** for GREEN/SKIP/INFORMATIONAL
6. **Exit with failure (1)** only for true violations

---

### B. Detection Implementation

Add to each gate workflow:

```yaml
- name: Detect Documentation-Only PR
  id: detect-doc-only
  run: |
    echo "🔍 Detecting PR type..."
    
    # Get changed files
    git fetch origin main --depth=50
    CHANGED_FILES=$(git diff --name-only origin/main...HEAD)
    
    echo "Changed files:"
    echo "$CHANGED_FILES"
    
    # Check for code/workflow changes
    if echo "$CHANGED_FILES" | grep -qE '\.(js|ts|jsx|tsx|py)$|\.github/workflows/.*\.ya?ml$|package\.json$|tests/|__tests__/|\.test\.|\.spec\.'; then
      echo "doc_only=false" >> $GITHUB_OUTPUT
      echo "📝 PR Type: Code/Workflow Changes"
    else
      echo "doc_only=true" >> $GITHUB_OUTPUT
      echo "📝 PR Type: Documentation-Only"
    fi
```

---

### C. Outcome Reporting

Add outcome-specific reporting:

```yaml
- name: Report Outcome
  if: always()
  run: |
    DOC_ONLY="${{ steps.detect-doc-only.outputs.doc_only }}"
    GATE_OUTCOME="${{ steps.validate.outputs.outcome }}"
    
    if [ "$DOC_ONLY" = "true" ]; then
      if [ -z "$GATE_OUTCOME" ] || [ "$GATE_OUTCOME" = "skip" ]; then
        echo "ℹ️ Gate SKIPPED - Documentation-only PR"
        echo "Status: Non-blocking"
        exit 0
      elif [ "$GATE_OUTCOME" = "success" ]; then
        echo "✅ Gate PASSED - Explicit GREEN"
        echo "Documentation-only PR validation complete"
        exit 0
      fi
    fi
    
    # Normal flow for code PRs
    if [ "$GATE_OUTCOME" = "failure" ]; then
      echo "❌ Gate FAILED"
      exit 1
    else
      echo "✅ Gate PASSED"
      exit 0
    fi
```

---

## VI. Specific Gate Implementations

### A. Agent QA Boundary Enforcement

**Behavior for documentation-only PRs**:
- Scan for QA reports
- If no QA reports found → **SKIP** (no boundary violations possible)
- If QA reports found → Validate normally and **GREEN/FAIL**

**Implementation**:
```yaml
- name: Documentation-Only Handling
  if: steps.detect-doc-only.outputs.doc_only == 'true' && steps.find-reports.outputs.found == 'false'
  run: |
    echo "ℹ️ Agent QA Boundary Enforcement - SKIP"
    echo "Reason: Documentation-only PR, no QA reports present"
    echo "Status: Non-blocking, no boundary violations possible"
    exit 0
```

---

### B. Build-to-Green Enforcement

**Behavior for documentation-only PRs**:
- Check if build-to-green enforcement is active
- If documentation-only → **SKIP** (no code to test)
- If code changes present → Validate normally

**Implementation**:
```yaml
- name: Documentation-Only Handling
  if: steps.detect-doc-only.outputs.doc_only == 'true'
  run: |
    echo "ℹ️ Build-to-Green Enforcement - SKIP"
    echo "Reason: Documentation-only PR, no code changes"
    echo "Status: Non-blocking, no test execution required"
    exit 0
```

---

### C. Builder QA Gate

**Behavior for documentation-only PRs**:
- Check for Builder QA Report
- If documentation-only AND no report → **SKIP** (informational)
- If report present → Validate normally

**Implementation**:
```yaml
- name: Documentation-Only Handling
  if: steps.detect-doc-only.outputs.doc_only == 'true' && steps.find-report.outputs.found == 'false'
  run: |
    echo "ℹ️ Builder QA Gate - SKIP"
    echo "Reason: Documentation-only PR, no code to test"
    echo "Status: Non-blocking, no Builder QA Report expected"
    exit 0
```

---

### D. Governance Compliance Gate

**Behavior for documentation-only PRs**:
- Check agent role applicability
- If applicable role AND governance artifacts present → Validate and **GREEN/FAIL**
- If no governance artifacts → **SKIP**
- If non-applicable role → **SKIP**

**Implementation**:
```yaml
- name: Documentation-Only Handling  
  if: steps.detect-doc-only.outputs.doc_only == 'true' && steps.find-artifacts.outputs.found == 'false'
  run: |
    echo "ℹ️ Governance Compliance Gate - SKIP"
    echo "Reason: Documentation-only PR, no governance artifacts present"
    echo "Status: Non-blocking"
    exit 0
```

---

## VII. PR Comment Templates

### A. Documentation-Only PR Detected

```markdown
ℹ️ **Documentation-Only PR Detected**

This PR contains only documentation changes:
- No code modifications
- No workflow changes
- No test changes

**Gate Behavior**:
- Gates will SKIP where not applicable
- Gates will validate governance artifacts if present
- All outcomes will be explicit (GREEN/SKIP)
- No ambiguous `action_required` status

**Merge Eligibility**: Determined by applicable gates only
```

---

### B. Gate Outcome Report (Documentation-Only)

```markdown
✅ **[Gate Name] - SKIP** (Documentation-Only PR)

**Outcome**: Non-blocking SKIP
**Reason**: No applicable artifacts for this gate in documentation-only PR
**Status**: This gate does not block merge

---

**Documentation-Only PR**: No code changes detected
**Applicable Gates**: Only gates relevant to documentation changes will enforce
```

---

## VIII. Success Criteria

This specification is successful when:

1. ✅ All gates report **explicit outcomes** (GREEN/SKIP/FAIL)
2. ✅ No `action_required` status for documentation-only PRs
3. ✅ Governance agents can determine proceed/hold **without interpretation**
4. ✅ Documentation-only PRs pass gates **deterministically**
5. ✅ No ad-hoc exceptions required
6. ✅ Blocked PR (from issue) can be re-evaluated cleanly

---

## IX. Governance Alignment

### A. Canonical Requirements

This specification **aligns with** canonical governance:
- ✅ Gates enforce canonical requirements only
- ✅ No reinterpretation of governance intent
- ✅ Agent role applicability respected
- ✅ Documentation-only PRs are valid workflow

### B. Non-Conflict Declaration

This specification **does not conflict with**:
- PR Gate Requirements Canon
- Agent Role Gate Applicability
- Two-Gatekeeper Model
- PR Gate Failure Handling Protocol

This specification **extends** canonical governance by defining behavior for the specific case of documentation-only PRs where canonical docs are silent.

---

## X. Audit Trail

### A. Decision Record

**Decision**: Documentation-only PRs shall receive explicit GREEN/SKIP outcomes, never `action_required`

**Rationale**:
- `action_required` is ambiguous and requires interpretation
- Documentation-only PRs are valid governance workflow
- Gates must be deterministic and predictable
- Governance agents must not invent exceptions

**Authority**: FM (gate-release authority per agent contract)

**Date**: 2025-12-31

---

### B. Precedent

This specification establishes precedent for:
- Documentation-only PR handling
- Explicit outcome reporting
- Deterministic gate behavior
- Context-aware gate enforcement

---

## XI. Version and Authority

**Version**: 1.0.0  
**Status**: Authoritative  
**Authority**: FM (Gate Release Authority)  
**Owner**: Foreman (FM)  
**Scope**: FM Repository PR Gates  
**Immutable**: true (once approved)

---

## XII. References

- **Issue**: Gate Release Behavior for Governance Layer-Down PRs
- **PR Gate Requirements Canon**: `governance/alignment/PR_GATE_REQUIREMENTS_CANON.md`
- **Agent Role Gate Applicability**: `governance/alignment/AGENT_ROLE_GATE_APPLICABILITY_REFERENCE.md`
- **Build Philosophy**: `BUILD_PHILOSOPHY.md`

---

**Deterministic. Predictable. Unambiguous.**

*END OF DOCUMENTATION-ONLY PR GATE BEHAVIOR SPECIFICATION*
