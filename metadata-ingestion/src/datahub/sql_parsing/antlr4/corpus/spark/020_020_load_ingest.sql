-- 020_load_ingest.sql
MSCK REPAIR TABLE ods.raw_click_logs;

INSERT OVERWRITE TABLE dwd.click_logs_clean PARTITION (dt={dt})
SELECT
    log_id,
    user_id,
    item_id,
    LOWER(source_channel)           AS source_channel,
    TRIM(device_type)               AS device_type,
    CAST(click_time AS TIMESTAMP)   AS click_time,
    CAST(duration_ms AS BIGINT)     AS duration_ms,
    {dt}                            AS dt
FROM ods.raw_click_logs
WHERE dt = {dt}
  AND user_id IS NOT NULL
  AND item_id IS NOT NULL
  AND CAST(duration_ms AS BIGINT) BETWEEN 0 AND 300000;