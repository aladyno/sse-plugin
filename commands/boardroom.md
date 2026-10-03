---
description: Multi-role executive deliberation — independent advisor positions, cross-examination, devil's advocate, board memo with dissent
argument-hint: "<decision question or path to a brief>"
---

# Boardroom

Decision: $ARGUMENTS

1. **Brief** — if the input is a file path, read it. Empty or no decision in it (only a topic) → ask what is being decided, the options and the deadline (≤ 3 questions) and stop.
2. **Route** — delegate to `ag-sse-chief-of-staff` (Mode 1) to pin the decision and pick the panel (2–5 roles). If it returns a single advisor, run `/sse-plugin:exec <role>` logic instead and stop. Show the panel and options to the user in 3–5 lines.
3. **Independent positions** — run the panel's `ag-sse-<role>` agents **in parallel**, each with the same brief and facts and **without** the other advisors' positions (isolation prevents anchoring). Each returns: vote (option), verdict 🟢/🟡/🔴, top 3 concerns, top 3 supports, missing data.
4. **Synthesize** — pass all positions to `ag-sse-chief-of-staff` (Mode 2) for the board memo: tally, cross-examination, devil's-advocate concerns, recommendation, success and kill criteria. An advisor that failed or returned no position is listed as such, never silently dropped.
5. **Present** the memo. The user decides; never record a decision on their behalf.
6. Offer to save the memo as `docs/decisions/boardroom/YYYY-MM-DD-<slug>.md` (or the repo's existing decision/ADR location). Write only after the user agrees. Next step once decided: `/sse-plugin:decide`.

Respond in the user's language, following [shared/communication-standard.md](../shared/communication-standard.md) §6.
