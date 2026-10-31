-- 026_generate_series.sql
-- Fill missing dates using generate_series
INSERT INTO ads.daily_metric_complete (user_id, stat_date, login_cnt, order_cnt)
WITH date_spine AS (
    SELECT generate_series(
        {start_date}::DATE,
        {end_date}::DATE,
        '1 day'::INTERVAL
    )::DATE AS stat_date
),
user_list AS (
    SELECT DISTINCT user_id FROM dwd.user_events
    WHERE dt BETWEEN {start_date} AND {end_date}
),
spine AS (
    SELECT u.user_id, d.stat_date FROM user_list u CROSS JOIN date_spine d
),
actuals AS (
    SELECT
        user_id,
        dt AS stat_date,
        COUNT(DISTINCT CASE WHEN event_type='login'  THEN event_id END) AS login_cnt,
        COUNT(DISTINCT CASE WHEN event_type='order'  THEN event_id END) AS order_cnt
    FROM dwd.user_events
    WHERE dt BETWEEN {start_date} AND {end_date}
    GROUP BY user_id, dt
)
SELECT
    s.user_id,
    s.stat_date,
    COALESCE(a.login_cnt, 0) AS login_cnt,
    COALESCE(a.order_cnt, 0) AS order_cnt
FROM spine s
LEFT JOIN actuals a ON s.user_id = a.user_id AND s.stat_date = a.stat_date;