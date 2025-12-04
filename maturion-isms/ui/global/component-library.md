# Maturion ISMS – Global Component Library Specification

**Version**: 1.0  
**Build Wave**: 1.1  
**Owner**: Maturion Foreman  
**Status**: DRAFT - AWAITING APPROVAL

---

## 1. Purpose

This document defines the global reusable component library for the Maturion ISMS platform.

The component library provides:
- Consistent UI patterns across all modules
- Reusable, accessible components
- Form elements and controls
- Data display components
- Feedback and notification components
- Navigation components

---

## 2. Component Architecture

### 2.1 Component Principles

1. **Accessibility First**: All components meet WCAG 2.1 Level AA
2. **Theme-Aware**: All components respect theme system
3. **Responsive**: All components adapt to screen sizes
4. **Type-Safe**: Full TypeScript definitions
5. **Tested**: Unit and integration tests for all components
6. **Documented**: Storybook documentation for all components

### 2.2 Component Categories

```
Global Component Library
├── Form Components
│   ├── Input (text, email, password, number, tel, url)
│   ├── TextArea
│   ├── Select (dropdown)
│   ├── Checkbox
│   ├── Radio
│   ├── Switch (toggle)
│   ├── DatePicker
│   ├── TimePicker
│   ├── FileUpload
│   └── RichTextEditor (future)
├── Data Display Components
│   ├── Table (sortable, filterable, paginated)
│   ├── Card
│   ├── List (ordered, unordered, definition)
│   ├── Badge
│   ├── Tag
│   ├── Avatar
│   ├── Tooltip
│   └── Popover
├── Feedback Components
│   ├── Toast (notification)
│   ├── Alert (inline message)
│   ├── Modal (dialog)
│   ├── Spinner (loading)
│   ├── Progress Bar
│   └── Skeleton (loading placeholder)
├── Navigation Components
│   ├── Breadcrumb
│   ├── Tabs
│   ├── Pagination
│   └── Menu (dropdown)
├── Layout Components
│   ├── Grid
│   ├── Stack (vertical/horizontal)
│   ├── Divider
│   └── Spacer
└── Utility Components
    ├── Button (primary, secondary, tertiary, danger)
    ├── Icon
    ├── Link
    └── Text
```

---

## 3. Form Components

### 3.1 Input Component

**Purpose**: Single-line text input for various data types

**Specification**:
```typescript
interface InputProps {
  id: string;
  name: string;
  type?: 'text' | 'email' | 'password' | 'number' | 'tel' | 'url' | 'search';
  value: string;
  onChange: (value: string) => void;
  onBlur?: () => void;
  onFocus?: () => void;
  label?: string;
  placeholder?: string;
  helpText?: string;
  errorText?: string;
  required?: boolean;
  disabled?: boolean;
  readOnly?: boolean;
  maxLength?: number;
  minLength?: number;
  pattern?: string;
  autoComplete?: string;
  autoFocus?: boolean;
  size?: 'sm' | 'md' | 'lg';
  width?: 'full' | 'auto';
  leftIcon?: ReactNode;
  rightIcon?: ReactNode;
  'aria-label'?: string;
  'aria-describedby'?: string;
  'aria-invalid'?: boolean;
}
```

**Accessibility**:
- Label associated with input via `for` attribute or wrapping
- Error messages linked via `aria-describedby`
- Required fields indicated with `aria-required`
- Invalid state indicated with `aria-invalid`
- Placeholder text not used as label replacement

**Visual States**:
- Default
- Hover
- Focus (visible outline)
- Disabled (grayed out, not interactive)
- Error (red border, error icon)
- Success (optional green border, check icon)

---

### 3.2 Select Component

**Purpose**: Dropdown selection from predefined options

**Specification**:
```typescript
interface SelectOption {
  value: string;
  label: string;
  disabled?: boolean;
  group?: string;
}

interface SelectProps {
  id: string;
  name: string;
  value: string | string[];
  onChange: (value: string | string[]) => void;
  options: SelectOption[];
  label?: string;
  placeholder?: string;
  helpText?: string;
  errorText?: string;
  required?: boolean;
  disabled?: boolean;
  multiple?: boolean;
  searchable?: boolean;
  clearable?: boolean;
  size?: 'sm' | 'md' | 'lg';
  width?: 'full' | 'auto';
  maxHeight?: number;
  'aria-label'?: string;
}
```

**Features**:
- Keyboard navigation (Arrow keys, Enter, Escape)
- Type-ahead search (if searchable)
- Multiple selection support
- Option grouping
- Clear selection button (if clearable)

