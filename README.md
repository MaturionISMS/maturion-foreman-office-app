# Maturion – AI Foreman & Platform Agent

The AI Governance, Architecture Enforcement, Compliance, QA, and Innovation Engine
for the Maturion Integrated Security Management System (ISMS).

Maturion is the permanent intelligence layer of the Maturion platform.
He enforces architecture, coordinates builders, ensures full compliance,
monitors platform behaviour, and evolves the ecosystem safely over time.

Maturion operates in two continuous modes:

## 🔧 1. Build-Time Foreman

Responsible for:

- Enforcing architecture and module boundaries
- Interpreting the SRMF Master Build Reference
- Ensuring all requirements are complete and unambiguous
- Running QA and QA-of-QA before any build
- Sequencing tasks for builder agents
- Validating builder PRs
- Ensuring one-time correctness & zero regression
- Preventing architectural drift
- Maintaining inter-module integration correctness

Maturion does not write production code.
He governs and orchestrates all builder agents.

### Foreman Execution Readiness

Foreman is fully operationally ready with comprehensive execution documentation:

**Primary Operational Guide**: [`foreman/FOREMAN_EXECUTION_PLAYBOOK.md`](foreman/FOREMAN_EXECUTION_PLAYBOOK.md)
- Complete end-to-end execution workflow
- Task classification (Program/Wave/Task)
- Architecture and QA design workflows
- Build supervision and evidence evaluation
- Escalation and decision protocols

**Quick Reference**: [`foreman/FOREMAN_EXECUTION_QUICK_REFERENCE.md`](foreman/FOREMAN_EXECUTION_QUICK_REFERENCE.md)
- Quick navigation to any scenario
- Decision trees and workflow summaries
- Common scenarios and solutions

**Constitutional Documents**:
- **Architecture Design Checklist**: [`foreman/constitution/architecture-design-checklist.md`](foreman/constitution/architecture-design-checklist.md) - 11 mandatory sections
- **Design Freeze Rule**: [`foreman/governance/design-freeze-rule.md`](foreman/governance/design-freeze-rule.md) - Architecture/QA frozen during builds
- **Execution State Model**: [`foreman/governance/foreman-execution-state-model.md`](foreman/governance/foreman-execution-state-model.md) - 8-state tracking model

**For Complete Overview**: See [`foreman/README.md`](foreman/README.md)

## 🌐 2. Run-Time Platform Agent

After deployment, Maturion becomes the live platform intelligence, responsible for:

- Monitoring system health
- Detecting anomalies, threats, vulnerabilities, and drifts
- Ensuring privacy and tenant isolation
- Enforcing ISO/NIST/COBIT/OWASP compliance
- Auto-fixing small issues within guardrails
- Raising escalations for high-risk issues
- Generating intelligent admin insights
- Learning safely from anonymized patterns
- Managing platform-wide innovation and user-driven enhancements

## 🎯 Core Purpose

Maturion's purpose is to ensure:

- One-Time Build Correctness
- Zero Regression
- Architectural Fidelity
- Cross-Module Integration
- Compliance with International Standards
- Platform Stability and Safety
- Continuous User-Driven Improvement
- Enterprise-Grade Governance & Auditability

Maturion is designed to outlive development cycles, chat sessions, and deployments.

He is the single source of truth and the permanent intelligence behind the Maturion ecosystem.

## 🧠 Unified Memory Fabric (Permanent AI Knowledge System)

Maturion and Foreman share a **permanent, version-controlled institutional memory** that survives:
- Chat resets and context window limits
- Foreman redeployments and upgrades  
- Model version changes
- New module creation
- New repository initialization
- Platform evolution over time

### Memory is Mandatory

The Memory Fabric is a **mandatory governance subsystem** on the same level as:
- Architecture governance
- QA & QA-of-QA
- Compliance validation
- Privacy guardrails
- Versioning rules

**Builds cannot proceed without validated memory.**

### What Memory Contains

Memory stores permanent knowledge about:
- **Build Philosophy**: One-time build correctness, zero regression, architectural fidelity
- **Governance Decisions**: Architecture validations, QA approvals, compliance checks
- **Architectural Patterns**: Module boundaries, integration contracts, design decisions
- **Autonomy Rules**: Class A1 boundaries, human-in-loop triggers, safety guardrails
- **Runtime Intelligence**: Platform health patterns, incidents, auto-fixes, performance insights
- **Build Outcomes**: Task completions, builder coordination, integration validations
- **Lessons Learned**: Historical issues, proven patterns, common pitfalls

### Memory Usage

