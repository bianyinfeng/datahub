-- 004_window_returning.sql
-- Score and rank users, then capture updated rows
WITH scored_users AS (
    SELECT
        user_id,
        username,
        total_orders,
        total_spent,
        recency_days,
        NTILE(10) OVER (ORDER BY total_spent DESC)   AS decile,
        PERCENT_RANK() OVER (ORDER BY total_spent DESC) AS pct_rank,
        CUME_DIST()    OVER (ORDER BY total_spent DESC) AS cume_dist,
        LAG(total_spent,  1, 0) OVER (PARTITION BY user_id ORDER BY stat_date) AS prev_spent,
        FIRST_VALUE(total_spent) OVER (
            PARTITION BY user_id ORDER BY stat_date
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS first_period_spent
    FROM dws.user_lifetime_stats
    WHERE stat_date = {stat_date}
)
UPDATE dwd.user_profile u
SET
    ltv_decile    = s.decile,
    ltv_pct_rank  = s.pct_rank,
    ltv_score     = ROUND(s.total_spent::NUMERIC, 2),
    updated_at    = CURRENT_TIMESTAMP
FROM scored_users s
WHERE u.user_id = s.user_id
RETURNING u.user_id, u.ltv_decile, u.ltv_score, u.updated_at;