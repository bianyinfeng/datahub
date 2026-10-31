-- 006_materialized_view.sql
CREATE MATERIALIZED VIEW IF NOT EXISTS ads.mv_daily_gmv AS
WITH daily_orders AS (
    SELECT
        DATE_TRUNC('day', created_at)::DATE     AS stat_date,
        user_id,
        order_id,
        order_amount,
        pay_channel,
        region_id,
        category_id
    FROM dwd.orders
    WHERE order_status = 'PAID'
)
SELECT
    stat_date,
    region_id,
    category_id,
    pay_channel,
    SUM(order_amount)               AS gmv,
    COUNT(DISTINCT order_id)        AS order_cnt,
    COUNT(DISTINCT user_id)         AS buyer_cnt,
    AVG(order_amount)               AS avg_order_value,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY order_amount) AS median_order_value
FROM daily_orders
GROUP BY stat_date, region_id, category_id, pay_channel
WITH DATA;

CREATE UNIQUE INDEX ON ads.mv_daily_gmv (stat_date, region_id, category_id, pay_channel);

REFRESH MATERIALIZED VIEW CONCURRENTLY ads.mv_daily_gmv;