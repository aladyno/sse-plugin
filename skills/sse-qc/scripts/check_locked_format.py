#!/usr/bin/env python3
"""
check_locked_format.py - verify a written sse-qc deliverable (test-plan /
test-case / checklist) matches its mode's Locked Format before it is reported to
the user as saved.

Usage:
    python check_locked_format.py --mode test-plan  <file.md>
    python check_locked_format.py --mode test-case  <file.md> --json
    python check_locked_format.py --mode checklist  <file.md> --verbose

Exit codes:
    0 - PASS
    1 - FAIL (errors printed to stderr, or JSON with "status": "FAIL")
    2 - usage / IO error
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Headers are matched literally (substring match), so a heading may carry a
# trailing note, e.g. "## 7. Roles & schedule (only if sourced ...)".
REQUIRED_HEADERS = {
    "test-plan": [
        "# Test Plan",
        "## 1. Scope",
        "## 2. Test objectives",
        "## 3. Test strategy",
        "## 4. Environment & test data",
        "## 5. Entry / Exit criteria",
        "## 6. Risks & mitigation",
        "## 7. Roles & schedule",
        "## 8. Deliverables",
    ],
    "test-case": [
        "# Test Case",
        "## Not covered",
    ],
    "checklist": [
        "## QC Checklist",
        "### Pre-deploy",
        "### Functional smoke",
        "### Regression",
        "### Data/Config",
        "### Rollback",
        "### Sign-off",
    ],
}

# Leftover Locked-Format placeholders: "<...>" tokens or a bare "..." (not part of
# a longer ellipsis run like "...."). This is a heuristic, not a full parser.
# Known-legit HTML tags used inside the Locked Format templates themselves (e.g.
# "<br>" for line breaks inside a table cell) are excluded so they don't false-positive.
_SAFE_TAGS = {"br", "br/", "br /"}
PLACEHOLDER_PATTERN = re.compile(
    r"<(?!(?:" + "|".join(re.escape(t) for t in _SAFE_TAGS) + r")>)[^<>\n]{1,80}>"
    r"|(?<!\.)\.\.\.(?!\.)"
)


class CheckResult:
    """Aggregated result of one Locked Format check run."""

    def __init__(self, file: str, mode: str):
        self.file = file
        self.mode = mode
        self.sections = []  # list of {"header": str, "present": bool}
        self.placeholders = []  # unique leftover placeholder tokens
        self.placeholder_count = 0
        self.errors = []  # human-readable error strings

    @property
    def passed(self) -> bool:
        return not self.errors

    def add_section(self, header: str, present: bool) -> None:
        self.sections.append({"header": header, "present": present})
        if not present:
            self.errors.append(f"Missing required section: {header!r}")

    def add_placeholders(self, tokens) -> None:
        self.placeholder_count = len(tokens)
        self.placeholders = sorted(set(tokens))[:8]
        if tokens:
            sample = ", ".join(self.placeholders)
            self.errors.append(
                f"{len(tokens)} leftover placeholder token(s) still in file "
                f"(e.g. {sample}) — fill them in before reporting this file as saved."
            )

    def to_dict(self) -> dict:
        """JSON-serializable summary (machine-readable output contract)."""
        return {
            "file": self.file,
            "mode": self.mode,
            "status": "PASS" if self.passed else "FAIL",
            "sections_total": len(self.sections),
            "sections_present": sum(1 for s in self.sections if s["present"]),
            "sections": self.sections,
            "placeholder_count": self.placeholder_count,
            "placeholder_samples": self.placeholders,
            "errors": self.errors,
        }


def load_text(path: str) -> str:
    """Read the deliverable file as UTF-8, mapping IO problems to clear messages."""
    try:
        return Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        raise SystemExit(f"check_locked_format: file not found: {path}")
    except (UnicodeDecodeError, ValueError) as e:
        raise SystemExit(f"check_locked_format: {path} is not valid UTF-8 text: {e}")
    except OSError as e:
        raise SystemExit(f"check_locked_format: cannot read {path}: {e}")


def check_headers(text: str, mode: str, result: CheckResult) -> None:
    """Record presence of every required header for the given mode."""
    try:
        headers = REQUIRED_HEADERS[mode]
    except KeyError:
        result.errors.append(
            f"Unknown mode: {mode!r} (expected one of {sorted(REQUIRED_HEADERS)})"
        )
        return
    for header in headers:
        result.add_section(header, header in text)


def check_placeholders(text: str, result: CheckResult) -> None:
    """Record leftover template placeholders ("<...>" tokens, bare "...")."""
    result.add_placeholders(PLACEHOLDER_PATTERN.findall(text))


def run_check(path: str, mode: str) -> CheckResult:
    """Run the full Locked Format check for one file and return the result."""
    text = load_text(path)
    result = CheckResult(file=path, mode=mode)
    check_headers(text, mode, result)
    check_placeholders(text, result)
    return result


def print_human(result: CheckResult, verbose: bool) -> None:
    """Human-readable report on stderr (stdout is reserved for --json)."""
    if verbose:
        for section in result.sections:
            state = "OK " if section["present"] else "MISS"
            print(f"  [{state}] {section['header']}", file=sys.stderr)
    if result.passed:
        print("check_locked_format: PASS", file=sys.stderr)
        return
    print(f"check_locked_format: {len(result.errors)} error(s) found:", file=sys.stderr)
    for err in result.errors:
        print(f"  - {err}", file=sys.stderr)


def build_parser() -> argparse.ArgumentParser:
    """CLI definition. Kept separate so tests can exercise parsing directly."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python check_locked_format.py --mode test-plan  assets/sample-test-plan.md\n"
            "  python check_locked_format.py --mode test-case  out/PROJ-123-test-case.md --json\n"
            "  python check_locked_format.py --mode checklist  out/checklist.md --verbose\n"
        ),
    )
    parser.add_argument(
        "--mode", required=True, choices=sorted(REQUIRED_HEADERS),
        help="which Locked Format to validate against",
    )
    parser.add_argument("file", help="path to the deliverable .md file to check")
    parser.add_argument(
        "--json", action="store_true",
        help="emit a machine-readable JSON report on stdout instead of text",
    )
    parser.add_argument(
        "--verbose", action="store_true",
        help="also list per-section OK/MISS detail (text mode only)",
    )
    return parser


def main(argv) -> int:
    args = build_parser().parse_args(argv[1:])
    try:
        result = run_check(args.file, args.mode)
    except SystemExit as e:
        # load_text() raises SystemExit with a message; route it to stderr + exit 2
        print(e, file=sys.stderr)
        return 2
    except Exception as e:  # defensive: never die with a bare traceback
        print(f"check_locked_format: unexpected error: {e}", file=sys.stderr)
        return 2

    if args.json:
        json.dump(result.to_dict(), sys.stdout, ensure_ascii=False, indent=2)
        print()
    else:
        print_human(result, args.verbose)
    return 0 if result.passed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
