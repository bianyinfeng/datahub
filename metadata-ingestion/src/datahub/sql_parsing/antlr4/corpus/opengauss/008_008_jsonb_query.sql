-- 008_jsonb_query.sql
-- Find products with specific attributes
INSERT INTO ads.premium_electronics
SELECT
    product_id,
    product_name,
    attributes->>'brand'                            AS brand,
    (attributes->>'weight_kg')::NUMERIC             AS weight_kg,
    attributes->'specs'->>'cpu'                     AS cpu_model,
    attributes->'specs'->>'ram_gb'                  AS ram_gb,
    attributes #>> '{warranty, months}'             AS warranty_months,
    price,
    stock_qty,
    CURRENT_DATE                                    AS loaded_at
FROM dwd.product_catalog
WHERE
    attributes @> '{"category": "electronics"}'
    AND (attributes->>'price')::NUMERIC > {min_price}
    AND attributes ? 'specs'
    AND (attributes->'specs'->>'ram_gb')::INTEGER >= {min_ram_gb}
    AND search_vector @@ plainto_tsquery('chinese', {search_keyword});