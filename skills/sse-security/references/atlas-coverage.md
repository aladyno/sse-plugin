# AI/LLM Threat Coverage — MITRE ATLAS × OWASP LLM Top 10

Reference for reviewing systems that call LLMs, run agents with tools, use retrieval (RAG), or
train/fine-tune models. MITRE ATLAS (Adversarial Threat Landscape for Artificial-Intelligence
Systems) is the AI counterpart of MITRE ATT&CK; the OWASP Top 10 for LLM Applications (2025) is
the application-level risk list. Governance framing: NIST AI RMF (Govern / Map / Measure / Manage).

Source of truth: <https://atlas.mitre.org/> and <https://genai.owasp.org/>. ATLAS IDs and names
are revised over time — confirm the current ID before quoting it in a formal document.

---

## 1. Review order for an LLM feature (80/20)

1. **What untrusted content reaches the model?** User input, retrieved documents, web pages,
   emails, tool outputs, file uploads. All of it is **data, never instructions**.
2. **What can the model cause?** List every tool/action and its privilege. Anything that writes,
   deletes, pays, sends messages or changes access is high-risk.
3. **Whose authority does a tool call run under?** It must be the requesting user's permissions,
   not a broad service account.
4. **What leaves the boundary?** Secrets, PII or other tenants' data placed in context can be
   echoed back or sent to the provider.
5. **What is the cost ceiling?** Tokens, tool calls and loops per request/user/tenant.

---

## 2. Risk mapping

| OWASP LLM Top 10 (2025) | Related ATLAS technique(s) | Core controls | Detection |
|---|---|---|---|
| LLM01 Prompt Injection (direct and indirect) | AML.T0051 LLM Prompt Injection (direct / indirect sub-techniques); AML.T0054 LLM Jailbreak | Separate trusted instructions from untrusted content; treat retrieved/tool content as data; least-privilege tools; human confirmation for consequential actions; output validation | Injection-pattern and anomaly classifiers on input and retrieved content; alert on tool calls that deviate from the user's stated intent |
| LLM02 Sensitive Information Disclosure | AML.T0057 LLM Data Leakage; AML.T0024 Exfiltration via ML Inference API | Minimise and redact PII/secrets before they enter context; per-user/tenant retrieval authorisation; output PII filtering | Output scanning for PII/secret patterns; audit log of prompts and responses with access control |
| LLM03 Supply Chain | AML.T0010 ML Supply Chain Compromise; AML.T0019 Publish Poisoned Datasets | Pin and verify model/dataset provenance and checksums; prefer safe serialisation formats (avoid arbitrary-code formats such as pickle for untrusted models); SBOM/AI-BOM | Hash verification in CI; alert on unexpected model/artifact changes |
| LLM04 Data and Model Poisoning | AML.T0020 Poison Training Data; AML.T0018 Backdoor ML Model | Provenance tracking and review for training/fine-tuning data and RAG corpora; restrict who can write to the index | Behavioural regression tests after each training run or index update; monitor for trigger-like outputs |
| LLM05 Improper Output Handling | (maps to classic injection: XSS, SQLi, command injection via model output) | Treat model output as untrusted input to the next component: encode, parameterise, validate against schema | Standard web/app injection detection downstream |
| LLM06 Excessive Agency | AML.T0053 LLM Plugin Compromise; prompt-injection-driven tool abuse | Minimum tool set, minimum permissions, user-scoped credentials, allow-listed parameters, human-in-the-loop for irreversible actions | Tool-call audit log; alert on high-risk tools, unusual volume or new destinations |
| LLM07 System Prompt Leakage | AML.T0056 (LLM system/meta prompt extraction) | Never put secrets or authorisation logic in the system prompt; enforce rules outside the model | Output matching against system-prompt fragments |
| LLM08 Vector and Embedding Weaknesses | Poisoned retrieval content; cross-tenant retrieval | Per-tenant/per-user partitioning and authorisation at retrieval time; validate ingested content | Retrieval audit log; alert on cross-tenant hits |
| LLM09 Misinformation | — (reliability rather than adversary technique) | Grounding with citations, confidence signalling, human review for high-stakes output | Sampling-based quality review; user feedback loops |
| LLM10 Unbounded Consumption | AML.T0029 Denial of ML Service; AML.T0040 ML Model Inference API Access; AML.T0005 Create Proxy ML Model (model extraction via high-volume querying) | Rate and quota limits per identity; token/step caps on agents; max input size; timeouts | Cost and volume anomaly alerts; systematic-querying patterns |

Identity and access to AI services (stolen API keys, over-broad service accounts) map to
AML.T0012 Valid Accounts and are reviewed like any other credential (see
[security-architecture-patterns.md](security-architecture-patterns.md)).

---

## 3. Control notes

**Prompt injection cannot be fully filtered away.** Classifiers and delimiters reduce it; the
durable controls are architectural: least privilege on tools, user-scoped authority, confirmation
before consequential actions, and deterministic checks outside the model (authorisation,
allow-lists, schema validation).

**Agent design checklist.**
- Each tool: purpose, required permission, reversible or not, confirmation required or not.
- Credentials for tools are scoped to the end user and short-lived.
- Plans that chain read-sensitive → send-external (the "exfiltration triad": private data,
  untrusted content, external communication) require explicit human approval.
- Loops have step, time and cost ceilings.

**Model-level attacks** (membership inference, model inversion, model stealing) matter mainly when
you host your own model or expose scores/logits: avoid returning raw confidence scores, rate-limit
inference, consider differential privacy for sensitive training data.

**Logging.** Log prompts, retrieved sources, tool calls and outputs for investigation, but treat
those logs as sensitive data (access control, retention, redaction) — they concentrate PII.

---

## 4. Coverage gaps that need non-advisory work

| Area | Why words are not enough | Recommended assessment |
|---|---|---|
| Jailbreak / injection resilience | Behaviour is empirical | Red-team with a maintained prompt corpus; regression-test after model or prompt changes |
| Poisoning / backdoors | Needs data inspection | Dataset provenance audit; behavioural trigger testing |
| Model extraction | Needs traffic analysis | Inference API log analysis for systematic querying |
| Artifact integrity | Needs tooling | Checksum/signature verification in CI; artifact scanning |
