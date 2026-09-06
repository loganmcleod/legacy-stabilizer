-- FALSE POSITIVE: a sequential scan that is optimal, not a defect.
--
-- country_codes is a tiny lookup table (~250 rows). PostgreSQL/AlloyDB will
-- sequential-scan it because that is cheaper than an index lookup — the planner
-- chooses it deliberately. Flagging "seq scan" here is exactly the mistake the
-- plan-required rule prevents. (An analytical scan of a large table can likewise
-- be served fast by AlloyDB's columnar engine — also not a defect.)
--
-- Context needed to clear it: country_codes has ~250 rows; seq scan is expected.
SELECT code, name
FROM   country_codes
ORDER  BY name;
