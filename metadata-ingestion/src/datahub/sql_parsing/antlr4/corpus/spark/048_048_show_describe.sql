-- 048_show_describe.sql
SHOW CREATE TABLE dwd.orders;
DESCRIBE EXTENDED dwd.orders PARTITION (dt={dt});
SHOW COLUMNS FROM dwd.order_items;
SHOW TABLES IN dws LIKE 'daily_*';