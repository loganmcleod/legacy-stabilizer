# Claude Code Skill Brief: Stabilization-First Architecture Remediation

## Purpose

Use this document as the design brief and introductory prompt for creating a reusable Claude Code skill/plugin that assesses and stabilizes complex polyrepo applications built with AngularJS 1.x, Java/Spring Boot, and Oracle.

The skill must optimize for production stability, defect reduction, regression prevention, and measurable performance improvement. Architectural modernization is a supporting tactic, not the default objective. Preserve behavior and existing contracts unless evidence shows that a narrow structural change is required to remove a material operational risk.

The skill is an engineering-quality and performance workflow. It must not perform a security audit or present security findings unless the user separately asks for that work.

## Recommended Claude Code Opening Prompt

> Act as a Principal Software Architect and Stabilization Engineer for legacy AngularJS 1.x, Java/Spring Boot, and Oracle systems. Your first objective is to reduce production risk, defects, regressions, and performance bottlenecks at the lowest safe cost. Do not assume that modernization or broad refactoring is desirable.
>
> Begin in read-only discovery mode. Map the polyrepo topology, build and deployment boundaries, runtime call paths, test coverage, observability, ownership, and persistence patterns. Separate confirmed findings from suspected risks. Never claim a database indexing problem, N+1 query, transaction defect, memory leak, or production bottleneck without stating the evidence and confidence level.
>
> Produce an initial architectural health baseline before proposing code changes. Rank candidate work by production impact, evidence strength, implementation cost, blast radius, reversibility, and verification quality. Prefer guardrails, characterization tests, query fixes, bounded configuration changes, resource cleanup, and small extractions over rewrites or new frameworks.
>
> Maintain a root `REMEDIATION_MASTER_PLAN.md` as the cross-repository index. Store detailed evidence in repository-local assessment files so the master plan remains concise. Every finding must have stable coordinates, evidence, affected runtime path, impact, confidence, proposed minimum intervention, verification plan, rollback plan, dependencies, and status.
>
> Do not edit production code during assessment unless explicitly authorized. When remediation is authorized, work in small independently testable batches, preserve public behavior, run relevant checks, and stop if evidence contradicts the proposed change or the verification signal is inadequate.

## Critique of the Initial Audit Prompt

The original prompt identifies useful legacy failure modes, but it should not be used unchanged for a large polyrepo estate.

1. **It is predisposed toward finding defects.** A scanner asked to “actively catalog occurrences” can turn weak static signals into conclusions. The skill must use evidence states: `Confirmed`, `Probable`, `Candidate`, and `Not Reproducible`.
2. **Some rules are proxies, not defects.** A 1,500-line controller is a review trigger. A long class is not automatically a production risk; a shorter method may still be the true orchestration bottleneck.
3. **Several database findings require runtime evidence.** “Unindexed query” and “implicit conversion causing a full scan” generally require schema metadata and an Oracle execution plan, not source inspection alone.
4. **“Taint tracking” conflicts with the non-security scope.** Call this state and data-flow tracing. Track transformations, ownership, side effects, and query fan-out rather than security taint.
5. **It jumps too quickly from audit to refactoring.** Stabilization should first consider instrumentation, tests, configuration, resource cleanup, transaction correction, query batching, and local extractions.
6. **A drop-in snippet is not always safe.** For cross-layer behavior, the correct deliverable may be a migration seam, characterization test, feature flag, or experiment instead of replacement code.
7. **A single detailed root plan will not scale.** Use a concise portfolio-level master plan linked to repo-local evidence and runbooks.
8. **Exact snippets need limits.** Include the smallest relevant excerpt, with surrounding context referenced by coordinates. Avoid copying large methods into the plan.

## Non-Negotiable Operating Principles

- Stabilize before modernizing.
- Measure before optimizing.
- Characterize behavior before changing it.
- Prefer the smallest reversible intervention that addresses a demonstrated risk.
- Preserve API, UI, database, event, batch, and integration contracts by default.
- Treat static-analysis matches as leads until corroborated.
- Separate observation, inference, recommendation, and authorized implementation.
- Do not combine unrelated fixes in one remediation batch.
- Do not introduce a new framework, persistence abstraction, state-management library, or service boundary solely for stylistic consistency.
- Do not perform wide formatting, renaming, package moves, or dependency upgrades alongside stabilization fixes.
- State when evidence is unavailable. Never fabricate line numbers, plans, metrics, ownership, or runtime paths.

