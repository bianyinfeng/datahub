-- 033_recursive_cte_sim.sql
-- Simulate recursive BOM expansion (Spark doesn't support RECURSIVE CTE natively)
-- Using fixed-depth unrolling
WITH level0 AS (
    SELECT
        component_id AS root_id, component_id, parent_id, 0 AS depth,
        CAST(component_id AS STRING) AS path
    FROM dim.bom_components
    WHERE parent_id IS NULL
),
level1 AS (
    SELECT l0.root_id, c.component_id, c.parent_id, 1, CONCAT(l0.path, '/', c.component_id)
    FROM level0 l0 JOIN dim.bom_components c ON l0.component_id = c.parent_id
),
level2 AS (
    SELECT l1.root_id, c.component_id, c.parent_id, 2, CONCAT(l1.path, '/', c.component_id)
    FROM level1 l1 JOIN dim.bom_components c ON l1.component_id = c.parent_id
),
level3 AS (
    SELECT l2.root_id, c.component_id, c.parent_id, 3, CONCAT(l2.path, '/', c.component_id)
    FROM level2 l2 JOIN dim.bom_components c ON l2.component_id = c.parent_id
),
all_levels AS (
    SELECT * FROM level0
    UNION ALL SELECT * FROM level1
    UNION ALL SELECT * FROM level2
    UNION ALL SELECT * FROM level3
)
INSERT INTO dwd.bom_expanded
SELECT root_id, component_id, parent_id, depth, path FROM all_levels;