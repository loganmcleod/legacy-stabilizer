# Expected assessment — module-federation-skew

## skewed.webpack.config.js
- **Flag it.** Host pins the `react`/`react-dom` singletons to `^18.2.0`; the
  remote requires `^19.0.0`. Incompatible majors on a `singleton: true` share
  cause "invalid hook call" / two-copies-of-React failures at runtime.
- Status: `Candidate` on the config. Promote to `Confirmed` with the **resolved
  shared config across host + remote** and the **version actually loaded** at
  runtime (or a reproduced invalid-hook-call error) — not one `package.json`.
- Minimum intervention: align the `requiredVersion` ranges to one compatible major
  across host and remotes. Intervention level L3 (configuration).
- Impact: `reliability`, `regression`.

## aligned.webpack.config.js
- **Do not flag it.** Host and remote share `react`/`react-dom` as singletons on
  the same `^19.0.0` range. Correct federation setup.

## Pass criteria
Correct assessment flags only `skewed.webpack.config.js`, names the incompatible
singleton `requiredVersion` ranges, and requires the resolved cross-config version
(or a runtime reproduction) as confirming evidence — not the mere presence of a
shared `react` singleton.
