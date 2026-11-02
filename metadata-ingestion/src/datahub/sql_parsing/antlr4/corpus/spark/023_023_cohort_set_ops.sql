-- 023_cohort_set_ops.sql
INSERT INTO ads.new_user_cohort PARTITION (month={cohort_month})
-- Users who registered this month AND made at least one purchase
SELECT user_id FROM dim.users
WHERE DATE_FORMAT(register_time, 'yyyy-MM') = {cohort_month}
INTERSECT
SELECT DISTINCT user_id FROM dwd.orders
WHERE DATE_FORMAT(created_at, 'yyyy-MM') = {cohort_month}
  AND pay_status = 'PAID'
EXCEPT
SELECT user_id FROM dim.users
WHERE is_fraud = 1;