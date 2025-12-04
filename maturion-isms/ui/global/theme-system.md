# Maturion ISMS – Theme & Branding System Specification

**Version**: 1.0  
**Build Wave**: 1.1  
**Owner**: Maturion Foreman  
**Status**: DRAFT - AWAITING APPROVAL

---

## 1. Purpose

This document defines the theming and branding engine for the Maturion ISMS platform.

The theme system provides:
- Consistent visual identity across the platform
- APGI default theme
- Tenant-specific theme customization
- Dark mode / Light mode support
- Accessible color palettes
- Typography system
- Brand asset management

---

## 2. Architecture

### 2.1 Theme Architecture Layers

```
┌─────────────────────────────────────────────┐
│           Platform Base Theme                │
│  (Core colors, fonts, spacing, shadows)     │
├─────────────────────────────────────────────┤
│           APGI Default Theme                 │
│  (APGI branding, logo, color overrides)     │
├─────────────────────────────────────────────┤
│         Tenant Theme Override (Optional)     │
│  (Tenant logo, colors, custom branding)     │
├─────────────────────────────────────────────┤
│         User Preference Layer                │
│  (Dark/Light mode, accessibility settings)  │
└─────────────────────────────────────────────┘
```

### 2.2 Theme Loading Priority

1. Load Platform Base Theme
2. Apply APGI Default Theme (if no tenant override)
3. Apply Tenant Theme Override (if exists and validated)
4. Apply User Preferences (dark mode, font size, etc.)

---

## 3. Platform Base Theme

### 3.1 Color System

#### Primary Colors

```css
/* Light Mode */
--color-primary-50: #eff6ff;
--color-primary-100: #dbeafe;
--color-primary-200: #bfdbfe;
--color-primary-300: #93c5fd;
--color-primary-400: #60a5fa;
--color-primary-500: #3b82f6;  /* Main brand color */
--color-primary-600: #2563eb;
--color-primary-700: #1d4ed8;
--color-primary-800: #1e40af;
--color-primary-900: #1e3a8a;

/* Dark Mode */
--color-primary-dark-50: #1e3a8a;
--color-primary-dark-100: #1e40af;
--color-primary-dark-200: #1d4ed8;
--color-primary-dark-300: #2563eb;
--color-primary-dark-400: #3b82f6;
--color-primary-dark-500: #60a5fa; /* Main in dark mode */
--color-primary-dark-600: #93c5fd;
--color-primary-dark-700: #bfdbfe;
--color-primary-dark-800: #dbeafe;
--color-primary-dark-900: #eff6ff;
```

#### Semantic Colors

```css
/* Success (Green) */
--color-success-light: #d1fae5;
--color-success: #10b981;
--color-success-dark: #047857;

/* Warning (Amber) */
--color-warning-light: #fef3c7;
--color-warning: #f59e0b;
--color-warning-dark: #d97706;

/* Error (Red) */
--color-error-light: #fee2e2;
--color-error: #ef4444;
--color-error-dark: #dc2626;

/* Info (Blue) */
--color-info-light: #dbeafe;
--color-info: #3b82f6;
--color-info-dark: #1d4ed8;
```

#### Neutral Colors

```css
/* Light Mode Neutrals */
--color-gray-50: #f9fafb;
--color-gray-100: #f3f4f6;
--color-gray-200: #e5e7eb;
--color-gray-300: #d1d5db;
--color-gray-400: #9ca3af;
--color-gray-500: #6b7280;
--color-gray-600: #4b5563;
--color-gray-700: #374151;
--color-gray-800: #1f2937;
--color-gray-900: #111827;

/* Dark Mode Neutrals */
--color-gray-dark-50: #111827;
--color-gray-dark-100: #1f2937;
--color-gray-dark-200: #374151;
--color-gray-dark-300: #4b5563;
--color-gray-dark-400: #6b7280;
--color-gray-dark-500: #9ca3af;
--color-gray-dark-600: #d1d5db;
--color-gray-dark-700: #e5e7eb;
--color-gray-dark-800: #f3f4f6;
--color-gray-dark-900: #f9fafb;
```

### 3.2 Typography System

#### Font Families

```css
--font-family-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 
                     Roboto, 'Helvetica Neue', Arial, sans-serif;
--font-family-mono: 'Fira Code', 'Courier New', monospace;
--font-family-display: 'Inter', sans-serif; /* For headings */
```

