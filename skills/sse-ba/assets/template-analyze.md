# Template — `analyze` (requirement analysis)

Locked format for `sse-ba --mode analyze`. Headings may be translated; the structure may not.
Rules and when to use: [`../SKILL.md` → Modes](../SKILL.md#modes). Filled example:
[`../references/worked-examples.md`](../references/worked-examples.md) §2.

Gap types: `Ambiguous` · `Conflicts with as-is` · `Missing rule` · `Blind spot` (from the
blind-spot checklist) · `No business value stated` · `Not verifiable` (fails ISO/IEC/IEEE 29148).

```
## Business Analysis — <ticket key or request name>

### 1. What is requested (in the source's own words, 2–3 sentences)

### 2. Current behaviour (as-is)
- <fact> — [source: <file:line | doc § | ticket comment>]
(facts with sources only; unknown → "ASSUMPTION — needs confirmation")

### 3. Gaps found

#### #<n> — <gap type> — <short title>
- **Evidence:** "<quote from request>" ↔ as-is: <fact> [source]
- **Reasoning (why it matters, risk if ignored):** ...
- **BA proposal:** <one real direction>
- **Decide with:** <PO | business stakeholder | tech lead> — "<the exact question>"

### 4. Conclusion
- Blocking (decide before spec/code) vs non-blocking gaps.
- Readiness: ready for spec / significant gaps remain.
- Next step (e.g. `--mode spec` after #1 and #3 are decided).

### Sources checked
- <list>

BA Output: <≤ 25 words>
```
