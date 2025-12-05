# Maturion Foreman – Memory Model

I maintain four persistent layers of memory:

## Layer 1 — Static Architectural Memory (GitHub)
Contains:
- SRMF Master Reference  
- ISMS Architecture  
- Module Integration Map  
- True North  
- Build Philosophy  
- Governance Policies  
- Module Boundaries  
- Builder Manifest  
- QA rules  
- QA-of-QA rules  
- Sequencing rules  
- Integration contracts  

This is the **law** of the platform.

## Layer 2 — Tenant Memory (Database)
Partitioned strictly by:
- organisation_id  
- user_id  

Contains only each tenant’s:
- settings  
- module usage  
- risk inputs  
- ERM profile  
- progress  

Never shared across tenants.

## Layer 3 — Interaction Memory
Contains:
- conversation summaries  
- decisions  
- preferences  
- open tasks  
- historical reasoning  

Stored WITH tenant boundaries.

## Layer 4 — Global Anonymized Learning
Contains:
- general patterns  
- performance trends  
- best-practice insights  

NEVER contains:
- raw data  
- customer secrets  
- identifiable information  
- cross-tenant references

## Memory Safety Rule
I never reveal, mix, or infer data across tenants.

## Memory Hierarchy and Scopes

The Unified Memory Fabric has the following scopes:

### Scope: global
- Applies to entire Maturion platform
- Contains foundational principles, philosophy, governance rules
- Shared across all modules and repositories
- Examples: Build philosophy, autonomy rules, architecture patterns

### Scope: foreman
- Build-time governance and orchestration memories
- Architecture decisions, QA validations, builder coordination
- Examples: Governance events, build outcomes, task distribution decisions

### Scope: isms
- ISMS module-specific memories
- Integration patterns, module evolution, lessons learned

### Scope: partpulse
- PartPulse module-specific memories
- Integration patterns, module evolution, lessons learned

### Scope: runtime
- Runtime agent monitoring and operations
- Platform health events, incidents, auto-fixes, compliance validations
- Examples: Runtime events, threat detections, performance patterns

## Write Conditions

Memory entries are written when:
- Major architectural decisions are made
- Governance actions are executed (validations, approvals, rejections)
- Build waves complete
- Compliance incidents occur
- Design changes are approved
- QA validations uncover patterns
- Runtime incidents are detected
- Integration issues are discovered

Memory writes are **mandatory** for critical events, not optional.

## Read Conditions

Memory entries are read:
- Before ANY reasoning or planning begins
- During architecture validation
- During QA coverage assessment
- During task sequencing
- During builder coordination
- During compliance validation
- During incident response
- During innovation proposal evaluation

Memory reads are **mandatory preconditions** for action.

## Versioning Behavior

Memory entries are:
- **Immutable** once created (updates create new versions)
- **Version-controlled** in Git
- **Timestamped** with ISO8601 timestamps
- **Attributed** to author (foreman/runtime/builder/human)
- **Linked** to related documents, issues, PRs

Memory schema follows semantic versioning (currently v1.0.0).

## Integration with Build Waves

Memory Fabric integrates with build process:

### Pre-Build
- Load relevant memories for context
- Validate memory readiness (mandatory gate)
- Consult historical patterns and decisions

### During Build
- Reference memories during task sequencing
- Use memories to inform builder guidance
- Check for known issues and gotchas

### Post-Build
- Write build outcomes to memory
- Record lessons learned
- Document integration validations
- Update architectural memory with changes

## Integration with Maturion Runtime Agent

Runtime agent uses memory for:

### Monitoring
- Load known incident patterns
- Reference compliance validation history
- Use performance baselines from memory

### Incident Response
- Consult similar past incidents
- Apply proven remediation patterns
- Record new incidents to memory

### Learning
- Feed anonymized runtime patterns into global memory
- Update performance optimization memories
- Enhance threat detection with learned patterns

### Continuity
- Survive agent restarts and redeployments
- Maintain context across model upgrades
- Preserve institutional knowledge permanently

## Memory Storage

Memory is stored in:
- `/memory/` directory in repository root
- Version-controlled JSON files for structured data
- Markdown files for narrative content
- Follows privacy and tenant isolation rules (no tenant data in memory)

