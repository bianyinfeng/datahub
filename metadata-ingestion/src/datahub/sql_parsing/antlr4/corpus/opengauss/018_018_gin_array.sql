-- 018_gin_array.sql
-- Efficient array containment queries
CREATE TABLE IF NOT EXISTS ads.user_interest_tags (
    user_id     BIGINT      PRIMARY KEY,
    tags        TEXT[]      NOT NULL DEFAULT '{}',
    tag_scores  JSONB       NOT NULL DEFAULT '{}',
    updated_at  TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_user_tags_gin ON ads.user_interest_tags USING GIN (tags);

INSERT INTO ads.user_interest_tags (user_id, tags, tag_scores)
SELECT
    user_id,
    ARRAY_AGG(DISTINCT tag ORDER BY tag) AS tags,
    JSONB_OBJECT_AGG(tag, score)         AS tag_scores
FROM (
    SELECT user_id, tag, SUM(weight)::NUMERIC(8,4) AS score
    FROM dwd.user_behavior_tags
    WHERE dt >= {start_date}
      AND dt <= {end_date}
    GROUP BY user_id, tag
    HAVING SUM(weight) > {min_score}
) t
GROUP BY user_id
ON CONFLICT (user_id) DO UPDATE
    SET tags = EXCLUDED.tags,
        tag_scores = EXCLUDED.tag_scores,
        updated_at = CURRENT_TIMESTAMP;

-- Efficient query: find users interested in both 'electronics' and 'gaming'
SELECT u.user_id, u.username
FROM dwd.user_profile u
JOIN ads.user_interest_tags t ON u.user_id = t.user_id
WHERE t.tags @> ARRAY['electronics', 'gaming']
  AND (t.tag_scores->>'electronics')::NUMERIC > {min_score};