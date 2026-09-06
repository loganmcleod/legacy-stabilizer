# Detectors — SOLR 9.x Search & Redis 7.2 Cache

Candidate detectors for two supporting infrastructure layers that estates often
lean on: **Apache SOLR 9.x** full-text search and **Redis 7.2** caching (commonly
GCP Memorystore for Redis). Every match here is a **lead**. These layers usually
require runtime evidence — query timings, cache hit rates, slow logs — before a
claim is more than a `Candidate`.

## SOLR 9.x — what to look for

- **Slow or unbounded queries** — wildcard/leading-wildcard terms, deep faceting,
  huge `rows` values, or `fq` filters that are not cached. Confirm with the SOLR
  slow-query log or `debugQuery=true` timing, not by reading the query string.
- **Deep pagination** — large `start` offsets instead of cursor mark
  (`cursorMark`), which forces SOLR to score and skip everything up to the offset.
- **Commit strategy problems** — explicit `commit=true` per write (each triggers a
  hard commit and segment churn) instead of `commitWithin` / autoCommit +
  autoSoftCommit. A throughput and GC hazard. Corroborate with commit-rate metrics.
- **Schema / analyzer mismatch** — index-time and query-time analyzers that differ
  in a way that silently drops matches, or `string` vs `text` field choices that
  defeat the intended search. Confirm against the managed schema and a reproducible
  query.
- **Missing result/filter caching or over-large caches** — `filterCache`,
  `queryResultCache`, and `documentCache` sized wrongly for the workload (thrash or
  memory pressure). Corroborate with the SOLR cache stats (hit ratio, evictions).
- **Reliability gaps** — no timeout, retry, or fallback on the SOLR client; a
  SolrCloud collection with no replica so one node loss breaks search. Flag as a
  reliability lead; confirm with the cluster/collection state.
- **Index/DB drift** — search results that diverge from the system of record
  because indexing is best-effort or lags. Trace the indexing path like any
  cross-system boundary.

## Redis 7.2 — what to look for

- **Cache stampede / thundering herd** — many callers recomputing the same expired
  key at once, with no lock, single-flight, or staggered TTL. Confirm with a hit-
  rate drop and a backend load spike on expiry.
- **Missing or unbounded TTL** — keys set with no expiry, growing memory until
  eviction pressure; or an eviction policy (`maxmemory-policy`) that silently drops
  data the app assumes is durable. Redis is a cache, not the system of record —
  flag code that treats it as durable.
- **Blocking / O(N) commands on the hot path** — `KEYS`, large `SMEMBERS`/`HGETALL`,
  `FLUSHALL`, or Lua scripts that scan big structures on the request thread,
  stalling the single-threaded server for all clients. Prefer `SCAN`. Corroborate
  with the Redis slow log.
- **Connection handling** — a new connection per request instead of a pool
  (Lettuce/Jedis), or pool exhaustion under load. Confirm with connection metrics.
- **Serialization cost / big values** — large serialized blobs per key inflating
  network and memory; chatty multi-round-trip access instead of pipelining/`MGET`.
- **Cache-invalidation correctness** — stale entries because writes update the DB
  but not the cache (or vice versa), or no invalidation on the write path. Trace
  read-through/write-through/write-behind intent against the actual code.
- **GCP Memorystore specifics** — for managed Redis, note maxmemory policy,
  read-replica staleness, and failover behavior; a "lost data" symptom may be a
  failover or eviction, not app logic.

## Evidence that promotes a candidate

- SOLR slow-query log, `debugQuery=true` timings, cache stats (hit ratio,
  evictions), or collection/cluster state;
- Redis `INFO stats` (hit/miss, evicted_keys), the slow log, `maxmemory-policy`,
  and connection-pool metrics;
- a hit-rate drop correlated with a backend load spike (stampede);
- a reproducible slow query or a forced expiry/failover reproduction;
- static coordinates for the client call site (file + line + symbol).

## Do not

- Assert a slow SOLR query from the query string alone — get a timing or the slow
  log. A wildcard on a small core may be fine.
- Assert a Redis command is harmful without the slow log or `INFO` — a `KEYS` on a
  tiny keyspace in a maintenance job is not the same as one on the request path.
- Treat a cache miss or eviction as a defect by default — that is the cache doing
  its job unless the code wrongly assumes durability.
- Recommend replacing SOLR or Redis for consistency alone — that is modernization,
  not stabilization.
