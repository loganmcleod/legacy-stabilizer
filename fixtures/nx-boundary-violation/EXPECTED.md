# Expected assessment — nx-boundary-violation

## violation.feature-cart.ts
- **Raise a `Candidate`, not a `Confirmed` defect.** Two `@nx/enforce-module-boundaries`
  breaches: a deep import into `billing/data-access` that bypasses its public
  `index.ts` barrel, and a `type:feature` / `scope:checkout` file importing the
  `type:app` `scope:billing`/`scope:shop` layer — both forbidden by the summarized
  `depConstraints`.
- The assessment must **verify against the real workspace and the lint/graph
  output** before confirming: the tag config in `project.json` / `.eslintrc` and
  `nx lint` (or `nx graph`) showing the violation. The tag comments in the fixture
  are a summary, not proof; config alone → stays `Candidate`.
- If confirmed: minimum intervention is to route the dependency through an allowed
  public barrel (or move the shared code into a `scope:shared` / `type:util` lib).
  Intervention level L3 (module structure), not a rewrite.
- Impact: `maintainability`, `regression` (boundary erosion defeats affected-build
  scoping).

## allowed.feature-cart.ts
- **Do not flag it.** Both imports use public barrels and target tags the source tag
  is permitted to depend on (`type:data-access` in-scope, `scope:shared` util).
  Legal per `depConstraints`; `nx lint` reports no error.

## Pass criteria
Correct assessment flags only `violation.feature-cart.ts`, names both the deep
(barrel-bypassing) import and the forbidden tag crossing, and requires the NX lint
or `nx graph` output as confirming evidence — not eyeballed import paths. It clears
the allowed-import file and does not assert a boundary violation from an import
string alone.
