-- 010_rollup_agg.sql
INSERT INTO ads.sales_rollup PARTITION (dt={dt})
SELECT
    COALESCE(country, 'ALL') AS country,
    COALESCE(province, 'ALL') AS province,
    COALESCE(city, 'ALL') AS city,
    SUM(gmv)         AS total_gmv,
    SUM(order_cnt)   AS total_orders,
    COUNT(DISTINCT user_id) AS unique_buyers
FROM dws.order_geo_daily
WHERE dt = {dt}
GROUP BY ROLLUP(country, province, city);