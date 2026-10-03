---
description: Record a decision the user has taken — chosen option, rejected options, binding success/kill criteria, preserved dissent, review date
argument-hint: "<board memo path, or the decision in words>"
---

# Decide

Input: $ARGUMENTS

1. **Source** — a memo path → read it; otherwise use the decision stated in the input and the conversation (e.g. a `/sse-plugin:boardroom` memo just presented).
2. **Gate** — record only a decision the **user** has taken. No explicit choice yet → restate the options and ask which one is chosen; stop.
3. **Build the record** (show it before writing):

   ```markdown
   # Decision: <title>
   **Decided:** YYYY-MM-DD · **By:** <who decided> · **Review checkpoint:** YYYY-MM-DD (default +90 days)
   **Memo / brief:** <links, if any>

   ## Decision
   **Chose:** <option> · **Rejected:** <each other option + one-line why>

   ## Success criteria (binding)
   - <metric, threshold, date>

   ## Kill criteria (binding)
   - <state and date that stops this, and the action taken then>

   ## Preserved dissent
   - **<role/person>:** <concern, verbatim — never summarised away>

   ## Status history
   - YYYY-MM-DD: APPROVED
   ```

   A missing success or kill criterion stays as a visible `TODO: <what is needed>` — never invented.
4. **Write** — offer `docs/decisions/YYYY-MM-DD-<slug>.md` (or the repo's existing decision/ADR location and numbering). Write only after the user agrees; if the memo file exists, also set its status to `APPROVED` with a link to the record.
5. Next step: execution plan → `/sse-plugin:sse`; irreversible change → name the one-way step and its rollback limits.

Respond in the user's language, following [shared/communication-standard.md](../shared/communication-standard.md) §6.
