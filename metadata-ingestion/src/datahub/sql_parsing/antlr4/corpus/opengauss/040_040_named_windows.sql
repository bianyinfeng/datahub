-- 040_named_windows.sql
INSERT INTO ads.user_behavior_analytics
SELECT
    user_id,
    event_type,
    event_time,
    COUNT(*) OVER w_user_day          AS daily_event_cnt,
    SUM(duration_ms) OVER w_user_day  AS daily_duration,
    AVG(duration_ms) OVER w_user      AS avg_duration_per_user,
    FIRST_VALUE(event_type) OVER w_time AS first_event_type,
    NTH_VALUE(event_type, 3) OVER w_time AS third_event_type
FROM dwd.user_events
WHERE dt = {dt}
WINDOW
    w_user     AS (PARTITION BY user_id),
    w_user_day AS (PARTITION BY user_id, dt),
    w_time     AS (PARTITION BY user_id ORDER BY event_time
                   ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING);