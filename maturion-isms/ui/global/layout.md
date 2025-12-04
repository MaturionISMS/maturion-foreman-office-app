# Maturion ISMS – Global UI Layout Specification

**Version**: 1.0  
**Build Wave**: 1.1  
**Owner**: Maturion Foreman  
**Status**: DRAFT - AWAITING APPROVAL

---

## 1. Purpose

This document defines the global layout architecture for the Maturion Integrated Security Management System (ISMS) platform.

The global layout provides:
- Consistent visual structure across all modules
- Responsive grid system
- Navigation framework
- Content regions and containers
- Accessibility-first design
- Multi-tenant branding support

---

## 2. Layout Architecture

### 2.1 Core Layout Regions

The platform uses a fixed set of layout regions:

```
┌─────────────────────────────────────────────────────────────┐
│                      HEADER (Fixed)                          │
│  [Logo] [Module Nav] [Search] [Notifications] [User Menu]   │
├──────────┬──────────────────────────────────────────────────┤
│          │                                                   │
│ SIDEBAR  │           MAIN CONTENT AREA                      │
│ (Fixed/  │                                                   │
│ Collap-  │  ┌─────────────────────────────────────────┐    │
│ sible)   │  │  MODULE CONTENT                          │    │
│          │  │                                           │    │
│ Module   │  │                                           │    │
│ Menu     │  │                                           │    │
│          │  │                                           │    │
│          │  └─────────────────────────────────────────┘    │
│          │                                                   │
├──────────┴──────────────────────────────────────────────────┤
│                     FOOTER (Fixed)                           │
│  [Copyright] [Version] [Support] [Privacy] [Terms]          │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Region Specifications

#### Header Region
- **Height**: 64px (fixed)
- **Background**: Theme primary color
- **Z-index**: 1000
- **Position**: Fixed top
- **Content**:
  - Logo/branding (left, max 200px)
  - Module selector/breadcrumb (left-center)
  - Global search (center-right)
  - Notification center icon (right)
  - User profile dropdown (right)
  - Maturion AI toggle (right)
  - Tenant switcher (right, admin only)

#### Sidebar Region
- **Width**: 240px (expanded), 64px (collapsed)
- **Background**: Theme sidebar color
- **Z-index**: 900
- **Position**: Fixed left
- **Behavior**: Collapsible via toggle button
- **Content**:
  - Module navigation tree
  - Sub-module links
  - Collapse/expand toggle
  - Bottom: Settings, Help, Admin (if applicable)

#### Main Content Area
- **Width**: Fluid (calc(100% - sidebar width))
- **Background**: Theme background color
- **Padding**: 24px
- **Min-height**: calc(100vh - header height - footer height)
- **Overflow**: Auto (vertical scroll)
- **Content**:
  - Module-specific content
  - Dynamic routing based on module
  - Respects module UI specifications

#### Footer Region
- **Height**: 48px (fixed)
- **Background**: Theme footer color
- **Z-index**: 800
- **Position**: Fixed bottom
- **Content**:
  - Copyright notice
  - Version information
  - Support/Help links
  - Privacy Policy link
  - Terms of Service link

---

## 3. Responsive Grid System

### 3.1 Breakpoints

Following industry-standard breakpoints:

| Breakpoint | Size | Behavior |
|------------|------|----------|
| **xs** | < 576px | Mobile portrait |
| **sm** | 576px - 768px | Mobile landscape |
| **md** | 768px - 992px | Tablet portrait |
| **lg** | 992px - 1200px | Tablet landscape / Small desktop |
| **xl** | 1200px - 1600px | Desktop |
| **xxl** | > 1600px | Large desktop |

### 3.2 Grid Specifications

- **Columns**: 12-column system
- **Gutter**: 16px (xs-md), 24px (lg+)
- **Container Max Width**: 
  - sm: 540px
  - md: 720px
  - lg: 960px
  - xl: 1140px
  - xxl: 1400px

### 3.3 Responsive Behavior

#### Mobile (xs, sm)
- Sidebar: Hidden by default, overlay when opened
- Header: Simplified, hamburger menu
- Content: Full width, single column
- Footer: Sticky bottom

#### Tablet (md, lg)
- Sidebar: Collapsible, narrow mode default
- Header: Full features
- Content: Adaptive multi-column
- Footer: Full width

#### Desktop (xl, xxl)
- Sidebar: Expanded by default
- Header: Full features with search
- Content: Multi-column layouts
- Footer: Full width

---

## 4. Z-Index Hierarchy

To prevent stacking conflicts:

| Component | Z-Index | Purpose |
|-----------|---------|---------|
| Modals | 2000 | Highest - overlay everything |
| Toasts/Notifications | 1500 | Above dialogs |
| Dialogs | 1200 | Above fixed elements |
| Dropdowns | 1100 | Above navigation |
| Header | 1000 | Fixed navigation |
| Sidebar | 900 | Fixed navigation |
| Footer | 800 | Fixed footer |
| Sticky elements | 500 | Content-level sticky |
| Base content | 1 | Default content layer |

---

## 5. Accessibility Requirements

### 5.1 WCAG 2.1 Level AA Compliance

All layout components must meet:

- **Perceivable**: 
  - Text contrast ratio ≥ 4.5:1 for normal text
  - Text contrast ratio ≥ 3:1 for large text
  - All interactive elements have visible focus indicators

- **Operable**:
  - All functionality available via keyboard
  - Skip navigation links provided
  - Focus order is logical
  - No keyboard traps

- **Understandable**:
  - Clear navigation labels
  - Predictable navigation behavior
  - Error identification and suggestions

- **Robust**:
  - Valid HTML5 semantic markup
  - ARIA landmarks for all regions
  - ARIA labels where needed

### 5.2 Semantic HTML Requirements

```html
<header role="banner">
  <nav role="navigation" aria-label="Primary">...</nav>
