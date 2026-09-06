-- POTENTIALLY HARMFUL sequential scan — but this is a LEAD, not a confirmed defect.
--
-- lower(email) on an indexed column makes the predicate non-sargable: a plain
-- B-tree index on email cannot serve it, so AlloyDB (PostgreSQL) sequential-scans
-- a large table. Classic pattern. It MUST be confirmed with an actual plan and the
-- table row count before asserting harm.
--
-- Context needed to confirm: customers has ~20M rows; a B-tree index exists on
-- email; the column is NOT in the columnar store (so no columnar acceleration).
-- Confirm with: EXPLAIN (ANALYZE, BUFFERS) SELECT ... ;  and pg_stat_statements.
SELECT customer_id, email, status
FROM   customers
WHERE  lower(email) = lower(:email);

-- Sargable rewrite to validate against the ACTUAL plan (PostgreSQL semantics):
--   CREATE INDEX ix_customers_email_lower ON customers (lower(email));
-- i.e. an EXPRESSION index matching the predicate — not an Oracle function-based
-- index; account for write cost and bloat before creating it.
