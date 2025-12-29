# Build Tree Visualization Dashboard Specification

**Version**: 1.0.0  
**Status**: Active  
**Authority**: BUILD_TREE_EXECUTION_MODEL.md (G-C8)  
**Last Updated**: 2025-12-25  
**Owner**: Johan (MaturionISMS)

---

## I. Purpose

Provide real-time visualization of the canonical build tree structure and execution state hierarchy for the Maturion FM build system.

**Key Objectives**:
- Visualize Program → Wave → Task hierarchy
- Display execution states at all levels
- Show activation states
- Display status indicators (Red/Amber/Green)
- Show completion percentages (informational only)
- Provide deterministic state roll-up
- Enable real-time monitoring
- Support drill-down navigation

**Explicitly Out of Scope**:
- Decision-making logic
- Automatic state transitions
- Evidence creation
- Task execution

---

## II. Governance Basis

This specification implements visualization for:

- **BUILD_TREE_EXECUTION_MODEL.md (G-C8)**: Canonical data model
- **foreman-execution-state-model.md**: Execution state definitions
- **FM_FUNCTIONAL_SPEC.md**: Program/Wave/Task hierarchy

**Compliance Requirements**:
- MUST visualize all nodes in the tree
- MUST show deterministic roll-up (worst-case propagation)
- MUST display status accurately
- MUST update in real-time
- MUST NOT imply authorization from percentage
- MUST be read-only (no state mutations in UI)

---

## III. Visual Hierarchy

### 3.1 Tree Structure

Display hierarchical tree with expandable/collapsible nodes:

```
▼ Program: Multi-Module ISMS Platform  [ACTIVE] [🟢 GREEN] [45%]
  ├─ ▼ Wave 0: Foundation Setup  [COMPLETE] [🟢 GREEN] [100%]
  │   ├─ ✓ Task: Architecture Foundation  [COMPLETE] [🟢 GREEN] [100%]
  │   ├─ ✓ Task: QA Infrastructure  [COMPLETE] [🟢 GREEN] [100%]
  │   └─ ✓ Task: Governance Setup  [COMPLETE] [🟢 GREEN] [100%]
  ├─ ▶ Wave 1: Multi-Module Skeleton  [IN_PROGRESS] [🟡 AMBER] [60%]
  │   ├─ ▼ Sub-Wave 1.1: Global UI Shell  [IN_PROGRESS] [🟢 GREEN] [80%]
  │   │   ├─ ✓ Task: Layout System  [COMPLETE] [🟢 GREEN] [100%]
  │   │   ├─ ⚙ Task: Component Library  [IN_PROGRESS] [🟢 GREEN] [0%]
  │   │   └─ ⏸ Task: AI Panel  [BLOCKED] [🔴 RED] [0%]
  │   └─ ▶ Sub-Wave 1.2: Module Skeletons  [PLANNED] [🟢 GREEN] [0%]
  └─ ▶ Wave 2: Core Functionality  [PLANNED] [🟢 GREEN] [0%]
```

### 3.2 Node Display Format

Each node shows:

```
[Expand Icon] [Type Icon] Name  [State Badge] [Status Indicator] [Completion %]
```

**Example**:
```
▼ 📋 Wave 1: Multi-Module Skeleton  [IN_PROGRESS] [🟡 AMBER] [60%]
```

### 3.3 Indentation and Connectors

- Use indentation to show hierarchy depth
- Use tree connectors (├─, └─, │) for visual relationships
- Align badges and indicators vertically for readability

---

## IV. Per-Node Display Elements

### 4.1 Node Icons

**Type Icons**:
- 🎯 Program
- 📋 Wave
- 📌 Sub-Wave
- ☑️ Task

**State Icons**:
- ▶ Collapsed (has children)
- ▼ Expanded (has children)
- ✓ Complete
- ⚙ In Progress
- ⏸ Blocked
- ⏹ Planned
- ✗ Aborted

### 4.2 Execution State Badge

Display current execution state as badge with color:

**Program States**:
- `[DRAFT]` - Gray
- `[ACTIVE]` - Blue
- `[SUSPENDED]` - Orange
- `[COMPLETE]` - Green
- `[ARCHIVED]` - Gray

**Wave/Sub-Wave States**:
- `[PLANNED]` - Gray
- `[READY]` - Light Blue
- `[IN_PROGRESS]` - Blue
- `[BLOCKED]` - Red
- `[COMPLETE]` - Green

