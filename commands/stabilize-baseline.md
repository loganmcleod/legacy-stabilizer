---
description: "Phases 0 & 2 — charter, safety boundaries, and the operational baseline"
argument-hint: "[known symptoms / critical journeys]"
allowed-tools: ["Read", "Grep", "Glob", "Bash"]
---

Follow `${CLAUDE_PLUGIN_ROOT}/skills/legacy-stabilizer/SKILL.md`, Phases 0 and 2.

Context from user: $ARGUMENTS

1. **Charter (Phase 0):** record business-critical journeys, current production
   symptoms, repos in scope, exclusions, and the mode (assessment-only or
   remediation-authorized, naming who authorized it). Restate the change
   boundaries.
2. **Baseline (Phase 2):** collect available evidence — incidents/defects, latency
   and error/throughput/saturation metrics, JVM/GC, browser performance, DB wait
   events, slow-query evidence and plans, existing tests, reproducible failing
   cases. Where telemetry is missing, downgrade confidence and label proxies.
3. Emit `INITIAL_HEALTH_BASELINE.md` from `templates/INITIAL_HEALTH_BASELINE.md`.
   Report only what discovery supports; state limitations; do not invent metrics.
