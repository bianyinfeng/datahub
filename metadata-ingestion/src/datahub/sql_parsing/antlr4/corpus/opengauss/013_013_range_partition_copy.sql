-- 013_range_partition_copy.sql
-- Hash-partitioned user table
CREATE TABLE IF NOT EXISTS dwd.user_profile (
    user_id         BIGINT          NOT NULL,
    username        VARCHAR(64)     NOT NULL,
    email           VARCHAR(128)    UNIQUE,
    phone           VARCHAR(20),
    age_group       VARCHAR(16),
    gender          CHAR(1),
    city            VARCHAR(64),
    region_id       INTEGER,
    vip_level       VARCHAR(16)     NOT NULL DEFAULT 'NORMAL',
    total_orders    INTEGER         NOT NULL DEFAULT 0,
    total_spent     NUMERIC(18,2)   NOT NULL DEFAULT 0.00,
    is_active       BOOLEAN         NOT NULL DEFAULT TRUE,
    is_deleted      BOOLEAN         NOT NULL DEFAULT FALSE,
    register_time   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_user_profile PRIMARY KEY (user_id)
)
PARTITION BY HASH (user_id) (
    PARTITION p0 VALUES WITH (modulus 8, remainder 0),
    PARTITION p1 VALUES WITH (modulus 8, remainder 1),
    PARTITION p2 VALUES WITH (modulus 8, remainder 2),
    PARTITION p3 VALUES WITH (modulus 8, remainder 3),
    PARTITION p4 VALUES WITH (modulus 8, remainder 4),
    PARTITION p5 VALUES WITH (modulus 8, remainder 5),
    PARTITION p6 VALUES WITH (modulus 8, remainder 6),
    PARTITION p7 VALUES WITH (modulus 8, remainder 7)
);

COPY dwd.user_profile FROM STDIN WITH (FORMAT BINARY);