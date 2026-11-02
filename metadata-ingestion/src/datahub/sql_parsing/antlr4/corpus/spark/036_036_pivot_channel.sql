-- 036_pivot_channel.sql
INSERT INTO ads.channel_daily_pivot PARTITION (dt={dt})
SELECT
    dt,
    SUM(CASE WHEN channel='APP'     THEN order_cnt ELSE 0 END) AS app_orders,
    SUM(CASE WHEN channel='WEB'     THEN order_cnt ELSE 0 END) AS web_orders,
    SUM(CASE WHEN channel='MINI'    THEN order_cnt ELSE 0 END) AS mini_orders,
    SUM(CASE WHEN channel='OFFLINE' THEN order_cnt ELSE 0 END) AS offline_orders,
    SUM(CASE WHEN channel='APP'     THEN gmv       ELSE 0 END) AS app_gmv,
    SUM(CASE WHEN channel='WEB'     THEN gmv       ELSE 0 END) AS web_gmv,
    SUM(CASE WHEN channel='MINI'    THEN gmv       ELSE 0 END) AS mini_gmv,
    SUM(CASE WHEN channel='OFFLINE' THEN gmv       ELSE 0 END) AS offline_gmv
FROM dws.daily_channel_stats
WHERE dt = {dt}
GROUP BY dt;