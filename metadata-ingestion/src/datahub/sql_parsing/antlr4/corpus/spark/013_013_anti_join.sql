-- 013_anti_join.sql
-- Find users who browsed but never purchased (anti-join)
INSERT INTO ads.lapsed_browsers PARTITION (dt={dt})
SELECT DISTINCT
    b.user_id,
    b.last_browse_time,
    b.browse_count_7d,
    u.age_group,
    u.city,
    {dt} AS dt
FROM dws.browse_summary_7d b
LEFT ANTI JOIN dwd.orders o
    ON b.user_id = o.user_id
    AND o.created_at >= DATE_SUB({dt}, 7)
JOIN dwd.user_profile u ON b.user_id = u.user_id
WHERE b.dt = {dt};