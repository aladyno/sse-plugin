# Backend forcing questions

Read on demand, when a backend **design decision** (not a code-level finding) is on the table:
deployment shape, database choice, sync vs async, tenancy, reliability targets.

Discipline: ask one at a time, in order, and only the ones the conversation hasn't already answered
(contract §2). An unanswerable question is itself the finding — surface it as the next thing to
measure or decide. Recommend an answer; don't just ask.

---

## Q1 — Read/write ratio and peak load?

- **Good answer:** numbers traced to evidence — e.g., "20:1 reads to writes; 30 req/s today, peak
  3× daily average, planning for 3× growth in 12 months".
- **Why first:** caching, replicas, partitioning, queueing and pool sizing all change shape with
  these numbers (Little's Law turns them into concurrency).
- **Stop if:** "we'll need to scale" with no number — pull current traffic from metrics first.
- **Canon:** Kleppmann, *Designing Data-Intensive Applications* (load parameters, replication).

## Q2 — Tenancy model?

- **Options:** single-tenant, shared multi-tenant (row/schema isolation), isolated multi-tenant
  (per-tenant database or stack).
- **Why:** it decides the data-access pattern, noisy-neighbour risk, and cache/queue key design;
  migrating later is expensive.
- **Stop if:** tenant isolation is required by contract or regulation but the design relies on
  every query remembering a tenant filter.
- **Canon:** AWS Well-Architected SaaS Lens (silo / pool / bridge models).

## Q3 — Sync request/response, async queue, or event-driven — default and exceptions?

- **Good answer:** one default plus a named exception class — e.g., "sync for user-facing reads and
  writes; async queue for email, webhooks and exports".
- **Why:** premature event-driven design spreads one problem across many components and trades
  latency for delivery-semantics complexity (ordering, duplicates, eventual consistency).
- **Stop if:** async is chosen without an answer for duplicates, ordering and the dead-letter path.
- **Canon:** Hohpe & Woolf, *Enterprise Integration Patterns*; Helland, "Life beyond Distributed
  Transactions".

## Q4 — Highest data-sensitivity tier present?

- **Tiers:** public, internal, personal data, special-category/health data, payment card data.
- **Why:** it sets the floor for logging, encryption, retention, audit and which services may touch
  the data (scope reduction — e.g., tokenising card data through a compliant provider).
- **Stop if:** regulated data is in scope with no named owner and no plan for encryption and access
  logging — hand to `sse-security`.
- **Canon:** GDPR (data protection by design), PCI DSS, NIST SP 800-53, OWASP ASVS.

## Q5 — Monolith, modular monolith or services — and the team-level justification?

- **Good answer:** modular monolith by default; extract a service when a boundary has an
  independent owner, independent deploy cadence, or clearly different scaling/availability needs.
- **Why:** each service adds a network hop, a failure mode and an operational surface.
- **Stop if:** "microservices" is justified by fashion rather than ownership and deploy
  independence — hand to `sse-architect`.
- **Canon:** Fowler, "MonolithFirst"; Newman, *Building Microservices*; Skelton & Pais,
  *Team Topologies*.

## Q6 — RPO and RTO per data store?

- **Good answer:** two numbers per surface — e.g., "orders DB: RPO 5 min, RTO 30 min; analytics:
  RPO 24 h, RTO 4 h".
- **Why:** they decide backup cadence, replication topology, multi-region cost and runbooks.
- **Stop if:** a customer-facing store has no RPO/RTO and no tested restore.
- **Canon:** ISO 22301 (business continuity); Google SRE Workbook; cloud provider disaster-recovery
  guidance.

## Q7 — SLO and who owns the error budget?

- **Good answer:** an SLI-based objective — e.g., "99.9% of checkout requests succeed within
  500 ms over 30 days" — and a named owner who changes priorities when the budget burns.
- **Why:** without it, timeouts, retries, pool sizes and capacity have no target to be tuned
  against.
- **Stop if:** "high availability" with no number — pick one, then hand to `/sse-plugin:observe`.
- **Canon:** Google *Site Reliability Engineering* and *The Site Reliability Workbook*
  (SLOs, error budgets).

---

## Using the answers

- Q1 + Q7 → concurrency and timeout budget (runtime checklist steps 5–6 in `SKILL.md`).
- Q3 → delivery semantics and idempotency (step 8; external calls → `sse-integration`).
- Q2 + Q4 → cache keys, context propagation, logging hygiene (step 7).
- Q5 + Q6 → hand to `/sse-plugin:design` for the ADR.
