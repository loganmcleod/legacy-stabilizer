---
description: "Start here — setup: gather everything, organize background notes, then begin Phase 0"
argument-hint: "[optional: anything you already want to tell me]"
allowed-tools: ["Read", "Grep", "Glob", "Bash"]
---

Load and follow `${CLAUDE_PLUGIN_ROOT}/skills/stabilization-init/SKILL.md`.

Anything the user said up front: $ARGUMENTS

Talk to the user like they are five years old the whole time: small words, short
sentences, explain every technical word with a tiny everyday picture, and check
they understand before moving on.

Do the setup in order:

1. Ask, in plain language, for the full paths to **every** repository, the
   background-notes folder, the important user journeys, the current symptoms,
   where to put the workspace, what to skip, whether we are looking-only or
   allowed-to-fix, and whether real-life telemetry exists.
2. Make a fresh `stabilization-workspace` and copy in `CHARTER.md` and
   `portfolio.yaml`.
3. If a background folder was given, read and sort every file into one master
   `evidence/BACKGROUND_DOSSIER.md` (seed from the init skill's template). No
   secrets; one line per file; list what is missing.
4. Show a plain-words summary and ask: "Are you ready for me to begin? (yes/no)"
5. On yes, begin **Phase 0** using the dossier as input — the same work as
   `/legacy-stabilizer:stabilize-baseline`. Stay read-only unless the user clearly
   authorized fixes.
