# Detectors — Spring Boot / Java

Candidate detectors for the service/application layer. Targeted stack: **Java 21,
Spring Boot 2.7.18, Hibernate 5.6.x**. Matches are leads. Attach runtime or test
evidence before raising confidence.

## Version context (record, do not auto-remediate)

- **Spring Boot 2.7.18** is the last 2.7 patch and is past OSS end-of-life. Note
  the support status as a risk; do **not** make a framework upgrade the default
  remediation — it is an L6–L7 move requiring a decision record.
- **Java 21** virtual threads are **not** wired in by Spring Boot 2.7 (that
  arrived in Boot 3.2). Blocking I/O still runs on platform threads here, so
  pool-exhaustion detectors below still apply. If virtual threads were retrofitted
  by hand, watch for pinning inside `synchronized` blocks or held monitors.
- **Hibernate 5.6.x**: default `open-session-in-view` masks
  `LazyInitializationException` and hides N+1 behind the view. Check the
  `spring.jpa.open-in-view` setting and the batch fetch size before drawing
  conclusions.

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