---

### 3.3 DatePicker Component

**Purpose**: Date input with calendar widget

**Specification**:
```typescript
interface DatePickerProps {
  id: string;
  name: string;
  value: Date | null;
  onChange: (date: Date | null) => void;
  label?: string;
  helpText?: string;
  errorText?: string;
  required?: boolean;
  disabled?: boolean;
  minDate?: Date;
  maxDate?: Date;
  excludeDates?: Date[];
  format?: string; // e.g., 'yyyy-MM-dd'
  placeholder?: string;
  showTimeSelect?: boolean;
  timeIntervals?: number; // minutes
  'aria-label'?: string;
}
```

**Features**:
- Calendar popup widget
- Manual text input support
- Date range validation
- Keyboard navigation (Tab, Arrow keys, Enter, Escape)
- Localization support

---

### 3.4 Checkbox Component

**Purpose**: Binary choice or multi-select from list

**Specification**:
```typescript
interface CheckboxProps {
  id: string;
  name: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
  label?: string;
  helpText?: string;
  disabled?: boolean;
  indeterminate?: boolean;
  size?: 'sm' | 'md' | 'lg';
  'aria-label'?: string;
}
```

**States**:
- Unchecked
- Checked
- Indeterminate (for partial selection)
- Disabled

---

## 4. Data Display Components

### 4.1 Table Component

**Purpose**: Tabular data display with sorting, filtering, pagination

**Specification**:
```typescript
interface Column<T> {
  key: string;
  header: string;
  accessor: (row: T) => ReactNode;
  sortable?: boolean;
  filterable?: boolean;
  width?: string | number;
  align?: 'left' | 'center' | 'right';
}

interface TableProps<T> {
  data: T[];
  columns: Column<T>[];
  keyExtractor: (row: T) => string;
  sortable?: boolean;
  filterable?: boolean;
  pagination?: {
    page: number;
    perPage: number;
    total: number;
    onPageChange: (page: number) => void;
  };
  selectable?: boolean;
  selectedRows?: string[];
  onSelectionChange?: (selected: string[]) => void;
  emptyState?: ReactNode;
  loading?: boolean;
  stickyHeader?: boolean;
  striped?: boolean;
  hover?: boolean;
  density?: 'compact' | 'normal' | 'comfortable';
  'aria-label'?: string;
}
```

**Features**:
- Column sorting (asc/desc)
- Column filtering
- Row selection (single/multiple)
- Pagination
- Sticky header
- Responsive (horizontal scroll on small screens)
- Empty state display
- Loading state with skeleton

**Accessibility**:
- Semantic `<table>`, `<thead>`, `<tbody>`, `<tr>`, `<th>`, `<td>`
- `scope` attribute on header cells
- `aria-sort` on sortable columns
- Keyboard navigation (Tab, Arrow keys)

---

### 4.2 Card Component

**Purpose**: Contained content with optional header, footer, actions

**Specification**:
```typescript
interface CardProps {
  children: ReactNode;
  header?: ReactNode;
  footer?: ReactNode;
  padding?: 'none' | 'sm' | 'md' | 'lg';
  shadow?: boolean;
  border?: boolean;
  hoverable?: boolean;
  onClick?: () => void;
  className?: string;
}
```

**Variants**:
- Basic card (content only)
- Card with header
- Card with header and footer
- Clickable card (entire card is interactive)
- Image card (with image at top)

---

### 4.3 Badge Component

**Purpose**: Small status or label indicator

**Specification**:
```typescript
interface BadgeProps {
  children: ReactNode;
  variant?: 'default' | 'success' | 'warning' | 'error' | 'info';
  size?: 'sm' | 'md' | 'lg';
  rounded?: boolean;
  removable?: boolean;
  onRemove?: () => void;
}
```

**Examples**:
- Status badge (Active, Inactive, Pending)
- Count badge (notification count)
- Tag badge (category label)

---

## 5. Feedback Components

### 5.1 Toast Component

**Purpose**: Temporary notification messages

**Specification**:
```typescript
interface ToastProps {
  id: string;
  message: string;
  variant?: 'success' | 'error' | 'warning' | 'info';
  duration?: number; // milliseconds, 0 = persistent
  position?: 'top-left' | 'top-center' | 'top-right' | 
             'bottom-left' | 'bottom-center' | 'bottom-right';
  closable?: boolean;
  onClose?: () => void;
  action?: {
    label: string;
    onClick: () => void;
  };
}

// Toast API
function showToast(props: Omit<ToastProps, 'id'>): string;
function hideToast(id: string): void;
```

