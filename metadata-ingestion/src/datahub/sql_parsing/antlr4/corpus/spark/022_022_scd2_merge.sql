-- 022_scd2_merge.sql
MERGE INTO dim.product_scd2 AS t
USING (
    SELECT
        product_id,
        product_name,
        category_id,
        brand_id,
        price,
        cost,
        supplier_id,
        CURRENT_TIMESTAMP() AS effective_start,
        '9999-12-31'        AS effective_end,
        TRUE                AS is_current
    FROM staging.product_updates
    WHERE batch_date = {batch_date}
      AND changed_flag = 1
) AS s
ON t.product_id = s.product_id AND t.is_current = TRUE
WHEN MATCHED AND (
    t.product_name <> s.product_name OR
    t.price <> s.price OR
    t.category_id <> s.category_id
) THEN
    UPDATE SET
        t.effective_end = DATE_SUB(s.effective_start, 1),
        t.is_current    = FALSE
WHEN NOT MATCHED THEN
    INSERT (product_id, product_name, category_id, brand_id, price, cost,
            supplier_id, effective_start, effective_end, is_current)
    VALUES (s.product_id, s.product_name, s.category_id, s.brand_id, s.price,
            s.cost, s.supplier_id, s.effective_start, s.effective_end, s.is_current);