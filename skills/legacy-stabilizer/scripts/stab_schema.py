"""Shared schema constants and helpers for the legacy-stabilizer helper scripts.

Deliberately stdlib-only so the scripts run anywhere Python 3.8+ is available,
including inside a portable ~/.claude/skills copy with no install step.

These helpers describe the *finding* record used across the workflow. They never
decide whether a finding is real — validation is structural only. Scanners emit
Candidates; humans/agents promote status after corroborating evidence.
"""
from __future__ import annotations

import re

# --- Enumerations -----------------------------------------------------------

STATUSES = [
    "Candidate",
    "Validating",
    "Confirmed",
    "Planned",
    "In Progress",
    "Verified",
    "Deferred",
    "Rejected",
]

# Statuses that assert the finding is real / being acted on. These carry the
# heaviest evidence burden in validate_plan.py.
COMMITTED_STATUSES = ["Confirmed", "Planned", "In Progress", "Verified"]

CONFIDENCE = ["High", "Medium", "Low"]

# Evidence states used in prose/artifacts (distinct from workflow Status).
EVIDENCE_STATES = ["Confirmed", "Probable", "Candidate", "Not Reproducible"]

IMPACT_KINDS = [
    "reliability",
    "defect",
    "performance",
    "regression",
    "operability",
    "testability",
]

# STAB-<AREA>-<NNNN>, e.g. STAB-DB-0042. AREA is 2-4 uppercase letters.
ID_RE = re.compile(r"^STAB-[A-Z]{2,4}-\d{4}$")

# SHA fragment: 7-40 hex chars, or the literal "unknown".
SHA_RE = re.compile(r"^([0-9a-f]{7,40}|unknown)$", re.IGNORECASE)

# Tokens that mean "not filled in yet" — reject these in committed findings.
PLACEHOLDER_RE = re.compile(r"(?:^|\b)(TODO|TBD|FIXME|XXX|\.\.\.|<[^>]+>)(?:\b|$)")

# Fields every finding record must define (may be empty for Candidate status).
REQUIRED_FIELDS = [
    "id",
    "status",
    "confidence",
    "repositories",  # list of {repo, sha}
    "coordinates",   # file+line range, symbol, sql_id, endpoint, or oracle object
    "runtime_path",
    "observed_behavior",
    "root_cause",
    "impact",
    "minimum_intervention",
    "verification",
    "rollback",
    "owner",
]

# Fields that must be non-empty once a finding reaches a committed status.
COMMITTED_REQUIRED = [
    "coordinates",
    "observed_behavior",
    "root_cause",
    "minimum_intervention",
    "verification",
    "rollback",
    "owner",
]


# --- Helpers ----------------------------------------------------------------

def is_placeholder(value) -> bool:
    """True if value is empty or contains an unresolved placeholder token."""
    if value is None:
        return True
    if isinstance(value, (list, dict)):
        return len(value) == 0
    s = str(value).strip()
    if not s:
        return True
    return bool(PLACEHOLDER_RE.search(s))


def fingerprint(finding: dict) -> str:
    """Stable dedupe key: root cause + primary coordinate + runtime path.

    Two findings with the same fingerprint describe the same root cause and
    should be merged, not counted twice.
    """
    coords = finding.get("coordinates", "")
    if isinstance(coords, dict):
        coords = "|".join(f"{k}={coords[k]}" for k in sorted(coords))
    parts = [
        str(finding.get("root_cause", "")).strip().lower(),
        str(coords).strip().lower(),
        str(finding.get("runtime_path", "")).strip().lower(),
    ]
    return "::".join(parts)


def validate_structure(finding: dict) -> list:
    """Return a list of structural error strings (empty == valid).

    Structural only: correct ID shape, known enum values, required fields
    present, committed findings carry evidence. Never judges truth.
    """
    errors = []
    fid = finding.get("id", "<missing>")

    if not ID_RE.match(str(finding.get("id", ""))):
        errors.append(f"{fid}: id must match STAB-<AREA>-<NNNN> (e.g. STAB-DB-0042)")

    status = finding.get("status")
    if status not in STATUSES:
        errors.append(f"{fid}: status '{status}' not in {STATUSES}")

    if finding.get("confidence") not in CONFIDENCE:
        errors.append(f"{fid}: confidence must be one of {CONFIDENCE}")

    impact = finding.get("impact")
    impacts = impact if isinstance(impact, list) else [impact]
    for i in impacts:
        if i not in IMPACT_KINDS:
            errors.append(f"{fid}: impact '{i}' not in {IMPACT_KINDS}")

    for field in REQUIRED_FIELDS:
        if field not in finding:
            errors.append(f"{fid}: missing required field '{field}'")

    # Repository coordinates must pin a commit SHA (or explicit 'unknown').
    for repo in finding.get("repositories", []) or []:
        if not isinstance(repo, dict) or "repo" not in repo or "sha" not in repo:
            errors.append(f"{fid}: each repository needs 'repo' and 'sha'")
            continue
        if not SHA_RE.match(str(repo["sha"])):
            errors.append(f"{fid}: sha '{repo['sha']}' invalid (7-40 hex or 'unknown')")

    # Committed findings must not carry placeholders in evidence fields.
    if status in COMMITTED_STATUSES:
        for field in COMMITTED_REQUIRED:
            if is_placeholder(finding.get(field)):
                errors.append(
                    f"{fid}: status '{status}' requires non-placeholder '{field}'"
                )
        # A committed finding claiming High/Medium confidence with no observed
        # behavior is exactly the "static match treated as proof" failure mode.
        if is_placeholder(finding.get("observed_behavior")):
            errors.append(
                f"{fid}: status '{status}' requires observed/measured behavior"
            )

    return errors
