# Template — `test-plan`

Locked format for `sse-qc --mode test-plan` (`.md` file, validated by
[`../scripts/check_locked_format.py`](../scripts/check_locked_format.py) `--mode test-plan`).
Keep the **English headings** exactly — the validator matches them literally; body text may be in
the user's language. Rules: [`../SKILL.md` → Modes](../SKILL.md#modes). Filled example:
[`../references/worked-examples.md`](../references/worked-examples.md) §4; full sample:
[`sample-test-plan.md`](sample-test-plan.md).

Fill only what the source supports; unknown items read "needs confirmation from PO/dev/lead" —
no invented dates or environments. Structure aligned with ISO/IEC/IEEE 29119-3. §6 is a risk
register (likelihood × impact), not prose; high-risk scope must name a concrete risk there.

```markdown
# Test Plan — <ticket key / feature name>

## 1. Scope
- In scope: ...
- Out of scope: ...

## 2. Test objectives
...

## 3. Test strategy
- Functional: ... (techniques)
- Regression (if existing flows are touched): ...
- Integration (third parties / other services, if any): ...
- Non-functional (only if signalled — ISO/IEC 25010 characteristics): ...
- Exploratory (charters, if risk is uncertain): ...

## 4. Environment & test data
...

## 5. Entry / Exit criteria
- Entry: ...
- Exit: ...

## 6. Risks & mitigation
| Risk | Likelihood | Impact | Level | Mitigation |
|---|---|---|---|---|

## 7. Roles & schedule (only if sourced, otherwise "needs confirmation")
...

## 8. Deliverables
- Test case list, test results, defect reports, ...
```
