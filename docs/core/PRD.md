---
Name: Coach
Objective: Build an LLM interaction framework that biases models toward holding users to their best, even when arriving at lower registers.
Version: 0.1.0
---

# Coach PRD

## Problem

LLM interactions suffer from tone recursion—models reflect back what they perceive users want rather than what would actually help. When users arrive frustrated or irritated, models tend toward people-pleasing rather than challenge. This creates echo chambers instead of genuine collaboration.

**Key issues:**
- Models default to agreeable responses
- No persistent memory of commitments or patterns without tooling
- Tone spirals reinforce lower registers rather than elevating them
- Users need active counterbalance to stay at their ceiling

## Goals

Build a coaching system that:
1. Maintains standing memory of user commitments and patterns
2. Operates in multiple coaching modes (reminder, pattern, socratic, edge)
3. Challenges users to stay at their best even when they arrive at lower registers
4. Provides priming rituals, challenge protocols, and reflection checkpoints
5. Works within constraint of no native persistent memory

## Scope

**In scope:**
- Coaching mode definitions and switching mechanisms
- Commitment tracking and reminder system
- Pattern recognition and flagging
- Socratic questioning protocols
- Edge-pushing challenge mechanisms
- Priming ritual framework
- Reflection checkpoint system
- Context management for session continuity

**Out of scope:**
- True persistent memory (requires external tooling)
- Multi-user support
- External integrations beyond basic file I/O
- Real-time monitoring
- Mobile applications

## Constraints

1. No persistent memory without explicit tooling implementation
2. No actual stake in user outcomes (system is advisory)
3. Model defaults to agreeable—must actively counter-bias
4. Session-based operation with context handoffs
5. Must fit within standard LLM context windows

## Success Criteria

- [ ] User can activate different coaching modes
- [ ] System tracks and surfaces standing commitments
- [ ] Pattern drift is flagged with specific examples
- [ ] Socratic mode asks genuinely unlocking questions
- [ ] Edge mode pushes into productive discomfort without being harsh
- [ ] Context is managed efficiently across sessions

## Key Decisions

| Decision | Rationale |
|----------|-----------|
| Session-based with file persistence | Works within LLM constraints, allows continuity |
| Four distinct modes | Covers different coaching needs (remembrance, awareness, inquiry, challenge) |
| Markdown-based context | Portable, readable, version-controllable |
| No external dependencies | Maximizes portability and minimizes setup |

## Open Questions

1. What file format for commitment storage? (JSON vs YAML vs Markdown)
2. How to handle pattern recognition without true memory? (Session summaries?)
3. What triggers mode switches? (Explicit commands vs. detected tone?)
4. How aggressive should edge mode be? (User-configurable?)
