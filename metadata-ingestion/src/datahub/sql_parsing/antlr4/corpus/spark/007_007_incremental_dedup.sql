-- 007_incremental_dedup.sql
-- CDC deduplication from Kafka source
INSERT OVERWRITE TABLE dwd.user_behavior_dedup PARTITION (dt={dt})
WITH raw AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY user_id, behavior_type, item_id
               ORDER BY event_time DESC
           ) AS rn
    FROM ods.user_behavior_log
    WHERE dt = {dt}
),
deduped AS (
    SELECT
        user_id, behavior_type, item_id, item_category,
        event_time, source_channel, device_type,
        properties, {dt} AS dt
    FROM raw
    WHERE rn = 1
)
SELECT * FROM deduped;