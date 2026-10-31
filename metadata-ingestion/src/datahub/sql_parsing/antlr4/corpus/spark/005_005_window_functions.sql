-- 005_window_functions.sql
INSERT OVERWRITE TABLE dws.user_purchase_analytics PARTITION (dt={dt})
WITH purchases AS (
    SELECT
        user_id,
        order_id,
        order_amount,
        pay_time,
        product_id,
        category_id
    FROM dwd.order_items
    WHERE dt = {dt}
      AND pay_status = 'PAID'
)
SELECT
    user_id,
    order_id,
    order_amount,
    pay_time,
    product_id,
    category_id,
    RANK()       OVER w_user                                    AS user_order_rank,
    DENSE_RANK() OVER w_user                                    AS user_dense_rank,
    ROW_NUMBER() OVER w_user                                    AS user_order_seq,
    LAG(order_amount, 1, 0) OVER w_user                        AS prev_order_amt,
    LEAD(order_amount, 1, 0) OVER w_user                       AS next_order_amt,
    NTILE(4) OVER (PARTITION BY category_id ORDER BY order_amount DESC) AS quartile,
    SUM(order_amount) OVER (PARTITION BY user_id)               AS user_total_amt,
    AVG(order_amount) OVER (PARTITION BY category_id
                            ORDER BY pay_time
                            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS rolling_avg_7d
FROM purchases
WINDOW w_user AS (PARTITION BY user_id ORDER BY pay_time);