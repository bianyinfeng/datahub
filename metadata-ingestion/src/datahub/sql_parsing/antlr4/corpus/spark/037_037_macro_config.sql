-- 037_macro_config.sql
INSERT INTO {target_db}.{target_table} PARTITION (dt={stat_date}, region={target_region})
SELECT
    {metric_id}         AS metric_id,
    {dim_col_1}         AS dim1,
    {dim_col_2}         AS dim2,
    {measure_expr}      AS metric_value,
    {stat_date}         AS stat_date,
    {target_region}     AS region
FROM {source_db}.{source_table}
WHERE dt = {stat_date}
  AND region = {target_region}
  AND {filter_condition}
GROUP BY {dim_col_1}, {dim_col_2};