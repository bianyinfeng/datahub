-- 050_full_etl.sql
-- Full ETL: 8 source tables → complex aggregation → multiple outputs
BEGIN;

-- Step 1: Upsert products
MERGE INTO dwd.products AS t
USING staging.products_delta AS s ON t.product_id = s.product_id
WHEN MATCHED THEN UPDATE SET price=s.price, updated_at=CURRENT_TIMESTAMP
WHEN NOT MATCHED THEN INSERT (product_id, product_name, category_id, brand_id, price)
    VALUES (s.product_id, s.product_name, s.category_id, s.brand_id, s.price);

-- Step 2: Aggregate daily stats
INSERT INTO dws.daily_category_stats (dt, category_id, gmv, order_cnt, buyer_cnt)
WITH oi_enriched AS (
    SELECT
        oi.order_id, oi.product_id, oi.quantity*oi.unit_price AS revenue,
        p.category_id, o.user_id, o.dt
    FROM dwd.order_items oi
    JOIN dwd.products p  ON oi.product_id = p.product_id
    JOIN dwd.orders o    ON oi.order_id   = o.order_id
    WHERE o.dt = {dt} AND o.order_status = 'PAID'
)
SELECT
    dt,
    category_id,
    SUM(revenue)              AS gmv,
    COUNT(DISTINCT order_id)  AS order_cnt,
    COUNT(DISTINCT user_id)   AS buyer_cnt
FROM oi_enriched
GROUP BY dt, category_id
ON CONFLICT (dt, category_id) DO UPDATE
    SET gmv       = EXCLUDED.gmv,
        order_cnt = EXCLUDED.order_cnt,
        buyer_cnt = EXCLUDED.buyer_cnt;

-- Step 3: Refresh MV
REFRESH MATERIALIZED VIEW CONCURRENTLY ads.mv_daily_gmv;

-- Step 4: Update user RFM
UPDATE dwd.user_profile u
SET vip_level = CASE
    WHEN s.total_spent > {vip_threshold}  THEN 'VIP'
    WHEN s.total_spent > {gold_threshold} THEN 'GOLD'
    ELSE 'NORMAL'
END
FROM dws.user_lifetime_stats s
WHERE u.user_id = s.user_id
  AND s.stat_date = {dt};

COMMIT;