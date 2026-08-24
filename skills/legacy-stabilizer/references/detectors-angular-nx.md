# Detectors — Angular 17 & NX 17.3.x

Candidate detectors for the **modern** presentation layer: Angular 17 components
and the NX 17.3.x monorepo that builds them. For AngularJS 1.x see
`detectors-angularjs.md` — the two frameworks share almost no failure modes, so
do not carry an AngularJS assumption into Angular code. Every match here is a
**lead**, not a defect. Record an evidence state and attach the named proof
before raising confidence above `Candidate`.

## Angular 17 — what to look for

- **RxJS subscription leaks** — `.subscribe()` without teardown: no
  `takeUntilDestroyed`, no `takeUntil(destroy$)`, no `async` pipe, subscriptions
  held in long-lived services or route-reused components. The modern analogue of
  the AngularJS `$destroy` leak. Confirm with a heap snapshot / retained-listener
  count across repeated navigation, not by reading the code alone.
- **Change-detection pressure** — default (non-`OnPush`) change detection on
  hot component trees, function calls and impure pipes invoked from templates
  (re-run every cycle), heavy work inside getters bound in templates, unnecessary
  `zone.js`-triggering work. Corroborate with change-detection profiling.
- **HTTP outside a data-access service** — `HttpClient` called directly from
  components instead of a service, or without cancellation on navigation. Note
  duplicate or waterfall requests and missing `switchMap`/cancellation.
- **Shared mutable state** — mutable state on `providedIn: 'root'` singletons or
  cross-component `BehaviorSubject`s that create action-at-a-distance regressions.
  Also flag a service unintentionally provided at multiple levels (duplicate
  instances) or unintentionally shared.
- **Missing lazy loading / bundle bloat** — eagerly loaded feature routes,
  standalone components not lazily imported, large third-party libs in the
  initial bundle. Corroborate with the build's bundle/stats output.
- **NgModule / standalone drift** — inconsistent mix of NgModules and standalone
  components that duplicates providers or re-declares shared pieces.

## NX 17.3.x — what to look for

- **Module-boundary violations** — imports that cross `nx enforce-module-boundaries`
  tags (e.g. `feature` importing `app`, `scope:a` importing `scope:b`), or deep
  imports bypassing a lib's public `index.ts` barrel. Corroborate with the lint
  rule output, not by eye.
- **Circular dependencies** between projects or files — confirm with
  `nx graph` / the dep-graph, not a guess.
- **Missing or wrong project boundaries** — app-level code that belongs in a lib,
  or libs with no clear type tag (`feature`/`ui`/`data-access`/`util`), which
  defeats affected-build scoping.
- **Broken affected/caching assumptions** — implicit dependencies not declared in
  `nx.json` / `project.json`, so `nx affected` under-builds or the computation
  cache returns stale output. This is a correctness risk, not just speed.
- **Inconsistent tooling versions** across the workspace (Angular vs NX vs
  TypeScript) that produce build skew.

## Evidence that promotes a candidate

- static coordinates (project + file + line range + symbol);
- change-detection / RxJS profiling, or a heap snapshot with retained-subscription
  counts across repeated navigation;
- bundle/stats output for lazy-loading and size claims;
- `nx graph`, `nx affected --graph`, or `enforce-module-boundaries` lint output
  for any boundary, cycle, or affected-scope claim;
- a reproducible navigation loop that grows memory or subscription count.

## Do not

- Flag component or service size alone as a production risk.
- Assert a memory leak from a missing `unsubscribe` without a heap/listener count
  — the `async` pipe or `takeUntilDestroyed` may already handle teardown.
- Assert a module-boundary violation or a cycle without the NX graph/lint output.
- Recommend rewriting NgModules to standalone (or the reverse) for consistency
  alone — that is a modernization move, not a stabilization fix.
