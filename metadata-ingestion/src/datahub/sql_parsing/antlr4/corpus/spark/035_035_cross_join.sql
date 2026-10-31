-- 035_cross_join.sql
INSERT INTO ads.promotion_matrix PARTITION (dt={dt})
SELECT
    p.product_id,
    p.product_name,
    promo.promo_id,
    promo.promo_type,
    promo.discount_rate,
    p.price * (1 - promo.discount_rate) AS promo_price
FROM dwd.products p
CROSS JOIN dim.promotions promo
WHERE p.category_id IN ({eligible_categories})
  AND promo.is_active = 1
  AND promo.valid_start <= {dt}
  AND promo.valid_end >= {dt};