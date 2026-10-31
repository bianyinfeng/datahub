-- 031_multi_insert.sql
FROM dwd.orders o
JOIN dwd.user_profile u ON o.user_id = u.user_id
WHERE o.dt = {dt}
INSERT OVERWRITE TABLE ads.vip_orders PARTITION(dt={dt})
SELECT o.order_id, o.user_id, o.order_amount, u.vip_level
WHERE u.vip_level = 'VIP'
INSERT OVERWRITE TABLE ads.regular_orders PARTITION(dt={dt})
SELECT o.order_id, o.user_id, o.order_amount, u.vip_level
WHERE u.vip_level != 'VIP';