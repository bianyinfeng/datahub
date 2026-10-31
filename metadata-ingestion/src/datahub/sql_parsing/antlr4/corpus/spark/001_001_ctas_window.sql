-- 001_ctas_window.sql
-- Layers: ods.user_events → dwd.user_event_enriched
CREATE TABLE dwd.user_event_enriched
USING delta
PARTITIONED BY (dt)
AS
WITH cte_raw AS (
    SELECT
        event_id,
        user_id,
        event_type,
        {event_date_macro} AS event_date,
        platform,
        session_id,
        page_url,
        created_at,
        TO_DATE(created_at) AS dt
    FROM ods.user_events
    WHERE event_type IS NOT NULL
      AND user_id IS NOT NULL
),
cte_session AS (
    SELECT
        user_id,
        session_id,
        COUNT(event_id)                                          AS session_event_cnt,
        MIN(created_at)                                         AS session_start,
        MAX(created_at)                                         AS session_end,
        DATEDIFF(MAX(created_at), MIN(created_at))              AS session_duration_sec
    FROM cte_raw
    GROUP BY user_id, session_id
)
SELECT
    r.event_id,
    r.user_id,
    r.event_type,
    r.event_date,
    r.platform,
    r.session_id,
    s.session_event_cnt,
    s.session_start,
    s.session_end,
    s.session_duration_sec,
    ROW_NUMBER() OVER (PARTITION BY r.user_id ORDER BY r.created_at)     AS user_event_seq,
    SUM(s.session_event_cnt) OVER (PARTITION BY r.user_id
                                   ORDER BY r.created_at
                                   ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_events,
    r.dt
FROM cte_raw r
JOIN cte_session s ON r.user_id = s.user_id AND r.session_id = s.session_id;