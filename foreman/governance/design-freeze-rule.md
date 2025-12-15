# Design Freeze Rule

**Version**: 1.0.0  
**Status**: Constitutional Governance Rule  
**Authority**: Build Philosophy + Governance Supremacy Rule  
**Last Updated**: 2025-12-15

---

## I. Principle

**Once "Build to Green" is issued, architecture and QA are FROZEN and cannot be modified until build completes successfully or is explicitly aborted.**

This rule ensures **One-Time Build Correctness** and **Zero Regression** by preventing moving targets during implementation.

---

## II. Authority and Precedence

This rule derives from:
- **Build Philosophy** - Principle #1 (One-Time Build Correctness)
- **Governance Supremacy Rule** - Architecture conformance is required
- **Build to Green Rule** - Architecture must be complete before building

**Hierarchy**:
```
BUILD_PHILOSOPHY.md (Supreme Authority)
    ↓
Governance Supremacy Rule
    ↓
Design Freeze Rule (This Document)
    ↓
Applied to: Foreman, Builders, Human Operators
```

---

## III. Freeze Scope

### What is Frozen

When Design Freeze is active:

**Architecture**:
- All architecture documents
- All component specifications
- All integration specifications
- All data models
- All business rules
- All validation rules
- All user workflows

**QA**:
- All test suites
- All test cases
- All test assertions
- All test data
- All acceptance criteria
- All coverage requirements

### What is NOT Frozen

Design Freeze does NOT prevent:

- **Builder implementation code** - Builders write code to satisfy tests
- **Evidence documentation** - Build evidence continues to be created
- **Memory updates** - Memory continues to be written
- **Build tooling** - Build scripts, linters, etc. can be modified
- **Documentation fixes** - Typos in docs (not architecture/QA) can be fixed
- **Test infrastructure improvements** - Test utilities, helpers (not tests themselves)

---

## IV. Freeze Trigger

### When Freeze Activates

Design Freeze activates at the moment "Build to Green" instruction is issued by Foreman.

**Specifically**:
1. Foreman completes architecture design and validation
2. Foreman completes QA design and validation (RED status)
3. Foreman issues "Build to Green" instruction to builder
4. **→ Design Freeze ACTIVATES immediately**

### Activation Checklist

Before activating freeze, Foreman must verify:

- [ ] Architecture validated via Architecture Design Checklist (100% complete)
- [ ] QA validated via QA-of-QA (100% coverage, RED status, zero debt)
- [ ] No "TBD" or "TODO" in architecture
- [ ] No ambiguous requirements
- [ ] Build-to-Green instruction prepared
- [ ] Builder identified and ready

**If ANY item not checked → Do NOT activate freeze → Complete remaining work first**

### Activation Recording

Record freeze activation:

```json
{
  "scope": "foreman",
  "key": "design-freeze-<task-id>",
  "status": "ACTIVE",
  "task_id": "<task-id>",
  "architecture_path": "<path-to-architecture>",
  "qa_path": "<path-to-qa-suite>",
  "builder": "<builder-type>",
  "activated_by": "Maturion Foreman",
  "timestamp": "<ISO 8601>"
}
```

---

## V. Who is Bound by Freeze

### Foreman (Maturion Foreman)

**MUST NOT**:
- Modify architecture documents
- Modify QA test suites
- Add new requirements
- Change acceptance criteria
- Revise specifications

**MAY**:
- Monitor builder progress
- Respond to escalations
- Provide clarifications (without modifying docs)
- Create evidence documentation
- Update memory

**Exception**: If fundamental issue discovered requiring architecture/QA change → ABORT build, modify, re-validate, re-issue

### Builders (All Builder Agents)

**MUST NOT**:
- Modify architecture documents
- Modify QA test suites
- Add tests beyond what exists
- Skip or disable existing tests
- Change acceptance criteria
- Interpret requirements beyond what's written

**MUST**:
- Implement code to make existing tests pass
- Follow architecture exactly as written
- Request clarification if architecture unclear (via escalation)
- Report if architecture and QA conflict (via escalation)

**Exception**: None - Builders have NO authority to modify architecture/QA

### Human Operators

**MUST NOT**:
- Edit architecture files during build
- Edit QA test files during build
- Add new requirements mid-build
- Change acceptance criteria mid-build

**MAY**:
- Monitor build progress
- Provide guidance to Foreman when requested
- Approve escalations requiring owner authority

**Exception**: Owner (Johan) may override for critical situations (see Section VIII)

---

## VI. Freeze Duration

### Normal Duration

Design Freeze remains ACTIVE from:
- **Start**: "Build to Green" instruction issued
- **End**: Build completes successfully OR build is aborted

**Typical Duration**: Hours to days, depending on build complexity

