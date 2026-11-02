-- 019_sequence.sql
CREATE SEQUENCE IF NOT EXISTS dim.product_id_seq
    START WITH 10000001
    INCREMENT BY 1
    MINVALUE 10000001
    MAXVALUE 9999999999
    NO CYCLE
    CACHE 100;

CREATE TABLE IF NOT EXISTS dim.products (
    product_id      BIGINT          NOT NULL DEFAULT NEXTVAL('dim.product_id_seq'),
    product_name    VARCHAR(256)    NOT NULL,
    product_name_en VARCHAR(256),
    category_id     INTEGER         NOT NULL,
    brand_id        INTEGER         NOT NULL,
    supplier_id     INTEGER,
    price           NUMERIC(12,2)   NOT NULL,
    cost            NUMERIC(12,2),
    weight_kg       NUMERIC(8,3),
    is_active       BOOLEAN         NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_products PRIMARY KEY (product_id)
);

INSERT INTO dim.products (product_name, product_name_en, category_id, brand_id, price)
SELECT
    product_name, product_name_en, category_id, brand_id, price
FROM staging.new_products
WHERE validated = TRUE
  AND batch_date = {batch_date}
RETURNING product_id, product_name, created_at;