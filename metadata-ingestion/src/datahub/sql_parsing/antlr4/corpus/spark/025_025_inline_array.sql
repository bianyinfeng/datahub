-- 025_inline_array.sql
INSERT INTO dwd.recommendation_flat PARTITION (dt={dt})
SELECT
    user_id,
    rec_pos,
    rec.item_id,
    rec.score,
    rec.reason,
    {dt} AS dt
FROM (
    SELECT
        user_id,
        COLLECT_LIST(STRUCT(item_id, score, reason)) AS recs
    FROM staging.recommendation_raw
    WHERE dt = {dt}
    GROUP BY user_id
) t
LATERAL VIEW INLINE(recs) recs_table AS rec_pos, rec
LIMIT {max_recs};