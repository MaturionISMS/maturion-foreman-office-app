# FOREMAN_FRONTEND_SPEC_v1.0.md

## Johan's Foreman Office — Frontend Component Specification

**Version**: 1.0  
**Date**: 2025-12-15  
**Technology Stack**: Next.js 14, React 18, TypeScript, Tailwind CSS, shadcn/ui

---

## 1. ROUTE STRUCTURE

### 1.1 File-Based Routing (Next.js App Router)

```
/app/foreman/
  /page.tsx                         # Dashboard (home page)
  /layout.tsx                       # Root layout with navigation
  /loading.tsx                      # Loading state
  /error.tsx                        # Error boundary
  
  /programs/
    /page.tsx                       # Programs list
    /[programId]/
      /page.tsx                     # Program detail view
      /edit/page.tsx                # Edit program
      /plan/page.tsx                # View execution plan
      /evidence/page.tsx            # Evidence trail
  
  /tasks/
    /page.tsx                       # All tasks list
    /[taskId]/
      /page.tsx                     # Task detail view
      /evidence/page.tsx            # Task evidence trail
  
  /blockers/
    /page.tsx                       # Blockers list
    /[blockerId]/page.tsx           # Blocker detail
  
  /builders/
    /page.tsx                       # Builders status
    /[builderId]/
      /page.tsx                     # Builder detail
      /logs/page.tsx                # Builder logs
  
  /settings/
    /page.tsx                       # Settings page
  
  /api/                             # API routes
    /programs/route.ts              # Programs API
    /tasks/route.ts                 # Tasks API
    /builders/route.ts              # Builders API
    /blockers/route.ts              # Blockers API
    /heartbeat/route.ts             # Heartbeat endpoint
```

---

## 2. COMPONENT HIERARCHY

### 2.1 Layout Components

```typescript
// app/foreman/layout.tsx
ForemanLayout
├── Header
│   ├── Logo
│   ├── Navigation
│   │   ├── NavLink (Dashboard)
│   │   ├── NavLink (Programs)
│   │   ├── NavLink (Tasks)
│   │   ├── NavLink (Builders)
│   │   └── NavLink (Blockers)
│   └── UserMenu
│       ├── Avatar
│       ├── UserInfo
│       └── DropdownMenu
│           ├── SettingsLink
│           └── LogoutButton
├── Sidebar (optional, collapsible)
│   ├── QuickStats
│   ├── ActiveProgram
│   └── RecentActivity
├── Main (children)
└── Footer
    ├── Version
    └── StatusIndicator
```

### 2.2 Dashboard Components

```typescript
// app/foreman/page.tsx
Dashboard
├── PageHeader
│   ├── Title
│   └── Actions
│       └── Button (+ New Program)
├── Grid (3 columns)
│   ├── ActiveProgramCard
│   │   ├── CardHeader (Program name, status)
│   │   ├── CardContent
│   │   │   ├── ProgressBar (program progress)
│   │   │   ├── CurrentWave
│   │   │   └── ProgressBar (wave progress)
│   │   └── CardFooter
│   │       ├── Button (View Details)
│   │       ├── Button (Plan)
│   │       └── Button (Evidence)
│   │
│   ├── BuilderStatusCard
│   │   ├── CardHeader
│   │   ├── CardContent
│   │   │   ├── BuilderStatusItem (UI Builder)
│   │   │   │   ├── BuilderIcon
│   │   │   │   ├── BuilderName
│   │   │   │   ├── StatusIndicator (● Active / ○ Idle)
│   │   │   │   └── HeartbeatTime
│   │   │   ├── BuilderStatusItem (API Builder)
│   │   │   ├── BuilderStatusItem (Schema Builder)
│   │   │   ├── BuilderStatusItem (Integration Builder)
│   │   │   └── BuilderStatusItem (QA Builder)
│   │   └── CardFooter
│   │       └── Button (View All Builders)
│   │
│   └── QuickActionsCard
│       └── CardContent
│           ├── Button (+ New Program)
│           ├── Button (📊 View Evidence)
│           ├── Button (🔍 Search Tasks)
│           └── Button (⚙️ Settings)
│
├── RunningTasksSection
│   ├── SectionHeader
│   │   ├── Title (Running Tasks)
│   │   └── Badge (count)
│   └── TaskList
│       ├── TaskCard (Task 1)
│       │   ├── TaskHeader
│       │   │   ├── TaskId
│       │   │   ├── BuilderBadge
│       │   │   └── StatusIndicator
│       │   ├── TaskTitle
│       │   ├── ProgressBar
│       │   ├── TaskMeta
│       │   │   ├── StartTime
│       │   │   └── Duration
│       │   └── TaskActions
│       │       ├── Button (View Task)
│       │       └── Button (Evidence)
│       ├── TaskCard (Task 2)
│       ├── TaskCard (Task 3)
│       └── Button (View All Tasks)
│
├── BlockersSection (if blockers exist)
│   ├── SectionHeader
│   │   ├── Title (Blockers & Alerts)
│   │   └── Badge (count, alert style)
│   └── BlockerList
│       └── BlockerAlert
│           ├── BlockerIcon (⚠️)
│           ├── BlockerType
│           ├── TaskInfo
│           ├── DetectedTime
│           ├── Description
│           └── BlockerActions
│               ├── Button (View Details)
│               ├── Button (Resolve)
│               └── Button (Escalate)
│
└── Grid (2 columns)
    ├── RecentActivityCard
    │   └── ActivityList
    │       ├── ActivityItem (Task completed)
    │       ├── ActivityItem (Wave completed)
    │       └── Button (View Full Log)
    └── (Quick Actions already above)
```

