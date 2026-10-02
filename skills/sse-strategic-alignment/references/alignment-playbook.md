# Alignment playbook

Read on demand. Generic ways to draw the goal tree, find where the strategy breaks, and repair it.
Company facts (real goals, owners, incentives, survey answers) override every default here.
No thresholds below are benchmarks — where a number is needed, the playbook names what to measure.

## 1. Goal-tree input

Ask the user for one row per goal (and, for the work-level sample, per in-flight initiative or epic).
A plain table or spreadsheet export is enough:

| Field | Meaning |
|---|---|
| `id` | Stable identifier (C1, ENG-2, …) |
| `level` | company / department / team / individual / work |
| `statement` | The objective or work item, as written |
| `owner` | One named person or team; blank if none |
| `parent` | `id` of the goal it serves; blank if none |
| `measure` | The key result or metric that shows progress |
| `incentive` | What the owner is rewarded on, if different from `measure` |
| `depends_on` | Other teams or `id`s it needs to succeed |

Missing columns are findings, not obstacles: a goal set with no `owner` or `parent` column has
already answered the first audit question.

## 2. Cascade audit — steps

1. **Source check.** Can the strategy be stated in one sentence with what it excludes? If not,
   stop: the cascade has nothing stable to carry → `sse-ceo`.
2. **Trace up.** For every non-company row: does `parent` exist and is it current? Blank or stale →
   **orphan**.
3. **Trace down.** For every company goal: list children and owners. None → **unsupported goal**;
   children that can't move it → **weak support**.
4. **Link strength.** For each edge ask: if the child is fully achieved, how much does the parent
   move? "Somewhat, indirectly" → mark as weak and ask for the causal chain (strategy-map logic).
5. **Sideways.** Pair goals and incentives that touch the same customer, system or resource: if
   both are achieved, is the company better off? If not → **conflict**.
6. **Seams.** For every `depends_on` across teams and every goal needing two teams: is there one
   owner and a shared measure? If not → **unowned seam**.
7. **Work sample.** Take a sample of in-flight work from the tracker and trace each item to a goal.
   Report the untraceable share as counted from the sample, with its size — not as a benchmark.
8. **Signal check.** Run §4 and compare with the written strategy.

## 3. Detection — orphans, gaps, conflicts, silos

| Pattern | Signals | Typical root cause | Fix |
|---|---|---|---|
| Orphan goal or work | "Nobody above us cares about this"; work outside any planning cycle | Goals carried from last cycle or set bottom-up without reconciling | Connect to a parent with a real causal link, or cut |
| Unsupported company goal | The same company goal misses every cycle; every team "supports" it | No explicit owner; everyone assumes another team has it | Name one owning team and leader; assign contributing teams |
| Over-concentration | Many teams on one company goal, none on another | Easy or visible goal attracts effort | Rebalance by named owner, not by headcount ratio |
| Conflict | Both teams green, company outcome red; recurring escalations between the same two teams | Incentives on local metrics (volume vs. quality, speed vs. stability, cost vs. service) | Shared guardrail metric owned by both; change the incentive before the goal |
| Silo | Teams can't describe an adjacent team's priorities; coordination only flows up; data not shared between dependent teams | No shared goals or language; structure cuts across the outcome | Shared goal with co-owners; explicit interaction mode per seam (Team Topologies); liaison or joint review |
| Unowned seam | Shared platform or dependency blocks several teams; "that's not our problem" | Interaction never designed; platform measured on output | One owner per seam, a service expectation, a shared measure |

Shared-ownership goal shape: objective · primary owner · contributing owner · key result owned by
each · one shared key result that needs both.

## 4. Communication-gap check

- **Articulation sample.** Ask people from several teams and levels, separately: "What is the most
  important thing the company is trying to achieve right now?" Record answers verbatim; group them;
  compare with the written strategy. Report the spread as observed, not as a score.
- **Back-brief (Bungay).** After a strategy briefing, each leader states back the intent, their
  team's contribution and what they will stop. Gaps show up before work starts.
- **Behaviour check.** "What changed in how your team works since the last strategy update?" and
  "Name a decision made recently that the strategy influenced." No answers → the message arrived,
  the strategy didn't.
- **Gap sources:** strategy too abstract to act on; repeated too rarely; filtered differently by each
  manager; contradicted by later messages; not believed ("we've heard this before").

## 5. Realignment protocol (catchball)

1. **Start from direction, not blame.** Frame as "here is where we're heading; let's check we're
   connected", not "here is our misalignment".
2. **One-page strategy.** Direction in a sentence · the few priorities, each with an owner · what we
   are not doing · how success is measured. The "not doing" line stops each team adding its own.
3. **Catchball workshop.** Company-goal owners explain the why → departments draft their
   contribution → all drafts are cross-checked together for gaps, conflicts and seams → resolve
   before publishing (assign owners, add shared/guardrail measures) → each department repeats with
   its teams.
4. **Fix incentives first.** Where a team is rewarded on a metric that conflicts with a company goal,
   change or pair the incentive in the same move — otherwise the old goal wins.
5. **Make links visible.** Goals and their parents published where every team can see them; tracker
   initiatives linked to goals.
6. **Close the loop.** Re-run the articulation sample and the work sample after the change.

## 6. Cadence

- **Before each planning cycle:** review last cycle's goals (hit/missed), run the cascade audit,
  hold the catchball workshop, publish goals with parents, owners and shared measures.
- **Periodic review (e.g. monthly):** each lead states how their work moves the company goals; a
  lead who can't state the link is a broken edge to investigate.
- **Leadership meeting standing question:** "Is anything happening in our area that is at odds with
  the strategy?"
- **Strategy reviews separate from operational reviews** (Kaplan & Norton), so deployment is
  discussed, not crowded out by status.

## 7. Patterns by scale

- **Everyone in the same conversations:** alignment is informal and works — until hiring breaks
  the shared context. Start writing the strategy and its "not doing" list before that point.
- **Functions forming:** product, engineering and go-to-market drift; promises and plans diverge.
  Shared planning and a joint review of the roadmap against customer commitments.
- **Several management layers:** strategy is re-interpreted at each layer; department heads optimise
  their own metrics; cross-functional work stalls at the intersection. Shared goals, guardrail
  metrics, a formal cascade audit each cycle.
- **Multiple business units or product lines:** sub-strategies drift; units compete for the same
  customers; platform teams build for internal needs that differ from product direction. Explicit
  unit-to-company and support-unit alignment (Kaplan & Norton, *Alignment*) and a named owner for
  deployment across units.

---

Portions adapted from claude-skills `strategic-alignment` by Alireza Rezvani (MIT).
