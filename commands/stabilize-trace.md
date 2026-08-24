---
description: "Phase 3 — trace one critical runtime path end to end across repos"
argument-hint: "<the workflow to trace, e.g. checkout>"
allowed-tools: ["Read", "Grep", "Glob", "Bash"]
---

Follow `${CLAUDE_PLUGIN_ROOT}/skills/legacy-stabilizer/SKILL.md`, Phase 3.

Workflow to trace: $ARGUMENTS

Trace it through every boundary:

```
AngularJS route/template -> controller/component/directive -> client service/HTTP
-> Spring endpoint -> service orchestration -> repository/DAO/stored proc
-> Oracle objects and SQL -> response mapping -> UI state update
```

At each boundary record: input/output shape, validation/transformation, state
owner, sync & async side effects, transaction scope, retry behavior, query count,
error translation, existing tests. Note duplicated business rules and hidden
coupling — but do not recommend moving logic merely because it sits in a legacy
layer. Produce a Mermaid sequence diagram (see `references/documentation.md`);
label any inferred element.
