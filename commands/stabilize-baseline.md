---
description: "Phases 0 & 2 — charter, safety boundaries, and the operational baseline"
argument-hint: "[known symptoms / critical journeys]"
allowed-tools: ["Read", "Grep", "Glob", "Bash"]
---

Follow `${CLAUDE_PLUGIN_ROOT}/skills/legacy-stabilizer/SKILL.md`, Phases 0 and 2.

Context from user: $ARGUMENTS

0. If `evidence/BACKGROUND_DOSSIER.md` exists (from `stabilize-init`), read it
   first and use it to pre-fill the charter; confirm each item with the user.
1. **Charter (Phase 0):** emit `CHARTER.md` from `templates/CHARTER.md` and fill
   it — business-critical journeys, current production symptoms, repos in scope,
   exclusions, and the Mode. Leave the Authorization table empty for an
   assessment-only run; a remediation-authorized run needs a row per finding/repo
   naming who authorized it. This file is the gate `stabilize-remediate` reads.
2. **Baseline (Phase 2):** collect available evidence — incidents/defects, latency
   and error/throughput/saturation metrics, JVM/GC, browser performance, DB wait
   events, slow-query evidence and plans, existing tests, reproducible failing
   cases. Where telemetry is missing, downgrade confidence and label proxies.
3. Emit `INITIAL_HEALTH_BASELINE.md` from `templates/INITIAL_HEALTH_BASELINE.md`.
   Report only what discovery supports; state limitations; do not invent metrics.