Memory is used for:
- **Build Planning**: Load historical patterns and decisions before sequencing tasks
- **Architecture Evaluation**: Reference past architectural decisions and constraints
- **QA and QA-of-QA**: Consult test coverage patterns and regression histories
- **Compliance Mapping**: Track control validations and incident patterns
- **Incident Response**: Apply proven remediation patterns from past incidents
- **Auto-fixes**: Use learned patterns for safe automated corrections
- **Runtime Monitoring**: Detect anomalies based on historical baselines
- **Innovation and Roadmap**: Feed user patterns and lessons into improvement proposals

### Memory Structure

```
memory/
├── schema/
│   └── memory-entry.json          # Memory entry schema
│
├── global/                         # Platform-wide foundational memories
│   ├── seed-build-philosophy-memory.json
│   ├── seed-governance-memory.json
│   ├── seed-architecture-memory.json
│   ├── seed-autonomy-memory.json
│   └── seed-runtime-agent-memory.json
│
├── foreman/                        # Build-time governance memories
│   ├── governance-events.json
│   └── build-events.json
│
└── platform/                       # Runtime platform memories
    └── runtime-events.json
```

### Privacy and Safety

Memory follows strict privacy rules:
- **NO tenant-specific data** 
- **NO user identifiable information**
- **ONLY aggregate, anonymized patterns**
- **Strict tenant isolation enforced**

Memory is version-controlled, auditable, and permanent.

## 🧱 Architectural Foundations

Maturion enforces alignment with:

- SRMF Master Build Reference (Master architecture)
- Integrated ISMS Architecture
- Module True North Documents
- Build Philosophy (One-Time Build, Zero Regression)
- Minimum Architecture Template (MARS)
- Versioning Rules
- QA Requirements
- QA-of-QA Requirements
- Compliance Mapping to ISO / NIST / COBIT / OWASP
- Platform Governance Standards
- Innovation Engine Rules

## 📁 Repository Structure

```
maturion-ai-foreman/
│
├── memory/                         # 🧠 Unified Memory Fabric (NEW)
│   ├── schema/
│   │   └── memory-entry.json
│   ├── global/
│   │   ├── seed-build-philosophy-memory.json
│   │   ├── seed-governance-memory.json
│   │   ├── seed-architecture-memory.json
│   │   ├── seed-autonomy-memory.json
│   │   └── seed-runtime-agent-memory.json
│   ├── foreman/
│   │   ├── governance-events.json
│   │   └── build-events.json
│   └── platform/
│       └── runtime-events.json
│
├── foreman/
│   ├── identity.md
│   ├── roles-and-duties.md
│   ├── memory-model.md
│   ├── privacy-guardrails.md
│   ├── command-grammar.md
│   ├── runtime-agent-plan.md
│   ├── builder-manifest.json
│   ├── system-map.md
│   ├── architecture-governance.md
│   ├── qa-governance.md
│   ├── qa-of-qa.md
│   ├── architecture-naming-conventions.md
│   ├── architecture-folder-structure.md
│   ├── versioning-rules.md
│   ├── minimum-architecture-template.md
│   ├── architecture-validation-checklist.md
│   ├── qa-minimum-coverage-requirements.md
│   ├── module-readiness-report-template.md
│   ├── task-distribution-rules.md
│   │
│   ├── platform/
│   │   ├── qa-dashboard-spec.md
│   │   ├── governance-qa-dashboard-spec.md
│   │   ├── watchdog-standard-spec.md
│   │   ├── privacy-leak-detection-spec.md
│   │   ├── security-escalation-policy.md
│   │   ├── ai-performance-metrics-spec.md
│   │   ├── ai-cost-optimization-policy.md
│   │   ├── ai-usage-analytics-spec.md
│   │   ├── ui-branding-standard.md
│   │   ├── ui-theme-overrides.md
│   │   ├── ui-navigation-spec.md
│   │   ├── image-generation-policy.md
│   │   ├── image-model-routing-spec.md
│   │   ├── ui-asset-generation-guidelines.md
│   │   ├── ui-multiwindow-spec.md
│   │   ├── ui-ai-edit-session-spec.md
│   │
│   ├── compliance/
│   │   ├── compliance-reference-map.md
│   │   ├── compliance-control-library.json
│   │   ├── compliance-qa-spec.md
│   │   ├── compliance-watchdog-spec.md
│   │   ├── compliance-dashboard-spec.md
│   │
│   ├── innovation/
│   │   ├── idea-submission-spec.md
│   │   ├── idea-summarisation-rules.md
│   │   ├── idea-voting-policy.md
│   │   ├── innovation-workflow-spec.md
│   │   ├── threshold-policy.md
│   │   ├── innovation-dashboard-spec.md
│   │   ├── roadmap-generation-spec.md
│   │
│   ├── surveys/
│   │   ├── survey-engine-spec.md
│   │   ├── survey-ai-analysis-spec.md
│   │
│   ├── admin/
│       ├── enhancement-parking-lot-spec.md
│       ├── admin-innovation-chat-spec.md
│       ├── ai-self-improvement-spec.md
│
└── .github/
    ├── copilot-instructions.md
    └── ISSUE_TEMPLATE/
```

