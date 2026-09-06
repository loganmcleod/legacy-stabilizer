// FALSE POSITIVE: cache-aside protected against stampede. Do not flag it.
//
// Two guards close the herd window:
//   1. Single-flight lock (SET NX): only the first concurrent miss loads from the
//      DB; the others wait and re-read the freshly populated key.
//   2. Jittered TTL: keys loaded together get slightly different lifetimes, so
//      they do not all expire on the same tick.
//
// Context needed to clear it: NX lock on the load path and per-key TTL jitter are
// both present. This is the correct concurrent cache-aside pattern.

const BASE_TTL = 3600;
const jitter = (id) => BASE_TTL + (hash(id) % 300); // spread expiry +/- up to 5 min

async function getProduct(id) {
  const key = `product:${id}`;
  const cached = await redis.get(key);
  if (cached) return JSON.parse(cached);

  const lockKey = `lock:${key}`;
  const gotLock = await redis.set(lockKey, '1', 'NX', 'EX', 10);
  if (!gotLock) {
    await sleep(50);        // another caller is loading; wait and re-read
    return getProduct(id);
  }
  try {
    const product = await db.query('SELECT * FROM products WHERE id = $1', [id]);
    await redis.set(key, JSON.stringify(product), 'EX', jitter(id));
    return product;
  } finally {
    await redis.del(lockKey);
  }
}

module.exports = { getProduct };
