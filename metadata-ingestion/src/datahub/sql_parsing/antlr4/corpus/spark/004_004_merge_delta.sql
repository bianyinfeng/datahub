-- 004_merge_delta.sql
-- Upsert user profile from staging into DWD
MERGE INTO dwd.user_profile AS target
USING (
    SELECT
        user_id,
        username,
        email,
        phone,
        register_channel,
        {city_macro} AS city,
        age_group,
        gender,
        vip_level,
        updated_at
    FROM staging.user_profile_updates
    WHERE batch_date = {batch_date}
) AS source
ON target.user_id = source.user_id
WHEN MATCHED AND source.updated_at > target.updated_at THEN
    UPDATE SET
        username         = source.username,
        email            = source.email,
        phone            = source.phone,
        city             = source.city,
        age_group        = source.age_group,
        vip_level        = source.vip_level,
        updated_at       = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (user_id, username, email, phone, register_channel, city, age_group, gender, vip_level, updated_at)
    VALUES (source.user_id, source.username, source.email, source.phone,
            source.register_channel, source.city, source.age_group, source.gender,
            source.vip_level, source.updated_at);