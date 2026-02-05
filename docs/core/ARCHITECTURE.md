---
Name: Coach
Version: 0.2.0
Last Updated: 2025-02-04
---

# Coach Architecture

## Overview

Coach is a context management and interaction framework designed to bias LLM conversations toward challenging users to stay at their best. It operates through a single Supportive stance with auto-tuning range, using session-based persistence via a seed file written at session end.

## Components

| Component | Responsibility | Location |
|-----------|----------------|----------|
| Coach Persona | Define stance, anti-sycophancy protocol, session flow | `AGENTS.md` |
| Session Seed | Compacted state to initialize next session | `SESSION.md` |
| Commitment Store | Persist and retrieve user commitments | `docs/reference/commitments.md` |
| Pattern Tracker | Log interaction patterns and flag drift | `docs/reference/patterns.md` |
| Session Capture | Skill for writing session state | `docs/skills/session-capture/SKILL.md` |
| Stance Reference | Detailed coaching persona documentation | `docs/core/COACH-PERSONA.md` |

## Session Flow

```
Session Start:
  Read AGENTS.md → Load Coach persona
  Read SESSION.md → Seed context from previous session
  ↓
During Session:
  Natural conversation
  Auto-tune supportive dial (1-10) based on user signals
  ↓
Session End (user signals):
  Use session-capture skill
  Write SESSION.md with distilled state
  User commits to git
```

## Key Abstractions

### Supportive Stance (Auto-Tuning)
Single stance that ranges from gentle to direct based on context:
- **1-3:** Gentle, spacious, exploratory (when user vulnerable or stuck)
- **4-7:** Direct but warm, asking hard questions with care (default range)
- **8-10:** Uncompromising, naming what user already knows but avoids (when coasting/avoiding)

**Auto-tuning triggers:**
- User signals: "push me", "be gentle", "challenge me"
- Context detection: confusion → more supportive, excuses → more direct
- Pattern recognition: recurring avoidance → increase directness

### Context Files
- `SESSION.md`: Seed state written at session end (standing commitments, priorities, patterns flagged, growth focus, insights, open threads)
- `commitments.md`: Detailed commitment tracking with history
- `patterns.md`: Pattern observations with examples and resolutions
- `LESSONS.md`: Accumulated insights and conventions

### Five Operations (from enso, reframed)
| Operation | Coaching Purpose |
|-----------|------------------|
| **Witness** | Persist insights, commitments, patterns outside working memory |
| **Attend** | Load only what serves this moment of growth |
| **Inquire** | Ask before assuming |
| **Distill** | Extract essential truth from complexity |
| **Elevate** | Bring in best resources for the challenge at hand |

## Integration Points

| External | Interface | Purpose |
|----------|-----------|---------|
| OpenCode/LLM | AGENTS.md persona injection | Automatic stance loading |
| File System | Markdown files | Persistence without external DB |
| Git | User-managed commits | Session history and versioning |
| User | Direct chat + file editing | Primary interaction surface |

## State Management

**Ephemeral (per-session):**
- Current supportive dial level (1-10)
- Conversation context
- Detected patterns and insights

**Persisted (in SESSION.md):**
- Standing commitments
- Active priorities
- Flagged avoidance patterns
- Growth focus area
- Key insights from session
- Open questions for next session
- Notes for Coach (observations about user state)

**Reference (docs/reference/):**
- Long-term commitment history
- Pattern library
- Coaching research and methodology

## Extension Points

1. **New Skills**: Add to `docs/skills/` for specific workflows
2. **Database Backend**: If SESSION.md grows too large, migrate to SQLite
3. **Integrations**: Add external APIs (calendar, task managers, etc.)
4. **Metrics**: Track session cadence, commitment completion rates, etc.