## Polyrepo Control Plane

Before scanning code, create a portfolio manifest. This prevents duplicated findings and makes cross-repository runtime paths traceable.

Recommended structure:

```text
stabilization-workspace/
├── portfolio.yaml                     # repos, paths, revisions, owners, deployables
├── REMEDIATION_MASTER_PLAN.md          # ranked cross-repo decision index
├── architecture/
│   ├── system-context.md               # actors, deployables, external systems
│   ├── container-map.md                # web apps, services, jobs, databases
│   ├── runtime-paths.md                 # critical end-to-end request/data flows
│   ├── dependency-map.md                # build-time and runtime dependencies
│   └── decision-log.md                  # accepted/rejected remediation decisions
├── evidence/
│   ├── inventory.json                  # machine-readable discovery results
│   ├── findings.json                   # normalized finding registry
│   └── metrics-baseline.md              # performance and reliability baseline
└── repositories/
    └── <repo-id>/
        ├── ARCHITECTURE_BASELINE.md
        ├── REMEDIATION_FINDINGS.md
        ├── TEST_GAP_MAP.md
        └── PERFORMANCE_EVIDENCE.md
```

`portfolio.yaml` should record, at minimum: repository identifier, absolute/local path or canonical URL, pinned commit SHA, default branch, language/build system, deployable units, database schemas used, upstream/downstream dependencies, production criticality, and known owner. Unknown values must be marked `unknown`, not guessed.

## End-to-End Workflow

### Phase 0 — Charter, Scope, and Safety Boundaries

Define the business-critical user journeys, current production symptoms, target environments, repositories in scope, and explicit exclusions. Record whether the current run is assessment-only or authorizes implementation.

Establish change boundaries:

- No production code changes during discovery.
- No database DDL, dependency upgrade, data migration, public-contract change, or deployment without separate authorization.
- No load testing against production.
- Redact credentials, personal data, customer data, and secrets from artifacts.
- Pin every finding to a repository and commit SHA so coordinates remain reproducible.

Exit criterion: the repository inventory and critical-runtime-path list are sufficiently complete to avoid auditing disconnected code as if it were production-critical.

### Phase 1 — Automated Topology and Build Mapping

For each repository, identify:

- build roots and package/module boundaries;
- deployable services, web applications, scheduled jobs, and database migration projects;
- AngularJS modules, routes, controllers, directives, services, factories, interceptors, and templates;
- Spring controllers, services, domain objects, repositories/DAOs, transaction annotations, schedulers, listeners, and integration clients;
- Oracle access paths including JPA, Hibernate, Spring JDBC, MyBatis, stored procedures, native SQL, and dynamic SQL builders;
- cross-repo HTTP, messaging, shared-library, file, and database coupling;
- CI checks, test types, code coverage if trustworthy, release process, feature flags, and observability hooks.

Use language-aware parsing when available. Text search is acceptable for candidate generation but must not be treated as proof of call relationships.

Deliverables:

- a system context map;
- a deployable/container map;
- a repository dependency graph;
- a list of high fan-in/high fan-out components;
- structural single points of failure, each with evidence and confidence.

### Phase 2 — Establish the Operational Baseline

Collect available evidence before recommending performance work:

- incident themes, defect history, support tickets, rollback frequency, and recent high-risk changes;
- endpoint latency distributions, throughput, error rate, saturation, JVM/GC metrics, browser performance, and database wait events;
- slow-query evidence, SQL IDs, AWR/ASH reports when authorized, execution plans, logical reads, row estimates versus actuals, and query frequency;
- existing unit, integration, contract, end-to-end, and performance tests;
- reproducible failing cases for known defects.

If production telemetry is unavailable, explicitly downgrade confidence. Use safe local or non-production measurements and label them as proxies.

