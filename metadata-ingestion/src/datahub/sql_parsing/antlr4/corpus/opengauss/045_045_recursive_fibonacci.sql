-- 045_recursive_fibonacci.sql
-- Recursive query for series generation (dimension population)
WITH RECURSIVE date_series AS (
    SELECT {start_date}::DATE AS d
    UNION ALL
    SELECT d + 1 FROM date_series WHERE d < {end_date}::DATE
),
fiscal_calendar AS (
    SELECT
        d AS calendar_date,
        EXTRACT(YEAR  FROM d)::INTEGER AS year,
        EXTRACT(MONTH FROM d)::INTEGER AS month,
        EXTRACT(DOW   FROM d)::INTEGER AS day_of_week,
        EXTRACT(DOY   FROM d)::INTEGER AS day_of_year,
        CASE WHEN EXTRACT(DOW FROM d) IN (0,6) THEN FALSE ELSE TRUE END AS is_workday,
        DATE_TRUNC('week',  d)::DATE AS week_start,
        DATE_TRUNC('month', d)::DATE AS month_start,
        DATE_TRUNC('quarter', d)::DATE AS quarter_start
    FROM date_series
)
INSERT INTO dim.fiscal_calendar (calendar_date, year, month, day_of_week, day_of_year, is_workday, week_start, month_start, quarter_start)
SELECT * FROM fiscal_calendar
ON CONFLICT (calendar_date) DO NOTHING;