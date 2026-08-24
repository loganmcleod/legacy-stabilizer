-- FALSE POSITIVE: a full scan that is optimal, not a defect.
--
-- COUNTRY_CODES is a tiny lookup table (~250 rows). A full scan is cheaper than an
-- index lookup here — the optimizer chooses it deliberately. Flagging "full scan"
-- on this is exactly the mistake the plan-required rule prevents.
--
-- Context needed to clear it: COUNTRY_CODES has ~250 rows; full scan is expected.
SELECT code, name
FROM   country_codes
ORDER  BY name;
