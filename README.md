# Maturion AI Foreman

The Foreman repository serves as the central governance, quality assurance, and orchestration hub for the Maturion ISMS ecosystem. It contains all architecture enforcement rules, QA requirements, watchdog logic, and AI task routing configurations.

## Purpose

Foreman supervises the entire Maturion ISMS ecosystem by:
- **Enforcing Architecture Boundaries**: Maps SRMF modules to monorepo paths and ensures ownership per module
- **Quality Assurance**: Validates changes against governance requirements and quality checklists
- **AI Task Routing**: Manages types 1–6 AI tasks with appropriate restrictions
- **Watchdog Monitoring**: Triggers alerts based on critical, high, medium, and low severity events

## Structure

```
/foreman
  /config              - Configuration files for governance and routing
  /scripts             - Automation and validation scripts
  /docs                - Documentation and principles
```

## Usage

Run Foreman checks to validate repository changes:

```bash
npm run foreman:check
```

## Configuration Files

- `architecture-map.json` - Maps SRMF modules to monorepo paths
- `module-boundaries.json` - Enforces ownership per module
- `qa-checklist.json` - Quality and governance requirements
- `ai-routing-rules.json` - AI task types 1–6 with restrictions
- `watchdog-rules.json` - Alert triggers by severity level

## Documentation

- `true-north.md` - Organizational True North principles
- `build-philosophy.md` - One-Time Build + Zero Regression philosophy
