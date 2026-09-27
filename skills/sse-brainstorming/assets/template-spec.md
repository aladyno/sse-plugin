# Template — `architectural` (design spec)

Locked format for `sse-brainstorming --mode architectural`. Headings may be translated; the
structure may not. Rules: [`../SKILL.md` → Modes](../SKILL.md#modes). Self-review:
[`../references/spec-self-review.md`](../references/spec-self-review.md).

Write only after the user approved every design section in chat. The spec records **what was
agreed** — it introduces nothing new. Path: the project's design-spec folder if one exists, else
`docs/specs/YYYY-MM-DD-<topic>-design.md`. Never commit it unless the user asks.

```markdown
# <Topic> — Design

- Date: YYYY-MM-DD · Status: Draft | Approved · Path: architectural
- Related: <tickets, requirements docs, ADRs — or "none">

## 1. Problem & purpose
- What problem, for whom: ...
- Success criteria (observable / measurable): ...

## 2. Goals and non-goals
- Goals: ...
- Non-goals (explicitly out, YAGNI): ...

## 3. Constraints & assumptions
- Constraints (project facts, with source): ...
- ASSUMPTION: ... (owner to confirm)

## 4. Approaches considered
| Approach | Trade-offs | Verdict |
|---|---|---|
| A — ... (recommended) | ... | Chosen because ... |
| B — ... | ... | Rejected because ... |

## 5. Design
### 5.1 Architecture overview
(Prose; optional Mermaid / C4 container-level diagram.)

### 5.2 Units
| Unit | Purpose (one) | Interface (how it is used) | Depends on |
|---|---|---|---|
| ... | ... | ... | ... |

### 5.3 Data flow
...

### 5.4 Error handling
- Failure → expected behaviour: ...

### 5.5 Testing
- What proves it works (levels, key cases): ...

### 5.6 Changes to existing code
- Targeted improvements the work needs (no unrelated refactoring): ...

## 6. Scope & decomposition
- This spec covers: ...
- Later sub-projects (own spec each), in build order: ... (or "none")

## 7. Open questions
- Question — owner — needed by: ...

## 8. Hand-off
- Next: `/sse-plugin:design` (ADR / contracts) | `/sse-plugin:implement`
- Decisions that need an ADR: ...

Brainstorm Output: <≤ 25 words>
```