**Features**:
- Auto-dismiss after duration
- Manual dismiss (close button)
- Optional action button
- Stack multiple toasts
- Animations (slide in/out)

**Accessibility**:
- `role="status"` or `role="alert"` based on variant
- `aria-live="polite"` or `aria-live="assertive"`
- Focus management (doesn't steal focus)

---

### 5.2 Modal Component

**Purpose**: Dialog overlay for important actions or content

**Specification**:
```typescript
interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: ReactNode;
  footer?: ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
  closeOnOverlayClick?: boolean;
  closeOnEscape?: boolean;
  showCloseButton?: boolean;
  centered?: boolean;
  scrollBehavior?: 'inside' | 'outside';
  'aria-labelledby'?: string;
  'aria-describedby'?: string;
}
```

**Features**:
- Overlay backdrop (dims background)
- Close on overlay click (optional)
- Close on Escape key (optional)
- Focus trap (keep focus inside modal)
- Restore focus on close
- Scroll lock (prevent body scroll)
- Animations (fade in/out)

**Accessibility**:
- `role="dialog"` or `role="alertdialog"`
- `aria-modal="true"`
- `aria-labelledby` points to title
- Focus management (auto-focus first focusable element)
- Escape key to close

---

### 5.3 Alert Component

**Purpose**: Inline contextual messages

**Specification**:
```typescript
interface AlertProps {
  variant: 'success' | 'error' | 'warning' | 'info';
  title?: string;
  children: ReactNode;
  closable?: boolean;
  onClose?: () => void;
  icon?: ReactNode;
  actions?: Array<{
    label: string;
    onClick: () => void;
  }>;
}
```

**Features**:
- Color-coded by variant
- Optional icon
- Optional close button
- Optional action buttons
- Persistent (doesn't auto-dismiss)

---

## 6. Navigation Components

### 6.1 Breadcrumb Component

**Purpose**: Hierarchical navigation path

**Specification**:
```typescript
interface BreadcrumbItem {
  label: string;
  href?: string;
  onClick?: () => void;
  icon?: ReactNode;
}

interface BreadcrumbProps {
  items: BreadcrumbItem[];
  separator?: ReactNode;
  maxItems?: number;
  'aria-label'?: string;
}
```

**Accessibility**:
- `<nav aria-label="Breadcrumb">`
- `aria-current="page"` on last item
- Each item is a link (except last)

---

### 6.2 Tabs Component

**Purpose**: Content organization with tab-based navigation

**Specification**:
```typescript
interface Tab {
  id: string;
  label: string;
  icon?: ReactNode;
  disabled?: boolean;
  badge?: string | number;
}

interface TabsProps {
  tabs: Tab[];
  activeTab: string;
  onChange: (tabId: string) => void;
  variant?: 'default' | 'pills' | 'underline';
  orientation?: 'horizontal' | 'vertical';
  fitted?: boolean;
  'aria-label'?: string;
}
```

**Accessibility**:
- `role="tablist"` on container
- `role="tab"` on each tab
- `role="tabpanel"` on content
- `aria-selected` on active tab
- Keyboard navigation (Arrow keys, Home, End)

---

### 6.3 Pagination Component

**Purpose**: Navigate through paginated data

**Specification**:
```typescript
interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  pageSize?: number;
  totalItems?: number;
  showPageSize?: boolean;
  pageSizeOptions?: number[];
  onPageSizeChange?: (size: number) => void;
  showFirstLast?: boolean;
  maxPagesShown?: number;
  'aria-label'?: string;
}
```

**Features**:
- First/Previous/Next/Last buttons
- Page number buttons (with ellipsis for many pages)
- Page size selector
- Total items display
- Keyboard navigation

---

## 7. Button Component

### 7.1 Specification

```typescript
interface ButtonProps {
  children: ReactNode;
  variant?: 'primary' | 'secondary' | 'tertiary' | 'danger' | 'ghost';
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  disabled?: boolean;
  loading?: boolean;
  fullWidth?: boolean;
  leftIcon?: ReactNode;
  rightIcon?: ReactNode;
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';
  'aria-label'?: string;
}
```

### 7.2 Button Variants

- **Primary**: Main call-to-action (filled, primary color)
- **Secondary**: Secondary actions (outlined, primary color)
- **Tertiary**: Less prominent actions (text only)
- **Danger**: Destructive actions (filled, error color)
- **Ghost**: Minimal style (transparent background)

### 7.3 Button States

- Default
- Hover
- Active (pressed)
- Focus (visible outline)
- Loading (spinner icon, disabled)
- Disabled (grayed out, not interactive)

---

## 8. Icon System

### 8.1 Icon Library

Use **Heroicons** (MIT license) as base icon set:
- Outline variant (24x24px) for most uses
- Solid variant (20x20px) for filled icons
- Mini variant (16x16px) for small spaces

### 8.2 Icon Component

```typescript
interface IconProps {
  name: string;
  size?: number | 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  color?: string;
  className?: string;
  'aria-label'?: string;
  'aria-hidden'?: boolean;
}
```

### 8.3 Icon Usage Guidelines

- **Decorative icons**: Use `aria-hidden="true"`
- **Meaningful icons**: Provide `aria-label`
- **Icon-only buttons**: Always include `aria-label`
- **Consistent sizing**: Use size prop, not inline styles

---

## 9. Component Testing Requirements

### 9.1 Unit Tests

Each component must have tests for:
- **Rendering**: Component renders without errors
- **Props**: All props work correctly
- **States**: All visual states render correctly
- **Events**: Event handlers called with correct args
- **Accessibility**: ARIA attributes present and correct

### 9.2 Integration Tests

- **Keyboard navigation**: Tab, Arrow keys, Enter, Escape
- **Screen reader**: Correct announcements
- **Form submission**: Form components work in forms
- **Theme switching**: Components respect theme changes

### 9.3 Visual Regression Tests

- Screenshot comparison for all component states
- Cross-browser visual consistency
- Responsive layout correctness

---

## 10. Documentation Requirements

### 10.1 Storybook

Each component must have Storybook stories for:
- Default state
- All variants
- All sizes
- All states (hover, focus, disabled, error, etc.)
- Dark mode
- Interactive examples
- Accessibility documentation
- Code examples

### 10.2 Component README

Each component folder includes `README.md` with:
- Purpose and use cases
- Props API reference
- Examples
- Accessibility notes
- Known issues/limitations

---

## 11. Implementation Checklist

### Builder: UI-Builder

#### Form Components
- [ ] Input (with all types)
- [ ] TextArea
- [ ] Select
- [ ] Checkbox
- [ ] Radio
- [ ] Switch
- [ ] DatePicker
- [ ] TimePicker
- [ ] FileUpload

#### Data Display
- [ ] Table (sortable, filterable, paginated)
- [ ] Card
- [ ] List
- [ ] Badge
- [ ] Tag
- [ ] Avatar
- [ ] Tooltip
- [ ] Popover

#### Feedback
- [ ] Toast
- [ ] Alert
- [ ] Modal
- [ ] Spinner
- [ ] Progress Bar
- [ ] Skeleton

#### Navigation
- [ ] Breadcrumb
- [ ] Tabs
- [ ] Pagination
- [ ] Menu

#### Layout
- [ ] Grid
- [ ] Stack
- [ ] Divider
- [ ] Spacer

#### Utility
- [ ] Button (all variants)
- [ ] Icon
- [ ] Link
- [ ] Text

#### Testing & Documentation
- [ ] Unit tests for all components
- [ ] Integration tests
- [ ] Visual regression tests
- [ ] Storybook stories
- [ ] Component README files
- [ ] Accessibility audit

---

## 12. QA Gates

### Functional
- [ ] All components render correctly
- [ ] All props work as documented
- [ ] All states display correctly
- [ ] All events fire correctly
- [ ] Theme integration works

### Accessibility
- [ ] WCAG 2.1 Level AA compliance
- [ ] Keyboard navigation works
- [ ] Screen reader compatible
- [ ] ARIA attributes correct
- [ ] Focus management correct

### Performance
- [ ] Bundle size acceptable (< 100KB per component)
- [ ] No unnecessary re-renders
- [ ] Animations run at 60fps

### Cross-Browser
- [ ] Chrome
- [ ] Firefox
- [ ] Safari
- [ ] Edge

---

## 13. Dependencies

### External Dependencies
- React 18+
- TypeScript 5+
- Heroicons (MIT)
- Date-fns (for DatePicker)

### Internal Dependencies
- Theme system (see `theme-system.md`)
- Layout system (see `layout.md`)

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
- Component API changes require Foreman review
- Breaking changes require major version bump
- New components require architecture review

---

*Document prepared by: Maturion Foreman*  
*Date: 2025-12-04*  
*Build Wave: 1.1*
