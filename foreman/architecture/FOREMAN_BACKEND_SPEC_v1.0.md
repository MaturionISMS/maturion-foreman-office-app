# FOREMAN_BACKEND_SPEC_v1.0.md

## Johan's Foreman Office — Backend API & Business Logic Specification

**Version**: 1.0  
**Date**: 2025-12-15  
**Technology Stack**: Next.js 14 API Routes, PostgreSQL (Supabase), TypeScript

---

## 1. API ROUTES

### 1.1 Programs API

#### GET /api/programs

**Purpose**: List all programs  
**Authentication**: Required  
**Parameters**:
- `state` (optional): Filter by state (planned, in-progress, blocked, completed, failed)
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Items per page (default: 10, max: 100)

**Response**:
```typescript
{
  success: true,
  data: {
    programs: Program[],
    total: number,
    page: number,
    per_page: number
  }
}
```

#### GET /api/programs/active

**Purpose**: Get currently active program  
**Authentication**: Required  
**Response**:
```typescript
{
  success: true,
  data: {
    program: Program | null
  }
}
```

#### GET /api/programs/[id]

**Purpose**: Get program details  
**Authentication**: Required  
**Response**:
```typescript
{
  success: true,
  data: {
    program: Program,
    waves: Wave[],
    active_tasks: Task[],
    blockers: Blocker[]
  }
}
```

#### POST /api/programs

**Purpose**: Create new program  
**Authentication**: Required  
**Body**:
```typescript
{
  name: string,
  description: string,
  objectives: string[]
}
```
**Response**:
```typescript
{
  success: true,
  data: {
    program_id: string
  }
}
```

####POST /api/programs/[id]/approve

**Purpose**: Approve execution plan  
**Authentication**: Required (Johan only)  
**Body**:
```typescript
{
  comments?: string
}
```
**Response**:
```typescript
{
  success: true,
  message: "Plan approved - execution starting"
}
```

---

### 1.2 Waves API

#### GET /api/waves

**Purpose**: List waves  
**Authentication**: Required  
**Parameters**:
- `program_id` (required): Filter by program
- `state` (optional): Filter by state

**Response**:
```typescript
{
  success: true,
  data: {
    waves: Wave[]
  }
}
```

#### GET /api/waves/[id]

**Purpose**: Get wave details  
**Authentication**: Required  
**Response**:
```typescript
{
  success: true,
  data: {
    wave: Wave,
    tasks: Task[],
    dependencies: Wave[],
    progress: {
      total_tasks: number,
      completed_tasks: number,
      progress_percentage: number
    }
  }
}
```

---

### 1.3 Tasks API

#### GET /api/tasks

**Purpose**: List tasks  
**Authentication**: Required  
**Parameters**:
- `state` (optional): Filter by state
- `wave_id` (optional): Filter by wave
- `assigned_builder` (optional): Filter by builder
- `page`, `per_page`: Pagination

**Response**:
```typescript
{
  success: true,
  data: {
    tasks: Task[],
    total: number
  }
}
```

#### GET /api/tasks/running

**Purpose**: Get currently running tasks  
**Authentication**: Required  
**Response**:
```typescript
{
  success: true,
  data: {
    tasks: Task[]
  }
}
```

#### GET /api/tasks/[id]

**Purpose**: Get task details  
**Authentication**: Required  
**Response**:
```typescript
{
  success: true,
  data: {
    task: Task,
    wave: Wave,
    program: Program,
    builder_status: BuilderStatus,
    qa_history: QAExecution[],
    evidence_trail: EvidenceItem[]
  }
}
```

#### POST /api/tasks/[id]/complete

**Purpose**: Builder claims task completion  
**Authentication**: Required (Builder)  
**Body**:
```typescript
{
  builder_id: string,
  qa_results: {
    total_tests: number,
    passing_tests: number,
    failing_tests: number,
    skipped_tests: number
  },
  evidence_location: string
}
```
**Response**:
```typescript
{
  success: boolean,
  message: string,
  validation_results?: {
    qa_pass: boolean,
    test_debt: number,
    build_quality: boolean,
    evidence_complete: boolean
  }
}
```

