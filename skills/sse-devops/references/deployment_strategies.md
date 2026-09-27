# Deployment strategies

Read on demand. Applies to Kubernetes, VMs, container services, PaaS and serverless; map each
idea onto the project's actual deploy target.

## 1. Choosing a strategy

| Strategy | Blast radius | Rollback speed | Extra cost | Needs | Good for |
|---|---|---|---|---|---|
| Recreate (stop all, start new) | 100% + downtime | Redeploy | None | Tolerable downtime | Batch workers, dev envs |
| Rolling | Grows per batch | Redeploy previous | Low (surge) | N/N+1 compatibility | Default for stateless services |
| Blue/green | 100% at switch | Instant (switch back) | 2× capacity during switch | Compatible data layer, warm-up | Fast, clean cut-over and rollback |
| Canary | Small %, stepwise | Fast (shift traffic back) | Low–medium | Traffic splitting + per-version metrics | High-risk or high-traffic changes |
| Feature flag (dark launch) | Per user/segment | Instant (flip) | Flag debt | Flag system, kill switches | Decoupling deploy from release |
| Shadow / mirroring | None to users | N/A | Duplicate load | Side-effect-free handling | Validating rewrites under real load |

Progressive delivery combines these: deploy dark → canary → progressive traffic increase →
full release, with automated analysis at each step.

## 2. Compatibility during rollout

While versions N and N+1 coexist, every shared surface must work both ways:

- **APIs**: additive changes only; tolerant readers; version or negotiate breaking changes.
- **Messages/events**: consumers handle both formats; deploy consumers before producers for new fields.
- **Cache entries**: new code reads old-format entries (or uses a new key namespace) for a full TTL.
- **Database**: expand–contract; schema must serve both versions.
- **Sessions/tokens**: signing keys and session formats readable by both versions.

Invariant: backward-compatible changes first, breaking changes later, never in the same deploy.

## 3. Canary analysis (Google SRE — canarying releases)

- Compare the canary against a **control** (current version at the same traffic share), not
  against yesterday.
- Choose a few SLIs tied to user impact: error rate, latency p95/p99, saturation, key business
  success rate (e.g. orders completed).
- Define **pass/fail thresholds and observation windows before deploying**; automate the verdict
  and the abort.
- Canary long enough to cover warm-up, caches, scheduled jobs and at least one traffic pattern
  of interest; small canaries need longer windows for statistical signal.
- Tag telemetry with version/deploy attributes (OpenTelemetry resource attributes) so the
  comparison is possible at all.

## 4. Feature flags (OpenFeature as the vendor-neutral API)

- Separate **release toggles** (short-lived, remove after rollout), **ops/kill switches**
  (long-lived, documented), **experiment** and **permission** toggles.
- Flags have an owner and an expiry; stale flags are tech debt and a test-matrix explosion.
- Default value must be safe when the flag service is unreachable.
- A flag flip is a production change: audit it, and watch the same signals as a deploy.

## 5. Graceful shutdown and zero-downtime (Twelve-Factor "disposability")

On termination (Kubernetes pod termination lifecycle; equivalent on other platforms):

1. Instance is removed from load balancing — this propagates asynchronously.
2. `preStop` hook (or a short sleep) covers the propagation delay so new requests stop arriving.
3. Process receives **SIGTERM**: stop accepting new work, finish in-flight requests, stop
   consumers (commit offsets / nack unprocessed messages), close pools.
4. Exit before the **grace period** ends, or be killed (SIGKILL) mid-flight.

Checks:
- Grace period ≥ longest request/job + drain time; long jobs must be checkpointed/resumable.
- The process is PID 1 or behind an init that forwards signals.
- Scheduled jobs: leader election or distributed lock so scaling/overlapping versions don't run them twice.

## 6. Health probes

- **Readiness**: "can I serve traffic now?" — may check critical dependencies with care; failing
  removes the instance from traffic, not the fleet.
- **Liveness**: "am I wedged?" — check only the process itself. Dependency checks in liveness
  turn a DB blip into a fleet-wide restart storm.
- **Startup**: protects slow-starting apps from premature liveness kills.
- Probes must be cheap, fast and time-bounded.

## 7. Rollback and roll-forward

- Rollback = redeploy the previous known-good artifact (kept in the registry) or flip the flag.
  Measure and rehearse the time it takes.
- Some changes are one-way: destructive migrations, published events, emails sent, external
  payments captured, files deleted. Identify them **before** deploying and gate them separately.
- Roll forward only when the fix is small, understood and faster than rollback — decided by a
  pre-agreed rule, not in the heat of the incident.
- **Abort criteria are numeric** (e.g. error rate above baseline + X for Y minutes, p99 above Z):
  "keep watching" is not a criterion.

## 8. Timing and coordination

- Avoid deploy windows that collide with peak traffic, batch runs, or scheduled jobs — or make
  them safe to interrupt.
- Deploy one change at a time where possible; batching changes hides which one failed.
- Add deploy markers/annotations to dashboards automatically.
- Multi-region/multi-cluster: roll out one failure domain at a time, bake between steps.

## 9. Serverless and managed platforms

- Use weighted aliases/versions or traffic-splitting features for canary.
- Cold starts, concurrency limits and downstream connection limits (e.g. database connections per
  concurrent execution) are the usual deploy-time surprises.
- Event-source mappings and queues continue delivering during rollout — handlers must be idempotent.
