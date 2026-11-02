-- 018_cluster_by.sql
INSERT INTO dwd.item_view_clustered
SELECT
    item_id,
    user_id,
    view_duration,
    scroll_depth,
    source_channel,
    device_type,
    event_time
FROM ods.item_views
WHERE dt = {dt}
  AND view_duration > 0
CLUSTER BY item_id;