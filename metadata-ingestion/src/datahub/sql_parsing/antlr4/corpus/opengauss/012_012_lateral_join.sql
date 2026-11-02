-- 012_lateral_join.sql
-- Get top 3 products per category using LATERAL
INSERT INTO ads.top_products_per_category (category_id, product_id, rank_in_cat, gmv)
SELECT
    c.category_id,
    top_p.product_id,
    top_p.rank_in_cat,
    top_p.gmv
FROM dim.categories c
CROSS JOIN LATERAL (
    SELECT
        oi.product_id,
        SUM(oi.quantity * oi.unit_price) AS gmv,
        ROW_NUMBER() OVER (ORDER BY SUM(oi.quantity * oi.unit_price) DESC) AS rank_in_cat
    FROM dwd.order_items oi
    JOIN dwd.products p ON oi.product_id = p.product_id
    WHERE p.category_id = c.category_id
      AND oi.dt = {dt}
    GROUP BY oi.product_id
    ORDER BY gmv DESC
    LIMIT {top_n}
) top_p
WHERE c.is_leaf = TRUE;