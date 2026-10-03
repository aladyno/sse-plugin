# Product strategy standards — deeper notes

Read on demand. For each: what it covers, when to invoke it, and how it is commonly misread.
Cite by name; never invent clause numbers or quotes. This is decision vocabulary, not certification.

## The job and the evidence

**Jobs To Be Done (Clayton Christensen; Tony Ulwick's ODI; Alan Klement)**
- Covers: customers hire products to make progress in a circumstance; outcomes they measure that
  progress by; the incumbent alternative is the real competitor.
- Invoke when: filling the **Job** cell; when a feature request arrives without a circumstance.
- Misreading: treating job statements as user stories. A job is solution-free; a story already
  picked the solution.

**Continuous Discovery Habits (Teresa Torres)**
- Covers: weekly customer touchpoints by the product trio, opportunity-solution trees, assumption
  testing before building.
- Invoke when: the **Evidence** cell rests on a one-off research project or stakeholder opinion.
- Misreading: "discovery phase" before delivery. The point is continuous, small and weekly.

**Inspired / Empowered (Marty Cagan, SVPG)**
- Covers: four product risks — value, usability, feasibility, business viability; empowered teams
  given problems, not features.
- Invoke when: a bet only checked feasibility; teams receive feature lists from leadership.
- Misreading: "empowered" = no direction. Leadership still sets strategy and objectives.

## Metrics and fit

**North Star Framework (Amplitude playbook; Sean Ellis)**
- Covers: one metric that captures value delivered to customers, decomposed into 3–5 input metrics
  teams can influence.
- Invoke when: filling the **Metric ladder** cell; when teams optimise local metrics.
- Misreading: choosing revenue as the North Star. Revenue is lagging; the North Star should predict it.

**Sean Ellis PMF survey**
- Covers: share of engaged users who would be "very disappointed" without the product; ~40% is the
  commonly cited threshold.
- Invoke when: a quick directional read is needed alongside retention.
- Misreading: surveying all sign-ups, or using it as proof alone. Sample recent active users and
  pair with cohort retention.

**Cohort retention curves (Reforge; Andrew Chen; Brian Balfour)**
- Covers: retention per acquisition cohort over time; flattening = a retained core exists;
  decaying to zero = no fit for that cohort.
- Invoke when: filling the **Fit signal** cell — the primary evidence.
- Misreading: reporting an aggregate retention number. Mix shifts hide decay; always split by cohort
  and by job/segment.

**Lean Startup — Build-Measure-Learn (Eric Ries)**
- Covers: falsifiable hypotheses, MVPs, innovation accounting, pivot-or-persevere decisions.
- Invoke when: writing the **Kill criterion** — metric, threshold, date.
- Misreading: MVP = low-quality release. It is the smallest test that answers the riskiest question.

**Escaping the Build Trap (Melissa Perri)**
- Covers: organisations measuring output instead of outcomes; product strategy as a system of
  decisions; product operations.
- Invoke when: success is reported as features shipped.
- Misreading: banning roadmaps. Roadmaps remain; they express outcomes and bets, not dates for features.

## Ranking and portfolio

**RICE (Intercom) / ICE**
- Covers: Reach × Impact × Confidence ÷ Effort as a relative score.
- Invoke when: ranking bets whose cards are already complete.
- Misreading: using it to decide whether a bet exists, or comparing scores across teams. It is
  ordinal within one list. For capacity trade-offs against non-product work → `sse-cto`.

**Kano model (Noriaki Kano)**
- Covers: basic, performance and attractive (delighter) attributes and how satisfaction responds.
- Invoke when: debating whether a feature differentiates or is table stakes.
- Misreading: delighters stay delighters; they decay into basics as markets mature.

**BCG growth-share matrix**
- Covers: products by market growth and relative share — stars, cash cows, question marks, dogs.
- Invoke when: assigning invest / maintain / kill postures.
- Misreading: share alone. In software, use retention and growth trend too; a "dog" with sticky
  revenue may be a cash cow on a maintain posture.

**Team Topologies (Matthew Skelton & Manuel Pais)**
- Covers: stream-aligned, platform, enabling and complicated-subsystem teams; interaction modes.
- Invoke when: product org can't execute the bets — queues, hand-offs, unclear ownership of a job.
- Misreading: a re-org as the fix while bets stay vague.

## Quality of use

**ISO/IEC 25010 (product quality model, quality in use) and ISO 9241-210 (human-centred design)**
- Covers: quality-in-use characteristics (effectiveness, efficiency, satisfaction, freedom from
  risk, context coverage); human-centred design activities with users throughout.
- Invoke when: a bet's value depends on usability claims, or for regulated/enterprise buyers asking
  for a quality vocabulary.
- Misreading: claiming "ISO compliant UX". The entity does gap analysis against the model, not
  certification.
