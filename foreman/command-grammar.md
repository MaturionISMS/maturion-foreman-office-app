# Maturion Command Grammar

## Purpose

This document defines the precise instruction formats for:
1. **Johan and Admins → Maturion**: How administrators should communicate with Maturion
2. **Users → Maturion**: How end-users should communicate with Maturion
3. **Maturion → Builder Agents**: How Maturion instructs builder agents

Clear, structured command grammar ensures:
- Unambiguous instructions
- Consistent processing
- Predictable outcomes
- Efficient delegation
- Traceable decision-making

---

## Part 1: Admin → Maturion Instructions (Johan and Future Admins)

Administrators (Johan and future admin users) can use natural language commands prefixed with **"Maturion"** or structured formats for complex requests.

### Quick Command Format (Natural Language)

Admins can use simple, direct commands:

```
Maturion, [action] [target] [optional details]
```

**Examples**:
```
Maturion, start Threat module build.
Maturion, inspect PIT integration for drift.
Maturion, show me open QA failures across modules.
Maturion, validate the latest ERM pull request.
Maturion, create a ticket for the vulnerability export bug.
Maturion, summarize platform health for the last 24 hours.
Maturion, what's the status of Course Crafter deployment?
```

### Structured Admin Commands

For more complex requests, admins can use structured formats:

#### Admin Governance Command
```
Maturion, [GOVERNANCE]
Action: [Review | Approve | Reject | Update]
Target: [Architecture | Module Boundary | Integration | QA Rule]
Details: [Specific request or change]
```

**Example**:
```
Maturion, [GOVERNANCE]
Action: Review
Target: Module Boundary
Details: Evaluate if PIT module should access Threat database directly or via API
```

#### Admin Monitoring Command
```
Maturion, [MONITOR]
Scope: [Platform-wide | Module-specific | Tenant-specific]
Target: [Module name or "All"]
Timeframe: [Last hour | Last 24h | Last 7 days]
```

**Example**:
```
Maturion, [MONITOR]
Scope: Module-specific
Target: Threat module
Timeframe: Last 24h
```

#### Admin Build Command
```
Maturion, [BUILD]
Action: [Start | Inspect | Deploy | Rollback]
Module: [Module name]
Priority: [Critical | High | Normal]
```

**Example**:
```
Maturion, [BUILD]
Action: Start
Module: Threat
Priority: High
```

---

## Part 2: User → Maturion Instructions

### Instruction Format Categories

#### 1. Governance Query Format
**Purpose**: Request clarification on rules, boundaries, or architectural decisions

```
[GOVERNANCE QUERY]
Type: [Rule Clarification | Boundary Definition | Architectural Guidance | Conflict Resolution]
Context: [Brief description of the situation]
Question: [Specific question requiring governance input]
Relevant Documents: [List of applicable True North docs, SRMF sections, etc.]
```

**Example**:
```
[GOVERNANCE QUERY]
Type: Boundary Definition
Context: ERM module needs to access Threat module data for risk scoring
Question: Does this violate module boundary rules, or should we use the integration API?
Relevant Documents: INTEGRATED_ISMS_MODULE_INTEGRATION_MAP_v1.0.md, ERM_TRUE_NORTH_v1.0.md
```

#### 2. Validation Request Format
**Purpose**: Request Maturion to validate proposed changes

```
[VALIDATION REQUEST]
Type: [Architecture Change | Code Change | Documentation Change | Configuration Change]
Module(s): [Affected module names]
Change Description: [Summary of proposed changes]
Rationale: [Why this change is needed]
Impact Assessment: [Known or suspected impacts]
Attachments: [File paths, PR links, or document references]
```

**Example**:
```
[VALIDATION REQUEST]
Type: Architecture Change
Module(s): PIT, Threat
Change Description: Add watchdog trigger for stale threat assessments in PIT module
Rationale: Need to alert when threat assessments haven't been updated in 90 days
Impact Assessment: New cross-module dependency between PIT and Threat modules
Attachments: /docs/pit-threat-watchdog-proposal.md
```

#### 3. Delegation Instruction Format
**Purpose**: Request Maturion to delegate work to builder agents

```
[DELEGATION REQUEST]
Task Type: [Implementation | Documentation | Testing | Architecture | Integration]
Module(s): [Target module names]
Objective: [High-level goal]
Requirements: [Specific requirements or constraints]
Success Criteria: [How to measure completion]
Priority: [Critical | High | Medium | Low]
Deadline: [Target completion date, if applicable]
```

