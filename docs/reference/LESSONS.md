# Lessons

Accumulated insights from building and using Coach.

## 2025-02-04: Project Initialization

### Patterns
- Start minimal: four modes cover the coaching spectrum
- File-based persistence maximizes portability
- Markdown enables human-readable context

### Technical
- enso structure provides clear separation of concerns
- Core docs for source of truth, stories for active work
- Context scope prevents scope creep

### Open Questions
- How to balance challenge without being abrasive?
- What's the right granularity for commitment tracking?
- Should patterns be auto-detected or user-reported?

## Conventions

### File Naming
- `docs/core/`: Source of truth documents
- `docs/stories/[STORY-ID]-*.md`: Active work items
- `docs/reference/*.md`: Long-term memory
- `docs/logs/session-YYYY-MM-DD-*.md`: Session summaries
- `docs/skills/[skill-name]/`: Reusable capabilities

### Context Scope Declaration
Always include in stories:
- Write: Files to modify
- Read: Reference materials
- Exclude: Off-limits areas

### Mode Switching
Explicit over implicit: user commands mode switches rather than auto-detection.

## Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2025-02-04 | Four coaching modes | Covers spectrum: remember, notice, inquire, challenge |
| 2025-02-04 | File-based persistence | No external dependencies, human-readable |
| 2025-02-04 | Markdown format | Portable, version-controllable, readable |

## Anti-Patterns to Avoid

1. **Over-engineering persistence**: Start with files, add DB only when needed
2. **Implicit mode switching**: Explicit commands prevent confusion
3. **Too many modes**: Four is enough; don't fragment the experience
4. **Writing without reading**: Always check context scope first

## Skills Needed

- [ ] Mode switching protocol
- [ ] Commitment CRUD operations
- [ ] Pattern logging and retrieval
- [ ] Session compaction and handoff
