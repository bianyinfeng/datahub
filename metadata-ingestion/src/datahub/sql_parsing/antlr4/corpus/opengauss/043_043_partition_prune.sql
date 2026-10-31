-- 043_partition_prune.sql
-- Efficiently query partitioned table
EXPLAIN ANALYZE
SELECT
    DATE_TRUNC('week', dt)::DATE AS week_start,
    region_id,
    COUNT(DISTINCT user_id)      AS unique_buyers,
    SUM(net_amount)              AS weekly_gmv
FROM dwd.orders
WHERE dt BETWEEN {start_date}::DATE AND {end_date}::DATE
  AND order_status = 'PAID'
  AND region_id = ANY(ARRAY[{region_ids}])
GROUP BY 1, 2
ORDER BY 1, weekly_gmv DESC;