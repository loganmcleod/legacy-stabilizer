# legacy-stabilizer

A Claude Code skill and plugin for **assessing and stabilizing complex legacy
polyrepos** built on AngularJS 1.x, Java/Spring Boot, and Oracle.

Its first objective is to reduce production risk — defects, regressions, and
performance bottlenecks — at the **lowest safe cost**. Modernization is a
supporting tactic, never the default. It maps architecture across repositories,
validates each risk with evidence, ranks work by benefit-over-cost, and produces a
`REMEDIATION_MASTER_PLAN.md`.

> This is an engineering-quality and performance workflow. **It does not perform a
> security audit** and will not present security findings unless you separately ask.

---

## Why this exists

Auditing a large multi-repo estate with a generic "find all the bugs" prompt fails
in predictable ways: it turns weak static signals into confident conclusions,
jumps from a code smell straight to a rewrite, and produces one giant plan nobody
can act on. This package encodes a stricter discipline:

- **Evidence states, not verdicts.** Every static match is a *lead*
  (`Candidate`) until corroborated (`Probable`/`Confirmed`) or dismissed
  (`Not Reproducible`). Database claims require an execution plan or query count,
  not source inspection.
- **Assessment before remediation.** The default mode is read-only. Code changes
  need explicit, recorded authorization.
- **Smallest reversible intervention.** A ladder from "document and monitor" up to
  "Strangler Fig migration" — you stop at the lowest rung that addresses a
  *demonstrated* risk.
- **A concise portfolio plan, not a scanner dump.** The master plan is a ranked
  decision index; detailed evidence lives in repo-local artifacts.

The full design rationale is in [`docs/DESIGN_BRIEF.md`](docs/DESIGN_BRIEF.md).

---

## Installation

### Option A — as a Claude Code plugin (recommended)

From inside Claude Code:

```
/plugin marketplace add loganmcleod/legacy-stabilizer
/plugin install legacy-stabilizer@legacy-stabilizer-marketplace
```

`/plugin marketplace add` accepts your GitHub `owner/repo`. Adjust it to wherever
you publish this repository. To try it before publishing, point Claude Code at a
local checkout:

```bash
claude --plugin-dir /path/to/legacy-stabilizer
```

Validate the package first:

```bash
claude plugin validate /path/to/legacy-stabilizer --strict
```

Installing the plugin gives you the skill, six phase commands, and the read-only
assessor subagent.

### Option B — as a portable skill (no plugin)

The skill core is self-contained. Copy it into your personal or project skills
directory:

```bash
# personal (all projects)
cp -r skills/legacy-stabilizer ~/.claude/skills/legacy-stabilizer

# or project-local
cp -r skills/legacy-stabilizer .claude/skills/legacy-stabilizer
```

Claude then loads it on relevance, or you invoke it with `/legacy-stabilizer`.
The slash commands and subagent are plugin-only; the skill and its Python helpers
work either way.

---

## Usage

Start with the router, or jump to a phase. Commands are namespaced
`/legacy-stabilizer:<command>`:

| Command | Phase | Does | Mode |
|---|---|---|---|
| `/legacy-stabilizer:stabilize` | — | Overview and router | read-only |
| `/legacy-stabilizer:stabilize-inventory <workspace>` | 1 | Map topology, builds, candidate layers | read-only |
| `/legacy-stabilizer:stabilize-baseline` | 0, 2 | Charter + operational baseline | read-only |
| `/legacy-stabilizer:stabilize-trace <workflow>` | 3 | Trace a critical runtime path end to end | read-only |
| `/legacy-stabilizer:stabilize-findings [area]` | 4, 5 | Run detectors, normalize + dedupe findings | read-only |
| `/legacy-stabilizer:stabilize-plan` | 6 | Triage → ranked master plan | read-only |
| `/legacy-stabilizer:stabilize-remediate <finding-id>` | 7–10 | Design → implement → release → prevent | **authorization-gated** |

Typical first run (assessment-only):

```
/legacy-stabilizer:stabilize-inventory ~/work/my-estate
/legacy-stabilizer:stabilize-baseline
/legacy-stabilizer:stabilize-trace checkout
/legacy-stabilizer:stabilize-findings all
/legacy-stabilizer:stabilize-plan
```

This produces the health baseline, a traced runtime path, a validated findings
registry, and a ranked `REMEDIATION_MASTER_PLAN.md` — **without modifying any
application code**.

Remediation (`stabilize-remediate`) refuses to touch code unless the charter
records authorization for that finding/repo and the finding already carries
evidence, verification, and rollback.

---

## What's in the box

```
legacy-stabilizer/
├── .claude-plugin/
│   ├── plugin.json                 # plugin manifest
│   └── marketplace.json            # so `/plugin marketplace add` resolves it
├── skills/legacy-stabilizer/       # ← the portable skill core
│   ├── SKILL.md                    # entry point: role, modes, principles, phase index
│   ├── references/                 # progressive-disclosure detail
│   │   ├── workflow.md             # Phases 0–10 in full
│   │   ├── detectors-angularjs.md
│   │   ├── detectors-spring.md
│   │   ├── detectors-oracle.md
│   │   ├── triage-model.md         # scoring formula + L0–L7 intervention ladder
│   │   ├── artifact-schemas.md     # workspace layout + finding record schema
│   │   └── documentation.md        # C4 views + Mermaid runtime diagrams
│   ├── scripts/                    # deterministic helpers (Python 3.8+, stdlib only)
│   │   ├── inventory_workspace.py  # discover repos/revisions/layers → JSON
│   │   ├── normalize_findings.py   # validate + dedupe findings
│   │   ├── validate_plan.py        # gate: evidence/verify/rollback/owner present
│   │   ├── stab_schema.py          # shared schema + validation
│   │   └── test_scripts.py         # self-checks
│   └── templates/                  # portfolio.yaml, master plan, baseline, finding.json
├── commands/                       # six phase slash commands (plugin)
├── agents/stabilization-assessor.md# read-only discovery subagent (plugin)
├── docs/DESIGN_BRIEF.md            # full design rationale
├── LICENSE
└── README.md
```

### Deterministic helpers

The scripts do the repeatable, boring work and **never classify defects** — a
scanner emits candidates, humans and agents confirm them.

```bash
cd skills/legacy-stabilizer/scripts

python inventory_workspace.py ~/work/my-estate --out inventory.json
python normalize_findings.py evidence/findings.json
python validate_plan.py evidence/findings.json --plan REMEDIATION_MASTER_PLAN.md
python test_scripts.py        # 11 self-checks, stdlib only
```

`validate_plan.py` exits non-zero if any committed finding is missing evidence,
verification, rollback, cost/risk, or ownership — use it as a CI gate on your
plan.

---

## Safety model

- **Read-only by default.** No production code, DDL, dependency, contract, or
  deployment changes during assessment.
- **Authorization is explicit and recorded** in the charter before any
  remediation, naming who authorized it and for which findings/repos.
- **No fabrication.** Line numbers, plans, metrics, ownership, and runtime paths
  are reported only from evidence; unknowns are stated, not guessed.
- **Contracts preserved** — API, UI, database, event, batch, integration — unless
  an approved exception is documented.
- **Not a security tool.** Security review is deliberately out of scope.

---

## Development

```bash
python skills/legacy-stabilizer/scripts/test_scripts.py
claude plugin validate . --strict
```

The core logic lives in `SKILL.md` and `references/` and is platform-neutral. The
`commands/` and `agents/` directories are Claude Code adapters — the workflow
stays portable without them.

## License

MIT — see [LICENSE](LICENSE).
