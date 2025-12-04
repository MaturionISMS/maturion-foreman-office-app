# TimescaleDB Strategy – Maturion ISMS

**Version**: 1.0  
**Date**: 2025-12-04  
**Status**: Active  
**Build Wave**: 1.2

---

## 1. Purpose

This document defines the **TimescaleDB time-series strategy** for the Maturion ISMS platform.

TimescaleDB is used for:
- Audit logs (immutable event tracking)
- System event logs (cross-module events)
- Performance metrics
- Security monitoring
- Compliance reporting
- Analytics and dashboards

---

## 2. What is TimescaleDB?

**TimescaleDB** is a PostgreSQL extension that adds time-series capabilities:
- Automatic partitioning by time (hypertables)
- High-performance time-range queries
- Continuous aggregates (materialized views with auto-refresh)
- Data retention policies
- Compression for historical data
- Full SQL compatibility (it's still PostgreSQL)

**Why TimescaleDB?**
- ✅ Native PostgreSQL extension (no separate database)
- ✅ SQL queries work as normal
- ✅ Automatic time-based partitioning
- ✅ 10-100x better performance for time-series queries
- ✅ Automatic data retention and compression
- ✅ Perfect for audit logs and event logs

---

## 3. Installation and Setup

### 3.1 Install Extension

```sql
-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;
```

### 3.2 Verify Installation

```sql
-- Check TimescaleDB version
SELECT default_version, installed_version
FROM pg_available_extensions
WHERE name = 'timescaledb';
```

---

## 4. Hypertables (Time-Series Tables)

### 4.1 What is a Hypertable?

A **hypertable** is a virtual table that looks like a normal table but is automatically partitioned by time.

**Regular table**:
- All data in single table
- Slow for large time-range queries
- No automatic retention

**Hypertable**:
- Automatically partitioned by time (chunks)
- Fast time-range queries (only scan relevant chunks)
- Automatic retention policies
- Automatic compression

### 4.2 Creating a Hypertable

```sql
-- Step 1: Create regular table
CREATE TABLE audit_log (
  id UUID PRIMARY KEY DEFAULT generate_uuidv7(),
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  user_id UUID REFERENCES users(id),
  module TEXT NOT NULL,
  entity_type TEXT NOT NULL,
  entity_id UUID NOT NULL,
  action TEXT NOT NULL,
  changes JSONB,
  ip_address INET,
  user_agent TEXT
);

-- Step 2: Convert to hypertable
SELECT create_hypertable('audit_log', 'timestamp');
```

**Key points**:
- Partition key MUST be a timestamp column (`TIMESTAMPTZ` recommended)
- Partition key MUST be `NOT NULL`
- Primary key MUST include partition key (if defined)

### 4.3 Hypertable with Composite Primary Key

```sql
-- Table with composite primary key (id + timestamp)
CREATE TABLE event_log (
  id UUID NOT NULL,
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  event_type TEXT NOT NULL,
  payload JSONB,
  PRIMARY KEY (timestamp, id) -- timestamp must be first!
);

-- Convert to hypertable
SELECT create_hypertable('event_log', 'timestamp');
```

---

## 5. Audit Log (Hypertable)

### 5.1 Audit Log Schema

```sql
CREATE TABLE audit_log (
  id UUID NOT NULL, -- Part of composite primary key defined below
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  
  -- Timestamp (PARTITION KEY)
  timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  
  -- User context
  user_id UUID REFERENCES users(id),
  user_email TEXT,
  user_role TEXT,
  
  -- Module context
  module TEXT NOT NULL,
  entity_type TEXT NOT NULL,
  entity_id UUID NOT NULL,
  
  -- Action performed
  action TEXT NOT NULL, -- 'created', 'updated', 'deleted', 'viewed', 'exported'
  
  -- Change details
  changes JSONB, -- Before/after values for updates
  
  -- Request context
  ip_address INET,
  user_agent TEXT,
  request_id UUID,
  
  -- Compliance metadata
  retention_until TIMESTAMPTZ,
  is_legally_protected BOOLEAN DEFAULT FALSE,
  
  -- Composite primary key (timestamp + id)
  PRIMARY KEY (timestamp, id)
);

-- Convert to hypertable (7-day chunks)
SELECT create_hypertable(
  'audit_log', 
  'timestamp',
  chunk_time_interval => INTERVAL '7 days'
);
```

### 5.2 Audit Log Indexes

```sql
-- Organisation + timestamp (most common query)
CREATE INDEX idx_audit_log_org_time 
  ON audit_log(organisation_id, timestamp DESC);

-- Entity lookup
CREATE INDEX idx_audit_log_entity 
  ON audit_log(organisation_id, entity_type, entity_id);

-- User activity
CREATE INDEX idx_audit_log_user 
  ON audit_log(organisation_id, user_id, timestamp DESC);

-- Module + action
CREATE INDEX idx_audit_log_module 
  ON audit_log(organisation_id, module, action);
```

---

## 6. Event Log (Hypertable)

### 6.1 Event Log Schema

```sql
CREATE TABLE event_log (
  id UUID NOT NULL,
  organisation_id UUID NOT NULL REFERENCES organisations(id),
  
  -- Timestamp (PARTITION KEY)
  timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  
  -- Event details
  event_type TEXT NOT NULL,
  source_module TEXT NOT NULL,
  source_entity_type TEXT,
  source_entity_id UUID,
  
  -- Target (for cross-module events)
  target_module TEXT,
  target_entity_type TEXT,
  target_entity_id UUID,
  
  -- Payload
  payload JSONB,
  
  -- Processing status
  processed_at TIMESTAMPTZ,
  processing_error TEXT,
  retry_count INTEGER DEFAULT 0,
  
  -- Composite primary key
  PRIMARY KEY (timestamp, id)
);

-- Convert to hypertable (1-day chunks)
SELECT create_hypertable(
  'event_log',
  'timestamp',
  chunk_time_interval => INTERVAL '1 day'
);
```

### 6.2 Event Log Indexes

```sql
CREATE INDEX idx_event_log_org_time 
  ON event_log(organisation_id, timestamp DESC);

CREATE INDEX idx_event_log_type 
  ON event_log(organisation_id, event_type);

CREATE INDEX idx_event_log_source 
  ON event_log(organisation_id, source_module, source_entity_id);

CREATE INDEX idx_event_log_unprocessed 
  ON event_log(organisation_id, timestamp)
  WHERE processed_at IS NULL;
```

---

## 7. Data Retention Policies

### 7.1 Automatic Retention

**Drop old data automatically after retention period**:

```sql
-- Retain audit logs for 7 years (ISO 27001, GDPR compliance)
SELECT add_retention_policy('audit_log', INTERVAL '7 years');

-- Retain event logs for 90 days
SELECT add_retention_policy('event_log', INTERVAL '90 days');
```

### 7.2 Legal Hold Override

**Prevent deletion of legally protected data**:

```sql
-- Mark audit log entry as legally protected
UPDATE audit_log
SET is_legally_protected = TRUE,
    retention_until = NULL -- Never expire
WHERE entity_id = :entity_id
  AND organisation_id = :org_id;
```

### 7.3 Retention Policy with Exceptions

```sql
-- Custom retention: Delete unless legally protected
DELETE FROM audit_log
WHERE timestamp < NOW() - INTERVAL '7 years'
  AND is_legally_protected = FALSE;
```

---

## 8. Compression

### 8.1 Automatic Compression

**Compress old chunks to save 90% storage**:

```sql
-- Enable compression on chunks older than 30 days
SELECT add_compression_policy('audit_log', INTERVAL '30 days');

-- Enable compression on chunks older than 7 days
SELECT add_compression_policy('event_log', INTERVAL '7 days');
```

### 8.2 Compression Settings

```sql
-- Set compression algorithm and level
ALTER TABLE audit_log SET (
  timescaledb.compress,
  timescaledb.compress_segmentby = 'organisation_id',
  timescaledb.compress_orderby = 'timestamp DESC'
);

ALTER TABLE event_log SET (
  timescaledb.compress,
  timescaledb.compress_segmentby = 'organisation_id',
  timescaledb.compress_orderby = 'timestamp DESC'
);
```

**Compression options**:
- `compress_segmentby`: Group similar data together (e.g., by `organisation_id`)
- `compress_orderby`: Sort order within compressed segments

### 8.3 Manual Compression

```sql
-- Compress specific chunk
SELECT compress_chunk('_timescaledb_internal._hyper_1_1_chunk');

-- Compress all chunks older than 30 days
SELECT compress_chunk(chunk)
FROM timescaledb_information.chunks
WHERE hypertable_name = 'audit_log'
  AND range_end < NOW() - INTERVAL '30 days';
```

---

## 9. Continuous Aggregates

### 9.1 What are Continuous Aggregates?

**Continuous aggregates** are materialized views that auto-refresh:
- Pre-compute aggregations (COUNT, SUM, AVG, etc.)
- Automatically update when new data arrives
- Much faster than real-time aggregation queries
- Perfect for dashboards and reports

### 9.2 Example: Daily Audit Summary

```sql
CREATE MATERIALIZED VIEW audit_log_daily
WITH (timescaledb.continuous) AS
SELECT 
  organisation_id,
  time_bucket('1 day', timestamp) AS day,
  COUNT(*) AS total_events,
  COUNT(DISTINCT user_id) AS active_users,
  COUNT(*) FILTER (WHERE action = 'created') AS creates,
  COUNT(*) FILTER (WHERE action = 'updated') AS updates,
  COUNT(*) FILTER (WHERE action = 'deleted') AS deletes
FROM audit_log
GROUP BY organisation_id, time_bucket('1 day', timestamp);
```

### 9.3 Refresh Policy

```sql
-- Refresh every hour
SELECT add_continuous_aggregate_policy(
  'audit_log_daily',
  start_offset => INTERVAL '3 days',
  end_offset => INTERVAL '1 hour',
  schedule_interval => INTERVAL '1 hour'
);
```

### 9.4 Query Continuous Aggregate

```sql
-- Get daily audit summary for last 30 days
SELECT 
  day,
  total_events,
  active_users
FROM audit_log_daily
WHERE organisation_id = :org_id
  AND day >= NOW() - INTERVAL '30 days'
ORDER BY day DESC;
```

---

## 10. Query Patterns

### 10.1 Time-Range Queries

```sql
-- Get recent audit logs (fast!)
SELECT * FROM audit_log
WHERE organisation_id = :org_id
  AND timestamp >= NOW() - INTERVAL '7 days'
ORDER BY timestamp DESC
LIMIT 100;
```

### 10.2 Entity History

```sql
-- Get history of a specific entity
SELECT 
  timestamp,
  action,
  user_email,
  changes
FROM audit_log
WHERE organisation_id = :org_id
  AND entity_type = 'risk'
  AND entity_id = :risk_id
ORDER BY timestamp DESC;
```

### 10.3 User Activity

```sql
-- Get user's recent activity
SELECT 
  timestamp,
  module,
  entity_type,
  action
FROM audit_log
WHERE organisation_id = :org_id
  AND user_id = :user_id
  AND timestamp >= NOW() - INTERVAL '30 days'
ORDER BY timestamp DESC
LIMIT 100;
```

### 10.4 Aggregations with time_bucket

```sql
-- Hourly event counts for last 24 hours
SELECT 
  time_bucket('1 hour', timestamp) AS hour,
  COUNT(*) AS event_count
FROM audit_log
WHERE organisation_id = :org_id
  AND timestamp >= NOW() - INTERVAL '24 hours'
GROUP BY hour
ORDER BY hour DESC;
```

---

## 11. Performance Optimization

### 11.1 Chunk Sizing

**Chunk interval** determines partition size:
- Too small: Too many chunks (high metadata overhead)
- Too large: Inefficient time-range queries

**Recommendations**:
- High-volume logs (audit_log): 7 days
- Medium-volume logs (event_log): 1 day
- Low-volume logs: 1 month

```sql
-- Change chunk interval
SELECT set_chunk_time_interval('audit_log', INTERVAL '7 days');
```

### 11.2 Partitioning by Space

**Partition by space AND time** for multi-tenant deployments:

```sql
SELECT create_hypertable(
  'audit_log',
  'timestamp',
  partitioning_column => 'organisation_id',
  number_partitions => 4 -- Hash partition by org_id
);
```

### 11.3 Index Strategies

- ✅ Index on `(organisation_id, timestamp)` for tenant queries
- ✅ Index on entity columns for lookups
- ✅ Avoid too many indexes (slows down inserts)

---

## 12. Monitoring

### 12.1 Chunk Information

```sql
-- List all chunks
SELECT 
  hypertable_name,
  chunk_name,
  range_start,
  range_end,
  total_bytes,
  compressed_total_bytes
FROM timescaledb_information.chunks
WHERE hypertable_name = 'audit_log'
ORDER BY range_start DESC;
```

### 12.2 Compression Stats

```sql
-- Compression savings
SELECT 
  hypertable_name,
  SUM(total_bytes) AS uncompressed_bytes,
  SUM(compressed_total_bytes) AS compressed_bytes,
  ROUND(100.0 * SUM(compressed_total_bytes) / SUM(total_bytes), 2) AS compression_ratio
FROM timescaledb_information.chunks
GROUP BY hypertable_name;
```

### 12.3 Query Performance

```sql
-- Analyze query performance
EXPLAIN ANALYZE
SELECT * FROM audit_log
WHERE organisation_id = :org_id
  AND timestamp >= NOW() - INTERVAL '7 days';
```

---

## 13. Backup and Restore

### 13.1 Logical Backup (pg_dump)

```bash
# Backup entire database (includes TimescaleDB metadata)
pg_dump -Fc maturion_isms > backup.dump

# Restore
pg_restore -d maturion_isms backup.dump
```

### 13.2 Point-in-Time Recovery (PITR)

TimescaleDB supports standard PostgreSQL PITR:
- WAL archiving
- Base backups
- Restore to specific timestamp

---

## 14. Conclusion

The TimescaleDB strategy for Maturion ISMS ensures:

- ✅ High-performance time-series queries
- ✅ Automatic data retention and cleanup
- ✅ 90% storage savings with compression
- ✅ Fast dashboard queries with continuous aggregates
- ✅ Full SQL compatibility
- ✅ Compliance with ISO 27001, GDPR, POPIA

**Use TimescaleDB for:**
- `audit_log` (immutable audit trail)
- `event_log` (cross-module events)
- Any time-series data (metrics, logs, events)

---

**Prepared by**: Maturion Foreman  
**Build Wave**: 1.2  
**Date**: 2025-12-04
