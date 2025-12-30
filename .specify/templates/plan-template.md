# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: FastAPI, SQLModel, Next.js (App Router), OpenAI Agents SDK, OpenAI ChatKit, Official MCP SDK, Better Auth (JWT), Dapr, Gordon, kubectl-ai, Kagent
**Storage**: Neon PostgreSQL
**Testing**: pytest
**Target Platform**: Minikube, DigitalOcean Kubernetes (DOKS)
**Project Type**: Web Application (Backend + Frontend)
**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]
**Constraints**: [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]
**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [ ] **Evolutionary Design**: Does this plan build on the previous phase without skipping steps?
- [ ] **Stateless First**: If in Phase III+, are all server components stateless?
- [ ] **API-First & Tool-Driven**: Is all business logic exposed via REST APIs or MCP tools? Do AI agents avoid direct database access?
- [ ] **Event-Driven by Default**: If in Phase V, are side effects handled asynchronously via the event stream?
- [ ] **Technology Constraints**: Does the plan adhere to the immutable core stack and cloud infrastructure?
- [ ] **Phase Governance**: Does the plan respect the boundaries and requirements of the current project phase?
- [ ] **Quality & Verification**: Does the plan include user stories, acceptance criteria, and tool/API definitions?
- [ ] **Security Principles**: Does the plan enforce JWT, user isolation, and proper secret management?

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
