-- 040_analyze_table.sql
ANALYZE TABLE dwd.orders COMPUTE STATISTICS FOR COLUMNS user_id, created_at, order_amount;
ANALYZE TABLE dwd.user_profile COMPUTE STATISTICS;
SHOW PARTITIONS dwd.orders;