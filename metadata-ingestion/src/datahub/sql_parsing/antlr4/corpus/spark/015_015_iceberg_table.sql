-- 015_iceberg_table.sql
CREATE TABLE IF NOT EXISTS dwd.iceberg_transactions
USING iceberg
PARTITIONED BY (dt)
TBLPROPERTIES (
    'write.format.default' = 'parquet',
    'write.metadata.compression-codec' = 'gzip',
    'history.expire.max-snapshot-age-ms' = '604800000'
)
AS
SELECT
    txn_id,
    user_id,
    merchant_id,
    amount,
    currency,
    txn_status,
    txn_type,
    {channel_macro} AS channel,
    risk_score,
    created_at,
    TO_DATE(created_at) AS dt
FROM ods.raw_transactions
WHERE TO_DATE(created_at) BETWEEN {start_date} AND {end_date};