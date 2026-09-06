# Detectors — AlloyDB (PostgreSQL) / Persistence

Candidate detectors for an **AlloyDB** data layer. AlloyDB is Google Cloud's
**PostgreSQL-compatible** engine, so PostgreSQL access patterns, SQL, and the
`EXPLAIN (ANALYZE, BUFFERS)` plan format apply. For Oracle 19c see
`detectors-oracle.md`. Like the Oracle detectors, these carry the **heaviest
evidence burden** in the workflow: most database claims require schema metadata and
an execution plan, not source inspection. Source inspection produces a lead only.

## AlloyDB context

- **PostgreSQL wire/SQL compatible** — most JPA/Hibernate/Spring JDBC/MyBatis code
  written for PostgreSQL runs unchanged. Confirm the actual dialect and driver
  (`org.postgresql` vs a Google connector) before assuming behavior.
- **Columnar engine** — AlloyDB can auto-populate an in-memory columnar store for
  analytical scans. A "full scan" that is slow on row storage may be served by the
  columnar engine; check whether the column is columnar-eligible before calling a
  sequential scan harmful.
- **Read pool vs primary** — AlloyDB serves reads from read-pool instances with
  replication lag. A "stale read" defect may be routing, not application logic;
  confirm which instance served the query.
- **Plan reading** — use `EXPLAIN (ANALYZE, BUFFERS)` and compare estimated vs
  actual rows. `pg_stat_statements` gives query frequency and total time. Autovacuum
  state and table bloat affect plans — check them before blaming the query.

## What to look for

- **N+1 query behavior** — ORM lazy-loading or DAO calls in a loop. Confirm with a
  query count (`pg_stat_statements` or an integration-test count), not by reading
  the loop — the collection may already be in memory.
- **String-built SQL** — SQL assembled by value concatenation or fragmented
  conditional strings. Harms correctness, plan stability, and testability; also a
  parameterization concern (noted structurally, not as a security finding).
- **Non-sargable predicates** — functions on indexed columns (`LOWER(col) = ...`
  without a matching expression index), implicit casts, leading-wildcard `LIKE`, or
  type mismatches that force a sequential scan. Confirm with a plan.
- **Missing / wrong indexes** — high-frequency predicates with no supporting index,
  or an index the planner ignores. Weigh a B-tree vs expression vs partial vs GIN
  index against write cost, bloat, and selectivity. Prove need with a plan.
- **Round-trip / fetch problems** — excessive round trips, over-fetching, unstable
  `OFFSET` pagination on large tables (prefer keyset), row-by-row processing.
- **Transaction / connection issues** — long transactions holding locks, idle-in-
  transaction connections, connection-pool exhaustion (HikariCP), plan regression,
  stale statistics, or table bloat — each only where evidence supports it.

## Evidence that promotes a candidate

- an `EXPLAIN (ANALYZE, BUFFERS)` plan (estimated vs actual rows, access method,
  buffers read);
- `pg_stat_statements` entry: calls, total/mean time, rows;
- a query-count assertion from an integration test;
- schema metadata: existing indexes, column types, table row counts, bloat/vacuum
  state, columnar-store eligibility;
- pool metrics (active/idle/wait) for a pool-exhaustion claim.

## Do not

- Assert a sequential scan is harmful without a plan. A seq scan can be optimal for
  small tables, low-selectivity queries, or columnar-served scans.
- Recommend an index without accounting for write cost, bloat, selectivity,
  existing indexes, and plan stability.
- Assume Oracle behavior. Hints, plan-baseline mechanics, and datatype rules differ
  — this is PostgreSQL.
