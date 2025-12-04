# Maturion ISMS – Maturion AI Panel Specification

**Version**: 1.0  
**Build Wave**: 1.1  
**Owner**: Maturion Foreman  
**Status**: DRAFT - AWAITING APPROVAL

---

## 1. Purpose

This document defines the Maturion AI Panel - the global runtime AI interface for the Maturion ISMS platform.

The AI Panel provides:
- Real-time platform intelligence and assistance
- Three operational modes (Tenant User, Admin, Global/Super Admin)
- Platform health monitoring
- Compliance notifications
- Threat and vulnerability alerts
- Interactive AI chat interface
- Detachable/floating panel (future)

---

## 2. AI Panel Architecture

### 2.1 Panel Positioning

```
Desktop Layout:
┌──────────────────────────────────────────┬──────────┐
│                                          │          │
│                                          │          │
│           Main Content Area              │    AI    │
│                                          │   Panel  │
│                                          │          │
│                                          │  (25-30% │
│                                          │   width) │
│                                          │          │
│                                          │          │
└──────────────────────────────────────────┴──────────┘

Mobile Layout:
┌──────────────────────────────────────────┐
│                                          │
│           Main Content Area              │
│                                          │
│                                          │
│                                          │
└──────────────────────────────────────────┘
                [AI Button]  ← Bottom-right floating button
```

### 2.2 Panel States

1. **Hidden** (default on mobile)
2. **Minimized** - Button only (bottom-right)
3. **Expanded** - Panel visible (sidebar-style)
4. **Detached** - Floating window (future feature)
5. **Fullscreen** - Full overlay (mobile only)

---

## 3. AI Panel UI Components

### 3.1 AI Toggle Button

**Location**: Bottom-right corner (floating action button)

**Specification**:
```typescript
interface AIToggleButtonProps {
  isOpen: boolean;
  onClick: () => void;
  hasNotifications: boolean;
  notificationCount?: number;
  pulseAnimation?: boolean;
}
```

**Visual Design**:
```
┌─────────┐
│   AI    │  ← Icon with "AI" text or robot icon
│  [●]    │  ← Notification badge (if alerts present)
└─────────┘
```

**Features**:
- Floating button (z-index: 1100)
- Pulse animation when alerts present
- Notification badge (count or dot)
- Smooth expand/collapse animation
- Accessible (keyboard: Alt+A, screen reader friendly)

**States**:
- Default (idle)
- Hover
- Active (panel open)
- Has alerts (pulsing)
- Disabled (loading or error)

---

### 3.2 AI Panel Container

**Dimensions**:
- **Width**: 
  - Desktop: 25-30% of viewport (min 320px, max 480px)
  - Mobile: 100% (fullscreen overlay)
- **Height**: calc(100vh - header height)
- **Position**: Fixed right, below header

**Specification**:
```typescript
interface AIPanelProps {
  isOpen: boolean;
  mode: 'tenant-user' | 'admin' | 'global';
  onClose: () => void;
  onModeSwitch: (mode: AIPanelMode) => void;
  canSwitchMode: boolean;
}

type AIPanelMode = 'tenant-user' | 'admin' | 'global';
```

**Layout Structure**:
```
┌─────────────────────────────────┐
│ [Header]                    [X] │
│  • Mode Selector                │
│  • Status Indicators            │
├─────────────────────────────────┤
│                                 │
│  [Content Area]                 │
│   - Chat Interface              │
│   - Alerts & Notifications      │
│   - Health Dashboard            │
│   - Compliance Status           │
│                                 │
│                                 │
│                                 │
│                                 │
│                                 │
├─────────────────────────────────┤
│ [Footer]                        │
│  • Quick Actions                │
│  • Input Bar (if chat mode)     │
└─────────────────────────────────┘
```

---

### 3.3 AI Panel Header

**Specification**:
```typescript
interface AIPanelHeaderProps {
  mode: AIPanelMode;
  onModeSwitch: (mode: AIPanelMode) => void;
  canSwitchMode: boolean;
  onClose: () => void;
  onDetach?: () => void; // Future feature
}
```

**Layout**:
```
┌─────────────────────────────────┐
│ 🤖 Maturion AI           [≡] [X]│
│                                 │
│ Mode: [Tenant User ▼]           │
│                                 │
│ Status:                         │
│   • Platform: 🟢 Healthy        │
│   • Watchdog: 🟢 Active         │
│   • Compliance: 🟡 2 Alerts     │
└─────────────────────────────────┘
```

