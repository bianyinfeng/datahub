-- 050_full_pipeline.sql
-- Full ETL pipeline demonstrating all operator types
WITH
-- SCAN: raw sources
raw_orders      AS (SELECT * FROM ods.orders      WHERE dt={dt}),
raw_items       AS (SELECT * FROM ods.order_items WHERE dt={dt}),
raw_users       AS (SELECT * FROM dim.users),
raw_products    AS (SELECT * FROM dim.products),
raw_categories  AS (SELECT * FROM dim.categories),
raw_regions     AS (SELECT * FROM dim.regions),

-- PROJECT + FILTER: clean and enrich
clean_orders AS (
    SELECT
        o.order_id,
        o.user_id,
        o.channel,
        o.order_status,
        o.pay_channel,
        o.created_at,
        u.city,
        u.age_group,
        u.vip_level,
        r.region_name,
        r.country_name
    FROM raw_orders o
    JOIN raw_users  u ON o.user_id    = u.user_id
    JOIN raw_regions r ON u.region_id = r.region_id
    WHERE o.order_status NOT IN ('CANCELLED','INVALID')
),

-- JOIN + PROJECT: item-level enrichment
clean_items AS (
    SELECT
        i.order_id,
        i.product_id,
        p.product_name,
        p.brand_id,
        c.category_id,
        c.category_name,
        c.parent_category_id,
        i.quantity,
        i.unit_price,
        i.quantity * i.unit_price AS line_amount
    FROM raw_items i
    JOIN raw_products   p ON i.product_id  = p.product_id
    JOIN raw_categories c ON p.category_id = c.category_id
),

-- AGGREGATE
order_totals AS (
    SELECT
        order_id,
        SUM(line_amount)  AS order_amount,
        SUM(quantity)     AS total_qty,
        COUNT(product_id) AS sku_cnt
    FROM clean_items
    GROUP BY order_id
),

-- WINDOW
order_ranked AS (
    SELECT
        o.*,
        t.order_amount,
        t.total_qty,
        t.sku_cnt,
        RANK()       OVER (PARTITION BY o.user_id ORDER BY t.order_amount DESC) AS user_rank,
        SUM(t.order_amount) OVER (PARTITION BY o.user_id) AS user_total_spent,
        LAG(t.order_amount) OVER (PARTITION BY o.user_id ORDER BY o.created_at) AS prev_order_amt
    FROM clean_orders o
    JOIN order_totals t ON o.order_id = t.order_id
),

-- SET (UNION)
high_value_orders AS (
    SELECT order_id, user_id, order_amount, 'HIGH_VALUE' AS segment FROM order_ranked
    WHERE order_amount > {high_value_threshold}
    UNION ALL
    SELECT order_id, user_id, order_amount, 'VIP_USER' AS segment FROM order_ranked
    WHERE vip_level = 'GOLD' AND order_amount > {vip_threshold}
)

-- WRITE: final output
INSERT OVERWRITE TABLE ads.priority_orders PARTITION (dt={dt})
SELECT
    order_id,
    user_id,
    order_amount,
    segment,
    user_rank,
    user_total_spent,
    {dt} AS dt
FROM high_value_orders;