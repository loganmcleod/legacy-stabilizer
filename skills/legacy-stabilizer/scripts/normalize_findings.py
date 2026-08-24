#!/usr/bin/env python3
"""Validate and normalize a findings registry.

Checks structure only: ID shape, enum values, required fields, repo/commit
coordinates, and duplicate root-cause fingerprints. It does NOT decide whether a
finding is real and it will NOT promote status. A scanner may hand this a pile of
Candidates; this script tells you which records are well-formed and which pairs
describe the same root cause and should be merged.

Usage:
    python normalize_findings.py findings.json [--out normalized.json]

Exit code 0 if all records are structurally valid, 1 otherwise.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

from stab_schema import fingerprint, validate_structure


def load(path: Path) -> list:
    data = json.loads(path.read_text())
    if isinstance(data, dict) and "findings" in data:
        data = data["findings"]
    if not isinstance(data, list):
        raise ValueError("findings file must be a JSON list, or {'findings': [...]}")
    return data


def check(findings: list) -> dict:
    errors = []
    for f in findings:
        errors.extend(validate_structure(f))

    # Duplicate detection by root-cause fingerprint.
    groups = defaultdict(list)
    for f in findings:
        groups[fingerprint(f)].append(f.get("id", "<missing>"))
    duplicates = {fp: ids for fp, ids in groups.items() if len(ids) > 1}

    return {
        "count": len(findings),
        "errors": errors,
        "duplicate_groups": [
            {"fingerprint": fp, "ids": ids} for fp, ids in duplicates.items()
        ],
        "valid": not errors,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("findings", help="Path to findings JSON")
    ap.add_argument("--out", help="Write normalized (deduped-flagged) JSON here")
    args = ap.parse_args(argv)

    findings = load(Path(args.findings))
    report = check(findings)

    for e in report["errors"]:
        print(f"ERROR  {e}", file=sys.stderr)
    for dup in report["duplicate_groups"]:
        print(f"DUP    same root cause: {', '.join(dup['ids'])}", file=sys.stderr)

    if args.out:
        Path(args.out).write_text(json.dumps(
            {"findings": findings, "report": report}, indent=2))

    print(json.dumps({
        "count": report["count"],
        "errors": len(report["errors"]),
        "duplicate_groups": len(report["duplicate_groups"]),
        "valid": report["valid"],
    }, indent=2))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