---

### 1.4 Builders API

#### GET /api/builders

**Purpose**: Get all builders status  
**Authentication**: Required  
**Response**:
```typescript
{
  success: true,
  data: {
    builders: Builder[]
  }
}
```

#### GET /api/builders/[id]

**Purpose**: Get builder details  
**Authentication**: Required  
**Response**:
```typescript
{
  success: true,
  data: {
    builder: Builder,
    current_task: Task | null,
    recent_heartbeats: Heartbeat[],
    performance_metrics: {
      execution_continuity: number,
      average_task_duration: number,
      total_tasks_completed: number
    }
  }
}
```

#### POST /api/heartbeat

**Purpose**: Builder sends heartbeat  
**Authentication**: Required (Builder)  
**Body**:
```typescript
{
  builder_id: string,
  task_id: string | null,
  status: 'active' | 'idle' | 'blocked',
  message?: string,
  progress_percentage?: number
}
```
**Response**:
```typescript
{
  success: true,
  message: "Heartbeat received"
}
```

---

### 1.5 Blockers API

#### GET /api/blockers

**Purpose**: List blockers  
**Authentication**: Required  
**Parameters**:
- `resolved` (optional): Filter by resolution status (true/false)
- `entity_type` (optional): Filter by entity type
- `classification` (optional): Filter by classification

**Response**:
```typescript
{
  success: true,
  data: {
    blockers: Blocker[]
  }
}
```

#### GET /api/blockers/[id]

**Purpose**: Get blocker details  
**Authentication**: Required  
**Response**:
```typescript
{
  success: true,
  data: {
    blocker: Blocker,
    entity: Program | Wave | Task,
    diagnostics: {
      iterations_attempted: number,
      last_error_message: string,
      suggested_remediation: string
    }
  }
}
```

#### POST /api/blockers/[id]/resolve

**Purpose**: Resolve blocker  
**Authentication**: Required (Johan)  
**Body**:
```typescript
{
  resolution_action: string,
  notes: string
}
```
**Response**:
```typescript
{
  success: true,
  message: "Blocker resolved"
}
```

---

### 1.6 Evidence API

#### GET /api/evidence/program/[id]

**Purpose**: Export program evidence  
**Authentication**: Required  
**Parameters**:
- `format` (optional): json | markdown | csv

**Response**: Evidence file download

#### GET /api/evidence/task/[id]

**Purpose**: Export task evidence  
**Authentication**: Required  
**Parameters**:
- `format` (optional): json | markdown | csv

**Response**: Evidence file download

---

## 2. BUSINESS LOGIC FUNCTIONS

### 2.1 Planning Engine Functions

#### createProgram()

**Purpose**: Create new program from Johan's intent  
**Input**: `{ name, description, objectives }`  
**Process**:
1. Validate input
2. Create program record
3. Set state = "planned"
4. Create audit trail entry
5. Return program_id

**Output**: `{ program_id, state: "planned" }`

#### decomposeIntoWaves()

**Purpose**: Break program into waves  
**Input**: `{ program_id }`  
**Process**:
1. Load program
2. Analyze objectives
3. Identify logical groupings
4. Create wave records with sequence numbers
5. Define dependencies
6. Return wave list

**Output**: `{ waves: Wave[] }`

#### decomposeIntoTasks()

**Purpose**: Break wave into tasks  
**Input**: `{ wave_id }`  
**Process**:
1. Load wave
2. Identify components to build
3. Create task records
4. Assign architecture references
5. Assign QA suite locations
6. Return task list

**Output**: `{ tasks: Task[] }`

---

### 2.2 Governance Engine Functions

#### validateArchitecture()

**Purpose**: Execute Architecture Validation Pipeline  
**Input**: `{ architecture_reference }`  
**Process**:
1. Check document exists
2. Execute checklist validation (all 169 items)
3. Calculate pass rate
4. Determine build readiness
5. Create validation record
6. Return validation results

**Output**: `{ passed: boolean, pass_rate: number, build_readiness: "READY" | "NOT_READY" }`

#### validateQA()

