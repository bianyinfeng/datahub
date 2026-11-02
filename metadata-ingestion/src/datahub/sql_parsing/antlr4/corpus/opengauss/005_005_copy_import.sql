-- 005_copy_import.sql
-- Import raw CSV data from external file
COPY staging.orders_raw (
    order_id, user_id, product_id, order_amount,
    pay_channel, order_status, created_at
)
FROM '{data_file_path}'
WITH (
    FORMAT CSV,
    HEADER TRUE,
    DELIMITER ',',
    QUOTE '"',
    ESCAPE '\',
    NULL '\N',
    ENCODING 'UTF8'
);

-- Export processed data to S3-mounted path
COPY (
    SELECT order_id, user_id, order_amount, order_status, created_at
    FROM dwd.orders
    WHERE dt = {export_date}
      AND order_status = 'PAID'
)
TO '{export_path}'
WITH (FORMAT CSV, HEADER TRUE, DELIMITER '	');