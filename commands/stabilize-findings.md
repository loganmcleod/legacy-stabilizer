---
description: "Phases 4-5 — run targeted detectors, then normalize and dedupe findings"
argument-hint: "[area: angularjs | angular-nx | spring | oracle | all]"
allowed-tools: ["Read", "Grep", "Glob", "Bash"]
---

Follow `${CLAUDE_PLUGIN_ROOT}/skills/legacy-stabilizer/SKILL.md`, Phases 4–5.

Area focus: $ARGUMENTS

1. Apply detectors from the relevant reference(s):
   `detectors-angularjs.md`, `detectors-angular-nx.md`, `detectors-spring.md`,
   `detectors-oracle.md`.
   Every match is a **Candidate** with an evidence state
   (`Confirmed`/`Probable`/`Candidate`/`Not Reproducible`). Attach the proof each
   detector requires before raising confidence. Do not assert DB behavior without
   a plan or query count.
2. Write records to `evidence/findings.json` using the schema in
   `references/artifact-schemas.md` (seed from `templates/finding.json`).
3. Validate and dedupe:
   `python ${CLAUDE_PLUGIN_ROOT}/skills/legacy-stabilizer/scripts/normalize_findings.py evidence/findings.json`
   Merge any duplicate root-cause fingerprints; one record per root cause.

Read-only. Findings are leads until corroborated.
