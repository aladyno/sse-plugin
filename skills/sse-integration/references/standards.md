# Integration standards — deeper notes

Read on demand. Expands the standards map in `SKILL.md` into the numbers and checklists that
usually decide an integration review. Partner documentation and the project's own config always
take precedence; where a partner's behaviour is unknown, write "needs verification".

## 1. Timeout budget

- Set **connect** and **read/response** timeouts separately, plus an **overall deadline** for the
  whole operation including retries.
- Derive from data, not defaults: a common starting point (AWS Builders' Library) is the partner's
  measured high-percentile latency (e.g., p99.9) plus margin, then check the false-timeout rate.
- Budget top-down: caller deadline > our overall deadline > (attempts × per-attempt timeout +
  backoff). Example: gateway 10 s → our operation 8 s → at most 2 attempts × 3 s + 1 s backoff.
- Propagate the remaining deadline downstream (gRPC deadlines, or a context/header value) so the
  partner call isn't started when the budget is already spent (Google SRE, cascading failures).
- Many HTTP clients default to **no timeout** or very long ones — verify the effective value, not
  just the configured one (pool acquire timeout counts too).

## 2. Retry policy

| Decide | Guidance |
|---|---|
| **What** to retry | Network errors, 408, 429, 502, 503, 504 — only if the operation is idempotent or carries an idempotency key. Never plain 4xx validation/auth errors. |
| **How many** | Small cap (commonly 2–3 attempts total) for user-facing calls; more only for async work with a deadline. |
| **Delay** | Capped exponential backoff with jitter ("full jitter": random between 0 and the exponential cap). Honour `Retry-After` when present. |
| **Where** | One layer only. Retries at client + SDK + service mesh + caller multiply (3 × 3 × 3 = 27 calls). |
| **Budget** | Limit retries to a fraction of normal traffic (token bucket / retry budget; the Google SRE book describes a per-client budget of roughly 10%) so retries can't amplify an outage. |
| **Hedging** | Hedged/backup requests cut tail latency for idempotent reads only ("The Tail at Scale", Dean & Barroso) — and cost extra load. |

## 3. Ambiguous outcomes and reconciliation

A timeout or 5xx after the request was sent means **unknown**, not failed.

1. Persist intent before calling (state `PENDING`, with our reference and the idempotency key).
2. On unknown outcome: query the partner's status/retrieve endpoint by our reference, or replay
   with the **same** idempotency key if the partner supports it.
3. If neither exists: park in a reconciliation queue; a scheduled reconciler compares both sides and
   resolves; after N attempts, escalate to a human with full context.
4. Only mark `FAILED` when the partner confirms failure; only mark `DONE` when confirmed success.
5. Monitor: count of items stuck in `PENDING` older than X, reconciliation mismatches.

Multi-step workflows: model as a **saga** — each step has a compensating action; record progress so
a crash can resume or compensate, never leave half-done state silently.

## 4. Circuit breakers, bulkheads, rate limits

- **One breaker per partner (and per critical operation)**, not one global breaker.
- Trip on failure rate **and** slow-call rate over a minimum volume; half-open with a few trial
  calls; define the open-state behaviour explicitly (error, degrade, cached/stale, defer to queue).
- **Bulkhead**: separate connection pool / concurrency limit per partner so one slow partner cannot
  consume all threads or connections (Release It!).
- **Client-side rate limiting** to the partner's published quota, shared across instances when the
  quota is per account (a distributed limiter or a fixed share per instance).
- On recovery, **ramp up** (gradual concurrency) and drain backlogs at a controlled rate — prefer
  fresh work over stale work when backlog items have lost their value (AWS Builders' Library,
  insurmountable queue backlogs).

## 5. Delivery semantics (messaging)

| Guarantee | Reality | Consequence |
|---|---|---|
| At-most-once | Messages can be lost | Only for disposable data (metrics, hints) |
| At-least-once | Duplicates will happen | Default; consumers must be idempotent |
| Exactly-once | Holds only inside one system's transaction boundary | Any external side effect is still at-least-once → idempotent consumer |

- **Idempotent Receiver** (EIP): dedupe by message id / business key stored in the same transaction
  as the side effect.
- **Transactional outbox**: write business state and the outgoing event in one local transaction;
  a relay publishes. Avoids "DB committed, publish failed" and the reverse.
- **Ordering**: only guaranteed per partition/key; design handlers to tolerate out-of-order
  (versions/timestamps, last-writer rules) unless ordering is truly required.
- **Poison messages**: bounded retries, then **Dead Letter Channel** with alerting and a replay tool.
- **Envelope**: CloudEvents attributes (`id`, `source`, `type`, `time`, `subject`) plus a
  correlation id; describe channels and payloads in AsyncAPI.
- **Large payloads**: Claim Check (store payload, send a reference).

## 6. Webhooks checklist

Receiving:
- Verify signature (HMAC over the **raw** body + timestamp + id, per Standard Webhooks or the
  partner's scheme) with constant-time comparison; reject outside a short timestamp window.
- Deduplicate by webhook/message id; treat events as hints and re-fetch state when order matters.
- Acknowledge quickly (2xx) after durable enqueue; process asynchronously.
- Allow secret rotation (multiple valid secrets during rotation).

Sending:
- Sign every delivery; include id and timestamp; retry with backoff over a documented window;
  disable endpoints after sustained failure and notify the owner; offer replay.
- Guard against SSRF when customers supply target URLs (block internal address ranges).

## 7. Contracts and change

- Sync APIs: OpenAPI as the contract; breaking-change detection in CI; **consumer-driven contract
  tests** (Pact) so providers learn which fields consumers actually use.
- Async APIs: AsyncAPI + schema registry with compatibility rules (backward/forward).
- **Tolerant Reader**: ignore unknown fields, don't fail on new enum values — map them to an
  explicit "unknown" and alert.
- Versioning: Semantic Versioning for SDKs/schemas; watch partner `Deprecation` (RFC 9745) and
  `Sunset` (RFC 8594) headers and changelogs; track an owner and sunset date per integration.
- **Anti-corruption layer**: translate partner models into our canonical model at the adapter;
  normalise time zones (store UTC + original zone when it matters), currencies (ISO 4217 codes,
  minor units), country codes (ISO 3166), language tags (BCP 47), timestamps (RFC 3339).

## 8. Partner authentication

- OAuth 2.0 client credentials (RFC 6749) for service-to-service; follow the OAuth 2.0 Security BCP
  (RFC 9700): short-lived tokens, least-privilege scopes, sender-constrained tokens (mTLS per
  RFC 8705, or DPoP) where supported.
- Cache tokens until shortly before expiry; refresh single-flight (one refresh, not one per request).
- API keys and secrets in a secret manager with rotation; never in code, logs or URLs.

## 9. Evidence to ask for

Per partner: request rate, error rate by class (timeout / 4xx / 5xx / 429), p50/p99 latency,
circuit state changes, retry count ratio, backlog size and age, reconciliation mismatches, and the
date of the last contract change. No evidence → the first recommendation is to add it
(`/sse-plugin:observe`).
