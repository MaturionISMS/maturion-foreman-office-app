# UI Builder Agent Specification

## Purpose
Generate all frontend/UI components for modules.

## Responsibilities
- React/Next.js components
- Layouts and page structures
- Component interaction logic
- Modal, forms, wizards
- UI event flows
- Navigation elements
- Theming using APGI Design System
- Tenant branding overrides

## Required Inputs from Foreman
- Frontend Component Map
- Wireframes
- Module UI requirements
- Naming conventions
- Folder structure rules

## Outputs
- UI code under /apps/{module}/frontend/
- UI tests
- Storybook stories (optional)
- Accessibility validations

## Forbidden Actions
- No backend logic
- No schema definitions
- No integration code
- No architecture updates

## PR Requirements
- Reference architecture sections
- Include UI QA test results
- Include screenshot diffs (when applicable)
