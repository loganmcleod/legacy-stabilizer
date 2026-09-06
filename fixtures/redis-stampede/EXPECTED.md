# Expected assessment — redis-stampede

## harmful.cache.js
- **Raise a `Candidate`, not a `Confirmed` defect.** Cache-aside with no
  single-flight lock on the load path: N concurrent misses run N identical DB
  queries (cache stampede). The fixed, un-jittered TTL compounds it — keys loaded
  together expire together and re-stampede on the same tick.
- The assessment must **require runtime evidence** before asserting harm: a DB
  query spike aligned to TTL expiry, Redis keyspace-miss metrics, or a reproduced
  thundering herd under concurrent load. Code shape alone → stays `Candidate`. A
  low-traffic key may never stampede in practice.
- If confirmed: minimum intervention is a **single-flight lock** (`SET NX`) on the
  load path plus **TTL jitter**. Intervention level L3 (usage pattern). Consider
  the lock's own failure modes (timeout, orphaned lock) when weighing it.
- Impact: `performance`, `scalability`, `reliability`.

## optimal.cache.js
- **Do not flag it.** The load path takes an `NX` lock (single-flight) and applies
  per-key TTL jitter. Both stampede guards are present. Correct pattern.

## Pass criteria
Correct assessment flags only `harmful.cache.js`, names both the missing
single-flight lock and the un-jittered fixed TTL, requires runtime evidence (DB
spike at expiry / miss metrics / reproduced herd) to promote past `Candidate`,
and clears the lock-plus-jitter version.
