-- 039_tsvector_trigger.sql
-- Keep search_vector in sync automatically
CREATE OR REPLACE FUNCTION dwd.update_product_search_vector()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.search_vector :=
        SETWEIGHT(TO_TSVECTOR('chinese', COALESCE(NEW.product_name, '')), 'A')
        || SETWEIGHT(TO_TSVECTOR('chinese', COALESCE(NEW.description, '')), 'B')
        || SETWEIGHT(TO_TSVECTOR('chinese',
            COALESCE(NEW.attributes->>'brand', '') || ' ' ||
            COALESCE(NEW.attributes->>'tags', '')), 'C');
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_product_search_vector
    BEFORE INSERT OR UPDATE OF product_name, description, attributes
    ON dwd.product_catalog
    FOR EACH ROW
    EXECUTE FUNCTION dwd.update_product_search_vector();

INSERT INTO dwd.product_catalog (product_id, product_name, description, attributes, price, stock_qty)
SELECT
    product_id, product_name, description,
    jsonb_build_object('brand', brand_name, 'tags', tags),
    price, stock_qty
FROM staging.products_batch
WHERE batch_date = {batch_date};