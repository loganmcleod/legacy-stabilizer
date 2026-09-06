---
description: "Phase 6 — triage findings and produce the ranked REMEDIATION_MASTER_PLAN"
allowed-tools: ["Read", "Grep", "Glob", "Bash"]
---

Follow `${CLAUDE_PLUGIN_ROOT}/skills/legacy-stabilizer/SKILL.md`, Phase 6, using
the scoring and intervention ladder in `references/triage-model.md`.

1. Score each finding on the 1–5 dimensions; show component scores and the
   priority result. The number ranks; judgment decides. A high score with weak
   evidence is a lead to strengthen, not a change to make.
2. Assign each finding its lowest sufficient intervention level (L0–L7) and state
   why lower levels are insufficient. L6–L7 need explicit approval + decision record.
3. Order work by the default remediation sequence (contain harm → observe →
   regression protection → low-risk fixes → seams → decomposition → replacement).
4. Emit `REMEDIATION_MASTER_PLAN.md` from `templates/REMEDIATION_MASTER_PLAN.md`.
   Keep it a concise decision index; push detailed evidence into repo-local files.
5. Gate it:
   `python ${CLAUDE_PLUGIN_ROOT}/skills/legacy-stabilizer/scripts/validate_plan.py evidence/findings.json --plan REMEDIATION_MASTER_PLAN.md`
   Run `--plan` only against your FILLED plan — the blank template intentionally
   contains `...` placeholders and will warn.
6. **Always also emit `SPEC_DRIVEN_BRIEF.md`** from
   `templates/SPEC_DRIVEN_BRIEF.md`. This is a self-contained brief designed to be
   fed, whole, into a spec-driven AI framework (BMad Method, GitHub Spec Kit, Kiro)
   to generate PRDs, epics, and stories. Inline the product context, repo +
   tech-stack inventory, the non-negotiable guardrails, the confirmed architecture,
   and the ranked backlog rewritten as epics/stories keyed by finding ID; carry each
   claim's evidence state so the spec inherits the uncertainty. Then tell the user,
   in plain words, what it is and how to hand it off: "Paste this page into your
   spec-writing AI tool as the starting document."

This is where **assessment mode ends**. Its deliverables are the ranked master plan
and the spec-driven brief. Remediation is a separate, authorized step.
