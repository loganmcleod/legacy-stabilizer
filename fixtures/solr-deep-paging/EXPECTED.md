# Expected assessment — solr-deep-paging

## harmful.query.txt
- **Raise a `Candidate`, not a `Confirmed` defect.** A large `start` offset
  (`start=100000`) forces SOLR to score and skip every prior document, so cost
  grows with depth. Classic deep-paging pattern.
- The assessment must **require timing evidence** before asserting harm: the SOLR
  slow-query log, `debugQuery=true` timing, or `QTime` rising with the offset. A
  large `start` in the query string alone → stays `Candidate`. A rarely-hit deep
  page on a small core may be harmless.
- If confirmed: minimum intervention is **`cursorMark` pagination** with a
  deterministic sort tiebreaker (for example `sort=price asc,id asc`). Intervention
  level L3 (query/usage), not a schema or infra change.
- Impact: `performance`, `scalability`.

## optimal.query.txt
- **Do not flag it.** `cursorMark` with a unique sort tiebreaker resumes from the
  sort position; per-page cost is flat regardless of depth. Correct pattern.

## Pass criteria
Correct assessment flags only `harmful.query.txt`, names the growing `start`
offset as the cause, requires timing evidence (slow-query log / `debugQuery` /
`QTime`) to promote past `Candidate`, and clears the `cursorMark` request.
