# CI/CD pipeline guide

Read on demand. Tool-agnostic: applies to any CI system. Cite standards by name; verify against
the project's actual pipeline files before recommending changes.

## 1. Principles (Continuous Delivery, Humble & Farley)

- **The pipeline is the only path to production.** No manual builds, no laptop deploys.
- **Build once, promote the same artifact.** Environments differ only by configuration
  (Twelve-Factor "config"). Rebuilding per environment means prod runs untested bits.
- **Everything in version control**: code, pipeline definition, infrastructure, config templates,
  migration scripts.
- **Fast feedback first**: cheapest, most likely-to-fail checks run earliest.
- **Stop the line**: a red mainline is the team's top priority.
- **Trunk-based development** with short-lived branches correlates with better DORA outcomes;
  long-lived branches defer integration risk.

## 2. Reference stage order

| Stage | Gate / purpose | Typical budget |
|---|---|---|
| Lint, format, static analysis | Fail fast on trivial issues | < 2 min |
| Build + unit tests | Correctness of units; produce artifact once | < 10 min |
| Security scans | Dependencies (SCA), secrets, SAST, container image, IaC misconfig | parallel |
| Package + sign + SBOM + provenance | Immutable, identifiable artifact | — |
| Integration / contract tests | Boundaries with DB, queues, other services | — |
| Deploy to lower env + smoke tests | The deploy procedure itself is tested | — |
| Gated production deploy | Progressive rollout with automated health checks | — |
| Post-deploy verification | SLIs vs baseline; auto-rollback on threshold | first 15–60 min |

Keep the commit-stage feedback loop under ~10 minutes; move slow suites to later stages or run
them in parallel.

## 3. Artifacts and versioning

- Reference images by **immutable digest**, not mutable tags (`latest`, `stable`).
- Tag with version + commit SHA; record which commit, pipeline run and inputs produced it.
- Keep artifacts for the rollback window: rolling back means redeploying the previous artifact,
  not rebuilding an old commit.
- Reproducible/hermetic builds (Google SRE, release engineering): pinned toolchains and
  dependencies (lockfiles), no network fetches of unpinned inputs during build.

## 4. Supply-chain security

- **SLSA**: progressively harden the build — scripted build, hosted build platform, signed
  provenance, isolated builds. Verify provenance at deploy/admission time.
- **SBOM** (SPDX or CycloneDX) generated per artifact and stored with it; used for vulnerability
  and license response.
- **NIST SSDF (SP 800-218)** practice groups — prepare the organisation, protect the software,
  produce well-secured software, respond to vulnerabilities — are a useful map for gap analysis
  of pipeline controls.
- **OpenSSF Scorecard** checks worth enforcing: branch protection, code review, pinned
  dependencies (including CI actions pinned to a full commit SHA), token permissions set to
  least privilege, no dangerous workflow triggers running untrusted code with secrets.
- Artifact signing and verification (e.g. Sigstore-style keyless signing) where the platform supports it.
- Dependency update automation with review; never auto-merge major versions into production paths blindly.

## 5. Credentials in pipelines

- Prefer **short-lived, federated credentials** (OIDC from the CI provider to the cloud) over
  long-lived static keys stored as secrets.
- Scope per environment: the job that deploys to staging cannot touch production.
- Secrets are masked in logs, never echoed, never baked into images or artifacts.
- Pull-request pipelines from forks must not receive deploy credentials.

## 6. Gates and approvals

- Automate evidence-based gates (tests, scans, policy-as-code, SLO/error-budget status) instead of
  manual sign-offs that rubber-stamp.
- ITIL 4 change enablement: classify **standard** (pre-approved, low risk, automated),
  **normal** (assessed), **emergency** (expedited, reviewed after). Most pipeline deploys should
  qualify as standard changes.
- Google SRE error budgets: when the budget is exhausted, freeze risky releases and prioritise
  reliability work — an explicit, pre-agreed policy.
- Separation of duties can be satisfied by mandatory code review + protected pipelines rather
  than a human pressing "deploy".

## 7. Database migrations in the pipeline

- Migrations run as a distinct, observable step — not implicitly at app startup across many
  replicas at once (race, partial application, startup timeouts).
- Expand–contract: the migration shipped with release N must be compatible with release N-1 code;
  destructive steps ship in a later release.
- Long-running backfills run as throttled, resumable jobs, not inside the deploy step.

## 8. Measuring delivery (DORA four keys)

| Metric | Measures | Source of truth |
|---|---|---|
| Deployment frequency | Throughput | Deploy events per service |
| Lead time for changes | Throughput | Commit time → running in prod |
| Change failure rate | Stability | Deploys causing incident/rollback/hotfix |
| Time to restore service | Stability | Incident start → recovery |

Use them to find bottlenecks, not to rank teams. Instrument deploy events so the numbers are
derived automatically.

## 9. Common anti-patterns

- Different build commands per environment; "hotfix" builds done outside the pipeline.
- Flaky tests retried until green — hides real regressions; quarantine and fix instead.
- Security scans that only warn, forever.
- Pipeline logic duplicated across repos with no shared, versioned templates.
- Deploy step with no post-deploy verification — success means "the command exited 0".
- CI runners with broad cloud-admin permissions shared across all projects.
