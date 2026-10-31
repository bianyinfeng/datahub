-- 032_complex_view.sql
CREATE OR REPLACE VIEW ads.v_user_360 AS
WITH user_base AS (
    SELECT user_id, username, email, city, age_group, vip_level, register_time
    FROM dwd.user_profile WHERE is_deleted = FALSE
),
user_orders AS (
    SELECT user_id,
           COUNT(DISTINCT order_id)   AS order_cnt_lifetime,
           SUM(net_amount)            AS gmv_lifetime,
           MAX(created_at)            AS last_order_time,
           MIN(created_at)            AS first_order_time
    FROM dwd.orders WHERE order_status = 'PAID'
    GROUP BY user_id
),
user_tags AS (
    SELECT user_id, tags, tag_scores FROM ads.user_interest_tags
),
user_rfm AS (
    SELECT user_id, rfm_segment FROM dwd.user_rfm_segments
    WHERE stat_date = (SELECT MAX(stat_date) FROM dwd.user_rfm_segments)
)
SELECT
    b.user_id, b.username, b.email, b.city, b.age_group, b.vip_level,
    COALESCE(o.order_cnt_lifetime, 0) AS order_cnt,
    COALESCE(o.gmv_lifetime, 0)       AS gmv,
    o.last_order_time,
    o.first_order_time,
    t.tags,
    r.rfm_segment
FROM user_base b
LEFT JOIN user_orders o ON b.user_id = o.user_id
LEFT JOIN user_tags   t ON b.user_id = t.user_id
LEFT JOIN user_rfm    r ON b.user_id = r.user_id;