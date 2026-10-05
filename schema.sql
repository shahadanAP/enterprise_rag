CREATE TABLE query_log (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    confidence TEXT NOT NULL,
    sources TEXT,
    latency_ms INTEGER,
    created_at TIMESTAMP DEFAULT NOW()

);