### 2.3 Program Detail Components

```typescript
// app/foreman/programs/[programId]/page.tsx
ProgramDetail
├── PageHeader
│   ├── Breadcrumbs
│   │   ├── Link (Dashboard)
│   │   └── Text (Program Name)
│   └── Actions
│       ├── Button (Edit Program)
│       ├── Button (View Plan)
│       └── Button (Export Report)
│
├── ProgramOverviewCard
│   ├── CardHeader
│   │   ├── ProgramTitle
│   │   ├── StatusBadge
│   │   └── ProgressBar
│   ├── CardContent
│   │   ├── Description
│   │   ├── ObjectivesList
│   │   │   ├── ObjectiveItem
│   │   │   ├── ObjectiveItem
│   │   │   └── ObjectiveItem
│   │   └── MetaInfo
│   │       ├── Created
│   │       └── Updated
│   └── CardFooter
│       ├── Button (Edit)
│       ├── Button (View Plan)
│       └── Button (Evidence)
│
├── WavesSection
│   ├── SectionHeader
│   │   ├── Title (Waves)
│   │   └── Badge (count)
│   └── WavesList
│       ├── WaveCard (Wave 1)
│       │   ├── WaveHeader
│       │   │   ├── WaveSequence (1)
│       │   │   ├── WaveName
│       │   │   └── StatusBadge (Completed ✓)
│       │   ├── ProgressBar
│       │   ├── WaveStats
│       │   │   ├── TasksCount (8/8 completed)
│       │   │   ├── Duration (2 weeks)
│       │   │   └── Completed (date)
│       │   └── WaveActions
│       │       ├── Button (View Wave)
│       │       └── Button (Evidence)
│       ├── WaveCard (Wave 2 - In Progress)
│       │   ├── (similar structure)
│       │   └── RemainingTasksList
│       │       ├── TaskLink (T-2345)
│       │       ├── TaskLink (T-2346)
│       │       └── TaskLink (T-2347)
│       └── WaveCard (Wave 3 - Planned)
│           └── DependenciesInfo
│
├── ActiveTasksSection
│   └── TasksTable
│       ├── TableHeader
│       │   ├── Column (Task ID)
│       │   ├── Column (Name)
│       │   ├── Column (Builder)
│       │   ├── Column (Progress)
│       │   └── Column (Duration)
│       └── TableBody
│           ├── TaskRow
│           ├── TaskRow
│           └── TaskRow
│
└── BlockersSection (if any)
    └── BlockersList
```

### 2.4 Task Detail Components

