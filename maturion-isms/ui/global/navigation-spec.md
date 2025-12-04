# Maturion ISMS – Navigation System Specification

**Version**: 1.0  
**Build Wave**: 1.1  
**Owner**: Maturion Foreman  
**Status**: DRAFT - AWAITING APPROVAL

---

## 1. Purpose

This document defines the navigation system architecture for the Maturion ISMS platform.

The navigation system provides:
- Consistent navigation across all modules
- ISMS module structure
- Permission-based visibility
- Active state management
- Breadcrumb navigation
- Search navigation
- Responsive mobile navigation

---

## 2. Navigation Architecture

### 2.1 Navigation Hierarchy

```
Root Navigation
├── Module Navigation (Sidebar)
│   ├── PIT (Personnel Information Tracker)
│   ├── ERM (Enterprise Risk Management)
│   ├── Risk Assessment
│   ├── Threat
│   ├── Vulnerability
│   ├── WRAC (Workforce Risk Assessment & Control)
│   ├── Course Crafter
│   ├── Policy Builder
│   ├── Analytics & Remote Assurance
│   ├── Auditor Mobile
│   └── Skills Development Portal
├── Utility Navigation (Sidebar Bottom)
│   ├── Settings
│   ├── Help & Support
│   └── Admin (if authorized)
└── User Navigation (Header Right)
    ├── Global Search
    ├── Notifications
    ├── Maturion AI Panel Toggle
    ├── Tenant Switcher (admin only)
    └── User Profile Menu
```

---

## 3. Module Navigation (Sidebar)

### 3.1 Module Structure

Each ISMS module has a consistent navigation pattern:

```typescript
interface ModuleDefinition {
  id: ModuleName;
  name: string;
  displayName: string;
  icon: string;
  route: string;
  permissions: Permission[];
  subModules?: SubModule[];
  badge?: BadgeInfo;
  enabled: boolean;
}

type ModuleName =
  | 'PIT'
  | 'ERM'
  | 'RISK_ASSESSMENT'
  | 'THREAT'
  | 'VULNERABILITY'
  | 'WRAC'
  | 'COURSE_CRAFTER'
  | 'POLICY_BUILDER'
  | 'ANALYTICS_REMOTE_ASSURANCE'
  | 'AUDITOR_MOBILE'
  | 'SKILLS_DEVELOPMENT_PORTAL';

interface SubModule {
  id: string;
  name: string;
  route: string;
  permissions?: Permission[];
  children?: SubModule[];
}

interface BadgeInfo {
  text: string;
  variant: 'default' | 'success' | 'warning' | 'error' | 'info';
}
```

### 3.2 Module List

#### PIT (Personnel Information Tracker)
```
/pit
├── /dashboard
├── /personnel
│   ├── /list
│   ├── /add
│   └── /import
├── /competencies
├── /certifications
├── /training
└── /reports
```

#### ERM (Enterprise Risk Management)
```
/erm
├── /dashboard
├── /risks
│   ├── /register
│   ├── /assessment
│   └── /treatment
├── /controls
├── /incidents
└── /reports
```

#### Risk Assessment
```
/risk-assessment
├── /dashboard
├── /assessments
│   ├── /list
│   ├── /new
│   └── /templates
├── /methodology
└── /reports
```

#### Threat
```
/threat
├── /dashboard
├── /threats
│   ├── /catalog
│   ├── /intelligence
│   └── /scenarios
├── /monitoring
└── /reports
```

#### Vulnerability
```
/vulnerability
├── /dashboard
├── /vulnerabilities
│   ├── /scans
│   ├── /registry
│   └── /remediation
├── /monitoring
└── /reports
```

#### WRAC (Workforce Risk Assessment & Control)
```
/wrac
├── /dashboard
├── /assessments
├── /controls
├── /monitoring
└── /reports
```

#### Course Crafter
```
/course-crafter
├── /dashboard
├── /courses
│   ├── /library
│   ├── /create
│   └── /templates
├── /assignments
└── /analytics
```

#### Policy Builder
```
/policy-builder
├── /dashboard
├── /policies
│   ├── /library
│   ├── /create
│   └── /templates
├── /compliance
└── /approvals
```

#### Analytics & Remote Assurance
```
/analytics-remote-assurance
├── /dashboard
├── /analytics
│   ├── /platform
│   ├── /compliance
│   └── /risk
├── /remote-assurance
└── /reports
```

#### Auditor Mobile
```
/auditor-mobile
├── /dashboard
├── /audits
│   ├── /schedule
│   ├── /fieldwork
│   └── /findings
├── /checklists
└── /reports
```

