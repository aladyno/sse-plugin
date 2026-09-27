# Design review cheatsheet — questions, numbers, formulas

Read on demand. A question bank and estimation aid for challenging a design already on the table —
not a process to run. Generic material: project evidence and measured numbers override it; the
figures below are orders of magnitude, not targets.

## Questions that expose the expensive decision

**Load & shape**
- Peak vs average QPS, and the peak-to-average ratio? (Assume 3–10× if unknown — and say so.)
- Read/write ratio per data path? Which path is latency-critical, which can be async?
- Largest tenant/customer as a share of load? (Hot tenant = hot partition.)
- Growth horizon the design must survive without re-architecture: 12 months? 10×?

**Data**
- Who is the single writer of each store? Who reads it, from where (primary, replica, cache)?
- Consistency each reader actually needs: read-your-writes, bounded staleness (how many seconds?), eventual?
- Retention and deletion obligations? What happens to replicas, caches, backups on delete?
- Largest entity/payload size, and how it grows?

**Failure**
- What happens to the user journey when each dependency is down for 30 minutes?
- Which failure is silent (wrong data, lost message) rather than loud (error)?
- RPO/RTO per store — who set them, and has a restore been timed?

**Change**
- Which part of this design is a one-way door? What would it cost to undo in 12 months?
- Can old and new versions run side by side during rollout?
- Which team owns each new component, and who is on call for it?

## Latency ladder (orders of magnitude)

| Operation | Approx. |
|---|---|
| Main-memory reference | ~100 ns |
| Read 1 MB sequentially from memory | ~10–50 µs |
| Round trip within one datacenter / availability zone | ~0.5 ms |
| Round trip across availability zones (same region) | ~1–2 ms |
| Random read, SSD | ~0.1 ms |
| Indexed point lookup in a warm database | ~1 ms |
| Round trip across continents | ~100–150 ms |
| TLS handshake over a cross-continent link | 1–2 extra round trips |

Rule of thumb: **each synchronous hop adds its p99, not its average**, to the caller's tail.

## Estimation formulas

| Quantity | Formula | Note |
|---|---|---|
| Average QPS | daily requests ÷ 86,400 | ~100k/day ≈ 1.2 QPS; 100M/day ≈ 1,200 QPS |
| Peak QPS | average × peak factor | Use the measured factor; else 3× and state it |
| Concurrency needed (Little's Law) | L = λ · W | 1,000 QPS × 0.2 s = 200 in-flight requests |
| CPU cores | peak QPS × CPU-seconds per request ÷ target utilisation | Target 60–70 % to absorb spikes and failover |
| Instances | ceil(cores needed ÷ cores per instance) + N+1 (or N+2) | Redundancy for one instance/zone loss |
| Storage per year | records/day × bytes/record × 365 × index factor × replicas | Index factor ~1.5–2×; replicas usually 2–3× |
| Bandwidth | peak QPS × average response size | 3,600 QPS × 10 KB ≈ 36 MB/s ≈ 290 Mbit/s |
| Connection budget | pool size × instances × services ≤ server connection limit | Recheck after autoscaling max |
| Composite availability (serial) | A₁ × A₂ × … × Aₙ | Three 99.9 % dependencies in series ≈ 99.7 % |
| Error budget | (1 − SLO) × period | 99.9 % over 30 days ≈ 43 minutes |

## Scaling levers — what each costs

| Lever | Buys | Costs |
|---|---|---|
| Vertical scale | Time, zero redesign | Hard ceiling; single failure domain |
| Horizontal stateless instances | Linear throughput | Needs externalised state; connection budget grows |
| Read replicas | Read throughput | Replica lag; read-after-write routing |
| Cache | Latency, offloaded reads | Invalidation, stampede, key-dimension bugs |
| Async queue | Smoothed peaks, decoupling | Eventual consistency, backlog and DLQ operations |
| Partitioning / sharding | Write throughput, data size | Shard-key lock-in (one-way door), cross-shard queries |
| CDN / edge | Static and cacheable latency | Purge semantics, stale content |

## Bottleneck signals by layer

| Layer | Signal |
|---|---|
| Edge / load balancer | Connection limits, TLS CPU, uneven distribution |
| Application | Worker/thread pool saturation, GC pauses, queueing before work starts |
| Database | Pool wait time, lock waits, rows examined ≫ rows returned, replica lag |
| Cache | Miss-rate spikes, evictions, hot keys |
| Queue | Backlog age growing, consumer lag, DLQ growth |
| Network | Bandwidth saturation, cross-zone traffic cost |

## Migration strategy trade-offs

| Strategy | Risk | Downtime | Reversibility |
|---|---|---|---|
| Big bang | High | Usually | Poor — rollback is another migration |
| Blue/green | Medium | Minimal | Good for code; data must stay compatible |
| Canary / percentage routing | Low | None | Good — shift traffic back |
| Strangler fig | Low | None | Good per slice; plan retirement or keep two systems forever |

Before any migration step, the design must name: the numeric rollback trigger (error rate,
p99, data mismatch count), the rollback time estimate, and whether data written by the new side
can flow back to the old one.
