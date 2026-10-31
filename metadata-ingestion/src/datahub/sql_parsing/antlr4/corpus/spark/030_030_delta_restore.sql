-- 030_delta_restore.sql
RESTORE TABLE dwd.orders TO VERSION AS OF {restore_version};

INSERT INTO audit.restore_log
VALUES ({restore_version}, current_timestamp(), {operator_id}, 'dwd.orders');