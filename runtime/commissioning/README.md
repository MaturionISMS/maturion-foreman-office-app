# Commissioning State Reference

This directory contains runtime commissioning state managed by the `CommissioningController`.

## File Structure

- `state.json` - Current commissioning state (gitignored, runtime only)

## State File Format

```json
{
  "state": "NOT_COMMISSIONED",
  "commissioned_at": "2025-12-29T05:00:00Z",
  "commissioned_by": "admin",
  "last_updated": "2025-12-29T05:00:00Z",
  "version": "1.0.0",
  "metadata": {
    "reason": "Initial setup",
    "notes": "Additional context"
  }
}
```

## States

- `NOT_COMMISSIONED` - Initial state
- `COMMISSIONING` - Setup in progress
- `COMMISSIONED` - Basic ops permitted
- `ACTIVE` - Fully operational
- `SUSPENDED` - Temporarily paused

## Managed By

`lib/commissioning/CommissioningController.ts`
