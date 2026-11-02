-- 046_cte_chain_cohort.sql
WITH
cohort_base AS (
    SELECT user_id, DATE_FORMAT(register_time,'yyyy-MM') AS cohort_month
    FROM dim.users WHERE DATE_FORMAT(register_time,'yyyy-MM') = {cohort_month}
),
m0 AS (
    SELECT cb.cohort_month, COUNT(DISTINCT o.user_id) AS active_users
    FROM cohort_base cb
    JOIN dwd.orders o ON cb.user_id=o.user_id
    AND DATE_FORMAT(o.created_at,'yyyy-MM')=cb.cohort_month
    GROUP BY cb.cohort_month
),
m1 AS (
    SELECT cb.cohort_month, COUNT(DISTINCT o.user_id) AS retained_m1
    FROM cohort_base cb
    JOIN dwd.orders o ON cb.user_id=o.user_id
    AND ADD_MONTHS(DATE_FORMAT(o.created_at,'yyyy-MM'),0)
        = DATE_ADD(cb.cohort_month,1)
    GROUP BY cb.cohort_month
),
m3 AS (
    SELECT cb.cohort_month, COUNT(DISTINCT o.user_id) AS retained_m3
    FROM cohort_base cb
    JOIN dwd.orders o ON cb.user_id=o.user_id
    AND MONTHS_BETWEEN(DATE_FORMAT(o.created_at,'yyyy-MM'), cb.cohort_month)=3
    GROUP BY cb.cohort_month
)
INSERT INTO ads.cohort_retention PARTITION(cohort_month={cohort_month})
SELECT m0.cohort_month,
       m0.active_users,
       m1.retained_m1,
       m3.retained_m3,
       ROUND(m1.retained_m1/m0.active_users,4) AS m1_rate,
       ROUND(m3.retained_m3/m0.active_users,4) AS m3_rate
FROM m0
LEFT JOIN m1 USING(cohort_month)
LEFT JOIN m3 USING(cohort_month);