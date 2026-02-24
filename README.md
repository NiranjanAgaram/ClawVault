# ClawVault: Institutional-Grade Solana Forensics via OpenClaw

**Project Title:** ClawVault  
**Bounty:** Spark Hackathon #1 — OpenClaw Instances for Investors  
**Lead Architect:** Niranjan Agaram (10+ YOE Lead Data Engineer and AI Consultant)

---

## 1. Project Vision
ClawVault is a production-grade AI Agent instance built on the **OpenClaw** framework. It bridges the gap between raw Solana RPC data and investor-ready intelligence. By implementing a **Medallion Data Architecture** (Bronze/Silver/Gold), ClawVault ensures that the AI Agent is fed high-integrity, idempotent on-chain data to provide reliable risk assessments on "Whales" and "Liquidity Locks."

---

## 2. Data Pipeline Architecture
The ClawVault data plane is organized as a classic lakehouse, optimized for low-latency Solana ingestion and AI-grade analytics.

graph TD
    A[Solana RPC: Helius/Alchemy] -->|Raw Logs| B(Bronze: Append-Only Storage)
    B -->|Normalization| C(Silver: Indexed SQL Tables)
    C -->|Whale Scoring| D(Gold: Analytic Warehouse)
    C -->|Lock Detection| D
    E[Off-Chain Signals: X/Discord] -->|Embeddings| F(Vector DB)
    D --> G{OpenClaw Agent}
    F --> G
    G -->|RAG Narrative| H[Investor Risk Report]
    style G fill:#f96,stroke:#333,stroke-width:4px

### Bronze Layer – Raw Ingestion (Helius/Alchemy RPC)
*   **Streaming Ingestion:** Maintains a loop against Helius/Alchemy Solana RPC endpoints, pulling confirmed transaction logs, account deltas, and program instruction traces.
*   **Append-Only Store:** Payloads are persisted in a raw store with no mutation, preserving exact RPC responses (hex-encoded instructions, signatures, slot, and log messages).
*   **Traceability:** Each record is annotated with a deterministic ingestion key: `signature`, `slot`, `source_rpc`, and `ingestion_ts` to support downstream idempotency and replay.

### Silver Layer – Normalization and Feature Indexing

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


A dedicated service decodes binary/hex data into structured, SQL-ready entities (transactions, instructions, accounts, and events).
*   **Whale Identification:** Pipelines compute address-level metrics (notional volume, velocity of capital rotation). Addresses breaching thresholds are tagged with a `whale_score`.
*   **Liquidity-Lock Detection:** Inspects instructions for known lock patterns (LP positions sent to lock contracts, time-locked vaults, renounced authorities). 
*   **Semantic Fields:** Extracts `lock_start`, `lock_end`, and `locked_notional` into indexed tables.

### Gold Layer – Analytic Warehouse and Vectorized Sentiment
Fuses two critical truth sources:
1.  **On-Chain Truth (SQL):** A columnar SQL warehouse containing the Silver-layer tables, indexed for low-latency analytical queries.
2.  **Market Sentiment (Vector DB):** Stores embeddings of off-chain signals (X posts, research notes, community messages) keyed by asset and time window.

---

## 3. Agentic Intelligence Layer
At the core of ClawVault is an **OpenClaw-based agent** that acts as the “brain” for investor-facing analytics.

### OpenClaw as the Agentic Brain
ClawVault extends the OpenClaw base agent class to define an **InvestorPersonality** agent. This subclass encodes risk preferences and decision heuristics oriented around Solana investors (conservative vs. degen profiles).

### RAG Pattern over Gold Layer (SQL + Vector DB)
The agent uses a **Retrieval-Augmented Generation (RAG)** pattern:
*   **Structured Retrieval (SQL):** Fetches canonical facts (whale participation, lock coverage, unlock schedules).
*   **Unstructured Retrieval (Vector DB):** Queries for semantically related sentiment (governance concerns, exploit reports, developer reputation).
*   **Explainability:** The agent’s reasoning chain is logged, enabling transparency on how each risk assessment was derived.

---

## 4. System Resiliency
Designed as a production-grade system with explicit measures for robustness.

*   **Idempotent Processing:** All ingestion and transformation jobs use `signature` and `slot` identifiers to ensure that replays cannot double-count on-chain activity.
*   **Exactly-Once Semantics:** Upserts into Silver/Gold tables ensure that the final state remains consistent regardless of retries.
*   **RPC Tolerance:** Implements automatic retries with exponential backoff and jitter for rate-limiting tolerance (Helius/Alchemy).
*   **Circuit-Breaker Logic:** Safely sheds non-critical workloads to preserve capacity for "tip of chain" ingestion during RPC congestion.

---

## 5. Roadmap
- **Week 1-2:** Scaffolding OpenClaw instance & Helius indexing pipeline.
- **Week 3-4:** Agentic Forensics implementation & RAG logic.
- **Week 5-6:** Investor Dashboard launch & Futarchy Governance integration.

---

## 6. About the Lead
**Niranjan Agaram** is a Lead Data Engineer and AI Consultant with 10+ years of experience in architecting high-throughput data systems using Databricks, Spark, and multi cloud stack(GCP,AWS,Azure). Specializing in data integrity and scalable AI-native pipelines.

[Website](https://niranjanagaram.com) | [LinkedIn](https://www.linkedin.com/in/niranjanagaram/) | [X (Twitter)](https://x.com/niranjanagaram)
