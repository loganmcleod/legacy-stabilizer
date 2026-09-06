# Fixtures

Small, deliberately-constructed code samples that prove the detectors distinguish a
real defect from a look-alike that is not one. They exist for the project's own
quality bar (see the acceptance criteria in `docs/DESIGN_BRIEF.md`): the skill must
avoid false positives, and it must refuse to confirm database claims without runtime
evidence.

Each fixture directory holds a **true-positive** file, a **false-positive** file
that trips a naive scanner, and an `EXPECTED.md` stating what a correct assessment
must and must not conclude.

## How to use

Point the skill (or the `stabilization-assessor` subagent) at a fixture directory
and ask it to apply the relevant detector. A correct run:

- flags the true-positive as a `Candidate` with the required evidence named,
- does **not** flag the false-positive, and
- for the database and search/cache pairs, states that harm cannot be confirmed
  without runtime evidence (an execution plan, query timing, or load metrics).

Compare the result against `EXPECTED.md`.

## Fixtures

| Directory | Detector | Proves |
|---|---|---|
| `nplus1-java/` | Spring/persistence | N+1 query vs a loop over an in-memory collection |
| `angularjs-listener-leak/` | AngularJS | uncleaned `$on`/`$interval` vs cleanup on `$destroy` |
| `oracle-fullscan/` | Oracle | full scan needs a plan; small-table scan is fine |
| `react-effect-leak/` | React 19 | `useEffect` with no cleanup vs one returning a teardown |
| `module-federation-skew/` | Module Federation | incompatible `singleton` version vs aligned ranges |
| `alloydb-nonsargable/` | AlloyDB/PostgreSQL | non-sargable scan needs a plan; small-table scan is fine |
| `solr-deep-paging/` | SOLR 9.x | growing `start` offset vs `cursorMark` pagination |
| `redis-stampede/` | Redis 7.2 | cache-aside with no lock/no TTL jitter vs single-flight + jitter |
| `angular-rxjs-leak/` | Angular 17 | `.subscribe()` with no teardown vs `async` pipe / `takeUntilDestroyed` |
| `nx-boundary-violation/` | NX 17.3.x | import crossing `enforce-module-boundaries` tags vs allowed barrel import |

These cover every current detector. The design brief also lists stateless vs stateful singletons, transaction-boundary
variants, an empty workspace, and a multi-repo version-skew case.
