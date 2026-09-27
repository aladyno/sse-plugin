#!/usr/bin/env python3
"""flow_forecast.py - flow metrics + Monte Carlo forecast from an issue-tracker export.

Optional, user-run analysis helper for the sse-pm entity. It reads a saved
issue export (Jira REST search shape `{"issues": [{"key", "fields": {...}}]}`, or a
flat JSON list of simplified issue dicts with the same field names) and prints:

  - the four Kanban Guide flow measures: WIP, throughput, cycle time
    (p50/p85/p95), work item age
  - Service Level Expectation (SLE) conformance and aging-WIP alerts
  - optional Monte Carlo "how many weeks to finish N more items" forecast
    (Vacanti-style throughput sampling, seeded, refuses on thin history)

Cycle time is approximated as created -> resolved unless the export carries a
`started` date per issue (add it from the changelog when you can; it is more
accurate). The output labels which basis was used.

Exit codes: 0 ok, 2 unreadable/invalid input.
Stdlib only; deterministic (as-of defaults to the newest date in the data, never
the wall clock; the forecast RNG is seeded).
"""

import argparse
import json
import math
import random
import sys
from datetime import date

# Status names treated as finished / not started (lower-case). A statusCategory
# field, when present, wins over these name lists.
DONE_STATUSES = {"done", "closed", "resolved", "released", "complete", "completed"}
NOT_STARTED_STATUSES = {"to do", "todo", "open", "backlog", "new", "created", "ready"}

SAMPLE_SNAPSHOT = {
    "issues": [
        {"key": "PROJ-1", "fields": {"summary": "Login flow", "status": {"name": "Done"},
         "created": "2026-05-04T09:00:00.000+0000",
         "resolutiondate": "2026-05-08T16:00:00.000+0000"}},
        {"key": "PROJ-2", "fields": {"summary": "Rate limiting", "status": {"name": "In Progress"},
         "created": "2026-05-18T09:00:00.000+0000", "started": "2026-05-19"}},
    ]
}


def parse_date(value):
    """Parse the leading YYYY-MM-DD of a timestamp; None when absent/invalid."""
    if not value:
        return None
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def name_of(value):
    """Return .name / .displayName of a tracker object, or the value itself."""
    if isinstance(value, dict):
        return value.get("name") or value.get("displayName") or ""
    return str(value) if value else ""


def normalize(raw):
    """Flatten tracker records into a minimal issue dict list."""
    if isinstance(raw, dict) and "issues" in raw:
        records = raw["issues"]
    elif isinstance(raw, list):
        records = raw
    else:
        raise ValueError("expected {'issues': [...]} or a JSON list of issues")
    issues = []
    for rec in records:
        if not isinstance(rec, dict):
            continue
        f = rec.get("fields", rec)
        status = name_of(f.get("status")).lower()
        category = ""
        if isinstance(f.get("status"), dict):
            category = name_of(f["status"].get("statusCategory")).lower()
        category = category or name_of(f.get("statusCategory")).lower()
        done = category == "done" if category else status in DONE_STATUSES
        started = (category != "to do") if category else status not in NOT_STARTED_STATUSES
        issues.append({
            "key": rec.get("key") or f.get("key") or "?",
            "summary": f.get("summary", ""),
            "done": done,
            "started_flag": started,
            "created": parse_date(f.get("created")),
            "started": parse_date(f.get("started")),
            "resolved": parse_date(f.get("resolutiondate") or f.get("resolved")),
        })
    return [i for i in issues if i["created"]]


def percentile(sorted_values, pct):
    """Nearest-rank percentile of an already-sorted list."""
    if not sorted_values:
        return None
    rank = max(1, math.ceil(pct / 100 * len(sorted_values)))
    return sorted_values[rank - 1]


def start_of(issue):
    """Best available start date: real start when exported, else created."""
    return issue["started"] or issue["created"]


