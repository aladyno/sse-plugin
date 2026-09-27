---
name: sse-playbook
description: Senior Software Engineer Definition-of-Done checklists for each SDLC phase (design, code, test, review, deploy, operate, maintain). Use when asked "is this done/ready?", "what am I missing?", or to self-check work before handing it off.
---

# SSE Playbook — Definition of Done per phase

## When to use
Quick self-check of a piece of work against senior-level standards. For doing the work itself, use the commands (`/sse-plugin:design`, `:implement`, `:test`, `:review`, `:ship`, `:observe`, `:incident`, `:maintain`) or `/sse-plugin:sse` to route.

## Workflow
1. Identify the phase(s) the work belongs to.
2. Walk the matching checklist below; mark each item ✅ / ⚠️ / ❌ with evidence (file:line, command output, link).
3. Report only ⚠️ / ❌ items with the concrete fix, most severe first. Respond in the user's language.

## Checklists

### Design
- Problem, users, constraints and non-goals written down
- Load numbers estimated (QPS, data size, latency target, growth)
- ≥ 2 options compared; decision + trade-offs recorded (ADR)
- Data model, API contracts, error model and idempotency defined
- Failure modes, security/PII, migration and rollout considered

### Code
- Follows existing patterns; minimal diff; no dead or speculative code
- Inputs validated at boundaries; errors handled, never swallowed
- No secrets or PII in code or logs; dependencies justified
- Builds, lints and passes tests locally

### Test
- Critical and failure paths covered (boundaries, null/empty, retries, timeouts)
- Tests are deterministic, isolated and fast; new tests fail without the change
- Integration/contract tests at external boundaries

### Review
- Intent understood; diff read with surrounding code
- Correctness, readability, architecture, security, performance all checked
- Every finding has evidence and a suggested fix

### Deploy
- CI green incl. security scans; same artifact promoted across envs
- Migrations backward-compatible (expand → migrate → contract)
- Config/secrets present in target env; feature flags for risky paths
- Rollout strategy, health gates and a tested rollback path

### Operate
- SLIs/SLOs for critical journeys; RED/USE metrics; structured logs with trace IDs
- Alerts page only on user impact / SLO burn and link to runbooks
- Dashboards exist for the new paths

### Maintain
- Debt items recorded with impact × effort
- Refactors are behavior-preserving, test-protected and independently revertible
- Dependencies current and free of known critical vulnerabilities
