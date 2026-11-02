-- 044_merge_jsonb.sql
MERGE INTO dwd.product_catalog AS t
USING (
    SELECT
        product_id,
        product_name,
        price,
        attributes,
        updated_at
    FROM staging.product_updates_delta
    WHERE batch_date = {batch_date}
) AS s
ON t.product_id = s.product_id
WHEN MATCHED AND s.updated_at > t.updated_at THEN
    UPDATE SET
        product_name = s.product_name,
        price        = s.price,
        attributes   = t.attributes || s.attributes,
        updated_at   = s.updated_at
WHEN NOT MATCHED THEN
    INSERT (product_id, product_name, price, attributes, stock_qty)
    VALUES (s.product_id, s.product_name, s.price, s.attributes, 0);