Exit criterion: each top-priority concern has either a measurable baseline or an explicit evidence-acquisition task.

### Phase 3 — Critical Runtime-Path Tracing

Trace the few workflows that dominate customer impact or operational cost. A runtime-path record should follow:

```text
AngularJS route/template
  -> controller/component/directive
  -> client service / HTTP adapter
  -> Spring endpoint and request mapping
  -> application/service orchestration
  -> repository/DAO/stored procedure
  -> Oracle objects and SQL
  -> response mapping and UI state update
```

At every boundary, record input/output shape, validation and transformation, state owner, synchronous and asynchronous side effects, transaction scope, retry behavior, query count, error translation, and existing tests. Identify duplicated business rules and hidden coupling, but do not recommend moving logic merely because it is located in a legacy layer.

### Phase 4 — Targeted Defect Detection

Apply targeted detectors after topology and runtime-path mapping so results can be ranked by real use.

#### AngularJS 1.x

Review candidates for:

- controllers/directives with excessive size, responsibility count, dependencies, or change frequency;
- direct `$http` use outside a dedicated client/data-access service (templates normally cannot inject `$http`; distinguish template expressions from controller/directive code);
- event listeners, intervals, timeouts, DOM/plugin handlers, and custom watchers not released on `$destroy`;
- high watcher count, deep watches, collection watches, watch functions that allocate or trigger work, and digest feedback loops;
- repeated network calls, route-level waterfalls, duplicated state, and expensive filters/functions invoked from templates;
- shared mutable state on services or `$rootScope` that creates action-at-a-distance regressions.

Evidence may include static coordinates, watcher profiling, heap snapshots, detached DOM nodes, network traces, digest timing, and a reproducible navigation loop.

#### Spring Boot / Java

Review candidates for:

- service methods combining policy, orchestration, persistence, mapping, retries, and side effects;
- mutable request-specific state held by singleton beans;
- ambiguous, overly broad, or missing transaction boundaries around multi-step consistency requirements;
- self-invocation that bypasses transactional proxies, unexpected propagation, and remote calls inside long transactions;
- repeated repository calls in loops, excessive entity loading, and chatty downstream calls;
- blocking operations on constrained executor/request threads;
- weak seams for testing critical behavior and hidden static/global dependencies.

Do not classify an anemic model as a defect solely by style. It becomes actionable when centralized procedural logic demonstrably increases defect risk, coupling, test cost, or inconsistent rule enforcement.

#### Oracle / Persistence

Review candidates for:

- ORM lazy-loading or DAO calls that produce N+1 query behavior;
- SQL built through value concatenation or fragmented conditional strings that hinder correctness, plan stability, and testability;
- high-frequency/high-cost SQL with access paths inconsistent with selectivity and available indexes;
- implicit conversions, functions on indexed columns, datatype mismatches, leading-wildcard searches, or non-sargable predicates;
- excessive round trips, over-fetching, unstable pagination, and row-by-row processing;
- transaction duration, lock contention, plan regression, cardinality-estimate errors, and stale statistics where supported by evidence.

Require an execution plan or equivalent runtime proof before asserting a full table scan is harmful. A full scan may be optimal for small tables or low-selectivity queries. Index recommendations must account for write cost, storage, selectivity, existing composite indexes, and plan stability.

### Phase 5 — Normalize and Validate Findings

Create one canonical finding record per root cause, even when symptoms appear in multiple repositories.

Required fields:

| Field | Meaning |
|---|---|
| ID | Stable identifier such as `STAB-DB-0042` |
| Status | Candidate, Validating, Confirmed, Planned, In Progress, Verified, Deferred, Rejected |
| Evidence confidence | High, Medium, Low |
| Repositories/revisions | Exact repos and commit SHAs |
| Coordinates | File and line range, symbol, SQL ID, endpoint, or Oracle object |
| Runtime path | Business workflow affected |
| Observed behavior | What was actually measured or reproduced |
| Root-cause hypothesis | Interpretation, clearly labeled |
| Impact | Reliability, defect, performance, regression, operability, or testability |
| Frequency/exposure | How often and under what conditions |
| Minimum intervention | Smallest credible change |
| Alternatives | Including “observe only” and “accept debt” |
| Verification | Tests and before/after metrics |
| Rollback | Concrete reversal mechanism |
| Dependencies/owner | Teams, repos, releases, schema, or environment needs |

