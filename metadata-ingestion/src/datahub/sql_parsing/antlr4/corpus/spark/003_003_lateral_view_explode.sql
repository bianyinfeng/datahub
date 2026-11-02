-- 003_lateral_view_explode.sql
INSERT INTO dwd.product_tag_flat
SELECT
    p.product_id,
    p.product_name,
    p.category_id,
    c.category_name,
    tag,
    p.price,
    p.stock_qty,
    TO_DATE(p.created_at) AS dt
FROM ods.products p
JOIN dim.categories c ON p.category_id = c.category_id
LATERAL VIEW EXPLODE(SPLIT(p.tags, ',')) tag_table AS tag
WHERE p.is_active = 1
  AND c.is_leaf = 1
  AND tag != '';