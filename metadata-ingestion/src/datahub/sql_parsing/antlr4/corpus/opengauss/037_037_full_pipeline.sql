-- 037_full_pipeline.sql
WITH
-- L1: raw
l1_orders AS (SELECT * FROM ods.raw_orders WHERE dt={dt}),
l1_items  AS (SELECT * FROM ods.raw_order_items WHERE dt={dt}),

-- L2: clean
l2_clean AS (
    SELECT o.*, u.city, u.age_group, u.vip_level
    FROM l1_orders o
    JOIN dim.users u ON o.user_id = u.user_id
    WHERE o.order_status NOT IN ('CANCELLED')
),

-- L3: enrich items
l3_items AS (
    SELECT i.*, p.category_id, p.brand_id, p.price AS list_price
    FROM l1_items i
    JOIN dim.products p ON i.product_id = p.product_id
),

-- L4: order totals
l4_totals AS (
    SELECT order_id, SUM(quantity*unit_price) AS order_total,
           ARRAY_AGG(product_id) AS products
    FROM l3_items GROUP BY order_id
),

-- L5: join
l5_full AS (
    SELECT c.*, t.order_total, t.products
    FROM l2_clean c JOIN l4_totals t ON c.order_id = t.order_id
),

-- L6: rank
l6_ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY order_total DESC) AS user_rank
    FROM l5_full
),

-- L7: filter and categorize
l7_final AS (
    SELECT *,
           CASE WHEN order_total > {high_value} THEN 'HIGH'
                WHEN order_total > {mid_value}  THEN 'MID'
                ELSE 'LOW' END AS value_tier
    FROM l6_ranked
    WHERE user_rank <= {max_rank}
)
INSERT INTO ads.enriched_orders PARTITION ({dt})
SELECT order_id, user_id, order_total, value_tier, vip_level, city, products, {dt}
FROM l7_final;