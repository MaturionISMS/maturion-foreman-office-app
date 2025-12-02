# maturion-ai-foreman
This is the foreman repository that will be responsible for managing all builder agents.

## GitHub Copilot Integration

This repository is configured to work with GitHub Copilot for issue management.

### Assigning Issues to Copilot

When you create or view an issue in this repository, you can assign it to GitHub Copilot:

1. Open an issue or create a new one
2. On the right sidebar, look for the "Assignees" section
3. Click on "Assign to Copilot" (or search for "copilot" in the assignees dropdown)
4. GitHub Copilot will analyze the issue and can help suggest solutions or create pull requests

### Copilot Instructions

Repository-specific instructions for GitHub Copilot can be found in [`.github/copilot-instructions.md`](.github/copilot-instructions.md).

## Repository Structure

```
.github/
  ├── copilot-instructions.md    # Instructions for GitHub Copilot
  └── ISSUE_TEMPLATE/             # Issue templates
      ├── bug_report.md
      ├── feature_request.md
      └── config.yml
```

## Getting Started

This repository manages builder agents for the Maturion ISMS project. For more information on how to work with this repository, please refer to the documentation in the `.github` directory.
