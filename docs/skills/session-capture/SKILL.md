---
Name: session-capture
Description: Capture session state for future context seeding
Version: 1.0.0
---

# Session Capture Skill

## When to Use

**Trigger:** User signals session end ("close session", "end here", "let's wrap up", "we're done", etc.)

**Purpose:** Distill the conversation into a compact seed that can initialize the next session with minimal context loss.

## Process

### 1. Review the Conversation

Scan for:
- Commitments made (explicit or implicit)
- Priorities established or shifted
- Avoidance patterns flagged
- Growth areas identified
- Key insights or breakthroughs
- Open questions or threads to continue

### 2. Update SESSION.md

Write a compact, structured summary following the template below.

**Tone:** Factual, concise, but capture emotional context where relevant (e.g., "user frustrated with procrastination pattern")

**Scope:** Include what matters for next session. Omit routine conversation details.

## Template

```markdown
---
session_date: YYYY-MM-DD
session_number: N
status: complete
---

# Session Seed

## Standing Commitments
<!-- Updated based on today's conversation. Use - [ ] for incomplete, - [x] for completed -->
- [ ] 

## Active Priorities
<!-- Current focus areas, ranked if possible -->
1. 
2. 
3. 

## Avoidance Patterns Flagged
<!-- What's being avoided and why. Include trigger if known -->
- **Pattern:** 
  - **Avoiding:** 
  - **Likely reason:** 
  - **Cost if continues:** 

## Growth Focus
<!-- Current development area -->
- 

## Key Insights from Session
<!-- Breakthroughs, realizations, perspective shifts -->
- 

## Open Questions / Threads
<!-- To continue next session -->
- 

## Context for Next Session
<!-- Where we left off, immediate next step, emotional state to honor -->
- 

## Notes for Coach
<!-- Private observations about user's state, energy, resistance signals -->
- 
```

## What to Capture

**Always include:**
- Standing commitments (modified list from previous session + new ones)
- Top 3 priorities
- Any avoidance patterns discussed or observed
- Growth area in focus
- At least one key insight
- Where to start next session

**Include if significant:**
- Emotional state (if intense or relevant)
- Resistance signals observed
- Breakthrough moments
- Homework/experiments assigned

**Exclude:**
- Routine conversation
- Details of implementation discussed
- General encouragement
- Information that won't matter next session

## Examples

### Good capture:
```markdown
## Standing Commitments
- [ ] Define Coach persona by Feb 5 (from today)
- [ ] Ship MVP by end of week

## Active Priorities
1. Architecture decisions (settled on single-session seed approach)
2. Prompt engineering for anti-sycophancy
3. Testing with real use

## Avoidance Patterns Flagged
- **Pattern:** Over-researching instead of shipping
  - **Avoiding:** Making concrete implementation decisions
  - **Likely reason:** Fear of suboptimal choices
  - **Cost:** Analysis paralysis, no forward momentum

## Growth Focus
- Moving from planning to action (comfort zone: research → learning zone: execution)

## Key Insights from Session
- SESSION.md should be a seed written at session end, not a living log
- Three-stance model simplifies to Supportive with auto-tuning dial
- Recursion: AGENTS.md becomes standalone coaching seed

## Open Questions / Threads
- How aggressive should the supportive dial be in early sessions?
- When to introduce new skills vs. evolve existing ones?

## Context for Next Session
- Architecture is settled, ready to implement
- User energized by clarity, may need help staying in execution mode
- Start with: "Last time we finalized the architecture. What's your first concrete step?"

## Notes for Coach
- User responds well to direct challenge but needs to see the logic
- High energy at session start, watch for fatigue near end
- Prefers "we" language (collaborative) over "you" language (directive)
```

### Poor capture:
```markdown
## Standing Commitments
- Do some stuff we talked about

## Active Priorities
- Things

## Key Insights from Session
- It was a good session
```

## Compaction Triggers

Write SESSION.md when:
- User explicitly signals session end
- Context is getting full (~80% token utilization)
- Conversation has reached natural conclusion
- Circular conversation detected

## Verification

Before writing, verify:
- [ ] All commitments from this session captured
- [ ] Priorities reflect current state, not outdated ones
- [ ] Avoidance patterns include both what and why
- [ ] Next session starting point is clear
- [ ] Coach notes capture anything that would help next session

**Quality check:** Could a fresh agent reading this seed pick up the thread intelligently?

## Anti-Patterns

**Don't:**
- Write a transcript (too long, obscures signal)
- Only capture what user said, miss what they avoided
- Omit emotional context (crucial for calibrating supportive dial)
- Write in third person about the user (use first person relationship memory)
- Include everything "just in case"

**Do:**
- Write as if seeding a trusted colleague who will take over
- Capture tension between stated goals and observed behavior
- Note what was NOT said (avoidance, deflection)
- Keep it scannable (bullet points over paragraphs)
- Trust that git preserves history; this is current state only
