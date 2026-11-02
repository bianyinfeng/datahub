-- 016_nested_cte_window.sql
WITH
user_orders AS (
    SELECT user_id, order_id, order_amount, pay_time,
           TO_DATE(pay_time) AS order_date
    FROM dwd.orders
    WHERE pay_status = 'PAID' AND dt = {dt}
),
user_stats AS (
    SELECT
        user_id,
        SUM(order_amount)                  AS total_amount,
        COUNT(order_id)                    AS order_count,
        MIN(pay_time)                      AS first_order_time,
        MAX(pay_time)                      AS last_order_time,
        DATEDIFF({dt}, MAX(order_date))    AS recency_days
    FROM user_orders
    GROUP BY user_id
),
rfm_scores AS (
    SELECT
        user_id,
        total_amount,
        order_count,
        recency_days,
        NTILE(5) OVER (ORDER BY total_amount DESC)   AS monetary_score,
        NTILE(5) OVER (ORDER BY order_count DESC)    AS frequency_score,
        NTILE(5) OVER (ORDER BY recency_days ASC)    AS recency_score
    FROM user_stats
)
INSERT INTO ads.rfm_segments PARTITION (dt={dt})
SELECT
    user_id,
    monetary_score,
    frequency_score,
    recency_score,
    monetary_score + frequency_score + recency_score AS rfm_total,
    CASE
        WHEN monetary_score + frequency_score + recency_score >= 12 THEN 'VIP'
        WHEN monetary_score + frequency_score + recency_score >= 8  THEN 'ACTIVE'
        WHEN monetary_score + frequency_score + recency_score >= 5  THEN 'AT_RISK'
        ELSE 'DORMANT'
    END AS customer_segment,
    {dt} AS dt
FROM rfm_scores;