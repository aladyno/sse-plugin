---
description: Tech-debt audit, dependency upgrade plan or safe refactor plan for a module or the whole repo
argument-hint: "[path | 'deps' | 'refactor <module>'] (default: whole repository)"
---

# Maintain

Scope: $ARGUMENTS

1. Delegate to the `ag-sse-maintainer` agent with the scope.
2. Present: debt register → ordered roadmap → first safe step.
3. If the user picks items to execute, hand them one at a time to `ag-sse-implementer`, followed by `/sse-plugin:review`.
