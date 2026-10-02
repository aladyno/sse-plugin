---
description: Release readiness — CI/CD, deploy config, release plan with rollout, verification and rollback
argument-hint: "[what is being released / target environment]"
---

# Ship

Release: $ARGUMENTS

1. Gather: changes since the last release tag (`git log <last-tag>..HEAD`), DB migrations, config/secret changes, CI config, deploy manifests.
2. Delegate to the `ag-sse-devops-engineer` agent to produce or fix pipeline/deploy files and a release plan.
3. Run the readiness checklist and mark each item ✅ / ⚠️ / ❌ with evidence:
   - build + tests green in CI · security scan clean · migrations backward-compatible · feature flags for risky paths
   - config/secrets present in target env · monitoring + alerts for new paths · rollback tested or documented · stakeholders informed
4. Output: readiness verdict (GO / GO WITH RISKS / NO-GO) · release plan · rollback plan.

Never deploy, tag or push yourself — give the user the exact commands to run after they approve.
