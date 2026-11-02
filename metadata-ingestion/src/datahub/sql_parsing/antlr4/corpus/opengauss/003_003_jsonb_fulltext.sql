-- 003_jsonb_fulltext.sql
-- Enrich product catalog with JSONB attributes and full-text index
CREATE TABLE IF NOT EXISTS dwd.product_catalog (
    product_id      BIGINT          PRIMARY KEY,
    product_name    VARCHAR(256)    NOT NULL,
    description     TEXT,
    attributes      JSONB           NOT NULL DEFAULT '{}',
    tags            TEXT[],
    price           NUMERIC(12,2)   NOT NULL,
    stock_qty       INTEGER         NOT NULL DEFAULT 0,
    search_vector   TSVECTOR,
    created_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_product_attrs_gin
    ON dwd.product_catalog USING GIN (attributes);
CREATE INDEX IF NOT EXISTS idx_product_search
    ON dwd.product_catalog USING GIN (search_vector);
CREATE INDEX IF NOT EXISTS idx_product_tags
    ON dwd.product_catalog USING GIN (tags);

INSERT INTO dwd.product_catalog (product_id, product_name, description, attributes, tags, price, stock_qty, search_vector)
SELECT
    p.product_id,
    p.product_name,
    p.description,
    jsonb_build_object(
        'brand',    p.brand_name,
        'color',    p.color,
        'size',     p.size_info,
        'material', p.material,
        'weight_kg', p.weight_kg,
        'country_of_origin', p.origin_country
    ) AS attributes,
    STRING_TO_ARRAY(p.tags, ',') AS tags,
    p.price,
    p.stock_qty,
    to_tsvector('chinese', COALESCE(p.product_name,'') || ' ' || COALESCE(p.description,''))
FROM staging.products_raw p
WHERE p.is_active = TRUE
ON CONFLICT (product_id) DO UPDATE
    SET product_name   = EXCLUDED.product_name,
        attributes     = EXCLUDED.attributes,
        search_vector  = EXCLUDED.search_vector,
        updated_at     = CURRENT_TIMESTAMP;