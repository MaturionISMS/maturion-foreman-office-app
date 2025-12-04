# Foreman Reinitialization

## Purpose

Define how Foreman re-enters active build mode with knowledge from the previous runtime phase.

---

## 1. Reinitialization Triggers

Foreman reinitializes when:

1. **Runtime Handback Received**
   - Maturion transfers control per `maturion-runtime-handback.md`

2. **New Version Needed**
   - Based on upgrade insights
   - Based on human admin decision

3. **Post-Incident Response**
   - After critical incident requiring architecture changes

---

## 2. Reinitialization Phases

### Phase 1: Knowledge Import

1. **Load Runtime Export**
   - Import runtime state per `foreman/upgrade/foreman-import-spec.md`
   - Validate export completeness
   - Validate privacy compliance

2. **Integrate Lessons**
   - Update `foreman/ai-memory/architectural-lessons.md`
   - Update `foreman/ai-memory/historical-issues-schema.json`
   - Update reasoning patterns

3. **Refresh Context**
   - Reload all governance documents
   - Reload architecture index
   - Reload compliance mappings
   - Reload QA frameworks

### Phase 2: Assessment

1. **Analyze Runtime Insights**
   - Review all incidents and their patterns
   - Identify recurring issues
   - Assess compliance posture changes
   - Review performance trends

2. **Identify Improvement Opportunities**
   - What can be fixed in architecture?
   - What can be improved in QA?
   - What new features are needed?
   - What technical debt should be addressed?

3. **Prioritize Tasks**
   - Critical security/compliance issues first
   - High-impact performance issues second
   - Feature requests by business value
   - Technical debt by risk reduction

### Phase 3: Planning

1. **Generate Builder Tasks**
   - Create tasks for each identified improvement
   - Sequence tasks per `task-distribution-rules.md`
   - Assign to appropriate builder agents
   - Define success criteria and QA requirements

2. **Update Governance**
   - Update architecture specs if needed
   - Update QA requirements based on lessons
   - Update compliance mappings
   - Update builder guidance

3. **Create Upgrade Plan**
   - Define version increment (major/minor/patch)
   - Define rollout strategy
   - Define rollback plan
   - Define success metrics

### Phase 4: Activation

1. **Validate Readiness**
   - All governance documents current
   - All builder specs updated
   - All tasks properly sequenced
   - All dependencies resolved

2. **Activate Builders**
   - Initialize builder agents
   - Distribute tasks
   - Begin build cycle

3. **Monitor Progress**
   - Track builder progress
   - Validate outputs against governance
   - Conduct QA-of-QA reviews
   - Ensure One-Time Build correctness

---

## 3. Reinitialization Checklist

- [ ] Runtime export imported successfully
- [ ] Privacy validation passed
- [ ] Architectural lessons updated
- [ ] Historical issues integrated
- [ ] Governance context refreshed
- [ ] Architecture index current
- [ ] Improvement opportunities identified
- [ ] Tasks generated and sequenced
- [ ] Builder agents ready
- [ ] Upgrade plan documented
- [ ] Human admin briefed

---

## 4. Special Cases

### 4.1 Emergency Reinitialization

For critical fixes:
- Streamlined import process
- Focus only on critical issue
- Fast-track builder tasks
- Expedited QA cycle
- Immediate deployment path

### 4.2 Major Version Upgrade

For significant platform changes:
- Extended assessment phase
- Comprehensive architecture review
- Full regression testing required
- Staged rollout plan
- Extended monitoring period

---

## 5. Success Criteria

Reinitialization is successful when:

- [ ] Foreman has full context from runtime
- [ ] All critical issues have corresponding tasks
- [ ] Builder agents are operational
- [ ] Upgrade plan is approved
- [ ] QA frameworks are ready
- [ ] Compliance validation is prepared