**Task States**:
- `[PLANNED]` - Gray
- `[IN_PROGRESS]` - Blue
- `[BLOCKED]` - Red
- `[COMPLETE]` - Green
- `[ABORTED]` - Dark Gray

### 4.3 Status Indicator

Display RAG status with clear visual distinction:

- 🟢 **GREEN**: Healthy, on track
- 🟡 **AMBER**: Attention needed
- 🔴 **RED**: Critical issue

**Color-Blind Friendly**:
- Use shapes/patterns in addition to colors
- GREEN = ✅ or solid circle
- AMBER = ⚠️ or triangle
- RED = ❌ or square

### 4.4 Completion Percentage

Display as `[XX%]` or progress bar:

**Text Format**: `[45%]`

**Progress Bar Format**:
```
[████████░░░░░░░░] 60%
```

**Critical UI Rule**: 
- Display with muted styling
- Include tooltip: "Informational only. Does not indicate authorization."
- Never highlight or emphasize percentage alone

### 4.5 Activation State (Optional Overlay)

Show activation state on hover or in detail panel:

- 📝 DRAFT
- ✅ APPROVED
- ⚡ ACTIVE
- 👁️ REVIEW
- ✔️ MERGED
- 🚫 BLOCKED

### 4.6 Blocker Indication

If node is BLOCKED, show blocker info:

```
⏸ Task: AI Panel  [BLOCKED] [🔴 RED] [0%]
  🚫 BLOCKER: Waiting for API endpoint completion
```

**Blocker Badge Color**:
- MINOR: Yellow
- MAJOR: Orange
- CRITICAL: Red

---

## V. Deterministic Roll-Up Display

### 5.1 Roll-Up Visualization

**Principle**: Parent status MUST reflect worst child status

**Visual Indication**:
1. Parent node shows its derived status
2. Hover tooltip explains roll-up:
   ```
   Wave 1: AMBER
   Derived from 1 RED task, 2 GREEN tasks
   Worst-case propagation applied
   ```

3. Click to expand shows child statuses

### 5.2 Roll-Up Explanation Panel

Optional panel showing roll-up logic:

```
┌─────────────────────────────────────────────┐
│ Roll-Up Analysis: Wave 1                    │
├─────────────────────────────────────────────┤
│ Status: 🟡 AMBER                            │
│                                             │
│ Child Status Breakdown:                     │
│   🔴 RED: 1 task (AI Panel - BLOCKED)       │
│   🟡 AMBER: 0 tasks                         │
│   🟢 GREEN: 2 tasks                         │
│                                             │
│ Rule: Worst-case propagation                │
│ Result: Wave inherits RED → AMBER (1 RED)  │
└─────────────────────────────────────────────┘
```

### 5.3 Blocking Propagation

If child is BLOCKED, parent shows blocking indication:

```
▼ Wave 1  [IN_PROGRESS] [🔴 RED] [60%]
  └─ 🚫 1 task blocked
```

Click to see which task(s) are blocking.

---

## VI. Real-Time Refresh

### 6.1 Update Frequency

**Polling Mode** (Minimum Viable):
- Poll every 5-10 seconds
- Full tree refresh on each poll
- Show "Last updated: X seconds ago"

**Event-Driven Mode** (Preferred):
- WebSocket or Server-Sent Events (SSE)
- Receive incremental updates
- Apply changes to tree in real-time
- Show "Connected" indicator

### 6.2 Update Visual Feedback

**On Update**:
- Flash/highlight updated nodes briefly (e.g., yellow glow for 1 second)
- Show "Updated now" badge
- Update timestamp

**Connection Status**:
- 🟢 Connected (real-time)
- 🟡 Polling (every X seconds)
- 🔴 Disconnected (last update: X minutes ago)

### 6.3 Optimistic Updates

**NOT ALLOWED**: UI is read-only, no optimistic state changes

All state changes originate from server.

---

## VII. Drill-Down Navigation

### 7.1 Tree Interaction

**Expand/Collapse**:
- Click node icon (▶/▼) to expand/collapse
- Persist expand state in local storage
- Option to "Expand All" or "Collapse All"

**Click Node Name**:
- Opens detail panel (see Section VIII)
- Does not navigate away from tree view

**Right-Click Context Menu** (Optional):
- View Evidence
- View PR
- View Blockers
- Copy Node ID

### 7.2 Filtering and Search

**Filter by State**:
- Show only: PLANNED, IN_PROGRESS, BLOCKED, COMPLETE
- Show only: RED, AMBER, GREEN

