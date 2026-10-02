# Architecture standards & proven practice — deeper notes

Read on demand. For each: what it covers, when to invoke it, and how it is commonly misread.
Cite by name; never invent clause numbers. This is gap-analysis vocabulary, not certification.

## Describing and evaluating architecture

**ISO/IEC/IEEE 42010 — Architecture description**
- Covers: the vocabulary of an architecture description — stakeholders, concerns, viewpoints, views,
  model kinds, correspondences, and architecture rationale.
- Invoke when: someone asks "is our architecture documented well enough?" or a review keeps talking
  past each other (each party cares about a different concern).
- Misreading: it is not a notation or a template, and it does not prescribe which views to draw.
  It says each view must exist *because a stakeholder concern needs it*.

**ISO/IEC 25010 — Systems and software quality models (SQuaRE family)**
- Covers: product quality characteristics (functional suitability, performance efficiency,
  compatibility, usability/interaction capability, reliability, security, maintainability,
  portability, and in the 2023 revision safety) with sub-characteristics.
- Invoke when: quality requirements are adjectives ("scalable", "robust"). Map each to a
  characteristic, then to a measurable target (the measures live in ISO/IEC 25023).
- Misreading: it is a checklist of *what* to specify, not target values. Names differ slightly
  between the 2011 and 2023 editions — cite the characteristic, not a numbered clause.

**ATAM (Architecture Tradeoff Analysis Method, SEI) & quality-attribute scenarios**
- Covers: eliciting business drivers, writing scenarios (source, stimulus, environment, artefact,
  response, response measure), building a utility tree, and finding sensitivity points, trade-off
  points, risks and non-risks.
- Invoke when: a significant, costly-to-reverse architecture needs structured evaluation with
  stakeholders. A lightweight version (just the scenarios + trade-off points) fits most reviews.
- Misreading: full ATAM is a multi-day workshop; don't propose it for a two-service change.

## Communicating and recording

**C4 model** — System Context, Container, Component, Code diagrams plus supplementary (deployment,
dynamic). Invoke to align on structure quickly. Misreading: "container" means a separately
runnable/deployable unit (app, database, queue), not a Docker container. Code-level diagrams are
rarely worth maintaining.

**arc42** — a 12-section template (introduction & goals, constraints, context & scope, solution
strategy, building-block view, runtime view, deployment view, cross-cutting concepts, decisions,
quality requirements, risks & technical debt, glossary). Invoke for whole-system documentation.
Misreading: sections are optional; fill what readers need, not all twelve.

**ADRs (Nygard; MADR)** — one decision per short record: title, status, context, decision,
consequences (MADR adds considered options and pros/cons). Invoke for any decision that is
hard to reverse or likely to be questioned later. Misreading: ADRs are not edited when the decision
changes — a new ADR supersedes the old one, preserving history.

## Designing boundaries

**Domain-Driven Design — strategic design (Evans; Vernon)**
- Bounded context = a boundary within which a model and its ubiquitous language are consistent.
  Context map patterns: shared kernel, customer/supplier, conformist, anticorruption layer, open-host
  service/published language, separate ways.
- Invoke when: deciding module or service boundaries, or when one term ("order", "account") means
  different things to different teams.
- Misreading: one microservice per entity/aggregate. Boundaries follow language and rule ownership;
  a bounded context may contain many services or one module.

**Conway's law / Team Topologies**
- Systems mirror the communication structures of the organisations that build them. Team Topologies
  names four team types (stream-aligned, platform, enabling, complicated-subsystem) and three
  interaction modes (collaboration, X-as-a-service, facilitating).
- Invoke when: a boundary requires two teams to change in lockstep, or ownership is unclear.
- Misreading: it is not only descriptive — the "inverse Conway manoeuvre" shapes teams to get the
  architecture you want.

**Hexagonal (Ports & Adapters, Cockburn) / Clean Architecture (Martin) / Onion**
- Common core: the domain does not depend on frameworks, databases or transports; dependencies point
  inward; infrastructure is plugged in via interfaces (ports).
- Invoke when: business logic is valuable and long-lived, or an external dependency is likely to change.
- Misreading: adding interfaces for everything in a CRUD app. Apply where there is logic to protect.

## Keeping architecture healthy over time

**Fitness functions (Building Evolutionary Architectures)** — any objective check of an architectural
characteristic: dependency-rule tests (ArchUnit, dependency-cruiser, import-linter), latency budgets
in load tests, bundle-size limits, coupling metrics in CI. Invoke whenever a design decision
depends on a property staying true. Misreading: it is not a new tool; existing tests and
monitors count if they guard an architectural property.

**Strangler Fig (Fowler)** — put a routing facade in front of the legacy system, move capabilities
one at a time, retire the old path when traffic reaches zero. Pairs with Branch by Abstraction
(in-process) and Parallel Change (interfaces/schemas). Misreading: without a retirement step it
becomes "two systems forever".

## Operating in the cloud / distributed systems

**Cloud Well-Architected frameworks (AWS, Microsoft Azure, Google Cloud)** — pillar-based review
questions: operational excellence, security, reliability, performance efficiency, cost optimisation,
sustainability (naming varies by provider). Invoke for workload reviews; the question sets are
useful even off-cloud. Misreading: they are review lenses, not a compliance standard.

**The Twelve-Factor App** — codebase, dependencies, config, backing services, build/release/run,
processes, port binding, concurrency, disposability, dev/prod parity, logs, admin processes.
Invoke for service deployability. Misreading: some factors (e.g. logs as stdout streams) are
defaults, not laws; justify deviations.

**Fallacies of distributed computing** — the network is reliable; latency is zero; bandwidth is
infinite; the network is secure; topology doesn't change; there is one administrator; transport
cost is zero; the network is homogeneous. Invoke whenever a split adds a network hop.

**CAP / PACELC** — under a network partition choose consistency or availability; else (normal
operation) trade latency against consistency. Invoke for replication, multi-region and cache
decisions. Misreading: "we chose CA" — partitions are not optional in a distributed system.

**Distributed data patterns** — Saga (orchestrated or choreographed compensations), Transactional
Outbox, idempotent consumers, CQRS. Invoke instead of cross-service ACID transactions.
Detail and trade-offs: `architecture_patterns.md`.