**Features**:
- Mode selector dropdown (if authorized)
- Close button
- Detach button (future)
- Status indicators (color-coded)
- Minimize/maximize toggle

---

## 4. AI Panel Modes

### 4.1 Tenant User Mode

**Purpose**: Day-to-day assistance for tenant users

**Features**:
- **Chat Interface**: Ask questions about the platform
- **Contextual Help**: Help for current page/module
- **Personal Notifications**: User-specific alerts
- **Quick Actions**: Common tasks for current module
- **Training Tips**: On-demand learning suggestions

**Permissions Required**: Any authenticated tenant user

**Data Scope**: 
- User's own data
- Organization data (based on permissions)
- Platform help documentation
- Module-specific guidance

**Example Interactions**:
```
User: "How do I create a new risk assessment?"
AI: "To create a new risk assessment:
     1. Navigate to Risk Assessment > Assessments
     2. Click 'New Assessment'
     3. Select a template or start from scratch
     [Show me how] [Open Risk Assessment]"

User: "Show me my pending tasks"
AI: "You have 3 pending tasks:
     • Complete Risk Assessment for Project X (due tomorrow)
     • Review Policy Draft ABC (due in 3 days)
     • Complete Compliance Training Module 2 (overdue by 1 day)
     [View all tasks]"
```

---

### 4.2 Admin Mode

**Purpose**: Administrative oversight and management

**Features**:
- **Platform Health**: System health metrics
- **User Activity**: Active users, recent actions
- **Alerts & Warnings**: System-level alerts
- **Watchdog Reports**: Automated monitoring results
- **Compliance Status**: Real-time compliance dashboards
- **Admin Quick Actions**: User management, settings, reports

**Permissions Required**: Admin or higher role

**Data Scope**:
- Organization-wide data
- User activity logs (anonymized where appropriate)
- System health metrics
- Compliance dashboards
- Watchdog alerts

**Example Interactions**:
```
Admin: "Show me active users"
AI: "Current active users: 47
     • Peak today: 89 users (10:30 AM)
     • Average session: 3.2 hours
     • Top modules: PIT (23), ERM (18), Risk Assessment (12)
     [View detailed analytics]"

Admin: "Any compliance issues?"
AI: "2 compliance alerts:
     ⚠️ ISO 27001: 3 controls require documentation update
     ⚠️ NIST CSF: Annual review due in 7 days
     [View compliance dashboard]"
```

---

### 4.3 Global Mode (Super Admin)

**Purpose**: Platform-wide intelligence and governance

**Features**:
- **Cross-Tenant Analytics**: Anonymized trends
- **Platform Governance**: Architecture drift detection
- **Security Intelligence**: Threat landscape overview
- **Innovation Insights**: Feature adoption, enhancement requests
- **System Administration**: Platform-level actions
- **AI Self-Improvement**: Learning and optimization suggestions

**Permissions Required**: Super Admin only

**Data Scope**:
- All tenants (anonymized)
- Platform-wide metrics
- Architecture compliance
- Security intelligence
- Innovation proposals

**Example Interactions**:
```
Super Admin: "Platform health overview"
AI: "Platform Status: 🟢 Healthy
     • Tenants: 247 active
     • Uptime: 99.97% (30 days)
     • Performance: Avg response 142ms
     • Security: No active threats
     • Compliance: 98.4% across all tenants
     [View detailed dashboard]"

Super Admin: "Show innovation requests"
AI: "Top 5 enhancement requests (last 30 days):
     1. Bulk import for PIT (42 requests)
     2. Custom dashboards (37 requests)
     3. Mobile app for Auditor (33 requests)
     4. Advanced reporting (29 requests)
     5. API integrations (24 requests)
     [View innovation dashboard]"
```

---

## 5. AI Panel Content Tabs

### 5.1 Chat Tab

**Purpose**: Conversational AI interface

**Specification**:
```typescript
interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  actions?: QuickAction[];
  metadata?: Record<string, any>;
}

interface QuickAction {
  label: string;
  onClick: () => void;
  icon?: ReactNode;
}
```

**Features**:
- Conversation history (session-based)
- Message timestamps
- Typing indicator (when AI is responding)
- Quick action buttons in messages
- Code syntax highlighting (for technical help)
- Markdown support
- Copy message button
- Message threading (future)

