# Template — `spec` (user stories + acceptance criteria)

Locked format for `sse-ba --mode spec`. Headings may be translated; the structure may not.
Rules and when to use: [`../SKILL.md` → Modes](../SKILL.md#modes). Filled example:
[`../references/worked-examples.md`](../references/worked-examples.md) §3.

Write only when the request is clear enough, or the user accepts labelled assumptions. Stories
pass INVEST; every AC is a Gherkin scenario a tester can execute without asking; a rule with ≥ 3
interacting conditions gets a decision table (DMN-style, explicit hit policy).

```markdown
# Spec — <ticket key / feature name>

## 1. Context & business value
- Current problem: ... (as-is, with source)
- Who benefits & how it is measured: ...

## 2. Scope
- In scope: ...
- Out of scope: ...

## 3. User stories
> US-01 — As a <role>, I want <behaviour>, so that <value>.

## 4. Business rules
| # | Rule | Origin (as-is kept / NEW / CHANGED from as-is) | Source |
|---|---|---|---|
| BR-01 | ... | ... | ... |

(Decision table here when a rule combines several conditions.)

## 5. Acceptance criteria
### US-01
- AC-01: Given ... When ... Then ...

## 6. Assumptions & open questions
- ASSUMPTION: ... (owner, pending)
- Question: ... (ask whom)

## 7. Related business impact (summary)
- <area>: ... (run `--mode impact` for detail)

## 8. Technical references (for developers)
- Tables / fields / services / endpoints involved: ... [source]

## Sources checked
- ...

BA Output: <≤ 25 words>
```
