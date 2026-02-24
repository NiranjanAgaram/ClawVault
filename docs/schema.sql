-- Silver Layer: Liquidity Lock Events
CREATE TABLE liquidity_lock_events (
    signature CHAR(88) PRIMARY KEY,
    slot BIGINT NOT NULL,
    pool_address CHAR(44),
    token_mint CHAR(44),
    locked_notional_usd DECIMAL(18, 2),
    lock_duration_seconds INT,
    unlock_timestamp TIMESTAMP,
    ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Silver Layer: Whale Signatures
CREATE TABLE whale_signatures (
    address CHAR(44) PRIMARY KEY,
    whale_score INT,
    total_volume_30d_usd DECIMAL(18, 2),
    capital_rotation_velocity FLOAT,
    last_active_slot BIGINT
);
