-- 008_complex_join.sql
INSERT INTO dws.order_enriched_daily PARTITION (dt={stat_date})
SELECT
    o.order_id,
    o.user_id,
    u.username,
    u.age_group,
    u.city             AS user_city,
    o.product_id,
    p.product_name,
    p.brand_id,
    b.brand_name,
    p.category_id,
    c.category_path,
    o.order_amount,
    o.discount_amount,
    o.net_amount,
    o.pay_channel,
    o.logistics_id,
    l.logistics_company,
    l.logistics_status,
    o.created_at,
    {stat_date}        AS dt
FROM dwd.orders o
JOIN dwd.user_profile      u ON o.user_id    = u.user_id
JOIN dwd.products          p ON o.product_id = p.product_id
JOIN dim.brands            b ON p.brand_id   = b.brand_id
JOIN dim.categories        c ON p.category_id= c.category_id
LEFT JOIN dwd.logistics    l ON o.logistics_id = l.logistics_id
WHERE o.dt = {stat_date}
  AND o.order_status NOT IN ('CANCELLED', 'INVALID');