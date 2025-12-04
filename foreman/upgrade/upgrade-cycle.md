# Upgrade Cycle

## Purpose

Define a full upgrade cycle: when Maturion returns control to Foreman, how new versions are prepared, and how handback is done.

---

## 1. Upgrade Triggers

An upgrade cycle may be triggered by:

1. **Scheduled Release**
   - Regular planned upgrades (e.g., quarterly)
   - New module completions
   - Major architecture improvements

2. **Incident-Driven**
   - Critical security vulnerability
   - Critical compliance gap
   - Platform stability issue

3. **Insight-Driven**
   - Accumulated runtime lessons reach threshold
   - User feedback indicates major improvement opportunity
   - Performance optimization potential identified

4. **Human-Initiated**
   - Admin decision for strategic reasons
   - Compliance deadline
   - Business requirement

---

## 2. Upgrade Phases

### Phase 1: Runtime Knowledge Export
- Maturion exports runtime state per `runtime-export-spec.md`
- Behaviour events, incidents, lessons aggregated
- Performance metrics and drift signals compiled

### Phase 2: Foreman Re-initialization
- Foreman imports runtime knowledge per `foreman-import-spec.md`
- Foreman updates governance context
- Foreman prioritizes improvement tasks

### Phase 3: Build Preparation
- Architecture updates planned
- QA and compliance requirements updated
- Builder tasks sequenced

### Phase 4: Build Execution
- Builders implement changes
- QA validation in test environment
- Compliance checks

### Phase 5: Production Deployment
- Test environment sign-off
- Production deployment per change management policy
- Maturion reinitialized with new version

### Phase 6: Post-Deployment Validation
- Runtime monitoring confirms stability
- No critical incidents in first 48 hours
- Performance within expected bounds

---

## 3. Upgrade Criteria

Before an upgrade is approved:

- [ ] All critical incidents from previous version resolved or understood
- [ ] All new changes have passed test environment validation
- [ ] Rollback plan exists and tested
- [ ] Human admin approval obtained
- [ ] Compliance validation passed

---

## 4. Version Tracking

Each upgrade cycle:

- Increments version number
- Updates `OPERATIONAL_STATUS_REPORT.md`
- Records in change log
- Links to runtime insights that triggered upgrade
