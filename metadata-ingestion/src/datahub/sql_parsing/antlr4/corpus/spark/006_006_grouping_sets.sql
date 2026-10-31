-- 006_grouping_sets.sql
INSERT INTO ads.gmv_multidim_report PARTITION (dt={dt})
SELECT
    COALESCE(region,    '__ALL__') AS region,
    COALESCE(channel,   '__ALL__') AS channel,
    COALESCE(category,  '__ALL__') AS category,
    SUM(order_amount)              AS gmv,
    COUNT(DISTINCT order_id)       AS order_cnt,
    COUNT(DISTINCT user_id)        AS buyer_cnt,
    GROUPING(region)               AS is_region_total,
    GROUPING(channel)              AS is_channel_total,
    GROUPING(category)             AS is_category_total,
    {dt}                           AS dt
FROM dwd.order_items oi
JOIN dim.regions r    ON oi.region_id  = r.region_id
JOIN dim.channels ch  ON oi.channel_id = ch.channel_id
JOIN dim.categories c ON oi.category_id= c.category_id
WHERE oi.dt = {dt}
  AND oi.pay_status = 'PAID'
GROUP BY GROUPING SETS (
    (region, channel, category),
    (region, channel),
    (region, category),
    (channel, category),
    (region),
    (channel),
    (category),
    ()
);