```typescript
// app/foreman/tasks/[taskId]/page.tsx
TaskDetail
├── PageHeader
│   ├── Breadcrumbs
│   └── Actions
│
├── TaskDetailsCard
│   ├── TaskHeader
│   │   ├── TaskId
│   │   ├── TaskTitle
│   │   └── StatusBadge
│   ├── TaskMeta
│   │   ├── Program
│   │   ├── Wave
│   │   ├── AssignedBuilder
│   │   └── ProgressBar
│   ├── Timing
│   │   ├── Started
│   │   ├── Duration
│   │   ├── EstimatedCompletion
│   │   └── Remaining
│   ├── References
│   │   ├── ArchitectureReference
│   │   │   ├── FileIcon
│   │   │   ├── Path
│   │   │   └── Link (View Architecture)
│   │   └── QASuiteLocation
│   │       ├── TestIcon
│   │       ├── Path
│   │       ├── CurrentStatus (RED/GREEN)
│   │       └── Link (View QA Suite)
│   └── AcceptanceCriteria
│       ├── CriteriaItem (All tests pass)
│       ├── CriteriaItem (Zero test debt)
│       └── CriteriaItem (Evidence complete)
│
├── BuilderStatusCard
│   ├── BuilderInfo
│   │   ├── BuilderId
│   │   ├── Backend
│   │   ├── Model
│   │   └── LastHeartbeat
│   ├── BuilderState
│   │   ├── State
│   │   └── ExecutionContinuity
│   ├── CurrentActivity
│   └── RecentHeartbeats
│       ├── HeartbeatItem
│       ├── HeartbeatItem
│       └── HeartbeatItem
│
├── QAExecutionHistoryCard
│   ├── CardHeader
│   └── QARunsList
│       ├── QARunItem (Run #8 - Latest)
│       │   ├── RunNumber
│       │   ├── Timestamp
│       │   ├── Status (RED/GREEN)
│       │   ├── TestCount (12/15 passing)
│       │   ├── FailingTestsList (expandable)
│       │   └── Actions
│       │       ├── Link (View Results)
│       │       └── Link (View Logs)
│       ├── QARunItem (Run #7)
│       └── Link (View All Runs)
│
├── EvidenceTrailCard
│   └── Timeline
│       ├── TimelineItem (Task assigned)
│       ├── TimelineItem (Builder started)
│       ├── TimelineItem (Architecture validated)
│       └── Link (View Full Trail)
│
└── ActionsCard
    ├── Button (View Architecture)
    ├── Button (View QA Suite)
    ├── Button (View Builder Logs)
    ├── Button (Escalate Issue)
    └── Button (Export Evidence)
```

---

## 3. COMPONENT PROPS & STATE

### 3.1 TaskCard Component

```typescript
// components/TaskCard.tsx
interface TaskCardProps {
  task: {
    task_id: string;
    name: string;
    assigned_builder: BuilderType;
    state: TaskState;
    progress_percentage: number;
    started_at: Date | null;
  };
  showActions?: boolean;
  onViewTask?: (taskId: string) => void;
  onViewEvidence?: (taskId: string) => void;
}

interface TaskCardState {
  isExpanded: boolean;
  isLoading: boolean;
}
```

### 3.2 BuilderStatusIndicator Component

```typescript
// components/BuilderStatusIndicator.tsx
interface BuilderStatusIndicatorProps {
  builder: {
    builder_id: BuilderType;
    state: BuilderState;
    last_heartbeat: Date;
  };
  showHeartbeat?: boolean;
  size?: 'sm' | 'md' | 'lg';
}

type BuilderType = 'ui-builder' | 'api-builder' | 'schema-builder' | 
                   'integration-builder' | 'qa-builder';
type BuilderState = 'idle' | 'active' | 'blocked' | 'failed';
```

### 3.3 ProgressBar Component

```typescript
// components/ProgressBar.tsx
interface ProgressBarProps {
  value: number;              // 0-100
  max?: number;               // default 100
  size?: 'sm' | 'md' | 'lg';
  variant?: 'default' | 'success' | 'warning' | 'error';
  showLabel?: boolean;
  showPercentage?: boolean;
  animate?: boolean;
}
```

### 3.4 BlockerAlert Component

```typescript
// components/BlockerAlert.tsx
interface BlockerAlertProps {
  blocker: {
    blocker_id: string;
    entity_type: 'program' | 'wave' | 'task';
    entity_id: string;
    classification: BlockerClassification;
    description: string;
    detected_at: Date;
  };
  onViewDetails?: (blockerId: string) => void;
  onResolve?: (blockerId: string) => void;
  onEscalate?: (blockerId: string) => void;
}

type BlockerClassification = 
  | 'architecture_qa_mismatch'
  | 'impossible_requirements'
  | 'protected_path'
  | 'repeated_failures'
  | 'constitutional_violation'
  | 'builder_stall';
```

