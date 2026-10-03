# Engineering operating-model standards — deeper notes

Read on demand. For each: what it covers, when to invoke it, and how it is commonly misread.
Cite by name; never invent clause numbers or quotes. This is decision vocabulary, not certification.

## Delivery measurement

**DORA four keys / *Accelerate* (Nicole Forsgren, Jez Humble, Gene Kim, 2018) + State of DevOps reports**
- Covers: deployment frequency, lead time for changes, change failure rate, time to restore service;
  the technical and cultural capabilities that predict them (CI, trunk-based development, loosely
  coupled architecture, test automation, generative culture).
- Invoke when: scoring a team's delivery or justifying platform/quality investment.
- Misreading: banding with numbers from an unstated year (bands change between reports); measuring
  only throughput keys; comparing teams or individuals against each other.

**SPACE framework (Forsgren, Storey, Maddila, Zimmermann, Houck, Butler, 2021)**
- Covers: five dimensions of developer productivity — Satisfaction & well-being, Performance,
  Activity, Communication & collaboration, Efficiency & flow.
- Invoke when: someone proposes a single productivity metric (commits, PRs, story points).
- Misreading: building a 30-metric dashboard. Pick at least three dimensions, a few metrics each.

**DevEx (Noda, Storey, Forsgren, Greiler, 2023)**
- Covers: developer experience through feedback loops, cognitive load and flow state.
- Invoke when: lead time is fine on paper but engineers report friction (slow builds, waiting on
  environments, interruptions).
- Misreading: treating survey scores as optional "soft" data; perception data finds waits that
  system data misses.

**Little's Law and flow metrics (Kanban Method)**
- Covers: average lead time = average WIP ÷ average throughput in a stable system; work item age,
  cycle time percentiles.
- Invoke when: decomposing lead time — queues in front of review, test and deploy are where time goes.
- Misreading: applying it to an unstable system (arrivals ≫ departures); fix WIP first.

## Structure

**Team Topologies (Matthew Skelton & Manuel Pais, 2019)**
- Covers: four team types (stream-aligned, platform, enabling, complicated-subsystem), three
  interaction modes (collaboration, X-as-a-service, facilitating), cognitive load as a design limit.
- Invoke when: splitting/merging teams, creating a platform team, or when every change needs
  several teams.
- Misreading: renaming existing teams to the four types without changing ownership or interaction modes.

**Conway's Law (Melvin Conway, 1968) and the inverse Conway manoeuvre**
- Covers: systems mirror the communication structure of the organisation that builds them.
- Invoke when: team boundaries and service boundaries disagree. Pair with `sse-architect`.
- Misreading: reorganising to fix architecture without changing the architecture plan, or vice versa.

**Spans and layers (Will Larson, *An Elegant Puzzle*, 2019; common industry heuristics)**
- Covers: sizing teams and manager spans; when to add managers and a director layer.
- Invoke when: managers have no time for 1:1s, reviews and hiring, or ICs have no dedicated manager.
- Misreading: treating ranges as rules. They are heuristics; context (seniority, remote, on-call) shifts them.

## Production discipline

**Google SRE book (2016) and SRE Workbook (2018)**
- Covers: SLOs and error budgets, on-call load limits, blameless postmortems, toil reduction,
  release engineering.
- Invoke when: on-call is concentrated in a few people, incidents repeat, or release cadence is erratic.
- Misreading: copying Google-scale practices wholesale. Adopt the principle (budget, blameless,
  bounded toil) at the team's scale.

**Incident Command System, adapted for software (e.g. PagerDuty Incident Response guide)**
- Covers: incident roles (commander, communications, operations/subject experts), severity levels,
  escalation and handover.
- Invoke when: incidents are run by whoever is loudest, or customers learn about outages first.
- Misreading: heavyweight process for every page. Severity decides how much of the structure is used.

## Hiring

**Structured interviewing and work samples (Schmidt & Hunter, 1998, and later meta-analyses)**
- Covers: evidence that structured interviews and work-sample tests predict job performance better
  than unstructured interviews.
- Invoke when: designing or debugging the interview loop (low onsite → offer conversion, inconsistent
  decisions).
- Misreading: quoting exact validity coefficients as settled — later re-analyses revised them; the
  ordering (structured > unstructured) is what matters.

**Funnel conversion analysis (recruiting practice)**
- Covers: stage-by-stage conversion, time in stage, offer-accept rate; required top-of-funnel volume
  = hires ÷ end-to-end conversion.
- Invoke when: "we can't find engineers" or hiring targets are set without pipeline math.
- Misreading: optimising the whole funnel at once; fix the leakiest stage first.
