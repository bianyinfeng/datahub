-- 016_jsonb_update.sql
-- Update product attributes using JSONB operators
UPDATE dwd.product_catalog
SET
    attributes = attributes
        || jsonb_build_object('last_updated', CURRENT_TIMESTAMP::TEXT)
        || jsonb_build_object('price_history',
            COALESCE(attributes->'price_history', '[]'::JSONB)
            || jsonb_build_array(
                jsonb_build_object('price', price, 'ts', CURRENT_TIMESTAMP::TEXT)
            )
        ),
    updated_at = CURRENT_TIMESTAMP
WHERE product_id IN (
    SELECT product_id FROM staging.price_updates
    WHERE batch_date = {batch_date}
)
RETURNING product_id, attributes->>'last_updated' AS last_updated;