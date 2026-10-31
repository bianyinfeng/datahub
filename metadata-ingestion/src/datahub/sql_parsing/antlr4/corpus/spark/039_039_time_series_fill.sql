-- 039_time_series_fill.sql
WITH date_spine AS (
    SELECT EXPLODE(SEQUENCE(TO_DATE({start_date}), TO_DATE({end_date}), INTERVAL 1 DAY)) AS dt
),
daily_metrics AS (
    SELECT
        user_id,
        TO_DATE(event_time) AS dt,
        COUNT(*) AS event_cnt
    FROM dwd.user_events
    WHERE TO_DATE(event_time) BETWEEN {start_date} AND {end_date}
      AND user_id IN ({user_ids})
    GROUP BY user_id, TO_DATE(event_time)
),
user_dates AS (
    SELECT DISTINCT user_id FROM daily_metrics
),
spine AS (
    SELECT u.user_id, d.dt FROM user_dates u CROSS JOIN date_spine d
)
INSERT INTO ads.daily_event_fill PARTITION (start_date={start_date})
SELECT
    s.user_id,
    s.dt,
    COALESCE(m.event_cnt, 0) AS event_cnt
FROM spine s
LEFT JOIN daily_metrics m ON s.user_id = m.user_id AND s.dt = m.dt;