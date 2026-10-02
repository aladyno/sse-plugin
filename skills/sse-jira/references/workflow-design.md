# Workflow Design — Workflow as a State Machine

Read on demand when designing, reviewing or simplifying a workflow. Jira terms are primary;
equivalents for other trackers are at the end. The user can lint a design with
`scripts/workflow_validator.py` (clean sample: `assets/sample_workflow.json`; demo with a
deliberate "Blocked" dead end: `assets/sample_workflow_with_defect.json`).

## The model

| State-machine term | Jira term | Rule |
|---|---|---|
| State | Status | A status is **where work waits for a different action or owner**. No distinct wait/owner → not a status. |
| Initial state | Create transition target | Exactly one. |
| Terminal state(s) | Statuses in the **Done** category (+ Resolution set) | At least one; every state must be able to reach one. |
| Transition | Transition (a named action) | Named as a verb: "Start work", not "In Progress". |
| Guard | Condition / Validator | Conditions hide the transition; validators reject it with a message. |
| Side effect | Post-function / Automation rule | Must be idempotent and must not fight other rules. |
| Invariant | Required fields, Resolution rules | E.g. "Done ⇔ Resolution is set"; "In Progress ⇒ assignee not empty". |

## Design checks (in order)

1. **Reachability** — every status reachable from the initial state (no orphans).
2. **Liveness** — every non-terminal status has an exit and can reach Done (no dead ends, no
   closed loops without an exit).
3. **Minimal states** — each status has a distinct owner or wait reason. Merge statuses that
   differ only in who is typing. Prefer ≤ ~7 per workflow for delivery teams.
4. **Waiting vs working made visible** — split "Review requested" (waiting) from "In review"
   (working) only if you will measure or limit it; otherwise one status.
5. **Status category mapping** — every status mapped to To Do / In Progress / Done correctly;
   flow metrics, boards and `statusCategory` JQL depend on it.
6. **Resolution discipline** — set Resolution on every transition into a Done-category status
   and clear it on reopen; otherwise "resolved" JQL and reports lie.
7. **Rework paths** — explicit backward transitions (Request changes, Reopen) rather than a
   free-for-all "any status → any status" global transition.
8. **Blocked is a flag, not a status** — a Blocked status loses where the item was; use the
   Flagged field / a blocker link, and keep the item in its real status so aging shows.
9. **Guards at the right place** — validators on the transition where the data is known
   (fix version before "Release", comment on "Reject"); avoid required fields on Create that
   people fill with junk.
10. **Scheme reuse** — share one workflow across projects/issue types unless the process
    genuinely differs; every variant is maintenance cost and breaks cross-project JQL.

## Typical shapes

```
Delivery:   Backlog → Ready → In Progress → In Review → Done      (+ Request changes, Reopen)
Bug:        Triage → Ready → In Progress → In Review → Done       (+ Won't do via Resolution)
Service:    New → Triaged → In Progress → Waiting for customer → Resolved → Closed
```

Service workflows (ITIL 4 practices: incident, service request, problem, change) need a
distinct "waiting for customer" status because SLA clocks usually pause there.

## Transitions — properties to decide

| Property | Decide |
|---|---|
| Name | Verb phrase describing the action |
| Screen | Only when data must be captured at that moment (e.g. resolution, reason) |
| Conditions | Who may do it (role/group) — least privilege, but never so strict that work stalls |
| Validators | What must be true (field set, sub-tasks done, comment added) |
| Post-functions | Set/clear Resolution, assign, fire event; keep "update change history" and "fire event" at the end of the list |

## Changing a live workflow

- Stage in a copy/test project first; walk sample issues through every transition.
- Map every old status to a new one before publishing (Jira forces a migration mapping).
- Check what depends on status names: saved filters, board columns, automation rules, SLAs,
  dashboards, integrations. Renaming a status silently breaks JQL that matches by name.
- Announce the change and the meaning of each new status (the policy), not just the diagram.

## Equivalents in other trackers

| Concept | Linear | GitHub Projects | Azure Boards |
|---|---|---|---|
| Status / category | Workflow states in fixed types (Backlog, Unstarted, Started, Completed, Canceled) | Single-select "Status" field on the project | States mapped to state categories (Proposed, In Progress, Resolved, Completed, Removed) |
| Guards / validators | Limited; rely on conventions and automations | None built in; use Actions/workflows | Rules on work item types (process customisation) |
| Automation | Built-in automations, integrations | Built-in project workflows + GitHub Actions | Rules, Service Hooks, Pipelines |
