# Startup Guard & Redirects Specification

**Version**: 1.0.0  
**Status**: Architecture Specification (F-U2)  
**Module**: Startup Guard  
**Type**: Enforcement Layer

---

## Purpose

The Startup Guard is the **enforcement layer** that ensures the FM application cannot be accessed before commissioning is complete.

**Core Principle**: Make it impossible to operate the system in an invalid state.

This specification is part of **Batch 2 — Memory & Commissioning Foundations** and adheres to strict constraints:

✅ **DOES**:
- Block access to all protected routes until commissioned
- Redirect unauthorized access to commissioning flow
- Enforce deterministic state-based routing
- Prevent all bypass paths
- Log all access attempts for audit

❌ **DOES NOT**:
- Grant temporary exceptions
- Allow "temporary unlocks"
- Make commissioning decisions (read-only state check)
- Auto-commission the system
- Execute builds or delegation

---

## Architecture

### Guard Mechanism

**Type**: Middleware-based route protection

**Scope**: All application routes except:
- `/commissioning/*` (commissioning wizard)
- `/api/commissioning/*` (commissioning APIs)
- `/health` (health check endpoint)
- `/public/*` (public assets)

**Decision Logic**:
```
IF commissioning state < COMMISSIONED THEN
  REDIRECT to /commissioning
ELSE
  ALLOW access
END IF
```

---

## Guard Behavior

### State-Based Routing

The guard enforces routing based on the commissioning state:

| Commissioning State | Attempted Route | Action |
|---------------------|----------------|--------|
| NOT_COMMISSIONED | Any protected route | Redirect to `/commissioning` |
| COMMISSIONING | Any protected route | Redirect to `/commissioning` (resume wizard) |
| COMMISSIONED | Any route | Allow access |
| ACTIVE | Any route | Allow access |
| SUSPENDED | Any protected route | Redirect to `/commissioning/suspended` |

### Protected Routes

The following routes are **protected** and require commissioning:

- `/` (root/dashboard)
- `/dashboard/*`
- `/memory/*`
- `/governance/*`
- `/settings/*`
- `/admin/*`
- `/api/*` (except `/api/commissioning/*`)

### Unprotected Routes

The following routes are **always accessible**:

- `/commissioning` (commissioning wizard)
- `/commissioning/*` (all wizard steps)
- `/api/commissioning/*` (commissioning APIs)
- `/health` (health check)
- `/public/*` (static assets, CSS, JS, images)

---

## Redirect Rules

### Rule 1: Deterministic Redirection

**Principle**: Every redirect is based on current state and is deterministic.

### Rule 2: No Bypass Paths

**Principle**: There must be no way to bypass the startup guard.

**Bypass Prevention Checklist**:
- ❌ No "Skip Commissioning" button
- ❌ No debug mode that bypasses guard
- ❌ No temporary exceptions
- ❌ No time-limited unlocks
- ❌ No query parameter overrides
- ❌ No environment variable bypasses (except test mode)

### Rule 3: Persistent State Check

**Principle**: State is checked on every navigation, not cached indefinitely.

---

## Batch 2 Compliance

Per Batch 2 requirements, this guard specification:

✅ **DOES**:
- Enforce deterministic redirects based on truth (commissioning state)
- Make it impossible to operate system in invalid state
- Provide no bypass paths
- Log all access attempts for audit

❌ **DOES NOT**:
- Grant temporary exceptions
- Allow "temporary unlocks"
- Make commissioning decisions (read-only state check)
- Auto-commission the system
- Execute builds or delegation

---

## Critical Statement

**This guard does NOT trigger execution, builds, or external delegation.**

The Startup Guard is a pure enforcement layer. It only checks state and redirects. All commissioning state is managed by the `CommissioningController`.

---

## Governance

**Authority**: Issue #173 (F-U2)  
**Batch**: Batch 2 — Memory & Commissioning Foundations  
**Architecture**: Enforcement layer with deterministic redirects  
**QA**: Integration tests required  
**Compliance**: Zero bypass paths, zero temporary exceptions

---

**End of Startup Guard & Redirects Specification**

**STATUS**: Architecture Specification Only — Implementation Pending
