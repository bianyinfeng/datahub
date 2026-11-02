-- 028_maintenance.sql
-- Regular maintenance script
VACUUM ANALYZE dwd.orders;
VACUUM ANALYZE dwd.user_profile;
VACUUM ANALYZE dwd.order_items;

REINDEX INDEX CONCURRENTLY idx_orders_user_id;
REINDEX INDEX CONCURRENTLY idx_orders_status;

-- Update statistics for query planner
ANALYZE dwd.orders (user_id, created_at, order_amount, order_status);
ANALYZE dwd.user_profile;

-- Show bloat info
SELECT schemaname, tablename, n_live_tup, n_dead_tup,
       ROUND(100.0 * n_dead_tup / NULLIF(n_live_tup + n_dead_tup, 0), 2) AS dead_pct
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY dead_pct DESC
LIMIT 20;