# Detectors — AngularJS 1.x

Candidate detectors for the presentation layer. Every match is a **lead**, not a
defect. Record an evidence state and attach the proof named below before raising
confidence above `Candidate`.

## What to look for

- **Oversized controllers/directives** — excessive size, responsibility count,
  dependency count, or change frequency. Size is a *review trigger*, not a defect.
  A 1,500-line controller earns a look; a 40-line one may still be the true
  orchestration bottleneck.
- **Direct `$http` outside a data-access service** — network calls scattered in
  controllers/directives instead of a dedicated client/service. Note: templates
  normally cannot inject `$http`; distinguish template expressions from
  controller/directive code before flagging.
- **Uncleaned resources on `$destroy`** — event listeners, `$interval`/`$timeout`,
  DOM/plugin handlers, and custom `$watch` registrations not released. These are
  the classic AngularJS memory leaks.
- **Digest pressure** — high watcher count, deep watches (`$watch(..., true)`),
  collection watches (`$watchCollection`), watch functions that allocate or
  trigger work, and digest feedback loops.
- **Redundant / expensive work** — repeated network calls, route-level
  waterfalls, duplicated state, and expensive filters/functions invoked directly
  from templates (re-run every digest).
- **Shared mutable state** — mutable state on services or `$rootScope` that
  creates action-at-a-distance regressions.

## Evidence that promotes a candidate

- static coordinates (file + line range + symbol);
- watcher profiling / digest timing;
- heap snapshots and detached-DOM-node counts across repeated navigation;
- network traces showing duplicate or waterfall calls;
- a reproducible navigation loop that grows memory or watcher count.

## Do not

- Flag controller size alone as a production risk.
- Assume a template can inject `$http`.
- Recommend a component-framework migration before trying a compatible service
  wrapper with cancellation and `$destroy` cleanup (see intervention ladder).
