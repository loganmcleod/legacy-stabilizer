# Expected assessment — nplus1-java

## TruePositive.java
- **Flag it.** `buildViews` calls `orderRepository.findLines(order.getId())` inside
  the loop → N+1.
- Status: `Candidate` on source inspection. Promote to `Confirmed` only with a
  **query-count assertion** (expect 1 + N queries).
- Minimum intervention: batch fetch (as in `FalsePositive`) or a join-fetch;
  assert query count drops to 2. Intervention level L4 (local fix), preceded by an
  L2 query-count characterization test.
- Impact: `performance`.

## FalsePositive.java
- **Do not flag it.** The only queries are `findOrders` and the batched
  `findLinesForOrders`; the loop touches an in-memory `Map`.
- A detector that flags this has produced a false positive — the failure this
  fixture guards against.

## Pass criteria
Correct assessment flags exactly one of the two files, names a query count as the
confirming evidence, and does not raise confidence above `Candidate` without it.
