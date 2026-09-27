# Database standards & proven practice — condensed notes

Read on demand. Cite by name; never invent clause numbers. Verify engine-specific behaviour
against the project's actual engine and version before relying on it.

## 1. Isolation levels and anomalies

**ISO/IEC 9075** defines four levels by the phenomena they prohibit:

| Level | Dirty read | Non-repeatable read | Phantom |
|---|---|---|---|
| READ UNCOMMITTED | possible | possible | possible |
| READ COMMITTED | prevented | possible | possible |
| REPEATABLE READ | prevented | prevented | possible |
| SERIALIZABLE | prevented | prevented | prevented |

**Berenson et al., "A Critique of ANSI SQL Isolation Levels"** shows these definitions are
incomplete. Anomalies to test against every invariant:

- **Lost update** — two read-modify-write cycles; the second overwrites the first.
- **Read skew** — reading two related rows at different points in time.
- **Write skew** — two transactions each read an overlapping set, each writes a disjoint row; the
  combined result violates an invariant (classic: "at least one on-call doctor").
- **Snapshot isolation** prevents the three standard phenomena but still allows write skew.

Engine reality (check the version in use):

- Defaults differ: several engines default to READ COMMITTED, others to REPEATABLE READ.
- Some engines' REPEATABLE READ is snapshot-based; some use gap/next-key locks to block phantoms
  for locking reads only; some SERIALIZABLE implementations are true serializable snapshot
  isolation (abort-on-conflict → the application must retry).
- Consistent reads and locking reads (`SELECT … FOR UPDATE` / `FOR SHARE`) can see different data
  in the same transaction on some engines.

Tactics, cheapest first: a unique/check/foreign-key constraint; an atomic single-statement update
(`SET qty = qty - 1 WHERE qty > 0`); optimistic concurrency (version column, check affected rows);
explicit row locks in a consistent order; SERIALIZABLE with retry on serialization failure.

## 2. Consistency models: ACID, BASE, CAP, PACELC

- **ACID** — per-transaction guarantees inside one database.
- **BASE** — basically available, soft state, eventually consistent; typical of distributed stores.
- **CAP** — during a network partition, choose consistency or availability.
- **PACELC** — if Partition: A or C; Else: Latency or Consistency. The "else" branch is the
  everyday trade-off (replica reads, quorum sizes, per-request consistency levels).
- For every read path, state: may it be stale? by how much? who notices? Quantify lag tolerance.

## 3. Schema design

- Normalise to **3NF/BCNF** by default: every fact stored once, invariants enforced by keys.
- Denormalise deliberately: a measured hot read path, a named mechanism keeping copies consistent
  (trigger, same-transaction write, event-driven projection), and a rebuild procedure.
- Prefer constraints in the database (NOT NULL, UNIQUE, CHECK, FK) over application-only checks —
  they hold under concurrency and across every writer.
- Surrogate vs natural keys: surrogate for stability; still enforce the natural key as UNIQUE.
- Money: exact numeric types, never floating point. Time: store UTC or timezone-aware types.

## 4. Indexing (Use The Index, Luke)

- B-tree: usable for equality and range on a **left prefix** of the key.
- Column order: equality → range → sort. After the first range column, later columns filter but
  no longer narrow the seek.
- Covering (index-only) access avoids table lookups; watch the visibility-map / heap-fetch caveat
  on MVCC engines.
- Pagination: **keyset/seek** (`WHERE (k1, k2) > (:last1, :last2) ORDER BY k1, k2 LIMIT n`) instead
  of `OFFSET`, whose cost grows with page number.
- Partial/filtered and expression/functional indexes fix specific sargability problems where supported.
- Every index costs writes, storage, buffer-pool space and a build (lock + replication) event. Remove unused ones.
- Read plans with actual row counts; large estimate-vs-actual gaps mean stale statistics or
  correlated predicates.

## 5. Safe schema change: expand–contract (parallel change)

Evolutionary Database Design (Ambler & Sadalage): small, versioned, automated migrations,
tested in CI like code. For any change touching columns live code uses:

