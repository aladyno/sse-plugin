# Data governance & data-asset standards — deeper notes

Read on demand. For each: what it covers, when to invoke it, and how it is commonly misread.
Cite by name; never invent clause numbers or quotes. This is decision vocabulary, not certification
or legal advice.

## Governance and management

**DAMA-DMBOK2 (DAMA International, *Data Management Body of Knowledge*, 2nd ed.)**
- Covers: the data management knowledge areas (governance, architecture, modelling, storage,
  security, integration, documents, reference & master data, warehousing & BI, metadata, quality)
  with governance at the centre.
- Invoke when: a data initiative has no named owner or steward, or a plan covers one area (e.g. a
  new warehouse) while ignoring metadata, quality and ownership.
- Misreading: treating it as a maturity checklist to complete. It is a map; pick the areas that
  block the decision on the table.

**ISO/IEC 38505-1 (governance of data)**
- Covers: applying the ISO/IEC 38500 governance model (Evaluate–Direct–Monitor) to data — value,
  risk and constraints across the data lifecycle.
- Invoke when: leadership must approve collecting, sharing or monetising data and needs a framing
  that assigns accountability and a monitoring measure.
- Misreading: assuming it prescribes controls. It sets governance responsibilities; controls come
  from security/privacy standards.

**DCAM — Data Management Capability Assessment Model (EDM Council)**
- Covers: a capability/maturity model for data management programmes.
- Invoke when: someone proposes buying a platform to fix what is really a capability gap (no owners,
  no definitions, no quality process).
- Misreading: chasing a maturity score. Use it to find the one capability that blocks the next decision.

## Rights, privacy and de-identification

**GDPR (Regulation (EU) 2016/679)**
- Covers: lawful bases for processing, purpose limitation, data minimisation, data subject rights
  (including rights around solely automated decisions), data protection by design, DPIAs for
  high-risk processing, controller vs processor responsibilities, international transfers.
- Invoke when: filling the **Rights** cell for personal data — especially a new purpose such as
  model training, sharing with partners, or a data product.
- Misreading: "it is in our ToS so we have consent". Consent must be specific and freely given;
  other bases (contract, legitimate interest) have their own tests. A new purpose needs its own check.

**ISO/IEC 27701 (privacy information management, extension to ISO/IEC 27001/27002)**
- Covers: PII controller and processor controls, records of processing, privacy roles.
- Invoke when: privacy decisions are made ad hoc and need to become a managed, auditable system.
- Misreading: equating certification with lawful processing. It manages privacy; it does not make a
  given purpose lawful.

**ISO/IEC 20889 (privacy-enhancing data de-identification terminology and techniques)**
- Covers: de-identification techniques (suppression, generalisation, randomisation, pseudonymisation,
  formal models such as k-anonymity and differential privacy) and their properties.
- Invoke when: anyone says "anonymised" before external sharing or productisation.
- Misreading: pseudonymised data is still personal data in most regimes; a technique without a
  measured residual risk is a label, not a guarantee.

**NIST Privacy Framework 1.0**
- Covers: privacy risk management organised as Identify, Govern, Control, Communicate, Protect.
- Invoke when: engineering teams need privacy expressed as data-processing actions and outcomes.
- Misreading: using it as a legal compliance test; it is a risk-management structure.

**EU AI Act (Regulation (EU) 2024/1689) — data governance for high-risk AI**
- Covers: obligations on training, validation and testing data for high-risk AI systems
  (relevance, representativeness, bias examination, documentation).
- Invoke when: customer or personal data feeds a model whose use case may be high-risk. Pair with
  `sse-caio` for the tier itself.
- Misreading: "only applies to EU companies". It applies by market placement and use of output in
  the EU. Application dates are phased — verify the current ones.

## Quality, architecture and value

**ISO/IEC 25012 (data quality model) / ISO 8000 (data quality)**
- Covers: data quality characteristics (accuracy, completeness, consistency, credibility,
  currentness, …) and master-data quality exchange.
- Invoke when: a decision depends on data whose fitness was never measured.
- Misreading: aiming for "high quality" in general. Name the characteristics this decision needs.

**Data Mesh (Zhamak Dehghani)**
- Covers: four principles — domain ownership, data as a product, self-serve data platform,
  federated computational governance.
- Invoke when: many domains consume data and the central team is the bottleneck.
- Misreading: adopting the label with only a central platform team. Without domain owners and
  federated governance it is a re-branded warehouse with extra cost.

**FAIR principles (Findable, Accessible, Interoperable, Reusable)**
- Covers: properties that make data reusable by people and machines.
- Invoke when: defining what "data product" means for internal or external consumers.
- Misreading: FAIR ≠ open. Data can be FAIR and access-controlled.

**Infonomics (Doug Laney)**
- Covers: treating information as an asset — valuation approaches (cost, market, use/economic value).
- Invoke when: valuing a corpus for productisation, fundraising or M&A.
- Misreading: valuing by volume. Value follows use, exclusivity and the decisions or revenue the
  data supports — minus the contractual and regulatory constraints on it.