**Purpose**: Execute QA Validation Pipeline  
**Input**: `{ qa_suite_location }`  
**Process**:
1. Check QA suite exists
2. Execute QA suite
3. Validate RED status (failing tests exist)
4. Detect test debt
5. Create validation record
6. Return validation results

**Output**: `{ passed: boolean, qa_status: "RED" | "PARTIAL" | "GREEN", test_debt_count: number }`

#### detectGovernanceViolation()

**Purpose**: Monitor for governance violations  
**Input**: `{ action, context }`  
**Process**:
1. Check against governance rules
2. Classify violation type
3. HALT current task if violation detected
4. Create blocker record
5. Log to governance memory
6. Escalate to Johan

**Output**: `{ violation_detected: boolean, violation_type?: string, blocker_id?: string }`

#### enforceZeroTestDebt()

**Purpose**: Reject task completion if test debt exists  
**Input**: `{ task_id, qa_results }`  
**Process**:
1. Check for failing tests
2. Check for skipped tests (.skip(), .todo())
3. Check for incomplete tests
4. If test_debt_count > 0, reject completion
5. Log quality integrity incident

**Output**: `{ passed: boolean, test_debt_count: number, test_debt_details: string[] }`

---

### 2.3 Orchestration Engine Functions

#### assignTask()

**Purpose**: Execute Task Assignment Pipeline  
**Input**: `{ task_id, builder_id }`  
**Process**:
1. Governance pre-check
2. Architecture validation
3. QA validation
4. Builder availability check
5. Update task.assigned_builder
6. Update task.state = "assigned"
7. Generate "Build to Green" instruction
8. Send to builder
9. Log to evidence trail

**Output**: `{ success: boolean, instruction: BuildToGreenInstruction }`

#### generateBuildToGreenInstruction()

**Purpose**: Create structured instruction for builder  
**Input**: `{ task_id }`  
**Process**:
1. Load task details
2. Load architecture document
3. Load QA suite
4. Format instruction per Builder Agent Contract
5. Return structured instruction

**Output**: `BuildToGreenInstruction`

---

### 2.4 Monitoring & Stall Detection Functions

#### trackHeartbeat()

**Purpose**: Record builder heartbeat  
**Input**: `{ builder_id, task_id, timestamp, status }`  
**Process**:
1. Update builder.last_heartbeat
2. Create heartbeat record
3. Update builder.state
4. Return confirmation

**Output**: `{ success: true }`

#### checkStallCondition()

**Purpose**: Detect builder stalls  
**Input**: `{ builder_id }`  
**Process**:
1. Get builder.last_heartbeat
2. Calculate time_since_heartbeat
3. If > 120 seconds, classify as stall
4. Determine stall type
5. Select recovery strategy
6. Execute recovery
7. Log to evidence trail

**Output**: `{ stall_detected: boolean, stall_type?: string, recovery_action?: string }`

#### classifyStall()

**Purpose**: Determine type of stall  
**Input**: `{ builder_id, task_state }`  
**Logic**:
```typescript
if (no_progress_for_3_iterations) {
  return "no_progress";
} else if (builder_waiting_for_input) {
  return "blocked_waiting";
} else {
  return "crashed";
}
```
**Output**: `StallType`

#### selectRecoveryStrategy()

**Purpose**: Choose recovery action  
**Input**: `{ stall_type, task_context }`  
**Logic**:
```typescript
if (stall_type === "no_progress" && attempts < 3) {
  return "restart_builder";
} else if (stall_type === "blocked_waiting") {
  return "escalate_to_johan";
} else {
  return "reassign_task";
}
```
**Output**: `RecoveryStrategy`

---

### 2.5 Evidence & Audit Trail Functions

#### logAction()

**Purpose**: Record action to evidence trail  
**Input**: `{ entity_type, entity_id, action, actor, context }`  
**Process**:
1. Create evidence_trail record
2. Include timestamp
3. Include provenance (actor, backend, model)
4. Store context as JSON
5. Return evidence_id

**Output**: `{ evidence_id }`

#### recordProvenance()

**Purpose**: Track who/what/when/why  
**Input**: `{ task_id, builder_id, model, escalation_rationale }`  
**Process**:
1. Create provenance record
2. Link to task
3. Store in evidence trail

