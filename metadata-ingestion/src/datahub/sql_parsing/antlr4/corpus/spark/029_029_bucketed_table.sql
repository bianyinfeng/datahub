-- 029_bucketed_table.sql
CREATE TABLE IF NOT EXISTS dwd.orders_bucketed
USING parquet
CLUSTERED BY (user_id) SORTED BY (created_at DESC) INTO 256 BUCKETS
AS
SELECT
    order_id, user_id, product_id, order_amount, pay_channel,
    order_status, logistics_id, created_at,
    TO_DATE(created_at) AS dt
FROM dwd.orders
WHERE dt BETWEEN {start_dt} AND {end_dt};