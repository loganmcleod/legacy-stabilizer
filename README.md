# legacy-stabilizer

A Claude Code skill and plugin for **assessing and stabilizing complex legacy and
modern polyrepos**. The estate may include any of:

- **Front end:** AngularJS 1.x, Angular 17 (NX 17.3.x), and React 19.
- **MFE composition:** micro-frontends via Webpack 5 Module Federation.
- **Back end:** Java 21; Spring Boot 2.7.18 and/or 3.5; Hibernate; Maven 3.8+.
- **Relational data:** Oracle 19c and AlloyDB (PostgreSQL-compatible, GCP).
- **Search:** SOLR 9.x. · **Cache:** Redis 7.2 (often GCP Memorystore).

Its first objective is to reduce production risk — defects, regressions, and
performance bottlenecks — at the **lowest safe cost**. Modernization is a
supporting tactic, never the default. It maps architecture across repositories,
validates each risk with evidence, ranks work by benefit-over-cost, and produces a
`REMEDIATION_MASTER_PLAN.md` plus a `SPEC_DRIVEN_BRIEF.md` — a ready-to-hand-off
input for spec-driven AI frameworks such as [BMad Method](https://github.com/bmad-code-org/BMAD-METHOD)
and [GitHub Spec Kit](https://github.com/github/spec-kit).

> This is an engineering-quality and performance workflow. **It does not perform a
> security audit** and will not present security findings unless you separately ask.

> **Plain-language by design.** Throughout, the workflow talks to you like you are
> five: small words, every technical term explained with an everyday picture, and a
> check that it made sense. It changes *how* things are explained, never *what* the
> workflow does.

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
- **A spec-driven hand-off.** Every assessment run also emits `SPEC_DRIVEN_BRIEF.md`
  — a self-contained brief (product context, tech stack, hard guardrails, and the
  ranked backlog as epics/stories) built to be pasted straight into a spec-driven
  AI tool like BMad or Spec Kit to generate PRDs and stories for the fix work.

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

Installing the plugin gives you **two skills** (`stabilization-init` and
`legacy-stabilizer`), **eight slash commands** (a router, the setup command, and
six phase commands), and the read-only `stabilization-assessor` subagent.

After installing, confirm it loaded by typing `/` in Claude Code and looking for
the `legacy-stabilizer:` commands, or run the router:

```
/legacy-stabilizer:stabilize
```

### Option B — as portable skills (no plugin)

The skill cores are self-contained. Copy **both** skill folders into your personal
or project skills directory:

```bash
# personal (all projects)
cp -r skills/legacy-stabilizer   ~/.claude/skills/legacy-stabilizer
cp -r skills/stabilization-init  ~/.claude/skills/stabilization-init

# or project-local
cp -r skills/legacy-stabilizer   .claude/skills/legacy-stabilizer
cp -r skills/stabilization-init  .claude/skills/stabilization-init
```

Claude loads them on relevance, or you invoke them by name: `/stabilization-init`
to start, or `/legacy-stabilizer` for the main workflow. The slash commands
(`stabilize-*`) and the subagent are plugin-only; the skills and their Python
helpers work either way.

---

## Usage

> **New here? The single command to start is `/legacy-stabilizer:stabilize-init`.**
> It asks you everything, sets up the workspace, and walks you into the rest. The
> [`docs/PLAYBOOK.md`](docs/PLAYBOOK.md) is the full prescriptive run; the sections
> below show how to invoke and interact with **every** stage, with examples.

The helper scripts need **Python 3.8+** on your PATH. All commands are namespaced
`/legacy-stabilizer:<command>`. Every stage except the last is read-only.

### The map of stages

| # | Command | Phase | What it does | Mode |
|---|---|---|---|---|
| — | `/legacy-stabilizer:stabilize` | — | Overview + router; points you to the right stage | read-only |
| 1 | `/legacy-stabilizer:stabilize-init` | setup | **Start here.** Asks for repos + background notes, builds the workspace and `BACKGROUND_DOSSIER.md`, then begins Phase 0 | read-only |
| 2 | `/legacy-stabilizer:stabilize-baseline` | 0, 2 | Writes the charter (scope + safety gate) and the operational baseline | read-only |
| 3 | `/legacy-stabilizer:stabilize-inventory <path>` | 1 | Maps repos, builds, and candidate layers | read-only |
| 4 | `/legacy-stabilizer:stabilize-trace <workflow>` | 3 | Traces one critical path end to end | read-only |
| 5 | `/legacy-stabilizer:stabilize-findings [area]` | 4, 5 | Runs detectors, normalizes + dedupes findings | read-only |
| 6 | `/legacy-stabilizer:stabilize-plan` | 6 | Triages into a ranked master plan **and the spec-driven brief** | read-only |
| 7 | `/legacy-stabilizer:stabilize-remediate <finding-id>` | 7–10 | Designs, implements, releases, prevents | **authorization-gated** |

### How you interact with it

You do not need to know the jargon. Each command **talks to you like you are
five**: it asks plain-language questions, explains any technical word with an
everyday picture, and waits for your answers. A typical exchange:

```
You:     /legacy-stabilizer:stabilize-init

Claude:  Before we look at your code, I need a few things. First one:
         a "repository" is one big folder that holds one app's code — like one
         LEGO box. What is the full path to each folder you want me to look at?

You:     /Users/me/work/orders-ui, /Users/me/work/orders-api

Claude:  Got it — two folders. Do you also have a folder of background notes
         (old bug lists, SQL, Jira exports)? If yes, what is its full path?

You:     /Users/me/work/handover-notes

...and so on. At the end it shows a summary and asks "Ready to begin? (yes/no)".
```

Answer in plain words. If you do not know something, say "not sure" — it records
that instead of guessing. You can also pass context up front:
`/legacy-stabilizer:stabilize-init checkout is slow and nightly recon fails`.

### Stage 1 — `stabilize-init` (start here)

```
/legacy-stabilizer:stabilize-init
```

**Asks you for:** full paths to every repository (required); a background-notes
folder (optional — reverse-engineered business cases, SQL, bug lists,
UI→API→SQL flows, Jira dumps); your most important user journeys; current
symptoms; where to put the workspace; anything to skip; looking-only vs
allowed-to-fix; and whether real-life telemetry exists.

**Produces:** a fresh `stabilization-workspace/` (with `CHARTER.md` and
`portfolio.yaml`), and — if you gave a notes folder — one tidy
`evidence/BACKGROUND_DOSSIER.md` summarizing every note. Then it asks
"Ready? (yes/no)" and, on yes, moves into Stage 2.

> **Prefer to set up by hand?** You can skip `stabilize-init` and scaffold the
> workspace yourself, then start at Stage 2:
> ```bash
> mkdir -p stabilization-workspace/{architecture,evidence,repositories}
> cd stabilization-workspace
> cp <skill>/templates/CHARTER.md .        # scope + authorization gate
> cp <skill>/templates/portfolio.yaml .    # repo manifest
> ```

### Stage 2 — `stabilize-baseline` (charter + baseline)

```
/legacy-stabilizer:stabilize-baseline "checkout is slow; nightly recon fails"
```

**Reads** `BACKGROUND_DOSSIER.md` if present, then fills `CHARTER.md` (scope,
critical journeys, symptoms, and the Mode — the safety gate) and writes
`INITIAL_HEALTH_BASELINE.md` from whatever evidence exists. Where telemetry is
missing it says so and downgrades confidence instead of inventing numbers.

### Stage 3 — `stabilize-inventory` (map the estate)

```
/legacy-stabilizer:stabilize-inventory ~/work/my-estate
```

**Produces** `evidence/inventory.json` (repos, revisions, build systems,
candidate layers) and helps you fill `portfolio.yaml`. Topology only — a match is
a lead, not proof of a call relationship.

### Stage 4 — `stabilize-trace` (follow one path)

```
/legacy-stabilizer:stabilize-trace checkout
```

**Traces** one dominant workflow across every layer (Angular/AngularJS →
Spring Boot → Oracle) and produces a Mermaid sequence diagram, labelling anything
inferred. Pick the journey that hurts most if it breaks.

### Stage 5 — `stabilize-findings` (detect + normalize)

```
/legacy-stabilizer:stabilize-findings all
# or narrow to one layer:
/legacy-stabilizer:stabilize-findings angular-nx
/legacy-stabilizer:stabilize-findings spring
/legacy-stabilizer:stabilize-findings oracle
```

**Applies** the detectors along the traced paths, writes each as a `Candidate`
in `evidence/findings.json`, and runs `normalize_findings.py` to validate and flag
duplicate root causes. It will not assert a database problem without a query count
or execution plan.

### Stage 6 — `stabilize-plan` (rank the work)

```
/legacy-stabilizer:stabilize-plan
```

**Produces** the ranked `REMEDIATION_MASTER_PLAN.md` and gates it with
`validate_plan.py`, then **always also produces `SPEC_DRIVEN_BRIEF.md`** — the
same portfolio rewritten as a self-contained brief (stack, guardrails, and the
ranked work as epics/stories) that you paste straight into a spec-driven AI
framework like BMad or Spec Kit. **This is the end of an assessment-only run** —
the deliverables are the plan and the brief, and no application code has changed.

> **What is the spec-driven brief for?** The master plan is for *humans* deciding
> what to do. `SPEC_DRIVEN_BRIEF.md` is *machine/agent-facing* input: hand it to a
> spec-driven development tool and it generates the PRDs, epics, and stories that
> implement the plan — without re-discovering the estate. It carries the guardrails
> (stabilize-first, preserve contracts, evidence-before-action) forward so the
> generated specs cannot quietly turn a stabilization job into a rewrite.

### Stage 7 — `stabilize-remediate` (only when authorized)

```
/legacy-stabilizer:stabilize-remediate STAB-DB-0042
```

**Refuses to touch code** unless `CHARTER.md` has an Authorization row for that
finding/repo *and* the finding already carries evidence, verification, and
rollback. To authorize: set the charter Mode to **Remediation-authorized** and add
a row naming the finding ID, repo, who authorized it, and the date. It then works
one small reversible batch: reproduce → characterization test → single change →
tests → before/after evidence → contract check → risk-proportional release.

### The whole assessment run, end to end

```
/legacy-stabilizer:stabilize-init                 # answer the questions
/legacy-stabilizer:stabilize-baseline "checkout is slow; nightly recon fails"
/legacy-stabilizer:stabilize-inventory ~/work/my-estate
/legacy-stabilizer:stabilize-trace checkout
/legacy-stabilizer:stabilize-findings all
/legacy-stabilizer:stabilize-plan
```

This yields the dossier, health baseline, a traced runtime path, a validated
findings registry, a ranked `REMEDIATION_MASTER_PLAN.md`, and the
`SPEC_DRIVEN_BRIEF.md` hand-off — **without modifying any application code**.

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
│   │   ├── detectors-angular-nx.md
│   │   ├── detectors-react-mfe.md  # React 19 + Webpack 5 Module Federation
│   │   ├── detectors-spring.md     # Spring Boot 2.7 & 3.5, Java 21, Maven
│   │   ├── detectors-oracle.md
│   │   ├── detectors-alloydb.md    # AlloyDB / PostgreSQL
│   │   ├── detectors-search-cache.md  # SOLR 9.x + Redis 7.2
│   │   ├── triage-model.md         # scoring formula + L0–L7 intervention ladder
│   │   ├── artifact-schemas.md     # workspace layout + finding record schema
│   │   └── documentation.md        # C4 views + Mermaid runtime diagrams
│   ├── scripts/                    # deterministic helpers (Python 3.8+, stdlib only)
│   │   ├── inventory_workspace.py  # discover repos/revisions/layers → JSON
│   │   ├── normalize_findings.py   # validate + dedupe findings
│   │   ├── validate_plan.py        # gate: evidence/verify/rollback/owner present
│   │   ├── stab_schema.py          # shared schema + validation
│   │   └── test_scripts.py         # self-checks
│   └── templates/                  # CHARTER, portfolio, master plan, baseline, spec-driven brief, finding, decision record
├── skills/stabilization-init/       # ← start-here setup skill (gather inputs, build dossier)
│   ├── SKILL.md
│   └── templates/BACKGROUND_DOSSIER.md
├── commands/                       # phase slash commands (plugin), incl. stabilize-init
├── agents/stabilization-assessor.md# read-only discovery subagent (plugin)
├── docs/
│   ├── PLAYBOOK.md                 # prescriptive step-by-step run (start here)
│   └── DESIGN_BRIEF.md             # full design rationale
├── fixtures/                       # true/false-positive pairs proving the detectors
├── .github/                        # CI: self-checks + manifest validation on push
├── LICENSE
└── README.md
```

### Deterministic helpers

The scripts do the repeatable, boring work and **never classify defects** — a
scanner emits candidates, humans and agents confirm them.

```bash
cd skills/legacy-stabilizer/scripts

python inventory_workspace.py ~/work/my-estate --out inventory.json
python normalize_findings.py evidence/findings.json                    # validate + flag dupes
python normalize_findings.py evidence/findings.json --out merged.json --merge  # collapse dupes
python validate_plan.py evidence/findings.json --plan REMEDIATION_MASTER_PLAN.md
python test_scripts.py        # 13 self-checks, stdlib only
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
python skills/legacy-stabilizer/scripts/test_scripts.py   # helper self-checks
python .github/scripts/check_manifests.py                 # manifests + front matter
claude plugin validate . --strict                         # full schema check (needs the CLI)
```

CI runs the first two on every push (see `.github/workflows/ci.yml`). The
`fixtures/` directory holds true/false-positive pairs you can point the skill at to
confirm the detectors distinguish a real defect from a look-alike — see
`fixtures/README.md`.

The core logic lives in `SKILL.md` and `references/` and is platform-neutral. The
`commands/` and `agents/` directories are Claude Code adapters — the workflow
stays portable without them.

## License

MIT — see [LICENSE](LICENSE).
