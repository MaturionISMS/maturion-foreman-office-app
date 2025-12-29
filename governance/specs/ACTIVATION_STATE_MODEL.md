# Activation State Model

**Version**: 1.0.0  
**Status**: Active  
**Authority**: BUILD_TREE_EXECUTION_MODEL.md (G-C8)  
**Last Updated**: 2025-12-25

---

## Purpose

This document provides a **quick reference** for the Activation State Model used in the Maturion FM build system.

**Primary Authority**: See `BUILD_TREE_EXECUTION_MODEL.md` (Section IV) for complete specification.

---

## Activation States

Activation states track the **approval and authorization status** of build tree nodes, independent of execution progress.

### State Definitions

#### DRAFT
**Meaning**: Not yet approved for execution

**Characteristics**:
- Planning in progress
- Architecture may be incomplete
- Not authorized to start execution
- Can be edited freely

**Applies To**: Programs, Waves

---

#### APPROVED
**Meaning**: Authorized to execute

**Characteristics**:
- Architecture complete and validated
- QA designed and RED status confirmed
- Build-to-Green instruction prepared
- Ready to assign to builder

**Applies To**: Programs, Waves, Tasks

---

#### ACTIVE
**Meaning**: Currently executing

**Characteristics**:
- Builder assigned (for Tasks)
- Execution in progress
- Design Freeze active
- Progress being monitored

**Applies To**: Programs, Waves, Tasks

---

#### REVIEW
**Meaning**: Execution complete, awaiting validation

**Characteristics**:
- Builder reports completion
- Evidence submitted
- QA results available
- Foreman reviewing

**Applies To**: Tasks

---

#### MERGED
**Meaning**: Accepted and merged

**Characteristics**:
- Evidence validated
- QA 100% pass
- PR merged
- Artifact preserved

**Applies To**: Tasks

---

#### BLOCKED
**Meaning**: Activation cannot proceed due to dependency or blocker

**Characteristics**:
- Specific blocker identified
- Resolution path defined or being investigated
- Execution paused

**Applies To**: Programs, Waves, Tasks

---

## State Transitions

### Task Activation Flow

```
DRAFT → APPROVED → ACTIVE → REVIEW → MERGED
         ↓           ↓         ↓
       BLOCKED ←───────────────┘
```

### Wave/Program Activation Flow

```
DRAFT → APPROVED → ACTIVE → COMPLETE
         ↓           ↓
       BLOCKED ←─────┘
```

---

## Relationship to Execution States

**Activation State** vs **Execution State**:

- **Execution State**: What is happening RIGHT NOW (PLANNED, IN_PROGRESS, BLOCKED, COMPLETE)
- **Activation State**: Authorization and approval status (DRAFT, APPROVED, ACTIVE, REVIEW, MERGED)

**Example**:
- A task can be EXECUTION=PLANNED (not started) and ACTIVATION=APPROVED (authorized to start)
- A task can be EXECUTION=COMPLETE (done) and ACTIVATION=REVIEW (awaiting sign-off)

---

## Visual Representation

When visualizing:
- Show Execution State as primary badge
- Show Activation State as secondary indicator or on hover/detail view
- Use distinct colors/icons to avoid confusion

**Example**:
```
Task: AI Panel  [IN_PROGRESS] ⚡ ACTIVE [🟢 GREEN] [0%]
                 ↑ Execution    ↑ Activation
```

---

## Governance Rules

1. **Cannot start execution until APPROVED**
   - Task cannot move to EXECUTION=IN_PROGRESS unless ACTIVATION=APPROVED or ACTIVE

2. **Cannot merge until REVIEW complete**
   - Task cannot be ACTIVATION=MERGED unless Foreman validates evidence

3. **BLOCKED overrides all**
   - If ACTIVATION=BLOCKED, execution must pause regardless of execution state

4. **Design Freeze during ACTIVE**
   - When ACTIVATION=ACTIVE, architecture and QA are frozen

---

## For Complete Details

See **BUILD_TREE_EXECUTION_MODEL.md (G-C8)** Section IV for:
- Detailed state definitions
- Transition rules
- Integration with execution states
- Evidence requirements per state

---

*END OF ACTIVATION STATE MODEL QUICK REFERENCE*
