-- POTENTIALLY HARMFUL full scan — but this is a LEAD, not a confirmed defect.
--
-- UPPER() on an indexed column makes the predicate non-sargable: the index on
-- EMAIL cannot be used, so Oracle full-scans a large table. This is the classic
-- pattern. It still MUST be confirmed with an execution plan and the table's row
-- count before asserting harm.
--
-- Context needed to confirm: CUSTOMERS has ~20M rows; an index exists on EMAIL.
SELECT customer_id, email, status
FROM   customers
WHERE  UPPER(email) = UPPER(:email);

-- Sargable rewrite to validate against the actual plan:
--   store/compare a normalized column, or use a function-based index on UPPER(email).
