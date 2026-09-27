# JQL Cookbook

Read on demand. Replace `PROJ` with the real project key. The entity drafts JQL itself from
these patterns; the user runs it and pastes back results or errors.

In the blocks below, `--` text is an annotation, not JQL — strip it before pasting.

## Rules that make JQL portable and correct

- Prefer `statusCategory` (`"To Do"`, `"In Progress"`, `Done`) over status names — survives
  workflow renames and works across projects with different workflows.
- Use `resolution` / `resolved` only if the workflow sets Resolution reliably (see
  `workflow-design.md` §6); otherwise use `statusCategory` + `status changed`.
- Custom fields: use the exact name in quotes (`"Story Points"`) or `cf[10016]`; names differ
  per site (e.g. team-managed projects use "Story point estimate").
- Epic relationships: modern Jira uses `parent = PROJ-123`; `"Epic Link"` is legacy.
- Relative dates: `-7d`, `-2w`, `startOfWeek()`, `endOfMonth(-1)`; absolute: `"2026-01-31"`.

## Flow & delivery

```text
-- Current WIP
project = PROJ AND statusCategory = "In Progress"

-- Aging WIP: in progress and last status change older than 10 days
project = PROJ AND statusCategory = "In Progress" AND status changed BEFORE -10d

-- Throughput this week
project = PROJ AND statusCategory = Done AND status changed TO Done DURING (startOfWeek(), now())

-- Finished in the last 12 weeks (export for flow_forecast / cycle-time analysis)
project = PROJ AND statusCategory = Done AND resolved >= -12w ORDER BY resolved ASC

-- Blocked / flagged
project = PROJ AND Flagged = Impediment AND statusCategory != Done

-- Reopened work (rework signal)
project = PROJ AND status WAS IN (Done) AND statusCategory != Done
```

## Sprint (Scrum)

```text
sprint in openSprints() AND project = PROJ ORDER BY Rank
project = PROJ AND sprint in closedSprints() AND sprint in openSprints()   -- carried over
project = PROJ AND sprint is EMPTY AND statusCategory != Done ORDER BY Rank   -- backlog
```

## Hygiene

```text
-- Stale open work
project = PROJ AND statusCategory != Done AND updated <= -30d ORDER BY updated ASC

-- Done without resolution (breaks reports)
project = PROJ AND statusCategory = Done AND resolution is EMPTY

-- Resolution set but not done (reopen did not clear it)
project = PROJ AND statusCategory != Done AND resolution is not EMPTY

-- In progress without owner
project = PROJ AND statusCategory = "In Progress" AND assignee is EMPTY

-- Open children of an epic/parent
parent = PROJ-123 AND statusCategory != Done
```

## Bugs & quality

```text
project = PROJ AND type = Bug AND priority in (Highest, High) AND statusCategory != Done ORDER BY created ASC
project = PROJ AND type = Bug AND created >= startOfMonth()
project = PROJ AND type = Bug AND fixVersion = "1.4.0" AND statusCategory != Done   -- release blockers
```

## People & dependencies

```text
assignee = currentUser() AND statusCategory != Done ORDER BY priority DESC
assignee in membersOf("team-payments") AND statusCategory = "In Progress"
issue in linkedIssues("PROJ-123", "is blocked by")
issueLinkType = "is blocked by" AND statusCategory != Done AND project = PROJ
```

## History operators

`WAS`, `WAS IN`, `CHANGED`, with `FROM`, `TO`, `BY`, `DURING`, `BEFORE`, `AFTER`, `ON`:

```text
status CHANGED FROM "In Review" TO "In Progress" AFTER -14d   -- review bounce-backs
assignee CHANGED BY currentUser() AFTER -7d
```

## Performance tips (Atlassian guidance, practical)

- Scope every filter used by boards/dashboards/automation with `project` (or a saved filter)
  — unbounded queries run against the whole site.
- Avoid broad text search (`text ~`, `summary ~ "*foo"`) in shared filters; leading
  wildcards are not supported and full-text search is costly.
- History operators (`WAS`, `CHANGED`) and large `IN (...)` lists are heavier — keep them out
  of high-frequency automation schedules.
- App-provided JQL functions can be very expensive; check them before using in boards.
- Save and share one canonical filter per board/report instead of copies that drift.

## Other trackers

Linear: filters + views (no query language exposed to users). GitHub Projects: filter syntax
(`is:open label:bug assignee:@me`) and GitHub search qualifiers. Azure Boards: WIQL / query
editor (`[System.State]`, `[System.AssignedTo]`, `@Me`, `@Today`).
