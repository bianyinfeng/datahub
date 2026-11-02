-- 002_multi_cte_etl.sql
INSERT OVERWRITE TABLE dws.daily_user_summary PARTITION (dt={report_date})
WITH ods_orders AS (
    SELECT order_id, user_id, order_amount, order_status, created_at,
           TO_DATE(created_at) AS order_date
    FROM ods.orders
    WHERE TO_DATE(created_at) = {report_date}
),
ods_payments AS (
    SELECT payment_id, order_id, pay_amount, pay_channel, pay_time
    FROM ods.payments
    WHERE TO_DATE(pay_time) = {report_date}
),
dwd_order_detail AS (
    SELECT
        o.order_id, o.user_id, o.order_amount,
        p.pay_amount, p.pay_channel, p.pay_time,
        CASE WHEN p.pay_amount IS NULL THEN 'UNPAID'
             WHEN p.pay_amount >= o.order_amount THEN 'PAID'
             ELSE 'PARTIAL' END AS pay_status,
        o.order_date
    FROM ods_orders o
    LEFT JOIN ods_payments p ON o.order_id = p.order_id
),
dws_summary AS (
    SELECT
        user_id,
        COUNT(order_id)                 AS order_cnt,
        SUM(order_amount)               AS total_order_amt,
        SUM(pay_amount)                 AS total_pay_amt,
        COUNT(CASE WHEN pay_status = 'PAID' THEN 1 END) AS paid_cnt,
        MAX(order_date)                 AS last_order_date
    FROM dwd_order_detail
    GROUP BY user_id
)
SELECT * FROM dws_summary;