Deduplicate by root cause and affected runtime path. Link related symptoms rather than inflating the finding count.

### Phase 6 — Triage for Maximum Benefit at Minimum Cost

Use a transparent score, but retain architectural judgment. Suggested dimensions use a 1–5 scale:

- production/customer impact;
- incident or defect frequency;
- evidence confidence;
- performance/reliability leverage;
- implementation effort;
- blast radius;
- regression risk;
- verification strength;
- reversibility.

A useful prioritization formula is:

```text
priority =
  (impact × frequency × evidence × leverage × verification × reversibility)
  / (effort × blast_radius × regression_risk)
```

Normalize inputs before comparing results and show the component scores. Do not let the numeric result override hard constraints, dependencies, or expert judgment.

Default remediation order:

1. **Contain active harm:** leaks, runaway retries, duplicate work, uncontrolled query fan-out, thread/connection exhaustion, and known data-consistency failures.
2. **Add observability and reproducibility:** measurements, focused logging/metrics, query-count assertions, and deterministic failing cases.
3. **Create regression protection:** characterization, contract, integration, and targeted performance tests around critical paths.
4. **Apply low-risk local fixes:** cleanup handlers, query batching/fetch tuning, parameterized SQL, bounded transactions, indexes proven by plans and workload evidence, and configuration corrections.
5. **Extract a test seam:** isolate side effects or policy only where needed to make the fix testable and safe.
6. **Perform structural decomposition:** only when smaller interventions cannot safely address the confirmed risk.
7. **Consider replacement or Strangler Fig migration:** only for persistently high-cost/high-risk areas with a stable seam, migration economics, parallel-run strategy, and rollback path.

### Phase 7 — Design the Minimum Safe Remediation

Choose from the following intervention ladder, stopping at the lowest level that meets the objective:

```text
L0  Document / accept / monitor
L1  Instrument and add guardrails
L2  Add characterization or regression tests
L3  Correct configuration or resource lifecycle
L4  Make a local code or SQL fix without changing boundaries
L5  Extract a narrow collaborator or adapter to create a test seam
L6  Introduce a compatibility facade and incrementally replace internals
L7  Replace a bounded subsystem using a Strangler Fig migration
```

Every recommendation must explain why lower intervention levels are insufficient. Levels 6–7 require explicit approval and a decision record.

Examples of stabilization-first remediation:

- Wrap existing AngularJS `$http` behavior behind a compatible service without changing route contracts; add cancellation and `$destroy` cleanup before considering component migration.
- Extract one pure policy function from a Spring orchestration method while leaving endpoint and persistence contracts intact; add characterization tests first.
- Batch an evidenced loop query or use a targeted fetch strategy; assert query counts in integration tests before considering repository replacement.
- Align bind datatypes and validate the actual Oracle plan before proposing a new index.
- Shorten a transaction around database consistency work and keep remote calls outside it only when failure semantics and idempotency are defined.

### Phase 8 — Implement in Small, Reversible Batches

For authorized changes:

1. Pin the baseline revision and reproduce the issue.
2. Add or identify a failing/characterization test.
3. Make one cohesive change with limited file and repository scope.
4. Run focused tests, then the relevant broader suite.
5. Compare before/after correctness and performance evidence.
6. Verify cross-repo contracts and deployment ordering.
7. Document rollback, feature-flag, canary, or disablement mechanics.
8. Update finding status only after evidence is captured.

Avoid mixing dependency upgrades, formatting, renames, and architectural cleanup into the same change.

### Phase 9 — Release and Verify

Use a risk-proportional release strategy: feature flag, dark read, shadow traffic, canary, percentage rollout, or standard deployment with enhanced monitoring. Define expected signals and automatic/manual rollback thresholds in advance.

Verification must cover:

- original behavior and known edge cases;
- performance delta at representative load and data volume;
- database plan/query-count stability;
- error, timeout, retry, and partial-failure behavior;
- resource cleanup after repeated navigation or requests;
- production signals over an agreed observation window.

