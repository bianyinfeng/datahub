-- 014_do_block.sql
DO $$
DECLARE
    v_date      DATE := {target_date}::DATE;
    v_cnt       INTEGER;
    v_threshold NUMERIC := {amount_threshold}::NUMERIC;
BEGIN
    -- Refresh staging table
    TRUNCATE TABLE staging.daily_summary;

    INSERT INTO staging.daily_summary (user_id, order_cnt, total_amt, stat_date)
    SELECT user_id, COUNT(*), SUM(net_amount), v_date
    FROM dwd.orders
    WHERE dt = v_date AND order_status = 'PAID'
    GROUP BY user_id
    HAVING SUM(net_amount) > v_threshold;

    GET DIAGNOSTICS v_cnt = ROW_COUNT;
    RAISE NOTICE 'Inserted % rows for date %', v_cnt, v_date;

    -- Update materialized view
    REFRESH MATERIALIZED VIEW CONCURRENTLY ads.mv_daily_gmv;

    RAISE NOTICE 'Done refreshing materialized view';
END;
$$;