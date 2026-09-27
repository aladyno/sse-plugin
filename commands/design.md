---
description: Turn requirements into a technical design / ADR (options, trade-offs, data model, API, rollout)
argument-hint: "<requirement, ticket or problem statement>"
---

# Design

Requirement: $ARGUMENTS

1. If the requirement is empty or too vague to design (no goal, no user, no constraint), ask up to 3 sharp questions and stop.
2. Delegate to the `ag-sse-architect` agent with the requirement and the relevant parts of the codebase.
3. Present its output: context → options table → decision (ADR) → diagram → risks & open questions.
4. Offer to save the ADR as `docs/adr/NNNN-<slug>.md` (follow the repo's existing ADR location/numbering if one exists). Write only after the user agrees.

Respond in the user's language.
