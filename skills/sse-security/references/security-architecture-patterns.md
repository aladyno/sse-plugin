# Security Architecture Patterns

Stack-agnostic patterns and anti-patterns for designing and reviewing secure systems. Grounded in
NIST SP 800-207 (Zero Trust), NIST SP 800-63B (authenticators), RFC 9700 (OAuth 2.0 Security BCP),
RFC 8725 (JWT BCP), OWASP ASVS, OWASP API Security Top 10 (2023) and the OWASP Cheat Sheet Series.

---

## 1. Zero Trust (NIST SP 800-207)

No implicit trust from network location. Every request to a resource is authenticated,
authorised and evaluated per session, using identity, device/workload posture and context.

| Principle | What it looks like in a system |
|---|---|
| Verify explicitly | Service-to-service authentication (mTLS or signed workload tokens), not "it came from the VPC" |
| Least privilege | Per-resource authorisation; just-in-time elevation for admins; narrow IAM roles per workload |
| Assume breach | Segmentation, encryption in transit inside the perimeter, detection on lateral movement |

Components: **policy decision point (PDP)** evaluates policy (identity provider, policy engine,
context signals); **policy enforcement point (PEP)** sits in the data path (gateway, sidecar,
middleware) and enforces the decision. Review question: *is there any path to the resource that
bypasses the PEP?*

| Segment | Typical controls |
|---|---|
| Edge / public | WAF, DDoS protection, rate limiting, TLS termination |
| Application | Authenticated workload identity, mTLS or service mesh, per-route authZ |
| Data | Network isolation, DB-level least-privilege accounts, encryption, audit logging |
| Management | Privileged access management, phishing-resistant MFA, session recording, break-glass procedure |

---

## 2. Defence in depth

Independent layers so that one failure does not become a breach:
edge → network → host/workload → application → data → detection & response.

| Layer | High-value controls |
|---|---|
| Edge | Rate limiting, WAF (as a supplement, never the only injection control) |
| Network | Segmentation, egress restrictions (blocks SSRF and exfiltration paths) |
| Workload | Patching cadence, minimal base images, non-root, read-only filesystems |
| Application | Server-side authZ, parameterised queries, output encoding, input validation |
| Data | Encryption at rest with managed keys, TLS 1.2+ (prefer 1.3) in transit, backups with versioning and deletion protection |
| Detection | Centralised, tamper-resistant audit logs; alerts on authZ failures, privilege changes, mass reads/exports |

**Secure defaults** (browser-facing apps): cookies `Secure`, `HttpOnly`, `SameSite`; a Content
Security Policy (use `frame-ancestors` for clickjacking); `X-Content-Type-Options: nosniff`;
HSTS; restrictive CORS (no reflected origins with credentials); generic error responses with a
correlation ID.

---

## 3. Authentication

**Passwords and MFA (NIST SP 800-63B).**
- Minimum length (and long passphrases allowed), no composition rules, no forced periodic change,
  screening against breached/common-password lists, no knowledge-based "security questions".
- Throttle and monitor failed attempts; prefer rate limiting plus anomaly detection over hard
  lockout (lockout is itself a DoS vector).
- MFA strength: **phishing-resistant** authenticators (WebAuthn/passkeys, FIDO2 security keys,
  PKI smart cards) > app-based TOTP / push with number matching > SMS/voice OTP (restricted —
  SIM swap and interception). Biometrics are only an unlock for a possession factor, never a
  standalone factor.
- Account recovery is an authentication path: it must be at least as strong as login.

**OAuth 2.0 / OIDC (RFC 9700).**
- Authorization code flow with **PKCE for every client**, including confidential ones.
- No implicit grant, no resource-owner password grant.
- Exact redirect-URI matching; `state`/nonce checked.
- Refresh tokens for public clients: rotation with reuse detection, or sender-constrained
  (DPoP or mTLS-bound).
- Access tokens short-lived and audience-restricted.
- Browser SPAs: consider a backend-for-frontend so tokens never reach JavaScript.

**JWT (RFC 8725).** Pin the algorithm server-side (reject `none` and algorithm switching);
validate `iss`, `aud`, `exp`, `nbf`; distinguish token types; publish keys via JWKS with `kid`
for rotation; keep revocation-sensitive state (refresh tokens, sessions) server-side.

**Service-to-service.** Workload identity (mTLS certificates, cloud workload identity, signed
short-lived tokens) over static shared API keys. Webhooks: verify an HMAC or signature over the
body plus timestamp, reject stale timestamps, dedupe on event ID.

---

## 4. Authorization

- Enforce **server-side, on every request, per object** — OWASP API1:2023 Broken Object Level
  Authorization (BOLA) is the most common API flaw.
- Check **function-level** authorisation for admin and internal operations (API5:2023 BFLA).
- Check **property-level** access: no mass assignment of fields like `role`, `price`, `ownerId`;
  no over-broad response objects (API3:2023).
- Deny by default; centralise policy (middleware or policy engine) but verify it is actually
  applied on every route, job and consumer.
