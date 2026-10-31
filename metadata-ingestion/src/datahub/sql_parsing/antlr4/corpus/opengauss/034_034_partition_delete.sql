-- 034_partition_delete.sql
-- Expire old partitioned data
DELETE FROM dwd.orders
WHERE dt < {retention_cutoff}
  AND order_status IN ('CANCELLED', 'INVALID', 'EXPIRED')
RETURNING order_id, user_id, order_amount, dt;

-- Archive before delete
INSERT INTO archive.orders_expired
SELECT *, CURRENT_TIMESTAMP AS archived_at
FROM dwd.orders
WHERE dt < {retention_cutoff}
  AND order_status IN ('CANCELLED', 'INVALID', 'EXPIRED');