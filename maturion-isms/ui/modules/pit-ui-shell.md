# PIT (Personnel Information Tracker) – UI Shell Specification

**Version**: 1.0  
**Build Wave**: 1.1  
**Module**: PIT  
**Owner**: Maturion Foreman  
**Status**: DRAFT - AWAITING APPROVAL

---

## 1. Module Overview

### Purpose
Personnel Information Tracker (PIT) manages employee data, competencies, certifications, and training records for the organization.

### Key User Personas
- **HR Manager**: Manages personnel records, training, certifications
- **Department Manager**: Views team data, assigns training
- **Employee**: Views own data, certificates, training progress
- **Admin**: System configuration, reporting

### Primary Workflows
1. Add/edit personnel records
2. Track competencies and skills
3. Manage certifications and renewals
4. Assign and track training
5. Generate personnel reports

---

## 2. Route Structure

```
/pit
├── /dashboard                    # Main dashboard
├── /personnel                    # Personnel management
│   ├── /list                     # All personnel list
│   ├── /add                      # Add new person
│   ├── /edit/:id                 # Edit person
│   ├── /view/:id                 # View person details
│   └── /import                   # Bulk import
├── /competencies                 # Competency management
│   ├── /list                     # Competency library
│   ├── /matrix                   # Skills matrix view
│   └── /gaps                     # Competency gap analysis
├── /certifications               # Certification tracking
│   ├── /list                     # All certifications
│   ├── /expiring                 # Expiring soon
│   └── /providers                # Certification providers
├── /training                     # Training management
│   ├── /list                     # All training records
│   ├── /assign                   # Assign training
│   ├── /schedule                 # Training schedule
│   └── /compliance               # Training compliance
├── /reports                      # Reporting
│   ├── /personnel                # Personnel reports
│   ├── /competency               # Competency reports
│   ├── /certification            # Certification reports
│   └── /training                 # Training reports
└── /settings                     # Module settings
    ├── /general                  # General settings
    ├── /fields                   # Custom fields
    └── /templates                # Document templates
```

---

## 3. Navigation Structure

### Sidebar Menu Items
```
📊 PIT
├── 📈 Dashboard
├── 👥 Personnel
│   ├── All Personnel
│   ├── Add New
│   └── Import
├── 🎯 Competencies
│   ├── Competency Library
│   ├── Skills Matrix
│   └── Gap Analysis
├── 📜 Certifications
│   ├── All Certifications
│   ├── Expiring Soon
│   └── Providers
├── 🎓 Training
│   ├── All Training
│   ├── Assign Training
│   ├── Schedule
│   └── Compliance
├── 📊 Reports
└── ⚙️  Settings
```

### Breadcrumb Patterns
- `Home > PIT > Dashboard`
- `Home > PIT > Personnel > All Personnel`
- `Home > PIT > Personnel > View Personnel > John Doe`
- `Home > PIT > Certifications > Expiring Soon`

---

## 4. Dashboard Shell

### Layout Structure
```
┌──────────────────────────────────────────────────────────────┐
│ PIT Dashboard                        [Export] [Settings]     │
├────────────┬────────────┬────────────┬──────────────────────┤
│ Total      │ Active     │ Certifi-   │ Training             │
│ Personnel  │ Personnel  │ cations    │ Compliance           │
│ 247        │ 234        │ 156 Active │ 92%                  │
│ [+5%]      │ [-2%]      │ [12 exp]   │ [+3%]                │
├────────────┴────────────┴────────────┴──────────────────────┤
│ Recent Activity                      │ Quick Actions        │
│ • John Doe added (5 min ago)         │ • Add Personnel      │
│ • Jane Smith cert renewed            │ • Assign Training    │
│ • Team Training completed (10 users) │ • View Reports       │
│ • 3 certifications expiring soon     │ • Import Data        │
├──────────────────────────────────────┴──────────────────────┤
│ Certification Status                                        │
│ [Pie Chart: Active, Expiring, Expired]                     │
├─────────────────────────────────────────────────────────────┤
│ Training Completion Trends                                  │
│ [Line Chart: Last 6 months]                                │
└─────────────────────────────────────────────────────────────┘
```

### Key Metrics
1. **Total Personnel**: Count of all personnel records
2. **Active Personnel**: Currently employed
3. **Certifications**: Active certifications count + expiring soon
4. **Training Compliance**: % of required training completed

### Widgets
- Recent Activity Feed
- Quick Actions Panel
- Certification Status Chart (Pie)
- Training Completion Trends (Line)
- Expiring Certifications Alert
- Competency Gap Summary

---

## 5. List View Shells

### Personnel List View

**Route**: `/pit/personnel/list`

