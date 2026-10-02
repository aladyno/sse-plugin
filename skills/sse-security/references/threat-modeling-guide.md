# Threat Modeling Guide

A lightweight, repeatable approach to finding and prioritising threats in a design or change.
Grounded in the Threat Modeling Manifesto's four questions, Microsoft's STRIDE-per-element method,
LINDDUN (privacy), PASTA (risk-centric), CVSS v4.0 / EPSS, and the OWASP Threat Modeling Cheat
Sheet.

---

## 1. The four questions

1. **What are we working on?** Scope, assets, data flows, trust boundaries.
2. **What can go wrong?** STRIDE per element (or LINDDUN for privacy, attack trees for one goal).
3. **What are we going to do about it?** Mitigate, eliminate, transfer or accept — each with an owner.
4. **Did we do a good enough job?** Every element covered; mitigations testable; residual risk
   explicitly accepted by someone with authority.

Scale depth to risk: a small change needs the four questions in ten minutes; a new
payment or health-data flow deserves a full DFD and a written model.

---

## 2. Process

1. **Scope** — system boundary, assets and their classification, actors and trust levels,
   assumptions (write them down; wrong assumptions are the top source of missed threats).
2. **Data-flow diagram** — external entities, processes, data stores, data flows, trust
   boundaries. Level 0 for context; Level 1 for most reviews; Level 2 only where risk concentrates.
3. **Enumerate threats** — STRIDE per element (§3), plus the blind spots in the SKILL.md checklist.
4. **Prioritise** — §6.
5. **Mitigate** — map each threat to a control (and a detection); note gaps.
6. **Validate** — turn mitigations into tests or review checks; revisit when the design changes.

### Threat record (keep it this small)

| ID | Element / flow | STRIDE | Threat (attacker, precondition, action, impact) | Priority | Mitigation + detection | Owner / status |
|---|---|---|---|---|---|---|

---

## 3. STRIDE

| Category | Violated property | Typical mitigations |
|---|---|---|
| **S**poofing | Authentication | Strong authN, MFA, mutual TLS, signed webhooks, workload identity |
| **T**ampering | Integrity | Server-side validation, signatures/MACs, AEAD, immutable audit trail, integrity of builds |
| **R**epudiation | Non-repudiation | Tamper-evident audit logs with actor, action, target, time; signed records where disputes matter |
| **I**nformation disclosure | Confidentiality | Least privilege, encryption, masking, minimisation, generic errors |
| **D**enial of service | Availability | Rate limits/quotas, timeouts, bounded queues and payloads, autoscaling with cost caps |
| **E**levation of privilege | Authorization | Deny-by-default, object/function-level checks, least-privilege identities, sandboxing |

### STRIDE per element

| DFD element | Applicable threats |
|---|---|
| External entity | S, R |
| Process | S, T, R, I, D, E |
| Data store | T, I, D (R when the store is an audit log) |
| Data flow | T, I, D |

### Worked example (compressed): authentication service

| STRIDE | Threat | Mitigation |
|---|---|---|
| S | Credential stuffing with breached passwords | Breached-password screening, rate limiting, phishing-resistant MFA |
| T | Token claims altered by client | Signed tokens, algorithm pinned, claims validated server-side |
| R | User disputes a privileged action | Audit log with actor, session, source, timestamp |
| I | Password hashes exposed via injection or backup | Parameterised queries, Argon2id, encrypted and access-controlled backups |
| D | Login endpoint exhausted by slow hashing | Per-IP and per-account throttling; hashing cost tuned to capacity |
| E | Regular user reaches admin function | Function-level authZ checked server-side on every admin route |

---

## 4. Beyond STRIDE

- **LINDDUN** (privacy): Linking, Identifying, Non-repudiation (as a privacy harm), Detecting,
  Data disclosure, Unawareness, Non-compliance. Use when personal data is the main asset.
- **PASTA**: seven-stage, business-impact-driven process; use for high-value systems where risk
  must be tied to business objectives.
