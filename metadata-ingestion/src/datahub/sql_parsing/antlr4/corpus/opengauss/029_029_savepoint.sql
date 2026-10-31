-- 029_savepoint.sql
BEGIN;

SAVEPOINT sp_start;

INSERT INTO dwd.audit_log (action, table_name, record_id, performed_by, performed_at)
VALUES ('BATCH_START', 'dwd.orders', {batch_id}, {operator}, CURRENT_TIMESTAMP);

SAVEPOINT sp_insert;

INSERT INTO dwd.orders (user_id, product_id, order_amount, order_status)
SELECT user_id, product_id, order_amount, 'PENDING'
FROM staging.order_queue
WHERE batch_id = {batch_id};

-- If count mismatch, rollback just the insert
-- ROLLBACK TO SAVEPOINT sp_insert;

RELEASE SAVEPOINT sp_insert;

UPDATE dwd.audit_log
SET status = 'COMPLETED', completed_at = CURRENT_TIMESTAMP
WHERE batch_id = {batch_id};

COMMIT;