-- 026_optimize_delta.sql
OPTIMIZE dwd.orders
WHERE dt >= DATE_SUB({dt}, 7)
ZORDER BY user_id, created_at;

INSERT INTO ads.order_summary PARTITION (dt={dt})
SELECT
    user_id,
    COUNT(*)           AS order_cnt,
    SUM(order_amount)  AS total_amt
FROM dwd.orders
WHERE dt = {dt}
GROUP BY user_id;