-- 038_sample_scan.sql
INSERT INTO staging.sample_audit_orders
SELECT
    order_id, user_id, order_amount, pay_status, created_at
FROM dwd.orders TABLESAMPLE(1 PERCENT)
WHERE dt = {dt}
  AND order_status = 'PAID'
LIMIT {sample_limit};