#### Font Sizes

```css
--font-size-xs: 0.75rem;    /* 12px */
--font-size-sm: 0.875rem;   /* 14px */
--font-size-base: 1rem;     /* 16px */
--font-size-lg: 1.125rem;   /* 18px */
--font-size-xl: 1.25rem;    /* 20px */
--font-size-2xl: 1.5rem;    /* 24px */
--font-size-3xl: 1.875rem;  /* 30px */
--font-size-4xl: 2.25rem;   /* 36px */
--font-size-5xl: 3rem;      /* 48px */
```

#### Font Weights

```css
--font-weight-light: 300;
--font-weight-normal: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;
```

#### Line Heights

```css
--line-height-tight: 1.25;
--line-height-snug: 1.375;
--line-height-normal: 1.5;
--line-height-relaxed: 1.625;
--line-height-loose: 2;
```

### 3.3 Spacing System

```css
--spacing-0: 0;
--spacing-1: 0.25rem;   /* 4px */
--spacing-2: 0.5rem;    /* 8px */
--spacing-3: 0.75rem;   /* 12px */
--spacing-4: 1rem;      /* 16px */
--spacing-5: 1.25rem;   /* 20px */
--spacing-6: 1.5rem;    /* 24px */
--spacing-8: 2rem;      /* 32px */
--spacing-10: 2.5rem;   /* 40px */
--spacing-12: 3rem;     /* 48px */
--spacing-16: 4rem;     /* 64px */
--spacing-20: 5rem;     /* 80px */
--spacing-24: 6rem;     /* 96px */
```

### 3.4 Border Radius

```css
--radius-none: 0;
--radius-sm: 0.125rem;  /* 2px */
--radius-base: 0.25rem; /* 4px */
--radius-md: 0.375rem;  /* 6px */
--radius-lg: 0.5rem;    /* 8px */
--radius-xl: 0.75rem;   /* 12px */
--radius-2xl: 1rem;     /* 16px */
--radius-full: 9999px;  /* Pill shape */
```

### 3.5 Shadows

```css
--shadow-xs: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
--shadow-base: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
--shadow-md: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
--shadow-lg: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
--shadow-xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
--shadow-inner: inset 0 2px 4px 0 rgba(0, 0, 0, 0.06);
```

---

## 4. APGI Default Theme

### 4.1 Brand Colors

```css
/* APGI Primary - Professional Blue */
--apgi-primary: #1e40af;
--apgi-primary-light: #3b82f6;
--apgi-primary-dark: #1e3a8a;

/* APGI Secondary - Trust Gray */
--apgi-secondary: #4b5563;
--apgi-secondary-light: #6b7280;
--apgi-secondary-dark: #374151;

/* APGI Accent - Innovation Teal */
--apgi-accent: #0d9488;
--apgi-accent-light: #14b8a6;
--apgi-accent-dark: #0f766e;
```

### 4.2 APGI Logo

```
Logo File: /public/branding/apgi-logo.svg
Logo Dimensions: 180x48px (header), 240x64px (full)
Logo Variants:
  - apgi-logo-light.svg (for light backgrounds)
  - apgi-logo-dark.svg (for dark backgrounds)
  - apgi-logo-icon.svg (square icon, 48x48px)
```

### 4.3 APGI Typography

```css
--apgi-font-display: 'Inter', sans-serif;
--apgi-font-body: 'Inter', sans-serif;
--apgi-font-mono: 'Fira Code', monospace;
```

---

## 5. Tenant Theme Override System

### 5.1 Tenant Theme Structure

Each tenant can provide a theme override file:

```json
{
  "tenant_id": "org_12345",
  "theme_version": "1.0",
  "enabled": true,
  "branding": {
    "name": "Example Corporation",
    "logo": {
      "light": "https://cdn.example.com/logo-light.svg",
      "dark": "https://cdn.example.com/logo-dark.svg",
      "icon": "https://cdn.example.com/favicon.svg"
    },
    "colors": {
      "primary": "#6366f1",
      "primary_light": "#818cf8",
      "primary_dark": "#4f46e5",
      "secondary": "#8b5cf6",
      "accent": "#ec4899"
    },
    "typography": {
      "font_family": "Roboto, sans-serif",
      "font_url": "https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap"
    }
  },
  "footer": {
    "copyright": "© 2024 Example Corporation",
    "support_email": "support@example.com",
    "privacy_url": "https://example.com/privacy",
    "terms_url": "https://example.com/terms"
  }
}
```

