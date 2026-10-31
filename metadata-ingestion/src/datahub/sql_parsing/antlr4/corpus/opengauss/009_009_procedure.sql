-- 009_procedure.sql
CREATE OR REPLACE PROCEDURE dwd.refresh_user_stats(
    IN p_stat_date  DATE,
    IN p_batch_size INTEGER DEFAULT 10000
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_rows_processed INTEGER := 0;
    v_total INTEGER;
BEGIN
    -- Mark stale records
    DELETE FROM dws.user_lifetime_stats
    WHERE stat_date = p_stat_date;

    -- Recompute in batches
    INSERT INTO dws.user_lifetime_stats (
        user_id, stat_date, total_orders, total_spent, recency_days, frequency, monetary
    )
    SELECT
        user_id,
        p_stat_date,
        COUNT(DISTINCT order_id)                                     AS total_orders,
        SUM(net_amount)                                              AS total_spent,
        (p_stat_date - MAX(dt))::INTEGER                            AS recency_days,
        COUNT(DISTINCT order_id)                                     AS frequency,
        SUM(net_amount)                                              AS monetary
    FROM dwd.orders
    WHERE order_status = 'PAID'
      AND dt <= p_stat_date
    GROUP BY user_id;

    GET DIAGNOSTICS v_rows_processed = ROW_COUNT;

    RAISE NOTICE 'Refreshed % user stats for %', v_rows_processed, p_stat_date;

    -- Update RFM segments
    CALL dwd.refresh_user_stats({stat_date}, {batch_size});
END;
$$;

CALL dwd.refresh_user_stats({target_date}::DATE, {batch_size}::INTEGER);