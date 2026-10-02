# Prioritisation playbook

Read on demand. Generic ways to fill the four cells, rank, stop and record accepted debt.
Project facts (real costs, dated tickets, capacity, deadlines) override every default here.

## 1. Filling the four cells when data is missing

Use a proxy only when it is labelled as a proxy and comes with what to measure to replace it.

| Cell | Direct evidence | Acceptable proxies | Measure to replace the proxy |
|---|---|---|---|
| Cost of delay | Revenue/penalty at risk per week; hours lost per week (tracked) | Incidents/month × mean hours per incident; manual workaround runs × minutes; support tickets tagged to the cause; cycle-time delta in the affected module | Tag the next 2–4 weeks of incidents/tickets/workarounds to the item |
| Cost of fix | Estimate from a spike or a comparable past change | Reference class: similar past items' actual cycle time (p50–p85); per-unit cost × number of integrations/runtimes to retest | Timebox a spike; record actual vs estimate |
| Cliff | A dated external event (contract, regulation, EOL, peak season) | Growth curve hitting a known ceiling (storage, pool, rate limit, table size); vendor deprecation notice | Plot the trend; date when it crosses the ceiling |
| Way back | Tested rollback procedure | Classify: code-only (two-way) / data or schema / public contract / vendor or legal commitment (one-way) | Rehearse the rollback in a non-production environment |

Rules:
- A proxy without a replacement measurement is an opinion; say so.
- Keep one horizon for every item (per week is the default). Mixing "per week" and "per quarter"
  silently re-ranks the list.
- Cost of fix always names **what stops** to pay for it — capacity is never free.

## 2. Ranking — worked example (illustrative numbers)

Five candidate items, one team, next quarter. Numbers below are invented to show the mechanics,
not benchmarks.

| Item | Cost of delay | Cost of fix | Cliff | Way back | Tier |
|---|---|---|---|---|---|
| A. Runtime upgrade before vendor EOL | Low now | 3 weeks | EOL in 10 weeks — no security patches after | Two-way (code) | 1 — near cliff |
| B. Fix shared auth lib that blocks partner team's release | Partner release slips ~1 week per week | 1 week | Partner's contract date in 6 weeks | Two-way | 2 — blocks others |
| C. Automate manual reconciliation | ~6 h/week of ops toil | 2 weeks | None | Two-way | 3 — high CoD / low fix |
| D. Rewrite reporting module "it's ugly" | Unknown | 6 weeks | None known | Partly one-way (data model) | — not rankable |
| E. Split the main database | Unknown; no capacity alarm yet | 10+ weeks | Possibly, at current growth | One-way | — not rankable |

Reading:
- A first despite low current cost: the cliff converts it from linear to sudden.
- B before C: it blocks another team and has a dated consequence.
- C: weekly cost is known and fix is small — strong CD3.
- D and E are **not ranked**: cost of delay is empty. Answer: "not enough data to rank". For D,
  measure lead time and defect rate in the module for a month. For E, plot write load and storage
  growth against current limits to date the cliff — if it is more than two quarters out, defer with
  that measurement as the revisit trigger.
- Within a tier, the reversible option goes first; E would need the one-way certainty bar anyway.

## 3. Accept, refuse, defer, stop

| Decision | When | Must record |
|---|---|---|
| **Do now** | Near cliff, blocks others, or best CD3 in the available capacity | What is stopped to fund it |
| **Accept debt** | Speed gain is real and the debt has bounded interest | Accept-debt record (§4) |
| **Defer** | Linear cost, no cliff inside the horizon | Revisit condition: a state or a date |
| **Refuse** | No cost of delay found after measurement, or cost of fix exceeds any plausible benefit | One-line reason, so it isn't re-raised unchanged |
| **Stop a direction** | Kill criteria hit, or remaining cost of fix exceeds remaining cost of delay | What is salvaged, what is switched off, and by when |

### Kill criteria (set before starting)

- Written as **state + date**: "if p95 latency is not below X by date D", "if fewer than N
  customers adopt by date D", "if the spike can't integrate with system S within 2 weeks".
- Owned by someone who is not the person most invested in continuing.
- Checked at the date — not re-negotiated after the result is known.
- Remaining-cost test at each checkpoint: compare **remaining** effort to the cost of delay of the
  alternatives; effort already spent doesn't enter the comparison.

### Revisit conditions (for every "later")

- A **date** ("re-rank at quarterly planning on …") or a **state** ("when incidents tagged X exceed
  2/month", "when storage passes 70 % of quota", "when vendor announces EOL").
- Attached to the item in the tracker, with an owner — a revisit nobody owns doesn't happen.

## 4. Accept-debt record — template

```
Debt item:        <what shortcut is being taken, where>
Why accepted:     <the speed/outcome it buys, and by when>
Quadrant:         prudent-deliberate (anything else is not an acceptance, it is a defect)
Interest:         <recurring cost while it stays: hours/week, incident risk, slower changes in module M>
Cliff / limit:    <the state or date at which interest jumps>
Way back:         <how it is repaid; is any step one-way?>
Payback trigger:  <state or date that forces repayment>
Owner:            <name>
Review date:      <date>
```

## 5. Common traps when presenting the decision

- Presenting a ranked list without the empty cells shown — readers assume the data exists.
- Bundling several items into one "initiative" so a weak item rides on a strong one.
- Comparing a fully loaded estimate for one option with a code-only estimate for another.
- Treating "no decision" as free — deferral is a decision with its own cost of delay.
