-- 043_six_layer_etl.sql
-- Layer: ADS report aggregating through 5 prior layers
WITH
l1_raw AS (
    SELECT * FROM ods.raw_sales WHERE dt={dt}
),
l2_clean AS (
    SELECT r.*, u.age_group, u.city
    FROM l1_raw r JOIN dim.users u ON r.user_id=u.user_id
),
l3_enrich AS (
    SELECT c.*, p.category_id, p.brand_id
    FROM l2_clean c JOIN dim.products p ON c.product_id=p.product_id
),
l4_agg_brand AS (
    SELECT brand_id, SUM(amount) AS brand_sales, COUNT(*) AS txn_cnt
    FROM l3_enrich GROUP BY brand_id
),
l5_rank AS (
    SELECT *, RANK() OVER (ORDER BY brand_sales DESC) AS brand_rank
    FROM l4_agg_brand
),
l6_top AS (
    SELECT * FROM l5_rank WHERE brand_rank <= {top_brands}
)
INSERT INTO ads.top_brand_report PARTITION (dt={dt})
SELECT l6.brand_id, b.brand_name, l6.brand_sales, l6.txn_cnt, l6.brand_rank, {dt} AS dt
FROM l6_top l6
JOIN dim.brands b ON l6.brand_id = b.brand_id;