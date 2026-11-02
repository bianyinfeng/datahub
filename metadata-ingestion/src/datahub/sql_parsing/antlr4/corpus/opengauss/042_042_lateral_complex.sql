-- 042_lateral_complex.sql
INSERT INTO ads.user_recent_purchases
SELECT
    u.user_id,
    u.username,
    recent.last_order_id,
    recent.last_order_amount,
    recent.last_order_date,
    recent.product_names
FROM dwd.user_profile u
CROSS JOIN LATERAL (
    SELECT
        o.order_id AS last_order_id,
        o.net_amount AS last_order_amount,
        o.dt AS last_order_date,
        STRING_AGG(p.product_name, ', ' ORDER BY oi.line_amount DESC) AS product_names
    FROM dwd.orders o
    JOIN dwd.order_items oi ON o.order_id = oi.order_id
    JOIN dim.products p    ON oi.product_id = p.product_id
    WHERE o.user_id = u.user_id
      AND o.order_status = 'PAID'
    GROUP BY o.order_id, o.net_amount, o.dt
    ORDER BY o.dt DESC
    LIMIT 1
) recent
WHERE u.is_active = TRUE
  AND u.total_orders > 0;