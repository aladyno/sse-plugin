# Runtime correctness by stack

Read on demand. The framework in `SKILL.md` is stack-neutral; this file lists what each failure
mode looks like in common runtimes. Always confirm the project's actual versions and libraries
first — behaviour changes between versions.

## 1. Pick the model first

| Model | Examples | Scarce resource | Classic killer |
|---|---|---|---|
| Thread-per-request (platform threads) | Servlet containers, classic ASP.NET, Rails/Django workers | Worker threads, memory per thread | Slow downstream holds threads → pool exhaustion → queueing |
| Event loop, single thread | Node.js, Python asyncio, Netty/Vert.x loops | The loop itself | One blocking call stalls every in-flight request |
| Reactive streams | Project Reactor, RxJava, Akka Streams, Mutiny | Event-loop threads + demand | Blocking inside operators; unbounded `flatMap`; lost context |
| Lightweight threads / coroutines | Go goroutines, JVM virtual threads, Kotlin coroutines, Erlang/Elixir processes | Downstream capacity (threads are cheap, connections are not) | Unlimited concurrency floods DB/partners; leaked goroutines/coroutines |
| Async/await on a thread pool | .NET async, Rust tokio, Java CompletableFuture | Pool threads, sync-context | Sync-over-async deadlocks and starvation |
| Actors | Akka, Orleans, Erlang/OTP | Mailbox size | Unbounded mailboxes, blocking inside a message handler |

Rule of thumb: cheap concurrency moves the bottleneck — it does not remove it. Always ask what the
**downstream** can absorb.

## 2. Per-stack pitfalls

### Reactive (Project Reactor, RxJava)
- `block()`, `blockingGet()`, `toFuture().get()` inside a pipeline; blocking drivers (JDBC, most
  ORMs, sync SDKs, sync file I/O, sync logging appenders) called inside operators without being
  offloaded to a bounded elastic/IO scheduler.
- `subscribeOn` affects the whole source subscription regardless of position; `publishOn` switches
  downstream operators only. Misplacement means offloading silently doesn't happen.
- `flatMap` without a concurrency argument = unbounded parallel subscriptions → pool drain.
- Empty path forgotten: an empty `Mono` flows to the end and returns 200 with no body; use an
  explicit empty handling (e.g., `switchIfEmpty`) with a defined outcome.
- `onErrorReturn`/`onErrorResume` that swallow the cause; errors mapped differently per branch.
- Request-scoped data must travel in the reactive `Context`, not `ThreadLocal`; MDC/tracing needs
  context-propagation support configured.
- Nothing happens until subscription; `subscribe()` fired-and-forgotten inside a request loses
  errors and outlives the request.
- `collectList()`/`buffer()` on unbounded sources; `cache()` of large results.

### Node.js
- Blocking the event loop: `*Sync` fs/crypto/zlib calls, large `JSON.parse`/`stringify`,
  catastrophic regex, CPU loops. Offload to worker threads or out of process.
- Unhandled promise rejections and floating promises (not awaited) — errors vanish or crash the
  process depending on version/flags.
- No default timeout on many HTTP clients; use `AbortController` / `AbortSignal.timeout` and pass
  the signal all the way down.
- `Promise.all` fails fast and does not cancel the others; `Promise.allSettled` for partial results;
  limit concurrency with a pool/queue instead of mapping thousands of promises at once.
- Streams: respect `write()` return value / `pipeline()` for backpressure.
- Context: `AsyncLocalStorage` for request context; OpenTelemetry relies on it.

### Python asyncio
- Blocking calls inside coroutines (`requests`, sync DB drivers, `time.sleep`, CPU work) → wrap
  with `asyncio.to_thread` / an executor, or use async drivers.
- Tasks created with `create_task` and not referenced can be garbage-collected mid-flight; prefer
  `asyncio.TaskGroup` (structured concurrency) so failures cancel siblings.
