# API handler contract patterns (stack-agnostic)

Read on demand. What a backend handler must promise its callers, grounded in HTTP standards.
Framework-specific implementation belongs to `/sse-plugin:implement`; API shape decisions across
services belong to `/sse-plugin:design` / `sse-architect`.

## 1. Method semantics (RFC 9110)

| Method | Safe | Idempotent | Typical use | Runtime consequence |
|---|---|---|---|---|
| GET / HEAD | Yes | Yes | Read | May be retried and cached; must not change state |
| PUT | No | Yes | Replace at a known URI | Retry-safe only if the handler really replaces, not appends |
| DELETE | No | Yes | Remove | Second call must succeed or return a stable "already gone" |
| POST | No | No | Create / trigger action | Needs an idempotency key to be retry-safe |
| PATCH | No | No (unless designed) | Partial update | Prefer conditional requests or idempotency keys |

- **Idempotent** means the intended effect of N identical requests equals one request — not that
  the response is identical.
- Use **conditional requests** (`ETag` + `If-Match`, RFC 9110) for optimistic concurrency on
  updates; `412 Precondition Failed` on a stale version prevents lost updates.

## 2. Error model

- Use **RFC 9457 Problem Details** (`application/problem+json`): `type` (stable URI identifying the
  problem kind), `title`, `status`, `detail`, `instance`, plus extension members (e.g., field
  errors, a correlation/trace ID).
- Status code families carry retry meaning for clients:

| Status | Meaning | Client should retry? |
|---|---|---|
| 400 / 422 | Invalid request / semantic validation failure | No — same input fails again |
| 401 / 403 | Not authenticated / not authorised | No (401: after re-auth) |
| 404 | Not found | No |
| 409 | Conflict with current state (duplicate, version clash) | Only after re-reading state |
| 412 | Precondition failed (stale ETag) | After re-reading |
| 429 | Rate limited (RFC 6585) | Yes, after `Retry-After` |
| 500 | Server bug | Maybe, with backoff — treat as unknown outcome for non-idempotent calls |
| 502 / 504 | Upstream failed / timed out | Yes if idempotent; unknown outcome otherwise |
| 503 | Overloaded / unavailable | Yes, after `Retry-After`, with backoff |

- Never return 200 with an error body; never leak stack traces, SQL or internal hostnames
  (OWASP ASVS error-handling guidance). Detail goes to logs with the correlation ID.
- Map errors **once**, at the edge; inner layers raise typed errors that keep the cause.

## 3. Idempotency keys

Pattern from the IETF draft "The Idempotency-Key HTTP Header Field" and widely used payment APIs:

1. Client generates a unique key per logical operation and resends it on every retry.
2. Server atomically claims the key (unique constraint / conditional insert) **before** executing —
   not check-then-set, which lets two concurrent duplicates both run.
3. Store the request fingerprint; same key with a different payload → reject (commonly 422).
4. Concurrent request while the first is in progress → reject with a retryable conflict (commonly
   409) rather than executing twice.
5. Store the final response and replay it for later retries; expire keys after a documented window
   longer than any client retry horizon.
6. Scope keys per client/tenant; the side effect and the key record should commit together (same
   transaction or an outbox).

## 4. Pagination

| Style | Good for | Watch out for |
|---|---|---|
| Offset/limit | Small, stable datasets, random page access | Deep offsets are slow; rows shift under concurrent writes |
| Cursor / keyset | Large or live datasets, feeds, sync | Cursor must encode a stable, unique sort key; opaque to clients |

- Always cap `limit` server-side; unbounded list endpoints are the "unbounded result set"
  anti-pattern from *Release It!*.
- `total` counts can be expensive; make them optional.

## 5. Versioning and deprecation

- Additive changes (new optional fields, new endpoints) are non-breaking if clients are tolerant
  readers; removing/renaming fields, changing types, tightening validation or changing defaults
  are breaking.
- Version style (path, header, media type) matters less than applying one consistently.
- Announce retirement with the `Deprecation` header (RFC 9745) and `Sunset` header (RFC 8594),
  plus a `Link` to migration docs; measure remaining traffic per client before removal.
- Keep the OpenAPI document as the contract; diff it in CI to catch accidental breaking changes.

## 6. Rate limiting (server side)

- Return `429 Too Many Requests` (RFC 6585) with `Retry-After` (RFC 9110).
- Advertise quota with the IETF RateLimit header fields draft (`RateLimit-Policy`, `RateLimit`)
  or the project's existing convention — don't mix conventions.
- Limit per identity (API key, tenant, user) and protect expensive endpoints separately.
- Distinguish rate limiting (fairness per client) from load shedding (protecting the service as a
  whole — Google SRE "Handling Overload"); shed with 503 + `Retry-After`.

## 7. Timeouts and deadlines at the handler

- Server request timeout < gateway/load-balancer timeout < client timeout — otherwise work
  continues after the caller has already given up.
- Propagate the remaining deadline to downstream calls (gRPC deadlines, or a header/context value);
  stop work when the caller cancels.
- Long operations: return `202 Accepted` with a status resource instead of holding a request open.

## 8. Authentication at the handler (brief)

- Validate tokens fully (signature, issuer, audience, expiry) at the edge; authorise per resource
  (object-level checks, OWASP API Security Top 10 "Broken Object Level Authorization").
- Service-to-service: OAuth 2.0 client credentials or mTLS; never long-lived shared secrets in code.
- Deeper threat modelling → `sse-security`.
