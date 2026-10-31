-- 024_nested_subquery.sql
INSERT INTO ads.top_products_per_category PARTITION (dt={dt})
SELECT p.*
FROM (
    SELECT
        category_id,
        product_id,
        total_sales,
        RANK() OVER (PARTITION BY category_id ORDER BY total_sales DESC) AS cat_rank
    FROM (
        SELECT
            p.category_id,
            oi.product_id,
            SUM(oi.quantity * oi.unit_price) AS total_sales
        FROM dwd.order_items oi
        JOIN dwd.products p ON oi.product_id = p.product_id
        WHERE oi.dt = {dt}
          AND oi.pay_status = 'PAID'
        GROUP BY p.category_id, oi.product_id
    ) t
) p
WHERE cat_rank <= {top_n};