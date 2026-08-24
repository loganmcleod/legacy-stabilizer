# Stabilization Workflow — Phases 0–10

The full end-to-end process. `SKILL.md` links here; load this file when you need
the detail of a phase. Phases are gated: do not advance until the exit criterion
is met, and never run a remediation phase without explicit authorization recorded
in Phase 0.

Two modes exist and must stay distinct:

- **Assessment mode (default).** Read-only. Phases 0–6 plus plan generation. No
  production code, DDL, dependency, or contract changes.
- **Remediation mode (opt-in).** Phases 7–10. Requires an authorization line in
  the charter and works one small reversible batch at a time.

---

## Phase 0 — Charter, Scope, and Safety Boundaries

If `evidence/BACKGROUND_DOSSIER.md` exists (produced by the `stabilization-init`
skill), **read it first** and use it to pre-fill the charter — it already holds
the critical journeys, current symptoms, known bug leads, and the repository
paths. Confirm each pre-filled item with the user rather than treating it as
settled.

Define, in writing, before touching any code:

- Business-critical user journeys and current production symptoms.
- Target environments and repositories in scope, with explicit exclusions.
- Whether this run is **assessment-only** or **authorizes implementation** (name
  who authorized it and for which findings/repos).

Record this in `CHARTER.md` (seed from `templates/CHARTER.md`). The charter's Mode
and Authorization table are the gate that `stabilize-remediate` reads before any
code change.

Change boundaries that hold unless separately authorized:

- No production code changes during discovery.
- No database DDL, dependency upgrade, data migration, public-contract change, or
  deployment.
- No load testing against production.
- Redact credentials, personal data, customer data, and secrets from every artifact.
- Pin every finding to a repository and commit SHA so coordinates reproduce.

**Exit criterion:** the repository inventory and critical-runtime-path list are
complete enough that disconnected code is not audited as if it were production-critical.

---

## Phase 1 — Automated Topology and Build Mapping

Run `scripts/inventory_workspace.py <workspace>` to seed the inventory, then
corroborate. For each repository identify:

- build roots and module boundaries; deployable services, web apps, scheduled
  jobs, DB migration projects;
- AngularJS 1.x modules, routes, controllers, directives, services, factories,
  interceptors, templates;
- Angular 17 apps/libs, standalone components and NgModules, services, routes,
  HTTP clients/interceptors, and the NX 17.3.x workspace layout (`nx.json`,
  `project.json`, module-boundary tags, project dependency graph);
- Spring Boot 2.7 controllers, services, domain objects, Hibernate 5.6
  repositories/DAOs, transaction annotations, schedulers, listeners, integration
  clients; note the Java 21 / Boot 2.7 / Hibernate 5.6 versions in use;
- Oracle access paths: JPA, Hibernate, Spring JDBC, MyBatis, stored procedures,
  native SQL, dynamic SQL builders;
- cross-repo HTTP, messaging, shared-library, file, and database coupling;
- CI checks, test types, trustworthy coverage, release process, feature flags,
  observability hooks.

Use language-aware parsing when available. **Text search generates candidates; it
does not prove call relationships.**

**Deliverables:** system-context map, deployable/container map, repository
dependency graph, high fan-in/fan-out list, structural single points of failure —
each with evidence and confidence.

---

## Phase 2 — Establish the Operational Baseline

Collect evidence before recommending any performance work:

- incident themes, defect history, support tickets, rollback frequency, recent
  high-risk changes;
- endpoint latency distributions, throughput, error rate, saturation, JVM/GC
  metrics, browser performance, DB wait events;
- slow-query evidence, SQL IDs, AWR/ASH (when authorized), execution plans,
  logical reads, estimated vs actual rows, query frequency;
- existing unit/integration/contract/e2e/performance tests;
- reproducible failing cases for known defects.

If production telemetry is unavailable, **downgrade confidence explicitly** and
label any local measurement a proxy.

**Exit criterion:** each top-priority concern has either a measurable baseline or
an explicit evidence-acquisition task.

---

## Phase 3 — Critical Runtime-Path Tracing

Trace the few workflows that dominate customer impact or operational cost:

```
Angular 17 route/component or AngularJS route/template
  -> controller/component/directive
  -> client service / HTTP adapter
  -> Spring endpoint and request mapping
  -> application/service orchestration
  -> repository/DAO/stored procedure
  -> Oracle objects and SQL
  -> response mapping and UI state update
```

