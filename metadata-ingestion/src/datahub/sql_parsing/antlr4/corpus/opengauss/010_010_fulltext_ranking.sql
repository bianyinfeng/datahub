-- 010_fulltext_ranking.sql
-- Search products with ranked results
INSERT INTO ads.search_results (query_id, product_id, rank_score, loaded_at)
SELECT
    {query_id}                                                      AS query_id,
    product_id,
    TS_RANK_CD(
        search_vector,
        plainto_tsquery('chinese', {search_keyword}),
        32  -- normalization: divide by (1 + log(length))
    )                                                               AS rank_score,
    CURRENT_TIMESTAMP                                               AS loaded_at
FROM dwd.product_catalog
WHERE
    search_vector @@ plainto_tsquery('chinese', {search_keyword})
    AND stock_qty > 0
    AND price BETWEEN {min_price} AND {max_price}
ORDER BY rank_score DESC
LIMIT {result_limit};