# Infrastructure as code, config and secrets

Read on demand. Tool-agnostic: Terraform/OpenTofu, Pulumi, CloudFormation/CDK, Bicep, Ansible,
Helm/Kustomize. Verify against the project's actual IaC layout before recommending changes.

## 1. Principles

- **Declarative, versioned, reviewed.** Every infrastructure change goes through version control
  and review, like application code.
- **OpenGitOps principles (CNCF)**: desired state is *declarative*, *versioned and immutable*,
  *pulled automatically* by an agent, and *continuously reconciled*. Drift is detected and corrected,
  not tolerated.
- **Immutable infrastructure**: replace rather than mutate servers/images; configuration changes
  produce new versions.
- **Operations as code** (Well-Architected operational excellence): runbooks, alerts and
  dashboards are defined as code too.
- **Small, frequent, reversible changes** — same as application delivery.

## 2. State and structure

- Remote state with locking, encryption at rest and restricted access; state often contains secrets.
- Split state by blast radius and change frequency (network/foundation vs per-service vs
  per-environment). One giant state = every plan risks everything.
- Reusable, versioned modules; pin module and provider versions; upgrade deliberately.
- Environments as parameterised instances of the same code, not copy-pasted directories that drift.

## 3. Plan review — the change-risk moment

For every plan/preview, check:

- **Replacements and deletions** — a renamed resource or changed immutable attribute can mean
  destroy-and-recreate (databases, volumes, load balancers, DNS). Look for replace markers explicitly.
- **Blast radius** — how many resources, which environments, shared components (networking, IAM,
  DNS, shared databases).
- **Ordering and dependencies** — will the app lose access mid-apply (IAM, security groups, routes)?
- **Data-bearing resources** protected with deletion protection / prevent-destroy lifecycle rules.
- The plan that was reviewed is the plan that is applied (saved plan artifact), with no
  unreviewed changes in between.
- Policy as code (e.g. OPA-style policies) enforces guardrails automatically: no public buckets,
  encryption on, tags present, allowed regions/instance types.

## 4. Drift

- Detect drift on a schedule; alert on it.
- Console "hot-fixes" during incidents are allowed only if reconciled back into code immediately
  afterwards — otherwise the next apply silently reverts the fix.
- Import manually created resources rather than leaving them unmanaged.

## 5. Configuration (Twelve-Factor)

- Config that varies per deploy lives in the environment (env vars, config service, mounted
  files), not in the artifact.
- Validate config at startup and fail fast with a clear message; don't discover a missing key on
  the first request that needs it.
- Every new key: default or explicit value in **every** environment and region; checked by CI
  (schema or diff across environment configs).
- Config changes are deploys: versioned, reviewed, rolled out progressively where possible, with
  a rollback path.
- Keep dev/staging/prod parity in shape (same keys, same topology type), differing in size and values.

## 6. Secrets

- Stored in a dedicated secret manager or encrypted-at-rest mechanism; never in source, images,
  IaC variables files committed to git, or CI logs.
- Injected at runtime with least-privilege identity (workload identity / instance roles / OIDC
  federation) rather than long-lived static keys.
- Rotation is automated and tested; applications reload or tolerate rotation without restart storms.
- Access is audited; break-glass access is time-bound and logged.
- Secret scanning runs in CI and on the repository history.

## 7. Hardening (CIS Benchmarks — Docker, Kubernetes)

Containers and images:
- Minimal, pinned base images (by digest); rebuilt regularly for patches.
- Run as non-root; read-only root filesystem where possible; drop Linux capabilities.
- No secrets in image layers; `.dockerignore` excludes local config and credentials.
- A `HEALTHCHECK` or platform probe defined; resource limits set.

Kubernetes:
- No privileged pods, no host namespaces/mounts unless justified; Pod Security Standards enforced.
- RBAC least privilege; service accounts per workload; automount of tokens disabled where unused.
- NetworkPolicies default-deny with explicit allows.
- Requests/limits set; PodDisruptionBudgets for availability during node maintenance.
- Images restricted to trusted registries; admission verifies signatures/provenance where supported (SLSA).

VMs:
- Hardened images built by pipeline; no SSH-and-edit configuration; patching automated.

## 8. Reliability of the infrastructure itself (Well-Architected)

- Spread across failure domains (zones/regions) in proportion to the availability target.
- Autoscaling bounded by downstream limits (database connections, third-party rate limits, quotas).
- Quotas and limits tracked as code; a scale-out that hits an account quota is a predictable outage.
- Backups and disaster recovery for stateful resources defined in code and restore-tested.

## 9. Common anti-patterns

- `apply` from a laptop with personal admin credentials.
- Auto-apply to production without a reviewed plan for destructive changes.
- One state file for the whole company.
- Unpinned providers/modules — an upstream release changes production behaviour.
- Secrets passed as plain IaC variables and printed in plan output.
- Environments that differ structurally ("prod has a cache, staging doesn't") — failures only in prod.