- Multi-tenant: tenant ID from the authenticated identity, never from the request body; tenant
  dimension in every query, cache key, search index and storage path.
- Choose the model deliberately: RBAC for coarse roles, ABAC/ReBAC for ownership and sharing.

---

## 5. API security

| Concern | Pattern |
|---|---|
| Input validation | Schema-based allow-list validation at the boundary (type, length, range, format); reject unknown fields where feasible |
| Injection | Parameterised queries / prepared statements everywhere; never build query, command or template strings from input; ORMs are safe only when their raw-string escape hatches are not used with input |
| Resource consumption (API4:2023) | Rate limits and quotas per identity and per tenant; pagination caps; max payload size; timeouts; cost-weighted limits for expensive operations |
| SSRF (API7:2023) | Allow-list outbound destinations; resolve and block internal/metadata address ranges; no redirects followed blindly; egress controls at network level |
| Unsafe consumption of third-party APIs (API10:2023) | Treat partner responses as untrusted input; validate, bound size, time out |
| Parsers | Disable XML external entities/DTDs; avoid native deserialisation of untrusted data; bound archive extraction |
| Errors | Generic message plus correlation ID to the client; detail only in protected logs |
| Inventory (API9:2023) | Know every exposed version and environment; retire old versions |

---

## 6. Data protection

- **Minimise first**: do not collect, store or log what you do not need; set retention limits.
- **Tokenise** highly sensitive values (e.g. payment card numbers) so most of the system never
  sees them — this also shrinks PCI DSS scope.
- **Field-level encryption** for high-value fields with keys from a KMS (envelope encryption),
  not keys derived from a configured password. See
  [cryptography-implementation.md](cryptography-implementation.md).
- **Masking** in logs, UIs and support tools; structured logging with deny-listed fields is a
  safety net, not a primary control.
- **Backups and exports** inherit the classification of their source data.
- **Deletion**: know every copy (replicas, caches, search indexes, analytics, backups) to honour
  retention and erasure obligations (e.g. GDPR).

### Secret management

| Option | When | Watch-outs |
|---|---|---|
| Secret manager / vault (cloud secret store, HashiCorp Vault) | Default for application secrets | Access policy per workload; audit log; rotation |
| Dynamic / short-lived credentials | Databases, cloud APIs | Preferred over static credentials — leaks expire |
| Workload identity (no secret at all) | Cloud-native service-to-service | Best option where available |
| Environment variables | Delivery mechanism only | Visible to process dumps, child processes, crash reports; never commit `.env` files |
| KMS / HSM | Cryptographic keys | Keys never exported; separate use and admin permissions |

Secret hygiene: secret scanning in pre-commit and CI; rotate immediately on exposure (removing a
commit does not un-leak it); never print secrets in CI logs.

---

## 7. Supply chain (NIST SSDF SP 800-218, SLSA)

- Lockfiles and pinned versions; pin CI actions and base images by digest.
- Generate an SBOM (SPDX or CycloneDX) per build; monitor it against vulnerability feeds.
- Prioritise findings by exploitability and reachability (EPSS, CISA KEV), not CVSS alone.
- Least-privilege CI tokens; untrusted pull-request code never runs with secrets.
- Build provenance and artifact signing; verify signatures at deploy time.

---

## 8. Anti-patterns

| Anti-pattern | Why it is wrong | Correct approach |
|---|---|---|
| Trusting client-supplied identity or role (headers, hidden fields, JWT claims not verified) | Trivially forged | Derive identity and role server-side from a verified credential |
| "Internal network = trusted" | One compromised workload reaches everything | Zero Trust: authenticate and authorise service calls |
| Security through obscurity (hidden admin URLs, custom crypto, Base64 "encryption") | Discoverable or reversible | Real authentication/authorisation; vetted crypto |
| Hard-coded or committed secrets | Leak with every clone, image and log | Secret manager, workload identity, secret scanning |
| Verbose errors and stack traces to clients | Reveal internals and data | Generic errors plus correlation ID |
| WAF as the only injection defence | Bypassable | Parameterisation and encoding in code |
| Password composition rules and forced rotation | Push users to predictable patterns (NIST SP 800-63B) | Length, breach screening, MFA |
| Logging full request/response payloads | Logs become the largest unprotected copy of sensitive data | Log metadata; mask or omit sensitive fields |
| One broad service account for everything | Maximises blast radius | Per-workload identities, least privilege |

---

## 9. Tool categories (for hand-off to verification)

| Category | Purpose |
|---|---|
| SAST | Static code analysis for injection, crypto misuse, dangerous APIs |
| DAST | Running-application testing |
| SCA / dependency scanning | Known-vulnerable dependencies, licence issues |
| Secret scanning | Credentials in repos, images, CI logs |
| Container / IaC scanning | Image vulnerabilities; misconfigured infrastructure-as-code |
| CSPM | Cloud configuration drift |

Choose tools that the project already uses; this entity names the category and the gap, it does
not run them.
