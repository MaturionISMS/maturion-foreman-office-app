# Builder Agent Registry - Quick Reference

## Current Status

✓ **All builder agents initialized and validated successfully**

## Registered Builders

| Builder | Responsibilities | Capabilities | Write Access |
|---------|-----------------|--------------|--------------|
| **ui-builder** | UI components, layouts, wizards | ui, frontend, components, styling | apps/*/frontend/* |
| **api-builder** | API endpoints, handlers | api, backend, logic, routes | apps/*/backend/* |
| **schema-builder** | Database schemas, models | schema, models, migrations | apps/*/data/* |
| **integration-builder** | Module integrations | integration, inter-module, events | apps/*/integration/* |
| **qa-builder** | QA tests, coverage | testing, coverage, qa-of-qa | apps/*/qa/* |

## Quick Commands

### Initialize & Validate
```bash
python3 foreman/init_builders.py
```

### Run Tests
```bash
python3 foreman/test-init-builders.py
```

### View Report
```bash
cat foreman/builder-registry-report.md
```

## Validation Checklist

- [x] builder-manifest.json loaded successfully
- [x] builder-capability-map.json loaded successfully
- [x] builder-permission-policy.json loaded successfully
- [x] All 5 builder specification files discovered
- [x] Spec file exists for each manifest agent
- [x] No orphaned spec files
- [x] Capability definitions aligned with manifest
- [x] Permission policies aligned with manifest
- [x] All agents have responsibilities defined
- [x] All agents have forbidden actions defined

## Configuration Files

### 1. foreman/builder-manifest.json
Defines agents, responsibilities, and forbidden actions

### 2. foreman/builder/builder-capability-map.json
Maps agents to their capabilities

### 3. foreman/builder/builder-permission-policy.json
Defines read/write permissions for each agent

### 4. foreman/builder/*-builder-spec.md
Detailed specification for each builder agent

## Adding a New Builder

1. Update `builder-manifest.json`
2. Update `builder-capability-map.json`
3. Update `builder-permission-policy.json`
4. Create `foreman/builder/new-builder-spec.md`
5. Run: `python3 foreman/init_builders.py`
6. Verify: No errors in the report

## Common Issues

| Issue | Solution |
|-------|----------|
| Missing spec file | Create `foreman/builder/{agent}-spec.md` |
| Capability misalignment | Add agent to `builder-capability-map.json` |
| Permission misalignment | Add agent to `builder-permission-policy.json` |
| Invalid JSON | Validate JSON syntax in config files |

## Test Coverage

✓ Valid configuration
✓ Missing files detection
✓ Missing specifications detection
✓ Capability alignment validation
✓ Permission alignment validation
✓ Invalid JSON handling
✓ Orphaned spec detection

**All 16 tests passing**

## Integration Points

- **Task Distribution**: Uses validated builder registry
- **Permission Enforcement**: File access controlled per builder
- **Capability Routing**: Tasks assigned based on capabilities
- **QA Validation**: QA builder validates all builder outputs

## References

- Full Documentation: `foreman/BUILDER_INITIALIZATION.md`
- Builder Identity: `foreman/identity.md`
- Command Grammar: `foreman/command-grammar.md`
- Collaboration Rules: `foreman/builder/builder-collaboration-rules.md`
- Master Architecture: `SRMF_MASTER_BUILD_REFERENCE_v1.0.md`

---

*Last Updated: 2025-12-03*
*Registry Version: 1.0*
*Total Builders: 5*
