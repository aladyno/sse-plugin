# Customer standards & proven practice — deeper notes

Read on demand. For each: what it covers, when to invoke it, and how it is commonly misread.
Cite by name; never invent clause numbers or quotes. This is decision vocabulary, not certification.

## Retention measurement

**Cohort analysis and survival curves (Kaplan–Meier estimator, 1958)**
- Covers: tracking customers grouped by start period; estimating the share still active at each
  age, handling customers whose outcome isn't known yet.
- Invoke when: a single blended churn rate hides that new cohorts behave differently from old ones,
  or when comparing before/after an onboarding or pricing change.
- Misreading: reading a cohort too young to be stable, or comparing cohorts at different ages.

**Gross vs. net revenue retention (SaaS metrics practice; David Skok, "SaaS Metrics 2.0")**
- Covers: gross retention = revenue kept after churn and contraction (capped at 100%); net
  retention adds expansion.
- Invoke when: net retention is presented alone as proof of customer health.
- Misreading: computing them on different bases (bookings vs. recognised revenue) or periods.
  Define once and reconcile with finance.

**Customer lifetime value (Sunil Gupta & Donald Lehmann, *Managing Customers as Investments*, 2005)**
- Covers: customer value from margin and retention over time, discounted.
- Invoke when: deciding how much effort a segment deserves.
- Misreading: LTV from revenue instead of margin, or from an immature retention rate.

## Listening to customers

**ISO 10002:2018 — Customer satisfaction: guidelines for complaints handling in organizations**
- Covers: a process to receive, acknowledge, track, respond to and learn from complaints.
- Invoke when: churn reasons are unknown because complaints die in individual inboxes.
- Misreading: a certification target; it is guidance. The core: every complaint recorded,
  categorised, answered and fed back.

**ISO 10004:2018 — Customer satisfaction: guidelines for monitoring and measuring**
- Covers: planning what customer-satisfaction information to collect, how, and how to act on it.
- Invoke when: surveys exist but nothing changes because of them.
- Misreading: measuring for the dashboard. The guidance ends in action and review.

**Net Promoter Score (Fred Reichheld, "The One Number You Need to Grow", HBR 2003)**
- Covers: likelihood-to-recommend survey; promoters minus detractors.
- Invoke when: a cheap, repeatable sentiment signal is needed.
- Misreading: treating NPS as a retention predictor without testing it against actual churn, or
  paying staff on it (it gets gamed).

**Customer Effort Score (Matthew Dixon, Karen Freeman & Nicholas Toman, "Stop Trying to Delight
Your Customers", HBR 2010)**
- Covers: the effort a customer spends to get an issue resolved predicts disloyalty better than
  satisfaction or delight.
- Invoke when: support and onboarding friction is suspected as a churn driver.
- Misreading: measuring effort only in support; onboarding and billing friction count too.

## Investing in customers

**Customer Success (Nick Mehta, Dan Steinman & Lincoln Murphy, 2016)**
- Covers: customer success as an operating discipline — outcomes, time-to-value, proactive
  engagement, health scoring, the CS role distinct from support.
- Invoke when: retention is handled only at renewal, or CS is a reactive ticket queue.
- Misreading: a health score as the deliverable. It must be back-tested against real churn.

**Time-driven activity-based costing (Robert Kaplan & Steven Anderson, HBR 2004)**
- Covers: cost per customer = time each activity takes × capacity cost rate; exposes customers who
  consume far more service than they pay for.
- Invoke when: sizing coverage per segment, or deciding which accounts are below the floor.
- Misreading: precision theatre — rough time estimates per activity are enough to rank accounts.

**Bow-tie model (Winning by Design)**
- Covers: post-sale stages (onboarding, adoption, expansion) measured with conversion and time per
  stage, like the acquisition funnel.
- Invoke when: onboarding and adoption have no measured stages or owners.
- Misreading: drawing it without data; each stage needs an entry definition and a metric.

**Goodhart's law (Charles Goodhart, 1975)**
- Covers: a measure that becomes a target stops measuring well.
- Invoke when: designing CS compensation and KPIs.
- Misreading: dropping metrics. Pay on gross retention with guardrails; never on NPS or activity counts.
