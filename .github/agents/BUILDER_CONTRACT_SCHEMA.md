# Builder Contract Schema
## Machine-Readable Builder Agent Contract Specification

**Version**: 1.0  
**Status**: CANONICAL SCHEMA  
**Authority**: Builder Recruitment Automation Corrective Design  
**Location**: `.github/agents/BUILDER_CONTRACT_SCHEMA.md`

---

## Purpose

This schema defines the required structure and format for all builder agent contracts in the Maturion ISMS ecosystem. Builder contracts MUST conform to this schema to enable automated builder recruitment, selection, and task assignment.

---

## File Location

All builder contracts MUST be located at:
```
.github/agents/<builder-id>.md
```

Examples:
- `.github/agents/ui-builder.md`
- `.github/agents/api-builder.md`
- `.github/agents/schema-builder.md`

---

## File Format

Builder contracts MUST use:
- **YAML frontmatter** for machine-readable metadata
- **Markdown body** for human-readable documentation

### Format Structure

```markdown
---
# YAML frontmatter (machine-readable)
builder_id: <builder-id>
builder_type: <type>
version: <version>
status: <status>
...
---

# Markdown body (human-readable)
## Section 1
Content...
```

---

## Required YAML Frontmatter Fields

### 1. builder_id (REQUIRED)

**Type**: `string`  
**Description**: Unique identifier for this builder  
**Format**: `lowercase-with-hyphens`  
**Example**: `ui-builder`

**Validation**:
- Must match filename (e.g., `ui-builder.md` → `builder_id: ui-builder`)
- Must be unique across all builders
- Must contain only lowercase letters, numbers, and hyphens

### 2. builder_type (REQUIRED)

**Type**: `string`  
**Description**: Classification of builder role  
**Allowed Values**: 
- `specialized` — Domain-specific builder (UI, API, schema, integration)
- `qa` — Quality assurance and testing builder
- `cross-cutting` — Builders that span multiple domains (rare)

**Example**: `builder_type: specialized`

### 3. version (REQUIRED)

**Type**: `string`  
**Description**: Contract version (semantic versioning)  
**Format**: `major.minor.patch`  
**Example**: `version: 1.0.0`

### 4. status (REQUIRED)

**Type**: `string`  
**Description**: Current recruitment status  
**Allowed Values**:
- `recruited` — Builder recruited and ready for assignment
- `active` — Builder actively working on assigned tasks
- `suspended` — Builder temporarily unavailable
- `revoked` — Builder recruitment revoked (no longer usable)

**Example**: `status: recruited`

### 5. capabilities (REQUIRED)

**Type**: `array of strings`  
**Description**: List of technical capabilities this builder possesses  
**Example**:
```yaml
capabilities:
  - ui
  - frontend
  - components
  - styling
```

**Validation**:
- Must contain at least 1 capability
- Capabilities must be lowercase, single-word or hyphenated
- Must align with `foreman/builder/builder-capability-map.json`

### 6. responsibilities (REQUIRED)

**Type**: `array of strings`  
**Description**: High-level responsibilities assigned to this builder  
**Example**:
```yaml
responsibilities:
  - UI components
  - Layouts
  - Wizards
```

**Validation**:
- Must contain at least 1 responsibility
- Must align with `foreman/builder-manifest.json`

### 7. forbidden (REQUIRED)

**Type**: `array of strings`  
**Description**: Actions or areas this builder MUST NOT perform or access  
**Example**:
```yaml
forbidden:
  - Backend logic
  - Cross-module logic
  - Database schema changes
```

**Validation**:
- Must contain at least 1 forbidden action
- Must align with `foreman/builder-manifest.json`

### 8. permissions (REQUIRED)

**Type**: `object`  
**Description**: File system access permissions  
**Structure**:
```yaml
permissions:
  read:
    - <glob-pattern>
  write:
    - <glob-pattern>
```

**Example**:
```yaml
permissions:
  read:
    - "foreman/**"
    - "architecture/**"
    - "governance/**"
  write:
    - "apps/*/frontend/**"
    - "apps/*/components/**"
```