### Monitoring Freeze Duration

Track freeze duration:

```json
{
  "scope": "foreman",
  "key": "design-freeze-duration-<task-id>",
  "task_id": "<task-id>",
  "freeze_start": "<ISO 8601>",
  "freeze_end": "<ISO 8601 or null if active>",
  "duration_minutes": "<calculated>",
  "status": "<ACTIVE | RELEASED>"
}
```

**Alert Thresholds**:
- Freeze active > 48 hours → Review progress
- Freeze active > 1 week → Investigate (possible stall)

---

## VII. Unfreeze Conditions

### Condition 1: Build Completes Successfully

Design Freeze is released when:

- [ ] Builder reports completion
- [ ] Evidence reviewed by Foreman
- [ ] All tests passing (100%)
- [ ] Zero test debt
- [ ] Build quality validated
- [ ] Completion approved by Foreman

**Action**: Foreman releases freeze and records completion

### Condition 2: Build is Explicitly Aborted

Design Freeze is released when:

- Build cannot proceed due to fundamental issue
- Architecture-QA mismatch discovered
- Impossible requirements found
- Critical issue requires redesign

**Action**: Foreman aborts build, releases freeze, allows architecture/QA modification

### Release Recording

Record freeze release:

```json
{
  "scope": "foreman",
  "key": "design-freeze-<task-id>",
  "status": "RELEASED",
  "task_id": "<task-id>",
  "release_reason": "<COMPLETION | ABORT>",
  "released_by": "Maturion Foreman",
  "timestamp": "<ISO 8601>"
}
```

---

## VIII. Freeze Violations

### What Constitutes a Violation

A freeze violation occurs when:

1. **Architecture Modified During Freeze**
   - Architecture document edited
   - Requirements changed
   - Specifications revised

2. **QA Modified During Freeze**
   - Tests added or removed
   - Test assertions changed
   - Acceptance criteria modified

3. **Scope Changed During Freeze**
   - New features added mid-build
   - Requirements expanded
   - Work beyond architecture/QA scope

### Violation Detection

Violations can be detected by:
- Git commit history showing changes to frozen files
- Builder reporting scope beyond architecture
- Evidence showing features not in QA
- Memory showing unauthorized modifications

### Violation Response

When violation detected:

**Step 1: HALT**
- Stop all build activity immediately
- Do NOT proceed with merge

**Step 2: ASSESS**
- Identify what was modified
- Identify who made modification
- Identify impact on build integrity

**Step 3: REMEDIATE**

**If minor clarification (no spec change)**:
- Document clarification
- Continue build

**If specification changed**:
- ABORT build
- Revert changes
- Re-validate architecture/QA
- Re-issue Build-to-Green
- Restart build cycle

**Step 4: RECORD**

Log violation to governance memory:

```json
{
  "scope": "foreman",
  "key": "freeze-violation-<incident-id>",
  "task_id": "<task-id>",
  "violation_type": "<ARCHITECTURE_MODIFIED | QA_MODIFIED | SCOPE_CHANGED>",
  "description": "<what was modified>",
  "impact": "<impact assessment>",
  "resolution": "<how it was resolved>",
  "timestamp": "<ISO 8601>"
}
```

**Step 5: ESCALATE**

Escalate to Johan:
- Report violation
- Explain impact
- Recommend process improvement

### Violation Consequences

Freeze violations compromise:
- **One-Time Build Correctness** - Moving target prevents first-time success
- **Zero Regression** - Untested changes may break existing functionality
- **Evidence Integrity** - Build evidence no longer matches specifications
- **Audit Trail** - Cannot trace what was built vs. what was designed

**Violations are governance incidents and must be taken seriously.**

---

## IX. Exceptions and Owner Override

### Exceptional Circumstances

Design Freeze may be overridden only for:

1. **Critical Security Vulnerability**
   - Security issue discovered in architecture
   - Must be fixed immediately
   - Cannot wait for build abort and restart

2. **Data Integrity Risk**
   - Architecture would cause data corruption
   - Must be corrected immediately

3. **Compliance Violation**
   - Architecture violates regulatory requirement
   - Must be fixed immediately

4. **Emergency Production Issue**
   - Live system down
   - Hotfix required
   - Normal process too slow

### Owner Override Authority

**Only Johan (repository owner) may override Design Freeze.**

**Override Process**:

1. **Johan explicitly states override**: "I am overriding Design Freeze for task-X"
2. **Foreman documents override**:
   ```json
   {
     "scope": "foreman",
     "key": "freeze-override-<task-id>",
     "task_id": "<task-id>",
     "override_by": "Johan",
     "reason": "<explicit reason>",
     "changes_made": ["<list of changes>"],
     "timestamp": "<ISO 8601>"
   }
   ```
