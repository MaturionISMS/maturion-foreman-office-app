# App Description Requirement Policy

**Status**: Mandatory  
**Last Updated**: 2025-12-22  
**Authority**: Johan Ras  
**Wave**: Governance Structure Enforcement

---

## I. Constitutional Authority

**App Descriptions are the authoritative source of product intent.**

All Functional Requirement Specifications, architectures, and implementations must derive from and align with an approved App Description.

**No architecture design or build may proceed without an approved App Description.**

---

## II. Purpose

This policy exists to ensure that:
1. Product intent is explicitly captured and authorized before requirements are defined
2. Functional specifications derive from authoritative product descriptions
3. Architecture design aligns with product vision
4. Traceability exists from product intent → requirements → architecture → implementation
5. No application is built without clear, approved product definition

---

## III. Policy Rules

### Rule 1: App Description Is Mandatory

**For every application, an App Description MUST exist before any of the following activities begin**:
- Functional Requirement Specification creation
- Architecture design
- Build authorization
- Implementation

**No exceptions.**

---

### Rule 2: App Description Must Be Authoritative

An App Description is considered authoritative when:
- ✅ Owner explicitly identified (must be Product Owner or authorized delegate)
- ✅ Status marked as "Authoritative" or "Approved"
- ✅ Version identified (e.g., "v1", "Wave 0", "2025-12-22")
- ✅ Purpose clearly defined
- ✅ Scope explicitly stated (what is included, what is not)
- ✅ Success criteria defined

**Non-authoritative, draft, or incomplete App Descriptions do NOT satisfy this policy.**

---

### Rule 3: Canonical Location

**Canonical Location**: `docs/governance/{APP}_APP_DESCRIPTION.md`

Where `{APP}` is the application identifier (e.g., `FM`, `COURSE_CRAFTER`, `RISK_REGISTER`).

**Example**: `docs/governance/FM_APP_DESCRIPTION.md`

**Optional Duplicate**: A duplicate copy MAY exist at repository root (`/APP_DESCRIPTION.md`) for convenience, but governance validation MUST reference the canonical location.

---

### Rule 4: Functional Requirement Specifications Must Derive From App Description

Every Functional Requirement Specification (FRS) MUST:
1. **Explicitly reference the App Description**
   - Include in Section 0 or Section 1
   - Statement format: "This specification is derived from `{APP}_APP_DESCRIPTION.md`"

2. **Align with App Description intent**
   - FRS purpose must align with App Description purpose
   - FRS scope must align with App Description scope
   - FRS success criteria must align with App Description success criteria

3. **Not contradict App Description**
   - No FRS requirement may contradict App Description intent
   - No FRS feature may be declared out-of-scope if App Description declares it in-scope
   - No FRS success criterion may conflict with App Description success criterion

**If alignment cannot be achieved, App Description must be revised (with owner approval) before FRS proceeds.**

---

### Rule 5: Architecture Must Align With App Description

Every architecture artifact (True North, Architecture Spec, etc.) MUST:
1. **Reference the App Description**
   - True North must state: "This True North is derived from and aligned with `{APP}_APP_DESCRIPTION.md`"

2. **Validate alignment**
   - Architecture must not introduce goals or scope not present in App Description
   - Architecture must not contradict App Description intent

**Architecture Compilation Contract cannot PASS without App Description validation.**

---

### Rule 6: Validation Is Mandatory

Before architecture compilation or build authorization:
1. **App Description Validation**
   - Confirm App Description exists
   - Confirm App Description is authoritative
   - Confirm owner and approval status

2. **Derivation Validation**
   - Confirm FRS explicitly references App Description
   - Confirm FRS aligns with App Description
   - Confirm no contradictions exist

3. **Traceability Validation**
   - Confirm traceability chain: App Description → FRS → Architecture

**Validation checklist**: `governance/contracts/app-description-frs-alignment-checklist.md`

---

## IV. Enforcement Mechanisms

### Enforcement Point 1: Architecture Compilation Contract

