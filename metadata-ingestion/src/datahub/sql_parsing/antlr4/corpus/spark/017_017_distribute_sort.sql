-- 017_distribute_sort.sql
INSERT OVERWRITE TABLE dwd.user_behavior_sorted
SELECT
    user_id,
    behavior_type,
    item_id,
    item_category,
    event_time,
    device_type,
    source_channel
FROM ods.user_behavior_log
WHERE dt = {dt}
  AND behavior_type IN ('click','buy','collect','share')
DISTRIBUTE BY user_id
SORT BY user_id, event_time;