**Search**:
- Search by name
- Highlight matching nodes
- Auto-expand to show results

**Builder Filter**:
- Filter tasks by assigned builder
- Show all tasks for ui-builder, api-builder, etc.

---

## VIII. Detail Panel

When node is clicked, show detail panel (slide-in from right or modal):

### 8.1 Node Details

```
┌─────────────────────────────────────────────┐
│ Task: AI Panel Implementation               │
├─────────────────────────────────────────────┤
│ Type: Task                                  │
│ ID: task-ai-panel-001                       │
│ Parent: Wave 1 > Sub-Wave 1.1               │
│                                             │
│ Execution State: BLOCKED                    │
│ Activation State: ACTIVE                    │
│ Status: 🔴 RED                              │
│ Completion: 0%                              │
│                                             │
│ Builder: ui-builder                         │
│ Assigned: 2025-12-20 10:00:00 UTC           │
│                                             │
│ Created: 2025-12-15 08:30:00 UTC            │
│ Updated: 2025-12-25 07:00:00 UTC            │
│                                             │
│ [View Evidence] [View PR] [View Blockers]   │
└─────────────────────────────────────────────┘
```

### 8.2 Blocker Details

If node is BLOCKED, show blockers:

```
┌─────────────────────────────────────────────┐
│ Blockers (1)                                │
├─────────────────────────────────────────────┤
│ 🔴 CRITICAL: API Endpoint Missing           │
│                                             │
│ Type: DEPENDENCY                            │
│ Severity: CRITICAL                          │
│ Description:                                │
│   AI Panel requires /api/ai/chat endpoint   │
│   which is pending in api-builder PR#123    │
│                                             │
│ Created: 2025-12-24 14:00:00 UTC            │
│ Resolution: Waiting for PR#123 merge        │
│                                             │
│ [View Dependency] [View PR#123]             │
└─────────────────────────────────────────────┘
```

### 8.3 Evidence List

Show evidence artifacts:

```
┌─────────────────────────────────────────────┐
│ Evidence (3 items)                          │
├─────────────────────────────────────────────┤
│ ✅ Architecture: ai-panel-spec.md           │
│    Validated: 2025-12-20 by Foreman        │
│                                             │
│ ✅ QA: test/ui/ai-panel.test.ts             │
│    Status: 100% pass (15/15 tests)          │
│    Validated: 2025-12-21 by Foreman        │
│                                             │
│ ⏳ Build: PR#145 (pending review)           │
│    Status: CI passing, awaiting review      │
│                                             │
│ [View All Evidence]                         │
└─────────────────────────────────────────────┘
```

### 8.4 Related Links

- **PR Link**: Link to GitHub PR
- **Architecture**: Link to architecture document
- **QA Results**: Link to QA dashboard
- **Evidence**: Link to evidence artifacts
- **Parent Wave**: Jump to parent wave
- **Dependencies**: Show dependent tasks/waves

---

## IX. Dashboard Layout

### 9.1 Full Dashboard Structure

```
┌──────────────────────────────────────────────────────────────┐
│ Maturion FM - Build Tree Visualization                      │
├──────────────────────────────────────────────────────────────┤
│ [Controls Bar]                                               │
│ [Refresh] [Expand All] [Collapse All] [Filter ▼] [Search]   │
│ Connection: 🟢 Connected | Last Update: now                  │
├─────────────────────┬────────────────────────────────────────┤
│ Tree View           │ Detail Panel                           │
│ (Left 60%)          │ (Right 40%, slide-in on click)         │
│                     │                                        │
│ ▼ 🎯 Program: ...   │ [Node details shown when clicked]     │
│   ├─ ▼ 📋 Wave 1    │                                        │
│   │   ├─ ☑️ Task 1  │                                        │
│   │   └─ ☑️ Task 2  │                                        │
│   └─ ▶ 📋 Wave 2    │                                        │
│                     │                                        │
│ [Scroll if needed]  │ [Scroll if needed]                     │
│                     │                                        │
└─────────────────────┴────────────────────────────────────────┘
```

### 9.2 Responsive Design

**Desktop (>1024px)**:
- Tree 60%, Detail Panel 40%
- Side-by-side layout

**Tablet (768-1024px)**:
- Tree 100%, Detail Panel overlay (modal)
- Detail panel slides in from right

**Mobile (<768px)**:
- Tree 100%, Detail Panel full-screen overlay
- Simplified tree view (less detail per node)

---