**Layout**:
```
┌──────────────────────────────────────────────────────────────┐
│ All Personnel                          [+ Add] [Import] [↓]  │
├──────────────────────────────────────────────────────────────┤
│ 🔍 Search by name, email, ID...                              │
│ [Filter: Department ▼] [Filter: Status ▼] [Sort: Name ▼]    │
├──────────────────────────────────────────────────────────────┤
│ ☐  Name          Department    Position      Status  Actions│
│ ☐  John Doe      IT            Developer     Active  [···]  │
│ ☐  Jane Smith    HR            Manager       Active  [···]  │
│ ☐  Bob Johnson   Finance       Analyst       Active  [···]  │
│ ☐  Alice Brown   IT            Senior Dev    Active  [···]  │
├──────────────────────────────────────────────────────────────┤
│ [←] Page 1 of 10 [→]                 Showing 1-25 of 247    │
└──────────────────────────────────────────────────────────────┘
```

**Features**:
- Search (name, email, employee ID)
- Filters (department, status, position)
- Sort (name, department, hire date)
- Bulk actions (export, assign training, delete)
- Row actions (view, edit, delete, assign training)
- Pagination

**Columns**:
| Column | Description | Sortable | Filterable |
|--------|-------------|----------|------------|
| Checkbox | Bulk select | No | No |
| Name | Full name | Yes | Yes (search) |
| Department | Department name | Yes | Yes (dropdown) |
| Position | Job title | Yes | Yes (dropdown) |
| Status | Active/Inactive | Yes | Yes (toggle) |
| Actions | Row actions | No | No |

---

### Competencies List View

**Route**: `/pit/competencies/list`

**Layout**:
```
┌──────────────────────────────────────────────────────────────┐
│ Competency Library                    [+ Add] [Matrix] [↓]   │
├──────────────────────────────────────────────────────────────┤
│ 🔍 Search competencies...                                    │
│ [Filter: Category ▼] [Filter: Level ▼]                      │
├──────────────────────────────────────────────────────────────┤
│ Competency Name    Category      Level      Personnel  Actions│
│ React Development  Technical     Expert     23         [···]  │
│ Project Mgmt       Soft Skills   Advanced   45         [···]  │
│ Risk Analysis      Technical     Inter...   12         [···]  │
├──────────────────────────────────────────────────────────────┤
│ [←] Page 1 of 5 [→]                   Showing 1-25 of 87    │
└──────────────────────────────────────────────────────────────┘
```

---

### Certifications List View

**Route**: `/pit/certifications/list`

**Layout**:
```
┌──────────────────────────────────────────────────────────────┐
│ All Certifications               [+ Add] [Expiring] [↓]      │
├──────────────────────────────────────────────────────────────┤
│ 🔍 Search certifications...                                  │
│ [Filter: Status ▼] [Filter: Provider ▼]                     │
├──────────────────────────────────────────────────────────────┤
│ ☐  Certification     Personnel   Issue Date  Expiry  Status │
│ ☐  CISSP             John Doe    2022-03-15  2025-03 Active │
│ ☐  PMP               Jane Smith  2023-06-20  2026-06 Active │
│ ☐  AWS Certified     Bob J.      2021-09-10  2024-09 Expiring│
├──────────────────────────────────────────────────────────────┤
│ [←] Page 1 of 8 [→]                  Showing 1-25 of 156    │
└──────────────────────────────────────────────────────────────┘
```

---

## 6. Detail View Shells

### Personnel Detail View

**Route**: `/pit/personnel/view/:id`

**Layout**:
```
┌──────────────────────────────────────────────────────────────┐
│ [← Back] John Doe              [Edit] [Delete] [Assign] [···]│
├──────────────────────────────────────────────────────────────┤
│ Details │ Competencies │ Certifications │ Training │ History │
├──────────────────────────────────────────────────────────────┤
│ Personal Information                                         │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Employee ID:    EMP-001234                               │ │
│ │ Email:          john.doe@example.com                     │ │
│ │ Department:     IT                                       │ │
│ │ Position:       Senior Developer                         │ │
│ │ Hire Date:      2020-01-15                              │ │
│ │ Status:         Active                                   │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                              │
│ Contact Information                                          │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Phone:          +27 123 456 789                          │ │
│ │ Mobile:         +27 987 654 321                          │ │
│ │ Address:        123 Main St, Cape Town                   │ │
│ └──────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

**Tabs**:
1. **Details**: Personal & contact information
2. **Competencies**: Skills matrix, competency levels
3. **Certifications**: Current & expired certifications
4. **Training**: Completed & assigned training
5. **History**: Activity log, changes, notes

---

## 7. Settings View Shell

**Route**: `/pit/settings`

**Layout**:
```
┌──────────────────────────────────────────────────────────────┐
│ PIT Settings                                     [Save]      │
├──────────────────────────────────────────────────────────────┤
│ General │ Custom Fields │ Templates │ Notifications │ Import │
├──────────────────────────────────────────────────────────────┤
│ General Settings                                             │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Module Enabled:       [✓] Yes                            │ │
│ │ Certification Alert:  [30] days before expiry            │ │
│ │ Training Compliance:  [90] % minimum threshold           │ │
│ │ Auto-Archive:         [✓] Archive after 2 years inactive │ │
│ └──────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

