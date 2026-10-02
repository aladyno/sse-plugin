# Prioritisation & investment standards — deeper notes

Read on demand. For each: what it covers, when to invoke it, and how it is commonly misread.
Cite by name; never invent clause numbers or quotes. This is decision vocabulary, not certification.

## Ranking competing work

**Cost of Delay & CD3 (Don Reinertsen, *The Principles of Product Development Flow*, 2009)**
- Covers: the economic view of product development — queues, batch size, WIP and, centrally, the
  cost of delay (value lost per unit of time an item is not delivered). CD3 = cost of delay divided
  by duration: the highest ratio goes first.
- Invoke when: a backlog is ordered by value, size or loudness alone; two items compete for the same
  people. Even a rough weekly cost per item beats an unexplained ranking.
- Misreading: cost of delay is not "business value". A high-value item with no urgency can have a
  low cost of delay; a dull fix before a deadline can have the highest.

**Urgency profiles / classes of service (Kanban Method, David Anderson; Joshua Arnold)**
- Covers: the *shape* of cost of delay over time — expedite (cost is high now), fixed date (cost
  jumps at a date), standard (roughly linear), intangible (low now, rises later and unpredictably).
- Invoke when: filling the **Cliff** cell. The class tells whether deferring is linear or not.
- Misreading: "intangible" is not "unimportant" — unpatched EOL runtimes and unowned debt live here
  and turn into fixed-date items without warning. Give them a review date.

**WSJF — Weighted Shortest Job First (SAFe)**
- Covers: a relative score = (user/business value + time criticality + risk reduction/opportunity
  enablement) ÷ job size, usually on a modified Fibonacci scale.
- Invoke when: a group needs to agree an order and has no real cost data — the scoring forces the
  conversation about time criticality.
- Misreading: treating WSJF scores as numbers to compute with or compare across teams. They are
  ordinal within one session. Where real weekly costs exist, use them instead.

**Theory of Constraints (Eli Goldratt, *The Goal*)**
- Covers: system throughput is limited by one constraint; improving anything else adds no output.
- Invoke when: answering "who does it block" — work that unblocks the bottleneck team, release or
  environment outranks local improvements.
- Misreading: assuming the constraint is engineering capacity; often it is review, test
  environments, approvals or one specialist.

## Debt and investment decisions

**Technical debt metaphor (Ward Cunningham, OOPSLA 1992) & Technical Debt Quadrant (Martin Fowler)**
- Covers: debt as shipping with an incomplete understanding/design and paying interest until it is
  repaid; the quadrant splits reckless/prudent × deliberate/inadvertent.
- Invoke when: deciding to **accept** debt. Prudent deliberate debt is a legitimate trade for speed
  if it is recorded with its interest, an owner and a payback trigger.
- Misreading: "debt" used for any code someone dislikes. Without interest (recurring cost) it is not
  debt worth ranking — record it and leave it.

**SQALE method (Jean-Louis Letouzey)**
- Covers: modelling debt as remediation cost per quality characteristic, so items become comparable
  and aggregatable; many static-analysis tools report a SQALE-style debt ratio.
- Invoke when: someone needs debt items on the same scale as feature work (cost of fix side).
- Misreading: tool-reported remediation minutes are cost of fix only — they say nothing about cost
  of delay. Pair them with incident, toil and lead-time data.

**Wardley Mapping (Simon Wardley)**
- Covers: mapping a value chain against evolution (genesis → custom-built → product → commodity).
- Invoke when: build vs buy vs rent, or "should we write our own X". Components that are already
  product or commodity are rarely worth building; differentiating ones are.
- Misreading: drawing the map for its own sake. One question is enough: where on the evolution axis
  is this component, and does owning it differentiate us?

**DORA metrics / *Accelerate* (Forsgren, Humble, Kim, 2018)**
- Covers: four key metrics — deployment frequency, lead time for changes, change failure rate,
  time to restore service — and the capabilities that predict them.
- Invoke when: justifying platform, CI or debt investment in terms leadership already tracks.
- Misreading: using them as team targets or comparing teams; or reporting speed without stability.

## Decision quality, deferral and stopping

**One-way vs two-way door decisions (Jeff Bezos, Amazon 2015 shareholder letter)**
- Covers: Type 1 decisions (consequential, near irreversible) deserve slow, careful process; Type 2
  (reversible) should be made quickly by small groups.
- Invoke when: filling the **Way back** cell and setting how much evidence to demand first.
- Misreading: labelling a decision two-way because the *code* can be reverted, while data,
  contracts or customer expectations cannot.

**Real options (Chris Matts & Olav Maassen, *Commitment*) & Last Responsible Moment (Mary & Tom
Poppendieck, *Lean Software Development*)**
- Covers: options have value and an expiry; commit as late as is responsible, when the cost of
  waiting starts to exceed the value of what you would learn.
- Invoke when: someone wants to decide now with little information, or to defer forever.
- Misreading: "last responsible moment" used as permission to procrastinate. It requires naming the
  moment (a date or a state) in advance.

**Kill criteria — "states and dates" (Annie Duke, *Quit*, 2022)**
- Covers: deciding in advance the signals that mean stop — a measurable state reached (or not) by a
  date; sunk-cost and escalation-of-commitment bias.
- Invoke when: a direction is in progress and losing; or before starting anything expensive.
- Misreading: setting the criteria after the results arrive, or moving the date when it is missed.

## Governance and risk framing

**ISO/IEC 38500 — Governance of IT for the organization**
- Covers: principles for those governing IT use (responsibility, strategy, acquisition, performance,
  conformance, human behaviour) and the Evaluate–Direct–Monitor model.
- Invoke when: framing an investment or stop decision for leadership — what was evaluated, what is
  directed, and how it will be monitored.
- Misreading: it governs *decision-making*, not engineering practice; it doesn't tell you what to build.

**ISO 31000 — Risk management guidelines**
- Covers: identifying, analysing and evaluating risk (consequence and likelihood) and choosing a
  treatment (avoid, remove the source, change likelihood or consequence, share, retain).
- Invoke when: a speed ↔ risk trade-off is argued with adjectives. Restate it as what breaks, how
  likely, who bears it, and the treatment chosen.
- Misreading: a risk register as the deliverable; the decision and its owner are the deliverable.