Close a finding only when the success criteria are met. “Code merged” is not verification.

### Phase 10 — Prevent Recurrence

Add narrowly scoped safeguards supported by actual findings:

- ArchUnit rules for validated package or dependency boundaries;
- query-count assertions for known N+1-prone flows;
- lint/custom static checks for lifecycle cleanup patterns;
- contract tests at high-risk cross-repo interfaces;
- performance budgets for critical endpoints and UI workflows;
- database plan monitoring for a small set of business-critical SQL statements;
- ownership metadata and decision records for fragile components.

Do not create broad rules that produce noise or freeze legitimate legacy patterns.

## Required Architectural Documentation

The skill should create documentation proportionate to the system, using lightweight C4-style views and targeted runtime diagrams:

1. **System context:** users, external systems, and the polyrepo application boundary.
2. **Container/deployable view:** AngularJS applications, Spring services/jobs, integration components, and Oracle schemas.
3. **Component hot-spot view:** only for high-risk/high-change areas.
4. **Critical runtime sequences:** the most important user and batch workflows.
5. **Data ownership map:** authoritative sources, shared tables/schemas, and cross-service database access.
6. **Deployment coupling map:** release ordering, compatibility windows, and rollback dependencies.

Diagrams must be generated from confirmed evidence where possible and labeled when inferred. Prefer Mermaid text so diagrams can be reviewed in version control.

## `REMEDIATION_MASTER_PLAN.md` Contract

The master plan is a decision and progress index, not a dump of scanner output. Use this structure:

```markdown
# Remediation Master Plan

## Scope and Baseline
- Portfolio revision: ...
- Repositories: ...
- Assessment date: ...
- Critical runtime paths: ...
- Evidence limitations: ...

## Architectural Health Baseline
- Presentation layer: ...
- Service/application layer: ...
- Persistence/database layer: ...
- Cross-repository coupling: ...
- Test and observability posture: ...

## Prioritized Remediation Portfolio
| Rank | ID | Finding | Runtime path | Impact | Confidence | Cost | Risk | Intervention | Owner | Status |
|---:|---|---|---|---|---|---|---|---|---|---|

## Findings

### [STAB-XX-0001] Defect or Anti-Pattern Name
- Status: Candidate / Confirmed / Planned / Verified / Deferred / Rejected
- Target Coordinates: repository, commit SHA, exact file and line range or runtime identifier
- Affected Runtime Path: user/system workflow
- Evidence and Confidence: observed facts, reproduction, metrics, and confidence
- Debt Impact: High / Medium / Low, with reliability, performance, testability, or regression impact
- Current Code State: smallest exact relevant excerpt
- Root Cause: confirmed cause or explicitly labeled hypothesis
- Minimum Safe Remediation: intervention level and why lower levels are insufficient
- Proposed Modular Architecture: only if boundary change is necessary; include text/Mermaid mapping
- Phased Remediation Snippet: concrete example or pseudocode clearly labeled; do not claim it is drop-in until compiled/tested in context
- Verification Plan: tests and before/after measures
- Rollback Plan: feature flag, revert, compatibility mechanism, or DDL rollback
- Dependencies and Ownership: repos, teams, schema, release ordering
- Detailed Evidence: links to repo-local assessment artifacts
```

Line numbers drift, so include stable symbols, commit SHAs, SQL IDs, endpoint mappings, or Oracle object names alongside them.

## Initial Architectural Health Baseline Format

The first skill run should acknowledge the role and report only what discovery supports:

```markdown
# Initial Architectural Health Baseline

## Scope Confidence
- Repositories discovered: ...
- Repositories unavailable: ...
- Revisions pinned: ...
- Production telemetry available: yes/no/partial

## Layer Locations
| Layer | Repository | Primary paths/modules | Deployable | Confidence |
|---|---|---|---|---|
| Presentation | ... | ... | ... | ... |
| Service/Application | ... | ... | ... | ... |
| Persistence/Oracle | ... | ... | ... | ... |

## Coupling and Criticality Signals
- High fan-in/fan-out candidates: ...
- Shared database/schema coupling: ...
- Cross-repo release coupling: ...
- Critical runtime paths identified: ...

## Quality and Performance Evidence
- Test posture: ...
- Observability posture: ...
- Known incidents/defects: ...
- Performance baseline: ...

## Immediate Next Actions
1. Evidence acquisition with the highest decision value.
2. Confirmed containment opportunities.
3. Candidate low-cost regression protections.

## Limitations
- Unknowns and inaccessible evidence.
- Conclusions that remain hypotheses.
```

