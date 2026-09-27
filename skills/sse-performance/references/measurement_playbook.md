# Performance measurement playbook — condensed notes

Read on demand. Cite by name; never invent numbers. Verify tool flags against the version the
project actually uses before suggesting a command.

## 1. Pick the tool by where the time goes

| Symptom | Category | Tools (examples, by stack) |
|---|---|---|
| High CPU, latency scales with CPU | On-CPU | JVM: async-profiler, JFR · .NET: dotnet-trace, PerfView · Go: pprof (cpu) · Node.js: `--cpu-prof`, 0x, clinic flame · Python: py-spy, cProfile · Native/Linux: `perf` + flame graphs |
| Low CPU, high latency | Off-CPU / waiting | Distributed traces (OpenTelemetry), async-profiler wall/lock mode, JFR thread/lock events, Go pprof block/mutex, pool wait metrics, slow-query log |
| Memory growth, GC pauses | Allocation / GC | GC logs, JFR allocation, async-profiler alloc, Go pprof heap/allocs, dotnet-counters/dotnet-gcdump, heap dumps |
| Requests wait before running | Queueing | Pool active/idle/pending metrics, executor queue depth, event-loop lag (Node.js), accept queue, load-balancer queue time |
| Latency only above some load | Saturation / contention | Load test with a ramp + USE metrics per resource to find the knee |

Rule: classify first (on-CPU vs off-CPU vs queueing), then profile. A CPU flame graph of a
service that is waiting on a pool shows nothing useful.

## 2. Load-test design

- **Open model** (constant arrival rate: k6 `constant-arrival-rate`, Gatling `constantUsersPerSec`,
  wrk2/vegeta rate mode) for request-driven services — it matches real traffic and exposes
  coordinated omission. **Closed model** (fixed virtual users) only for systems where clients
  really do wait (e.g. a fixed worker fleet).
- **Workload mix** from production: endpoint ratios, payload sizes, cache-hit ratio, data
  distribution (hot keys, large tenants). A single-endpoint test answers a single-endpoint question.
- **Shapes**, each answering one question:
  - *Baseline* — expected load, steady — "do we meet the target today?"
  - *Ramp / stress* — step load up until errors or latency bend — "where is the knee, which
    resource saturates first?"
  - *Soak* — expected load for hours — "leaks, pool exhaustion, GC drift, log/disk growth?"
  - *Spike* — sudden burst — "does autoscaling / load shedding react in time?"
- **Pass/fail in the script** (k6 thresholds, Gatling assertions): percentile + error-rate limits,
  so the test is a gate, not a chart.
- Check the **load generator** itself (CPU, sockets, bandwidth) — if it saturates, the result is
  its limit, not the system's.

## 3. Benchmark hygiene

- Use the stack's harness (JMH, BenchmarkDotNet, `go test -bench` + `benchstat`, Criterion,
  pytest-benchmark) — they handle warm-up, dead-code elimination and statistics.
- Warm up; pin versions, config and instance type; same data volume as production or state the gap.
- Run multiple iterations; report distribution and variance; compare with a statistical tool
  (`benchstat`, harness confidence intervals) rather than eyeballing one number.
- Change **one** variable per comparison.
- Micro-benchmark wins only matter if the function is a meaningful share of end-to-end time
  (Amdahl) — confirm with a profile of the real request path.

## 4. Reading results

- Report **p50 / p95 / p99 / max** plus throughput and error rate at that load; never only the mean.
- Tail latency percentiles cannot be averaged across instances or time windows — merge histograms
  (HdrHistogram, Prometheus histograms with `histogram_quantile`) instead.
- Separate latency of successful and failed requests (fast failures make latency look better).
- Plot latency against throughput: the knee is the capacity; operate with headroom below it.
- Little's Law cross-check: in-flight requests ≈ RPS × mean latency. If observed concurrency is far
  off, a queue or a measurement error is hiding somewhere.

## 5. Keeping the gain

- Add a regression guard proportional to risk: a benchmark with a threshold in CI, a load-test
  gate before release, or a latency SLO alert after release.
- Record the baseline, change and result (environment, version, data size) next to the change —
  a number without its conditions cannot be re-checked.