def flow_report(issues, as_of, sle_days, forecast_items, seed):
    done = [i for i in issues if i["done"] and i["resolved"]]
    wip = [i for i in issues if not i["done"] and i["started_flag"]]
    has_real_start = any(i["started"] for i in done)
    cycles = sorted(max((i["resolved"] - start_of(i)).days, 0) + 1 for i in done)
    p50, p85, p95 = (percentile(cycles, p) for p in (50, 85, 95))

    # Weekly throughput over the full observed span (first resolution -> as_of),
    # zero-filled: empty weeks are real observations, dropping them biases the
    # forecast optimistic.
    weekly_counts = []
    if done:
        first_resolved = min(i["resolved"] for i in done)
        observed_weeks = max(((as_of - first_resolved).days // 7) + 1, 1)
        weekly_counts = [0] * observed_weeks
        for i in done:
            idx = min((i["resolved"] - first_resolved).days // 7, observed_weeks - 1)
            weekly_counts[idx] += 1

    sle = sle_days if sle_days else p85
    conformance = (
        round(100 * sum(1 for c in cycles if c <= sle) / len(cycles), 1)
        if cycles and sle is not None else None
    )
    aging = sorted(
        ({"key": i["key"], "summary": i["summary"][:60],
          "age_days": (as_of - start_of(i)).days + 1} for i in wip),
        key=lambda a: -a["age_days"],
    )
    aging_alerts = [a for a in aging if sle is not None and a["age_days"] > sle]

    report = {
        "as_of": as_of.isoformat(),
        "counts": {"total": len(issues), "done": len(done), "wip": len(wip)},
        "cycle_time_days": {
            "p50": p50, "p85": p85, "p95": p95,
            "basis": "started->resolved" if has_real_start
                     else "created->resolved (approximation: includes queue time before start)",
        },
        "throughput": {
            "weekly_counts": weekly_counts,
            "mean_per_week": round(sum(weekly_counts) / len(weekly_counts), 2) if weekly_counts else 0,
        },
        "sle": {"days": sle, "conformance_pct": conformance,
                "source": "user-supplied" if sle_days else "p85 cycle time"},
        "work_item_age": aging[:10],
        "aging_wip_alerts": aging_alerts,
        "warnings": [],
    }
    if len(done) < 10:
        report["warnings"].append(
            f"only {len(done)} completed items - percentiles are low-confidence below 10")
    if forecast_items:
        if len(weekly_counts) < 4 or len(done) < 10:
            report["warnings"].append(
                "forecast refused: need >= 10 completed items across >= 4 observed weeks")
        else:
            rng = random.Random(seed)
            trials = []
            for _ in range(10000):
                remaining, wk = forecast_items, 0
                while remaining > 0 and wk < 520:
                    remaining -= rng.choice(weekly_counts)
                    wk += 1
                trials.append(wk)
            trials.sort()
            report["forecast"] = {
                "items": forecast_items,
                "method": "Monte Carlo over historical weekly throughput (10k trials, seeded)",
                "weeks_at_confidence": {f"p{p}": percentile(trials, p) for p in (50, 70, 85, 95)},
                "note": "Assumes future throughput resembles the sampled history and "
                        "scope stays fixed; re-run weekly as data arrives.",
            }
    return report


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Flow metrics (WIP, throughput, cycle time, work item age, SLE) and a "
                    "Monte Carlo forecast from a saved issue-tracker export.")
    ap.add_argument("--input", help="Path to the saved export JSON ('-' for stdin).")
    ap.add_argument("--as-of", help="Analysis date YYYY-MM-DD (default: newest date in data).")
    ap.add_argument("--sle-days", type=int,
                    help="Service Level Expectation in days (default: p85 cycle time).")
    ap.add_argument("--forecast", type=int, metavar="N",
                    help="Forecast weeks needed to finish N more items.")
    ap.add_argument("--seed", type=int, default=42, help="RNG seed (default 42).")
    ap.add_argument("--sample", action="store_true",
                    help="Print a sample input shape and exit.")
    args = ap.parse_args()

    if args.sample:
        print(json.dumps(SAMPLE_SNAPSHOT, indent=2))
        return 0
    if not args.input:
        ap.error("--input is required (use --sample to see the expected shape)")
    try:
        if args.input == "-":
            raw = json.load(sys.stdin)
        else:
            with open(args.input, encoding="utf-8") as fh:
                raw = json.load(fh)
        issues = normalize(raw)
    except (OSError, ValueError) as exc:
        print(f"ERROR: cannot read export: {exc}", file=sys.stderr)
        return 2
    if not issues:
        print("ERROR: no issues with a created date found.", file=sys.stderr)
        return 2

    as_of = parse_date(args.as_of) if args.as_of else max(
        (i["resolved"] or i["started"] or i["created"]) for i in issues)
    if as_of is None:
        print(f"ERROR: --as-of '{args.as_of}' is not a valid YYYY-MM-DD date.", file=sys.stderr)
        return 2
    print(json.dumps(flow_report(issues, as_of, args.sle_days, args.forecast, args.seed), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
