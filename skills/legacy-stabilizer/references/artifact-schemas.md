# Artifact Schemas

The workspace layout and the exact shape of each machine-readable artifact. The
helper scripts in `scripts/` read and write these; keep them conformant so the
scripts stay useful.

## Workspace layout

```
stabilization-workspace/
├── CHARTER.md                         # scope, mode, remediation authorization gate
├── portfolio.yaml                     # repos, paths, revisions, owners, deployables
├── INITIAL_HEALTH_BASELINE.md         # first assessment output
├── REMEDIATION_MASTER_PLAN.md         # ranked cross-repo decision index
├── SPEC_DRIVEN_BRIEF.md               # spec-driven AI framework input (BMad/Spec Kit); always produced
├── architecture/
│   ├── system-context.md
│   ├── container-map.md
│   ├── runtime-paths.md
│   ├── dependency-map.md
│   └── decision-log.md                # accepted/rejected decisions (DECISION_RECORD entries)
├── evidence/
│   ├── inventory.json                 # output of inventory_workspace.py
│   ├── findings.json                  # normalized finding registry
│   └── metrics-baseline.md
└── repositories/
    └── <repo-id>/
        ├── ARCHITECTURE_BASELINE.md
        ├── REMEDIATION_FINDINGS.md
        ├── TEST_GAP_MAP.md
        └── PERFORMANCE_EVIDENCE.md
```

## `portfolio.yaml`

Records, at minimum, per repository: identifier, absolute/local path or canonical
URL, pinned commit SHA, default branch, language/build system, deployable units,
database schemas used, upstream/downstream dependencies, production criticality,
known owner. **Unknown values are marked `unknown`, never guessed.** See
`templates/portfolio.yaml`.

## `evidence/inventory.json`

Produced by `inventory_workspace.py`. Topology only — build systems, revisions,
file counts, candidate layer paths (directory-name heuristics). It never sets
deployables/owner/criticality; those come back as `unknown` for a human to fill.
Candidate layer keys include `presentation-angularjs`, `presentation-angular`,
`presentation-react`, `service-spring`, `persistence-sql` (Oracle or AlloyDB),
`search-solr`, and `cache-redis`. Build-system labels include `java/maven`,
`javascript/nx`, `javascript/angular`, `javascript/webpack`, and
`javascript/module-federation`. Every one is a lead, not proof of a runtime role.

## `SPEC_DRIVEN_BRIEF.md`

Seeded from `templates/SPEC_DRIVEN_BRIEF.md` and produced at the end of every
assessment run. A self-contained, machine/agent-facing brief meant to be fed whole
into a spec-driven AI framework (BMad Method, GitHub Spec Kit, Kiro) to generate
PRDs/epics/stories. It inlines the product context, repo + tech-stack inventory,
the non-negotiable guardrails, the confirmed architecture, and the ranked
remediation backlog rewritten as epics/stories keyed by finding ID. It is not
consumed by the helper scripts; it is a deliverable for downstream tooling.

## `evidence/findings.json` — the finding record

A JSON list of finding objects (or `{"findings": [...]}`). `normalize_findings.py`
and `validate_plan.py` consume this shape:

```json
{
  "id": "STAB-DB-0042",
  "status": "Confirmed",
  "confidence": "High",
  "repositories": [{"repo": "orders-api", "sha": "a1b2c3d"}],
  "coordinates": "OrderDao.java:88-140",
  "runtime_path": "checkout -> place order",
  "observed_behavior": "101 selects per checkout in integration test",
  "root_cause": "N+1 lazy load on OrderLine",
  "impact": ["performance"],
  "frequency": "every checkout",
  "minimum_intervention": "batch fetch; assert query count",
  "alternatives": ["observe only", "accept debt"],
  "verification": "query-count assertion 101 -> 2",
  "rollback": "revert single commit; no schema change",
  "owner": "orders-team",
  "effort": 2,
  "blast_radius": 1,
  "regression_risk": 1,
  "evidence_links": ["repositories/orders-api/PERFORMANCE_EVIDENCE.md#stab-db-0042"]
}
```

### Field rules (enforced by the scripts)

| Field | Rule |
|---|---|
| `id` | Must match `STAB-<AREA>-<NNNN>`, e.g. `STAB-DB-0042`. AREA = 2–4 uppercase letters. |
| `status` | One of: Candidate, Validating, Confirmed, Planned, In Progress, Verified, Deferred, Rejected. |
| `confidence` | High, Medium, Low. |
| `repositories[]` | Each needs `repo` and `sha` (7–40 hex, or `unknown`). |
| `impact` | Each value in: reliability, defect, performance, regression, operability, testability. |
| Committed statuses | Confirmed / Planned / In Progress / Verified additionally require non-placeholder `coordinates`, `observed_behavior`, `root_cause`, `minimum_intervention`, `verification`, `rollback`, `owner`, plus triage `effort`, `blast_radius`, `regression_risk`. |

A **placeholder** is empty, or contains `TODO`, `TBD`, `FIXME`, `XXX`, `...`, or
`<...>`. Committed findings may not carry placeholders — that is how the scripts
stop a static match from being dressed up as a confirmed defect.

### Deduplication

`normalize_findings.py` computes a fingerprint from `root_cause` + primary
`coordinates` + `runtime_path`. Two findings with the same fingerprint describe
one root cause and must be merged — link symptoms, do not inflate the count.

## `REMEDIATION_MASTER_PLAN.md` contract

A decision and progress index, not a scanner dump. Structure in
`templates/REMEDIATION_MASTER_PLAN.md`. Because line numbers drift, always carry
stable symbols, commit SHAs, SQL IDs, endpoint mappings, or Oracle object names
alongside line ranges.
