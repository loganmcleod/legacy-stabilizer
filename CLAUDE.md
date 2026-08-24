# Project instructions — legacy-stabilizer

## Keep documentation in sync before every push

**Before any `git push` to GitHub, update all documentation and `README.md` to
match the code and skill changes in the commits being pushed.** Do this as the
last step before pushing — never push stale docs.

When preparing to push, check and update as needed:

- `README.md` — install steps, the stage/command table, per-stage examples, the
  "what's in the box" file tree, and command/skill counts.
- `docs/PLAYBOOK.md` — the step order, commands, and quick-reference table.
- `docs/DESIGN_BRIEF.md` — the targeted tech stack and detector/file lists.
- `skills/*/SKILL.md` and `commands/*.md` — descriptions and phase indexes.
- `fixtures/README.md` — detector/fixture coverage.

Then verify nothing drifted:

```bash
python skills/legacy-stabilizer/scripts/test_scripts.py   # helper self-checks
python .github/scripts/check_manifests.py                 # manifests + front matter
grep -rniE "six|seven|eight" README.md                    # sanity-check command/skill counts
```

If any command, skill, phase, detector, template, or the tech stack changed and
the docs above do not reflect it, fix the docs in the same push. If docs are
already current, say so and proceed.

> Note: this is an instruction I follow when I run the push. For enforcement that
> does not depend on me remembering, add a git `pre-push` hook (or a Claude Code
> `PreToolUse` hook on `git push` in `.claude/settings.json`) that blocks the push
> until docs are updated. Ask if you want that wired up.
