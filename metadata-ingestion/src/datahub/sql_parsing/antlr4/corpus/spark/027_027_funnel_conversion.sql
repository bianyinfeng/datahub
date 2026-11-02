-- 027_funnel_conversion.sql
WITH funnel AS (
    SELECT
        user_id,
        step,
        event_time,
        LAG(step, 1) OVER (PARTITION BY user_id ORDER BY event_time) AS prev_step,
        LAG(event_time, 1) OVER (PARTITION BY user_id ORDER BY event_time) AS prev_time
    FROM dwd.event_funnel_all
    WHERE dt = {dt}
),
transitions AS (
    SELECT
        prev_step AS from_step,
        step      AS to_step,
        COUNT(DISTINCT user_id)  AS user_cnt,
        AVG(UNIX_TIMESTAMP(event_time) - UNIX_TIMESTAMP(prev_time)) AS avg_sec
    FROM funnel
    WHERE prev_step IS NOT NULL
    GROUP BY prev_step, step
)
INSERT INTO ads.funnel_transition_stats PARTITION (dt={dt})
SELECT from_step, to_step, user_cnt, avg_sec, {dt} AS dt FROM transitions;