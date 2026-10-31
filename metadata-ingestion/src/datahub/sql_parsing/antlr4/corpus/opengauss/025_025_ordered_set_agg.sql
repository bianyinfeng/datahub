-- 025_ordered_set_agg.sql
INSERT INTO ads.order_amount_percentiles (dt, category_id, p25, p50, p75, p90, p95, p99)
SELECT
    dt,
    category_id,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY net_amount) AS p25,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY net_amount) AS p50,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY net_amount) AS p75,
    PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY net_amount) AS p90,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY net_amount) AS p95,
    PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY net_amount) AS p99
FROM dwd.orders
WHERE order_status = 'PAID'
  AND dt BETWEEN {start_date} AND {end_date}
GROUP BY dt, category_id;