**Output**: `{ success: true }`

#### generateEvidenceTrail()

**Purpose**: Create complete evidence trail for entity  
**Input**: `{ entity_type, entity_id }`  
**Process**:
1. Query evidence_trail table
2. Order by timestamp
3. Format as timeline
4. Return evidence items

**Output**: `{ evidence_items: EvidenceItem[] }`

---

### 2.6 Provenance Tracking Functions

#### recordActor()

**Purpose**: Record who performed action  
**Input**: `{ action_id, actor }`  
**Process**: Store actor (Foreman or Builder ID)

#### recordBackend()

**Purpose**: Record which backend was used  
**Input**: `{ action_id, backend }`  
**Process**: Store backend (local/hosted/burst)

#### recordModel()

**Purpose**: Record which AI model was used  
**Input**: `{ action_id, model }`  
**Process**: Store model (GPT-4, Claude, etc.)

#### recordEscalation()

**Purpose**: Record escalation rationale  
**Input**: `{ action_id, rationale }`  
**Process**: Store why escalation occurred

---

## 3. BUSINESS RULES IMPLEMENTATION

### 3.1 BR-1: Architecture Completeness Rule

```typescript
async function enforceArchitectureCompleteness(task_id: string): Promise<boolean> {
  const task = await getTask(task_id);
  const validation = await validateArchitecture(task.architecture_reference);
  
  if (validation.pass_rate < 100) {
    await createBlocker({
      entity_type: 'task',
      entity_id: task_id,
      classification: 'architecture_incomplete',
      description: `Architecture validation failed: ${validation.pass_rate}% pass rate`
    });
    return false;
  }
  
  return true;
}
```

### 3.2 BR-2: QA Completeness Rule

```typescript
async function enforceQACompleteness(task_id: string): Promise<boolean> {
  const task = await getTask(task_id);
  const qa_validation = await validateQA(task.qa_suite_location);
  
  if (!qa_validation.qa_suite_exists) {
    await createBlocker({
      entity_type: 'task',
      entity_id: task_id,
      classification: 'qa_missing',
      description: 'QA suite does not exist'
    });
    return false;
  }
  
  if (qa_validation.qa_status !== 'RED') {
    await createBlocker({
      entity_type: 'task',
      entity_id: task_id,
      classification: 'qa_not_red',
      description: 'QA must be RED before build starts'
    });
    return false;
  }
  
  return true;
}
```

### 3.3 BR-3: Zero Test Debt Rule

```typescript
async function enforceZeroTestDebt(task_id: string, qa_results: QAResults): Promise<boolean> {
  const test_debt = await detectTestDebt(task_id);
  
  if (test_debt.count > 0) {
    await logQualityIntegrityIncident({
      task_id,
      incident_type: 'test_debt_detected',
      details: test_debt.items
    });
    
    await createBlocker({
      entity_type: 'task',
      entity_id: task_id,
      classification: 'test_debt',
      description: `Test debt detected: ${test_debt.count} items`
    });
    
    return false;
  }
  
  return true;
}
```

### 3.4 BR-4: Governance Supremacy Rule (GSR)

```typescript
async function enforceGSR(action: string, context: any): Promise<void> {
  const violation = await detectGovernanceViolation(action, context);
  
  if (violation.detected) {
    // HALT immediately
    await haltTask(context.task_id);
    
    // Create blocker
    await createBlocker({
      entity_type: 'task',
      entity_id: context.task_id,
      classification: 'constitutional_violation',
      description: violation.description
    });
    
    // Log to governance memory
    await logGovernanceViolation(violation);
    
    // Escalate to Johan
    await notifyJohan({
      type: 'governance_violation',
      violation: violation
    });
    
    throw new Error('Governance violation detected - execution halted');
  }
}
```

### 3.5 BR-5: Heartbeat Monitoring Rule