1. **Expand** — add the new column/table/index; nullable or defaulted; nothing removed.
2. **Dual write** — new code writes both shapes; old code keeps working.
3. **Backfill** — in bounded batches with checkpoints, throttled by replica lag; idempotent and resumable.
4. **Switch reads** — behind a flag where possible; verify with comparison queries.
5. **Stop old writes** — release N+1.
6. **Contract** — drop the old shape in a later release, after the rollback window closes.

Rules: never ship a destructive step in the same deploy as the code change that depends on it;
each release must work with the schema of the previous and next step; the migration itself must
be rerunnable or clearly guarded.

## 6. Online schema change on large tables

- Know what the engine's native online DDL can do for *this* operation without a table rewrite
  or long exclusive lock — it varies by operation and version.
- Copy-and-swap tools (gh-ost, pt-online-schema-change) build a shadow table, sync changes, then
  cut over; pg_repack rebuilds tables/indexes online. All need: disk headroom (~table size),
  throttling on replica lag/load, a planned cut-over window, and a tested abort path.
- Even "online" operations take brief metadata/exclusive locks; a long-running query ahead of
  them can queue every subsequent query behind the DDL. Set a lock timeout and retry.
- Build indexes concurrently/online where supported; check for invalid leftovers on failure.

## 7. Messaging and the database

- **Transactional outbox**: write business rows and an outbox row in one transaction; a relay
  publishes and marks sent. Delivery is at-least-once → consumers must be idempotent (dedupe key
  or natural idempotency).
- Change data capture from the log is an alternative relay.
- Never call remote services inside an open transaction: locks are held for network latency, and
  a rollback cannot undo the remote side effect.

## 8. Connections, pools and replicas

- HikariCP "About Pool Sizing": throughput peaks at a small pool; a starting point is
  `connections ≈ (core_count × 2) + effective_spindle_count` on the DB side, then measure.
- Budget: Σ over services (pool max × max instances, including autoscaling, batch jobs and
  migrations) + admin headroom ≤ server connection limit. Poolers (transaction mode) change
  semantics: session state, prepared statements and advisory locks may break.
- Pool wait time is the signal, not pool utilisation alone.
- Replicas: route only lag-tolerant reads; read-your-writes paths go to the primary or use
  session stickiness / LSN-GTID waiting. Alert on lag; decide behaviour when lag exceeds tolerance.
- Failover: connection strings/DNS TTL, driver retry, and in-flight transaction handling must be
  tested, not assumed.

## 9. Backup, recovery and continuity

- **RPO** (max acceptable data loss) and **RTO** (max acceptable downtime) come from the business
  impact analysis — ISO 22301 frames this as part of business continuity management.
- **3-2-1**: three copies, two storage types, one off-site; add an immutable or offline copy.
- Point-in-time recovery requires continuous log archiving; verify retention covers the RPO.
- A backup is unproven until a restore is performed and timed against the RTO — schedule drills.
- Well-Architected reliability pillars (AWS/Azure/Google Cloud): automate recovery, test it,
  replicate across failure domains in proportion to the RTO.

## 10. Data lifecycle and privacy

- GDPR principles most relevant to schema design: **data minimisation**, **storage limitation**,
  **purpose limitation**, and the **right to erasure**.
- Design retention per table: TTL/archival job, partition drop instead of mass delete where
  possible, and legal-hold exceptions.
- Erasure must reach replicas, analytics copies, caches, search indexes and — per policy — backups
  (expire them, or re-apply deletions on restore).
- Pseudonymise or tokenise PII columns used only for joins/analytics; keep PII out of logs and
  slow-query captures.

## 11. Injection and access

- OWASP SQL Injection Prevention Cheat Sheet: parameterised queries / prepared statements first;
  stored procedures only if they don't build dynamic SQL internally; allow-list for identifiers
  (sort column, direction, table name); escaping is a last resort.
- ORMs are not immune: raw-query escape hatches and string-built `ORDER BY` are the usual holes.
- Least privilege: application accounts without DDL rights; separate migration account; read-only
  accounts for replicas and reporting.
