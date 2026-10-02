# Automation Rules — Design, Guardrails, Recipes

Read on demand when designing or reviewing tracker automation. Jira Automation terms are
primary. An automation rule is a **side effect attached to the state machine** — treat it
with the same care as code: named owner, tested, idempotent, reversible.

## Rule anatomy

```
TRIGGER (exactly one) → CONDITIONS (0..n, narrow first) → ACTIONS (1..n) [→ branches]
```

| Part | Common options (Jira) |
|---|---|
| Triggers | Issue created / transitioned / updated / commented / assigned / linked; field value changed; sprint started/completed; version released; scheduled (with or without JQL); incoming webhook; manual |
| Conditions | Issue fields condition; JQL condition; related issues condition; user condition; advanced compare (smart values); if/else block |
| Actions | Edit / transition / assign / comment / create / clone / link issue; log work; lookup issues (JQL); send email / Slack / Teams message; send web request |
| Branches | For current/related issues (parent, sub-tasks, linked, JQL results) |

## Guardrails (check every rule against these)

1. **Scope** — single-project rules by default; global/multi-project rules only with an owner
   and a reason. Global scope multiplies blast radius and execution usage.
2. **Actor** — know which identity the rule acts as ("Automation for Jira" or a named user).
   That identity needs exactly the permissions required — least privilege — and shows up in
   history and notifications.
3. **Loop prevention** — a rule that edits issues can trigger other rules (or itself). Leave
   "allow other rule actions to trigger this rule" off unless required; never have A→B→A.
4. **Idempotency** — running twice must not double-comment, double-create or double-notify.
   Guard with a condition on the state the action produces (label present, field set).
5. **Narrow before acting** — JQL/field conditions first; scheduled rules always with JQL
   that excludes already-processed issues.
6. **Execution limits & usage** — Jira Cloud meters automation executions per plan and
   throttles heavy rules; prefer event triggers over frequent schedules, batch lookups over
   per-issue branches.
7. **Transitions via workflow, not edits** — automation should use transitions (so
   validators, resolution and post-functions run), never set Status directly.
8. **Notifications** — every notify action has an audience that asked for it; alert fatigue
   kills trust in all automation.
9. **Test and observe** — build in a test project, run manually on sample issues, check the
   audit log; after enabling, watch the audit log for errors and unexpected volume.
10. **Documentation & lifecycle** — descriptive name, description with *why*, owner; disable
    and observe before deleting; export rules before large changes.
11. **Personal data** — rules that copy description/comments into emails, chat or web
    requests move personal data to other systems (GDPR purpose limitation and data
    minimisation) — send links, not content, where possible.

## Smart values (Jira) — the few you need

```
{{issue.key}} {{issue.summary}} {{issue.status.name}} {{issue.assignee.displayName}}
{{issue.priority.name}} {{issue.fixVersions.name}} {{issue.url}}
{{now}} {{now.plusBusinessDays(3)}} {{issue.created.diff(now).days}}
{{lookupIssues.size}} {{#lookupIssues}}{{key}} {{/lookupIssues}}
{{#if(equals(issue.priority.name, "Highest"))}}urgent{{/}}
```

Verify syntax against Atlassian's smart-value documentation for your edition before relying
on it — functions differ between Cloud and Data Center.

## Recipes (with the guardrail that matters)

**Sub-tasks done → move parent**
Trigger: issue transitioned to Done (sub-task) · Branch: parent · Condition: all sub-tasks in
Done category · Action: transition parent to In Review.
Guardrail: condition on parent's current status so re-runs do nothing.

**Aging-work nudge (flow, not nagging)**
Trigger: scheduled daily, JQL `statusCategory = "In Progress" AND status changed BEFORE -10d AND Flagged is EMPTY`
· Action: comment/mention assignee once, add label `aging`.
Guardrail: exclude issues already labelled `aging`; tie the threshold to the team's SLE.

**Auto-close resolved after N days**
Trigger: scheduled daily, JQL `status = Resolved AND updated <= -7d` · Action: transition
Close (resolution kept). Guardrail: service desks must tell the customer first.

**Sprint spillover tagging**
Trigger: sprint completed · Branch: JQL issues in that sprint not in Done category ·
Action: add label `carried-over`. Guardrail: one label, no comment spam; review in the retro.

**Balanced assignment**
Trigger: issue created (type = Bug, assignee empty) · Action: assign issue using the
built-in balanced-workload / round-robin method over a group.
Guardrail: exclude people on leave; triage often beats auto-assignment.

**Release notes on version release**
Trigger: version released · Action: lookup issues `fixVersion = {{version.name}} AND statusCategory = Done`
→ send email / create page with the list. Guardrail: send summaries and links, not
descriptions that may carry personal data.

## Equivalents

Linear: built-in workflow automations + integrations/webhooks. GitHub Projects: built-in project
workflows + GitHub Actions on `issues`/`pull_request` events. Azure Boards: work item rules,
Service Hooks, Pipelines. The same guardrails apply everywhere.