---

## 4. STATE MANAGEMENT

### 4.1 Server State (React Query)

```typescript
// hooks/usePrograms.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

// Fetch active program
export function useActiveProgram() {
  return useQuery({
    queryKey: ['programs', 'active'],
    queryFn: () => fetch('/api/programs/active').then(res => res.json()),
    refetchInterval: 30000, // Refetch every 30 seconds
  });
}

// Fetch program details
export function useProgramDetails(programId: string) {
  return useQuery({
    queryKey: ['programs', programId],
    queryFn: () => fetch(`/api/programs/${programId}`).then(res => res.json()),
  });
}

// Fetch running tasks
export function useRunningTasks() {
  return useQuery({
    queryKey: ['tasks', 'running'],
    queryFn: () => fetch('/api/tasks?state=in-progress').then(res => res.json()),
    refetchInterval: 10000, // Refetch every 10 seconds
  });
}

// Fetch builders status
export function useBuildersStatus() {
  return useQuery({
    queryKey: ['builders', 'status'],
    queryFn: () => fetch('/api/builders').then(res => res.json()),
    refetchInterval: 5000, // Refetch every 5 seconds (heartbeat monitoring)
  });
}

// Fetch active blockers
export function useActiveBlockers() {
  return useQuery({
    queryKey: ['blockers', 'active'],
    queryFn: () => fetch('/api/blockers?resolved=false').then(res => res.json()),
    refetchInterval: 15000, // Refetch every 15 seconds
  });
}

// Approve plan mutation
export function useApprovePlan() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (programId: string) => 
      fetch(`/api/programs/${programId}/approve`, { method: 'POST' }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['programs'] });
    },
  });
}

// Resolve blocker mutation
export function useResolveBlocker() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ blockerId, resolution }: { blockerId: string; resolution: string }) =>
      fetch(`/api/blockers/${blockerId}/resolve`, {
        method: 'POST',
        body: JSON.stringify({ resolution }),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['blockers'] });
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
    },
  });
}
```

### 4.2 Client State (Zustand)

```typescript
// stores/uiStore.ts
import { create } from 'zustand';

interface UIState {
  sidebarOpen: boolean;
  theme: 'light' | 'dark';
  filters: {
    taskState?: TaskState;
    builderType?: BuilderType;
    dateRange?: { start: Date; end: Date };
  };
  
  toggleSidebar: () => void;
  setTheme: (theme: 'light' | 'dark') => void;
  setFilter: (key: string, value: any) => void;
  clearFilters: () => void;
}

export const useUIStore = create<UIState>((set) => ({
  sidebarOpen: true,
  theme: 'light',
  filters: {},
  
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  setTheme: (theme) => set({ theme }),
  setFilter: (key, value) => set((state) => ({
    filters: { ...state.filters, [key]: value },
  })),
  clearFilters: () => set({ filters: {} }),
}));
```

### 4.3 Form State (React Hook Form + Zod)

```typescript
// forms/ProgramForm.tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';

const programSchema = z.object({
  name: z.string().min(3, 'Name must be at least 3 characters'),
  description: z.string().min(10, 'Description must be at least 10 characters'),
  objectives: z.array(z.string()).min(1, 'At least one objective required'),
});

type ProgramFormData = z.infer<typeof programSchema>;

export function ProgramForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<ProgramFormData>({
    resolver: zodResolver(programSchema),
  });
  
  const onSubmit = async (data: ProgramFormData) => {
    await fetch('/api/programs', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  };
  
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* Form fields */}
    </form>
  );
}
```

---

## 5. FORM VALIDATION RULES

### 5.1 Program Intent Form

```typescript
const programIntentSchema = z.object({
  intent: z.string()
    .min(10, 'Intent must be at least 10 characters')
    .max(500, 'Intent must be less than 500 characters'),
  priority: z.enum(['low', 'medium', 'high']),
  deadline: z.date().optional(),
});
```

### 5.2 Blocker Resolution Form

