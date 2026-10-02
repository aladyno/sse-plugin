# Commercial playbook

Read on demand. Generic ways to build the revenue bridge, find where revenue leaks, audit a
forecast, test a price, and size the go-to-market. Company facts (real billing, pipeline, contracts,
comp plans) override every default here. Numbers marked **heuristic** are widely used rules of thumb,
not benchmarks — calibrate them against the company's own history before using them in a decision.

## 1. Revenue bridge input

Ask the user for one row per customer (or per account × period). A billing or CRM export is enough:

| Field | Meaning |
|---|---|
| `customer_id` | Stable identifier |
| `segment` | Size, vertical or channel — whatever the company uses to sell differently |
| `source` | Acquisition channel (inbound, outbound, partner, self-serve, …) |
| `start_date` | First paid period |
| `revenue_open` | Revenue at the start of the period (contract value, run-rate, or period volume × price) |
| `revenue_close` | Revenue at the end of the period |
| `churn_date` | Blank if active |
| `churn_reason` | As recorded; blank is a finding |

Classify each row's change: **new** (no opening revenue), **expansion** (close > open),
**contraction** (0 < close < open), **churn** (close = 0). Sum by term, then by segment and source.
For transactional models (bookings, GMV × take rate), use the same period-over-period logic per
customer; seasonality → compare the same period year over year.

Missing columns are findings: no `churn_reason` means churn has never been diagnosed.

## 2. Retention and churn diagnosis

1. **Gross before net.** Compute gross retention (floor) and net retention together, per segment
   and per start cohort. Net well above gross → expansion masking a leak; check how concentrated
   the expansion is.
2. **Cohort curves.** Plot retained revenue by months since start for each cohort. A curve that
   flattens shows a retained core; one that keeps falling shows no lasting value. Compare cohorts
   before and after a pricing, product or channel change.
3. **Churn reason taxonomy** — classify every churned account into exactly one:

   | Reason | Typical signal | Owner of the fix |
   |---|---|---|
   | Never reached value | Low activation, no usage after onboarding | Onboarding / product |
   | Bad fit | Segment or use case outside the ICP | Sales qualification / marketing |
   | Champion left | Contact changed, engagement dropped suddenly | Account management (multi-thread) |
   | Competitor won | Named alternative in exit notes | Product + pricing |
   | Budget / company event | Downsizing, acquisition, shutdown | Largely unavoidable — track, don't chase |
   | Involuntary | Failed payment, expired card | Billing / dunning — usually the fastest win |

4. **Exit evidence.** Exit conversations run by someone other than the account owner; verbatim notes;
   "what would have had to be true for you to stay?" Feed patterns to product and sales each period.
5. **Health signals.** Use behaviour (usage depth, engagement, support friction, contract timing),
   weighted by what actually preceded churn in past data — not by opinion.

## 3. Pipeline and forecast audit

| Check | How | Broken when |
|---|---|---|
| Stage definitions | Each stage has a buyer-evidence exit criterion (MEDDPICC elements) | Stages describe seller activity only |
| Coverage | Open pipeline for the period ÷ target | Below what history shows is needed (heuristic: ~3x for sales-led B2B) |
| Conversion | Stage-to-stage conversion and win rate from closed history, by segment | Forecast weights assume better than history |
| Cycle time | Created-to-close by segment | Deals forecast to close faster than they ever have |
| Aging | Deals older than the typical cycle still at the same stage | Stale deals inflating coverage |
| Concentration | Share of the forecast in the top few deals | One slipped deal misses the period |
| Accuracy | Past forecasts vs. actuals | Repeated misses in the same direction (sandbagging or optimism) |

Build the forecast bottom-up from calibrated conversion, then compare with the top-down target —
the gap is the honest conversation. Scenarios (conservative / base / upside) differ by stated
assumptions, not by a percentage applied to the base.

## 4. Pricing and packaging

- **Value first.** Name the economic outcome the customer gets, quantify it per customer, compare
  with their next-best alternative. Price captures a share of that difference.
- **Price metric.** The unit charged should grow with the customer's value (seats, usage,
  transactions, outcomes). A metric that doesn't scale with value produces contraction or leaves
  expansion uncaptured.
- **Packaging.** Tiers follow segments with different willingness to pay; each tier useful on its
  own; upgrade triggers obvious; features that drive adoption not gated.
- **Discount governance.** Written policy, approval levels, a log. Track realised price vs. list by
  segment and rep; leakage hides here.
- **"Too expensive" in loss notes.** First check whether value was demonstrated and whether the deal
  was in the ICP; price is the answer only when both hold.
- **Changing price.** Test before rolling out — new customers first (cohort test) or one segment
  first; existing customers get notice and a grandfathering rule decided in advance; measure win
  rate, conversion and churn for a fixed window after the change. Never change price retroactively.
- **Competition law.** Agreements on price with competitors, resale-price restrictions on partners
  and discriminatory pricing are legal questions → counsel before acting.

## 5. Go-to-market model and sales capacity

| Motion | Fits when | Watch |
|---|---|---|
| Self-serve / product-led | Low price point, fast time to value, user can buy alone | Activation and conversion; when to add sales assist for larger accounts |
| Inside sales | Mid price, short cycle, few stakeholders | Rep productivity, cycle time, discounting |
| Field / enterprise | High price, long cycle, many stakeholders, procurement | Concentration, forecast evidence, cost of sale vs. deal size |
| Partner / channel | Partners own customer access or local presence | Channel conflict, margin to partners, partner concentration, who owns the customer |

Capacity from measured data: productive capacity = ramped reps × measured attainment; new hires
counted only after measured ramp time. Hiring plan derived from the target **and** the measured
ramp and attainment — never from target ÷ quota alone. Attainment spread matters: if most reps miss,
check quota calibration, territory and qualification before individuals.

## 6. Comp-plan checks

- What behaviour does the plan pay for — and what does a rep do at period end to maximise it?
- Pays on bookings only? Add a guardrail: clawback window on early churn, or a retention/margin component.
- Discounts reduce commission? If not, discounting is free to the rep.
- Account ownership after the sale is explicit — who is paid on expansion and renewal.
- Short-term incentives used sparingly; frequent ones teach reps to wait for them.
- Comp changes are communicated with the reasoning and modelled on last period's deals first.

## 7. Board revenue section

One page, same definitions every period:

- Revenue bridge for the period (opening → new, expansion, contraction, churn → closing), by segment.
- Gross and net retention trend; cohort curve for the latest cohorts.
- Forecast vs. target with coverage, and last periods' forecast accuracy.
- Concentration: top customers / channels / partners as a share of revenue.
- Unit economics by segment: acquisition cost and payback.
- Top risks with owner and date; bad news stated first, with what is being done.

---

Portions adapted from claude-skills `cro-advisor` by Alireza Rezvani (MIT).
