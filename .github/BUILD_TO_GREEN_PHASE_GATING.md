# Build-to-Green Phase Gating

**Purpose**: Control when Build-to-Green enforcement runs based on the current build wave.

---

## How It Works

The Build-to-Green workflow checks `.github/build-wave-phase.json` to determine if enforcement should run.

### Phase Configuration File

**Location**: `.github/build-wave-phase.json`

**Structure**:
```json
{
  "current_wave": "2.5B",
  "wave_name": "Governance Normalization",
  "build_to_green_enabled": false,
  "description": "Wave 2.5B - Governance normalization phase. Build-to-Green enforcement paused.",
  "updated_at": "2025-12-18T15:00:00Z",
  "notes": "Build-to-Green enforcement will be re-enabled in Wave 3"
}
```

### Fields

- **`current_wave`**: Current wave identifier (e.g., "2.5B", "3")
- **`wave_name`**: Human-readable wave name
- **`build_to_green_enabled`**: Boolean flag controlling enforcement
- **`description`**: Explanation of the current wave
- **`updated_at`**: ISO timestamp of last update
- **`notes`**: Additional context or instructions

---

## Workflow Behavior

### When `build_to_green_enabled` is `true`:
- Full Build-to-Green enforcement runs
- Tests are executed
- Test dodging is checked
- DP-RED validation occurs
- Success/failure comments posted to PR

### When `build_to_green_enabled` is `false`:
- All enforcement steps are skipped
- A comment is posted explaining the pause
- No tests run, no validation occurs
- Workflow completes successfully

---

## Enabling/Disabling Enforcement

### To Pause Enforcement (e.g., during governance work):

Edit `.github/build-wave-phase.json`:
```json
{
  "current_wave": "2.5B",
  "wave_name": "Governance Normalization",
  "build_to_green_enabled": false,
  "description": "Wave 2.5B - Governance normalization phase. Build-to-Green enforcement paused.",
  "updated_at": "2025-12-18T15:00:00Z",
  "notes": "Build-to-Green enforcement will be re-enabled in Wave 3"
}
```

### To Re-enable Enforcement:

Edit `.github/build-wave-phase.json`:
```json
{
  "current_wave": "3",
  "wave_name": "Build-to-Green Active",
  "build_to_green_enabled": true,
  "description": "Wave 3 - Full Build-to-Green enforcement active.",
  "updated_at": "2025-12-20T00:00:00Z",
  "notes": "All PRs must pass Build-to-Green checks"
}
```

---

## Use Cases

### Wave 2.5B - Governance Normalization
**Status**: Enforcement PAUSED  
**Reason**: Structural changes to governance artefacts don't require test validation  
**Duration**: Until governance reorganization is complete

### Wave 3 - Build-to-Green Active
**Status**: Enforcement ENABLED  
**Reason**: All code changes must pass tests and governance checks  
**Duration**: Ongoing for all feature development

---

## Troubleshooting

### Workflow fails with "Phase file not found"
- The phase file is optional
- If missing, enforcement defaults to **enabled**
- Create `.github/build-wave-phase.json` to control behavior

### Enforcement runs when it should be paused
- Check that `build_to_green_enabled` is set to `false` (not "false" string)
- Verify the phase file is committed to the branch
- Check workflow logs for phase detection output

### PR comments not appearing
- Ensure `build_to_green_enabled` matches expected state
- Check GitHub Actions permissions (pull-requests: write)
- Review workflow run logs in GitHub Actions tab

---

## Governance Rules

1. **Phase file changes require approval**: Updates to wave phase must be deliberate
2. **Document wave transitions**: Update `notes` field when changing waves
3. **Coordinate across repos**: All repos should be in sync on wave transitions
4. **Never bypass for convenience**: Only disable during legitimate governance phases

---

## Example Workflow Output

### When Paused:
```
⏸️ Build-to-Green Enforcement PAUSED

Current Wave: 2.5B - Governance Normalization

Build-to-Green enforcement is intentionally disabled during this phase.

Reason: Wave 2.5B - Governance normalization phase. Build-to-Green enforcement paused.

Enforcement will be re-enabled in Wave 3.
```

### When Active:
```
✅ Build-to-Green Check Completed

- No test dodging detected
- Test suite executed
- DP-RED handled according to governance rules
```

---

## Related Files

- `.github/workflows/build-to-green-enforcement.yml` - The workflow that checks phase
- `foreman/qa/current-phase.json` - QA phase tracking (separate from wave phase)
- `BUILD_PHILOSOPHY.md` - Build-to-Green doctrine

---

*Phase gating implemented: 2025-12-18*  
*Current phase: Wave 2.5B - Governance Normalization*
