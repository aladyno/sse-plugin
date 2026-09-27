# Flow Metrics & Probabilistic Forecasting

Read on demand when the question is "are we flowing?" or "when will it be done?".
The optional helper `scripts/flow_forecast.py` computes everything below from a saved
issue export; the numbers it emits are explained here.

## The four flow measures (The Kanban Guide)

The Kanban Guide (Vacanti & Coleman, kanbanguides.org) names four minimum flow measures:

| Measure | Definition | Script field |
|---|---|---|
| **WIP** | Items started but not finished | `counts.wip` |
| **Throughput** | Items finished per unit of time | `throughput.weekly_counts` |
| **Cycle time** | Elapsed time from start to finish of an item | `cycle_time_days.p50/p85/p95` |
| **Work item age** | Elapsed time since start for items not yet finished | `work_item_age` |

**Service Level Expectation (SLE)**: "items of this type finish within N days, X% of the
time". Default here: the p85 cycle time. **Work item age is the leading indicator** — an
in-progress item older than the SLE is the earliest visible slip (`aging_wip_alerts`);
cycle time only tells you after the fact.

Caveat: many exports carry no in-progress timestamp, so cycle time falls back to
created → resolved and includes queue time. Add a `started` date from the changelog
(first transition into an "In Progress"-category status) when you can.

## Little's Law — why limiting WIP works

Average cycle time = average WIP ÷ average throughput (Little, 1961; applied to
knowledge work by Vacanti). Holds only for a roughly stable system (arrivals ≈
departures, items not abandoned). Practical reading: with throughput fixed, **halving
WIP halves average cycle time**. It is a relationship for averages over time — do not use
it to forecast individual items.

## Percentiles, not averages

Cycle-time distributions are right-skewed; the mean hides the tail. Report p50/p85/p95.
Commit externally at p85, plan internally at p50, treat p95 as the tail-risk budget.

## Monte Carlo forecasting ("when will it be done?")

Sample historical weekly throughput thousands of times until N items are done; read the
distribution of weeks at p50/p70/p85/p95 (Vacanti, *When Will It Be Done?*). Rules:

- **Minimum history** — the script refuses below 10 completed items or 4 observed weeks.
- **Zero weeks count** — empty weeks are real observations; dropping them is optimistic bias.
- **Seeded** — same data, same answer (reproducible).
- **Ranges with confidence, never a single date.** "85% likely within 10 weeks."
- **Scope is an input** — if backlog grows during delivery, forecast the growth too
  (split rate / arrival rate), or re-run weekly.
- Works without estimates (#NoEstimates / right-sizing): items only need to be
  "small enough", checked against the SLE, not story-pointed.

## Outcomes above flow

Flow says whether delivery is smooth, not whether it is valuable or safe:

- **DORA software delivery performance** — throughput (deployment frequency, lead time for
  changes) and instability (change failure rate, recovery time). Flow without these can
  hide a team shipping fast into incidents.
- **Evidence-Based Management (Scrum.org)** — Current Value, Unrealized Value,
  Time-to-Market, Ability to Innovate. Measuring only time-to-market measures motion.
- **SPACE (Forsgren, Storey et al.)** — a metrics set should span several dimensions;
  activity-only metrics (PR counts, tickets closed) are the known anti-pattern.
- **Derived status beats self-reported RAG** — diff aging WIP, scope churn and forecast
  drift against the reported colour to find "watermelon" projects.

## Anti-patterns

- Velocity (story points) compared across teams or used as a target (Goodhart's law).
- Single-date commitments from average velocity.
- Resource-utilisation targets near 100% — queueing theory: wait time grows sharply as
  utilisation approaches 100% (Reinertsen, *The Principles of Product Development Flow*).

## Sources

1. The Kanban Guide — https://kanbanguides.org/
2. D. Vacanti, *Actionable Agile Metrics for Predictability*; *When Will It Be Done?*
3. D. Reinertsen, *The Principles of Product Development Flow*
4. DORA research — https://dora.dev/
5. Scrum.org, *Evidence-Based Management Guide* — https://www.scrum.org/resources/evidence-based-management
6. Forsgren, Storey et al., "The SPACE of Developer Productivity", ACM Queue — https://queue.acm.org/detail.cfm?id=3454124