**Location**: `governance/architecture/ARCHITECTURE_COMPILATION_CONTRACT.md`

**Enforcement**:
- App Description listed as required input artifact
- Input validation blocks compilation if App Description missing or non-authoritative
- Phase 1 validates FRS derivation from App Description

---

### Enforcement Point 2: Build Authorization Gate

**Location**: `governance/build/BUILD_AUTHORIZATION_GATE.md`

**Enforcement**:
- Precondition 1 validates App Description existence and authority
- Precondition 1 validates FRS references App Description
- Gate cannot PASS if validation fails

---

### Enforcement Point 3: Minimum Architecture Template

**Location**: `governance/specs/minimum-architecture-template.md`

**Enforcement**:
- True North requires explicit App Description alignment statement
- Template validation fails if alignment statement missing

---

## V. Roles and Responsibilities

### Product Owner (Johan Ras for FM)

**Responsibilities**:
- Create and approve App Descriptions
- Maintain App Description authority
- Approve App Description revisions
- Resolve conflicts between App Description and downstream artifacts

**Authority**:
- Final authority on App Description content
- May revise App Description (triggers FRS/architecture re-validation)
- May declare App Description frozen

---

### Governance Liaison

**Responsibilities**:
- Validate App Description exists and is authoritative
- Validate FRS derives from App Description
- Validate architecture aligns with App Description
- Block builds if validation fails
- Escalate validation failures to Product Owner

**Authority**:
- Veto power over builds lacking App Description
- Authority to demand App Description before FRS creation
- Authority to block architecture compilation

---

### Functional Spec Author

**Responsibilities**:
- Derive FRS from App Description
- Explicitly reference App Description in FRS
- Ensure FRS aligns with and does not contradict App Description
- Escalate alignment issues to Product Owner

**Prohibitions**:
- Cannot create FRS without approved App Description
- Cannot ignore or override App Description intent

---

### Architecture Designer

**Responsibilities**:
- Align architecture with App Description
- State alignment explicitly in True North
- Escalate conflicts to Product Owner

**Prohibitions**:
- Cannot design architecture without approved App Description
- Cannot proceed if FRS does not reference App Description

---

## VI. Failure Modes and Handling

### Failure Mode 1: App Description Missing

**Symptoms**: App Description file does not exist at canonical location

**Handling**:
1. BLOCK all downstream activities (FRS, architecture, build)
2. Escalate to Product Owner
3. Do NOT proceed until App Description created and approved
4. Log failure: `FAILURE_TYPE: APP_DESCRIPTION_MISSING`

---

### Failure Mode 2: App Description Not Authoritative

**Symptoms**: App Description exists but:
- Status is "Draft" or "In Progress"
- Owner not identified
- Approval not confirmed

**Handling**:
1. BLOCK all downstream activities
2. Escalate to Product Owner
3. Request approval or revision
4. Do NOT proceed until authoritative status confirmed
5. Log failure: `FAILURE_TYPE: APP_DESCRIPTION_NOT_AUTHORITATIVE`

---

### Failure Mode 3: FRS Does Not Reference App Description

**Symptoms**: FRS exists but:
- No App Description reference in Section 0 or 1
- No derivation statement
- No alignment validation

**Handling**:
1. BLOCK architecture compilation
2. BLOCK build authorization
3. Request FRS revision
4. Add explicit App Description reference and derivation statement
5. Re-validate alignment
6. Log failure: `FAILURE_TYPE: FRS_MISSING_APP_DESC_REFERENCE`

---

### Failure Mode 4: FRS Contradicts App Description

**Symptoms**: FRS contains requirements that:
- Contradict App Description intent
- Declare features out-of-scope that App Description declares in-scope
- Define success criteria conflicting with App Description

**Handling**:
1. BLOCK architecture compilation
2. Identify contradictions explicitly
3. Escalate to Product Owner
4. Either: Revise FRS to align, OR
5. Or: Revise App Description (requires owner approval)
6. Re-validate alignment
7. Log failure: `FAILURE_TYPE: FRS_CONTRADICTS_APP_DESC`

