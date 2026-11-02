-- 009_posexplode.sql
INSERT INTO dwd.order_item_flat
SELECT
    o.order_id,
    o.user_id,
    item_pos,
    item.product_id,
    item.quantity,
    item.unit_price,
    item.quantity * item.unit_price AS line_amount,
    TO_DATE(o.created_at) AS dt
FROM ods.orders_json o
LATERAL VIEW POSEXPLODE(FROM_JSON(o.items_json,
    'array<struct<product_id:string,quantity:int,unit_price:decimal(18,2)>>'))
    items_table AS item_pos, item
WHERE o.dt = {order_date};