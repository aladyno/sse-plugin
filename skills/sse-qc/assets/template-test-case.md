# Template — `test-case`

Locked format for `sse-qc --mode test-case` (`.md` file, validated by
[`../scripts/check_locked_format.py`](../scripts/check_locked_format.py) `--mode test-case`).
Keep the **English headings** exactly — the validator matches them literally; body text may be in
the user's language. Rules: [`../SKILL.md` → Modes](../SKILL.md#modes). Filled example:
[`../references/worked-examples.md`](../references/worked-examples.md) §5; full sample:
[`sample-test-case.md`](sample-test-case.md).

Every case traces to a flow or condition in the source. Minimum coverage where relevant: happy
path, negative/invalid input, boundary, permission/role, third-party integration,
currency/timezone/localisation, regression for linked bugs. High-risk scope (money, security,
personal data, data loss, Blocker/Critical) → at least one Security and one Boundary case per
money/identity flow. Rules the sources do not support → labelled assumption under "Not covered".

```markdown
# Test Case — <ticket key / feature name>

| ID | Flow / Function | Type | Technique | Precondition | Steps | Test Data | Expected Result | Priority |
|---|---|---|---|---|---|---|---|---|
| TC-01 | ... | Positive | EP | ... | 1. ...<br>2. ... | ... | ... | P0 |

Type ∈ {Positive, Negative, Boundary, Edge, Security, Accessibility, Regression}. Technique ∈ {EP, BVA, Decision table, State transition, Pairwise, Error guessing, Exploratory}. Priority ∈ {P0, P1, P2} from risk level (P0 = blocks release if it fails).

## Not covered
- <axis/case not writable because the source lacks information — reason + proposed handling (e.g. assume a threshold, label it, confirm with PO)>
```

"Not covered" is mandatory; if everything is covered write "No axis left uncovered."
