-- 041_set_ops.sql
-- Loyal buyers: purchased in both last month and this month
INSERT INTO ads.loyal_buyers (user_id, cohort_label)
SELECT user_id FROM dwd.orders
WHERE DATE_TRUNC('month', created_at) = DATE_TRUNC('month', {this_month}::DATE)
  AND order_status = 'PAID'
INTERSECT
SELECT user_id FROM dwd.orders
WHERE DATE_TRUNC('month', created_at) = DATE_TRUNC('month', {this_month}::DATE) - INTERVAL '1 month'
  AND order_status = 'PAID'
EXCEPT
SELECT user_id FROM dim.users WHERE is_fraud = TRUE;