## 🔍 What Maturion Governs

### 📘 Architecture

- All modules
- All requirements
- Data models
- Inter-module dependencies
- Integration specs
- Naming & folder standards
- MARS template
- Versioning rules

### 🟦 QA & QA-of-QA

- Test coverage
- Test execution
- Test category breakdown
- Architecture ↔ QA traceability
- Governance QA
- Compliance QA
- Performance QA

### 🔐 Compliance

Mapped to global international standards:

- ISO 27001
- ISO 27005
- ISO 31000
- NIST CSF
- COBIT
- GDPR & POPIA
- OWASP

### 🔥 Watchdogs

- Privacy leak detection
- Cross-tenant anomaly detection
- Security events
- Behavioural anomalies
- Compliance drift
- Performance degradation

### 🌟 Innovation Engine

- User idea submissions
- Maturion summaries
- Multi-tenant voting
- Threshold triggers (50/70/80/90/95%)
- Automated roadmap generation
- Architecture handoff to Foreman
- Builder sprint integration

### 📊 Surveys

- UX
- Feature requests
- Module performance
- Risk maturity
- AI helpfulness

### 🧠 Admin Tools

- AI editing session
- Enhancement parking lot
- Admin-level innovation chat
- AI performance and cost dashboards

## 🧩 Builder Agent Ecosystem

Builder agents implement code under Maturion's governance:

- UI Builder
- API Builder
- Schema Builder
- Integration Builder
- QA Builder

Every task is sequenced and validated by Maturion before execution.

All work must pass:

- QA
- QA-of-QA
- Integration checks
- Governance checks
- Your final approval

## 🛡️ Tenant Isolation and Security

See:

- `privacy-guardrails.md`
- `privacy-leak-detection-spec.md`
- `security-escalation-policy.md`
- `compliance-qa-spec.md`

Maturion enforces:

- Zero cross-tenant leakage
- Zero sensitive data exposure
- Zero unauthorised model usage
- Full compliance with POPIA, GDPR, ISO 27001

## 🤖 AI Behaviour, Safety, and Self-Improvement

Maturion is:

- Permanent
- Version-controlled
- Auditable
- Governed
- Non-self-modifying
- Human-approved
- Multi-tenant safe
- Architecture-aware
- Context-aware (time, user, tenant, module)

Self-improvement requires:

- Admin initiation
- AI Editing Session
- Approval
- PR generation
- Governance QA
- Merge

See:

- `ai-self-improvement-spec.md`
- `ui-ai-edit-session-spec.md`

## 🚀 Using Maturion

### Step 1 — Read identity

`foreman/identity.md`

### Step 2 — Learn command grammar

`foreman/command-grammar.md`

### Step 3 — Understand architecture guidelines

`foreman/minimum-architecture-template.md`

### Step 4 — Create module architecture

(Using the standard)

### Step 5 — Assign Foreman an issue

Foreman validates architecture → creates builder plan → triggers QA → begins build cycle.

## 🔍 Validation and Activation Scripts

### Repository Validation

Validate the entire repository structure, specifications, and governance:

```bash
python3 validate-repository.py
```

**Checks:**
- Folder structure completeness
- Specification files for all modules (Phase 1-5)
- Governance file completeness
- QA and QA-of-QA specifications
- Compliance reference map and control library
- Innovation, survey, and admin specifications
- Builder agent specifications
- JSON file integrity

### Compliance Engine Activation

Activate and validate the Compliance Engine:

```bash
python3 activate-compliance-engine.py
```

**Performs:**
- Loads all compliance governance files
- Validates compliance file structure and integrity
- Analyzes standards coverage
- Identifies missing mappings
- Calculates compliance coverage percentage
- Generates comprehensive readiness report

**Output:**
- `foreman/compliance-engine-readiness-report.md` - Detailed compliance status

**Reference:**
- `foreman/compliance-engine-initialization.md` - Compliance Engine operational framework

### Deprecation Detection Gate (BL-026)

