---
description: "Phase 1 — map polyrepo topology, builds, and candidate layer paths"
argument-hint: "<workspace-dir containing the repositories>"
allowed-tools: ["Read", "Grep", "Glob", "Bash"]
---

Follow `${CLAUDE_PLUGIN_ROOT}/skills/legacy-stabilizer/SKILL.md`, Phase 1.

Workspace: $ARGUMENTS

1. Seed the inventory:
   `python ${CLAUDE_PLUGIN_ROOT}/skills/legacy-stabilizer/scripts/inventory_workspace.py $ARGUMENTS --out evidence/inventory.json`
2. Corroborate the script output — it emits topology candidates only. Text and
   directory-name matches are leads, not proof of runtime roles.
3. Produce: system-context map, deployable/container map, repository dependency
   graph, high fan-in/fan-out list, structural single points of failure — each
   with evidence and confidence.
4. Draft `portfolio.yaml` from `templates/portfolio.yaml`; mark unknowns `unknown`.

Read-only. Do not classify defects yet.