**Validation**:
- Must contain at least one `read` pattern
- Must contain at least one `write` pattern
- Must align with `foreman/builder/builder-permission-policy.json`

### 9. recruitment_date (REQUIRED)

**Type**: `string`  
**Description**: ISO 8601 date when builder was recruited  
**Format**: `YYYY-MM-DD`  
**Example**: `recruitment_date: 2025-12-30`

### 10. qa_range (OPTIONAL)

**Type**: `object`  
**Description**: QA range assignment for builders in build waves  
**Structure**:
```yaml
qa_range:
  start: <qa-id>
  end: <qa-id>
  count: <integer>
```

**Example**:
```yaml
qa_range:
  start: QA-019
  end: QA-057
  count: 39
```

**When Required**: During build wave assignment (Wave 1.0+), not during initial recruitment

---

## Required Markdown Sections

All builder contracts MUST include the following markdown sections:

### 1. Purpose (## Purpose)

**Content**: Brief description of why this builder exists and its role in the ecosystem

**Example**:
```markdown
## Purpose

The UI Builder is responsible for implementing all user interface components,
layouts, and interactive wizards in the Foreman Office App.
```

### 2. Responsibilities (## Responsibilities)

**Content**: Detailed list of what this builder is responsible for

**Format**: Bulleted list or subsections

**Example**:
```markdown
## Responsibilities

- Implement React UI components from architecture specifications
- Create responsive layouts using existing design system
- Build multi-step wizards for conversational interface
- Ensure accessibility compliance (WCAG 2.1 AA)
```

### 3. Capabilities (## Capabilities)

**Content**: Technical skills and domains this builder can work in

**Example**:
```markdown
## Capabilities

- **UI Development**: React components, hooks, state management
- **Frontend Technologies**: TypeScript, JSX, CSS-in-JS
- **Styling**: CSS modules, responsive design, accessibility
- **Component Architecture**: Reusable components, composition patterns
```

### 4. Forbidden Actions (## Forbidden Actions)

**Content**: Explicit list of what this builder MUST NOT do

**Example**:
```markdown
## Forbidden Actions

❌ **Backend Logic**: No API handlers, business logic, or data processing  
❌ **Database Changes**: No schema modifications or migrations  
❌ **Cross-Module Logic**: No integration code between modules  
❌ **Governance Changes**: No modification of governance artifacts
```

### 5. Permissions (## Permissions)

**Content**: Detailed explanation of file system access rights