### 5.2 Tenant Theme Validation

Before applying, tenant themes must be validated:

1. **Logo URLs**: HTTPS only, valid image formats (SVG, PNG)
2. **Colors**: Valid hex codes, contrast ratio ≥ 4.5:1 for text
3. **Fonts**: Google Fonts or self-hosted HTTPS URLs
4. **File Size**: Logo files < 200KB each
5. **Security**: No JavaScript injection, XSS vectors

### 5.3 Tenant Theme Application

```typescript
interface TenantTheme {
  tenant_id: string;
  theme_version: string;
  enabled: boolean;
  branding: {
    name: string;
    logo: {
      light: string;
      dark: string;
      icon: string;
    };
    colors: {
      primary: string;
      primary_light: string;
      primary_dark: string;
      secondary?: string;
      accent?: string;
    };
    typography?: {
      font_family: string;
      font_url?: string;
    };
  };
  footer?: {
    copyright: string;
    support_email?: string;
    privacy_url?: string;
    terms_url?: string;
  };
}
```

### 5.4 Fallback Behavior

If tenant theme loading fails:
1. Log error to platform monitoring
2. Fall back to APGI default theme
3. Display non-blocking error notification to admin
4. Allow platform to function normally

---

## 6. Dark Mode Support

### 6.1 Dark Mode Color Mappings

```css
/* Backgrounds */
--bg-primary: var(--color-gray-50);         /* Light */
--bg-primary-dark: var(--color-gray-900);   /* Dark */

--bg-secondary: var(--color-gray-100);
--bg-secondary-dark: var(--color-gray-800);

--bg-tertiary: var(--color-gray-200);
--bg-tertiary-dark: var(--color-gray-700);

/* Text */
--text-primary: var(--color-gray-900);
--text-primary-dark: var(--color-gray-50);

--text-secondary: var(--color-gray-700);
--text-secondary-dark: var(--color-gray-300);

--text-tertiary: var(--color-gray-500);
--text-tertiary-dark: var(--color-gray-500);

/* Borders */
--border-primary: var(--color-gray-300);
--border-primary-dark: var(--color-gray-600);

--border-secondary: var(--color-gray-200);
--border-secondary-dark: var(--color-gray-700);
```

### 6.2 Dark Mode Toggle

**Location**: User profile dropdown  
**Persistence**: Stored in user preferences (database)  
**Default**: System preference (prefers-color-scheme)  
**Transition**: Smooth (300ms ease)

```typescript
interface DarkModePreference {
  user_id: string;
  mode: 'light' | 'dark' | 'system';
  updated_at: string;
}
```

### 6.3 Dark Mode Implementation

Use CSS custom properties with `data-theme` attribute:

```html
<html data-theme="light">  <!-- or "dark" -->
```

```css
:root[data-theme="light"] {
  --bg-primary: var(--color-gray-50);
  --text-primary: var(--color-gray-900);
}

:root[data-theme="dark"] {
  --bg-primary: var(--color-gray-900);
  --text-primary: var(--color-gray-50);
}
```

---

## 7. Accessibility Compliance

### 7.1 Color Contrast Requirements

All theme colors must meet WCAG 2.1 Level AA:

- **Normal text** (< 18pt): Contrast ratio ≥ 4.5:1
- **Large text** (≥ 18pt or 14pt bold): Contrast ratio ≥ 3:1
- **UI components**: Contrast ratio ≥ 3:1

### 7.2 Contrast Validation

Automated contrast checking:

```typescript
function validateContrast(
  foreground: string, 
  background: string, 
  minRatio: number = 4.5
): boolean {
  const ratio = calculateContrastRatio(foreground, background);
  return ratio >= minRatio;
}
```

### 7.3 Color Blindness Support

Theme must remain usable for:
- Protanopia (red-blind)
- Deuteranopia (green-blind)
- Tritanopia (blue-blind)

**Strategy**:
- Never use color alone to convey information
- Use icons, labels, and patterns alongside colors
- Provide text alternatives for color-coded information

---

## 8. Theme Loading & Performance

