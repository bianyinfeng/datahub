-- 047_external_table.sql
CREATE EXTERNAL TABLE IF NOT EXISTS ods.ext_crm_customers (
    customer_id     STRING  COMMENT '客户ID',
    customer_name   STRING  COMMENT '客户名称',
    contact_email   STRING  COMMENT '联系邮箱',
    phone           STRING  COMMENT '联系电话',
    region          STRING  COMMENT '所在区域',
    tier            STRING  COMMENT '客户等级',
    annual_revenue  DECIMAL(18,2) COMMENT '年营业额',
    created_at      TIMESTAMP COMMENT '创建时间'
)
PARTITIONED BY (dt STRING COMMENT '数据日期')
ROW FORMAT SERDE 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
STORED AS INPUTFORMAT 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat'
OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
LOCATION '{s3_base_path}/crm/customers/'
TBLPROPERTIES ('parquet.compression'='SNAPPY');