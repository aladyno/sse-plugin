# Decision playbook

Read on demand. Generic ways to test a direction, decide a bet, allocate across bets, stop one, and
communicate it. Company facts (real cash, revenue, people, commitments) override every default here.
No thresholds below are benchmarks — where a number is needed, the playbook names what to measure.

## 1. Kernel worksheet

| Element | Write down | Test it with |
|---|---|---|
| Diagnosis | The crux in one or two sentences, with the evidence (metric, customer behaviour, competitor move, cash date) | Could a competent outsider disagree with it? If not, it's too vague to guide anything |
| Guiding policy | The choice: where to play, how to win, and an explicit "we will not" list | Does it rule out something someone in the company currently wants? |
| Coherent actions | Each bet with owner, people, budget, and what is stopped to fund it | Do the actions reinforce each other, and does the budget actually change? |

Bad-strategy smells: a slogan as diagnosis; ten "strategic priorities"; objectives that restate the
problem ("fix churn"); every department's wish list stapled together; no line that says what stops.

## 2. Go / no-go for a bet

Each criterion is answered with evidence or marked **unknown** with what to measure — never scored
from opinion to make the matrix add up.

| Criterion | Evidence that counts | If unknown, measure |
|---|---|---|
| Demand | Paying or committed customers, usage of a prototype, win/loss notes | Run a smallest test that asks for money or commitment, not interest |
| Fit with the guiding policy | It serves the chosen where-to-play / how-to-win | — if it doesn't fit, the answer is no or a policy change, not an exception |
| Feasibility | Spike, prior delivery of similar scope, required capabilities present | Timeboxed spike; capability gap list |
| Unit economics | Price, cost to serve, acquisition cost from real data | Pilot cohort economics |
| Capacity & cash | Owner and people named; funded within the cash horizon | Allocation plan (§3) and runway impact |
| Way back | Reversible (two-way) or not (one-way) — hires, contracts, public commitments | List the irreversible steps and how late each can be deferred |
| Kill criteria | State + date agreed before start (§4) | — no kill criteria, no go |

Decision: **go** · **go small** (staged: fund the next milestone only) · **not now** (with a revisit
state or date) · **no** (one-line reason, so it is not re-raised unchanged).
Before a one-way go: run a premortem and an outside-view check against a reference class.

## 3. Capital & people allocation

Map every budget line and every person (or FTE share) to one bucket: keep the lights on / protect
the core / grow the core / new bets.

| Step | Do | Output |
|---|---|---|
| Current split | From budget and headcount plan, not from the strategy deck | Table: bucket → spend, people, senior-leader time |
| Intended split | Derived from the diagnosis and cash horizon | Same table, target state |
| Gap | Difference, and what must stop or shrink to close it | Named stops with owners and dates |
| Staging | New bets funded milestone by milestone | Next milestone, its cost, its evidence gate |

Rules:
- There is no default ratio. A company in a cash squeeze and one entering a new market should
  split differently; say why the intended split follows from the diagnosis.
- "Protect the core" is cut last, not first — its cost shows up later as churn and incidents.
- A budget request is routed by question: required to operate or comply → keep the lights on;
  defends existing revenue → protect; expands what works → grow; otherwise → new bet with kill
  criteria. Approval limits and return hurdles are company policy — ask for them, don't invent them.
- Runway = cash ÷ net monthly burn; recompute it for every scenario of the plan, including the
  downside one.

## 4. Kill / pivot criteria

- Written as **state + date**: "if fewer than N paying customers by date D", "if cost to serve is
  not below X by date D", "if partner P has not signed by date D".
- Owned by someone not most invested in continuing; checked on the date, not renegotiated after.
- At each checkpoint compare **remaining** cost with the value of the alternatives; money already
  spent doesn't enter.
- Outcomes: **continue** · **pivot** (same diagnosis, new policy or actions — restate the kernel) ·
  **stop** (what is salvaged, who moves where, what is communicated to whom, by when).

## 5. Board & investor communication

- **No surprises.** Material bad news goes out promptly between meetings: facts first, own it, the
  plan, a realistic timeline, what is needed from the board.
- **Update structure** (monthly or per agreed cadence): headlines · key metrics vs plan · bets —
  status against their kill criteria · challenges with mitigation · cash and runway · asks.
- **Board meeting**: send the pre-read early enough to be read; lead with the decisions required;
  spend the meeting on discussion, not on reading slides aloud; record decisions and owners.
- **One story**: the diagnosis and bets told to the board match what the team and key customers hear.
- **Dissent**: listen fully, restate the concern, answer with data, record the decision and who
  disagreed; on reversible matters, decide and move (disagree and commit).
- Disclosure, securities and fundraising specifics depend on jurisdiction and company type →
  qualified counsel; never advise selective disclosure to some investors.

## 6. Culture & organisation signals

Culture is read from what people do and what the systems reward, not from the values page.

| Signal | What it suggests | Measure |
|---|---|---|
| Regrettable attrition rising, or exits nobody predicted | Bets or leadership not trusted; workload or growth problem | Attrition by team and tenure; exit-interview themes |
| Most decisions wait on the CEO | Unclear decision rights; bottleneck at the top | Count decisions escalated per week; time-to-decision |
| Team can't state the strategy in a sentence | Diagnosis/policy not communicated, or not real | Ask a sample; compare answers |
| Key-person dependency, no successor | Single point of failure for a bet or the company | Successor named per critical role; emergency cover |
| Debate in meetings is absent or performative | Low trust; artificial harmony (Lencioni, *The Five Dysfunctions of a Team*) | Decisions revisited after meetings; skip-level feedback |
| Reorg proposed | Often a substitute for a decision about bets | Which bet does the new structure serve? |

Change and reorganisation: urgency and a guiding coalition before the announcement; announce
structure, leaders and reasons together; change incentives, hiring criteria and budgets in the same
move — otherwise the old behaviour wins (Kotter, *Leading Change*).

## 7. Decision hygiene

- Problem stated; options ≥ 2 genuinely different (including "don't"); criteria set before options
  are scored.
- Biases checked: confirmation (assign a dissenter), anchoring (independent estimates first), sunk
  cost (zero-based question: would we start this today?), overconfidence (reference class).
- Implementation owner, success measure and review date recorded with the decision.

---

Portions adapted from claude-skills `ceo-advisor` by Alireza Rezvani (MIT).