## X. Controls and Actions

### 10.1 Refresh Control

**Manual Refresh**:
- Button to force refresh
- Shows loading indicator

**Auto-Refresh Toggle**:
- Enable/disable real-time updates
- Useful for presentations or screenshots

### 10.2 Expand/Collapse Controls

- **Expand All**: Opens all nodes
- **Collapse All**: Closes all nodes
- **Expand to Level N**: Expand only to specific depth (Program, Wave, Task)

### 10.3 Filter Controls

**Status Filter**:
- Dropdown: All, RED only, AMBER only, GREEN only

**State Filter**:
- Dropdown: All, PLANNED, IN_PROGRESS, BLOCKED, COMPLETE

**Builder Filter**:
- Dropdown: All, ui-builder, api-builder, schema-builder, etc.

### 10.4 Search

**Search Input**:
- Text input for node name
- Real-time filter as user types
- Highlight matching nodes
- Auto-expand to show matches

### 10.5 View Options

**Compact View**:
- Smaller text, less padding
- Fits more nodes on screen

**Detailed View**:
- Larger text, more spacing
- Shows more info per node inline

---

## XI. Visual Design Standards

### 11.1 Color Palette

**Status Colors**:
- RED: `#DC2626` (Tailwind red-600)
- AMBER: `#F59E0B` (Tailwind amber-500)
- GREEN: `#10B981` (Tailwind green-500)

**State Colors**:
- DRAFT: `#9CA3AF` (gray-400)
- ACTIVE/IN_PROGRESS: `#3B82F6` (blue-500)
- COMPLETE: `#10B981` (green-500)
- BLOCKED: `#DC2626` (red-600)
- PLANNED: `#6B7280` (gray-500)

**Background**:
- Primary: `#FFFFFF` (white)
- Secondary: `#F9FAFB` (gray-50)
- Hover: `#F3F4F6` (gray-100)

### 11.2 Typography

**Node Names**:
- Font: Inter, system-ui
- Size: 14px (base), 16px (heading)
- Weight: 500 (medium)

**Badges**:
- Font: Inter, monospace
- Size: 12px
- Weight: 600 (semi-bold)

**Percentages**:
- Font: Inter, monospace
- Size: 12px
- Weight: 400 (regular)
- Color: `#6B7280` (gray-500, muted)

### 11.3 Spacing and Layout

**Node Indentation**:
- 24px per level (Wave = 24px, Task = 48px)

**Node Height**:
- Compact: 32px
- Default: 40px
- Detailed: 56px

**Padding**:
- Horizontal: 16px
- Vertical: 8px

### 11.4 Accessibility

**WCAG 2.1 Level AA**:
- Color contrast ratio ≥ 4.5:1 for text
- Color contrast ratio ≥ 3:1 for UI components
- Keyboard navigation support
- Screen reader support
- Focus indicators visible

**Keyboard Navigation**:
- Tab: Move between nodes
- Enter: Expand/collapse node
- Arrow keys: Navigate tree
- Escape: Close detail panel

**Screen Reader**:
- ARIA labels for all interactive elements
- ARIA live regions for updates
- Descriptive text for status indicators

---

## XII. Edge Cases and Error Handling

### 12.1 Empty Tree

If no programs exist:

```
┌──────────────────────────────────────────┐
│ No build programs found                  │
│                                          │
│ [Create New Program]                     │
└──────────────────────────────────────────┘
```

### 12.2 Loading State

While fetching tree:

```
┌──────────────────────────────────────────┐
│ Loading build tree...                    │
│ [Spinner animation]                      │
└──────────────────────────────────────────┘
```

### 12.3 Connection Error

If real-time connection fails:

```
┌──────────────────────────────────────────┐
│ 🔴 Connection lost                       │
│ Falling back to polling mode             │
│ [Retry Connection]                       │
└──────────────────────────────────────────┘
```

### 12.4 Stale Data Warning

If data hasn't updated in >5 minutes:

```
⚠️ Warning: Data may be stale
Last update: 12 minutes ago
[Refresh Now]
```

### 12.5 Large Trees

If tree has >1000 nodes:

- Virtualized scrolling for performance
- Load children on-demand (lazy loading)
- Option to view single wave at a time

---

## XIII. Integration Points

### 13.1 Data Source

**Primary Source**: FM execution state database

**API Endpoints**:
- `GET /api/build-tree` - Full tree
- `GET /api/build-tree/:program_id` - Single program
- `GET /api/build-tree/wave/:wave_id` - Single wave
- `GET /api/build-tree/task/:task_id` - Single task

