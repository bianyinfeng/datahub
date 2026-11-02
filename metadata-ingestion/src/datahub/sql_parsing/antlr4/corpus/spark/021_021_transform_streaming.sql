-- 021_transform_streaming.sql
INSERT INTO dwd.geo_decoded_events PARTITION (dt={dt})
SELECT
    TRANSFORM(user_id, ip_address, event_time)
    USING '{geo_decoder_script}'
    AS (user_id STRING, country STRING, province STRING, city STRING, event_time TIMESTAMP)
FROM ods.user_events
WHERE dt = {dt}
  AND ip_address IS NOT NULL;