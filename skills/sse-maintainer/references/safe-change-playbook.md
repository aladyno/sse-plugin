# Safe-change playbook

Read on demand. Generic sequences for changing things that other code, data or people depend on.
Project facts (deploy model, migration tool, cache TTLs, consumer list) override these defaults.

## 1. Universal rule: expand → migrate → contract

Every step is its own deploy, independently revertible, and observed before the next one.

| Phase | Do | Gate before next phase |
|---|---|---|
| Expand | Add the new thing alongside the old (column, field, endpoint, key, config, interface) | New path deployed everywhere; old path untouched |
| Migrate | Move writers, then readers, then backfill existing data | Usage telemetry shows zero traffic/rows on the old path for an agreed window |
| Contract | Remove the old thing | Rollback plan no longer needs the old path |

## 2. Sequences by change type

**Database column rename / type change**
1. Add new column (nullable or with safe default). 2. Dual-write old + new. 3. Backfill in batches
(idempotent, resumable, throttled). 4. Switch reads to new; compare results. 5. Stop writing old.
6. Drop old column in a later release. Never rename in place while old code is still running.

**Enum / status value change**
Readers must accept the new value **before** any writer emits it. Check stored rows and in-flight
messages for old values; decide whether to migrate them or keep a mapping forever.

**Public API / event contract change**
Additive changes only within a version (new optional fields; tolerant readers ignore unknowns).
Breaking change → new version side by side, deprecation signal (`Deprecation`/`Sunset` headers or
event metadata), per-consumer usage tracking, published sunset date, then removal.

**Cache format change**
Change the **key** (version it, e.g. `v2:` prefix) together with the format. Old and new instances
coexist during rollout; entries in the old format live until TTL expiry.

**Config / feature flag**
New keys get defaults that preserve current behaviour. Remove a flag only after it has been at 100%
for an agreed period and the old branch is deleted from code first.

**Module / package move or rename**
Check convention-based wiring (DI scanning, routing, plugin discovery, serialization type names,
reflection, string-referenced queries/templates) — these fail at runtime, not compile time.
Keep a forwarding alias for one release when the name is public.

**Dependency / runtime upgrade**
One major version at a time; read the migration guide; isolate the upgrade in its own change;
full test suite + smoke test; watch error rate and latency after deploy.

**Deleting "dead" code**
Prove it is dead: static callers = 0, hidden callers (jobs, consumers, reflection, config, other
repos) = 0, runtime telemetry = 0 over a representative period (including month-end/batch cycles).
Optionally log-and-keep for one release before deletion.

## 3. Rollback order

- Roll back in **reverse order of deployment**; consumers before producers when a contract changed.
- Code can roll back; **data usually cannot**. A migration that dropped, rewrote or backfilled data
  makes the release effectively one-way — say so before deploying and prefer roll-forward plans.
- Rollback must be rehearsed or at least written down: trigger (metric + threshold), steps, owner,
  expected time.

## 4. Incident triage from the maintainer lens

1. Pin **when it started** (first bad signal, not first report).
2. List **every change before that moment**: deploys, config/flag flips, migrations, dependency
   updates, traffic shifts, third-party changes, certificate/secret expiry, cache TTL boundaries.
3. Mitigate first (revert/flag off) if a recent change correlates; root-cause after.
4. Postmortem action items must name an owner and a detection improvement.

## 5. Pricing a debt item

| Field | Content |
|---|---|
| Location | Module/file/table |
| Category | Corrective / preventive / adaptive / perfective (ISO/IEC/IEEE 14764) |
| Interest | Recurring cost if left: incidents, toil hours, lead-time drag, security exposure |
| Principal | Effort to fix, including tests and migration |
| Blast radius | Which rings (callers, hidden, data, contract, operations) the fix touches |
| Trigger | The event that makes it urgent (EOL date, scale threshold, next feature in that area) |
| Recommendation | Quick win / planned / defer, with the first safe step |

Prioritise by interest ÷ principal, adjusted by risk; debt in low-churn code rarely charges interest.
