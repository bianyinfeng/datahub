-- 038_natural_join.sql
INSERT INTO ads.product_full_details (product_id, product_name, category_name, brand_name, supplier_name)
SELECT
    p.product_id,
    p.product_name,
    c.category_name,
    b.brand_name,
    s.supplier_name
FROM dim.products p
NATURAL JOIN dim.product_categories pc
JOIN dim.categories c ON pc.category_id = c.category_id
JOIN dim.brands     b ON p.brand_id     = b.brand_id
LEFT JOIN dim.suppliers s ON p.supplier_id = s.supplier_id
WHERE p.is_active = TRUE;