-- 033_unnest_ordinality.sql
-- Expand ordered recommendation list
INSERT INTO dwd.rec_impressions (user_id, position, product_id, score, impression_time)
SELECT
    r.user_id,
    pos.ordinality,
    pos.product_id,
    pos.score,
    r.served_at
FROM dwd.recommendation_batches r
CROSS JOIN LATERAL UNNEST(
    r.product_ids, r.scores
) WITH ORDINALITY AS pos(product_id, score, ordinality)
WHERE r.served_date = {dt}
  AND r.user_id IS NOT NULL;