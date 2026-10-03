# Product bet playbook

Read on demand. Generic ways to fill the product bet card and review a portfolio.
Project facts (real cohorts, real usage, real capacity) override every default here.

## 1. Bet card template

```
Bet: <name>                     Owner: <one person>      Review date: YYYY-MM-DD
Job:          When <circumstance>, <user> wants to <progress>, so they can <outcome>.
              Today they use: <alternative>
Evidence:     <what users did — interviews n=?, usage, experiment result, cohort>
Metric ladder:<input metric> → <North Star> → <business outcome>
Fit signal:   <cohort, curve shape, period>  | Sean Ellis: <% very disappointed, n=?>
Opportunity cost: <initiative / team-weeks that stop>
Kill criterion:   if <metric> < <threshold> by <date>, we <stop | pivot to …>
```

An empty cell = not ready to commit. Say which cell and what to collect.

## 2. Reading retention curves

| Shape | Meaning | Action |
|---|---|---|
| Decays toward zero | No retained core for this cohort/job | Don't scale acquisition; go back to Job/Evidence |
| Flattens at a plateau | A retained core exists | Find who is in the plateau → sharpen ICP; improve activation |
| Smiles (rises later) | Users return/expand over time | Strong fit; invest in expansion paths |

Rules: split by acquisition cohort and by segment/job; aggregate retention hides mix shifts.
Commonly cited floors (very context-dependent): consumer D30 below ~20% or B2B below ~40% without
improvement is a warning, not a verdict.

## 3. North Star ladder check

1. Write the North Star. Does it measure value delivered to customers (not revenue)?
2. List 3–5 input metrics. Can each team name which one its work moves?
3. Check correlation with retention over the last 2–4 quarters. North Star up + retention down →
   the metric is wrong.
4. For each roadmap item: which input moves, by how much, measured how? Items with no answer are
   outputs, not bets.

## 4. Portfolio review (quarterly)

| Product | Revenue | Growth trend | Retention trend | Eng. allocation % | Posture | Decision date |
|---|---|---|---|---|---|---|

- Every product gets exactly one posture: invest / maintain / kill.
- A product in "question mark" for 2+ quarters gets a forced decision with a date.
- Allocation check: more than ~30% of team time on declining products is a red flag.
- Kill = sunset date + migration plan for affected customers + communication owner.

## 5. Kill-criteria examples (illustrative)

- "If fewer than 25% of activated accounts use <feature> weekly by 2026-03-31, remove it from the
  roadmap and keep maintenance only."
- "If the D30 retention of the new-segment cohort stays below the core cohort's by more than
  10 points after two release cycles, stop segment-specific acquisition."

Write them before launch; review on the date even if the result is inconvenient.

## 6. Feature request triage

| Signal | Interpretation |
|---|---|
| "How do I do X?" support tickets | Usability/activation gap — fix before building more |
| "I want it to also do Y" | Expansion demand — candidate bet; check the job |
| One large customer demands Z | Sales request — card it; check reach before committing |
| Competitor shipped Z | Parity pressure — check if Z is basic (Kano) for your ICP |
