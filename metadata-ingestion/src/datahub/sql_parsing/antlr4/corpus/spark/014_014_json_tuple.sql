-- 014_json_tuple.sql
INSERT INTO dwd.event_attributes PARTITION (dt={dt})
SELECT
    e.event_id,
    e.user_id,
    e.event_type,
    attrs.page_name,
    attrs.ref_source,
    attrs.ab_version,
    attrs.experiment_id,
    e.created_at,
    {dt} AS dt
FROM ods.user_events e
LATERAL VIEW JSON_TUPLE(e.properties, 'page_name','ref_source','ab_version','experiment_id')
    attrs AS page_name, ref_source, ab_version, experiment_id
WHERE e.dt = {dt};