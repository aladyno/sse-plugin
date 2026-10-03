# sse-plugin

Senior Software Engineer plugin for Claude Code — end-to-end software development covering design, coding, testing, review, DevOps/deployment, operations & monitoring, and maintenance. Language- and stack-agnostic: every agent reads your project's existing conventions before acting.

## Features
- ✅ One orchestrator command (`/sse-plugin:sse`) that routes a task through the right SDLC phases
- ✅ 8 phase commands, each backed by a dedicated senior specialist subagent
- ✅ C-level executive suite: 12 advisor entities (`sse-cfo` … `sse-vpe`), matching `ag-sse-<role>` review agents with helper scripts, `/sse-plugin:boardroom` multi-role deliberation and `/sse-plugin:decide` decision log
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
| `/sse-plugin:exec <role> <plan>` | Executive | One C-level review: forcing questions, script-backed numbers, 🟢/🟡/🔴 verdict |
| `/sse-plugin:boardroom <decision>` | Executive | Panel of 2–5 roles, isolated positions, cross-examination, devil's advocate, board memo with dissent |
| `/sse-plugin:decide <memo\|decision>` | Executive | Record a decision the user took: chosen/rejected options, binding success & kill criteria, preserved dissent |

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
| `ag-sse-<role>` (`cfo`, `cro`, `cxo`, `cmo`, `cpo`, `coo`, `chro`, `ciso`, `gc`, `cdo`, `caio`, `vpe`) | Executive review behind `/exec` and `/boardroom`; runs the role's helper scripts | No |
| `ag-sse-chief-of-staff` | Picks the boardroom panel, synthesizes the board memo | No |

### Skills
- `sse-playbook` — Definition-of-Done checklists for every phase.
- `chat` — receiver-centric workplace communication (slash-only): `send` (copy-ready message: why → ask →
  impact/options → next step), `receive` (paraphrase-confirm, clarifying questions, ack line), `check`
  (8-check grade). Built for cross-border planner ↔ dev ↔ QA hand-offs; never invents facts.
- `sse-<role>` — expert-entity skills (slash-only): each joins work in progress and contributes one
  senior lens, grounded in international standards. Shared rules: [`shared/expert-entity-contract.md`](shared/expert-entity-contract.md).
  - advisory (analysis in words): `sse-architect`, `sse-backend`, `sse-database`, `sse-devops`,
    `sse-integration`, `sse-maintainer`, `sse-performance`, `sse-security`, `sse-pm`, `sse-cto`, `sse-ceo`,
    `sse-cso`, `sse-cco`, `sse-jira`
  - executive advisory (each has an `ag-sse-<role>` review agent + helper scripts): `sse-cfo`, `sse-cro`,
    `sse-cxo` (Chief Customer Officer), `sse-cmo`, `sse-cpo`, `sse-coo`, `sse-chro`, `sse-ciso`, `sse-gc`
    (General Counsel — issue-spotting, not legal advice), `sse-cdo`, `sse-caio`, `sse-vpe`
  - hybrid (also writes requirement / test / design-spec documents): `sse-ba`, `sse-qc`,
    `sse-brainstorming` (idea → approved design; optional local browser "visual companion")
  - Not to be confused with the `ag-sse-*` subagents above, which drive the phase commands.

### Shared knowledge
- [`shared/communication-standard.md`](shared/communication-standard.md) — Communication Standard: why before how,
  receiver's context per hand-off direction (planner ↔ dev ↔ QA), active receiving (paraphrase, say what's
  unclear, silence ≠ agreement), cross-border rules, an 8-check gate. Every command, subagent and entity
  follows its §6 when reporting or asking; the `chat` skill applies it to your own messages.
- [`shared/expert-entity-contract.md`](shared/expert-entity-contract.md) — rules shared by all `sse-<role>` entities.

### Hooks
- `PreToolUse` (`Bash|PowerShell`) → `scripts/guard-destructive.js`: flags destructive commands and returns a permission `ask`, so Claude Code asks the user to confirm that command (nothing is hard-blocked).

## Usage
```
/sse-plugin:sse add rate limiting to the public API
/sse-plugin:design multi-tenant export of invoices to S3
/sse-plugin:review 142
/sse-plugin:ship v1.4.0 to production
/sse-plugin:incident p99 latency on /checkout jumped to 4s after 10:05 deploy
/sse-plugin:exec cfo hire 6 engineers in Q1 on current runway
/sse-plugin:boardroom raise prices 20% for the SMB tier in 2027-Q1?
```

## Requirements
- Claude Code 2.1.x or later (tested on 2.1.283)
- Node.js ≥ 18 on `PATH` (for the safety hook and the `sse-brainstorming` visual companion server)
- Optional: bash for the companion's launcher scripts (built in on macOS/Linux; Git Bash on Windows —
  without it, the companion guide documents a PowerShell + `node` recipe)
- Optional: `gh` CLI for reviewing GitHub PRs by number
- Optional: Python ≥ 3.8 (standard library only) for the helper scripts in `sse-jira`, `sse-pm`, `sse-qc` and the executive entities (`sse-cco`, `sse-cfo` … `sse-vpe`; the CFO scripts need ≥ 3.9). Executive scripts are adapted from [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) (MIT)

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
