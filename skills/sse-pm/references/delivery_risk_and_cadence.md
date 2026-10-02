# Scope, Risk, Dependencies & Stakeholder Cadence

Read on demand for sequencing, risk and communication questions. Flow and forecasting
live in `flow_forecasting_canon.md`.

## Sequencing scope — Cost of Delay

- **Cost of Delay (CoD)** — value lost per unit of time an item is not delivered
  (Reinertsen). Makes urgency explicit instead of arguing about "priority".
- **CD3 / WSJF** — divide CoD by duration (or job size) and do the highest first.
  SAFe popularised WSJF with relative scoring (business value + time criticality +
  risk reduction/opportunity enablement) ÷ job size; treat the relative scores as a
  conversation tool, not precise economics.
- **Urgency profiles** — standard, fixed-date, expedite, intangible (Kanban classes of
  service). A fixed-date item with low value still wins if its date is near.
- **Cut scope, not quality** — when the forecast misses the date, the levers in order:
  reduce scope (MoSCoW / slice thinner), move the date, add people last (Brooks's law:
  adding people to a late project tends to make it later).

## Risk — ISO 31000 loop in practice

ISO 31000 frames risk management as identify → analyse → evaluate → treat, with
monitoring, review and communication running throughout.

- **Pre-mortem** (Klein, HBR 2007): "It is six months later and this failed — why?"
  Surfaces risks people are reluctant to raise; run it at kickoff of any big bet.
- **RAID log** — Risks (may happen), Assumptions (believed true, unverified), Issues
  (happening now), Dependencies (need from others). Every entry: owner, next review date,
  trigger/indicator, response. An entry without an owner is decoration.
- **Responses** — avoid, reduce, transfer/share, accept (with a named acceptor).
- **Probability × impact** scoring ranks; it does not decide. Prefer early, cheap
  risk-reduction spikes over precise scores.
- **Assumptions are the cheapest risks to kill** — convert each into a test with a date.

## Dependencies

- Map them explicitly (item → needed-from team → needed-by date → status). Cross-team
  dependencies are the most common cause of aging WIP.
- Remove before managing: re-slice so the team owns the whole slice, move the work to
  the team, or stub the contract.
- Remaining ones get a visible owner on both sides and a date checked at every sync.

## Roles & decisions — RACI

One **Accountable** per decision or deliverable; Responsible can be many; Consulted is
two-way, Informed is one-way. Two A's = nobody accountable. Use it only for the handful of
decisions that keep stalling, not as a whole-project spreadsheet.

## Stakeholder cadence

- **Match cadence to decision rhythm** — weekly written update for sponsors, sprint/
  flow review for delivery, event-driven escalation for red risks. No status meetings
  that could be a written update.
- **Update format (3P-style)** — Progress (what finished, with evidence), Plans (next
  period), Problems (risks/blocks + the decision needed and by when).
- **Forecast in every update** — range + confidence from the latest data, plus what
  changed since last time. Surprise is the failure, not bad news.
- **Escalate with a decision, not a problem** — options, recommendation, deadline.

## Goals — OKRs

Objectives qualitative, key results measurable outcomes (not task lists); few per
period. Connect delivery work to a key result or question why it is in progress.

## Sources

1. ISO 31000 Risk management — Guidelines
2. G. Klein, "Performing a Project Premortem", Harvard Business Review, 2007
3. D. Reinertsen, *The Principles of Product Development Flow*
4. F. Brooks, *The Mythical Man-Month*
5. PMI, *PMBOK Guide* 7th ed. — stakeholder, planning, uncertainty performance domains
6. J. Doerr, *Measure What Matters* (OKRs)
