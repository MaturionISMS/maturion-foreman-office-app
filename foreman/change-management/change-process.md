# Change Process

## Stages

1. **Change Idea / Request**
   - Created using `change-risk-assessment-template.md` and
     `change-impact-analysis-template.md`.

2. **Triage**
   - Categorise (defect / improvement / feature / compliance).
   - Assign initial priority & owner.

3. **Analysis**
   - Complete risk assessment.
   - Complete impact analysis.
   - Draft test plan and rollback plan.

4. **Approval**
   - Follow `change-approval-workflow.md`.

5. **Implementation**
   - Builders implement change in dev → test.
   - Foreman checks QA and governance impact.

6. **Validation**
   - Execute test plan.
   - Evaluate against acceptance criteria.

7. **Release**
   - Promote to production according to `prod-to-test-switch-protocol.md`.
   - Update `change-log-schema.json` record.

8. **Review**
   - Post-implementation review and lessons captured to
     `ai-memory/architectural-lessons.md`.
