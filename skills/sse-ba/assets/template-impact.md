# Template — `impact` (business impact of a rule change)

Locked format for `sse-ba --mode impact`. Headings may be translated; the structure may not.
Rules and when to use: [`../SKILL.md` → Modes](../SKILL.md#modes). Filled example:
[`../references/worked-examples.md`](../references/worked-examples.md) §5.

Business level, not code level (code blast radius → `sse-maintainer`). Use the project's own
bounded contexts/modules as rows when a domain map exists; otherwise the generic areas below.
Every row is answered — "No" carries a one-line reason so the reader knows it was considered.

```
## Business Impact — <proposed change>

### The change (1–2 sentences)

### Impact by area
| Area | Affected | Detail | As-is source |
|---|---|---|---|
| Calculations & money (prices, fees, refunds, rounding) | Yes/No | ... | ... |
| Business rules & policies | ... | ... | ... |
| Customer-facing flows & UI | ... | ... | ... |
| State lifecycle (statuses, cancellation, reversal) | ... | ... | ... |
| Integrations & third parties | ... | ... | ... |
| Reporting, finance & reconciliation | ... | ... | ... |
| Notifications & communications | ... | ... | ... |
| Security, privacy & compliance | ... | ... | ... |
| Operations & support | ... | ... | ... |
| Existing data & migration | ... | ... | ... |

### What each stakeholder sees differently
- Customer: ... / Operations: ... / Finance: ... / Partners: ...

### Highest risk & recommendation
- ... (BA proposal, pending decision)

### Sources checked
- ...

BA Output: <≤ 25 words>
```