**Real-Time**:
- WebSocket: `ws://[host]/api/build-tree/subscribe`
- Server-Sent Events: `GET /api/build-tree/stream`

### 13.2 External Links

**GitHub Integration**:
- PR links open in new tab
- CI status badges (if available)

**Evidence Links**:
- Link to architecture documents (GitHub, local)
- Link to QA dashboard
- Link to evidence validation reports

### 13.3 Navigation Integration

**Link to Other Dashboards**:
- QA Dashboard (for QA evidence)
- Compliance Dashboard (for compliance checks)
- Governance Dashboard (for governance violations)

---

## XIV. Performance Requirements

### 14.1 Load Time

- Initial load: < 2 seconds (tree up to 500 nodes)
- Subsequent updates: < 500ms

### 14.2 Rendering

- Tree rendering: < 100ms (up to 100 visible nodes)
- Virtualization for trees >1000 nodes

### 14.3 Update Latency

- Real-time update: < 1 second from server event
- Polling update: Within polling interval (5-10 seconds)

### 14.4 Scalability

- Support trees up to 10,000 nodes
- Virtualized scrolling for large trees
- Lazy loading for deep hierarchies

---

## XV. Security and Authorization

### 15.1 Access Control

**Who Can View**:
- Johan (Owner)
- FM (AI Supervisor)
- Builder agents (read-only)

**Who Cannot View**:
- External users
- Unauthenticated sessions

### 15.2 Read-Only Interface

- No state mutations from UI
- No direct task assignment
- No blocker creation/resolution
- All actions escalate to FM

### 15.3 Audit Logging

- Log all view actions (who viewed what, when)
- Log all drill-down actions
- Log all filter/search actions
- Preserve audit trail for governance

---

## XVI. Testing Requirements

### 16.1 Unit Tests

- Test roll-up logic
- Test status derivation
- Test tree rendering
- Test state badge colors

### 16.2 Integration Tests

- Test API integration
- Test real-time updates
- Test WebSocket connection
- Test fallback to polling

### 16.3 Visual Regression Tests

- Screenshot tests for tree layout
- Screenshot tests for badges and indicators
- Screenshot tests for detail panel

### 16.4 Accessibility Tests

- WCAG 2.1 Level AA compliance
- Keyboard navigation
- Screen reader compatibility

### 16.5 Performance Tests

- Load time with 100, 500, 1000 nodes
- Update latency
- Memory usage over time

---

## XVII. Documentation Requirements

### 17.1 User Guide

- How to navigate the tree
- How to interpret states and statuses
- How to use filters and search
- How to view evidence and blockers

### 17.2 Developer Guide

- API integration
- Data model reference
- Customization options
- Troubleshooting

### 17.3 Governance Documentation

- Compliance with BUILD_TREE_EXECUTION_MODEL.md
- Roll-up algorithm implementation
- State transition handling
- Evidence validation integration

---

## XVIII. Summary

This Build Tree Visualization Dashboard provides:

1. ✅ **Hierarchical Tree View**: Program → Wave → Task with expandable nodes
2. ✅ **Per-Node Display**: Execution state, activation state, status (R/A/G), completion %
3. ✅ **Deterministic Roll-Up**: Worst-state propagation with explainability
4. ✅ **Real-Time Refresh**: Polling or event-driven updates
5. ✅ **Drill-Down Navigation**: Detail panels, evidence, blockers, PRs
6. ✅ **Filtering and Search**: By state, status, builder, name
7. ✅ **Responsive Design**: Desktop, tablet, mobile
8. ✅ **Accessibility**: WCAG 2.1 AA, keyboard navigation, screen reader support
9. ✅ **Governance Compliance**: Read-only, no authorization from %, GSR enforcement
10. ✅ **Performance**: <2s load, <100ms render, virtualization for large trees

**This is a visualization specification. Implementation happens in builder repositories.**

---

## XIX. Version and Authority

**Version**: 1.0.0  
**Status**: Active  
**Authority**: BUILD_TREE_EXECUTION_MODEL.md (G-C8)  
**Last Updated**: 2025-12-25  
**Owner**: Johan (MaturionISMS)  
**Maintained By**: Maturion Foreman

**Changelog**:
- 1.0.0 (2025-12-25): Initial Build Tree Visualization Dashboard specification

---

*END OF BUILD TREE VISUALIZATION DASHBOARD SPECIFICATION*
