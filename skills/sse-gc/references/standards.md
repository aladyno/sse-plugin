# Legal-risk standards and market practice — deeper notes

Read on demand. For each: what it covers, when to invoke it, and how it is commonly misread.
Cite by name; never invent statute sections, clause numbers or case law. **Not legal advice** —
this is issue-spotting vocabulary to prepare a conversation with qualified counsel.

## Contracts

**World Commerce & Contracting (WorldCC, formerly IACCM) — "most negotiated terms" research**
- Covers: recurring studies of which terms parties spend most negotiation time on — consistently
  limitation of liability, indemnities, price, and termination.
- Invoke when: deciding where to spend limited negotiation capital.
- Misreading: the most negotiated terms are not always the most important to *this* deal; check
  which loss is most likely here.

**Limitation of liability & indemnity (common commercial practice)**
- Covers: caps (often fees paid/payable over 12 months), exclusions of indirect/consequential loss,
  carve-outs from the cap (IP infringement, confidentiality, data breach, wilful misconduct), "super
  caps" for data-protection losses.
- Invoke when: any MSA, SaaS agreement or vendor contract.
- Misreading: "standard" means the same everywhere; enforceability of exclusions varies by governing
  law — a question for counsel.

## Data protection

**GDPR Art. 28 (processor) · EU Standard Contractual Clauses (Commission Implementing Decision (EU) 2021/914)**
- Covers: mandatory content of controller–processor contracts; SCC modules for transfers outside the EEA.
- Invoke when: the deal moves EU personal data to a processor or a third country.
- Misreading: the DPA alone solves transfers — transfers also need a mechanism (adequacy, SCCs + a
  transfer impact assessment, or another basis).

**CCPA / CPRA (California) · Vietnam Decree 13/2023/ND-CP**
- Covers: California consumer privacy rights and service-provider contract terms; Vietnam personal
  data protection, including impact assessments for processing and for cross-border transfer.
- Invoke when: data subjects are in those jurisdictions.
- Misreading: one global DPA template covers every regime; each adds specific contract and filing duties.

## Financing and equity

**NVCA model legal documents (US) · Y Combinator post-money SAFE**
- Covers: widely used templates for venture financings (term sheet, stock purchase, investor rights,
  voting, ROFR/co-sale) and for early-stage SAFEs.
- Invoke when: reading a term sheet — compare against the template and focus on deviations.
- Misreading: "it's the NVCA form" ≠ founder-friendly; the template contains alternative provisions,
  and which alternative is chosen matters.

**Market norms for key economic terms**
- Covers: 1x non-participating liquidation preference; broad-based weighted-average anti-dilution;
  option pool sizing; 4-year vesting with 1-year cliff; double-trigger acceleration.
- Invoke when: scoring a term sheet's economics.
- Misreading: headline valuation as the only number — a pre-money option pool, participating
  preference or full ratchet can move more value than a valuation change. Run the dilution math with
  `sse-cfo`.

## Intellectual property

**OpenChain — ISO/IEC 5230:2020 · SPDX — ISO/IEC 5962:2021**
- Covers: requirements for an open-source licence compliance programme; a standard format for
  software bill-of-materials and licence data.
- Invoke when: shipping software that includes third-party open source, or answering customer/M&A
  diligence on it.
- Misreading: "open source = free to use any way". Copyleft licences (GPL, AGPL for network use)
  attach obligations depending on how software is distributed or served.

**Paris Convention (12-month priority) · Patent Cooperation Treaty (PCT)**
- Covers: priority right to file in other member countries within 12 months of the first filing; PCT
  route to defer national filings.
- Invoke when: an invention may be patentable and a public disclosure (demo, paper, pitch) is planned.
- Misreading: grace periods are universal — many jurisdictions have no grace period for the
  applicant's own disclosure. File before disclosing; confirm with patent counsel.

**Madrid System (WIPO) for trademarks**
- Covers: one international application designating multiple countries, based on a home filing.
- Invoke when: launching a brand across markets.
- Misreading: a company or domain name registration gives trademark rights — it does not.

## Regulation and compliance

**EU AI Act — Regulation (EU) 2024/1689**
- Covers: risk-tiered obligations (prohibited practices, high-risk systems, transparency duties,
  general-purpose AI models) with phased application dates.
- Invoke when: an AI feature is placed on the EU market or affects people in the EU.
- Misreading: "we only call a model API, so it doesn't apply" — deployers also have obligations.
  Classification is a question for counsel; pair with `sse-caio`.

**PCI DSS v4.0.1**
- Covers: security requirements for cardholder data; enforced through card-brand and acquirer
  contracts rather than statute in most countries.
- Invoke when: payment flows appear in a contract — allocate responsibilities explicitly.
- Misreading: outsourcing to a PSP removes all obligations; the merchant keeps scoped responsibilities.

**ISO 37301:2021 (compliance management systems)**
- Covers: obligations register, risk assessment, controls, monitoring, culture.
- Invoke when: the company needs a repeatable way to track legal obligations as it scales.
- Misreading: a policy library equals compliance; ownership and monitoring do.