- Timeouts via `asyncio.timeout` / `wait_for`; `CancelledError` must not be swallowed.
- `contextvars` for request context; thread-locals don't work across tasks.
- Sync web workers (WSGI/gunicorn): worker count × threads is the concurrency ceiling — size it
  against DB pool size.

### Go
- Goroutine leaks: goroutines blocked forever on channels or I/O without a `context` deadline.
- `http.Client{}` zero value has no timeout; always set client timeouts and pass `ctx` to requests.
- Always close `resp.Body` (and drain if reusing connections); `defer rows.Close()`.
- Unbounded `go func()` fan-out → use `errgroup` with `SetLimit` or a semaphore.
- `context.Context` carries deadlines, cancellation and request values; never store it in structs
  long-term.
- `database/sql` pool: `SetMaxOpenConns`, `SetMaxIdleConns`, `SetConnMaxLifetime` default to
  unlimited/unset — set them explicitly.

### JVM platform threads and virtual threads
- Platform threads: request pool size bounds concurrency; a slow dependency without timeout fills
  the pool. `CompletableFuture.*Async` without an executor uses the shared common pool — keep I/O off it.
- Virtual threads make blocking cheap, but connection pools, rate limits and partner capacity are
  unchanged — add semaphores/bulkheads per downstream.
- Pinning: blocking while pinned to a carrier thread (native frames; `synchronized` on older JDKs)
  reduces throughput — check the JDK version and pinning diagnostics.
- `ThreadLocal`-heavy code (large per-thread caches) multiplies memory with millions of virtual
  threads; prefer scoped values/context objects.
- Structured concurrency APIs keep fan-out scoped; check whether they are final or preview in the
  project's JDK before recommending.

### .NET async
- Sync-over-async (`.Result`, `.Wait()`, `GetAwaiter().GetResult()`) → thread-pool starvation and,
  with a sync context, deadlocks.
- `async void` outside event handlers loses exceptions.
- Pass `CancellationToken` end to end; `HttpClient` should be reused (or via
  `IHttpClientFactory`) to avoid socket exhaustion; set `Timeout`.

### Kotlin coroutines
- `runBlocking` inside request handlers; blocking calls on `Dispatchers.Default` instead of `IO`.
- `GlobalScope` launches escape structured concurrency; use scoped jobs and `SupervisorJob`
  deliberately when siblings should survive a failure.
- `withTimeout` throws `TimeoutCancellationException`; don't catch `CancellationException` broadly.

## 3. Sizing and saturation

- **Little's Law**: in-flight = arrival rate × time in system. 200 req/s × 0.25 s = 50 concurrent
  requests; if each holds a DB connection for the whole request, a pool of 20 queues.
- **Pool sizing heuristic** for a DB connection pool: start small (the PostgreSQL wiki / HikariCP
  "About Pool Sizing" guidance of roughly cores × 2 + effective spindles on the DB side), then
  measure. Bigger pools often make the DB slower.
- **Budget across instances**: pool size × instance count (× services sharing the DB) must stay
  under the DB's connection limit with headroom for admin and failover.
- **USE per resource** (threads, connections, CPU, memory, file descriptors): utilisation,
  saturation (wait queue, pending acquires), errors (acquire timeouts).
- **RED per endpoint**: rate, errors, duration (p50/p95/p99) — tail latency is where pool waits show.

## 4. Lifecycle

- Graceful shutdown: stop accepting → drain in-flight requests and consumer batches → close pools.
  The drain window must exceed the longest legitimate request and fit the orchestrator's
  termination grace period.
- Readiness vs liveness: readiness fails while warming up or draining; liveness must not depend on
  downstreams (or a partner outage restarts the whole fleet).
- Every acquired resource (connection, stream, file, lock, lease) released on success, error **and**
  cancellation paths.
- Scheduled jobs: prevent overlap in-process and across instances (lock/lease with expiry);
  make each run idempotent so a crash mid-run can simply re-run.
