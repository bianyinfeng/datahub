-- 044_flatten_struct.sql
INSERT INTO dwd.event_properties_flat PARTITION (dt={dt})
SELECT
    event_id,
    user_id,
    event_type,
    props.app_version,
    props.os_name,
    props.os_version,
    props.device_model,
    props.screen_width,
    props.screen_height,
    props.network_type,
    props.timezone,
    event_time,
    {dt} AS dt
FROM (
    SELECT
        event_id, user_id, event_type, event_time,
        FROM_JSON(properties,
            'struct<app_version:string,os_name:string,os_version:string,' ||
            'device_model:string,screen_width:int,screen_height:int,' ||
            'network_type:string,timezone:string>'
        ) AS props
    FROM ods.user_events
    WHERE dt = {dt}
) t;