-- 030_notify.sql
-- Event-driven pipeline trigger using NOTIFY
CREATE OR REPLACE FUNCTION dwd.notify_pipeline_trigger()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    PERFORM pg_notify(
        'pipeline_trigger',
        json_build_object(
            'table',  TG_TABLE_NAME,
            'action', TG_OP,
            'id',     NEW.batch_id,
            'ts',     CURRENT_TIMESTAMP
        )::TEXT
    );
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_notify_pipeline
    AFTER INSERT ON staging.batch_metadata
    FOR EACH ROW
    EXECUTE FUNCTION dwd.notify_pipeline_trigger();

LISTEN pipeline_trigger;