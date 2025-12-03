# Builder Agent Initialization

## Overview

The Maturion Foreman uses a builder agent registry system to manage and validate all builder agents in the ISMS ecosystem. This document describes the initialization process and validation requirements.

## Builder Agents

The following builder agents are registered in the Maturion ecosystem:

1. **ui-builder** - Frontend UI components and layouts
2. **api-builder** - Backend API endpoints and business logic
3. **schema-builder** - Database schemas and data models
4. **integration-builder** - Cross-module integrations
5. **qa-builder** - Quality assurance tests and coverage

## Configuration Files

### 1. builder-manifest.json

Located at: `foreman/builder-manifest.json`

Defines all builder agents, their responsibilities, and forbidden actions.

**Structure:**
```json
{
  "version": "1.0",
  "agents": {
    "agent-name": {
      "responsibilities": ["list of responsibilities"],
      "forbidden": ["list of forbidden actions"]
    }
  }
}
```

### 2. builder-capability-map.json

Located at: `foreman/builder/builder-capability-map.json`

Maps each builder to their specific capabilities.

**Structure:**
```json
{
  "version": "1.0",
  "capabilities": {
    "agent-name": ["capability1", "capability2", ...]
  }
}
```

### 3. builder-permission-policy.json

Located at: `foreman/builder/builder-permission-policy.json`

Defines file system access permissions for each builder.

**Structure:**
```json
{
  "builders": {
    "agent-name": {
      "write": ["path/pattern/*"],
      "read": ["path/pattern/*"]
    }
  }
}
```

### 4. Builder Specifications

Located at: `foreman/builder/*-builder-spec.md`

Each builder agent must have a corresponding specification file that documents:
- Purpose
- Responsibilities
- Required Inputs from Foreman
- Outputs
- Forbidden Actions
- PR Requirements

## Initialization Process

### Running the Initialization

```bash
python3 foreman/init-builders.py
```

### Validation Checks

The initialization script performs the following validations:

1. **Configuration Loading**
   - Loads builder-manifest.json
   - Loads builder-capability-map.json
   - Loads builder-permission-policy.json
   - Validates JSON structure

2. **Specification Discovery**
   - Discovers all *-builder-spec.md files
   - Validates spec file naming conventions

3. **Manifest Structure Validation**
   - Checks for version field
   - Validates agents section exists
   - Ensures each agent has responsibilities
   - Ensures each agent has forbidden actions

4. **Specification Alignment**
   - Verifies each manifest agent has a spec file
   - Checks for orphaned spec files

5. **Capability Alignment**
   - Ensures each manifest agent has capabilities defined
   - Checks for orphaned capability definitions
   - Validates capability definitions are non-empty

6. **Permission Alignment**
   - Ensures each manifest agent has permissions defined
   - Checks for orphaned permission policies
   - Validates read/write access patterns

### Output

The script generates:

1. **Console Output** - Real-time validation results
2. **builder-registry-report.md** - Comprehensive validation report

The report includes:
- Summary of registered agents
- Detailed agent configurations
- All validation results
- Warnings (if any)
- Errors (if any)
- Final status

### Exit Codes

- `0` - Success: All validations passed
- `1` - Failure: One or more errors detected

## Adding a New Builder Agent

To add a new builder agent to the registry:

1. **Update builder-manifest.json**
   ```json
   "new-builder": {
     "responsibilities": ["task1", "task2"],
     "forbidden": ["action1", "action2"]
   }
   ```

2. **Update builder-capability-map.json**
   ```json
   "new-builder": ["capability1", "capability2"]
   ```

3. **Update builder-permission-policy.json**
   ```json
   "new-builder": {
     "write": ["apps/*/newarea/*"],
     "read": ["foreman/*"]
   }
   ```

4. **Create Specification File**
   Create `foreman/builder/new-builder-spec.md` with:
   - Purpose
   - Responsibilities
   - Required Inputs
   - Outputs
   - Forbidden Actions
   - PR Requirements

5. **Run Initialization**
   ```bash
   python3 foreman/init-builders.py
   ```

6. **Verify Report**
   Check that the new builder appears in the report with no errors

## Troubleshooting

### Common Errors

**"Missing spec file for agent 'agent-name'"**
- Create the missing spec file: `foreman/builder/agent-name-spec.md`

**"Agent 'agent-name' in manifest has no capability definition"**
- Add the agent to `builder-capability-map.json`

**"Agent 'agent-name' in manifest has no permission policy"**
- Add the agent to `builder-permission-policy.json`

**"Invalid JSON in builder-manifest.json"**
- Validate JSON syntax using a JSON validator
- Check for trailing commas, missing quotes, etc.

### Common Warnings

**"Spec file found for 'agent-name' but not in manifest"**
- Either add the agent to manifest or remove the orphaned spec file

**"Capability defined for 'agent-name' but not in manifest"**
- Either add the agent to manifest or remove from capability map

**"Permission defined for 'agent-name' but not in manifest"**
- Either add the agent to manifest or remove from permission policy

## Governance

The builder registry is governed by Maturion Foreman and follows these principles:

1. **Complete Alignment** - All configuration files must be synchronized
2. **Zero Ambiguity** - Every builder must have clear responsibilities and boundaries
3. **Full Documentation** - Every builder must have a complete specification
4. **Explicit Permissions** - File access must be explicitly defined
5. **Capability Clarity** - Builder capabilities must be clearly mapped

Any changes to the builder registry must:
- Pass all validation checks
- Be reviewed by Foreman
- Include updated documentation
- Maintain backward compatibility where possible

## Integration with Builder Workflow

The initialization process is the first step in the builder workflow:

1. **Initialization** (this process)
   - Validate all builder configurations
   - Generate registry report

2. **Task Distribution** (foreman/task-distribution-rules.md)
   - Foreman assigns tasks to builders
   - Tasks are sequenced according to dependencies

3. **Builder Execution**
   - Builders execute within their defined permissions
   - Output is validated against specifications

4. **QA & Review**
   - QA Builder runs tests
   - Foreman performs QA-of-QA
   - Human validation (final approval)

## References

- `foreman/identity.md` - Maturion Foreman identity and authority
- `foreman/command-grammar.md` - Command syntax for builder tasks
- `foreman/builder/builder-collaboration-rules.md` - Inter-builder coordination
- `foreman/task-distribution-rules.md` - Task sequencing and distribution
- `SRMF_MASTER_BUILD_REFERENCE_v1.0.md` - Master architecture reference