```typescript
const blockerResolutionSchema = z.object({
  action: z.enum([
    'update_qa',
    'update_architecture',
    'escalate',
    'mark_false_positive',
  ]).required('Action is required'),
  resolution_notes: z.string().min(10, 'Please provide resolution notes'),
  estimated_time: z.number().min(0).optional(),
});
```

### 5.3 Builder Configuration Form

```typescript
const builderConfigSchema = z.object({
  backend_type: z.enum(['local', 'hosted', 'burst']),
  model_preference: z.string().optional(),
  heartbeat_interval: z.number().min(30).max(300),
  stall_threshold: z.number().min(60).max(600),
  max_iterations: z.number().min(1).max(20),
});
```

---

## 6. ERROR STATES

### 6.1 Component Error States

```typescript
// Error boundary for components
<ErrorBoundary fallback={<ErrorFallback />}>
  <DashboardContent />
</ErrorBoundary>

// Loading states
{isLoading && <LoadingSpinner />}
{error && <ErrorMessage error={error} />}
{!data && !isLoading && <EmptyState />}
```

### 6.2 Error Messages

```typescript
const errorMessages = {
  network: 'Unable to connect. Please check your internet connection.',
  unauthorized: 'You are not authorized to perform this action.',
  not_found: 'The requested resource was not found.',
  server_error: 'An unexpected error occurred. Please try again.',
  validation: 'Please check the form for errors.',
  timeout: 'Request timed out. Please try again.',
};
```

---

## 7. LOADING STATES

### 7.1 Page-Level Loading

```typescript
// loading.tsx
export default function Loading() {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="text-center">
        <Spinner className="h-12 w-12 mx-auto" />
        <p className="mt-4 text-gray-600">Loading...</p>
      </div>
    </div>
  );
}
```

### 7.2 Component-Level Loading

```typescript
// Skeleton loading for cards
<Card>
  <CardHeader>
    <Skeleton className="h-6 w-32" />
  </CardHeader>
  <CardContent>
    <Skeleton className="h-4 w-full mb-2" />
    <Skeleton className="h-4 w-3/4" />
  </CardContent>
</Card>
```

---

## 8. EMPTY STATES

### 8.1 No Programs

```typescript
<EmptyState
  icon={<FileIcon />}
  title="No Programs"
  description="No programs are currently running."
  action={
    <Button onClick={handleCreateProgram}>
      + Create Program
    </Button>
  }
/>
```

### 8.2 No Tasks

```typescript
<EmptyState
  icon={<CheckCircleIcon />}
  title="No Running Tasks"
  description="All tasks have been completed."
  action={<Link href="/programs">View Programs</Link>}
/>
```

### 8.3 No Blockers

```typescript
<EmptyState
  icon={<ShieldCheckIcon />}
  title="No Active Blockers"
  description="All tasks are progressing smoothly."
  variant="success"
/>
```

---

## 9. RESPONSIVE BEHAVIOR

### 9.1 Breakpoints

```typescript
const breakpoints = {
  sm: '640px',   // Mobile landscape
  md: '768px',   // Tablet
  lg: '1024px',  // Desktop
  xl: '1280px',  // Large desktop
  '2xl': '1536px', // Extra large
};
```

### 9.2 Responsive Grid

```typescript
// Desktop: 3 columns
// Tablet: 2 columns
// Mobile: 1 column

<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <ActiveProgramCard />
  <BuilderStatusCard />
  <QuickActionsCard />
</div>
```

### 9.3 Mobile Navigation

```typescript
// Hamburger menu for mobile
// Full navigation bar for desktop

<nav className="hidden lg:flex">
  <NavLinks />
</nav>

<button className="lg:hidden" onClick={toggleMobileMenu}>
  <MenuIcon />
</button>

<MobileMenu open={mobileMenuOpen}>
  <NavLinks />
</MobileMenu>
```

---

## 10. ACCESSIBILITY

### 10.1 ARIA Labels

```typescript
<button
  aria-label="View task details"
  aria-describedby="task-description"
>
  View Details
</button>

<ProgressBar
  aria-label="Task progress"
  aria-valuenow={75}
  aria-valuemin={0}
  aria-valuemax={100}
  role="progressbar"
/>
```

### 10.2 Keyboard Navigation

```typescript
// All interactive elements must be keyboard accessible
<Button onKeyDown={handleKeyDown} tabIndex={0}>
  Action
</Button>

// Skip links for screen readers
<a href="#main-content" className="sr-only focus:not-sr-only">
  Skip to main content
</a>
```