### 8.1 Loading Strategy

1. **Inline Critical CSS**: Base theme variables inline in `<head>`
2. **Async Theme CSS**: Load full theme stylesheet asynchronously
3. **Font Loading**: Use `font-display: swap` to prevent FOIT
4. **Tenant Theme**: Load after base theme, apply overrides

### 8.2 Performance Targets

- **Theme Load Time**: < 100ms
- **Theme Switch Time**: < 300ms
- **Flash of Unstyled Content (FOUC)**: None (critical CSS inline)
- **Flash of Incorrect Theme (FOIT)**: None (system detection)

### 8.3 Caching Strategy

- **Base Theme**: Cache-Control: public, max-age=31536000 (1 year)
- **APGI Theme**: Cache-Control: public, max-age=86400 (1 day)
- **Tenant Theme**: Cache-Control: public, max-age=3600 (1 hour)

---

## 9. Theme Customization Limits

### 9.1 What Tenants CAN Customize

✅ Primary brand colors (with contrast validation)  
✅ Logo (light, dark, icon variants)  
✅ Typography (Google Fonts or approved list)  
✅ Footer text (copyright, support)  
✅ Secondary/accent colors (optional)

### 9.2 What Tenants CANNOT Customize

❌ Layout structure (fixed by platform)  
❌ Spacing system (consistency required)  
❌ Border radius (design coherence)  
❌ Shadow system (depth hierarchy)  
❌ Semantic colors (success, warning, error, info)  
❌ Accessibility features (non-negotiable)

---

## 10. Implementation Checklist

### Builder: UI-Builder

- [ ] Implement CSS custom property system
- [ ] Create APGI default theme
- [ ] Create tenant theme loader
- [ ] Implement tenant theme validator
- [ ] Implement dark mode toggle
- [ ] Implement theme switcher (light/dark/system)
- [ ] Create contrast ratio validator
- [ ] Implement theme caching
- [ ] Create theme preview tool (for tenant admins)
- [ ] Implement fallback handling
- [ ] Write theme documentation for tenants
- [ ] Create theme testing suite
- [ ] Performance testing

---

## 11. QA Gates

### Functional
- [ ] APGI default theme loads correctly
- [ ] Tenant theme overrides apply correctly
- [ ] Dark mode toggle works smoothly
- [ ] Theme persists across sessions
- [ ] Invalid tenant themes fall back gracefully

### Accessibility
- [ ] All color combinations meet WCAG 2.1 AA
- [ ] Dark mode meets contrast requirements
- [ ] Theme works for color blind users
- [ ] No information conveyed by color alone

### Performance
- [ ] Theme load time < 100ms
- [ ] Theme switch time < 300ms
- [ ] No FOUC (Flash of Unstyled Content)
- [ ] Caching works correctly

### Cross-Browser
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)

---

## 12. Security Considerations

### 12.1 Tenant Theme Security

- **XSS Prevention**: Sanitize all tenant-provided URLs
- **CSP Headers**: Content Security Policy for external resources
- **Logo Validation**: Verify image formats, scan for malicious code
- **Font Loading**: Whitelist approved font sources
- **No JavaScript**: Tenant themes are CSS/images only

### 12.2 Theme Injection Attack Prevention

```typescript
// Validate tenant theme before applying
function sanitizeTenantTheme(theme: TenantTheme): TenantTheme {
  return {
    ...theme,
    branding: {
      ...theme.branding,
      logo: {
        light: sanitizeURL(theme.branding.logo.light),
        dark: sanitizeURL(theme.branding.logo.dark),
        icon: sanitizeURL(theme.branding.logo.icon),
      },
      colors: {
        primary: sanitizeHexColor(theme.branding.colors.primary),
        // ... validate all colors
      }
    }
  };
}
```

---

## 13. Dependencies

### External Dependencies
- CSS Custom Properties (CSS Variables)
- CSS Grid / Flexbox
- Web Fonts API (Google Fonts)

### Internal Dependencies
- Layout system (see `layout.md`)
- Component library (see `component-library.md`)
- User preferences service

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
- Theme variable changes require Foreman review
- Color palette changes require accessibility validation
- Breaking changes require major version bump

---

*Document prepared by: Maturion Foreman*  
*Date: 2025-12-04*  
*Build Wave: 1.1*