- **Attack trees**: root = attacker goal, children = ways to achieve it (OR = any path, AND = all
  steps needed). Use to find the **cheapest path** to a critical asset and to check that each
  path has at least one control. Estimated probabilities are rough — compare paths relatively,
  do not treat the numbers as precise.

---

## 5. Data-flow diagrams and trust boundaries

| Element | Security focus |
|---|---|
| External entity | Who is it, how is it authenticated, what can it send? |
| Process | Input validation, authZ decisions, secrets it holds |
| Data store | Classification, encryption, access list, backups |
| Data flow | Encryption in transit, integrity, what data rides on it |
| Trust boundary | Authentication, authorisation, validation must happen here |

Trust-boundary table (fill one row per crossing):

| Crossing | Authentication | Authorisation | Transport protection | Validation |
|---|---|---|---|---|
| e.g. browser → API | session or OIDC token | per-object check | TLS 1.2+ | schema validation |
| e.g. service → service | mTLS / workload token | scoped service role | TLS | contract validation |
| e.g. app → third-party API | API key or OAuth client credentials (from secret manager) | least-privilege scope | TLS | response validated and size-bounded |
| e.g. untrusted content → LLM | n/a | tools run with user's rights | — | treated as data, not instructions |

---

## 6. Prioritisation

Prefer transparent, evidence-based scoring over subjective composites.

- **Vulnerabilities in code or dependencies**: CVSS v4.0 for severity, **EPSS** for probability of
  exploitation, **CISA KEV** for known exploitation — then adjust for reachability and exposure in
  *this* system. A reachable, internet-facing, KEV-listed issue beats a higher CVSS score behind
  three controls.
- **Design threats**: simple likelihood × impact (e.g. 3×3 or 5×5) with a one-line justification
  per score, or the OWASP Risk Rating Methodology when finer factors help.
- **DREAD** is legacy (subjective and inconsistent between raters; Microsoft moved away from it) —
  use only if the organisation already standardises on it.

Impact anchors: data classification affected, number of users/tenants, financial or regulatory
exposure (e.g. breach notification duties), reversibility.

---

## 7. Common attack patterns ↔ STRIDE

OWASP Top 10 (2021) mapping (a newer edition may exist — check the current list; the mapping
logic does not change):

| ID | Category | STRIDE | Typical example |
|---|---|---|---|
| A01 | Broken Access Control | E, I | IDOR/BOLA, missing function-level checks |
| A02 | Cryptographic Failures | I | Plaintext sensitive data, weak algorithms, exposed keys |
| A03 | Injection | T, E, I | SQL/NoSQL/OS command injection, XSS |
| A04 | Insecure Design | All | Missing business-logic limits, trust in client state |
| A05 | Security Misconfiguration | I, E | Default credentials, verbose errors, open storage, XXE |
| A06 | Vulnerable and Outdated Components | All | Known-vulnerable dependencies |
| A07 | Identification and Authentication Failures | S | Credential stuffing, weak session handling |
| A08 | Software and Data Integrity Failures | T | Unsigned updates, CI/CD compromise, unsafe deserialisation |
| A09 | Security Logging and Monitoring Failures | R | Missing audit trail, no alerting |
| A10 | Server-Side Request Forgery | I, E | Reaching metadata services or internal APIs |

For each pattern, record **detection** as well as prevention: which log, metric or alert would
show the attack in progress. Validation of mitigations belongs in tests (`/sse-plugin:test`) and
authorised security testing — this guide does not include exploit payloads.

---

## 8. Threat-intelligence inputs

| Source | Use |
|---|---|
| CVE / NVD, supplier security advisories, GitHub advisories | Known vulnerabilities in dependencies |
| CISA KEV, EPSS | Exploitation evidence and likelihood |
| MITRE ATT&CK / ATLAS | Realistic adversary techniques and detection ideas |
| CWE Top 25 | Root-cause weakness classes to eliminate |
| Sector ISACs | Industry-specific campaigns |
