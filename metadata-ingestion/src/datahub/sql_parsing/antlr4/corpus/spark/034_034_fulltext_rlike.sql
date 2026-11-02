-- 034_fulltext_rlike.sql
INSERT INTO ads.product_search_index PARTITION (dt={dt})
SELECT
    product_id,
    product_name,
    description,
    LOWER(CONCAT_WS(' ', product_name, description, brand_name)) AS search_text,
    category_path,
    price,
    rating
FROM dwd.products p
JOIN dim.categories c ON p.category_id = c.category_id
JOIN dim.brands     b ON p.brand_id    = b.brand_id
WHERE dt = {dt}
  AND (
      p.product_name RLIKE {search_pattern}
      OR p.description RLIKE {search_pattern}
  );