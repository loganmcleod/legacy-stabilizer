# Detectors — React 19 & Webpack 5 Module Federation

Candidate detectors for a **React 19** presentation layer and for micro-frontends
(MFEs) composed with **Webpack 5 Module Federation**. For AngularJS 1.x see
`detectors-angularjs.md`; for Angular 17 / NX see `detectors-angular-nx.md`. The
three frameworks share almost no failure modes — do not carry an Angular
assumption into React code. Every match here is a **lead**, not a defect. Record an
evidence state and attach the named proof before raising confidence above
`Candidate`.

## React 19 — what to look for

- **Effect cleanup leaks** — `useEffect` that subscribes (event listener,
  interval, WebSocket, observable, `AbortController`) without returning a cleanup
  function, or a cleanup that does not match the subscription. The React analogue
  of the AngularJS `$destroy` leak. Confirm with a heap snapshot / retained-listener
  count across repeated mount/unmount, not by reading the code alone.
- **Unstable references causing re-render** — new object/array/function literals
  passed as props or effect deps every render, missing `useMemo`/`useCallback` on a
  hot path, context values recreated each render forcing all consumers to re-render.
  Corroborate with the React Profiler (commit count / render duration), not by eye.
- **Data fetching in effects without cancellation** — `fetch`/axios in `useEffect`
  with no `AbortController` or stale-response guard; duplicate or waterfall requests
  on navigation; fetching in a component instead of a data-access hook/service.
- **Missing key / index-as-key on dynamic lists** — reconciliation churn and state
  bleed between rows. Flag as a lead; confirm with a re-render or state-corruption
  reproduction.
- **Shared mutable module state** — mutable singletons in a module scope or a
  context provider used as a global store, creating action-at-a-distance
  regressions across routes.
- **Legacy-pattern drift under React 19** — class components with deprecated
  lifecycles, `unmountComponentToNode`/legacy `ReactDOM.render` instead of
  `createRoot`, patterns that break under Strict Mode's double-invoke. Note as a
  version/compat risk; do **not** make a rewrite the default remediation.

## Webpack 5 Module Federation (MFE) — what to look for

- **Singleton version skew** — a `shared` dependency (React, React DOM, a router,
  a design system) marked `singleton: true` but with incompatible
  `requiredVersion` ranges across host and remotes, causing runtime "two copies of
  React" / invalid-hook-call errors. Confirm with the built federation config and a
  loaded-version check, not by reading one `package.json`.
- **Unshared heavy dependencies** — the same large library bundled into multiple
  remotes because it is not in `shared`, inflating total transferred bytes.
  Corroborate with bundle/stats output across the host and remotes.
- **Remote load failure handling** — a host that mounts a remote with no error
  boundary, timeout, or fallback, so one remote's fetch failure blanks the shell.
  Flag as a reliability lead; confirm with a forced remote-outage reproduction.
- **Eager vs lazy remote loading** — `eager: true` on shared modules or
  synchronous remote imports that defeat lazy loading and bloat the host's initial
  bundle. Corroborate with stats output.
- **Contract drift between host and remote** — the shape a host expects from an
  exposed module differs from what the remote exposes (props, event names, mount
  signature). This is a cross-repo contract; trace it like any other boundary and
  do not change it without a contract test.
- **Duplicated / conflicting global state** — shared state (auth, feature flags,
  theme) held independently in each MFE instead of via a shared singleton,
  producing inconsistent UI across federated fragments.

## Evidence that promotes a candidate

- static coordinates (package + file + line range + symbol);
- React Profiler output (commit count, render duration) for re-render claims;
- a heap snapshot with retained-listener/detached-node counts across repeated
  mount/unmount for a leak claim;
- bundle/stats output (`webpack --json`, `webpack-bundle-analyzer`) for size and
  shared-dependency claims;
- the resolved Module Federation config (host + each remote) and the actual loaded
  version for any singleton/skew claim;
- a forced remote-outage or version-mismatch reproduction.

## Do not

- Flag component or hook count alone as a production risk.
- Assert a memory leak from a missing cleanup without a heap/listener count.
- Assert singleton version skew from a single `package.json` — check the resolved
  federation `shared` config and the version actually loaded at runtime.
- Recommend migrating class components to hooks, or restructuring the federation
  topology, for consistency alone — that is modernization, not a stabilization fix.
