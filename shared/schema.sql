-- ============================================
-- GEO AI Agent for E-commerce VN — DB Schema
-- ============================================
-- Source: GEO_AI_Agent_Ecommerce_VN.md §19.3
-- Ngày: 2026-08-02
-- Owner: Đăng (Tech Lead)
-- ============================================

-- Enable UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- 1. Brands (2 brand target + 4-6 đối thủ)
-- ============================================
CREATE TABLE brands (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    name_variants JSONB NOT NULL DEFAULT '[]',  -- ['Minh Long', 'Minh Long Book', 'MLB']
    brand_type VARCHAR(50),  -- 'sàn' | 'd2c' | 'retailer'
    is_target BOOLEAN NOT NULL DEFAULT FALSE,
    category VARCHAR(100),
    shopee_url VARCHAR(500),
    lazada_url VARCHAR(500),
    website_url VARCHAR(500),
    knowledge_base JSONB NOT NULL DEFAULT '{}',  -- {price_table, ship_policy, faq, rating}
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_brands_name ON brands(name);
CREATE INDEX idx_brands_is_target ON brands(is_target);

-- ============================================
-- 2. Prompts (prompt library ~100 prompts / 5 nhóm)
-- ============================================
CREATE TABLE prompts (
    id SERIAL PRIMARY KEY,
    text VARCHAR(1000) NOT NULL,
    "group" VARCHAR(50) NOT NULL,  -- 'uy_tin' | 'gia' | 'so_sanh' | 'review' | 'ship'
    language VARCHAR(10) NOT NULL DEFAULT 'vi',
    tags JSONB NOT NULL DEFAULT '[]',
    difficulty VARCHAR(20) NOT NULL DEFAULT 'medium',  -- 'easy' | 'medium' | 'hard'
    expected_mentions JSONB NOT NULL DEFAULT '[]',
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_prompts_group ON prompts("group");

-- ============================================
-- 3. Responses (raw response từ 4 AI: ChatGPT, Gemini, Claude, Tavily)
-- ============================================
CREATE TABLE responses (
    id SERIAL PRIMARY KEY,
    brand_id INT NOT NULL REFERENCES brands(id) ON DELETE CASCADE,
    prompt_id INT NOT NULL REFERENCES prompts(id) ON DELETE CASCADE,
    ai_engine VARCHAR(20) NOT NULL,  -- 'chatgpt' | 'gemini' | 'claude' | 'tavily'
    model_version VARCHAR(100),
    response_text TEXT NOT NULL,
    citations JSONB NOT NULL DEFAULT '{}',  -- URL citation mà AI/Tavily tham chiếu
    run_index INT NOT NULL,  -- 1, 2, 3 (3 lần/prompt/ngày cho Stability)
    latency_ms INT,
    cost_usd DECIMAL(10, 6),
    trace_id VARCHAR(64),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_responses_brand_id ON responses(brand_id);
CREATE INDEX idx_responses_prompt_id ON responses(prompt_id);
CREATE INDEX idx_responses_ai_engine ON responses(ai_engine);
CREATE INDEX idx_responses_run_index ON responses(run_index);
CREATE INDEX idx_responses_created_at ON responses(created_at);
CREATE INDEX idx_responses_brand_prompt ON responses(brand_id, prompt_id);

-- ============================================
-- 4. Mentions (extracted mention từ response)
-- ============================================
CREATE TABLE mentions (
    id SERIAL PRIMARY KEY,
    response_id INT NOT NULL REFERENCES responses(id) ON DELETE CASCADE,
    brand_name VARCHAR(255) NOT NULL,
    is_target_brand BOOLEAN NOT NULL DEFAULT FALSE,
    position INT NOT NULL,  -- 1, 2, 3 (vị trí nhắc đến)
    sentiment DECIMAL(3, 2) NOT NULL,  -- -1.00 to +1.00
    context_quote TEXT,
    claim_type VARCHAR(20),  -- 'price' | 'ship' | 'review' | 'general'
    confidence DECIMAL(3, 2) DEFAULT 1.00,
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,  -- HITL verified
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_mentions_response_id ON mentions(response_id);
CREATE INDEX idx_mentions_brand_name ON mentions(brand_name);
CREATE INDEX idx_mentions_is_target ON mentions(is_target_brand);

-- ============================================
-- 5. Stability Scores (per brand, prompt, ai_engine)
-- ============================================
CREATE TABLE stability_scores (
    id SERIAL PRIMARY KEY,
    brand_id INT NOT NULL REFERENCES brands(id) ON DELETE CASCADE,
    prompt_id INT NOT NULL REFERENCES prompts(id) ON DELETE CASCADE,
    ai_engine VARCHAR(20),
    stability_score DECIMAL(4, 3) NOT NULL,  -- 1 - normalized variance
    visibility_rate DECIMAL(4, 3) NOT NULL,  -- 0.000 to 1.000
    n_runs INT NOT NULL,
    is_stable BOOLEAN NOT NULL,  -- TRUE if score >= 0.7
    computed_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_stability_brand_id ON stability_scores(brand_id);
CREATE INDEX idx_stability_prompt_id ON stability_scores(prompt_id);
CREATE INDEX idx_stability_is_stable ON stability_scores(is_stable);

-- ============================================
-- 6. Diagnoses (output từ Diagnosis Agent)
-- ============================================
CREATE TABLE diagnoses (
    id SERIAL PRIMARY KEY,
    brand_id INT NOT NULL REFERENCES brands(id) ON DELETE CASCADE,
    prompt_id INT NOT NULL REFERENCES prompts(id) ON DELETE CASCADE,
    is_stable BOOLEAN NOT NULL,
    stability_score DECIMAL(4, 3) NOT NULL,
    hypotheses JSONB NOT NULL DEFAULT '[]',
    -- [{hypothesis, confidence, evidence_urls: [url], quote_span: str, claim_type: str}]
    evidence_package JSONB NOT NULL DEFAULT '{}',
    recommended_actions JSONB NOT NULL DEFAULT '[]',
    severity VARCHAR(20) NOT NULL DEFAULT 'medium',  -- 'low' | 'medium' | 'high' | 'critical'
    status VARCHAR(20) NOT NULL DEFAULT 'pending_review',  -- 'pending_review' | 'approved' | 'rejected' | 'in_progress'
    reviewed_by VARCHAR(100),
    reviewed_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_diagnoses_brand_id ON diagnoses(brand_id);
CREATE INDEX idx_diagnoses_prompt_id ON diagnoses(prompt_id);
CREATE INDEX idx_diagnoses_status ON diagnoses(status);
CREATE INDEX idx_diagnoses_severity ON diagnoses(severity);
CREATE INDEX idx_diagnoses_created_at ON diagnoses(created_at);

-- ============================================
-- 7. Tasks (action backlog + closed-loop)
-- ============================================
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    brand_id INT NOT NULL REFERENCES brands(id) ON DELETE CASCADE,
    diagnosis_id INT REFERENCES diagnoses(id),
    action_type VARCHAR(50) NOT NULL,
    -- 'listing_update' | 'schema_add' | 'outreach' | 'content_pr' | 'content_add'
    action_payload JSONB NOT NULL DEFAULT '{}',
    owner_team VARCHAR(100),
    status VARCHAR(20) NOT NULL DEFAULT 'todo',  -- 'todo' | 'in_progress' | 'done' | 'cancelled'
    pre_scan_id INT REFERENCES responses(id),
    post_scan_id INT REFERENCES responses(id),
    result VARCHAR(20),  -- 'improved' | 'no_evidence' | 'regressed'
    ci_lower DECIMAL(4, 3),
    ci_upper DECIMAL(4, 3),
    pre_visibility DECIMAL(4, 3),
    post_visibility DECIMAL(4, 3),
    completed_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tasks_brand_id ON tasks(brand_id);
CREATE INDEX idx_tasks_diagnosis_id ON tasks(diagnosis_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_result ON tasks(result);
CREATE INDEX idx_tasks_created_at ON tasks(created_at);

-- ============================================
-- Comments
-- ============================================
COMMENT ON TABLE brands IS 'Brand E-commerce (2 target + 4-6 đối thủ)';
COMMENT ON TABLE prompts IS 'Prompt library ~100 prompts / 5 nhóm';
COMMENT ON TABLE responses IS 'Raw responses từ 4 AI (ChatGPT, Gemini, Claude, Tavily)';
COMMENT ON TABLE mentions IS 'Extracted mentions từ response (NER)';
COMMENT ON TABLE stability_scores IS 'Stability Score per (brand, prompt, ai_engine) - gate cho diagnosis';
COMMENT ON TABLE diagnoses IS 'Diagnosis output từ Diagnosis Agent (HITL approve/reject)';
COMMENT ON TABLE tasks IS 'Action backlog + closed-loop result (improved/no_evidence/regressed)';
