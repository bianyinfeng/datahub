-- 012_union_funnel.sql
INSERT OVERWRITE TABLE dwd.event_funnel_all PARTITION (dt={dt})
SELECT user_id, 'view'     AS step, item_id, event_time, dt FROM ods.item_views   WHERE dt={dt}
UNION ALL
SELECT user_id, 'cart'     AS step, item_id, event_time, dt FROM ods.cart_actions  WHERE dt={dt} AND action='add'
UNION ALL
SELECT user_id, 'checkout' AS step, item_id, event_time, dt FROM ods.checkouts    WHERE dt={dt}
UNION ALL
SELECT user_id, 'purchase' AS step, order_id AS item_id, pay_time AS event_time, dt
FROM ods.payments WHERE dt={dt} AND pay_status='SUCCESS';