# FOREMAN_EVIDENCE_ARCHITECTURE_v1.0.md

## Version: 1.0  
## Date: 2025-12-15

---

## 1. EVIDENCE TYPES

### 1.1 Execution Evidence
- Program initiation records
- Wave start/completion records
- Task assignment records
- Task completion records

### 1.2 Governance Evidence
- Architecture validation reports
- QA execution results
- Governance violation logs
- Test debt detection logs

### 1.3 Provenance Evidence
- Actor identification (Foreman/Builder)
- Backend used (local/hosted/burst)
- Model used (GPT-4, etc.)
- Escalation rationale

### 1.4 Audit Evidence
- All state changes
- All decisions made
- All actions taken
- Timestamps for all events

---

## 2. EVIDENCE FORMATS

### 2.1 JSON Structured Evidence
```json
{
  "evidence_id": "uuid",
  "entity_type": "task",
  "entity_id": "uuid",
  "action": "task_completed",
  "actor": "ui-builder",
  "backend": "burst",
  "model": "GPT-4",
  "context": {
    "qa_results": {...},
    "validation_results": {...}
  },
  "timestamp": "ISO 8601"
}
```

### 2.2 Markdown Reports
- Architecture validation reports
- QA execution summaries
- Sprint completion reports

---

## 3. STORAGE LOCATIONS

- **Database**: evidence_trail table
- **File System**: /foreman/evidence/{program_id}/{wave_id}/{task_id}/
- **Memory Fabric**: Governance and execution memory

---

## 4. RETENTION POLICY

- Execution evidence: Permanent
- Governance evidence: Permanent
- Provenance evidence: Permanent
- Heartbeat logs: 90 days (then archive)

---

## 5. TRACEABILITY

### 5.1 Input → Output Traceability
- Task architecture → Task code
- QA suite → QA results
- Build instruction → Build output

### 5.2 Decision → Outcome Traceability
- Architecture validation decision → Task assignment
- QA validation decision → Task completion
- Stall detection → Recovery action

---

## 6. AUDIT REPLAY CAPABILITY

**Requirement**: System state must be reconstructable from evidence trail

**Implementation**:
1. Load all evidence for entity in chronological order
2. Replay state transitions
3. Verify final state matches recorded state

**Test**: Audit replay tested for all critical paths

---

## 7. EVIDENCE INTEGRITY

- Evidence stored in append-only tables
- Tampering detected via checksums (future)
- Evidence versioning: each change creates new record

---

## 8. COMPLIANCE EVIDENCE MAPPING

- ISO 27001: Architecture validation, QA results, governance logs
- NIST: Provenance tracking, audit trails
- COBIT: Decision traceability, evidence completeness

---

## 9. EVIDENCE EXPORT

**Formats Supported**:
- JSON (machine-readable)
- Markdown (human-readable)
- CSV (for analysis)

**Export API**:
- `GET /api/evidence/program/:id` - Export all program evidence
- `GET /api/evidence/task/:id` - Export task evidence

---

*Generated for Issue #2 - Architecture & QA Design (Wave 0 Completion)*
