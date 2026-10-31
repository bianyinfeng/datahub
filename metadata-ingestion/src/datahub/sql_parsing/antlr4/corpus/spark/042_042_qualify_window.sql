-- 042_qualify_window.sql
-- Get the latest record per user (QUALIFY replaces outer WHERE on window func)
INSERT INTO dwd.user_latest_event PARTITION (dt={dt})
SELECT
    user_id, event_type, event_time, device_type, source_channel, item_id
FROM dwd.user_events
WHERE dt = {dt}
QUALIFY ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_time DESC) = 1;