</header>

<aside role="complementary" aria-label="Module navigation">
  <nav role="navigation" aria-label="Module">...</nav>
</aside>

<main role="main" aria-label="Main content">
  <!-- Module content -->
</main>

<footer role="contentinfo">
  <!-- Footer content -->
</footer>
```

### 5.3 Keyboard Navigation

- **Tab**: Move focus forward
- **Shift+Tab**: Move focus backward
- **Esc**: Close modals/dialogs/dropdowns
- **Arrow keys**: Navigate within menus
- **Enter/Space**: Activate controls
- **Ctrl+/**: Global search focus

---

## 6. Layout Components

### 6.1 Header Component

**Specification**:
```typescript
interface HeaderProps {
  tenantLogo?: string;
  tenantName: string;
  currentModule?: ModuleName;
  currentUser: User;
  notificationCount: number;
  showTenantSwitch: boolean;
  showAIPanel: boolean;
}
```

**Features**:
- Responsive logo display
- Module breadcrumb navigation
- Global search (debounced, min 3 chars)
- Notification center (with unread count)
- User profile menu (avatar, name, role, logout)
- Maturion AI panel toggle
- Tenant switcher (admin/super admin only)

### 6.2 Sidebar Component

**Specification**:
```typescript
interface SidebarProps {
  modules: ModuleDefinition[];
  activeModule?: ModuleName;
  collapsed: boolean;
  onToggle: () => void;
  userPermissions: Permission[];
}
```

**Features**:
- Hierarchical module navigation
- Active state indication
- Collapse/expand functionality
- Permission-based visibility
- Bottom utility links (Settings, Help, Admin)
- Responsive behavior (overlay on mobile)

### 6.3 Content Container

**Specification**:
```typescript
interface ContentContainerProps {
  children: React.ReactNode;
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | 'xxl' | 'fluid';
  padding?: 'none' | 'sm' | 'md' | 'lg';
}
```

**Features**:
- Fluid width with optional max-width
- Configurable padding
- Scroll behavior management
- Print-friendly layout

### 6.4 Footer Component

**Specification**:
```typescript
interface FooterProps {
  version: string;
  environment: 'dev' | 'staging' | 'production';
  supportEmail?: string;
}
```

**Features**:
- Copyright notice (dynamic year)
- Version display
- Environment indicator (non-production)
- Support/Help links
- Legal links (Privacy, Terms)

---

## 7. Theme Integration

### 7.1 Layout Theme Variables

```css
--layout-header-height: 64px;
--layout-sidebar-width: 240px;
--layout-sidebar-collapsed-width: 64px;
--layout-footer-height: 48px;
--layout-content-padding: 24px;

--layout-bg-primary: var(--theme-bg-primary);
--layout-bg-secondary: var(--theme-bg-secondary);
--layout-text-primary: var(--theme-text-primary);
--layout-text-secondary: var(--theme-text-secondary);

