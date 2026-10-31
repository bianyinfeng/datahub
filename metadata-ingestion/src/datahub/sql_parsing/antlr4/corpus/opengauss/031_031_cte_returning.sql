-- 031_cte_returning.sql
-- Multi-step upsert with RETURNING chain
WITH inserted_orders AS (
    INSERT INTO dwd.orders (user_id, product_id, order_amount, order_status, created_at)
    SELECT user_id, product_id, order_amount, 'PENDING', CURRENT_TIMESTAMP
    FROM staging.new_orders
    WHERE batch_date = {batch_date}
    RETURNING order_id, user_id, order_amount
),
inserted_items AS (
    INSERT INTO dwd.order_items (order_id, product_id, quantity, unit_price)
    SELECT io.order_id, ni.product_id, ni.quantity, ni.unit_price
    FROM inserted_orders io
    JOIN staging.new_order_items ni ON io.user_id = ni.user_id
    RETURNING order_id, product_id, quantity
)
INSERT INTO dwd.audit_log (entity_type, entity_id, action, details, created_at)
SELECT 'ORDER', order_id::TEXT, 'CREATED',
       json_build_object('amount', order_amount)::TEXT,
       CURRENT_TIMESTAMP
FROM inserted_orders;