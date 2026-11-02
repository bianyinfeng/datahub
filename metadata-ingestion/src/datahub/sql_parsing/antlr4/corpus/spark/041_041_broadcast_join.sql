-- 041_broadcast_join.sql
INSERT INTO dws.enriched_clicks PARTITION (dt={dt})
SELECT /*+ BROADCAST(dim_items) */
    c.click_id,
    c.user_id,
    c.item_id,
    i.item_name,
    i.category_id,
    i.brand_id,
    c.click_time,
    c.source_channel
FROM dwd.click_logs c
JOIN dim.items i ON c.item_id = i.item_id
WHERE c.dt = {dt};