--layout-border-color: var(--theme-border-color);
--layout-shadow: var(--theme-shadow-md);
```

### 7.2 Dark Mode Support

All layout components must support dark mode via CSS custom properties:

- Background colors automatically switch
- Text colors maintain contrast ratios
- Shadows adjust for dark backgrounds
- Focus indicators remain visible

---

## 8. Performance Requirements

### 8.1 Initial Load

- **Time to Interactive**: < 2 seconds
- **Largest Contentful Paint (LCP)**: < 2.5 seconds
- **Cumulative Layout Shift (CLS)**: < 0.1
- **First Input Delay (FID)**: < 100ms

### 8.2 Runtime Performance

- **Sidebar toggle animation**: < 300ms, 60fps
- **Navigation transition**: < 200ms
- **Scroll performance**: 60fps minimum
- **Memory**: < 50MB for layout alone

### 8.3 Optimization Strategies

- Lazy load sidebar menu items
- Virtualize long navigation lists
- Use CSS transforms for animations
- Minimize re-renders via React.memo
- Use CSS Grid/Flexbox (no JavaScript layout)

---

## 9. Multi-Tenancy Support

### 9.1 Tenant Branding

Layout must support per-tenant customization:

- **Logo**: Custom tenant logo in header
- **Colors**: Theme-based color overrides
- **Typography**: Optional custom fonts
- **Footer text**: Custom copyright/support info

### 9.2 Tenant Isolation

- All tenant data rendered client-side must be scoped by `organisation_id`
- No cross-tenant data leakage in UI state
- Navigation menus filtered by tenant permissions
- Module visibility based on tenant subscription

---

## 10. Print Layout

### 10.1 Print Styles

When printing:

- Hide: Header, Sidebar, Footer, AI Panel
- Show: Main content only
- Apply print-specific styles (white background, black text)
- Remove shadows and borders
- Optimize for A4/Letter paper

```css
@media print {
  header, aside, footer, .ai-panel { display: none; }
  main { width: 100%; padding: 0; }
  body { background: white; color: black; }
}
```

---

## 11. Implementation Checklist

### Builder: UI-Builder

- [ ] Create Header component with all features
- [ ] Create Sidebar component with collapse/expand
- [ ] Create ContentContainer component
- [ ] Create Footer component
- [ ] Implement responsive grid system
- [ ] Implement theme integration
- [ ] Implement dark mode support
- [ ] Implement accessibility features (WCAG 2.1 AA)
- [ ] Implement keyboard navigation
- [ ] Implement print styles
- [ ] Implement multi-tenancy support
- [ ] Create layout storybook/documentation
- [ ] Write unit tests for layout components
- [ ] Write integration tests for layout behavior
- [ ] Performance testing and optimization

---

## 12. QA Gates

### Functional
- [ ] All layout regions render correctly
- [ ] Sidebar collapses/expands smoothly
- [ ] Responsive behavior works across all breakpoints
- [ ] Navigation is functional
- [ ] Dark mode toggles correctly

### Accessibility
- [ ] WCAG 2.1 Level AA compliance verified
- [ ] Keyboard navigation works completely
- [ ] Screen reader compatibility tested
- [ ] Focus indicators visible
- [ ] ARIA landmarks present

### Performance
- [ ] LCP < 2.5s
- [ ] CLS < 0.1
- [ ] FID < 100ms
- [ ] Animations run at 60fps
- [ ] Memory usage acceptable

### Cross-Browser
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)

---

## 13. Dependencies

### External Dependencies
- React 18+
- CSS Grid / Flexbox support
- CSS Custom Properties support

### Internal Dependencies
- Theme system (see `theme-system.md`)
- Component library (see `component-library.md`)
- Navigation spec (see `navigation-spec.md`)

---

## 14. Versioning

**Current Version**: 1.0  
**Next Review**: Upon Wave 1.1 completion  
**Breaking Changes**: None yet

---

## 15. Governance

**Approval Required**: Yes  
**Approver**: Johan  
**Status**: DRAFT  

**Change Control**:
- Any changes to core layout structure require Foreman review
- Breaking changes require major version bump
- Must maintain backward compatibility

---

*Document prepared by: Maturion Foreman*  
*Date: 2025-12-04*  
*Build Wave: 1.1*
