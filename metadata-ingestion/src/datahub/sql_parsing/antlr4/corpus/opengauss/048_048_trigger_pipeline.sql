-- 048_trigger_pipeline.sql
CREATE OR REPLACE FUNCTION dwd.sync_user_stats()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    -- Update user aggregate stats on each new paid order
    IF NEW.order_status = 'PAID' THEN
        INSERT INTO dws.user_lifetime_stats (user_id, stat_date, total_orders, total_spent)
        VALUES (NEW.user_id, CURRENT_DATE, 1, NEW.net_amount)
        ON CONFLICT (user_id, stat_date) DO UPDATE
            SET total_orders = dws.user_lifetime_stats.total_orders + 1,
                total_spent  = dws.user_lifetime_stats.total_spent + NEW.net_amount;

        -- Notify downstream
        PERFORM pg_notify('user_stats_updated', NEW.user_id::TEXT);
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_sync_user_stats
    AFTER INSERT OR UPDATE OF order_status ON dwd.orders
    FOR EACH ROW WHEN (NEW.order_status = 'PAID')
    EXECUTE FUNCTION dwd.sync_user_stats();