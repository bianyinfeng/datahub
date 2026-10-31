-- 007_plpgsql_function.sql
CREATE OR REPLACE FUNCTION dwd.calculate_rfm_segment(
    p_recency_days    INTEGER,
    p_frequency       INTEGER,
    p_monetary        NUMERIC
)
RETURNS VARCHAR
LANGUAGE plpgsql
STABLE PARALLEL SAFE
AS $$
DECLARE
    v_r_score INTEGER;
    v_f_score INTEGER;
    v_m_score INTEGER;
    v_rfm     INTEGER;
BEGIN
    -- Recency score (lower days = higher score)
    v_r_score := CASE
        WHEN p_recency_days <= 7   THEN 5
        WHEN p_recency_days <= 30  THEN 4
        WHEN p_recency_days <= 90  THEN 3
        WHEN p_recency_days <= 180 THEN 2
        ELSE 1
    END;

    -- Frequency score
    v_f_score := CASE
        WHEN p_frequency >= 20 THEN 5
        WHEN p_frequency >= 10 THEN 4
        WHEN p_frequency >= 5  THEN 3
        WHEN p_frequency >= 2  THEN 2
        ELSE 1
    END;

    -- Monetary score
    v_m_score := CASE
        WHEN p_monetary >= 10000 THEN 5
        WHEN p_monetary >= 5000  THEN 4
        WHEN p_monetary >= 1000  THEN 3
        WHEN p_monetary >= 200   THEN 2
        ELSE 1
    END;

    v_rfm := v_r_score * 100 + v_f_score * 10 + v_m_score;

    RETURN CASE
        WHEN v_rfm >= 444 THEN 'CHAMPION'
        WHEN v_rfm >= 334 THEN 'LOYAL'
        WHEN v_rfm >= 224 THEN 'POTENTIAL_LOYAL'
        WHEN v_rfm >= 422 THEN 'RECENT_CUSTOMER'
        WHEN v_rfm >= 322 THEN 'PROMISING'
        WHEN v_rfm >= 212 THEN 'AT_RISK'
        WHEN v_rfm >= 111 THEN 'CANT_LOSE'
        ELSE 'HIBERNATING'
    END;
END;
$$;

INSERT INTO dwd.user_rfm_segments (user_id, rfm_segment, calculated_at)
SELECT
    user_id,
    dwd.calculate_rfm_segment(recency_days, frequency, monetary) AS rfm_segment,
    CURRENT_TIMESTAMP
FROM dws.user_lifetime_stats
WHERE stat_date = {stat_date}
ON CONFLICT (user_id) DO UPDATE
    SET rfm_segment = EXCLUDED.rfm_segment,
        calculated_at = EXCLUDED.calculated_at;