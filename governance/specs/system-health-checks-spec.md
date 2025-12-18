# System Health Checks Specification

## Purpose

Define the **standard health checks** Foreman expects Maturion to run across:

- Platform-level services
- Module boundaries
- AI subsystems
- Integrations

---

## 1. Health Check Categories

1. **Core Platform**
   - Uptime per service
   - Error rates
   - Latency SLOs

2. **Module-Specific**
   - Key workflows (e.g., risk assessment creation, WRAC submission)
   - Expected integration flows

3. **AI Health**
   - Model availability
   - Routing success rate
   - Safety engine availability

4. **Integration Health**
   - Edge functions
   - External connectors
   - Internal module calls

---

## 2. Health Check States

- `HEALTHY`
- `DEGRADED`
- `UNSTABLE`
- `DOWN`

Each health check must include:

- `module_id`
- `check_id`
- `environment_id`
- `state`
- `timestamp`
- `summary`

---

## 3. Output Format

Health check results are aggregated into the behaviour log format defined in:

- `foreman/runtime/behaviour-log-spec.md`

They also contribute to the **runtime export** (see `upgrade/runtime-export-spec.md`).

---

## 4. QA Expectations

- Health checks must run on a predictable schedule.
- Test environment must validate health checks before production rollout.
- Failures with severity `UNSTABLE` or above must link to at least one risk entry in `runtime-risk-model-spec.md`.
