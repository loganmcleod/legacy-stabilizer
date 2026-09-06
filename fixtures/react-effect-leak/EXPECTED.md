# Expected assessment — react-effect-leak

## leaky.hook.jsx
- **Flag it.** The `useEffect` adds a `resize` listener and a `setInterval` and
  returns no cleanup, so both leak on every mount. The React analogue of the
  AngularJS `$destroy` leak.
- Status: `Candidate` on source. Promote to `Confirmed` with a **heap snapshot or
  retained-listener/timer count** growing across repeated mount/unmount.
- Minimum intervention: return a cleanup from the effect that calls
  `removeEventListener` and `clearInterval`. Intervention level L3 (resource
  lifecycle).
- Impact: `reliability`, `performance`.

## clean.hook.jsx
- **Do not flag it.** Same APIs, but the effect returns a cleanup that removes the
  listener and clears the interval. Correct code.

## Pass criteria
Correct assessment flags only `leaky.hook.jsx`, names the missing effect cleanup,
and cites a heap/listener count as the confirming evidence — not the mere presence
of `addEventListener`/`setInterval` inside `useEffect`.
