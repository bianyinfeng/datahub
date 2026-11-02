-- 049_comprehensive.sql
-- Full data pipeline using all OpenGauss features
WITH
-- Use recursive CTE for region hierarchy
region_tree AS (
    SELECT region_id, parent_id, region_name, 0 AS depth
    FROM dim.regions WHERE parent_id IS NULL
    UNION ALL
    SELECT r.region_id, r.parent_id, r.region_name, rt.depth+1
    FROM dim.regions r JOIN region_tree rt ON r.parent_id=rt.region_id
),
-- Join orders with enriched data
enriched AS (
    SELECT
        o.order_id,
        o.user_id,
        u.username,
        u.vip_level,
        o.net_amount,
        o.dt,
        rt.region_name,
        p.attributes->>'brand' AS brand,
        p.search_vector @@ plainto_tsquery('chinese', {keyword}) AS is_keyword_match,
        ROW_NUMBER() OVER (PARTITION BY o.user_id ORDER BY o.net_amount DESC) AS rn
    FROM dwd.orders o
    JOIN dwd.user_profile u ON o.user_id = u.user_id
    JOIN dim.products p     ON o.product_id = p.product_id
    JOIN region_tree rt     ON u.region_id = rt.region_id
    WHERE o.dt = {dt}
      AND o.order_status = 'PAID'
      AND p.attributes @> jsonb_build_object('active', true)
)
INSERT INTO ads.comprehensive_report
SELECT order_id, user_id, username, vip_level, net_amount, region_name, brand, is_keyword_match
FROM enriched
WHERE rn <= {top_per_user}
RETURNING order_id, user_id;