-- 028_skew_join.sql
INSERT INTO dws.heavy_user_orders PARTITION (dt={dt})
SELECT /*+ SKEW_JOIN(o, 'user_id', ({skew_user_ids})) */
    o.order_id,
    o.user_id,
    o.order_amount,
    u.vip_level,
    u.city
FROM dwd.orders o
JOIN dwd.user_profile u ON o.user_id = u.user_id
WHERE o.dt = {dt}
  AND o.order_amount > {min_amount};