---

## 8. Reports View Shell

**Route**: `/pit/reports`

**Layout**:
```
┌──────────────────────────────────────────────────────────────┐
│ PIT Reports                                      [Generate]  │
├──────────────────────────────────────────────────────────────┤
│ Report Type                                                  │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ ○ Personnel Summary                                       │ │
│ │ ○ Competency Matrix                                       │ │
│ │ ○ Certification Status                                    │ │
│ │ ○ Training Compliance                                     │ │
│ │ ○ Custom Report                                           │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                              │
│ Filters                                                      │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Department:     [All Departments ▼]                       │ │
│ │ Date Range:     [Last 6 months ▼]                        │ │
│ │ Status:         [All Statuses ▼]                         │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                              │
│ Export Format                                                │
│ [PDF] [Excel] [CSV]                           [Generate]    │
└──────────────────────────────────────────────────────────────┘
```

---

## 9. UI Components

### PIT-Specific Components

#### 1. Personnel Card Component
```typescript
interface PersonnelCardProps {
  person: PersonnelData;
  onView: () => void;
  onEdit: () => void;
  compact?: boolean;
}
```
Displays personnel summary with avatar, name, position, status.

#### 2. Competency Badge Component
```typescript
interface CompetencyBadgeProps {
  competency: string;
  level: 'Beginner' | 'Intermediate' | 'Advanced' | 'Expert';
  verified: boolean;
}
```
Color-coded badge showing competency and proficiency level.

#### 3. Certification Status Component
```typescript
interface CertificationStatusProps {
  certification: CertificationData;
  showExpiry: boolean;
}
```
Shows certification with status indicator (active, expiring, expired).

#### 4. Skills Matrix Component
```typescript
interface SkillsMatrixProps {
  personnel: PersonnelData[];
  competencies: CompetencyData[];
  editable: boolean;
}
```
Interactive grid showing personnel vs. competencies.

#### 5. Training Progress Component
```typescript
interface TrainingProgressProps {
  training: TrainingData;
  progress: number;
  dueDate: Date;
}
```
Progress bar with completion percentage and deadline.

---

## 10. Responsive Behavior

### Mobile (<768px)
- **Dashboard**: Single column, stacked metrics
- **List Views**: Show only name, status, actions (tap to expand)
- **Detail Views**: Full-screen, tab navigation at bottom
- **Filters**: Collapsible sidebar or bottom sheet

### Tablet (768-1024px)
- **Dashboard**: 2-column grid
- **List Views**: Show key columns, hide secondary data
- **Detail Views**: Tabs at top, 2-column form layout

### Desktop (>1024px)
- **Dashboard**: 4-column grid, full widgets
- **List Views**: All columns visible, inline filters
- **Detail Views**: Tabs at top, 3-column layout with sidebar

---

## 11. Accessibility

- All forms have proper labels
- Keyboard navigation (Tab, Enter, Escape)
- Screen reader friendly (ARIA labels)
- High contrast mode support
- Focus indicators visible
- Error messages descriptive

---

## 12. Implementation Checklist

### Builder: UI-Builder

- [ ] Dashboard component
- [ ] Personnel list view
- [ ] Personnel detail view
- [ ] Personnel add/edit form
- [ ] Competencies list view
- [ ] Competencies matrix view
- [ ] Certifications list view
- [ ] Certifications detail view
- [ ] Training list view
- [ ] Training assignment interface
- [ ] Reports interface
- [ ] Settings interface
- [ ] Personnel card component
- [ ] Competency badge component
- [ ] Certification status component
- [ ] Skills matrix component
- [ ] Training progress component
- [ ] Route configuration
- [ ] Navigation integration
- [ ] Responsive layouts
- [ ] Accessibility compliance
- [ ] Unit tests
- [ ] Integration tests

---

## 13. Dependencies

- Global layout (`layout.md`)
- Component library (`component-library.md`)
- Theme system (`theme-system.md`)
- Navigation (`navigation-spec.md`)

---

## 14. Governance

**Approval Required**: Yes  
**Approver**: Johan  
**Status**: DRAFT

---

*Document prepared by: Maturion Foreman*  
*Date: 2025-12-04*  
*Build Wave: 1.1*
