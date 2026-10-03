# Operating loop playbook

Read on demand. Generic ways to run the execution-loop audit and close the gaps.
Project facts (real owners, real meetings, real queue times) override every default here.

## 1. Loop-audit table

List 5–15 recurring outcomes (company goals, critical processes, services). Fill one row each.

| Outcome | DRI (one) | Leading metric + target | Forum & frequency | Escalation (threshold → who → within) | Constraint | Breaks at |
|---|---|---|---|---|---|---|

Rules:
- Empty DRI or two names → first finding for that row.
- A metric that takes more than a day to pull is not a scorecard metric yet.
- Escalation without a time limit is a suggestion.

## 2. Constraint hunt

1. Map the steps of the process end to end (value stream): step, owner, touch time, wait time,
   rework %.
2. The constraint is usually where work **waits** longest or where everyone needs the same person,
   approval or environment.
3. Exploit before elevating: remove idle time at the constraint (batching, priority rules, prepared
   inputs) before hiring or buying.
4. Subordinate: other steps pace to the constraint; don't push more WIP into it.
5. Re-measure; the constraint moves — repeat.

Proxy if no flow data: ask "what do people wait for most?" across 5 people; then measure that step
for 2 weeks.

## 3. Cadence audit — add / keep / kill

| Meeting | Purpose | Decision it produces | Attendees | Last 4 instances produced actions? | Verdict |
|---|---|---|---|---|---|

Default rhythm to compare against (adjust by stage):
- **Daily** (team, ≤15 min) — blockers only.
- **Weekly** (leadership/team) — scorecard review, issues solved, owners + dates.
- **Monthly** — business review: metrics vs. plan, trends, cross-team issues.
- **Quarterly** — goal reset, retro on the quarter, resource shifts.
- **Annual** — strategy and plan (owned with `sse-ceo` / `sse-cso`).

Kill any meeting with no decision in its last four instances, or merge it.

## 4. Scorecard design

- 5–15 numbers for a leadership team; each has one owner, a weekly target, a source.
- Mix: leading (pipeline created, cycle time, backlog age) over lagging (revenue, churn).
- Pair metrics to avoid gaming (speed with quality, volume with rework).
- Red for two weeks running → goes on the issues list automatically.

## 5. Escalation rules (template)

```
If <blocker type> is unresolved for <N hours/days> at <level>,
the owner escalates to <role>, who decides within <time>.
A blocker reported in 3 consecutive weekly syncs escalates automatically.
```

Track decision cycle time (raised → decided). Rising cycle time as headcount grows means decision
rights are too centralised.

## 6. Scale-point check

| Signal | Typical break |
|---|---|
| ~10 → 30 people | Tribal knowledge stops travelling; first managers needed; written decisions |
| ~30 → 80 | Coordination across teams; need cadence, scorecards, explicit decision rights |
| ~80 → 200 | Decision speed; layers; functional leaders who are operators |
| Volume ×3 | Manual steps per transaction, spreadsheets as systems, single-person approvals |

For each recurring process: manual steps per unit × projected volume = hours needed. Compare with
capacity and date the crossing. Remove or automate steps **after** the process is stable (PDCA).

## 7. Single-point-of-failure register

| Critical activity | Person/tool/vendor | Backup | Documented? | Impact if lost for 2 weeks |
|---|---|---|---|---|

Anything with no backup and high impact gets an owner and a date to fix.
