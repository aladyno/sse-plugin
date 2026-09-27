# Maintenance standards & proven practice — deeper notes

Read on demand. For each: what it covers, when to invoke it, and how it is commonly misread.
Cite by name; never invent clause numbers. This is gap-analysis vocabulary, not certification.

## Framing maintenance work

**ISO/IEC/IEEE 14764 — Software maintenance**
- Covers: the maintenance process (implementation, problem and modification analysis, modification
  implementation, review/acceptance, migration, retirement) and the categories of maintenance:
  corrective (fix faults found), preventive (fix latent faults before they fail), adaptive (keep
  working in a changed environment), perfective (improve performance/maintainability).
- Invoke when: prioritising a backlog that mixes bug fixes, upgrades and cleanup — the category
  explains urgency and who should fund it. Also for *retirement*: the standard treats retiring
  software as a planned activity, not a deletion.
- Misreading: it is not a lifecycle model; it plugs into ISO/IEC/IEEE 12207 life-cycle processes.

**ISO/IEC 25010 — Maintainability**
- Sub-characteristics: modularity, reusability, analysability, modifiability, testability.
- Invoke when: arguing for debt reduction. Tie each item to a sub-characteristic and a measure
  (e.g. change lead time in the module, test coverage of the critical path, defect density).
- Misreading: maintainability is not "code looks clean"; it is the cost and risk of the next change.

## Pricing and classifying debt

**Technical Debt Quadrant (Martin Fowler)** — reckless/prudent × deliberate/inadvertent. Prudent
deliberate debt ("ship now, refactor after launch") is legitimate if recorded with a payback trigger.
**SQALE method** — models debt as remediation cost per quality characteristic, making it comparable
and aggregatable (many static-analysis tools report a SQALE-style "debt ratio").
- Invoke when: a debt item needs priority. Express both **remediation cost** and **interest**
  (the recurring cost of leaving it: incidents, toil, slower lead time).
- Misreading: tool-reported debt minutes are not business impact. Hotspots (churn × complexity)
  tell you which debt actually charges interest.

## Changing code safely

**Refactoring (Fowler, 2nd ed.)** — behaviour-preserving transformations in small named steps
(extract function, move field, replace conditional with polymorphism…), tests green after each.
Misreading: "refactoring" used for rewrites or behaviour changes. If behaviour changes, it is not
a refactor — separate the commits.

**Working Effectively with Legacy Code (Feathers)** — legacy code = code without tests. Find seams,
break dependencies, write characterization tests that pin current behaviour (even if wrong), then
change. Invoke for any change to untested, critical code.

**Mikado Method (Ellnestam & Brolund)** — attempt the goal naively; when it breaks, note the
prerequisites as a graph, revert, and solve prerequisites from the leaves up; the main branch stays
releasable. Invoke for large refactors or upgrades with tangled dependencies.

**Strangler Fig / Branch by Abstraction / Parallel Change (expand–contract)**
- Strangler Fig: facade routes traffic between old and new systems; migrate capability by capability.
- Branch by Abstraction: introduce an interface in-process, implement new behind it, switch, delete old.
- Parallel Change: for interfaces, schemas, messages — expand (add new alongside old), migrate
  (move all callers/data), contract (remove old). Each phase is a separate, revertible deploy.
- Misreading: skipping "contract" — debt doubles. Skipping "migrate verification" — you delete
  something still used. Measure remaining usage before contracting.

## Versioning, changelogs, deprecation

**Semantic Versioning 2.0.0** — MAJOR.MINOR.PATCH; MAJOR for incompatible API changes, MINOR for
backward-compatible features, PATCH for backward-compatible fixes; 0.y.z means anything may change.
Invoke for anything consumed by others (libraries, APIs, events, CLIs). Misreading: SemVer describes
the *public API* you declare — undeclared behaviour consumers rely on (Hyrum's law) still breaks them.

**Keep a Changelog** — curated, human-oriented changelog with Added / Changed / Deprecated / Removed /
Fixed / Security, newest first, an "Unreleased" section. Misreading: a git log dump is not a changelog.

**HTTP deprecation signalling** — RFC 8594 defines the `Sunset` response header (when a resource
will stop responding); the `Deprecation` response header signals that a resource is deprecated.
Combine with `Link` to migration docs, usage telemetry per consumer, and a published policy
(minimum notice period). Misreading: headers alone don't migrate anyone — track who still calls.

## Operability and delivery

**Google SRE (Site Reliability Engineering; The SRE Workbook)**
- Toil: manual, repetitive, automatable, tactical work that scales with service size — measure it and
  cap it. Blameless postmortems: timeline, impact, contributing factors, owned action items.
- Error budgets: when the SLO budget is spent, reliability work (often maintenance) takes priority.
- Invoke when: arguing for maintenance capacity, or learning from a change-induced incident.

**DORA metrics** — deployment frequency, lead time for changes, change failure rate, time to restore
service (recent DORA reports also discuss rework rate). Invoke to show whether maintenance improves
delivery. Misreading: using them as individual performance targets.

## Dependency and supply-chain hygiene

- **SBOM** in SPDX or CycloneDX format — know exactly which components and versions you ship; the
  basis for answering "are we affected?" when a CVE drops.
- **OpenSSF Scorecard** — automated health checks of upstream projects (maintenance activity,
  branch protection, signed releases, dependency update tooling…). Use when choosing or keeping a dependency.
- **SLSA** — levels of build provenance and integrity for artefacts you produce or consume.
- **Upgrade discipline** — one major version at a time; read breaking-change notes/migration guides;
  full test suite after each step; upgrade before the runtime/framework reaches end-of-life, not after.
- Misreading: "automated update PRs = hygiene". Unreviewed, unmerged update PRs are just noise; the
  measure is time-to-patch for critical vulnerabilities.
