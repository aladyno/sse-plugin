---
description: Senior 5-axis code review of a diff, branch or PR with verdict and prioritized findings
argument-hint: "[branch | PR number/URL | commit range] (default: current changes vs base branch)"
---

# Review

Target: $ARGUMENTS

1. Resolve the diff:
   - empty → uncommitted changes plus commits on the current branch vs its base (`git merge-base HEAD origin/HEAD`, fallback `main`/`master`)
   - PR number/URL → `gh pr diff <n>` and `gh pr view <n>` (if `gh` is available)
   - branch / range → `git diff <base>...<target>`
2. If the diff is large (> ~1500 lines or > 30 files), split by module and review the parts in parallel with several `ag-sse-code-reviewer` agents, then merge and de-duplicate findings.
3. Otherwise delegate to one `ag-sse-code-reviewer` agent with the diff and the intent (PR description / commit messages).
4. Present: verdict → findings table (most severe first) → strengths → questions.

Read-only: never post comments to the PR unless the user explicitly asks and confirms the exact text.
