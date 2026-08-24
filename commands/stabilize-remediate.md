---
description: "Phases 7-10 — design, implement, release, and prevent (AUTHORIZATION REQUIRED)"
argument-hint: "<finding id, e.g. STAB-DB-0042>"
allowed-tools: ["Read", "Grep", "Glob", "Bash", "Edit", "Write"]
---

Follow `${CLAUDE_PLUGIN_ROOT}/skills/legacy-stabilizer/SKILL.md`, Phases 7–10.

Finding to remediate: $ARGUMENTS

**STOP — authorization gate.** Do not modify any code until you have confirmed, by
reading `CHARTER.md`:

- Mode is **Remediation-authorized**, and the Authorization table has a row for
  THIS finding ID and repo (naming who authorized it), and
- the finding is at `Confirmed` (or `Planned`) status with evidence, verification,
  and rollback already defined.

If either is missing, stay read-only and tell the user what is required.

Once authorized, work Phases 7–10:

1. **Design (7):** pick the lowest sufficient intervention level; explain why lower
   levels fail. L6–L7 need explicit approval and a decision record — write one from
   `templates/DECISION_RECORD.md` before proceeding.
2. **Implement (8):** pin baseline, reproduce, add/identify a characterization
   test, make ONE cohesive change (limited file/repo scope), run focused then
   broader tests, capture before/after evidence, verify cross-repo contracts and
   deployment ordering. Never mix upgrades, formatting, renames, or cleanup in.
3. **Release & verify (9):** risk-proportional rollout with predefined signals and
   rollback thresholds. "Code merged" is not verification.
4. **Prevent (10):** add one narrowly scoped safeguard tied to this finding.
5. Update finding status only after evidence is captured; re-run `validate_plan.py`.
