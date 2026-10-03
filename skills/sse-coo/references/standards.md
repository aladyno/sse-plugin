# Operations standards — deeper notes

Read on demand. For each: what it covers, when to invoke it, and how it is commonly misread.
Cite by name; never invent clause numbers or quotes. This is decision vocabulary, not certification.

## Flow and constraints

**Theory of Constraints — five focusing steps (Eli Goldratt, *The Goal*)**
- Covers: a system's throughput is set by one constraint; identify it, exploit it (no idle time),
  subordinate everything else to it, elevate it (add capacity), then repeat as it moves.
- Invoke when: filling the **Constraint** cell; when improvement effort is spread evenly.
- Misreading: assuming the constraint is headcount. Often it is an approval, a specialist, a test
  environment or a weekly meeting that batches decisions.

**Lean / Toyota Production System (Taiichi Ohno; Womack & Jones, *Lean Thinking*)**
- Covers: value stream mapping, the wastes (waiting, rework, hand-offs, overprocessing…), flow,
  pull, standard work as the base for kaizen.
- Invoke when: a process has many hand-offs and long waits relative to touch time.
- Misreading: lean = cost cutting/headcount reduction. It is about flow and removing waste for the
  customer; cutting people from the constraint lowers throughput.

**Little's Law (John Little, queueing theory)**
- Covers: average WIP = throughput × average lead time in a stable system.
- Invoke when: lead times grow; the fastest lever is often limiting work in progress.
- Misreading: applying it to unstable systems or mixing units; it describes averages, not each item.

**PDCA (Walter Shewhart; W. Edwards Deming)**
- Covers: Plan-Do-Check-Act loop for controlled change.
- Invoke when: a fix is proposed — insist on the Check step before standardising.
- Misreading: running Plan-Do repeatedly without Check; nobody learns whether the change worked.

## Goals, rhythm and accountability

**OKRs (Andrew Grove; John Doerr, *Measure What Matters*)**
- Covers: objectives with measurable key results, set quarterly, checked weekly; stretch goals with
  partial attainment expected.
- Invoke when: filling the **Measure** cell; diagnosing OKR scores always at 1.0 or below 0.3.
- Misreading: OKRs as task lists or as performance-review targets — the latter drives sandbagging.

**EOS — Entrepreneurial Operating System (Gino Wickman, *Traction*)**
- Covers: weekly scorecard of 5–15 numbers with owners, weekly Level 10 meeting, quarterly rocks,
  issues list solved with Identify-Discuss-Solve, accountability chart.
- Invoke when: a small-to-mid company has no rhythm; simple and prescriptive.
- Misreading: adopting the vocabulary without the weekly discipline; rocks without owners.

**Scaling Up / Rockefeller Habits (Verne Harnish)**
- Covers: daily, weekly, monthly, quarterly and annual meeting rhythm; one-page strategic plan;
  priorities, data, rhythm.
- Invoke when: designing the **Rhythm** cell for a growth-stage company.
- Misreading: adding every meeting at once. Start with the weekly and quarterly; add when needed.

**High Output Management (Andrew Grove)**
- Covers: managerial leverage, indicators (leading, paired to avoid gaming), meetings as process
  meetings vs. mission meetings, task-relevant maturity.
- Invoke when: leaders are busy but output doesn't move; scorecards show only lagging numbers.
- Misreading: more 1:1s and reviews as the fix. The point is leverage per hour.

**The 4 Disciplines of Execution (McChesney, Covey & Huling)**
- Covers: focus on the wildly important, act on lead measures, keep a compelling scoreboard, create
  a cadence of accountability.
- Invoke when: teams are swamped by "the whirlwind" of daily work and goals never get attention.
- Misreading: choosing lead measures that the team can't directly influence.

**RACI and RAPID (Bain & Company)**
- Covers: who is responsible, accountable, consulted, informed (RACI); who recommends, agrees,
  performs, inputs, decides (RAPID).
- Invoke when: filling **Owner** and **Escalation** cells; decisions wait or get re-opened.
- Misreading: multiple "A"s or a "D" by committee; "consulted" treated as a veto.

## Management systems and continuity

**ISO 9001:2015 (quality management systems)**
- Covers: process approach, PDCA, risk-based thinking, documented information, management review,
  continual improvement.
- Invoke when: a customer or regulator asks for a quality system; designing management review.
- Misreading: a binder of procedures. The standard asks for processes that are operated, measured and
  reviewed; the entity performs gap analysis only.

**ISO 22301 (business continuity management systems)**
- Covers: business impact analysis, continuity strategies for critical activities, exercising plans.
- Invoke when: the **Scale point** cell reveals single points of failure in people, vendors or tools.
- Misreading: equating continuity with IT disaster recovery only; people and suppliers count.

**CMMI (CMMI Institute / ISACA)**
- Covers: maturity levels and practice areas describing process capability.
- Invoke when: a shared vocabulary for "how mature" is needed (initial → managed → defined →
  quantitatively managed → optimizing).
- Misreading: chasing a level as the goal; maturity without throughput improvement is overhead.
