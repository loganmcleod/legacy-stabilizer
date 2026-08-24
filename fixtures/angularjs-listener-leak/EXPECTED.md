# Expected assessment — angularjs-listener-leak

## leaky.controller.js
- **Flag it.** `$rootScope.$on('cart:updated', ...)` discards its deregistration
  function and `$interval(...)` discards its handle, with no `$destroy` cleanup.
  Leaks a listener and a timer per instantiation.
- Status: `Candidate` on source. Promote to `Confirmed` with a **heap snapshot or
  listener/timer count** growing across repeated navigation.
- Minimum intervention: capture and release both on `$scope.$on('$destroy', ...)`.
  Intervention level L3 (resource lifecycle).
- Impact: `reliability`, `performance`.

## clean.controller.js
- **Do not flag it.** Same APIs, but the deregistration fn and interval promise are
  captured and cancelled on `$destroy`. Correct code.

## Pass criteria
Correct assessment flags only `leaky.controller.js`, names the missing `$destroy`
cleanup, and cites a heap/listener count as the confirming evidence — not the mere
presence of `$on`/`$interval`.
