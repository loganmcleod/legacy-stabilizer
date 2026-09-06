# Expected assessment — alloydb-nonsargable

## harmful.sql
- **Raise a `Candidate`, not a `Confirmed` defect.** `lower(email)` on an indexed
  column is non-sargable and a likely sequential scan on a large table.
- The assessment must **require an `EXPLAIN (ANALYZE, BUFFERS)` plan and the table
  row count** before asserting harm. No plan → stays `Candidate`. Check whether the
  column is columnar-eligible first — a columnar scan may already be fast.
- If confirmed: minimum intervention is a PostgreSQL **expression index** on
  `lower(email)` (not an Oracle function-based index), validated against the actual
  plan and weighed against write cost and bloat. Intervention level L4.
- Impact: `performance`.

## optimal.sql
- **Do not flag it.** A sequential scan of a ~250-row lookup table is optimal.
  Flagging "seq scan" here is a false positive.

## Pass criteria
Correct assessment does **not** confirm a scan defect from SQL text alone. It
requires a PostgreSQL execution plan and row-count evidence, treats `harmful.sql`
as a `Candidate`, clears `optimal.sql`, and does not carry Oracle plan/index
mechanics into AlloyDB.
