#!/usr/bin/env python3
"""Validate and normalize a findings registry.

Checks structure only: ID shape, enum values, required fields, repo/commit
coordinates, and duplicate root-cause fingerprints. It does NOT decide whether a
finding is real and it will NOT promote status. A scanner may hand this a pile of
Candidates; this script tells you which records are well-formed and which pairs
describe the same root cause and should be merged.

Usage:
    python normalize_findings.py findings.json [--out normalized.json] [--merge]

With --out and --merge, records sharing a root-cause fingerprint are collapsed
into one canonical record (strongest status/confidence wins; coordinates,
repositories, impact, and evidence links are unioned; merged ids are recorded).

Exit code 0 if all records are structurally valid, 1 otherwise.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

from stab_schema import (
    CONFIDENCE,
    STATUS_STRENGTH,
    fingerprint,
    validate_structure,
)


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


def _union(*lists) -> list:
    """Concatenate lists preserving order, dropping duplicates (JSON-hashable)."""
    seen, out = set(), []
    for lst in lists:
        for item in lst or []:
            key = json.dumps(item, sort_keys=True) if isinstance(item, dict) else item
            if key not in seen:
                seen.add(key)
                out.append(item)
    return out


def merge_duplicates(findings: list) -> tuple:
    """Collapse same-fingerprint findings into one canonical record.

    Canonical = strongest status (earliest in STATUSES), tie-broken by strongest
    confidence. Its id is kept; other ids are recorded under 'merged_ids'.
    Repositories, impact, alternatives, and evidence_links are unioned so no
    evidence is lost. Returns (merged_findings, merge_map).
    """
    groups = defaultdict(list)
    for f in findings:
        groups[fingerprint(f)].append(f)

    merged, merge_map = [], {}
    for group in groups.values():
        if len(group) == 1:
            merged.append(group[0])
            continue
        # Strongest first: lowest index in STATUS_STRENGTH / CONFIDENCE = strongest.
        canonical = min(group, key=lambda f: (
            STATUS_STRENGTH.index(f["status"]) if f.get("status") in STATUS_STRENGTH else 99,
            CONFIDENCE.index(f["confidence"]) if f.get("confidence") in CONFIDENCE else 99,
        ))
        result = dict(canonical)
        others = [f for f in group if f is not canonical]
        result["repositories"] = _union(
            canonical.get("repositories", []), *[o.get("repositories", []) for o in others])
        result["impact"] = _union(
            canonical.get("impact", []) if isinstance(canonical.get("impact"), list)
            else [canonical.get("impact")],
            *[o.get("impact", []) if isinstance(o.get("impact"), list) else [o.get("impact")]
              for o in others])
        result["alternatives"] = _union(
            canonical.get("alternatives", []), *[o.get("alternatives", []) for o in others])
        result["evidence_links"] = _union(
            canonical.get("evidence_links", []), *[o.get("evidence_links", []) for o in others])
        result["merged_ids"] = [o.get("id") for o in others]
        merged.append(result)
        merge_map[canonical.get("id")] = result["merged_ids"]

    return merged, merge_map


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("findings", help="Path to findings JSON")
    ap.add_argument("--out", help="Write normalized JSON here")
    ap.add_argument("--merge", action="store_true",
                    help="With --out, collapse duplicate root-cause findings into one record")
    args = ap.parse_args(argv)

    findings = load(Path(args.findings))
    report = check(findings)

    for e in report["errors"]:
        print(f"ERROR  {e}", file=sys.stderr)
    for dup in report["duplicate_groups"]:
        print(f"DUP    same root cause: {', '.join(dup['ids'])}", file=sys.stderr)

    if args.out:
        out_findings = findings
        if args.merge:
            out_findings, merge_map = merge_duplicates(findings)
            for keep, gone in merge_map.items():
                print(f"MERGE  {keep} absorbs {', '.join(gone)}", file=sys.stderr)
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({"findings": out_findings, "report": report}, indent=2))

    print(json.dumps({
        "count": report["count"],
        "errors": len(report["errors"]),
        "duplicate_groups": len(report["duplicate_groups"]),
        "valid": report["valid"],
    }, indent=2))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
