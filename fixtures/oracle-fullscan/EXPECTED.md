# Expected assessment — oracle-fullscan

## harmful.sql
- **Raise a `Candidate`, not a `Confirmed` defect.** `UPPER(email)` on an indexed
  column is non-sargable and a likely full scan on a large table.
- The assessment must **require an execution plan and the table row count** before
  asserting harm. No plan → stays `Candidate`.
- If confirmed: minimum intervention is a function-based index on `UPPER(email)` or
  a normalized comparison column — validated against the *actual* plan, accounting
  for write cost. Intervention level L4.
- Impact: `performance`.

## optimal.sql
- **Do not flag it.** A full scan of a ~250-row lookup table is optimal. Flagging
  "full scan" here is a false positive.

## Pass criteria
Correct assessment does **not** confirm a full-scan defect from SQL text alone. It
requires an execution plan and row-count evidence, treats `harmful.sql` as a
`Candidate`, and clears `optimal.sql`.
