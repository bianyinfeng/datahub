-- 011_cube_agg.sql
INSERT INTO ads.product_cube PARTITION (dt={dt})
SELECT
    COALESCE(brand_name, 'ALL')    AS brand_name,
    COALESCE(category_name, 'ALL') AS category_name,
    COALESCE(price_band, 'ALL')    AS price_band,
    COUNT(DISTINCT product_id)     AS sku_cnt,
    SUM(sales_qty)                 AS total_qty,
    SUM(sales_amt)                 AS total_amt,
    AVG(avg_rating)                AS avg_rating
FROM dws.product_sales_daily
WHERE dt = {dt}
GROUP BY CUBE(brand_name, category_name, price_band);