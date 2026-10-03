---
description: Executive review of a plan by one C-level advisor (forcing questions, helper-script numbers, green/yellow/red verdict)
argument-hint: "<role> <plan, decision or question>   role: cfo|cro|cxo|cmo|cpo|coo|chro|ciso|gc|cdo|caio|vpe"
---

# Exec — single executive review

Input: $ARGUMENTS

1. Split the input into `<role>` (first word) and `<plan>` (the rest).
   - `<role>` missing or not in the list → if the plan clearly maps to one role, say which and continue; if it spans several, suggest `/sse-plugin:boardroom` and stop; otherwise ask which role and stop.
   - `ceo`, `cto`, `cso`, `cco` have no review agent → tell the user to call the entity `sse-<role>` instead and stop.
   - `<plan>` empty → ask what plan or decision to review and stop.
2. Delegate to the `ag-sse-<role>` agent with the plan, everything relevant already in the conversation (numbers, constraints, dates) and the paths of any data files the user named.
3. Present its output: bottom line → numbers (each with its source or "N/A — needs data") → verdict 🟢/🟡/🔴 with conditions → next actions → the decision the user owns.
4. Missing inputs block the verdict → list exactly which numbers are needed and from where; never fill them in.
5. Next step: decision spans other roles → `/sse-plugin:boardroom`; decision taken → offer `/sse-plugin:decide`.

Respond in the user's language, following [shared/communication-standard.md](../shared/communication-standard.md) §6.
