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
- for the Oracle pair, states that harm cannot be confirmed without an execution
  plan.

Compare the result against `EXPECTED.md`.

## Fixtures

| Directory | Detector | Proves |
|---|---|---|
| `nplus1-java/` | Spring/persistence | N+1 query vs a loop over an in-memory collection |
| `angularjs-listener-leak/` | AngularJS | uncleaned `$on`/`$interval` vs cleanup on `$destroy` |
| `oracle-fullscan/` | Oracle | full scan needs a plan; small-table scan is fine |

These three cover the highest-value traps. The design brief lists five more
(stateless vs stateful singletons, transaction-boundary variants, an empty
workspace, and a multi-repo version-skew case) — add them as the skill matures.