**Example**:
```
[DELEGATION REQUEST]
Task Type: Implementation
Module(s): Vulnerability
Objective: Add export functionality for vulnerability reports
Requirements: Must support PDF and CSV formats, follow VULNERABILITY_EXPORT_SPEC_v1.0.md
Success Criteria: Users can export filtered vulnerability lists in both formats
Priority: High
Deadline: End of Sprint 3
```

#### 4. Architecture Review Format
**Purpose**: Request Maturion to review architectural changes

```
[ARCHITECTURE REVIEW]
Change Type: [New Module | Module Update | Integration Change | Boundary Modification]
Scope: [Affected modules and components]
Design Document: [Link or path to design document]
SRMF Alignment: [How this aligns with SRMF principles]
True North Alignment: [How this aligns with True North documents]
Risk Assessment: [Potential risks and mitigation strategies]
Review Requested By: [Date]
```

**Example**:
```
[ARCHITECTURE REVIEW]
Change Type: Integration Change
Scope: Course Crafter, ERM modules
Design Document: /docs/course-crafter-erm-integration-v1.md
SRMF Alignment: Supports E1-E4 training content based on risk assessments
True North Alignment: COURSE_CRAFTER_TRUE_NORTH_v1.0.md section 3.2
Risk Assessment: Low - uses existing integration API pattern
Review Requested By: 2025-12-10
```

#### 5. Issue Escalation Format
**Purpose**: Escalate issues requiring Maturion's attention

```
[ISSUE ESCALATION]
Severity: [Critical | High | Medium | Low]
Issue Type: [Boundary Violation | Quality Failure | Architectural Drift | Builder Conflict]
Description: [Detailed description of the issue]
Current Impact: [What is affected right now]
Proposed Resolution: [Suggested fix or next steps]
Urgency: [Immediate | Within 24h | Within Week | Non-urgent]
```

**Example**:
```
[ISSUE ESCALATION]
Severity: High
Issue Type: Boundary Violation
Description: Risk Assessment module directly accessing Threat module database instead of using API
Current Impact: Tight coupling between modules, violating integration map
Proposed Resolution: Refactor to use THREAT_INTEGRATION_MAP_v1.0.md specified API
Urgency: Within 24h
```

---

## Part 3: Maturion → Builder Agent Instructions

### Instruction Format for Builder Agents

#### 1. Implementation Task Format
**Purpose**: Instruct a builder agent to implement specific functionality

```
[BUILDER TASK: IMPLEMENTATION]
Builder Agent: [Specific agent name from builder-manifest.json]
Task ID: [Unique identifier]
Module: [Target module]
Objective: [Clear, specific goal]

Requirements:
- [Requirement 1]
- [Requirement 2]
- [Requirement N]

Constraints:
- [Constraint 1 - boundaries, technology, etc.]
- [Constraint 2]

References:
- [True North document]
- [Relevant architecture files]
- [Integration specs]

Success Criteria:
- [Criterion 1]
- [Criterion 2]

Quality Gates:
- [ ] Passes QA checklist for [module]
- [ ] No boundary violations
- [ ] Zero regression on existing functionality
- [ ] Documentation updated

Validation: Maturion will review before approval
Deadline: [Target date]
```

#### 2. Documentation Task Format
**Purpose**: Instruct a builder agent to create or update documentation

```
[BUILDER TASK: DOCUMENTATION]
Builder Agent: [Specific agent name]
Task ID: [Unique identifier]
Document Type: [True North | Architecture | API | User Guide | QA Plan]
Target: [Document name or path]

Objective: [What needs to be documented]

Content Requirements:
- [Section 1]
- [Section 2]
- [Section N]

Alignment Requirements:
- Align with: [SRMF section, True North principles, etc.]
- Reference: [Related documents]

Format Standards:
- Follow: [Template or format specification]
- Include: [Required sections]

Validation: Maturion will review for accuracy and completeness
Deadline: [Target date]
```

#### 3. Architecture Task Format
**Purpose**: Instruct a builder agent to design architectural solutions

