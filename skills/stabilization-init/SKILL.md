---
name: stabilization-init
description: >-
  Start-here setup skill for the legacy-stabilizer workflow. Ask the user, in
  plain everyday language, for everything the whole end-to-end run needs — the
  full paths to every repository, a folder of background material (reverse-
  engineered business cases, SQL, bug lists, UI-to-API-to-SQL flows, Jira dumps),
  the critical user journeys, and the current symptoms. Organize the background
  folder into one master BACKGROUND_DOSSIER.md, then ask if the user is ready and
  hand that dossier to Phase 0. Use at the very beginning, before any other
  stabilization command.
---

# Stabilization — Start Here (Setup)

## Talk like the person is five years old

Read this first. It is the most important rule, and it holds for **every message
you send the user** during this skill and the whole stabilization workflow that
follows.

- Use small, everyday words. Short sentences.
- The first time you use any technical word, explain it right away with a tiny
  everyday picture. Example: "A **repository** (repo for short) is just one big
  folder that holds the code for one app. Think of it like one LEGO box."
- After you explain something, check that it landed: "Does that make sense, or
  should I say it a different way?"
- Never make the user feel behind for not knowing a word. Assume they are smart
  but have never seen this before.
- One question at a time when it matters. Do not dump ten questions in one wall
  of text.
- No scary jargon without a translation. If you must use a word like "topology"
  or "N+1 query," give the kid-simple version in the same breath.

You are the friendly helper. The user is the boss who happens to be new to this.

## What this setup does (say this to the user in your own simple words)

"Before we look at your code, I need to gather a few things and tidy up your
notes into one neat page. Then I will ask if you are ready, and we will start.
Nothing gets changed in your code today — we are only looking and organizing."

## Step 1 — Ask for everything we need

Ask for these one group at a time. Explain each in kid-simple words **before**
you ask. Wait for the answer. Write every answer down so you can repeat it back
later. If the user does not know an answer, that is fine — write "not sure yet"
and move on. Never guess or make up an answer.

1. **The code folders (repositories).**
   Say: "A repository is one big folder that holds one app's code. I need the
   full path — the complete address on your computer — for **every** folder you
   want me to look at." Ask for all of them. This one is required; we cannot
   start without at least one real path. Read each path back and confirm it
   exists before moving on.

2. **The background-notes folder (source directory).**
   Say: "Do you have a folder full of notes and homework about this system? I can
   read it so I understand the story before I look at the code. Give me the full
   path to that folder." Tell them the kinds of notes that help:
   - **Reverse-engineered business cases** — write-ups of what the app is
     *supposed* to do for the business, figured out after the fact.
   - **Existing SQL queries** — the questions the app asks the database.
   - **Analyzed potential bug lists** — lists of things someone thinks might be
     broken.
   - **UI-to-API-to-SQL flows** — maps showing how a button click travels from
     the screen, to the server, to the database, and back.
   - **Dumped stories, issues, and bugs from Jira** — the team's to-do and
     problem tickets, exported from Jira (a tool teams use to track work).
   If they have no such folder, say that is okay and skip the dossier step.

3. **The important things people do (critical user journeys).**
   Say: "What are the one to three most important things a person does with this
   app — the ones that would hurt most if they broke? Like 'check out a cart' or
   'log in.'"

4. **What is going wrong right now (current symptoms).**
   Say: "Is anything acting up today? Slow pages, error messages, things
   crashing? Tell me what you have seen or heard about."

5. **Where to work and what to skip.**
   Say: "Where should I put my notes? I will make a fresh, empty folder called
   `stabilization-workspace` so I never touch your code." Ask for a location.
   Then: "Are there any code folders I should **not** look at? Any parts that are
   off-limits or not part of this?"

6. **Are we just looking, or are we allowed to fix?**
   Say: "There are two modes. **Looking-only** means I study and write a plan but
   change nothing — this is the safe default. **Allowed-to-fix** means someone in
   charge has said I may change specific things later. Which one are we in?" If
   they say allowed-to-fix, ask **who** gave permission and **which** code folders
   it covers. If they are unsure, choose looking-only. Never assume permission to
   change code.

7. **Can we see how it behaves in real life (telemetry)?**
   Say: "**Telemetry** is like a fitness tracker for the app — numbers about
   speed, errors, and traffic. Do we have any of that? Answer yes, no, or a
   little." Also ask: "Is there anything you know I will not be able to see or
   open?"

When you finish, repeat the whole list back in plain words and ask: "Did I get
all of that right?"

## Step 2 — Make the workspace (a clean desk to work on)

Explain: "I am making a fresh, empty folder for my notes so I never touch your
real code." Then create it:

```bash
mkdir -p <chosen-location>/stabilization-workspace/{architecture,evidence,repositories}
```

Copy the starting paperwork from the main skill's templates (the
`legacy-stabilizer` skill, usually next to this one):

```bash
cp <legacy-stabilizer>/templates/CHARTER.md   <workspace>/
cp <legacy-stabilizer>/templates/portfolio.yaml <workspace>/
```

Tell the user: "Done — I have a clean desk to work on."

## Step 3 — Tidy the background notes into one master page

Only if the user gave a background folder in Step 1.

Explain first: "You handed me a pile of notes. I am going to read each one, sort
them into piles, and write one tidy summary page so we both remember what is in
there. I am **not** changing your notes — just making a table of contents."

Do this:

1. List every file in the background folder (look in sub-folders too).
2. Open and read each one you can (text, markdown, `.sql`, `.csv`, `.json`,
   exported Jira files, and so on). If a file is a type you cannot read, note
   that and move on — do not guess what is inside.
3. Sort each file into one of these piles (use "Other" if it fits none):
   - Reverse-engineered business cases
   - Existing SQL queries
   - Analyzed potential bug lists
   - UI-to-API-to-SQL flows
   - Jira stories / issues / bugs
   - Other
4. Write everything into one file:
   `<workspace>/evidence/BACKGROUND_DOSSIER.md`, seeded from this skill's
   `templates/BACKGROUND_DOSSIER.md`. For each file give a one-line, plain-words
   summary and a link to the original. Never copy secrets (passwords, keys,
   personal or customer data) into the dossier — if you see any, leave it out and
   say you left it out.
5. At the bottom, list which piles are **empty** (so we know what is missing) and
   any questions the notes raised.

Then tell the user, simply, what you found: "I read N files. Here is the short
version…" and point them to the dossier page.

## Step 4 — Ask if they are ready, then start Phase 0

Show a short, plain-words summary: the code folders, the background page, the
important journeys, the symptoms, the mode, and where your notes live.

Then ask, clearly: **"Are you ready for me to begin? (yes / no)"**

- If **no**: ask what they want to change or add, fix it, and ask again. Do not
  move on until they say yes.
- If **yes**: begin **Phase 0** of the main workflow. Load the `legacy-stabilizer`
  skill (`../legacy-stabilizer/SKILL.md`, or the plugin path
  `${CLAUDE_PLUGIN_ROOT}/skills/legacy-stabilizer/SKILL.md`) and follow its
  Phase 0. Use `BACKGROUND_DOSSIER.md` as the **input** to fill in the charter —
  it already holds the journeys, symptoms, and known problems. In the plugin this
  is the same work as `/legacy-stabilizer:stabilize-baseline`.

Remember all the way through: keep talking like the user is five, stay in
looking-only mode unless they clearly gave permission to fix, and never invent a
fact you do not have.
