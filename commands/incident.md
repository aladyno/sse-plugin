---
description: Triage a production issue (mitigate first, then root cause) or write a blameless postmortem
argument-hint: "<symptom, error, alert or 'postmortem <summary>'>"
---

# Incident

Input: $ARGUMENTS

1. Collect evidence the user provided (errors, stack traces, logs, metrics screenshots, timeline). Ask for the single most useful missing piece if nothing actionable is given.
2. Check recent changes in the repo (`git log --since="3 days ago"`, recent config/deploy changes).
3. Delegate to the `ag-sse-sre` agent (incident mode). If the root cause is in code, use `ag-sse-implementer` for the fix only after mitigation is agreed.
4. Output:
   - Triage: impact · likely cause (with confidence) · immediate mitigation · verification steps
   - Postmortem (if requested): summary · impact · timeline · root cause (5 Whys) · what went well/poorly · action items

Never execute mutations against production; propose the commands.
