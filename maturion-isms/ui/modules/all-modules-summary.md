# All Modules – UI Shell Specifications Summary

**Version**: 1.0  
**Build Wave**: 1.1  
**Owner**: Maturion Foreman  
**Status**: DRAFT - AWAITING APPROVAL

---

## Overview

This document provides concise UI shell specifications for all 11 ISMS modules (excluding PIT which has its own detailed spec).

All modules follow the same structural patterns defined in `README.md` with module-specific routes, navigation, and components.

---

## 1. ERM (Enterprise Risk Management)

### Routes
```
/erm
├── /dashboard
├── /risks
│   ├── /register                # Risk register
│   ├── /assessment              # Risk assessments
│   ├── /treatment               # Treatment plans
│   └── /view/:id                # Risk details
├── /controls
│   ├── /list                    # All controls
│   └── /effectiveness           # Control effectiveness
├── /incidents
│   ├── /list                    # All incidents
│   └── /report                  # Report incident
├── /reports
└── /settings
```

### Key Features
- Risk register with heat map visualization
- Risk assessment workflows
- Control effectiveness tracking
- Incident management
- Bow-tie diagram visualization

### Module-Specific Components
- `RiskHeatMap`: Visual risk matrix
- `RiskCard`: Risk summary card
- `ControlCard`: Control information card
- `BowTieD iagram`: Cause-effect visualization
- `IncidentTimeline`: Incident history

---

## 2. Risk Assessment

### Routes
```
/risk-assessment
├── /dashboard
├── /assessments
│   ├── /list                    # All assessments
│   ├── /new                     # New assessment
│   ├── /view/:id                # Assessment details
│   └── /templates               # Assessment templates
├── /methodology
│   ├── /frameworks              # Risk frameworks
│   └── /scoring                 # Scoring methodology
├── /reports
└── /settings
```

### Key Features
- Multiple risk assessment methodologies
- Template-based assessments
- Risk scoring and rating
- Assessment workflows (draft, review, approve)
- Comparison and trending

### Module-Specific Components
- `AssessmentWorkflow`: Multi-step assessment wizard
- `RiskScoreCalculator`: Interactive risk scoring
- `MethodologySelector`: Framework selection
- `AssessmentComparison`: Side-by-side comparison

---

## 3. Threat

### Routes
```
/threat
├── /dashboard
├── /threats
│   ├── /catalog                 # Threat catalog
│   ├── /intelligence            # Threat intelligence feeds
│   ├── /scenarios               # Threat scenarios
│   └── /view/:id                # Threat details
├── /monitoring
│   ├── /alerts                  # Threat alerts
│   └── /indicators              # Indicators of compromise
├── /reports
└── /settings
```

### Key Features
- Threat catalog (STRIDE, MITRE ATT&CK)
- Threat intelligence integration
- Scenario modeling
- Real-time threat monitoring
- IoC (Indicators of Compromise) tracking

### Module-Specific Components
- `ThreatCatalog`: Browsable threat library
- `ThreatIntelFeed`: Intelligence feed display
- `ScenarioBuilder`: Threat scenario creator
- `ThreatLandscape`: Visual threat overview
- `IoC Indicator`: Compromise indicator display

---

## 4. Vulnerability

### Routes
```
/vulnerability
├── /dashboard
├── /vulnerabilities
│   ├── /scans                   # Vulnerability scans
│   ├── /registry                # Vulnerability registry
│   ├── /remediation             # Remediation plans
│   └── /view/:id                # Vulnerability details
├── /monitoring
│   ├── /active                  # Active monitoring
│   └── /alerts                  # Vulnerability alerts
├── /reports
└── /settings
```

### Key Features
- Vulnerability scanning integration
- CVE database integration
- Remediation tracking
- SLA management
- Vulnerability scoring (CVSS)

### Module-Specific Components
- `VulnerabilityScannerStatus`: Scan status dashboard
- `CVSSScoreDisplay`: CVSS score visualization
- `RemediationPlan`: Remediation workflow
- `VulnerabilityTrend`: Trend analysis chart
- `PatchStatus`: Patch management status

---

