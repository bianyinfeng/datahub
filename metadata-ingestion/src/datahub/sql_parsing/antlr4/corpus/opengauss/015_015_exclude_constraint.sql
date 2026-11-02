-- 015_exclude_constraint.sql
-- Booking table with EXCLUDE constraint to prevent overlapping reservations
CREATE TABLE IF NOT EXISTS dwd.resource_bookings (
    booking_id      BIGSERIAL       PRIMARY KEY,
    resource_id     INTEGER         NOT NULL,
    user_id         BIGINT          NOT NULL,
    booking_start   TIMESTAMP       NOT NULL,
    booking_end     TIMESTAMP       NOT NULL,
    status          VARCHAR(16)     NOT NULL DEFAULT 'CONFIRMED',
    created_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_booking_period CHECK (booking_end > booking_start),
    EXCLUDE USING GIST (
        resource_id WITH =,
        TSRANGE(booking_start, booking_end) WITH &&
    ) WHERE (status = 'CONFIRMED')
);

INSERT INTO dwd.resource_bookings (resource_id, user_id, booking_start, booking_end)
SELECT
    resource_id,
    user_id,
    booking_start::TIMESTAMP,
    booking_end::TIMESTAMP
FROM staging.booking_requests
WHERE status = 'PENDING'
  AND booking_end > booking_start
  AND resource_id IS NOT NULL
RETURNING booking_id, resource_id, user_id, booking_start, booking_end;