### 10.3 Color Contrast

```typescript
// Ensure WCAG AA compliance (4.5:1 for normal text)
const colors = {
  text: {
    primary: '#1a1a1a',   // Contrast ratio: 14.5:1 on white
    secondary: '#6b7280', // Contrast ratio: 5.4:1 on white
  },
  status: {
    active: '#10b981',    // Green - sufficient contrast
    idle: '#9ca3af',      // Gray - sufficient contrast
    blocked: '#ef4444',   // Red - sufficient contrast
  },
};
```

### 10.4 Screen Reader Support

```typescript
// Announce dynamic updates to screen readers
<div aria-live="polite" aria-atomic="true">
  {notification && <p>{notification}</p>}
</div>

// Use semantic HTML
<main>
  <h1>Dashboard</h1>
  <nav aria-label="Primary navigation">
    <ul>
      <li><a href="/programs">Programs</a></li>
    </ul>
  </nav>
</main>
```

---

## 11. STYLING & THEMING

### 11.1 Design System (Tailwind CSS)

```typescript
// tailwind.config.ts
export default {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          500: '#0ea5e9',
          900: '#0c4a6e',
        },
        // ... more colors
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
};
```

### 11.2 Dark Mode Support

```typescript
// Use CSS variables for theme switching
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  --primary: 221.2 83.2% 53.3%;
}

.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
  --primary: 217.2 91.2% 59.8%;
}

// Apply in components
<div className="bg-background text-foreground">
  <Button className="bg-primary">Action</Button>
</div>
```

---

## 12. PERFORMANCE OPTIMIZATIONS

### 12.1 Code Splitting

```typescript
// Lazy load heavy components
const ProgramDetail = lazy(() => import('./ProgramDetail'));
const TaskDetail = lazy(() => import('./TaskDetail'));

<Suspense fallback={<Loading />}>
  <ProgramDetail />
</Suspense>
```

### 12.2 Memoization

```typescript
// Memoize expensive calculations
const filteredTasks = useMemo(
  () => tasks.filter(task => task.state === 'in-progress'),
  [tasks]
);

// Memoize callbacks
const handleViewTask = useCallback(
  (taskId: string) => {
    router.push(`/tasks/${taskId}`);
  },
  [router]
);
```

### 12.3 Virtual Scrolling (for large lists)

```typescript
import { useVirtualizer } from '@tanstack/react-virtual';

// Render only visible items
const virtualizer = useVirtualizer({
  count: tasks.length,
  getScrollElement: () => parentRef.current,
  estimateSize: () => 80,
});
```

---

## 13. USER ROLE VIEWS

### 13.1 Johan (Governor) View

- Full access to all features
- Program creation and approval
- Blocker resolution
- Builder configuration
- Evidence export

### 13.2 Builder (Agent) View (Future)

- Read-only access to:
  - Assigned tasks
  - Architecture documents
  - QA suites
- Write access to:
  - Heartbeat submission
  - Progress updates
  - Escalations

### 13.3 Read-Only Observer View (Future)

- View-only access to:
  - Dashboard
  - Program progress
  - Task status
- No actions permitted

---

## 14. NAVIGATION FLOWS

### 14.1 Primary Navigation Flow

```
Dashboard → Program List → Program Detail → Task Detail → Evidence Trail
     ↓          ↓              ↓               ↓
  Tasks     Wave Detail    Builder Logs    QA Results
     ↓          ↓              ↓
 Builders   Blocker List   Architecture Doc
```

### 14.2 Blocker Resolution Flow

```
Dashboard (Blocker Alert) 
    → Click "View Details"
    → Blocker Detail Dialog
    → Select Resolution Option
    → Execute Action
    → Blocker Resolved
    → Task Resumes
    → Dashboard Updates
```

### 14.3 Plan Approval Flow

```
Foreman Creates Plan
    → Johan Notified
    → Opens Plan Dialog
    → Reviews Sections
        → View Architecture Validation
        → View QA Status
        → View Risk Assessment
    → Makes Decision
        → Approve → Plan Executes
        → Reject → Plan Cancelled
        → Request Changes → Foreman Adjusts
```

---

*Generated for Issue #2 - Architecture & QA Design (Wave 0 Completion)*