**Example**:
```markdown
## Permissions

### Read Access
- `foreman/**` — Builder specifications and task definitions
- `architecture/**` — Architecture specifications for implementation
- `governance/**` — Governance rules and constraints

### Write Access
- `apps/*/frontend/**` — Frontend application code
- `apps/*/components/**` — UI component libraries
```

### 6. Recruitment Information (## Recruitment Information)

**Content**: Metadata about when and how builder was recruited

**Example**:
```markdown
## Recruitment Information

**Recruited**: 2025-12-30 (Wave 0.1)  
**Recruited By**: Maturion Foreman (FM)  
**Validation Status**: ✅ PASS  
**Contract Version**: 1.0.0
```

### 7. Gate Binding (## Gate Binding) [OPTIONAL during recruitment]

**Content**: Information about QA gates and PR requirements

**Example**:
```markdown
## Gate Binding

**PR Gate**: Builder QA Gate (`.github/workflows/builder-qa-gate.yml`)  
**Required Artifacts**:
- Builder QA Report (`BUILDER_QA_REPORT.md`)
- QA coverage evidence
- Architecture alignment proof
```

---

## Complete Example

```markdown
---
builder_id: ui-builder
builder_type: specialized
version: 1.0.0
status: recruited
capabilities:
  - ui
  - frontend
  - components
  - styling
responsibilities:
  - UI components
  - Layouts
  - Wizards
forbidden:
  - Backend logic
  - Cross-module logic
  - Database schema changes
permissions:
  read:
    - "foreman/**"
    - "architecture/**"
    - "governance/**"
  write:
    - "apps/*/frontend/**"
    - "apps/*/components/**"
recruitment_date: 2025-12-30
---

# UI Builder Contract

## Purpose

The UI Builder is responsible for implementing all user interface components,
layouts, and interactive wizards in the Foreman Office App according to
architecture specifications and UX requirements.

## Responsibilities

- Implement React UI components from architecture specifications
- Create responsive layouts using existing design system
- Build multi-step wizards for conversational interface
- Ensure accessibility compliance (WCAG 2.1 AA)
- Maintain component documentation and examples

## Capabilities

- **UI Development**: React components, hooks, state management
- **Frontend Technologies**: TypeScript, JSX, CSS-in-JS
- **Styling**: CSS modules, responsive design, accessibility
- **Component Architecture**: Reusable components, composition patterns

## Forbidden Actions

❌ **Backend Logic**: No API handlers, business logic, or data processing  
❌ **Database Changes**: No schema modifications or migrations  
❌ **Cross-Module Logic**: No integration code between modules  
❌ **Governance Changes**: No modification of governance artifacts

## Permissions

### Read Access
- `foreman/**` — Builder specifications and task definitions
- `architecture/**` — Architecture specifications for implementation
- `governance/**` — Governance rules and constraints

### Write Access
- `apps/*/frontend/**` — Frontend application code
- `apps/*/components/**` — UI component libraries

## Recruitment Information

**Recruited**: 2025-12-30 (Wave 0.1)  
**Recruited By**: Maturion Foreman (FM)  
**Validation Status**: ✅ PASS  
**Contract Version**: 1.0.0  
**Canonical Reference**: `foreman/builder/ui-builder-spec.md`

## Gate Binding

**PR Gate**: Builder QA Gate (`.github/workflows/builder-qa-gate.yml`)  
**Required Artifacts**:
- Builder QA Report (`BUILDER_QA_REPORT.md`)
- QA coverage evidence
- Architecture alignment proof

---

**Contract Status**: ✅ ACTIVE  
**Last Updated**: 2026-01-01
```

---

## Validation Rules

### Schema Validation

A valid builder contract MUST:
1. ✅ Be located in `.github/agents/<builder-id>.md`
2. ✅ Have valid YAML frontmatter with all required fields
3. ✅ Have `builder_id` matching filename
4. ✅ Have all required markdown sections
5. ✅ Align with `foreman/builder-manifest.json` responsibilities/forbidden
6. ✅ Align with `foreman/builder/builder-capability-map.json` capabilities
7. ✅ Align with `foreman/builder/builder-permission-policy.json` permissions
8. ✅ Have no placeholder text ("TBD", "TODO", etc.)
9. ✅ Have valid ISO 8601 recruitment date
10. ✅ Have valid semantic version number

### Automated Validation

Validation should be performed:
- On contract creation (new builder recruitment)
- On contract modification (PR changes to contracts)
- During platform readiness verification
- Before Wave 1.0+ builder assignment

### Validation Failure Handling

If validation fails:
- ❌ Builder CANNOT be recruited
- ❌ Platform readiness CANNOT be approved
- ❌ Wave execution CANNOT proceed
- 🔴 Escalation required

---

## Schema Versioning

**Current Version**: 1.0  
**Compatibility**: All contracts must specify schema version they conform to

Future schema changes:
- **Major version bump**: Breaking changes (require contract updates)
- **Minor version bump**: New optional fields (backward compatible)
- **Patch version bump**: Clarifications only (no changes required)

---

## Enforcement

This schema is **mandatory** and **enforced** via:
1. Platform readiness validation
2. CI checks on `.github/agents/` changes
3. Builder recruitment approval process
4. Wave execution preconditions

**Ratchet Condition**: No builder recruitment without schema-conformant contract (BL-016).

---

**Schema Authority**: Maturion Foreman (FM)  
**Schema Status**: CANONICAL — ACTIVE  
**Last Updated**: 2026-01-01
