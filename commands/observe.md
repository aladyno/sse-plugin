---
description: Design monitoring — SLIs/SLOs, metrics, logs, traces, dashboards, alerts and runbooks for a service or feature
argument-hint: "<service, feature or critical user journey>"
---

# Observe

Scope: $ARGUMENTS

1. Find the service's entry points, dependencies and current instrumentation (logging config, metrics libraries, tracing setup, existing dashboards/alerts as code).
2. Delegate to the `ag-sse-sre` agent (observability design mode).
3. Output: SLO table · instrumentation gaps with exact code locations · alert rules · dashboard layout · runbook skeleton for each paging alert.
4. Offer to add the instrumentation code via `ag-sse-implementer` — only after the user agrees.
