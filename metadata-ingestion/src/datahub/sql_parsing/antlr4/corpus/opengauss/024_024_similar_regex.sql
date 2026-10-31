-- 024_similar_regex.sql
-- Validate and clean phone numbers
INSERT INTO dwd.user_contact_clean
SELECT
    user_id,
    phone,
    CASE
        WHEN phone SIMILAR TO '1[3-9][0-9]{9}' THEN 'CN_MOBILE'
        WHEN phone SIMILAR TO '0[0-9]{2,3}-[0-9]{7,8}' THEN 'CN_LANDLINE'
        WHEN phone SIMILAR TO '[0-9]{3}-[0-9]{3}-[0-9]{4}' THEN 'US'
        ELSE 'OTHER'
    END AS phone_type,
    email,
    CASE
        WHEN email ~ '^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$' THEN TRUE
        ELSE FALSE
    END AS email_valid
FROM dwd.user_profile
WHERE is_active = TRUE
  AND phone IS NOT NULL
  AND phone <> '';