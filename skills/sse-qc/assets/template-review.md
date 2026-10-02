# Template — `review` (requirement gap analysis)

Locked format for `sse-qc --mode review` (inline). Headings may be translated; the structure may
not. Rules and when to use: [`../SKILL.md` → Modes](../SKILL.md#modes). Filled examples:
[`../references/worked-examples.md`](../references/worked-examples.md) §2–3; full sample:
[`sample-review.md`](sample-review.md).

The gate before code: every issue carries reasoning and a resolution. Scan seven axes; an axis
with no evidence is skipped, never forced.

1. **Ambiguous** — readable in two or more ways.
2. **Missing AC** — behaviour described without a measurable "done".
3. **Missing negative/edge cases** — happy path only; invalid, empty, over-limit, concurrent not covered.
4. **Contradiction** — two parts of the source disagree, or the latest comment (task or any
   sub-task) contradicts the description.
5. **Missing NFR** — performance, security, privacy, localisation, accessibility, rollback; only
   when the change signals it (ISO/IEC 25010 as the checklist).
6. **Untestable** — subjective wording ("faster", "user-friendly") with no threshold.
7. **Contradicts as-is** — conflicts with current behaviour in code, tests or docs; requires a
   cited source (`file:line` allowed here), otherwise skip the axis.

```
## Review & Gap Analysis — <ticket key or document name>

### Requirement summary (1–2 sentences, as the source states it)

### Issues found

#### #<n> — <Ambiguous | Missing AC | Missing negative/edge | Contradiction | Missing NFR | Untestable | Contradicts as-is> — <short title>
- **Quote / location:** "..."
- **Reasoning (why it matters, risk if ignored):** ...
- **Proposed resolution:** <one real direction: most reasonable reading, default value, measurable threshold>
- **Needs confirmation:** Yes/No — from **BA/PO** (business decision) and/or **QC** (how to test it), with the exact question

(No issues at all → "No significant gaps found" plus one sentence why.)

### Summary & recommendation
- Blocking (decide before code) vs non-blocking issues, with reasons.
- Readiness for development: clear enough / significant gaps.
```
