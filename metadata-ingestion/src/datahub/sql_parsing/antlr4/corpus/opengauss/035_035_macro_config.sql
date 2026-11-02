-- 035_macro_config.sql
INSERT INTO {target_schema}.{target_table}
SELECT
    {metric_id}                         AS metric_id,
    {dimension_1}                       AS dim1,
    {dimension_2}                       AS dim2,
    {measure_expression}                AS metric_value,
    {stat_date}::DATE                   AS stat_date,
    {region_code}                       AS region_code
FROM {source_schema}.{source_table}
WHERE dt = {stat_date}::DATE
  AND {filter_condition}
GROUP BY {dimension_1}, {dimension_2};