```typescript
async function enforceHeartbeatMonitoring(): Promise<void> {
  const builders = await getActiveBuilders();
  
  for (const builder of builders) {
    const time_since_heartbeat = Date.now() - builder.last_heartbeat.getTime();
    
    if (time_since_heartbeat > 120000) { // 120 seconds
      // Stall detected
      await setBuilderState(builder.builder_id, 'failed');
      
      if (builder.current_task_id) {
        await setTaskState(builder.current_task_id, 'blocked');
        
        await createBlocker({
          entity_type: 'task',
          entity_id: builder.current_task_id,
          classification: 'builder_stall',
          description: `Builder ${builder.builder_id} stalled - no heartbeat for ${time_since_heartbeat/1000}s`
        });
        
        // Trigger recovery workflow
        await executeStallRecovery(builder.builder_id, builder.current_task_id);
      }
    }
  }
}
```

### 3.6 BR-6: Wave Dependency Rule

```typescript
async function enforceWaveDependencies(wave_id: string): Promise<boolean> {
  const wave = await getWave(wave_id);
  const dependencies = await getWaveDependencies(wave.dependencies);
  
  for (const dep of dependencies) {
    if (dep.state !== 'completed') {
      return false;
    }
  }
  
  return true;
}
```

### 3.7 BR-7: Progress Calculation Rule

```typescript
async function calculateProgress() {
  // Task progress = (completed_steps / total_steps) * 100
  // This is determined by builder based on test pass rate
  
  // Wave progress = AVG(task progress)
  const waves = await getWaves();
  for (const wave of waves) {
    const tasks = await getTasksByWave(wave.wave_id);
    const avg_progress = tasks.reduce((sum, t) => sum + t.progress_percentage, 0) / tasks.length;
    await updateWaveProgress(wave.wave_id, Math.round(avg_progress));
  }
  
  // Program progress = WEIGHTED_AVG(wave progress)
  const programs = await getPrograms();
  for (const program of programs) {
    const waves = await getWavesByProgram(program.program_id);
    const total_weight = waves.length;
    const weighted_sum = waves.reduce((sum, w) => sum + w.progress_percentage, 0);
    const weighted_avg = weighted_sum / total_weight;
    await updateProgramProgress(program.program_id, Math.round(weighted_avg));
  }
}
```

---

## 4. VALIDATION RULES

### 4.1 Architecture Validation

```typescript
async function validateArchitectureDocument(arch_ref: string): Promise<ValidationResult> {
  // Check existence
  if (!await fileExists(arch_ref)) {
    return { passed: false, reason: 'Architecture document not found' };
  }
  
  // Execute checklist
  const checklist_results = await executeChecklist(arch_ref);
  const pass_rate = (checklist_results.passed / checklist_results.total) * 100;
  
  // Determine readiness
  const build_readiness = pass_rate === 100 ? 'READY' : 'NOT_READY';
  
  return {
    passed: pass_rate === 100,
    pass_rate,
    build_readiness,
    details: checklist_results
  };
}
```

### 4.2 QA Validation

```typescript
async function validateQASuite(qa_location: string): Promise<ValidationResult> {
  // Check existence
  if (!await directoryExists(qa_location)) {
    return { passed: false, reason: 'QA suite not found' };
  }
  
  // Execute QA
  const qa_results = await executeQASuite(qa_location);
  
  // Check RED status
  if (qa_results.failing_tests === 0) {
    return { passed: false, reason: 'QA must be RED (have failing tests) before build' };
  }
  
  // Check for test debt
  const test_debt = await detectTestDebt(qa_location);
  if (test_debt.count > 0) {
    return { passed: false, reason: `Test debt detected: ${test_debt.count} items` };
  }
  
  return {
    passed: true,
    qa_status: 'RED',
    test_debt_count: 0
  };
}
```

---

## 5. ERROR HANDLING

### 5.1 Database Errors

```typescript
try {
  const result = await db.query(...);
} catch (error) {
  if (error.code === 'CONNECTION_ERROR') {
    // Retry with exponential backoff
    await retryWithBackoff(operation, { maxRetries: 3 });
  } else if (error.code === 'CONSTRAINT_VIOLATION') {
    // Return user-friendly error
    return { success: false, error: 'Data validation failed' };
  } else {
    // Log error and return generic message
    await logError(error);
    return { success: false, error: 'An unexpected error occurred' };
  }
}
```

