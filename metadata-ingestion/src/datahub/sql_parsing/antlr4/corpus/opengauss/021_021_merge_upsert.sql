-- 021_merge_upsert.sql
MERGE INTO dwd.user_profile AS t
USING (
    SELECT
        user_id,
        username,
        email,
        phone,
        city,
        age_group,
        vip_level,
        updated_at,
        {batch_date} AS sync_date
    FROM staging.user_profile_delta
    WHERE batch_date = {batch_date}
) AS s
ON t.user_id = s.user_id
WHEN MATCHED AND s.updated_at > t.updated_at AND t.is_deleted = FALSE THEN
    UPDATE SET
        username   = s.username,
        email      = s.email,
        phone      = s.phone,
        city       = s.city,
        age_group  = s.age_group,
        vip_level  = s.vip_level,
        updated_at = s.updated_at
WHEN MATCHED AND t.is_deleted = TRUE THEN
    UPDATE SET is_deleted = FALSE, updated_at = s.updated_at
WHEN NOT MATCHED THEN
    INSERT (user_id, username, email, phone, city, age_group, vip_level, updated_at)
    VALUES (s.user_id, s.username, s.email, s.phone, s.city, s.age_group, s.vip_level, s.updated_at);