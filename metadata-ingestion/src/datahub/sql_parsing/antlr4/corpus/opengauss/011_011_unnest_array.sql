-- 011_unnest_array.sql
-- Expand product tags into individual rows
INSERT INTO dwd.product_tag_facts
SELECT
    p.product_id,
    p.product_name,
    TRIM(tag)                       AS tag,
    p.price,
    p.category_id,
    array_position(p.tags, TRIM(tag)) AS tag_ordinal,
    CURRENT_DATE                    AS dt
FROM dwd.product_catalog p
CROSS JOIN UNNEST(p.tags) AS t(tag)
WHERE p.stock_qty > 0
  AND TRIM(tag) <> ''
ON CONFLICT (product_id, tag) DO UPDATE
    SET tag_ordinal = EXCLUDED.tag_ordinal,
        dt = EXCLUDED.dt;