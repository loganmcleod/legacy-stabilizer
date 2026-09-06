// TRUE POSITIVE: cache-aside with no single-flight and no TTL jitter.
//
// On a miss, every concurrent caller runs the expensive DB query and writes the
// same key. Under load (cold start, or the moment a hot key expires) this is a
// cache stampede: hundreds of identical queries hit the DB at once. All keys also
// share one fixed TTL, so entries loaded together expire together and re-stampede
// on the same tick.
//
// This is a LEAD, not a confirmed defect. Confirm with runtime evidence, not the
// code shape: a DB query spike aligned to TTL expiry, Redis keyspace-miss metrics,
// or a reproduced thundering herd under concurrent load.

const TTL_SECONDS = 3600; // fixed, no jitter — synchronized expiry across keys

async function getProduct(id) {
  const key = `product:${id}`;
  const cached = await redis.get(key);
  if (cached) return JSON.parse(cached);

  // No lock / no single-flight: N concurrent misses => N identical DB queries.
  const product = await db.query('SELECT * FROM products WHERE id = $1', [id]);
  await redis.set(key, JSON.stringify(product), 'EX', TTL_SECONDS);
  return product;
}

module.exports = { getProduct };
