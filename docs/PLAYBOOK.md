# Playbook — a prescriptive run, start to finish

This is the exact sequence to follow. Do the steps in order. Each step names the
command to run, the decision to make at its gate, the artifact it produces, and the
condition that lets you proceed. Do not skip a gate.

If you only read one thing, read this. The `references/` files are the detail
behind each step.

---

## Before you start

- **Prerequisites:** Claude Code with the plugin installed (or the skill copied
  in), and Python 3.8+ on your PATH for the helper scripts.
- **Mindset:** you are in **assessment mode** until you deliberately leave it. The
  default output of this entire playbook is a *plan*, not a code change.
- **Golden rule:** every finding is a lead until evidence corroborates it. If you
  cannot show a plan, a query count, a metric, or a reproduction, the finding stays
  a `Candidate` and does not drive a change.

---

## Step 0 — Create the workspace

Pick a directory *outside* the code you are assessing and scaffold it:

```bash
mkdir -p stabilization-workspace/{architecture,evidence,repositories}
cd stabilization-workspace
```

Copy the starting artifacts from the skill's templates (adjust the path to where
the skill lives — `${CLAUDE_PLUGIN_ROOT}/skills/legacy-stabilizer/templates` when
installed as a plugin, or `~/.claude/skills/legacy-stabilizer/templates` when
copied in):

```bash
cp <templates>/CHARTER.md .
cp <templates>/portfolio.yaml .
```

**Gate:** you have an empty, structured workspace and a blank charter.

---

## Step 1 — Write the charter (Phase 0)

```
/legacy-stabilizer:stabilize-baseline <known symptoms / critical journeys>
```

Fill `CHARTER.md`: scope, in/out repos, critical journeys, production symptoms,
and — the important part — the **Mode**. Leave it `Assessment-only` for now; the
Authorization table stays empty.

**Decision:** what are the one to three user journeys whose failure hurts most?
Everything downstream is ranked by impact on these.

**Artifact:** `CHARTER.md`.
**Gate:** scope is written and the mode is explicit. Do not proceed on a vague
scope — that is how disconnected code gets audited as if it were critical.

---

## Step 2 — Map the estate (Phase 1)

```
/legacy-stabilizer:stabilize-inventory /path/to/your/repos
```

This runs `inventory_workspace.py` (topology only) and then you corroborate:
system-context map, container/deployable map, dependency graph, fan-in/fan-out,
and structural single points of failure.

**Decision:** which repos and modules actually sit on the critical journeys?
Mark the rest out of focus.

**Artifacts:** `evidence/inventory.json`, `portfolio.yaml` (unknowns marked
`unknown`), maps under `architecture/`.
**Gate:** you can name every repo on a critical journey and its pinned SHA.

---

## Step 3 — Baseline the operation (Phase 2)

Continue from the baseline command. Gather what evidence exists: incidents,
defects, latency/error/throughput/saturation, JVM/GC, browser performance, DB wait
events, slow-query evidence and plans, existing tests, reproducible failures.

**Decision:** for each top concern, do you have a measurable baseline, or do you
need an evidence-acquisition task? Where telemetry is missing, say so and label any
local number a proxy.

**Artifact:** `INITIAL_HEALTH_BASELINE.md`.
**Gate:** every top concern has either a baseline or an explicit task to get one.

---

## Step 4 — Trace the critical path (Phase 3)

```
/legacy-stabilizer:stabilize-trace checkout
```

Trace one dominant workflow across all layers, recording input/output shape,
transaction scope, side effects, query count, and existing tests at every
boundary. Produce a Mermaid sequence diagram; label anything inferred.

**Decision:** where on this path does cost or risk actually concentrate?
**Artifact:** an entry in `architecture/runtime-paths.md`.
**Gate:** one end-to-end path is traced with evidence, not assumption.

---

## Step 5 — Detect and normalize findings (Phases 4–5)

```
/legacy-stabilizer:stabilize-findings all
```

Apply the detectors, but only along the paths you traced. Write each as a
`Candidate` in `evidence/findings.json` with its evidence state, then:

```bash
python <scripts>/normalize_findings.py evidence/findings.json
```

**Decision:** for each candidate, what single piece of evidence would confirm or
kill it? Go get that, or leave it a `Candidate`. Merge any duplicate root-cause
fingerprints the script reports.

**Artifact:** `evidence/findings.json`.
**Gate:** no duplicates; every committed finding carries observed behavior.

---

## Step 6 — Triage and produce the plan (Phase 6)

```
/legacy-stabilizer:stabilize-plan
```

Score each finding, assign its lowest sufficient intervention level (L0–L7), order
by the default remediation sequence, and write the plan. Then gate it:

```bash
python <scripts>/validate_plan.py evidence/findings.json --plan REMEDIATION_MASTER_PLAN.md
```

**Decision:** which findings clear the gate and are worth doing first? A high score
with weak evidence is a lead to strengthen, not work to schedule.

**Artifact:** `REMEDIATION_MASTER_PLAN.md`.
**Gate:** `validate_plan.py` exits 0.

**This is the end of an assessment-only run.** The deliverable is the ranked plan.
Stop here unless you are authorizing changes.

---

## Step 7 — Authorize, then remediate (Phases 7–10, opt-in)

Only now, and only for specific findings:

1. In `CHARTER.md`, set Mode to **Remediation-authorized** and add a row to the
   Authorization table naming the finding ID, repo, who authorized it, and the date.
2. Confirm the finding is at `Confirmed`/`Planned` with evidence, verification, and
   rollback already defined.
3. Run:
   ```
   /legacy-stabilizer:stabilize-remediate STAB-DB-0042
   ```

The command refuses to touch code if the authorization row or the evidence is
missing. It then works one small reversible batch: reproduce, characterization
test, single cohesive change, focused then broader tests, before/after evidence,
cross-repo contract check, risk-proportional release, one recurrence safeguard.

For any L6–L7 intervention, write a `DECISION_RECORD.md` first.

**Gate to close a finding:** success criteria met and evidence captured.
"Code merged" is not verification. Re-run `validate_plan.py` and update status.

---

## Quick reference

| Step | Command | Produces | Proceed when |
|---|---|---|---|
| 0 | (scaffold) | workspace + blank charter | structure exists |
| 1 | `stabilize-baseline` | `CHARTER.md` | scope + mode explicit |
| 2 | `stabilize-inventory` | `inventory.json`, `portfolio.yaml`, maps | critical repos + SHAs named |
| 3 | `stabilize-baseline` | `INITIAL_HEALTH_BASELINE.md` | baseline or acquisition task per concern |
| 4 | `stabilize-trace` | `runtime-paths.md` | one path traced with evidence |
| 5 | `stabilize-findings` | `findings.json` | no dupes; committed findings have evidence |
| 6 | `stabilize-plan` | `REMEDIATION_MASTER_PLAN.md` | `validate_plan.py` exits 0 |
| 7 | `stabilize-remediate` | code change + verification | authorized + finding verified |
