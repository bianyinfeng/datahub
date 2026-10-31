-- 017_recursive_org.sql
WITH RECURSIVE org_tree AS (
    SELECT
        employee_id,
        employee_name,
        employee_name_en,
        manager_id,
        department_id,
        job_title,
        0                           AS level,
        ARRAY[employee_id]          AS path,
        employee_name::TEXT         AS path_names
    FROM dim.employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT
        e.employee_id,
        e.employee_name,
        e.employee_name_en,
        e.manager_id,
        e.department_id,
        e.job_title,
        ot.level + 1,
        ot.path || e.employee_id,
        ot.path_names || ' > ' || e.employee_name
    FROM dim.employees e
    JOIN org_tree ot ON e.manager_id = ot.employee_id
    WHERE ot.level < {max_org_depth}
)
INSERT INTO ads.org_hierarchy (employee_id, level, path, path_names, manager_id, loaded_at)
SELECT employee_id, level, path, path_names, manager_id, CURRENT_TIMESTAMP
FROM org_tree
ON CONFLICT (employee_id) DO UPDATE
    SET level = EXCLUDED.level,
        path = EXCLUDED.path,
        path_names = EXCLUDED.path_names;