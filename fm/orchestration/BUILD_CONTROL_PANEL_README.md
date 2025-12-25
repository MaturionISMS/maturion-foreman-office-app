# Build Control Panel & Execution Console

## Overview

The Build Control Panel is the primary human-facing interface for initiating, monitoring, and controlling builds in a governed manner according to the Maturion Build Authorization Gate.

## Purpose

This implementation provides:
- **Explicit Human Control**: No build can start without explicit human action
- **Governance Enforcement**: All builds must pass the Build Authorization Gate before execution
- **Transparent Blocking**: Readiness failures are explicit, actionable, and auditable
- **No Silent Execution**: All execution paths are explicit and logged

## Architecture

### Components

1. **Build Authorization Gate Validator** (`build_authorization_gate.py`)
   - Validates all 8 mandatory preconditions
   - Generates evidence packages
   - Produces PASS/FAIL determinations

2. **Build Control API** (`build_control_api.py`)
   - Flask-based REST API
   - Handles build validation requests
   - Routes build execution (authorization check)
   - Provides build status queries

3. **Web UI** (`static/`)
   - HTML/CSS/JS interface
   - Build selection and identification
   - "Request Build Execution" action
   - Modal feedback for blocking conditions

## Build Authorization Gate

The Build Authorization Gate validates **8 mandatory preconditions**:

1. ✅ App Description Exists and Is Authoritative
2. ✅ Architecture Compilation Contract = PASS
3. ✅ QA Derivation & Coverage Rules = PASS
4. ✅ FL/CI Learning Integration = COMPLETE
5. ✅ Deployment and Runtime Validation = COMPLETE
6. ✅ Governance Checklist = PASS
7. ✅ Scope Freeze = CONFIRMED
8. ✅ Zero Test Debt = CONFIRMED

**ALL preconditions must be satisfied for the gate to resolve to PASS.**

## Usage

### Starting the Server

```bash
# Install dependencies
pip install -r requirements.txt

# Start the Build Control API
cd fm/orchestration
python build_control_api.py
```

The server will start on `http://localhost:5000`

### Using the Web Interface

1. Open your browser to `http://localhost:5000`
2. Enter a Build ID or click "List Available Builds"
3. Select a build from the list
4. Click "Request Build Execution Readiness Validation"
5. Review the gate validation results
6. If PASS, you can proceed with "Execute Build"
7. If FAIL, review blocking conditions and remediate

### API Endpoints

#### Health Check
```
GET /api/health
```

#### List Builds
```
GET /api/builds
```

Returns all builds found in `architecture/builds/`

#### Validate Build
```
POST /api/builds/<build_id>/validate
```

Invokes the Build Authorization Gate for the specified build.

**Response:**
```json
{
  "build_id": "fm-app-v1.0",
  "gate_result": "PASS" | "FAIL",
  "timestamp": "2025-12-25T12:00:00Z",
  "summary": "Build Authorization Gate: PASS...",
  "preconditions": [...],
  "evidence_path": "architecture/builds/fm-app-v1.0/authorization-evidence",
  "can_proceed": true
}
```

#### Execute Build
```
POST /api/builds/<build_id>/execute
```

Requests build execution. **Only succeeds if authorization gate passed.**

**Response (if authorized):**
```json
{
  "status": "authorized",
  "message": "Build authorization confirmed. Ready for execution.",
  "build_id": "fm-app-v1.0"
}
```

**Response (if blocked):**
```json
{
  "error": "Build execution blocked",
  "message": "Build failed Authorization Gate",
  "action_required": "Resolve blocking conditions",
  "blocker_details": "..."
}
```

#### Get Build Status
```
GET /api/builds/<build_id>/status
```

Returns the current authorization status of a build.

## Evidence Package

When a build is validated, a complete evidence package is generated at:

```
architecture/builds/<build-id>/authorization-evidence/
├── gate-validation-report.md
├── authorization-decision.md
├── gate-validation-result.json
├── authorization-timestamp.txt (if PASS)
└── blocker-report.md (if FAIL)
```

This package provides:
- Full audit trail
- Precondition validation results
- Evidence file references
- Blocking conditions (if any)

## Testing

Run the test suite:

```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run all tests
pytest tests/test_build_authorization_gate.py -v
pytest tests/test_build_control_api.py -v
```

## Governance Alignment

This implementation is based on:
- `governance/build/BUILD_AUTHORIZATION_GATE.md` (G-C8, G-C9, G-C10)
- Build Execution Readiness Gate requirements
- Foreman Execution State Model

## Security & Governance

- **No Silent Execution**: All build actions require explicit human approval
- **Evidence-Based**: All decisions backed by evidence packages
- **Audit Trail**: Complete logging of all validation and execution requests
- **Governance Supremacy**: Gate preconditions are non-negotiable
- **Binary Resolution**: PASS or FAIL only, no partial approvals

## Out of Scope

This implementation does **NOT** include:
- Pipeline execution engines
- CI/CD implementation
- Builder agent logic
- New governance rules

Build execution routing to CI/CD systems is delegated and not implemented in this scope.

## References

- **Build Authorization Gate**: `governance/build/BUILD_AUTHORIZATION_GATE.md`
- **Build Philosophy**: `/BUILD_PHILOSOPHY.md`
- **FM Orchestration**: `fm/orchestration/README.md`
- **Architecture Governance**: `governance/architecture/`

---

*Build Control Panel - Governed, Explicit, Auditable Build Execution*
