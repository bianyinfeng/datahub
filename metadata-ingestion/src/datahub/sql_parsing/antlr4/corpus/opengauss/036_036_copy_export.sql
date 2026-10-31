-- 036_copy_export.sql
COPY (
    WITH monthly_summary AS (
        SELECT
            DATE_TRUNC('month', dt)::DATE AS month,
            category_id,
            SUM(gmv)                 AS total_gmv,
            SUM(order_cnt)           AS total_orders,
            COUNT(DISTINCT user_id)  AS unique_buyers
        FROM ads.mv_daily_gmv
        WHERE dt >= {start_date}
          AND dt <= {end_date}
        GROUP BY 1, 2
    )
    SELECT ms.month, c.category_name, ms.total_gmv, ms.total_orders, ms.unique_buyers
    FROM monthly_summary ms
    JOIN dim.categories c ON ms.category_id = c.category_id
    ORDER BY ms.month, ms.total_gmv DESC
)
TO STDOUT WITH (FORMAT CSV, HEADER TRUE, DELIMITER ',');