#### Skills Development Portal
```
/skills-development-portal
├── /dashboard
├── /my-skills
├── /learning-paths
├── /certifications
└── /progress
```

---

## 4. Navigation Component Specifications

### 4.1 Sidebar Navigation Component

```typescript
interface SidebarNavigationProps {
  modules: ModuleDefinition[];
  activeModule?: ModuleName;
  activeRoute: string;
  collapsed: boolean;
  onToggle: () => void;
  userPermissions: Permission[];
  tenantSubscription: ModuleName[];
}
```

**Features**:
- Hierarchical tree structure
- Expand/collapse sub-modules
- Active state highlighting (module & sub-module)
- Permission-based filtering
- Subscription-based filtering
- Icon + label (or icon only when collapsed)
- Smooth expand/collapse animation
- Keyboard navigation (Arrow keys, Enter, Escape)

**Visual States**:
- Default
- Hover
- Active (current module/page)
- Expanded (showing sub-modules)
- Collapsed (icon only)
- Disabled (no permission or subscription)

**Responsive Behavior**:
- Desktop (≥1024px): Sidebar visible, expanded by default
- Tablet (768-1024px): Sidebar visible, collapsed by default
- Mobile (<768px): Sidebar hidden, overlay when opened

---

### 4.2 Module Menu Item Component

```typescript
interface ModuleMenuItemProps {
  module: ModuleDefinition;
  active: boolean;
  collapsed: boolean;
  expanded: boolean;
  onToggle: () => void;
  onClick: () => void;
  hasPermission: boolean;
  isSubscribed: boolean;
}
```

**Layout**:
```
┌────────────────────────────────────────┐
│ [Icon]  Module Name              [>]  │  ← Not active
│ [Icon]  Module Name (Badge)      [v]  │  ← Active, expanded
│   └─ [Icon]  Sub-module               │  ← Sub-module
│   └─ [Icon]  Sub-module (Active)      │  ← Active sub-module
└────────────────────────────────────────┘

Collapsed mode:
┌─────┐
│ [I] │  ← Icon only
│ [I] │  ← Active (highlighted)
└─────┘
```

**Accessibility**:
- `role="navigation"` on sidebar
- `aria-label="Module navigation"` on sidebar
- `aria-current="page"` on active item
- `aria-expanded` on expandable items
- Keyboard navigation support

---

### 4.3 Breadcrumb Navigation Component

```typescript
interface BreadcrumbNavigationProps {
  items: BreadcrumbItem[];
  maxItems?: number;
  separator?: ReactNode;
}

interface BreadcrumbItem {
  label: string;
  route?: string;
  onClick?: () => void;
  icon?: ReactNode;
}
```

**Example**:
```
Home > Risk Assessment > Assessments > New Assessment
```

**Features**:
- Clickable items (except last)
- Truncation with ellipsis for long paths
- Responsive (collapse on mobile)
- Custom separator (default: `/` or `>`)

**Location**: Top of main content area, below header

---

### 4.4 Global Search Component

```typescript
interface GlobalSearchProps {
  onSearch: (query: string) => void;
  placeholder?: string;
  suggestions?: SearchSuggestion[];
  recentSearches?: string[];
}

interface SearchSuggestion {
  type: 'module' | 'page' | 'document' | 'person';
  title: string;
  route?: string;
  icon?: ReactNode;
}
```

**Features**:
- Keyboard shortcut: `Ctrl+/` or `Cmd+/`
- Autocomplete suggestions
- Recent searches
- Search across modules
- Type-ahead filtering
- Fuzzy matching

**Location**: Header (center-right)

**Responsive**:
- Desktop: Always visible
- Mobile: Icon only, expands to full search bar

---

### 4.5 User Profile Menu Component

```typescript
interface UserProfileMenuProps {
  user: User;
  menuItems: MenuItem[];
  onLogout: () => void;
}

interface MenuItem {
  label: string;
  icon?: ReactNode;
  onClick: () => void;
  divider?: boolean;
}

interface User {
  id: string;
  name: string;
  email: string;
  role: string;
  avatar?: string;
  organisation: {
    id: string;
    name: string;
  };
}
```

