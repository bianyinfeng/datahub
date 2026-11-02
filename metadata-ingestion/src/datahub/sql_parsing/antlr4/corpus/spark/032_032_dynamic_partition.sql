-- 032_dynamic_partition.sql
SET spark.sql.shuffle.partitions=200;
SET hive.exec.dynamic.partition=true;
SET hive.exec.dynamic.partition.mode=nonstrict;

INSERT OVERWRITE TABLE dwd.order_items_partitioned
PARTITION(year, month)
SELECT
    order_id, item_id, product_id, quantity, unit_price,
    pay_status, created_at,
    YEAR(created_at)  AS year,
    MONTH(created_at) AS month
FROM ods.order_items_raw
WHERE dt = {dt};