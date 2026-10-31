-- 047_partition_wise_join.sql
-- Both tables partitioned by user_id for partition-wise join
SET enable_partitionwise_join = on;

INSERT INTO ads.user_order_product_matrix
SELECT
    o.user_id,
    o.order_id,
    oi.product_id,
    p.category_id,
    oi.quantity,
    oi.unit_price,
    o.created_at::DATE AS dt
FROM dwd.orders o
JOIN dwd.order_items oi ON o.order_id = oi.order_id
JOIN dim.products p     ON oi.product_id = p.product_id
WHERE o.dt = {dt}
  AND o.order_status = 'PAID';