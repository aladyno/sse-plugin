# chat — copy-ready templates

Fill `[brackets]` with real facts only; leave unknowns as placeholders and list them as missing.
Translate headings into the receiver's language; keep the structure.

## 1. Technical limitation / schedule risk (dev → planner/PO)

```
Context: [what was requested and why it matters]
Issue: [what blocks it] — because [technical reason in plain terms]
Options:
  A) [option] — effort [x], impact [schedule/business/user]
  B) [option] — effort [x], impact [...]
  C) [option] — effort [x], impact [...]
Recommendation: [A/B/C] because [one line]
Decision needed from: [person] by [YYYY-MM-DD TZ] — after that, [what slips]
```

## 2. Bug report (QA → dev)

```
Summary: [one line: what is wrong, where]
Environment: [env / build / browser / account type]
Steps to reproduce:
  1. [...]
  2. [...]
Expected: [...]
Actual: [...] (evidence: [screenshot / log / request id])
Scope: [who/what is affected — users, vendors, % traffic, data]
Reproducibility: [always / x of y / once]
Priority: [P1–P4] because [blocks release / money at risk / workaround exists]
```

## 3. Requirement hand-off (planner → dev/QA)

```
Why: [business goal + metric it moves]
Who: [user / partner affected]
What: [the change, in user terms]
Preconditions & constraints: [dependencies, data, vendor limits, deadlines]
Acceptance criteria:
  - Given [...] When [...] Then [...]
Out of scope: [...]
Open questions: [owner — by date]
```

## 4. Paraphrase-confirm (receiver → sender)

```
Let me confirm I understood correctly:
1. Goal: [...]
2. You want me to: [...] using [approach]
3. By: [date]
Not clear to me yet: [specific point]
Is this correct?
```

## 5. Acknowledge (can't answer yet)

```
Received — I'll reply by [YYYY-MM-DD TZ].
```

## 6. Status update (async)

```
[Ticket/feature] — status: [on track / at risk / blocked]
Done: [...]
Next: [...] by [date]
Risk/blocker: [what] — need [who] to [what] by [date]
```
