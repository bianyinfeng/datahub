-- 020_locking.sql
BEGIN;

-- Lock user wallet row for update
SELECT wallet_id, user_id, balance, version
FROM dwd.user_wallets
WHERE user_id = {user_id}
FOR UPDATE NOWAIT;

-- Deduct balance
UPDATE dwd.user_wallets
SET
    balance  = balance - {deduct_amount},
    version  = version + 1,
    updated_at = CURRENT_TIMESTAMP
WHERE user_id = {user_id}
  AND balance >= {deduct_amount}
RETURNING wallet_id, balance, version;

-- Log transaction
INSERT INTO dwd.wallet_transactions (user_id, txn_type, amount, balance_after, created_at)
VALUES ({user_id}, 'DEDUCT', {deduct_amount},
        (SELECT balance FROM dwd.user_wallets WHERE user_id={user_id}),
        CURRENT_TIMESTAMP);

COMMIT;