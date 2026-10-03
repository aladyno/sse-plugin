# Tracker Adoption Playbook — Restructuring Communication, Not Installing a Tool

Read on demand when a team is introducing (or re-launching) an issue tracker, when adoption is
stalling, or when someone asks "why do we need the tracker at all?". Jira is the example; the
reasoning is tracker-agnostic. Configuration details live in `workflow-design.md`,
`jql-cookbook.md` and `automation-rules.md` — this file is about *why* and *how it lands*.

## Core principle — Conway's law

> "Organizations which design systems are constrained to produce designs which are copies of the
> communication structures of these organizations." — Melvin E. Conway, 1968 (essay written 1967)

| Consequence | What it means for tracker adoption |
|---|---|
| System quality follows communication quality | Recurring defects, unclear ownership and lost decisions are usually communication-structure defects, not skill defects. Diagnose them as such. |
| The tracker *is* a communication structure | Projects, components, workflows and assignment rules decide who talks to whom about what. Design them deliberately. |
| Inverse Conway maneuver | Shape the tracker around the system's domain boundaries (e.g. Booking, Payment, Vendor integration), not the org chart — or the org chart gets copied into the system again. |
| The tool is the container, not the content | Adoption succeeds only if the *structure* (single intake, ownership, linked history) is enforced; the tool brand is irrelevant. |

## Six symptoms → mechanism → check

Each symptom of a missing communication structure maps to a tracker capability, an engineering
mechanism that makes it real, and a measurable check that it works.

| # | Symptom (no structure) | Tracker capability | Engineering mechanism | Verifiable check |
|---|---|---|---|---|
| 1 | Decisions have no history — "why is it like this?" is answered from memory | Decision record on the issue | Business *why* in the issue; technical *why* in an ADR in the repo, linked both ways | Every Epic/Story that changes architecture has an ADR link; sample 10 → ≥ 9 have one |
| 2 | Ownership unclear — people look at each other when something breaks | Assignee on every issue | Assignee required to leave To Do; CODEOWNERS per module mirrors component owners | JQL: `statusCategory = "In Progress" AND assignee IS EMPTY` returns 0 |
| 3 | Same bug recurs (regression) — nobody knows why | Issue links (causes / is fixed by / relates to) | Bug can close only with: link to causing change, link to fixing PR, a regression test | Reopened-or-duplicate bug rate trends down quarter over quarter |
| 4 | Requests vanish — sent straight to a developer via chat, PM never sees them | Single intake (one source of truth) | "No ticket, no work"; the receiver converts a chat request into a ticket in < 1 min | Spot-check: work in recent PRs without a ticket key ≈ 0 |
| 5 | Progress invisible — must ask a person to learn status | Board + status categories | Status driven by dev events (branch → In Progress, PR → In Review, merge → Done) via SCM integration | Board status matches PR state for ≥ 95 % of sampled items |
| 6 | Organisation's work invisible — "what is engineering doing?" | Reports / dashboards from issue data | Team-level flow metrics (throughput, cycle time, WIP age), not per-person ticket counts | A recurring report answers "what shipped, what is blocked" without a meeting |

## Rollout principles

1. **Tool and training ship together.** Everyone starts from the same line with the same written
   guide; no "install it and figure it out".
2. **State the purpose before the procedure.** The goal is restructuring communication; people
   tolerate friction they understand the reason for.
3. **Automate the bookkeeping.** Every manual status update is a reason to abandon the tool —
   wire SCM events (ticket key in branch/commit/PR) to transitions first.
4. **Make the record the path of least resistance.** If asking in chat is easier than filing a
   ticket, chat wins. Provide templates, quick-create, and a chat-to-ticket shortcut.
5. **Pilot, then expand.** One team, one workflow, two to four weeks, measured with the checks
   above, before copying to other teams.

## Resistance — name it accurately

- Expect discomfort and the urge to revert; it is a normal reaction, not sabotage.
- The old way (chat requests, email confirmation, spreadsheet tracking) feels better because it
  is **familiar**, not because it is **effective**. Familiarity and effectiveness are separate
  questions — judge the old way by the six symptoms it keeps producing.
- Keeping the purpose visible is what carries people through the friction.

## Feedback rule — a complaint is not feedback

Accept feedback in this shape only:

| Part | Question it answers |
|---|---|
| **What** | Which step, field or rule is inconvenient? |
| **Why it matters** | What does it cost (time, errors, lost information) and for whom? |
| **Alternative** | What concrete change would fix it, and what would it trade off? |

"It was better before" or "why do we have to do this" lacks all three parts and does not move the
change forward. Route valid feedback into the tracker itself (a "process improvement" issue type)
so the process eats its own dog food.

## Failure modes to pre-empt

| Failure mode | Why it happens | Counter-measure |
|---|---|---|
| Double entry (tracker + SCM updated by hand) | No integration | Ticket key mandatory in branch/commit/PR; status transitions automated |
| Process blocks incident response | "Ticket first" applied to a 2 a.m. outage | Allow retroactive ticket within 24 h for hotfixes, plus a mandatory postmortem link |
| Decisions buried in comment threads | No designated place for the decision | "Decision" field or required ADR link on architecture-changing work |
| Metrics weaponised per person | Ticket counts used for appraisal | Goodhart's law: people split tickets to inflate counts. Report flow at team level only |
| Org chart copied into project/component layout | Projects split by reporting line | Split by domain boundary (inverse Conway); align components with code modules |
| Status/field sprawl from day one | Every stakeholder adds "their" status or field | Start minimal (see `workflow-design.md`); add a status only for a distinct wait/owner |

## Adoption health check (30 / 60 / 90 days)

- [ ] ≥ 95 % of merged PRs carry a ticket key.
- [ ] 0 in-progress issues without an assignee.
- [ ] Board status agrees with PR/deploy state on a 20-item sample.
- [ ] Every closed bug in the period links to a fixing PR; regression-test link on ≥ 80 %.
- [ ] Leadership status questions answered from a dashboard, not a status meeting.
- [ ] Feedback issues received are in what/why/alternative form, and each has an owner.

## Hand-off

- Workflow/status design → `workflow-design.md`; queries for the checks above → `jql-cookbook.md`;
  SCM-driven transitions → `automation-rules.md`.
- Flow metrics and forecasting → `sse-pm`. Ticket content quality (stories, AC) → `sse-ba`.
- Org-level alignment and change narrative → `sse-cso`.
