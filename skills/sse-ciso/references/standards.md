# Security-programme standards — deeper notes

Read on demand. For each: what it covers, when to invoke it, and how it is commonly misread.
Cite by name; never invent clause numbers or quotes. This is gap-analysis vocabulary, not
certification or audit.

## Quantifying and treating risk

**FAIR — Factor Analysis of Information Risk (Jack Jones; The Open Group O-RT risk taxonomy and O-RA risk analysis)**
- Covers: risk as probable frequency × probable magnitude of future loss, decomposed into threat
  event frequency, vulnerability, primary and secondary loss; estimates as calibrated ranges.
- Invoke when: someone needs security risk in money to compare with control cost or other spend.
- Misreading: treating FAIR output as precise. Its value is explicit assumptions and ranges that can
  be challenged; a single point estimate defeats the purpose.

**ALE = SLE × ARO (classic quantitative risk analysis)**
- Covers: single-loss expectancy × annual rate of occurrence = annualised loss expectancy.
- Invoke when: a quick first-pass ranking is needed and FAIR is too heavy.
- Misreading: averaging away tail risk — a rare event that ends the company needs a separate
  "can we survive the worst case?" check, not just its ALE.

**ISO/IEC 27005:2022 (information security risk management)**
- Covers: the risk process aligned with ISO 31000 — context, identification (event- or asset-based),
  analysis, evaluation, treatment (modify, retain, avoid, share), monitoring.
- Invoke when: establishing or reviewing the risk-management process behind an ISMS.
- Misreading: building a huge asset × threat matrix nobody maintains. Event-based scenarios on the
  crown jewels are allowed and usually more useful.

**NIST SP 800-30 Rev.1 (guide for conducting risk assessments)**
- Covers: threat sources, events, vulnerabilities, likelihood and impact, with assessment tiers
  (organisation, mission/business process, system).
- Invoke when: a documented, repeatable assessment method is needed, e.g. for US public-sector clients.
- Misreading: stopping at qualitative heat maps; the method allows semi-quantitative and quantitative scales.

## Programme frameworks and control sets

**NIST Cybersecurity Framework (CSF) 2.0 (2024)**
- Covers: six functions — Govern, Identify, Protect, Detect, Respond, Recover — with categories and
  outcome-based subcategories; profiles (current vs target) and implementation tiers.
- Invoke when: assessing programme coverage or presenting maturity to leadership.
- Misreading: aiming for the highest tier everywhere. Target profiles should follow the risk register.

**ISO/IEC 27001:2022 + ISO/IEC 27002:2022**
- Covers: requirements for an ISMS (clauses 4–10) and the Annex A reference control set (93 controls
  in four themes), with implementation guidance in 27002.
- Invoke when: customers or markets require certification, or a structured control baseline is wanted.
- Misreading: implementing every Annex A control. Selection is risk-based and justified in the
  Statement of Applicability.

**SOC 2 (AICPA Trust Services Criteria)**
- Covers: attestation report on controls for security (mandatory) plus optional availability,
  processing integrity, confidentiality and privacy criteria. Type I = design at a point in time;
  Type II = operating effectiveness over a period.
- Invoke when: selling to US/enterprise B2B buyers whose questionnaires ask for it.
- Misreading: "SOC 2 certified" — it is an auditor's attestation, not a certification; and Type II
  needs an observation window, so start the clock early.

**CIS Critical Security Controls v8 (Implementation Groups IG1–IG3)**
- Covers: prioritised safeguards; IG1 is the essential cyber-hygiene baseline.
- Invoke when: deciding what to do first with little budget.
- Misreading: skipping IG1 to buy advanced tooling.

**NIST SP 800-207 (Zero Trust Architecture)**
- Covers: no implicit trust from network location; per-session, per-resource access decisions by a
  policy engine using identity, device and context.
- Invoke when: setting the multi-year architecture direction.
- Misreading: buying a "zero trust product". It is a direction; sequence identity → device →
  segmentation → data.

## Incident readiness and regulatory clocks

**NIST SP 800-61 (computer security incident handling) · ISO/IEC 27035**
- Covers: incident lifecycle — preparation, detection and analysis, containment, eradication and
  recovery, post-incident activity (800-61 Rev.3, 2025, aligns this with CSF 2.0).
- Invoke when: building or testing the IR capability; deciding roles (incident commander, legal, comms).
- Misreading: a runbook on a wiki counts as readiness. Only exercised plans count.

**GDPR Art. 33 / 34 · HIPAA Breach Notification Rule · Vietnam Decree 13/2023/ND-CP**
- Covers: personal-data breach notification to authorities (GDPR: within 72 hours of awareness where
  feasible) and to data subjects when high risk; HIPAA: notification without unreasonable delay and no
  later than 60 days from discovery; Decree 13: notification to the authority within 72 hours.
- Invoke when: mapping regulatory clocks per market before an incident happens.
- Misreading: the clock starts at investigation completion — it starts at awareness/discovery.
  Exact obligations are legal questions → `sse-gc` and counsel.

**ISO 22301 (business continuity management)**
- Covers: business-impact analysis, RTO/RPO, continuity strategies, exercising.
- Invoke when: ransomware or outage scenarios dominate the risk register.
- Misreading: "we have backups" = recoverable. Only a timed restore test proves RTO.

## Third-party risk

**ISO/IEC 27036 · Shared Assessments SIG · CSA CAIQ / STAR**
- Covers: supplier-relationship security; standard questionnaires for vendor due diligence.
- Invoke when: tiering vendors and sizing assessment depth.
- Misreading: questionnaire = assurance. Weight evidence (SOC 2 report, pen-test summary) over
  self-attestation for tier-1 vendors.

**PCI DSS v4.0.1**
- Covers: requirements for entities that store, process or transmit cardholder data.
- Invoke when: card data is in scope; first question is always how to shrink scope.
- Misreading: applying it to systems that never touch card data — scoping is the main lever.
