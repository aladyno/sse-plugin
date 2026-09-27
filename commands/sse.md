---
description: SSE orchestrator — route a software task through the right SDLC phase(s) and specialist agents
argument-hint: "<task, ticket or question>"
---

# SSE — Senior Software Engineer

Task: $ARGUMENTS

If the task is empty, ask the user what they want to achieve and stop.

1. **Classify** the task into one or more SDLC phases:

   | Phase | Signals | Agent |
   |---|---|---|
   | Design | new feature, "how should we", trade-off, schema/API design | `ag-sse-architect` |
   | Code | implement, fix, refactor | `ag-sse-implementer` |
   | Test | test cases, coverage, flaky | `ag-sse-test-engineer` |
   | Review | diff, PR, "check my code" | `ag-sse-code-reviewer` |
   | Deploy | CI/CD, Docker, infra, release | `ag-sse-devops-engineer` |
   | Operate | SLO, alerts, dashboards, incident, outage | `ag-sse-sre` |
   | Maintain | tech debt, upgrade, legacy, cleanup | `ag-sse-maintainer` |

2. **Plan** — state the phases in order and why, in 3–5 lines. For a full feature the default chain is Design → Code → Test → Review → Deploy → Operate. Skip phases that add no value for this task.
3. **Gate** — if a phase produces a decision the user must own (design choice, release, destructive change), stop after that phase and ask before continuing.
4. **Execute** each phase by delegating to its agent with the previous phase's output as context. Run independent phases in parallel (e.g. Test + Review of the same diff).
5. **Synthesize**: summary → key decisions → changes made → risks / open questions → next command to run (e.g. `/sse-plugin:ship`).

Respond in the user's language.
