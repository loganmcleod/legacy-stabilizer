# Triage Model and Intervention Ladder

## Scoring

Use a transparent score to rank, then apply architectural judgment. Rate each
dimension 1–5 and normalize before comparing:

- production/customer impact
- incident or defect frequency
- evidence confidence
- performance/reliability leverage
- implementation effort
- blast radius
- regression risk
- verification strength
- reversibility

Prioritization formula:

```
priority =
  (impact × frequency × evidence × leverage × verification × reversibility)
  / (effort × blast_radius × regression_risk)
```

Show the component scores next to the result. The number ranks candidates; it does
not override hard constraints, dependencies, or expert judgment. A high score with
weak evidence is a lead to strengthen, not a change to make.

## Intervention Ladder

Stop at the lowest level that meets the objective. Every recommendation states why
lower levels are insufficient.

```
L0  Document / accept / monitor
L1  Instrument and add guardrails
L2  Add characterization or regression tests
L3  Correct configuration or resource lifecycle
L4  Make a local code or SQL fix without changing boundaries
L5  Extract a narrow collaborator or adapter to create a test seam
L6  Introduce a compatibility facade and incrementally replace internals
L7  Replace a bounded subsystem using a Strangler Fig migration
```

**L6–L7 require explicit approval and a decision record.**

## Stabilization-first examples

- Wrap existing AngularJS `$http` behavior behind a compatible service without
  changing route contracts; add cancellation and `$destroy` cleanup before
  considering component migration. (L5 before L7.)
- Extract one pure policy function from a Spring orchestration method while leaving
  endpoint and persistence contracts intact; add characterization tests first.
  (L2 then L5.)
- Batch an evidenced loop query or use a targeted fetch strategy; assert query
  counts in integration tests before considering repository replacement.
  (L2 then L4.)
- Align bind datatypes and validate the actual Oracle plan before proposing a new
  index. (L4, evidence-gated.)
- Shorten a transaction around database consistency work and keep remote calls
  outside it — only when failure semantics and idempotency are defined. (L4.)
