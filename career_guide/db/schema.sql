-- =====================================================
-- career_guide_ai : Database Schema (with pgvector support)
-- =====================================================

-- Enable pgvector extension (run this once)
-- CREATE EXTENSION IF NOT EXISTS vector;

-- =====================================================
-- USERS TABLE
-- =====================================================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- QUESTIONS TABLE
-- =====================================================
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    section VARCHAR(100),
    difficulty VARCHAR(50),
    text TEXT NOT NULL,
    options JSONB NOT NULL,
    correct_option VARCHAR(255),
    weight FLOAT DEFAULT 1.0
);

-- =====================================================
-- ASSESSMENTS TABLE
-- =====================================================
CREATE TABLE assessments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- =====================================================
-- RESPONSES TABLE
-- =====================================================
CREATE TABLE responses (
    id SERIAL PRIMARY KEY,
    assessment_id INTEGER REFERENCES assessments(id) ON DELETE CASCADE,
    question_id INTEGER REFERENCES questions(id) ON DELETE CASCADE,
    selected_option VARCHAR(255),
    score FLOAT DEFAULT 0
);

-- =====================================================
-- RESULTS TABLE
-- =====================================================
CREATE TABLE results (
    id SERIAL PRIMARY KEY,
    assessment_id INTEGER REFERENCES assessments(id) ON DELETE CASCADE,
    scores JSONB,
    primary_track VARCHAR(100),
    secondary_track VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- CAREERS TABLE (with vector embedding)
-- =====================================================
CREATE TABLE careers (
    id SERIAL PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    track VARCHAR(100),
    skills JSONB,
    description TEXT,
    avg_salary_range VARCHAR(100),
    sample_roles JSONB
    -- embedding VECTOR(1536)  -- OpenAI/transformer-based embeddings
);

-- =====================================================
-- CAREER KNOWLEDGE BASE TABLE (with vector embedding)
-- =====================================================
CREATE TABLE career_kb (
    id SERIAL PRIMARY KEY,
    career_id INTEGER REFERENCES careers(id) ON DELETE CASCADE,
    title VARCHAR(150),
    content TEXT,
    tags TEXT[]
    -- embedding VECTOR(1536)
);

-- =====================================================
-- PLANS TABLE
-- =====================================================
CREATE TABLE plans (
    id SERIAL PRIMARY KEY,
    result_id INTEGER REFERENCES results(id) ON DELETE CASCADE,
    plan_json JSONB
);
-- =====================================================
-- INDEXES for Performance
-- =====================================================
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_questions_section ON questions(section);
CREATE INDEX idx_assessments_user_id ON assessments(user_id);
CREATE INDEX idx_responses_assessment_id ON responses(assessment_id);
CREATE INDEX idx_results_assessment_id ON results(assessment_id);
CREATE INDEX idx_careers_track ON careers(track);
CREATE INDEX idx_career_kb_tags ON career_kb USING GIN (tags);
CREATE INDEX idx_career_skills ON careers USING GIN (skills);
CREATE INDEX idx_plans_result_id ON plans(result_id);

-- Vector indexes for similarity search
-- CREATE INDEX idx_careers_embedding ON careers USING ivfflat (embedding vector_cosine_ops);
-- CREATE INDEX idx_career_kb_embedding ON career_kb USING ivfflat (embedding vector_cosine_ops);

-- =====================================================
-- End of schema.sql
-- =====================================================
