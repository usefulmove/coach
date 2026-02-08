-- ACT-aligned Daily Accountability Schema
-- Based on Acceptance and Commitment Therapy framework

-- Daily entries table (core tracking)
CREATE TABLE IF NOT EXISTS daily_entries (
    date DATE PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Energy & Health Metrics (1-10 scales, NULL if not logged)
    overall_energy INTEGER CHECK(overall_energy BETWEEN 1 AND 10 OR overall_energy IS NULL),
    mental_health INTEGER CHECK(mental_health BETWEEN 1 AND 10 OR mental_health IS NULL),
    physical_health INTEGER CHECK(physical_health BETWEEN 1 AND 10 OR physical_health IS NULL),
    connection_quality INTEGER CHECK(connection_quality BETWEEN 1 AND 10 OR connection_quality IS NULL),
    
    -- ACT Core: Facing (not completing)
    faced_today TEXT,              -- "What did you face that was hard/scary?"
    facing_minutes INTEGER CHECK(facing_minutes >= 0 OR facing_minutes IS NULL), -- Time engaging with discomfort
    
    -- ACT Core: Avoidance awareness
    avoidance_urges TEXT,          -- "What did you notice wanting to avoid?"
    avoidance_noticed BOOLEAN DEFAULT FALSE, -- Did you catch yourself avoiding?
    
    -- ACT Core: Values in action
    values_in_action TEXT,         -- "What value did you move toward today?"
    values_moved_toward TEXT,      -- Specific value domains (health, relationships, growth, therapy, work)
    
    -- ACT Core: Clean vs Dirty Pain
    clean_pain_level INTEGER CHECK(clean_pain_level BETWEEN 1 AND 10 OR clean_pain_level IS NULL), -- Natural discomfort of growth
    dirty_pain_added BOOLEAN DEFAULT FALSE, -- Did self-judgment show up?
    self_judgment_noticed TEXT,    -- What self-critical thoughts arose?
    
    -- ACT Core: What did you get (not what you planned)
    what_i_got TEXT,               -- "What did you actually receive from today?"
    quality_of_presence INTEGER CHECK(quality_of_presence BETWEEN 1 AND 10 OR quality_of_presence IS NULL), -- Presence scale
    
    -- Link to narrative
    journal_path TEXT,             -- Path to detailed journal entry
    
    -- Metadata
    is_morning_entry BOOLEAN DEFAULT TRUE, -- Morning vs evening entry
    conversation_initiated_by TEXT -- How did this entry start (user, prompt, etc.)
);

-- Values and Commitments (ongoing, not daily)
CREATE TABLE IF NOT EXISTS commitments (
    id INTEGER PRIMARY KEY,
    created_date DATE DEFAULT CURRENT_DATE,
    commitment_text TEXT NOT NULL,
    value_domain TEXT CHECK(value_domain IN ('health', 'relationships', 'growth', 'therapy', 'work', 'creativity', 'other')),
    
    -- ACT: Is this a "facing" commitment? (involves discomfort)
    is_facing BOOLEAN DEFAULT FALSE,
    
    -- Status tracking
    status TEXT DEFAULT 'active' CHECK(status IN ('active', 'completed', 'migrated', 'abandoned')),
    completed_date DATE,
    
    -- ACT: Psychological flexibility tracking
    times_avoided INTEGER DEFAULT 0, -- How many times did avoidance show up?
    times_faced INTEGER DEFAULT 0,   -- How many times did you engage despite discomfort?
    
    -- Notes on the journey
    notes TEXT,
    
    -- Link to originating entry
    source_entry_date DATE,
    
    -- For tracking drift
    last_touched_date DATE DEFAULT CURRENT_DATE
);

-- Pattern Detection (auto-flagged or manually noted)
CREATE TABLE IF NOT EXISTS patterns (
    id INTEGER PRIMARY KEY,
    detected_date DATE DEFAULT CURRENT_DATE,
    pattern_type TEXT CHECK(pattern_type IN (
        'avoidance',           -- Repeated task avoidance
        'energy_drop',         -- Sustained low energy
        'inconsistency',       -- Streak breaking
        'overcommitment',      -- Too many facing tasks
        'self_judgment_spike', -- Increased dirty pain
        'isolation',           -- Connection quality drop
        'growth_stall',        -- No values movement
        'other'
    )),
    description TEXT,
    evidence TEXT,             -- Data supporting the pattern
    
    -- Tracking discussion
    discussed BOOLEAN DEFAULT FALSE,
    discussed_date DATE,
    discussion_notes TEXT,
    
    -- Resolution
    resolved BOOLEAN DEFAULT FALSE,
    resolved_date DATE
);

-- Weekly Synthesis (auto-generated + collaborative)
CREATE TABLE IF NOT EXISTS weekly_reviews (
    week_start DATE PRIMARY KEY,
    week_end DATE,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Metrics summary
    avg_energy DECIMAL(3,1),
    avg_mental_health DECIMAL(3,1),
    avg_physical_health DECIMAL(3,1),
    avg_connection DECIMAL(3,1),
    days_logged INTEGER,
    
    -- ACT-focused counts
    facing_moments INTEGER,        -- Days with facing_minutes > 0
    avoidance_flags INTEGER,       -- Days with avoidance_noticed = TRUE
    values_engaged INTEGER,        -- Days with values_in_action not NULL
    
    -- Pattern references
    patterns_detected TEXT,        -- JSON array of pattern IDs
    
    -- Collaborative notes
    discussion_notes TEXT,
    commitments_set TEXT,          -- JSON array of commitment IDs for next week
    
    -- Sonia integration
    mit_tasks_created INTEGER,
    mit_tasks_completed INTEGER,
    longest_mit_task TEXT          -- Task text of longest-running :mit: item
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_daily_entries_date ON daily_entries(date);
CREATE INDEX IF NOT EXISTS idx_commitments_status ON commitments(status);
CREATE INDEX IF NOT EXISTS idx_commitments_domain ON commitments(value_domain);
CREATE INDEX IF NOT EXISTS idx_patterns_type ON patterns(pattern_type);
CREATE INDEX IF NOT EXISTS idx_patterns_discussed ON patterns(discussed);