### 5.2 GitHub API Errors

```typescript
try {
  const response = await githubAPI.get(...);
} catch (error) {
  if (error.status === 429) {
    // Rate limit exceeded - queue and throttle
    await queueRequest(request);
    await throttleRequests();
  } else if (error.status === 503) {
    // Service unavailable - retry later
    await scheduleRetry(request, { delay: 60000 });
  } else {
    // Fallback to local cache if available
    const cached = await getFromCache(request);
    return cached || { success: false, error: 'GitHub API unavailable' };
  }
}
```

### 5.3 Builder Backend Errors

```typescript
try {
  const response = await builderBackend.execute(instruction);
} catch (error) {
  if (error.code === 'BACKEND_UNAVAILABLE') {
    // Try alternate backend
    const alternate = await selectAlternateBackend();
    return await alternate.execute(instruction);
  } else if (error.code === 'EXECUTION_TIMEOUT') {
    // Escalate to stall detection
    await handleStall(builder_id);
  } else {
    // Log and escalate
    await logError(error);
    await escalateToJohan({ type: 'builder_error', error });
  }
}
```

---

## 6. AUTHENTICATION & AUTHORIZATION

### 6.1 Authentication

```typescript
// JWT-based authentication
async function authenticate(request: Request): Promise<User | null> {
  const token = request.headers.get('Authorization')?.replace('Bearer ', '');
  
  if (!token) {
    return null;
  }
  
  try {
    const payload = await verifyJWT(token);
    const user = await getUserById(payload.user_id);
    return user;
  } catch {
    return null;
  }
}
```

### 6.2 Authorization

```typescript
// Role-based access control
async function authorize(user: User, action: string, resource: string): Promise<boolean> {
  if (user.role === 'governor') {
    // Johan has full access
    return true;
  }
  
  if (user.role === 'builder') {
    // Builders can only access assigned tasks
    if (action === 'read' && resource.startsWith('tasks/')) {
      const task = await getTask(resource);
      return task.assigned_builder === user.builder_id;
    }
    
    if (action === 'write' && resource.startsWith('heartbeat')) {
      return true;
    }
    
    return false;
  }
  
  return false;
}
```

---

## 7. RATE LIMITING

```typescript
// Rate limit external API calls
const rateLimiter = new RateLimiter({
  github: { max: 5000, window: 3600000 }, // 5000 requests per hour
  builder_backends: { max: 100, window: 60000 }, // 100 requests per minute
});

async function executeWithRateLimit(api: string, fn: () => Promise<any>) {
  if (await rateLimiter.isAllowed(api)) {
    return await fn();
  } else {
    // Queue request
    await rateLimiter.queue(api, fn);
    throw new Error('Rate limit exceeded - request queued');
  }
}
```

---

## 8. CACHING STRATEGY

```typescript
// Cache frequently accessed data
const cache = {
  programs: new TTLCache({ ttl: 30000 }), // 30 seconds
  tasks: new TTLCache({ ttl: 10000 }),    // 10 seconds
  builders: new TTLCache({ ttl: 5000 }),  // 5 seconds
};

async function getCachedProgram(id: string): Promise<Program> {
  const cached = cache.programs.get(id);
  if (cached) {
    return cached;
  }
  
  const program = await db.getProgram(id);
  cache.programs.set(id, program);
  return program;
}
```

---

## 9. PERFORMANCE CONSIDERATIONS

### 9.1 Database Query Optimization

- Use indexes on frequently queried columns (state, timestamps, foreign keys)
- Batch queries where possible
- Use pagination for large result sets
- Implement database connection pooling

### 9.2 API Response Optimization

- Return only necessary data fields
- Implement field selection (GraphQL-style)
- Use gzip compression for large responses
- Implement ETag caching for static resources

### 9.3 Background Jobs

```typescript
// Use cron jobs for periodic tasks
// Run every minute
cron.schedule('*/1 * * * *', async () => {
  await checkStallConditions();
  await calculateProgress();
  await cleanupOldHeartbeats();
});
```

---

*Generated for Issue #2 - Architecture & QA Design (Wave 0 Completion)*
