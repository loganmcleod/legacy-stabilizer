# Detectors — Oracle / Persistence

Candidate detectors for the data layer. Targeted platform: **Oracle 19c**. These
carry the **heaviest evidence burden** in the whole workflow: most database claims
require schema metadata and an execution plan, not source inspection. Source
inspection produces a lead only.

## Oracle 19c context

19c actively reshapes plans at runtime — adaptive plans, real-time and automatic
statistics, SQL Plan Management baselines, and (on Enterprise Edition) automatic
indexing. A plan you read once may not be the plan that ran. So: capture the
*actual* plan for the SQL ID, check for an accepted SQL plan baseline before
proposing a hint or index, and account for bind peeking / cardinality feedback
before calling a plan "wrong".

## What to look for

- **N+1 query behavior** — ORM lazy-loading or DAO calls in a loop. Confirm with a
  query count, not by reading the loop (the collection may already be in memory).
- **String-built SQL** — SQL assembled by value concatenation or fragmented
  conditional strings. Harms correctness, plan stability, and testability.
- **Access path vs selectivity mismatch** — high-frequency/high-cost SQL whose
  plan does not match selectivity and available indexes.
- **Non-sargable predicates** — implicit conversions, functions on indexed
  columns, datatype mismatches, leading-wildcard `LIKE`, or other predicates that
  defeat index use.
- **Round-trip / fetch problems** — excessive round trips, over-fetching, unstable
  pagination, row-by-row processing.
- **Transaction / plan issues** — long transaction duration, lock contention, plan
  regression, cardinality-estimate errors, stale statistics — each only where
  evidence supports it.

## Evidence that promotes a candidate

- an execution plan (estimated vs actual rows, access method, logical reads);
- SQL ID and execution frequency;
- AWR/ASH report (only when authorized);
- a query-count assertion from an integration test;
- schema metadata: existing indexes, column types, table row counts.

## Do not

- Assert a full table scan is harmful without a plan. A full scan can be optimal
  for small tables or low-selectivity queries.
- Recommend an index without accounting for write cost, storage, selectivity,
  existing composite indexes, and plan stability.
- Propose a new bind or index before validating the *actual* Oracle plan.
