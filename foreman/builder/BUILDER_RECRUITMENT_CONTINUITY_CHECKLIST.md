# Builder Recruitment Continuity Checklist

**Purpose**: Verify canonical builder recruitment continuity across build waves  
**Authority**: FM Agent Contract Section 6E — Builder Recruitment Continuity  
**Applies To**: Wave 1.0+ (re-entry after Wave 0 canonical recruitment)

---

## I. Recruitment vs Appointment Distinction

### Definitions

**Recruitment**: One-time canonical registration of builders into the Maturion system
- Occurs in Wave 0.1
- CS2-approved
- Persists across all waves
- Cannot be undone without explicit revocation

**Appointment**: Assignment of recruited builders to specific tasks
- Occurs in Wave 1.0+
- Task-specific
- Does not re-gate recruitment
- Assumes recruitment already complete

---

## II. Mandatory Verification (Before Wave Re-Entry)

Before FM proceeds with Wave 1.0+ planning or builder task assignment, FM MUST verify:

### ✅ 1. Builder Recruitment Artifacts Exist

| Artifact | Location | Status | Notes |
|----------|----------|--------|-------|
| Builder Manifest | `foreman/builder-manifest.json` | [ ] Verified | Defines all builder agents |
| Builder Specifications | `foreman/builder/*-builder-spec.md` | [ ] Verified | 5 specs required (ui, api, schema, integration, qa) |
| Builder Capability Map | `foreman/builder/builder-capability-map.json` | [ ] Verified | Maps agent capabilities |
| Builder Permission Policy | `foreman/builder/builder-permission-policy.json` | [ ] Verified | Defines access permissions |
| Builder Registry Report | `foreman/builder-registry-report.md` | [ ] Verified | Validation report |

**Verification Command**:
```bash
python3 foreman/init_builders.py
```

**Expected Result**: All 5 builder agents registered with 0 errors, 0 warnings

---

### ✅ 2. Builder Recruitment Approval Status

| Builder | Recruited in Wave 0.1 | CS2 Approved | Canonical Status |
|---------|----------------------|--------------|------------------|
| ui-builder | [ ] Yes | [ ] Yes | [ ] Active |
| api-builder | [ ] Yes | [ ] Yes | [ ] Active |
| schema-builder | [ ] Yes | [ ] Yes | [ ] Active |
| integration-builder | [ ] Yes | [ ] Yes | [ ] Active |
| qa-builder | [ ] Yes | [ ] Yes | [ ] Active |

**Evidence Location**: 
- Wave 0 recruitment: `foreman/BUILDER_INITIALIZATION.md`
- Registry report: `foreman/builder-registry-report.md`

---

### ✅ 3. No Re-Recruitment Gates Invented

FM MUST confirm:
- [ ] No "pending appointment" state invented for recruited builders
- [ ] No new recruitment gates added beyond BUILD_PHILOSOPHY.md sequencing
- [ ] No re-execution of Wave 0 recruitment process
- [ ] Builders treated as active and eligible for appointment

---

### ✅ 4. Continuity from Prior Waves

FM MUST acknowledge:
- [ ] Builder recruitment is one-time (Wave 0.1)
- [ ] Recruitment remains valid unless explicitly revoked
- [ ] Wave 1.0+ uses appointment, not recruitment
- [ ] No governance gap exists between recruitment and appointment

---

### ✅ 5. Ripple Intelligence Alignment

FM MUST confirm:
- [ ] Governance canon version is known and documented
- [ ] Last canonical sync status is verified (ALIGNED status required)
- [ ] Builder agent contracts (.agent files) reflect current Ripple Intelligence obligations
- [ ] All canonical_authorities in builder contracts are current
- [ ] No governance ripple (downward) is in progress
- [ ] No ripple ambiguity or conflict exists
- [ ] Ripple alignment confirmation can be provided for each builder appointment

**Verification Command**:
```bash
# Check canonical sync status
cat governance/alignment/canonical_sync_status.json

# Verify builder contract versions
for builder in ui api schema integration qa; do
  echo "Checking ${builder}-builder..."
  grep "maturion_doctrine_version\|canonical_authorities" .github/agents/${builder}-builder.md
done
```

**Expected Result**: 
- Sync status = "ALIGNED"
- All builder contracts reference current BUILD_PHILOSOPHY.md version
- All canonical_authorities exist and are current

---

## III. Hard Stop Conditions

FM MUST STOP and escalate if:

| Condition | Action |
|-----------|--------|
| Builder recruitment artifacts missing or incomplete | STOP → Escalate to CS2 |
| Builder specifications not found | STOP → Escalate to CS2 |
| Builder registry report shows errors | STOP → Fix errors → Re-run validation |
| Builders not canonically recruited | STOP → Execute Wave 0 recruitment (exceptional case) |
| FM attempts to re-recruit already-recruited builders | STOP → Self-correct → Acknowledge existing recruitment |
| **Ripple alignment cannot be confirmed** | **STOP → Execute governance sync → Re-verify → Escalate if persistent** |
| **Governance ripple in progress** | **STOP → Wait for ripple completion → Re-verify** |
| **Ripple conflict detected** | **STOP → Escalate to Johan immediately** |

---

## IV. Wave Re-Entry Authorization

FM MAY proceed with Wave 1.0+ execution ONLY when:

- ✅ All builder recruitment artifacts verified
- ✅ All 5 builders confirmed as canonically recruited
- ✅ Builder recruitment continuity acknowledged
- ✅ No re-recruitment gates invented
- ✅ **Ripple Intelligence Alignment confirmed for all builders**
- ✅ **Governance canon version documented**
- ✅ **No ripple ambiguity or conflict exists**
- ✅ FM ready to proceed with builder appointment (not recruitment)

**Authorization Statement**:
```
Builder recruitment continuity verified.
All 5 builders (ui-builder, api-builder, schema-builder, integration-builder, qa-builder)
are canonically recruited, CS2-approved, and active.

Ripple Intelligence Alignment confirmed.
Governance canon version: <version>
Last canonical sync: <date>
Ripple status: STABLE
All builder contracts are governance-current.

FM authorized to proceed with builder appointment for Wave 1.0+ tasks.
```

---

## V. Post-Verification Actions

After successful verification:

1. **Document Continuity**
   - Update wave planning documents to reflect builder status: "recruited and active"
   - Avoid language implying pending recruitment or approval

2. **Proceed with Appointment**
   - Assign recruited builders to specific tasks
   - Use BUILD_PHILOSOPHY.md sequencing (Architecture → QA-to-Red → Build-to-Green)
   - Do NOT re-gate or re-validate recruitment

3. **Maintain Evidence Trail**
   - Record verification completion in wave planning documents
   - Link to this checklist in Platform Readiness Evidence

---

## VI. References

- FM Agent Contract Section 6E: Builder Recruitment Continuity
- BUILD_PHILOSOPHY.md: Sacred Workflow (Architecture → QA-to-Red → Build-to-Green)
- foreman/BUILDER_INITIALIZATION.md: Builder initialization and validation
- foreman/builder-registry-report.md: Current builder status

---

**Checklist Version**: 1.0  
**Effective Date**: 2025-12-30  
**Authority**: FM Agent Contract (Section 6E)  
**Enforcement**: Mandatory before Wave 1.0+ re-entry

---

*END OF BUILDER RECRUITMENT CONTINUITY CHECKLIST*