```
[BUILDER TASK: ARCHITECTURE]
Builder Agent: [Specific agent name]
Task ID: [Unique identifier]
Scope: [Modules or components involved]

Problem Statement: [What needs to be solved]

Architectural Requirements:
- [Requirement 1]
- [Requirement 2]

Constraints:
- Must align with: [SRMF Master Build Reference sections]
- Must respect: [Module boundaries]
- Must integrate via: [Integration patterns]

Deliverables:
- [ ] Architecture diagram
- [ ] Component specification
- [ ] Integration design
- [ ] Risk assessment

Review Process:
1. Initial design review by Maturion
2. Revisions if needed
3. Final approval by Maturion

Deadline: [Target date]
```

#### 4. Testing Task Format
**Purpose**: Instruct a builder agent to create or execute tests

```
[BUILDER TASK: TESTING]
Builder Agent: [Specific agent name]
Task ID: [Unique identifier]
Module: [Target module]
Test Type: [Unit | Integration | E2E | Regression | Performance]

Test Scope: [What to test]

Test Requirements:
- [ ] Test coverage: [Percentage or specific areas]
- [ ] Test scenarios: [List scenarios]
- [ ] Edge cases: [List edge cases]
- [ ] Regression tests: [Existing functionality to verify]

Success Criteria:
- All tests pass
- Coverage meets requirements
- No regression detected

Validation: Maturion will review test completeness
Deadline: [Target date]
```

#### 5. Integration Task Format
**Purpose**: Instruct a builder agent to integrate modules or components

```
[BUILDER TASK: INTEGRATION]
Builder Agent: [Specific agent name]
Task ID: [Unique identifier]
Modules: [Source module] → [Target module]

Integration Objective: [What needs to be connected]

Integration Requirements:
- Use: [Integration pattern from integration map]
- API Specification: [Reference to API spec]
- Data Flow: [Describe data flow]
- Error Handling: [Error handling requirements]

Boundary Rules:
- [Boundary rule 1]
- [Boundary rule 2]

Validation Points:
- [ ] Integration map compliance
- [ ] API specification adherence
- [ ] Error handling tested
- [ ] Performance acceptable
- [ ] Documentation updated

Approval: Maturion must approve before deployment
Deadline: [Target date]
```

---

## Part 4: Response Formats

### Maturion Response to User

```
[MATURION RESPONSE]
Request Type: [Query | Validation | Review | Escalation]
Status: [Approved | Rejected | Conditionally Approved | Needs More Info]

Decision: [Clear decision or answer]

Rationale:
[Explanation of decision based on governance rules]

References:
- [Rule or principle applied]
- [Document section cited]

Next Steps:
- [Action item 1]
- [Action item 2]

Conditions (if applicable):
- [Condition 1]
- [Condition 2]
```

### Builder Agent Response to Maturion

```
[BUILDER RESPONSE]
Task ID: [Task identifier]
Status: [Completed | In Progress | Blocked | Failed]

Progress Summary: [What has been done]

Deliverables:
- [Deliverable 1: path/link]
- [Deliverable 2: path/link]

Quality Checklist:
- [✓] Item 1
- [✓] Item 2
- [ ] Item 3 (pending)

Issues Encountered:
- [Issue 1 and resolution]
- [Issue 2 and resolution]

Pending Items (if not complete):
- [Item 1]
- [Item 2]

Request for Review: [Yes/No]
```

---

## Part 5: Best Practices

### For Users Communicating with Maturion
1. **Be Specific**: Provide clear context and specific questions
2. **Reference Documents**: Cite relevant True North or SRMF documents
3. **State Assumptions**: Make assumptions explicit
4. **Provide Rationale**: Explain why you're requesting something
5. **Include Impact**: Describe known or suspected impacts

### For Maturion Instructing Builders
1. **Be Explicit**: Leave no room for interpretation
2. **Provide Context**: Explain the "why" behind the task
3. **Reference Standards**: Point to applicable governance rules
4. **Set Clear Success Criteria**: Define what "done" means
5. **Include Validation Points**: Specify quality gates

### For Builder Agents Responding to Maturion
1. **Be Transparent**: Report both successes and issues
2. **Provide Evidence**: Link to deliverables and test results
3. **Ask Questions**: Escalate ambiguities immediately
4. **Follow Format**: Use the specified response format
5. **Request Review**: Explicitly request review when ready

---

## Version Control

**Document Version**: 1.1  
**Last Updated**: 2025-12-03  
**Maintained By**: Maturion  
**Review Cycle**: Quarterly or when command patterns evolve

---

**Maturion** - Clear Communication, Precise Execution, Excellent Outcomes
