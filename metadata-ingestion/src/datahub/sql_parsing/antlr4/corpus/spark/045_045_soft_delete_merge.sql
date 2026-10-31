-- 045_soft_delete_merge.sql
MERGE INTO dwd.user_profile AS tgt
USING (
    SELECT user_id, 'DELETE' AS action_type, CURRENT_TIMESTAMP() AS ts
    FROM staging.gdpr_delete_requests
    WHERE batch_date = {batch_date}
) AS src
ON tgt.user_id = src.user_id
WHEN MATCHED THEN
    UPDATE SET
        tgt.is_deleted     = TRUE,
        tgt.deleted_at     = src.ts,
        tgt.delete_reason  = 'GDPR_REQUEST',
        tgt.username       = CONCAT('deleted_', tgt.user_id),
        tgt.email          = CONCAT('deleted_', tgt.user_id, '@anon.com'),
        tgt.phone          = NULL;