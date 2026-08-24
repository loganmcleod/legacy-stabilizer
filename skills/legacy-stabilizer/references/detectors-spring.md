# Detectors — Spring Boot / Java

Candidate detectors for the service/application layer. Matches are leads. Attach
runtime or test evidence before raising confidence.

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