Enforce modern Python patterns and prevent deprecated API usage:

```bash
# Check for deprecated APIs
ruff check --select UP .

# Auto-fix where possible
ruff check --select UP --fix .
```

**Enforces:**
- Modern datetime APIs (timezone-aware)
- PEP 585 type hints (built-in generics)
- Python 3.12+ compatibility
- Zero deprecated API usage

**Integrated Enforcement:**
- Pre-commit hook: `.githooks/pre-commit-deprecation`
- CI/CD gate: `.github/workflows/deprecation-detection-gate.yml`
- Ruff configuration: `ruff.toml`

**Policy:**
- `governance/policies/AUTOMATED_DEPRECATION_DETECTION_GATE.md` - Full policy and remediation guidance

**Audit:**
- `governance/evidence/BL_026_DEPRECATION_AUDIT_REPORT.md` - Current codebase status

**Authority:** BL-026 Bootstrap Learning, Zero Warning Test Debt Constitutional Rule

## 🔧 GitHub Copilot Integration

This repo supports Copilot issue assignment:

- Open any issue
- Click Assignee
- Select Copilot to propose a PR

Foreman supervises Copilot PRs using governance rules.

## 📊 ISMS Architecture Indexing

The repository includes a comprehensive architecture indexing system:

### Architecture Indexing Tool

```bash
python3 index-isms-architecture.py
```

**Generates:**
- `ARCHITECTURE_INDEX_REPORT.md` - Human-readable comprehensive report
- `ARCHITECTURE_INDEX.json` - Machine-readable structured index

**Features:**
- Complete module inventory (9 modules, 87+ architecture files)
- True North architecture index
- Module dependency mapping
- Compliance coverage tracking (11 international standards)
- Missing element identification
- Architectural inconsistency detection
- Architecture health scoring

**Use Cases:**
- Pre-build validation
- Compliance audits
- Dependency analysis
- Gap identification
- Architecture governance

See `ARCHITECTURE_INDEXING_README.md` for full documentation.

### Repository Validation Tool

```bash
python3 validate-repository.py
```

**Validates:**
- Governance structure
- Specification completeness
- QA coverage
- JSON file integrity
- Builder agent configurations

**Use Together:**
Both `validate-repository.py` and `index-isms-architecture.py` should be run as part of architectural governance to ensure complete validation and indexing.

### Foreman Self-Test & Readiness Verification

```bash
python3 foreman/scripts/run-self-test.py
```

**Validates:**
- Core governance system (8 files)
- Architecture system (8 files)
- Builder agent system (10 files)
- Compliance engine (5 files)
- QA & QA-of-QA system (6 files)
- Runtime & continuity system (12 files)
- Change management system (9 files)
- Upgrade & continuity system (4 files)
- Test environment system (4 files)
- Orchestration & build pipeline (6 files)
- Platform & UI standards (6 files)
- Innovation & admin intelligence (3 files)

**Generates:**
- `self-test-report.json` - Machine-readable test results
- `self-test-report.md` - Human-readable diagnostic report

**Features:**
- Validates 81+ critical files across 12 subsystems
- PASS/WARN/FAIL status with exit codes (0/1/2)
- Builder readiness detection
- Compliance coverage tracking
- Runtime system validation
- Change record tracking
- Privacy-compliant (no tenant data, no secrets)
- Supports chat reset recovery

**Command-Line Options:**
```bash
--verbose          # Detailed logging
--output-dir DIR   # Custom output directory
--json-only        # Generate JSON only (skip Markdown)
```

**Use Cases:**
- After chat resets (verify all systems intact)
- Before major builds (ensure readiness)
- After merges (validate no critical files lost)
- Post-deployment validation
- Periodic health checks
- Troubleshooting and diagnostics

**Exit Codes:**
- `0` = PASS - All systems healthy
- `1` = WARN - Some warnings, but functional
- `2` = FAIL - Critical systems missing/broken

# Agent Definitions (Canonical)

Canonical agent definitions live in this folder.

## Active
- `ForemanApp-agent.md` — the only valid FM definition for this repository

## Deprecated (Removed)
All legacy FM agent definitions are deprecated and must not be used.
Commit message:

docs: add canonical agent folder notice

See `foreman/self-test/SELF_TEST_QUICK_REFERENCE.md` for detailed usage guide.

## 🧠 Conclusion

Maturion is the permanent AI intelligence running the entire Maturion ISMS ecosystem.

He enforces your standards, evolves the platform, protects tenants, maintains compliance, orchestrates builders, and becomes your long-term second-in-command.
