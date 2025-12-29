# Commissioning Controller

**Version**: 1.0.0  
**Status**: Architecture Implementation (F-A1)  
**Module**: `lib/commissioning`

---

## Purpose

The Commissioning Controller governs whether the Maturion Foreman application may operate.

**Core Principle**: The app MUST NOT function unless commissioning state ≥ COMMISSIONED.

This is an **architecture-only** implementation providing state management and access control logic without UI, automation triggers, or memory activation.

---

## Architecture

### States

The commissioning lifecycle follows these states:

```
NOT_COMMISSIONED → COMMISSIONING → COMMISSIONED → ACTIVE → SUSPENDED
```

#### State Definitions

- **NOT_COMMISSIONED**: Initial state, no operations permitted
- **COMMISSIONING**: Setup in progress, only commissioning operations allowed
- **COMMISSIONED**: Basic operations permitted, ready for activation
- **ACTIVE**: Fully operational, all features available
- **SUSPENDED**: Temporarily paused, read-only mode

### State Persistence

Commissioning state is persisted to:
```
runtime/commissioning/state.json
```

Structure:
```json
{
  "state": "COMMISSIONED",
  "commissioned_at": "2025-12-29T05:00:00Z",
  "commissioned_by": "admin",
  "last_updated": "2025-12-29T05:00:00Z",
  "version": "1.0.0",
  "metadata": {
    "reason": "Initial setup completed",
    "notes": "..."
  }
}
```

---

## Usage

### Initialization

```typescript
import { commissioningController } from '@/lib/commissioning';

// Initialize controller (loads state from disk)
await commissioningController.initialize();
```

### Check Commissioning Status

```typescript
// Check if app is commissioned
if (!commissioningController.isCommissioned()) {
  // Redirect to commissioning flow
  const route = commissioningController.getCommissioningRoute();
  router.push(route);
}

// Check if app is fully operational
if (commissioningController.isOperational()) {
  // Allow all operations
}
```

### Access Control

```typescript
import { CommissioningState } from '@/lib/commissioning';

// Check if specific operation is allowed
const result = commissioningController.checkAccess(
  CommissioningState.COMMISSIONED
);

if (!result.allowed) {
  console.log(result.message);
  // Handle unauthorized access
}

// Validate and throw if access denied
try {
  commissioningController.validateAccess(CommissioningState.ACTIVE);
  // Proceed with operation
} catch (error) {
  // Redirect to commissioning
}
```

### Get Status

```typescript
const status = commissioningController.getStatus();
console.log('Current state:', status.currentState);
console.log('Is commissioned:', status.isCommissioned);
console.log('Is operational:', status.isOperational);
```

### Get Commissioning Route

```typescript
// Get appropriate commissioning route for current state
const route = commissioningController.getCommissioningRoute();

// Routes:
// - /commissioning/welcome (NOT_COMMISSIONED)
// - /commissioning/setup (COMMISSIONING)
// - /commissioning/suspended (SUSPENDED)
// - /commissioning/status (default)
```

---

## API Reference

### Class: CommissioningController

#### Methods

##### `initialize(): Promise<void>`

Initialize the controller by loading persisted state from disk.

**Throws**: Error if initialization fails  
**Emits**: `initialized` event

##### `getState(): CommissioningState`

Get current commissioning state.

**Returns**: Current state  
**Throws**: Error if not initialized

##### `isCommissioned(): boolean`

Check if application is commissioned (state >= COMMISSIONED).

**Returns**: `true` if commissioned or beyond

##### `isOperational(): boolean`

Check if application is fully operational (state === ACTIVE).

**Returns**: `true` if active

##### `checkAccess(requiredState: CommissioningState): AccessCheckResult`

Check if operation is allowed in current state.

**Parameters**:
- `requiredState`: Minimum state required

**Returns**: `AccessCheckResult` with details

##### `validateAccess(requiredState: CommissioningState): void`

Validate access and throw if denied.

**Parameters**:
- `requiredState`: Minimum state required

**Throws**: Error with message if access denied

##### `getCommissioningRoute(): string`

Get commissioning flow route for current state.

**Returns**: Route path string

##### `getStatus(): StatusObject`

Get detailed status information.

**Returns**: Object with full status details

##### `getStateHistory(): StateTransitionEvent[]`

Get state transition history.

**Returns**: Array of transitions

---

## Events

The controller extends `EventEmitter` and emits:

### `initialized`

Emitted when controller successfully initializes.

**Payload**:
```typescript
{
  state: CommissioningState;
  timestamp: Date;
}
```

---

## Integration Points

### Router Guards

```typescript
// In Next.js middleware or router guard
export async function middleware(request: NextRequest) {
  await commissioningController.initialize();
  
  if (!commissioningController.isCommissioned()) {
    const route = commissioningController.getCommissioningRoute();
    return NextResponse.redirect(new URL(route, request.url));
  }
  
  return NextResponse.next();
}
```

### API Route Protection

```typescript
// In API route handler
export async function GET(request: Request) {
  commissioningController.validateAccess(CommissioningState.COMMISSIONED);
  
  // API logic here
}
```

---

## Constraints (F-A1)

Per issue requirements, this implementation:

✅ **DOES**:
- Provide commissioning state management
- Implement read-only state persistence
- Enforce access control logic
- Route invalid access to commissioning flow

❌ **DOES NOT** (yet):
- Include UI components
- Trigger automation
- Activate memory subsystem
- Implement state transitions (read-only)

---

## Future Extensions

The following will be implemented in subsequent issues:

- **UI**: Commissioning wizard and status pages
- **Write Operations**: State transition methods
- **Automation**: Automated commissioning workflows
- **Memory Integration**: Memory fabric activation on commission
- **Audit**: Full audit trail of commissioning events

---

## Governance

**Authority**: Issue F-A1  
**Architecture**: Architecture-only implementation  
**QA**: Unit tests in `tests/test_commissioning_controller.py`  
**Compliance**: Enforces operational boundaries per governance

---

## Files

```
lib/commissioning/
├── CommissioningController.ts   # Core controller implementation
├── index.ts                      # Module exports
└── README.md                     # This file

runtime/commissioning/
└── state.json                    # Persisted state (gitignored)

tests/
└── test_commissioning_controller.py  # Unit tests
```
