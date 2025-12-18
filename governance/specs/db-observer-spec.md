# DB Observer Specification

## Purpose

Define how Maturion/Foreman conceptually **observe** database behaviour without accessing raw tenant records.

The DB Observer focuses on:

- Structural health (migrations, indices)
- Performance (latency, contention, throughput)
- Anomalies (sudden spikes, timeouts, unusual patterns)

No business content or tenant information is exposed.

---

## 1. Observed Metrics

### 1.1 Structural

- Pending migrations count
- Failed migrations count
- Schema drift indicators (unexpected columns/tables vs canonical schemas)

### 1.2 Performance

- Read/write latency bands per module
- Connection pool utilisation
- Deadlock and lock-wait incidents

### 1.3 Reliability

- Transaction failure rates
- Retry counts
- Timeouts per module

---

## 2. Anomaly Categories

- **Performance Degradation**
- **Schema Drift**
- **Data Volume Surges**
- **High Error Density in Specific Module**

Each anomaly:

- Links to a **module** and **environment** (no tenant id)
- Is assigned a severity level (mapped to `watchdog-rules.json`)

---

## 3. Outputs

The DB Observer produces meta-events that follow the structure in:

- `foreman/runtime/behaviour-log-spec.md`
- `foreman/runtime/incident-detection-spec.md`

---

## 4. Integration

- **Risk Model** → `runtime-risk-model-spec.md`
- **Upgrade triggers** → `upgrade-insights-schema.json`
- **Compliance** → can tag any violations affecting data retention or integrity
