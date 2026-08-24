#!/usr/bin/env python3
"""Gate a remediation plan before it is trusted or acted on.

Every finding at a committed status (Confirmed, Planned, In Progress, Verified)
must carry evidence, verification, rollback, cost/risk, and ownership — with no
unresolved placeholders (TODO, TBD, ..., <fill me>). This is the check that stops
a half-written plan from being treated as decision-ready.

Accepts the findings registry (JSON). Optionally also scans a master-plan
markdown file for leftover placeholder tokens in committed sections. Run --plan
against a FILLED plan, not the blank template — the template is full of `...`
placeholders on purpose and will (correctly) produce warnings.

Usage:
    python validate_plan.py findings.json [--plan REMEDIATION_MASTER_PLAN.md]

Exit code 0 if the plan is gate-clean, 1 otherwise.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from stab_schema import (
    COMMITTED_STATUSES,
    is_placeholder,
    validate_structure,
)

# Cost/risk fields a committed finding needs so triage is auditable.
TRIAGE_FIELDS = ["effort", "blast_radius", "regression_risk"]


def load(path: Path) -> list:
    data = json.loads(path.read_text())
    if isinstance(data, dict) and "findings" in data:
        data = data["findings"]
    return data


def gate(findings: list) -> list:
    """Return list of gate-failure strings (empty == plan is clean)."""
    failures = []
    for f in findings:
        # Structural errors are gate failures too.
        failures.extend(validate_structure(f))

        if f.get("status") not in COMMITTED_STATUSES:
            continue
        fid = f.get("id", "<missing>")

        for field in ("verification", "rollback", "owner", "minimum_intervention"):
            if is_placeholder(f.get(field)):
                failures.append(f"{fid}: committed finding missing '{field}'")

        for field in TRIAGE_FIELDS:
            if is_placeholder(f.get(field)):
                failures.append(f"{fid}: committed finding missing triage '{field}'")

    return failures


def scan_plan_markdown(path: Path) -> list:
    """Flag placeholder tokens left inside the master plan prose."""
    warnings = []
    for n, line in enumerate(path.read_text().splitlines(), 1):
        stripped = line.strip()
        # Skip the schema/template rows that legitimately show enum lists.
        if stripped.startswith("|") or stripped.startswith("- Status:"):
            continue
        if is_placeholder(stripped) and stripped not in ("...", ""):
            warnings.append(f"{path.name}:{n}: unresolved placeholder -> {stripped[:60]}")
    return warnings


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("findings", help="Path to findings JSON")
    ap.add_argument("--plan", help="Optional master-plan markdown to scan for placeholders")
    args = ap.parse_args(argv)

    findings = load(Path(args.findings))
    failures = gate(findings)

    for e in failures:
        print(f"GATE-FAIL  {e}", file=sys.stderr)

    if args.plan:
        for w in scan_plan_markdown(Path(args.plan)):
            print(f"WARN       {w}", file=sys.stderr)

    committed = sum(1 for f in findings if f.get("status") in COMMITTED_STATUSES)
    print(json.dumps({
        "findings": len(findings),
        "committed": committed,
        "gate_failures": len(failures),
        "plan_ready": not failures,
    }, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
