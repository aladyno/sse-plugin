# Template — `checklist`

Locked format for `sse-qc --mode checklist` (inline; written as a file, and validated by
[`../scripts/check_locked_format.py`](../scripts/check_locked_format.py) `--mode checklist`, when
it exceeds ~25 checkboxes or 5 regression areas). Keep the **English headings** exactly in a
file. Rules: [`../SKILL.md` → Modes](../SKILL.md#modes). Filled example:
[`../references/worked-examples.md`](../references/worked-examples.md) §6; full sample:
[`sample-checklist.md`](sample-checklist.md).

Short checkboxes grouped by stage; not a copy of the test cases. Unknown items →
`- [ ] [NEEDS CONFIRMATION] <item>` instead of an invented checkbox. Regression names the
concrete areas affected.

```markdown
## QC Checklist — <ticket key / release>

### Pre-deploy
- [ ] ...

### Functional smoke
- [ ] ...

### Regression (affected areas)
- [ ] ...

### Data/Config
- [ ] ...

### Rollback
- [ ] Rollback plan exists / revert method confirmed.

### Sign-off
- [ ] QA sign-off
- [ ] PO sign-off (if required)
```