**Menu Items** (default):
```
┌──────────────────────────────────┐
│ [Avatar] John Doe                │
│          john.doe@example.com    │
│          Administrator           │
├──────────────────────────────────┤
│ [Icon] My Profile                │
│ [Icon] Account Settings          │
│ [Icon] Preferences               │
├──────────────────────────────────┤
│ [Icon] Dark Mode: On [Toggle]   │
├──────────────────────────────────┤
│ [Icon] Help & Support            │
│ [Icon] Keyboard Shortcuts        │
├──────────────────────────────────┤
│ [Icon] Logout                    │
└──────────────────────────────────┘
```

**Location**: Header (right)

---

### 4.6 Notification Center Component

```typescript
interface NotificationCenterProps {
  notifications: Notification[];
  unreadCount: number;
  onMarkAsRead: (id: string) => void;
  onMarkAllAsRead: () => void;
  onClear: (id: string) => void;
  onClearAll: () => void;
}

interface Notification {
  id: string;
  type: 'info' | 'success' | 'warning' | 'error';
  title: string;
  message: string;
  timestamp: Date;
  read: boolean;
  actionUrl?: string;
  actionLabel?: string;
}
```

**Features**:
- Badge with unread count
- Dropdown panel with notifications
- Mark as read (individual or all)
- Clear notifications (individual or all)
- Click to navigate to related page
- Real-time updates (via WebSocket or polling)

**Location**: Header (right, before user menu)

---

## 5. Permission-Based Navigation

### 5.1 Permission Model

```typescript
interface Permission {
  module: ModuleName;
  resource: string;
  action: 'read' | 'create' | 'update' | 'delete' | 'admin';
}

interface UserPermissions {
  user_id: string;
  organisation_id: string;
  permissions: Permission[];
  role: 'user' | 'manager' | 'admin' | 'super_admin';
}
```

### 5.2 Permission Checking

Navigation items are filtered based on:
1. **User Role**: Basic visibility by role
2. **Module Permissions**: Specific module access
3. **Tenant Subscription**: Modules enabled for tenant
4. **Feature Flags**: Beta features or gradual rollout

```typescript
function isModuleVisible(
  module: ModuleDefinition,
  userPermissions: Permission[],
  tenantSubscription: ModuleName[]
): boolean {
  // Check tenant subscription
  if (!tenantSubscription.includes(module.id)) {
    return false;
  }

  // Check user permissions
  const hasPermission = userPermissions.some(
    p => p.module === module.id && p.action === 'read'
  );

  return hasPermission && module.enabled;
}
```

---

## 6. Active State Management

### 6.1 Active Module Detection

The active module is determined by the current route:

```typescript
function getActiveModule(route: string): ModuleName | null {
  const routeSegments = route.split('/').filter(Boolean);
  const moduleSlug = routeSegments[0];
  return MODULE_SLUG_MAP[moduleSlug] || null;
}

const MODULE_SLUG_MAP: Record<string, ModuleName> = {
  'pit': 'PIT',
  'erm': 'ERM',
  'risk-assessment': 'RISK_ASSESSMENT',
  'threat': 'THREAT',
  'vulnerability': 'VULNERABILITY',
  'wrac': 'WRAC',
  'course-crafter': 'COURSE_CRAFTER',
  'policy-builder': 'POLICY_BUILDER',
  'analytics-remote-assurance': 'ANALYTICS_REMOTE_ASSURANCE',
  'auditor-mobile': 'AUDITOR_MOBILE',
  'skills-development-portal': 'SKILLS_DEVELOPMENT_PORTAL',
};
```

### 6.2 Active Sub-Module Detection

Active sub-module is determined by exact route match or route prefix:

```typescript
function getActiveSubModule(
  module: ModuleDefinition,
  route: string
): string | null {
  if (!module.subModules) return null;

  // Find exact match first
  const exactMatch = findSubModuleByRoute(module.subModules, route);
  if (exactMatch) return exactMatch.id;

  // Find by prefix match
  const prefixMatch = findSubModuleByPrefix(module.subModules, route);
  return prefixMatch?.id || null;
}
```

### 6.3 Breadcrumb Generation

Breadcrumbs are auto-generated based on route and module structure:

```typescript
function generateBreadcrumbs(
  route: string,
  modules: ModuleDefinition[]
): BreadcrumbItem[] {
  const items: BreadcrumbItem[] = [
    { label: 'Home', route: '/' }
  ];

  const activeModule = getActiveModule(route);
  if (!activeModule) return items;

  const module = modules.find(m => m.id === activeModule);
  if (!module) return items;

  items.push({
    label: module.displayName,
    route: module.route
  });

  // Add sub-module breadcrumbs
  const subModule = getActiveSubModule(module, route);
  if (subModule) {
    const subModulePath = findSubModulePath(module, subModule);
    subModulePath.forEach(sm => {
      items.push({
        label: sm.name,
        route: sm.route
      });
    });
  }

  return items;
}
```

