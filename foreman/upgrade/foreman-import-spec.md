# Foreman Import Specification

## Purpose

Define how Foreman consumes exported runtime knowledge when preparing the next version.

---

## 1. Import Process

### 1.1 Pre-Import Validation
- Verify export format matches `runtime-export-spec.md`
- Verify privacy validation passed
- Verify export is from expected platform version
- Verify no tenant data present

### 1.2 Knowledge Integration
- Load runtime state into governance context
- Integrate behaviour events into historical issues
- Update reasoning patterns with new learnings
- Feed performance trends into architecture planning

### 1.3 Priority Setting
- Map incidents to builder tasks
- Prioritize architectural lessons
- Flag compliance gaps for immediate attention
- Identify performance optimization opportunities

---

## 2. Import Mapping

| Export Artefact | Foreman Knowledge Layer | Action |
|----------------|------------------------|--------|
| Runtime State | Architecture Index | Update module health baselines |
| Behaviour Events | Historical Issues | Add to incident database |
| AI Metrics | Reasoning Patterns | Update AI behaviour baselines |
| User Feedback | Enhancement Backlog | Prioritize feature requests |
| Compliance State | Compliance Engine | Update compliance posture |

---

## 3. Post-Import Actions

After successful import:

1. **Governance Update**
   - Update architecture validation rules if needed
   - Update QA requirements based on lessons
   - Update compliance mappings if new requirements

2. **Builder Task Generation**
   - Create tasks for critical incidents
   - Create tasks for recurring issues
   - Create tasks for compliance gaps
   - Create tasks for performance optimizations

3. **Documentation Update**
   - Update `architectural-lessons.md`
   - Update builder guidance documents
   - Update QA-of-QA rules

4. **Reporting**
   - Generate upgrade planning report
   - Document what was learned
   - Identify version improvement themes

---

## 4. Validation Post-Import

- [ ] All critical issues have corresponding tasks
- [ ] All compliance gaps are tracked
- [ ] Performance baselines updated
- [ ] Architectural lessons documented
- [ ] Import logged in change management system