## 5. WRAC (Workforce Risk Assessment & Control)

### Routes
```
/wrac
├── /dashboard
├── /assessments
│   ├── /list                    # Workforce assessments
│   ├── /new                     # New assessment
│   └── /view/:id                # Assessment details
├── /controls
│   ├── /list                    # Workforce controls
│   └── /monitoring              # Control monitoring
├── /monitoring
│   ├── /workforce-health        # Workforce health metrics
│   └── /alerts                  # Workforce alerts
├── /reports
└── /settings
```

### Key Features
- Workforce risk assessment
- Control effectiveness monitoring
- Workforce health dashboards
- Compliance tracking
- Risk trend analysis

### Module-Specific Components
- `WorkforceRiskMatrix`: Risk assessment matrix
- `ControlEffectivenessGauge`: Control performance
- `WorkforceHealthDashboard`: Health metrics
- `ComplianceTracker`: Compliance status

---

## 6. Course Crafter

### Routes
```
/course-crafter
├── /dashboard
├── /courses
│   ├── /library                 # Course library
│   ├── /create                  # Create course
│   ├── /edit/:id                # Edit course
│   ├── /view/:id                # Course details
│   └── /templates               # Course templates
├── /assignments
│   ├── /list                    # All assignments
│   └── /assign                  # Assign course
├── /analytics
│   ├── /completion              # Completion rates
│   └── /engagement              # Engagement metrics
└── /settings
```

### Key Features
- Course builder (WYSIWYG)
- Template library
- Course assignment
- Progress tracking
- Analytics and reporting

### Module-Specific Components
- `CourseBuilder`: Drag-and-drop course editor
- `ModuleEditor`: Course module creator
- `QuizBuilder`: Assessment creator
- `ProgressTracker`: Student progress
- `EngagementChart`: Engagement analytics

---

## 7. Policy Builder

### Routes
```
/policy-builder
├── /dashboard
├── /policies
│   ├── /library                 # Policy library
│   ├── /create                  # Create policy
│   ├── /edit/:id                # Edit policy
│   ├── /view/:id                # Policy details
│   └── /templates               # Policy templates
├── /compliance
│   ├── /mapping                 # Compliance mapping
│   └── /gaps                    # Compliance gaps
├── /approvals
│   ├── /pending                 # Pending approvals
│   └── /history                 # Approval history
└── /settings
```

### Key Features
- Policy document builder
- Template library (ISO, NIST, GDPR)
- Version control
- Approval workflows
- Compliance mapping

### Module-Specific Components
- `PolicyEditor`: Rich text policy editor
- `TemplateSelector`: Template browser
- `VersionControl`: Version history
- `ApprovalWorkflow`: Approval process tracker
- `ComplianceMapper`: Policy-to-framework mapper

---

## 8. Analytics & Remote Assurance

### Routes
```
/analytics-remote-assurance
├── /dashboard
├── /analytics
│   ├── /platform                # Platform analytics
│   ├── /compliance              # Compliance analytics
│   ├── /risk                    # Risk analytics
│   └── /custom                  # Custom dashboards
├── /remote-assurance
│   ├── /assessments             # Remote assessments
│   ├── /monitoring              # Continuous monitoring
│   └── /reports                 # Assurance reports
├── /reports
└── /settings
```

### Key Features
- Real-time analytics dashboards
- Custom dashboard builder
- Remote assurance monitoring
- Automated reporting
- Data visualization

### Module-Specific Components
- `AnalyticsDashboard`: Customizable dashboard
- `ChartBuilder`: Chart configuration tool
- `DataExplorer`: Data query interface
- `RemoteMonitor`: Live monitoring display
- `ReportScheduler`: Automated report scheduler

---

## 9. Auditor Mobile

### Routes
```
/auditor-mobile
├── /dashboard
├── /audits
│   ├── /schedule                # Audit schedule
│   ├── /fieldwork               # Active audits
│   ├── /findings                # Audit findings
│   └── /view/:id                # Audit details
├── /checklists
│   ├── /library                 # Checklist library
│   ├── /create                  # Create checklist
│   └── /view/:id                # Checklist details
├── /reports
└── /settings
```

