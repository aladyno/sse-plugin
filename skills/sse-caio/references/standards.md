# AI governance & AI investment standards — deeper notes

Read on demand. For each: what it covers, when to invoke it, and how it is commonly misread.
Cite by name; never invent clause numbers or quotes. This is decision vocabulary, not certification,
conformity assessment or legal advice.

## Management systems and risk

**ISO/IEC 42001:2023 (AI management system)**
- Covers: requirements for an AI management system — AI policy, roles, AI risk assessment and
  treatment, AI system impact assessment, lifecycle and third-party controls, continual improvement.
- Invoke when: AI moves from one experiment to several production features and needs owners,
  review points and evidence.
- Misreading: certification as the goal. For a small portfolio, adopt the structure (policy, owner,
  impact assessment per use case) long before any audit.

**ISO/IEC 23894:2023 (AI — guidance on risk management)**
- Covers: applying the ISO 31000 process (identify, analyse, evaluate, treat, monitor) to
  AI-specific risk sources (data, model behaviour, autonomy, lifecycle changes).
- Invoke when: a risk discussion lists fears without likelihood, consequence or treatment.
- Misreading: a one-off assessment. Model and data changes re-open the risk.

**NIST AI Risk Management Framework 1.0 (NIST AI 100-1) + Generative AI Profile (NIST AI 600-1)**
- Covers: four functions — Govern, Map, Measure, Manage — and trustworthiness characteristics
  (valid and reliable, safe, secure and resilient, accountable and transparent, explainable,
  privacy-enhanced, fair). The GenAI profile adds risks such as confabulation, information
  integrity and harmful content.
- Invoke when: structuring evals and controls; answering enterprise customer questionnaires.
- Misreading: voluntary means optional in practice — enterprise buyers increasingly ask for it.

## Regulation

**EU AI Act (Regulation (EU) 2024/1689)**
- Covers: prohibited practices; high-risk systems (product-safety components and listed use cases
  such as employment, education, credit, essential services, law enforcement, migration, biometrics)
  with risk management, data governance, documentation, logging, human oversight, accuracy and
  robustness obligations; transparency duties (chatbots, generated content); general-purpose AI
  model obligations.
- Invoke when: users or affected people are in the EU, or outputs are used there.
- Misreading: classifying by technology ("it's just an LLM") instead of by use case; assuming one
  application date — obligations are phased; verify the current dates.

**US federal/state measures (non-exhaustive, change often)**
- Covers: e.g. NYC Local Law 144 (automated employment decision tools — bias audit, notice),
  Colorado AI Act (SB 24-205, high-risk consumer decisions), Illinois AI Video Interview Act and
  BIPA, sector rules (credit adverse-action notices, insurance, health).
- Invoke when: the use case makes or supports consequential decisions about people in those places.
- Misreading: treating a list as complete. Always confirm the current state with counsel.

## Documentation and engineering practice

**Model Cards (Mitchell et al., 2019) and Datasheets for Datasets (Gebru et al., 2018/2021)**
- Covers: intended use, out-of-scope use, evaluation by relevant slices, limitations; dataset
  motivation, composition, collection, consent and maintenance.
- Invoke when: shipping a model-backed feature or fine-tune — the card is where the eval lives.
- Misreading: writing them after launch as marketing. They are the eval and scope contract.

**"Hidden Technical Debt in Machine Learning Systems" (Sculley et al., NeurIPS 2015)**
- Covers: ML-specific debt — entanglement, undeclared consumers, data dependencies, feedback loops,
  configuration debt.
- Invoke when: a fine-tune or in-house model is proposed; count the surrounding system, not the model.
- Misreading: "applies only to classic ML". Prompt pipelines, RAG indexes and agent configs carry
  the same data and config debt.

**Wardley Mapping (Simon Wardley)**
- Covers: placing components on an evolution axis (genesis → custom → product → commodity).
- Invoke when: build vs buy for models, vector stores, eval tooling, inference platforms.
- Misreading: building what is already commodity because the team finds it interesting.

**FinOps Framework (FinOps Foundation)**
- Covers: cloud cost management — inform, optimise, operate; unit economics; cost allocation.
- Invoke when: AI cost per request/feature is unknown, or a self-host migration is proposed.
- Misreading: optimising rates (GPU price) before usage (caching, routing, prompt length).

**OWASP Top 10 for LLM Applications**
- Covers: common LLM application risks (prompt injection, sensitive information disclosure,
  supply chain, excessive agency, …).
- Invoke when: naming a security gap to hand off — the threat model belongs to `sse-security`.
- Misreading: treating the list as an AI governance programme; it is a security checklist.

**OECD AI Principles**
- Covers: inclusive growth, human-centred values, transparency, robustness, accountability.
- Invoke when: drafting an AI policy or external commitments; many regulations reuse this vocabulary.
- Misreading: citing principles instead of measurable controls.