If a repository is empty or the application sources are unavailable, say so and stop short of inventing a baseline.

## Suggested Skill/Plugin Package

Create a compact skill with progressive disclosure rather than one oversized instruction file:

```text
legacy-stabilization/
├── SKILL.md
├── references/
│   ├── workflow.md
│   ├── detectors-angularjs.md
│   ├── detectors-spring.md
│   ├── detectors-oracle.md
│   ├── triage-model.md
│   └── artifact-schemas.md
├── scripts/
│   ├── inventory_workspace.py
│   ├── normalize_findings.py
│   └── validate_plan.py
└── agents/ or commands/              # platform-specific invocation metadata
```

Recommended skill description:

> Assess and stabilize complex legacy AngularJS, Java/Spring Boot, and Oracle polyrepos by mapping architecture, validating engineering and performance risks, prioritizing low-cost/high-impact remediation, and producing evidence-backed plans. Use for stabilization audits and narrowly scoped remediation planning; do not use for security reviews or greenfield redesign.

Keep platform-neutral logic in `SKILL.md` and `references/`. Treat Claude Code commands/hooks/subagents as optional adapters so the core workflow remains portable. If packaged as a Claude Code plugin, document the minimum supported Claude Code version and validate its current plugin manifest/command conventions against the installed version rather than hardcoding assumptions in this brief.

## Deterministic Helper Responsibilities

Use scripts only where repeatability is valuable:

- `inventory_workspace.py`: discover repositories, revisions, build roots, languages, and likely layer paths; emit JSON; never classify defects.
- `normalize_findings.py`: validate IDs, enum values, required evidence, duplicate fingerprints, and repo/commit coordinates.
- `validate_plan.py`: ensure every confirmed/planned finding has evidence, verification, rollback, cost/risk, and ownership fields; reject unresolved placeholders.

Scanners may emit candidates for human/agent validation. They must not write “confirmed” findings directly.

## Quality Gates for the Skill Itself

Test the skill against representative fixtures before relying on it:

1. A clean small application where scanners must avoid false positives.
2. An AngularJS fixture with both correctly cleaned and leaking listeners/watchers.
3. A Spring fixture with safe stateless singletons and unsafe request-specific instance state.
4. Transaction fixtures covering valid, missing, overly broad, and proxy-bypassed boundaries.
5. Oracle fixtures where a full scan is both optimal and harmful, proving the skill requires plan context.
6. An N+1 fixture with query-count evidence and a false-positive loop that uses an in-memory collection.
7. A multi-repo workflow with version skew and deployment-order constraints.
8. An empty/incomplete workspace where the skill reports limitations without fabricated findings.

Acceptance criteria:

- findings are reproducible and evidence-linked;
- no unsupported line numbers or runtime claims;
- recommended work is ordered by value, risk, and cost;
- the lowest sufficient intervention is selected;
- public contracts are preserved unless an approved exception is documented;
- implementation and audit modes remain distinct;
- plans remain usable after source lines move because stable identifiers and commit SHAs are present;
- verification and rollback are present for every planned change.

## Recommended First Milestone

Build the skill in assessment-only mode first. The first milestone should:

1. inventory a polyrepo workspace;
2. produce the architectural health baseline;
3. trace one critical runtime path;
4. identify and validate a small number of high-confidence candidates;
5. generate a ranked `REMEDIATION_MASTER_PLAN.md` without modifying application code;
6. validate the artifact schema and surface evidence gaps.

Only after the assessment output proves useful should the plugin add opt-in remediation commands. This keeps the initial tool safe, testable, and focused on decision quality.

