# Expected assessment — angular-rxjs-leak

## leaky.component.ts
- **Raise a `Candidate`, not a `Confirmed` defect.** Two `.subscribe()` calls with
  no teardown — no `takeUntilDestroyed`, no `takeUntil(destroy$)`, no `async` pipe.
  The `interval(...)` stream keeps emitting after destroy, so each navigation leaks
  a live subscription and a timer.
- The assessment must **require a heap snapshot or a retained-subscription count
  across repeated navigation** before asserting a leak. Source alone → stays
  `Candidate`; the teardown may live elsewhere.
- If confirmed: minimum intervention is `takeUntilDestroyed()` on the imperative
  subscription and the `async` pipe (or `takeUntilDestroyed`) for the template
  stream. Intervention level L3 (resource lifecycle).
- Impact: `reliability`, `performance`.

## clean.component.ts
- **Do not flag it.** The template stream uses the `async` pipe and the interval
  subscription is scoped with `takeUntilDestroyed`. Both teardowns present.
- Do **not** carry an AngularJS `$destroy` assumption into Angular 17 — the teardown
  mechanisms differ.

## Pass criteria
Correct assessment flags only `leaky.component.ts`, names the missing teardown, and
requires a heap/subscription count across navigation as confirming evidence — not
the mere presence of `.subscribe()`. It clears the `async` pipe / `takeUntilDestroyed`
version and does not assert a leak from a missing `unsubscribe` alone.
