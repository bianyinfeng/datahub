-- 001_partitioned_table.sql
CREATE TABLE IF NOT EXISTS dwd.orders (
    order_id        BIGSERIAL       NOT NULL,
    user_id         BIGINT          NOT NULL,
    product_id      BIGINT          NOT NULL,
    category_id     INTEGER         NOT NULL,
    order_amount    NUMERIC(18,2)   NOT NULL DEFAULT 0.00,
    discount_amount NUMERIC(18,2)   NOT NULL DEFAULT 0.00,
    net_amount      NUMERIC(18,2)   GENERATED ALWAYS AS (order_amount - discount_amount) STORED,
    pay_channel     VARCHAR(32),
    order_status    VARCHAR(16)     NOT NULL DEFAULT 'PENDING',
    logistics_id    BIGINT,
    region_id       INTEGER,
    created_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dt              DATE            NOT NULL,
    CONSTRAINT pk_orders PRIMARY KEY (order_id, dt),
    CONSTRAINT chk_amount CHECK (order_amount >= 0)
)
PARTITION BY RANGE (dt) (
    PARTITION p_2024_01 VALUES LESS THAN ('2024-02-01'),
    PARTITION p_2024_02 VALUES LESS THAN ('2024-03-01'),
    PARTITION p_2024_03 VALUES LESS THAN ('2024-04-01'),
    PARTITION p_2024_q2 VALUES LESS THAN ('2024-07-01'),
    PARTITION p_2024_q3 VALUES LESS THAN ('2024-10-01'),
    PARTITION p_2024_q4 VALUES LESS THAN ('2025-01-01'),
    PARTITION p_future  VALUES LESS THAN (MAXVALUE)
)
WITH (parallel_workers=4, autovacuum_enabled=true);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_user_id
    ON dwd.orders USING BTREE (user_id, created_at DESC);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_status
    ON dwd.orders USING BTREE (order_status, dt)
    WHERE order_status NOT IN ('CANCELLED','INVALID');