**Input Bar**:
```typescript
interface ChatInputProps {
  onSend: (message: string) => void;
  placeholder?: string;
  disabled?: boolean;
  maxLength?: number;
}
```

**Keyboard Shortcuts**:
- `Enter`: Send message
- `Shift+Enter`: New line
- `Ctrl+K`: Clear chat
- `Ctrl+Up/Down`: Navigate history

---

### 5.2 Alerts Tab

**Purpose**: Real-time alerts and notifications

**Specification**:
```typescript
interface Alert {
  id: string;
  type: 'info' | 'warning' | 'error' | 'critical';
  category: 'watchdog' | 'compliance' | 'security' | 'performance';
  title: string;
  message: string;
  timestamp: Date;
  acknowledged: boolean;
  actionUrl?: string;
  actionLabel?: string;
}
```

**Alert Categories**:
- **Watchdog**: Automated monitoring alerts
- **Compliance**: Compliance requirement notifications
- **Security**: Threat and vulnerability alerts
- **Performance**: System performance warnings

**Features**:
- Real-time updates
- Filter by type/category
- Acknowledge/dismiss alerts
- Jump to related page
- Export alerts (admin/global)

**Visual**:
```
┌─────────────────────────────────┐
│ 🔴 CRITICAL (1)                 │
│   • Database backup failed      │
│     2 mins ago     [View] [Ack] │
│                                 │
│ 🟡 WARNING (2)                  │
│   • ISO 27001: Review due       │
│     15 mins ago    [View] [Ack] │
│   • Memory usage: 87%           │
│     1 hour ago     [View] [Ack] │
│                                 │
│ 🟢 INFO (5)                     │
│   [View all info alerts]        │
└─────────────────────────────────┘
```

---

### 5.3 Health Tab (Admin/Global only)

**Purpose**: Platform health monitoring

**Specification**:
```typescript
interface HealthMetrics {
  overall: 'healthy' | 'warning' | 'critical';
  components: {
    database: HealthStatus;
    api: HealthStatus;
    cache: HealthStatus;
    storage: HealthStatus;
    queue: HealthStatus;
  };
  performance: {
    avgResponseTime: number;
    p95ResponseTime: number;
    errorRate: number;
    uptime: number;
  };
}

interface HealthStatus {
  status: 'up' | 'degraded' | 'down';
  latency?: number;
  lastCheck: Date;
}
```

**Visual**:
```
┌─────────────────────────────────┐
│ Overall: 🟢 Healthy             │
│                                 │
│ Components:                     │
│   Database:  🟢 Up (12ms)       │
│   API:       🟢 Up (45ms)       │
│   Cache:     🟢 Up (3ms)        │
│   Storage:   🟢 Up (8ms)        │
│   Queue:     🟡 Degraded (234ms)│
│                                 │
│ Performance:                    │
│   Avg Response:  142ms          │
│   P95 Response:  387ms          │
│   Error Rate:    0.02%          │
│   Uptime:        99.97%         │
│                                 │
│ [View detailed metrics]         │
└─────────────────────────────────┘
```

---

### 5.4 Compliance Tab (Admin/Global only)

**Purpose**: Real-time compliance status

**Specification**:
```typescript
interface ComplianceStatus {
  framework: 'ISO27001' | 'NIST' | 'COBIT' | 'GDPR' | 'POPIA';
  overallScore: number; // 0-100
  controls: {
    total: number;
    implemented: number;
    inProgress: number;
    notStarted: number;
  };
  gaps: ComplianceGap[];
  nextReview: Date;
}

interface ComplianceGap {
  control: string;
  description: string;
  severity: 'high' | 'medium' | 'low';
  dueDate: Date;
}
```

**Visual**:
```
┌─────────────────────────────────┐
│ ISO 27001                       │
│ ████████░░ 82% Complete         │
│                                 │
│ Controls:                       │
│   Implemented:  114 / 138       │
│   In Progress:  18              │
│   Not Started:  6               │
│                                 │
│ Gaps (3):                       │
│   🔴 A.9.1.2 - Access Control   │
│      Due: 2024-12-15            │
│   🟡 A.12.1.3 - Capacity Mgmt   │
│      Due: 2025-01-10            │
│                                 │
│ [View full compliance report]   │
└─────────────────────────────────┘
```

---

## 6. AI Capabilities

### 6.1 Conversational AI

**Powered By**: OpenAI GPT-4 or equivalent