---

## 7. Routing Strategy

### 7.1 Route Structure

```
/:module/:subModule?/:action?/:id?
```

**Examples**:
- `/pit/dashboard` - PIT Dashboard
- `/erm/risks/register` - ERM Risk Register
- `/risk-assessment/assessments/new` - New Risk Assessment
- `/threat/threats/catalog` - Threat Catalog
- `/vulnerability/scans/edit/123` - Edit Vulnerability Scan #123

### 7.2 Route Guards

```typescript
interface RouteGuard {
  path: string;
  permissions: Permission[];
  redirect?: string;
  beforeEnter?: (to: Route, from: Route) => boolean;
}
```

**Guard Types**:
- **Auth Guard**: User must be logged in
- **Permission Guard**: User must have specific permissions
- **Subscription Guard**: Tenant must have module subscription
- **Role Guard**: User must have specific role

---

## 8. Mobile Navigation

### 8.1 Mobile Menu (Hamburger)

On mobile (<768px):
- Sidebar hidden by default
- Hamburger icon in header (left)
- Sidebar slides in from left as overlay
- Backdrop dims background
- Close on backdrop click or close button
- Swipe gesture to close (future)

### 8.2 Mobile Breadcrumbs

On mobile:
- Collapse breadcrumbs to show only last 2 items
- First item replaced with `...` (tap to expand)

---

## 9. Keyboard Navigation

### 9.1 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+/` or `Cmd+/` | Focus global search |
| `Alt+1` | Navigate to first module (PIT) |
| `Alt+2` | Navigate to second module (ERM) |
| `Alt+N` | Open notifications |
| `Alt+U` | Open user menu |
| `Alt+S` | Open settings |
| `Alt+H` | Open help |
| `Esc` | Close dropdown/menu |

### 9.2 Sidebar Navigation Keys

| Key | Action |
|-----|--------|
| `Tab` | Move focus to next item |
| `Shift+Tab` | Move focus to previous item |
| `Arrow Up/Down` | Navigate between items |
| `Arrow Right` | Expand sub-module |
| `Arrow Left` | Collapse sub-module |
| `Enter` or `Space` | Select item |
| `Esc` | Close mobile sidebar |

---

## 10. Implementation Checklist

### Builder: UI-Builder

- [ ] Create SidebarNavigation component
- [ ] Create ModuleMenuItem component
- [ ] Create BreadcrumbNavigation component
- [ ] Create GlobalSearch component
- [ ] Create UserProfileMenu component
- [ ] Create NotificationCenter component
- [ ] Implement permission-based filtering
- [ ] Implement active state detection
- [ ] Implement breadcrumb auto-generation
- [ ] Implement routing guards
- [ ] Implement mobile navigation (hamburger menu)
- [ ] Implement keyboard shortcuts
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Accessibility audit

---

## 11. QA Gates

### Functional
- [ ] All navigation items render correctly
- [ ] Active states highlight correctly
- [ ] Permission filtering works
- [ ] Breadcrumbs generate correctly
- [ ] Mobile navigation works
- [ ] Search functionality works

### Accessibility
- [ ] WCAG 2.1 Level AA compliance
- [ ] Keyboard navigation works
- [ ] Screen reader compatible
- [ ] ARIA landmarks present
- [ ] Focus indicators visible

### Performance
- [ ] Navigation renders quickly (< 100ms)
- [ ] No unnecessary re-renders
- [ ] Smooth animations (60fps)

### Cross-Browser
- [ ] Chrome
- [ ] Firefox
- [ ] Safari
- [ ] Edge

---

## 12. Dependencies

### External Dependencies
- React Router v6+
- React 18+

### Internal Dependencies
- Theme system (see `theme-system.md`)
- Component library (see `component-library.md`)
- Layout system (see `layout.md`)
- Permission system (platform-level)

---

## 13. Versioning

**Current Version**: 1.0  
**Next Review**: Upon Wave 1.1 completion  
**Breaking Changes**: None yet

---

## 14. Governance

**Approval Required**: Yes  
**Approver**: Johan  
**Status**: DRAFT  

**Change Control**:
- Module structure changes require Foreman review
- Navigation patterns must remain consistent
- Breaking changes require major version bump

---

*Document prepared by: Maturion Foreman*  
*Date: 2025-12-04*  
*Build Wave: 1.1*
