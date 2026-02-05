---
Status: active
Priority: high
Created: 2025-02-04
---

# [COACH-001] Define Mode Switching Protocol

## Goal

Define and implement the protocol for switching between Coach's four coaching modes (reminder, pattern, socratic, edge) including command structure, mode-specific behaviors, and context handling.

## Acceptance Criteria

- [ ] Document the four coaching modes with specific behaviors
- [ ] Define command syntax for mode switching
- [ ] Create mode-specific prompt templates
- [ ] Implement mode detection logic (if auto-switching)
- [ ] Test mode transitions with example conversations

## Context Scope

**Write:**
- docs/skills/mode-switching/SKILL.md
- docs/reference/mode-definitions.md
- docs/skills/mode-switching/templates/

**Read:**
- docs/core/PRD.md
- docs/core/ARCHITECTURE.md

**Exclude:**
- Implementation code (not yet)
- External integrations

## Approach & Verification Plan

1. Research existing mode-based coaching systems
2. Define concrete behaviors for each mode
3. Design minimal command interface
4. Create prompt templates that embody each mode's stance
5. Document activation triggers and context requirements
6. Test with sample user inputs to verify mode character

## Notes

Mode switching is the core interaction pattern. Each mode should feel distinctly different while maintaining the Coach's fundamental stance (holding users to their best).

Reminder mode = "What did you say you'd do?"
Pattern mode = "I've noticed..."
Socratic mode = "What if...?"
Edge mode = "The hard truth is..."
