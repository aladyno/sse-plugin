# sse-plugin

Senior Software Engineer plugin for Claude Code — end-to-end software development covering design, coding, testing, review, DevOps/deployment, operations & monitoring, and maintenance. Language- and stack-agnostic: every agent reads your project's existing conventions before acting.

## Features
- ✅ One orchestrator command (`/sse-plugin:sse`) that routes a task through the right SDLC phases
- ✅ 8 phase commands, each backed by a dedicated senior specialist subagent
- ✅ `sse-playbook` skill: Definition-of-Done checklists per phase
- ✅ Safety hook that asks the user to confirm irreversible shell commands (force-push, `reset --hard`, `DROP TABLE`, `terraform destroy`, …) before they run

## Installation
```bash
# from GitHub (this repo is both the plugin and its marketplace)
/plugin marketplace add aladyno/sse-plugin
/plugin install sse-plugin@aladyno-sse

# local development
claude --plugin-dir <path-to-this-repo>   # then /reload-plugins after edits
```

## What's Included

### Commands
| Command | Phase | Purpose |
|---|---|---|
| `/sse-plugin:sse <task>` | All | Classify the task, plan the phases, delegate, synthesize |
| `/sse-plugin:design <req>` | Design | Options, trade-offs, ADR, data model, API contracts, diagrams |
| `/sse-plugin:implement <task>` | Code | Small, test-verified increments following project conventions |
| `/sse-plugin:test [target]` | Test | Test strategy, case table, write and run tests |
| `/sse-plugin:review [branch\|PR]` | Review | 5-axis review with verdict and evidence-backed findings |
| `/sse-plugin:ship [release]` | Deploy | CI/CD, deploy config, readiness checklist, rollout + rollback plan |
| `/sse-plugin:observe <service>` | Operate | SLIs/SLOs, metrics/logs/traces, alerts, dashboards, runbooks |
| `/sse-plugin:incident <symptom>` | Operate | Mitigate-first triage, root cause, blameless postmortem |
| `/sse-plugin:maintain [scope]` | Maintain | Tech-debt register, dependency upgrades, safe refactor plan |

### Subagents
| Agent | Role | Writes files? |
|---|---|---|
| `ag-sse-architect` | Design & ADRs | No |
| `ag-sse-implementer` | Coding | Yes |
| `ag-sse-test-engineer` | Testing | Yes (tests) |
| `ag-sse-code-reviewer` | Code review | No |
| `ag-sse-devops-engineer` | CI/CD, containers, IaC, release plans | Yes (never deploys) |
| `ag-sse-sre` | Observability & incidents | Docs only (never mutates prod) |
| `ag-sse-maintainer` | Tech debt & upgrades | No |

### Skills
- `sse-playbook` — Definition-of-Done checklists for every phase.
- `sse-<role>` — expert-entity skills (slash-only): each joins work in progress and contributes one
  senior lens, grounded in international standards. Shared rules: [`shared/expert-entity-contract.md`](shared/expert-entity-contract.md).
  - advisory (analysis in words): `sse-architect`, `sse-backend`, `sse-database`, `sse-devops`,
    `sse-integration`, `sse-maintainer`, `sse-performance`, `sse-security`, `sse-pm`, `sse-cto`, `sse-ceo`,
    `sse-strategic-alignment`, `sse-jira`
  - hybrid (also writes requirement / test / design-spec documents): `sse-ba`, `sse-qc`,
    `sse-brainstorming` (idea → approved design; optional local browser "visual companion")
  - Not to be confused with the `ag-sse-*` subagents above, which drive the phase commands.

### Hooks
- `PreToolUse` (`Bash|PowerShell`) → `scripts/guard-destructive.js`: flags destructive commands and returns a permission `ask`, so Claude Code asks the user to confirm that command (nothing is hard-blocked).

## Usage
```
/sse-plugin:sse add rate limiting to the public API
/sse-plugin:design multi-tenant export of invoices to S3
/sse-plugin:review 142
/sse-plugin:ship v1.4.0 to production
/sse-plugin:incident p99 latency on /checkout jumped to 4s after 10:05 deploy
```

## Requirements
- Claude Code 2.1.x or later (tested on 2.1.283)
- Node.js ≥ 18 on `PATH` (for the safety hook and the `sse-brainstorming` visual companion server)
- Optional: bash for the companion's launcher scripts (built in on macOS/Linux; Git Bash on Windows —
  without it, the companion guide documents a PowerShell + `node` recipe)
- Optional: `gh` CLI for reviewing GitHub PRs by number
- Optional: Python ≥ 3.8 (standard library only) for the helper scripts in `sse-jira`, `sse-pm`, `sse-qc`

## Configuration
| Variable | Purpose |
|---|---|
| `SSE_GUARD=off` | Disable the destructive-command guard (no confirmation prompts) for the session |

No credentials are required or stored by this plugin.

## Validate
```bash
claude plugin validate .
node scripts/guard-destructive.test.js   # safety-hook tests (plain Node, no deps)
```

## License
MIT
