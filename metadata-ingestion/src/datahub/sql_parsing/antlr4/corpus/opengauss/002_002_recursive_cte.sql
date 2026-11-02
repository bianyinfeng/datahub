-- 002_recursive_cte.sql
-- Recursive category tree traversal
WITH RECURSIVE category_tree AS (
    -- Anchor: root categories
    SELECT
        category_id,
        category_name,
        category_name_en,
        parent_id,
        0                           AS depth,
        ARRAY[category_id]          AS path_ids,
        category_name::TEXT         AS path_names
    FROM dim.categories
    WHERE parent_id IS NULL

    UNION ALL

    -- Recursive: children
    SELECT
        c.category_id,
        c.category_name,
        c.category_name_en,
        c.parent_id,
        ct.depth + 1,
        ct.path_ids || c.category_id,
        ct.path_names || ' > ' || c.category_name
    FROM dim.categories c
    JOIN category_tree ct ON c.parent_id = ct.category_id
    WHERE ct.depth < {max_depth}
)
INSERT INTO dwd.category_hierarchy
SELECT
    category_id,
    category_name,
    category_name_en,
    parent_id,
    depth,
    path_ids,
    path_names,
    CURRENT_DATE AS loaded_at
FROM category_tree
ON CONFLICT (category_id) DO UPDATE
    SET path_ids = EXCLUDED.path_ids,
        path_names = EXCLUDED.path_names,
        depth = EXCLUDED.depth,
        loaded_at = EXCLUDED.loaded_at;