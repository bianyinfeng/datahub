-- 019_cache_table.sql
CACHE LAZY TABLE cached_active_users
AS
SELECT user_id, username, city, age_group, vip_level
FROM dwd.user_profile
WHERE is_active = 1
  AND vip_level >= {min_vip_level};

INSERT INTO ads.active_user_orders PARTITION (dt={dt})
SELECT
    u.user_id,
    u.username,
    u.city,
    u.vip_level,
    COUNT(o.order_id)    AS order_cnt,
    SUM(o.order_amount)  AS total_amt,
    {dt}                 AS dt
FROM cached_active_users u
JOIN dwd.orders o ON u.user_id = o.user_id
WHERE o.dt = {dt}
GROUP BY u.user_id, u.username, u.city, u.vip_level;

UNCACHE TABLE IF EXISTS cached_active_users;