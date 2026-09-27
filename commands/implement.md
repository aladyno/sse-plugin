---
description: Implement a feature/fix/refactor in small, test-verified increments following project conventions
argument-hint: "<what to build or fix, or path to a design doc>"
---

# Implement

Task: $ARGUMENTS

1. Confirm the working tree state (`git status`) and the current branch. If on the default branch with a non-trivial change, suggest creating a branch first.
2. If a design/ADR exists for this task, read it. If the task needs a design decision that is not made yet, recommend `/sse-plugin:design` first and stop.
3. Delegate to the `ag-sse-implementer` agent with the task, relevant design and conventions found.
4. Report: change summary · files touched · build/test commands and results · follow-ups.
5. Suggest the next step: `/sse-plugin:review` on the resulting diff.

Do not commit or push unless the user asks.
