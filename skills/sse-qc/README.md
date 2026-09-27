# sse-qc

QA/QC expert entity (hybrid tier) for the sse-plugin. It reads a requirement source — a
ticket via an issue-tracker tool, or a pasted BRD/SRS/spec — and, using **risk-based testing**
and internationally recognised practice (ISO/IEC/IEEE 29119, ISTQB test techniques,
ISO/IEC 25010, OWASP WSTG, WCAG 2.2), produces one of:

- `diag` — 3 most expensive QA blind spots + 1 decisive question (≤ 200 words, inline)
- `review` — requirement gap analysis (inline)
- `test-plan` — test strategy document (`.md` file, validated)
- `test-case` — detailed test cases with the technique used per case (`.md` file, validated)
- `checklist` — short pre-release / regression checklist (inline, or a validated file when long)

It writes documents only: no test code, no test runs, no writes to external systems without
explicit confirmation. See [SKILL.md](SKILL.md) for the full behaviour and the
[Expert Entity Contract](../../shared/expert-entity-contract.md) it follows.

## How to use

Slash-only — invoke it by name:

```
/sse-plugin:sse-qc                              # diag on the current discussion
/sse-plugin:sse-qc PROJ-123 --mode review       # gap analysis of the ticket
/sse-plugin:sse-qc PROJ-123 --mode test-case    # test cases, written to docs/qa/
/sse-plugin:sse-qc "pasted spec" --mode test-plan
```

File deliverables go to the project's existing QA docs folder if one exists, otherwise `docs/qa/`.

## Format validator

Every file deliverable must pass the Locked Format checker before it is reported as saved
(Python ≥ 3.9, standard library only):

```
python scripts/check_locked_format.py --mode test-plan  assets/sample-test-plan.md
python scripts/check_locked_format.py --mode test-case  assets/sample-test-case.md --json
python scripts/check_locked_format.py --mode checklist  assets/sample-checklist.md --verbose
```

Exit codes: `0` PASS · `1` FAIL (missing section or leftover `<...>` / `...` placeholder) ·
`2` usage or IO error. `--json` prints a machine-readable report on stdout.

## Layout

```
SKILL.md                        # the skill (modes, locked-format rules, standards map)
scripts/check_locked_format.py  # Locked Format validator
references/worked-examples.md   # filled examples for every mode
assets/template-*.md            # locked-format templates per document mode
assets/sample-*                 # fictional ticket, deliverables and test data (e-commerce refund)
expected_outputs/*.json         # validator --json output for the samples (run from this folder)
```

## Contributing

When a locked format changes, update in the same change: `assets/template-<mode>.md`, the
mode row in `SKILL.md`, `REQUIRED_HEADERS` in the script, the matching sample in `assets/`, its
JSON in `expected_outputs/`, and `references/worked-examples.md`.