---

### Failure Mode 5: Architecture Does Not Align With App Description

**Symptoms**: Architecture (True North, specs) does not:
- Reference App Description
- Align with App Description intent
- Satisfy App Description success criteria

**Handling**:
1. BLOCK build authorization
2. Identify misalignments
3. Revise architecture to align
4. Add explicit App Description alignment statement
5. Re-validate
6. Log failure: `FAILURE_TYPE: ARCHITECTURE_MISALIGNED_WITH_APP_DESC`

---

## VII. Escalation Protocol

### When to Escalate

Escalate to Product Owner (Johan Ras for FM) if:
1. App Description missing and urgency is high
2. App Description conflicts with business objectives
3. FRS cannot align with App Description
4. Architecture cannot satisfy App Description intent
5. App Description revision required

### Escalation Content

Must include:
- Which policy rule is blocking
- What artifact is missing or misaligned
- Evidence of validation failure
- Proposed resolution
- Impact of delay

### Escalation Response

Product Owner will:
- Approve App Description creation/revision, OR
- Clarify App Description intent, OR
- Authorize FRS/architecture adjustment, OR
- Confirm block remains until resolution

---

## VIII. Audit and Compliance

### Audit Queries

Auditors can verify:
- Does App Description exist for this application?
- Is App Description authoritative and approved?
- Does FRS explicitly reference App Description?
- Does FRS align with App Description?
- Does architecture align with App Description?
- Was build authorized without App Description?

### Evidence Requirements

For each application:
- App Description file (canonical location)
- App Description approval record
- FRS with explicit App Description reference
- Alignment validation checklist (completed)
- Traceability matrix (App Desc → FRS → Architecture)

**Retention**: Indefinite (audit requirement)

---

## IX. Exception Policy

### No Exceptions Permitted

This policy has **zero exceptions**.

**Why**:
- App Descriptions are foundational to product intent
- Without App Description, product goals are undefined
- Risk of building wrong thing is unacceptably high
- Governance integrity depends on authoritative product definition

**Even for**:
- Small changes
- Urgent fixes
- Experimental features
- Prototypes

**All applications require App Descriptions.**

---

## X. Success Criteria

This policy is successful when:
1. ✅ Every application has an approved App Description
2. ✅ Every FRS explicitly references its App Description
3. ✅ Every architecture aligns with its App Description
4. ✅ No build proceeds without App Description validation
5. ✅ Traceability from product intent to implementation is complete
6. ✅ Zero governance violations related to App Description compliance

---

## XI. Machine Decidability

**This policy is designed to be mechanically enforceable.**

Future FM Agent implementation will:
- Automate App Description existence check
- Automate authoritative status validation
- Automate FRS reference validation
- Automate alignment checking
- Block builds automatically on policy violation
- Generate audit trail automatically

**Human interpretation MUST NOT be required for policy enforcement.**

---

## XII. References

- **Build Authorization Gate**: `governance/build/BUILD_AUTHORIZATION_GATE.md`
- **Architecture Compilation Contract**: `governance/architecture/ARCHITECTURE_COMPILATION_CONTRACT.md`
- **Minimum Architecture Template**: `governance/specs/minimum-architecture-template.md`
- **Alignment Validation Checklist**: `governance/contracts/app-description-frs-alignment-checklist.md`
- **Build Philosophy**: `/BUILD_PHILOSOPHY.md`

---

## XIII. Constitutional Rules

1. **App Description Is Mandatory** - Non-negotiable
2. **App Description Must Be Authoritative** - Non-negotiable
3. **FRS Must Derive From App Description** - Non-negotiable
4. **Architecture Must Align With App Description** - Non-negotiable
5. **Validation Is Required** - Non-negotiable
6. **No Exceptions** - Non-negotiable

**Violation of these rules is a governance violation requiring immediate escalation and remediation.**

---

*App Description Requirement Policy - Authoritative Product Intent, Zero Compromise*
