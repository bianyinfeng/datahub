-- 049_streaming_agg.sql
-- Simulated micro-batch aggregation (streaming ETL pattern)
INSERT INTO dws.realtime_gmv_5min PARTITION (window_start)
SELECT
    WINDOW(event_time, '5 minutes').start  AS window_start,
    WINDOW(event_time, '5 minutes').end    AS window_end,
    SUM(order_amount)                       AS gmv,
    COUNT(DISTINCT order_id)               AS order_cnt,
    COUNT(DISTINCT user_id)                AS buyer_cnt,
    {region_macro}                          AS region
FROM streaming.orders_stream
WHERE event_time >= {watermark_ts}
GROUP BY WINDOW(event_time, '5 minutes'), {region_macro};