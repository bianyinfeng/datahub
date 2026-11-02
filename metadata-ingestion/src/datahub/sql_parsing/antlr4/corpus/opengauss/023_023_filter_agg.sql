-- 023_filter_agg.sql
INSERT INTO ads.channel_conversion_stats (dt, channel, total_views, paid_views, paid_rate)
SELECT
    dt,
    channel,
    COUNT(*)                             AS total_views,
    COUNT(*) FILTER (WHERE pay_status = 'PAID') AS paid_views,
    ROUND(
        COUNT(*) FILTER (WHERE pay_status = 'PAID')::NUMERIC
        / NULLIF(COUNT(*), 0), 4
    )                                    AS paid_rate
FROM dwd.user_events
WHERE dt = {dt}
GROUP BY dt, channel;