-- 027_gist_range.sql
-- Effective-dated dimension table with GiST range index
CREATE TABLE IF NOT EXISTS dim.product_price_history (
    price_id    BIGSERIAL   PRIMARY KEY,
    product_id  BIGINT      NOT NULL,
    price       NUMERIC(12,2) NOT NULL,
    cost        NUMERIC(12,2),
    valid_range DATERANGE   NOT NULL,
    EXCLUDE USING GIST (product_id WITH =, valid_range WITH &&)
);

CREATE INDEX IF NOT EXISTS idx_price_history_gist
    ON dim.product_price_history USING GIST (product_id, valid_range);

-- Query: find price at a specific date
SELECT p.product_id, p.product_name, ph.price, ph.cost
FROM dim.products p
JOIN dim.product_price_history ph
    ON p.product_id = ph.product_id
    AND ph.valid_range @> {query_date}::DATE
WHERE p.is_active = TRUE;