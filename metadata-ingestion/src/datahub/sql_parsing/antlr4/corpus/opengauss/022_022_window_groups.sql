-- 022_window_groups.sql
INSERT INTO ads.category_sales_trend (category_id, stat_date, gmv, moving_avg_3d, rank_in_period)
SELECT
    category_id,
    stat_date,
    gmv,
    AVG(gmv) OVER (
        PARTITION BY category_id
        ORDER BY stat_date
        GROUPS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS moving_avg_3d,
    RANK() OVER (
        PARTITION BY stat_date
        ORDER BY gmv DESC
    ) AS rank_in_period
FROM dws.category_daily_stats
WHERE stat_date BETWEEN {start_date} AND {end_date};