### Key Features
- Mobile-optimized audit interface
- Offline mode support
- Photo capture and annotation
- GPS tagging
- Checklist management

### Module-Specific Components
- `AuditChecklist`: Interactive checklist
- `FindingCapture`: Finding entry form
- `PhotoAnnotator`: Image annotation tool
- `GPSTracker`: Location tracker
- `OfflineSync`: Sync status indicator

---

## 10. Skills Development Portal

### Routes
```
/skills-development-portal
├── /dashboard
├── /my-skills
│   ├── /current                 # Current skills
│   ├── /assessment              # Self-assessment
│   └── /goals                   # Skill goals
├── /learning-paths
│   ├── /browse                  # Browse paths
│   ├── /recommended             # Recommended for me
│   └── /view/:id                # Path details
├── /certifications
│   ├── /available               # Available certifications
│   ├── /in-progress             # In progress
│   └── /earned                  # Earned certifications
├── /progress
│   ├── /overview                # Progress overview
│   └── /achievements            # Achievements and badges
└── /settings
```

### Key Features
- Personal skill inventory
- Learning path recommendations
- Certification tracking
- Gamification (badges, achievements)
- Progress analytics

### Module-Specific Components
- `SkillsInventory`: Personal skills list
- `LearningPathCard`: Learning path display
- `ProgressCircle`: Circular progress indicator
- `BadgeDisplay`: Achievement badge
- `RecommendationEngine`: Skill recommendations

---

## Common Implementation Guidelines

### All Modules Must Include:

#### 1. Dashboard
- 4 key metrics (top row)
- Recent activity feed
- Quick actions panel
- 2-3 visualizations (charts/graphs)
- Alert/notification area

#### 2. List Views
- Search functionality
- Column filters
- Sort options
- Pagination
- Bulk actions
- Export functionality

#### 3. Detail Views
- Tabbed interface (3-5 tabs)
- Edit/delete/share actions
- Activity history
- Related data
- Back navigation

#### 4. Forms
- Field validation
- Error messages
- Help text
- Save/cancel actions
- Draft save (auto-save)

#### 5. Reports
- Report type selector
- Filter options
- Date range picker
- Export formats (PDF, Excel, CSV)
- Schedule option

### Responsive Breakpoints
- Mobile: < 768px (single column, simplified)
- Tablet: 768-1024px (2 columns, condensed)
- Desktop: > 1024px (full layout, all features)

### Accessibility
- WCAG 2.1 Level AA compliance
- Keyboard navigation
- Screen reader support
- Focus indicators
- High contrast mode
- Alt text for images

---

## Integration Points

### All Modules Integrate With:
- **Global Navigation**: Sidebar, breadcrumbs
- **Theme System**: Colors, typography, spacing
- **Component Library**: All UI components
- **Maturion AI Panel**: Contextual help, insights
- **Notification System**: Alerts, toasts
- **Permission System**: Role-based access
- **Search**: Global and module-specific

---

## Testing Requirements

### Each Module Must Have:
- [ ] Unit tests (components, utilities)
- [ ] Integration tests (routes, workflows)
- [ ] E2E tests (critical paths)
- [ ] Accessibility tests (axe, WAVE)
- [ ] Visual regression tests (screenshots)
- [ ] Performance tests (load time, render time)
- [ ] Mobile tests (responsive behavior)

---

## Implementation Priority

### Phase 1 (High Priority)
1. PIT
2. ERM
3. Risk Assessment

### Phase 2 (Medium Priority)
4. Threat
5. Vulnerability
6. WRAC

### Phase 3 (Standard Priority)
7. Course Crafter
8. Policy Builder
9. Analytics & Remote Assurance

### Phase 4 (Future)
10. Auditor Mobile
11. Skills Development Portal

---

## Governance

**Approval Required**: Yes  
**Approver**: Johan  
**Status**: DRAFT

**Change Control**:
- Module structure changes require Foreman review
- Must maintain consistency across all modules
- Breaking changes require major version bump

---

*Document prepared by: Maturion Foreman*  
*Date: 2025-12-04*  
*Build Wave: 1.1*
