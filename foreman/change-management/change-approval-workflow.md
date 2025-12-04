# Change Approval Workflow

## Roles

- **Requester** – proposes change.
- **Foreman** – governance + architecture approval.
- **Human Admin** – business/tenant oversight.
- **Builder Agents** – implement, cannot self-approve.

## Approval Rules

- High/critical risk changes require **Foreman + Human Admin**.
- Compliance-relevant changes must involve the compliance engine owner.
- Emergency changes follow an emergency workflow but require
  retrospective review within 24h.

All approvals and comments must be stored via `change-log-schema.json`.
