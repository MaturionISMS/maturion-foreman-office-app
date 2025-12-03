# Maturion Foreman

**Maturion Foreman** is the governance, architecture enforcement, and AI orchestration hub for the Maturion Integrated Security Management System (ISMS) ecosystem.

## Purpose

**Maturion Foreman** is responsible for:

- **Governance & Enforcement**: Ensuring all modules adhere to architectural boundaries, QA standards, and build philosophy
- **Architecture Enforcement**: Validating module boundaries and preventing architectural drift
- **Quality Assurance**: Enforcing QA checklists, watchdog rules, and zero-regression principles
- **Rule Interpretation**: Interpreting and applying SRMF Master Build Reference and True North principles
- **AI Orchestration**: Managing builder agents and coordinating AI-driven development tasks
- **Watchdog Management**: Monitoring critical, high, medium, and low severity triggers across modules

## Core Principles

**Maturion Foreman** operates according to the Maturion Build Philosophy:

- **One-Time Build Correctness**: Build it right the first time
- **Zero Regression**: Never break what already works
- **Full Architectural Alignment**: All modules connect to the master reference
- **Zero Loss of Context**: Preserve all architectural decisions and rationale
- **Zero Ambiguity**: Clear, explicit governance rules

## Architectural Foundation

**Maturion Foreman** enforces alignment with:

- **[SRMF Master Build Reference](SRMF_MASTER_BUILD_REFERENCE_v1.0.md)**: Single source of truth for the ISMS ecosystem
- **[Integrated ISMS Architecture](Integrated_ISMS_Architecture_v1.1.md)**: High-level system architecture and module integration
- **Module True North Documents**: Each module's architectural vision and principles
- **Build Philosophy**: One-time correctness and zero-regression methodology

## System Structure

```
maturion-ai-foreman/
├── foreman/                       # Foreman system files
│   ├── identity.md               # Foreman identity and responsibilities
│   ├── command-grammar.md        # Instruction format specifications
│   ├── builder-manifest.json     # Builder agent registry
│   └── system-map.md             # Monorepo structure and boundaries
├── .github/
│   ├── copilot-instructions.md   # Repository-specific Copilot instructions
│   └── ISSUE_TEMPLATE/           # Issue templates
└── [Architecture Files]          # ISMS module specifications
```

## Key Modules Governed

**Maturion Foreman** oversees the following modules:

- **Course Crafter**: E1-E4 content factory for training and awareness
- **ERM (Enterprise Risk Management)**: Risk matrices, scales, and heatmaps
- **PIT (Project & Issues Tracker)**: Project tracking with watchdog and AI routing
- **Risk Assessment**: Assessment workflows and methodologies
- **Threat Module**: Threat intelligence with watchdog and AI routing
- **Vulnerability Module**: Vulnerability tracking with watchdog and AI routing
- **WRAC (Workplace Risk Assessment & Control)**: Workplace safety controls

## GitHub Copilot Integration

This repository is configured to work with GitHub Copilot for issue management and AI-assisted development.

### Assigning Issues to Copilot

1. Open an issue or create a new one
2. On the right sidebar, look for the "Assignees" section
3. Click on "Assign to Copilot" (or search for "copilot" in the assignees dropdown)
4. GitHub Copilot will analyze the issue and create pull requests with proposed solutions

### Copilot Instructions

Repository-specific instructions for GitHub Copilot can be found in [`.github/copilot-instructions.md`](.github/copilot-instructions.md).

## Getting Started

1. **Review the Foreman Identity**: See [`foreman/identity.md`](foreman/identity.md) to understand Maturion Foreman's role and authority
2. **Understand Command Grammar**: See [`foreman/command-grammar.md`](foreman/command-grammar.md) for instruction formats
3. **Explore Builder Agents**: See [`foreman/builder-manifest.json`](foreman/builder-manifest.json) for agent responsibilities
4. **Review System Map**: See [`foreman/system-map.md`](foreman/system-map.md) for module boundaries and ownership

## Documentation

- [`foreman/identity.md`](foreman/identity.md) - Maturion Foreman identity and responsibilities
- [`foreman/command-grammar.md`](foreman/command-grammar.md) - Command and instruction formats
- [`foreman/builder-manifest.json`](foreman/builder-manifest.json) - Builder agent registry
- [`foreman/system-map.md`](foreman/system-map.md) - System structure and module boundaries
- [SRMF Master Build Reference](SRMF_MASTER_BUILD_REFERENCE_v1.0.md) - Master reference document
- [Integrated ISMS Architecture](Integrated_ISMS_Architecture_v1.1.md) - System architecture

## Contributing

When contributing to this repository:

1. Ensure changes align with the SRMF Master Build Reference
2. Follow the One-Time Build + Zero Regression philosophy
3. Update relevant governance configs when adding new modules
4. Consult Maturion Foreman (via issue assignment) for architectural questions

---

**Maturion Foreman** - Governance, Enforcement, and Orchestration for the Maturion ISMS Ecosystem