At every boundary record: input/output shape, validation and transformation,
state owner, sync and async side effects, transaction scope, retry behavior,
query count, error translation, existing tests. Note duplicated business rules and
hidden coupling — but do not recommend moving logic merely because it sits in a
legacy layer.

---

## Phase 4 — Targeted Defect Detection

Apply detectors *after* topology and path mapping, so results rank by real use.
See `detectors-angularjs.md`, `detectors-angular-nx.md`, `detectors-spring.md`,
`detectors-oracle.md`.

Everything a detector produces is a **Candidate** until corroborated. Assign an
evidence state: `Confirmed`, `Probable`, `Candidate`, `Not Reproducible`.

---

## Phase 5 — Normalize and Validate Findings

One canonical finding record per root cause, even when symptoms appear in multiple
repositories. Use the schema in `artifact-schemas.md`. Run
`scripts/normalize_findings.py findings.json` to check structure and flag
duplicate root-cause fingerprints. Deduplicate by root cause and affected runtime
path; link related symptoms rather than inflating the count.

---

## Phase 6 — Triage for Maximum Benefit at Minimum Cost

Score with the transparent model in `triage-model.md`, then apply judgment. The
default remediation order:

1. **Contain active harm** — leaks, runaway retries, duplicate work, uncontrolled
   query fan-out, thread/connection exhaustion, known data-consistency failures.
2. **Add observability and reproducibility** — measurements, focused
   logging/metrics, query-count assertions, deterministic failing cases.
3. **Create regression protection** — characterization, contract, integration,
   targeted performance tests around critical paths.
4. **Apply low-risk local fixes** — cleanup handlers, query batching/fetch tuning,
   parameterized SQL, bounded transactions, indexes proven by plans and workload,
   configuration corrections.
5. **Extract a test seam** — isolate side effects or policy only where needed to
   make the fix safe and testable.
6. **Structural decomposition** — only when smaller interventions cannot safely
   address the confirmed risk.
7. **Replacement / Strangler Fig** — only for persistently high-cost/high-risk
   areas with a stable seam, migration economics, parallel-run strategy, rollback.

**Assessment mode ends here** with a ranked `REMEDIATION_MASTER_PLAN.md`.

---

## Phase 7 — Design the Minimum Safe Remediation

Choose from the intervention ladder (`triage-model.md`), stopping at the lowest
level that meets the objective. Every recommendation must explain why lower levels
are insufficient. Levels 6–7 require explicit approval and a decision record
(seed from `templates/DECISION_RECORD.md`).

---

## Phase 8 — Implement in Small, Reversible Batches

For authorized changes only:

1. Pin the baseline revision and reproduce the issue.
2. Add or identify a failing/characterization test.
3. Make one cohesive change, limited file and repo scope.
4. Run focused tests, then the relevant broader suite.
5. Compare before/after correctness and performance evidence.
6. Verify cross-repo contracts and deployment ordering.
7. Document rollback, feature-flag, canary, or disablement mechanics.
8. Update finding status only after evidence is captured.

Never mix dependency upgrades, formatting, renames, or architectural cleanup into
a stabilization change.

---

## Phase 9 — Release and Verify

Risk-proportional release: feature flag, dark read, shadow traffic, canary,
percentage rollout, or standard deploy with enhanced monitoring. Define expected
signals and rollback thresholds in advance.

Verification must cover: original behavior and edge cases; performance delta at
representative load and data volume; DB plan/query-count stability; error,
timeout, retry, partial-failure behavior; resource cleanup after repeated
navigation/requests; production signals over an agreed window.

Close a finding only when success criteria are met. **"Code merged" is not
verification.**

---

## Phase 10 — Prevent Recurrence

Add narrowly scoped safeguards supported by actual findings: ArchUnit rules for
validated boundaries; query-count assertions for known N+1 flows; lint/custom
checks for lifecycle cleanup; contract tests at high-risk cross-repo interfaces;
performance budgets for critical endpoints/workflows; DB plan monitoring for a
small set of business-critical SQL; ownership metadata and decision records for
fragile components.

Do not create broad rules that produce noise or freeze legitimate legacy patterns.
Run `scripts/validate_plan.py findings.json --plan REMEDIATION_MASTER_PLAN.md`
before declaring the plan decision-ready.
