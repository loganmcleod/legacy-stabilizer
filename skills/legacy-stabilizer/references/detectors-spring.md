# Detectors — Spring Boot / Java

Candidate detectors for the service/application layer. Targeted stack: **Java 21,
Spring Boot 2.7.18 and/or 3.5, Hibernate (5.6.x on Boot 2.7 / 6.x on Boot 3.x),
built with Maven 3.8+**. An estate may run both major Boot lines side by side.
Matches are leads. Attach runtime or test evidence before raising confidence.

## Version context (record, do not auto-remediate)

- **Establish the Boot line first.** Spring Boot 2.7 uses the `javax.*` namespace
  and Hibernate 5.6; Spring Boot 3.x uses `jakarta.*` and Hibernate 6.x. The
  namespace tells you which line a module is on — do not carry a 2.7 assumption
  into a 3.5 module or vice versa.
- **Spring Boot 2.7.18** is the last 2.7 patch and is past OSS end-of-life. Note
  the support status as a risk; do **not** make a framework upgrade the default
  remediation — it is an L6–L7 move requiring a decision record.
- **Spring Boot 3.5**: on `jakarta.*`, Hibernate 6.x, and Spring Framework 6.x.
  Virtual threads are available (`spring.threads.virtual.enabled`) — if enabled,
  watch for pinning inside `synchronized` blocks or held monitors, and note that
  the classic fixed-pool-exhaustion detector applies differently. Micrometer
  observability is built in; check whether it is actually wired before assuming
  telemetry exists. A mixed 2.7/3.5 estate has cross-line contract and dependency
  skew — trace shared libraries across both.
- **Java 21** virtual threads are **not** auto-wired by Spring Boot 2.7 (they
  arrived for MVC/`@Async` in Boot 3.2+). On 2.7, blocking I/O still runs on
  platform threads, so the pool-exhaustion detectors below apply. If virtual
  threads were retrofitted by hand, watch for monitor pinning.
- **Hibernate (5.6 / 6.x)**: default `open-session-in-view` masks
  `LazyInitializationException` and hides N+1 behind the view. Check the
  `spring.jpa.open-in-view` setting and the batch fetch size before drawing
  conclusions.
- **Maven 3.8+**: `http://` repositories are blocked by default; a build failing on
  a mirror or a dependency-version drift across modules is a build-reliability lead,
  not a runtime defect — keep it separate from stabilization fixes.

## What to look for

- **God service methods** — a single method combining policy, orchestration,
  persistence, mapping, retries, and side effects. Actionable when it demonstrably
  raises defect risk, coupling, or test cost — not for length alone.
- **Mutable state on singletons** — request-specific state held on singleton beans
  (instance fields mutated per request). A concurrency and correctness hazard.
- **Transaction boundary defects** — ambiguous, overly broad, or missing
  `@Transactional` around multi-step consistency requirements.
- **Proxy-bypassing self-invocation** — a bean calling its own `@Transactional`
  method internally, which skips the proxy and the transaction. Also watch
  unexpected propagation and remote calls held inside long transactions.
- **Chatty persistence / downstream** — repository calls in loops, excessive
  entity loading, N+1 via lazy associations, chatty downstream service calls.
- **Hibernate 5.6 lazy-loading traps** — `LazyInitializationException` outside a
  session, or the reverse: `open-in-view` silently keeping the session open and
  hiding N+1. Corroborate with a query count, and note the `open-in-view` setting
  and `default_batch_fetch_size`.
- **Blocking on constrained threads** — blocking I/O on request or fixed executor
  threads that can exhaust the pool.
- **Weak test seams** — critical behavior with hidden static/global dependencies
  that resist characterization tests.

## Evidence that promotes a candidate

- an integration test showing query count or call count;
- a thread/heap dump or pool-exhaustion trace;
- a reproduction of a transaction anomaly (partial commit, lost update);
- profiler output attributing latency to the method or call.

## Do not

- Classify an anemic domain model as a defect on style alone. It becomes
  actionable only when centralized procedural logic increases defect risk,
  coupling, test cost, or inconsistent rule enforcement.
- Assert a transaction is "too broad" without showing the held resource or
  contention it causes.
- Recommend splitting a class before extracting one pure function behind a
  characterization test.
