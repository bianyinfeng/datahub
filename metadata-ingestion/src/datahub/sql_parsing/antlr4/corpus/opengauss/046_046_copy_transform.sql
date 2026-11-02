-- 046_copy_transform.sql
-- Stage raw CSV then transform
CREATE TEMP TABLE tmp_raw_events (
    event_id    TEXT,
    user_id     TEXT,
    event_type  TEXT,
    properties  TEXT,
    event_time  TEXT
);

COPY tmp_raw_events FROM '{event_file_path}'
WITH (FORMAT CSV, HEADER TRUE, NULL '');

INSERT INTO ods.user_events (event_id, user_id, event_type, properties, event_time, dt)
SELECT
    event_id::BIGINT,
    user_id::BIGINT,
    event_type,
    properties::JSONB,
    event_time::TIMESTAMP,
    event_time::DATE AS dt
FROM tmp_raw_events
WHERE event_id ~ '^[0-9]+$'
  AND user_id ~ '^[0-9]+$'
  AND event_time ~ '^[0-9]{4}-[0-9]{2}-[0-9]{2}';

DROP TABLE tmp_raw_events;