**Capabilities**:
- Natural language understanding
- Context-aware responses
- Multi-turn conversations
- Platform-specific knowledge
- Code generation (for API usage)
- Data analysis and insights

**Limitations**:
- No access to sensitive user data
- No execution of system commands
- No modification of data (read-only)
- Respects user permissions

---

### 6.2 Watchdog Intelligence

**Capabilities**:
- Real-time monitoring of platform health
- Anomaly detection (usage patterns, errors)
- Predictive alerts (before issues occur)
- Auto-remediation suggestions
- Drift detection (architecture, compliance)

**Data Sources**:
- Application logs
- Performance metrics
- User activity
- Error tracking
- Compliance audits

---

### 6.3 Contextual Assistance

**Context-Aware Help**:
- Current module/page
- User's recent actions
- Common pain points
- Related documentation
- Similar user queries

**Example**:
```
[User is on Risk Assessment > New Assessment page]

AI: "I see you're creating a new risk assessment. 
     Would you like to:
     • Use a template? (faster)
     • Import from spreadsheet? (bulk)
     • Start from scratch? (custom)
     
     Tip: Most users start with a template to save time."
```

---

## 7. Privacy & Security

### 7.1 Data Privacy

- **No PII in AI Context**: Personal identifiable information never sent to AI
- **Anonymization**: Data anonymized before analysis
- **Tenant Isolation**: AI has no cross-tenant data access (except Global mode with aggregated, anonymized data)
- **User Consent**: Users can opt-out of AI assistance

### 7.2 Security Measures

- **Encrypted Communication**: All AI API calls over HTTPS
- **Rate Limiting**: Prevent abuse
- **Audit Logging**: All AI interactions logged
- **Permission Checking**: AI respects user permissions
- **No Code Execution**: AI cannot execute code or modify data

---

## 8. Implementation Checklist

### Builder: UI-Builder

- [ ] Create AIToggleButton component
- [ ] Create AIPanelContainer component
- [ ] Create AIPanelHeader component
- [ ] Create ChatTab component
- [ ] Create ChatMessage component
- [ ] Create ChatInput component
- [ ] Create AlertsTab component
- [ ] Create HealthTab component
- [ ] Create ComplianceTab component
- [ ] Implement mode switching (Tenant/Admin/Global)
- [ ] Implement expand/collapse animations
- [ ] Implement mobile fullscreen mode
- [ ] Implement real-time updates (WebSocket)
- [ ] Implement AI chat API integration
- [ ] Implement notification system
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Accessibility audit

---

## 9. QA Gates

### Functional
- [ ] Panel opens/closes correctly
- [ ] All modes work correctly
- [ ] Chat interface functional
- [ ] Alerts update in real-time
- [ ] Mode switching works
- [ ] Mobile fullscreen works

### Accessibility
- [ ] WCAG 2.1 Level AA compliance
- [ ] Keyboard navigation (Alt+A to toggle)
- [ ] Screen reader compatible
- [ ] Focus management correct
- [ ] ARIA attributes present

### Performance
- [ ] Panel load time < 300ms
- [ ] Chat response time < 2s
- [ ] Real-time updates < 500ms lag
- [ ] Smooth animations (60fps)

### Security
- [ ] No PII sent to AI
- [ ] Tenant isolation enforced
- [ ] Permission checking works
- [ ] Audit logging functional

---

## 10. Dependencies

### External Dependencies
- OpenAI API (or equivalent LLM)
- WebSocket for real-time updates
- React 18+

### Internal Dependencies
- Theme system (see `theme-system.md`)
- Component library (see `component-library.md`)
- Layout system (see `layout.md`)
- Permission system
- Monitoring/logging infrastructure

---

## 11. Future Enhancements

- [ ] Detached/floating window mode
- [ ] Voice interface (speech-to-text, text-to-speech)
- [ ] Message threading
- [ ] File attachments (for AI analysis)
- [ ] Multi-language support
- [ ] Custom AI assistants per module

---

## 12. Versioning

**Current Version**: 1.0  
**Next Review**: Upon Wave 1.1 completion  
**Breaking Changes**: None yet

---

## 13. Governance

**Approval Required**: Yes  
**Approver**: Johan  
**Status**: DRAFT  

**Change Control**:
- AI capabilities require security review
- Data privacy changes require compliance review
- Breaking changes require major version bump

---

*Document prepared by: Maturion Foreman*  
*Date: 2025-12-04*  
*Build Wave: 1.1*