3. **Changes are made** to architecture/QA
4. **Override completes**
5. **Design Freeze resumes** immediately (now with updated architecture/QA)

**Override Characteristics**:
- **Temporary**: Applies only to specific changes
- **Explicit**: Must be clearly stated
- **Documented**: Recorded in memory
- **Automatic Reversion**: Freeze resumes after changes made

---

## X. Rationale and Benefits

### Why Design Freeze Matters

**Prevents Moving Targets**:
- Builders implement against stable specifications
- Tests validate against consistent requirements
- Evidence trail is coherent and auditable

**Enables One-Time Build Correctness**:
- Complete architecture before building
- No mid-build pivots
- No interpretation changes
- First implementation matches design

**Ensures Zero Regression**:
- Changes are intentional, not reactive
- All changes go through validation
- No surprise modifications

**Maintains Evidence Integrity**:
- Evidence matches specifications
- Audit trail is clear
- Can trace every decision

**Enforces Discipline**:
- Forces complete design upfront
- Rewards thorough planning
- Discourages "code first, design later"

### Cost of NOT Having Design Freeze

Without Design Freeze:

- ❌ **Moving targets** - Builders chase changing specs
- ❌ **Wasted effort** - Code rewritten due to spec changes
- ❌ **Hidden changes** - Requirements drift without visibility
- ❌ **Evidence mismatch** - What was built ≠ what was designed
- ❌ **Regression risk** - Untested changes break existing code
- ❌ **Audit failure** - Cannot prove what was built matches requirements

---

## XI. Implementation Checklist

### For Foreman

When issuing Build-to-Green:

- [ ] Verify architecture 100% complete
- [ ] Verify QA 100% complete and RED
- [ ] Activate Design Freeze
- [ ] Record freeze activation in memory
- [ ] Communicate freeze status to builder
- [ ] Monitor for violations during build
- [ ] Release freeze upon completion or abort

### For Builders

When receiving Build-to-Green:

- [ ] Acknowledge Design Freeze is active
- [ ] Do NOT modify architecture or QA documents
- [ ] Implement code to make tests pass
- [ ] Escalate if architecture unclear (do NOT interpret)
- [ ] Escalate if architecture-QA conflict (do NOT resolve independently)
- [ ] Report completion when all tests pass
- [ ] Await freeze release

### For Human Operators

During active Design Freeze:

- [ ] Do NOT edit architecture files
- [ ] Do NOT edit QA test files
- [ ] Provide guidance if requested (without modifying docs)
- [ ] Monitor for violations
- [ ] Override only if critical and authorized

---

## XII. Integration with Build Philosophy

Design Freeze Rule implements:

**Principle #1: One-Time Build Correctness**
- Complete specifications before building
- No mid-build changes
- First implementation is correct

**Principle #2: Zero Regression**
- All changes validated before building
- No surprise modifications
- Intentional evolution only

**Principle #3: Full Architectural Alignment**
- Architecture is frozen and enforced
- No drift during implementation
- Builders follow architecture exactly

**Principle #5: Zero Ambiguity**
- Specifications don't change mid-build
- Requirements are stable
- Acceptance criteria fixed

---

## XIII. Related Documents

This rule connects with:

- **BUILD_PHILOSOPHY.md** - Supreme authority for all building
- **foreman/governance/governance-supremacy-rule.md** - Governance enforcement
- **foreman/builder-specs/build-to-green-rule.md** - Builder protocol
- **foreman/constitution/architecture-design-checklist.md** - Architecture completeness
- **foreman/qa-governance.md** - QA requirements
- **foreman/FOREMAN_EXECUTION_PLAYBOOK.md** - Operational guide

---

## XIV. Version and Authority

**Version**: 1.0.0  
**Status**: Active and Enforced  
**Authority**: Constitutional Governance Rule  
**Precedence**: Mandatory for all builds  
**Last Updated**: 2025-12-15  
**Owner**: Johan (MaturionISMS)  
**Enforcer**: Maturion Foreman

**Changelog**:
- 1.0.0 (2025-12-15): Initial Design Freeze Rule

---

## XV. Summary: The Commitment

Design Freeze Rule ensures:

1. ✅ **Stable Specifications** - Architecture and QA don't change during build
2. ✅ **One-Time Correctness** - Builders implement against complete, frozen specs
3. ✅ **Zero Regression** - All changes are validated before building
4. ✅ **Evidence Integrity** - What was built matches what was designed
5. ✅ **Audit Trail** - Clear, coherent record of all decisions

**Once Build to Green is issued, specifications are FROZEN.**  
**Build completes or aborts.**  
**No moving targets.**  
**Ever.**

---

*END OF DESIGN FREEZE RULE*
