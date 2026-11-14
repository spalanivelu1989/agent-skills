---
name: analyze-feature-impact
description: 'Map the files, components and dependencies a planned feature will touch, before any tasks are written. Use at the start of feature planning; its output feeds assess-refactoring.'
---

# Analyze Feature Impact
Works out where in the codebase a feature lands, so planning starts from the real code rather than guesses.

## When to Use
- At the start of feature planning, before breaking work into tasks.
- Run `assess-refactoring` next, using this skill's output as its input.

## Inputs
- The feature request: a description, ticket, spec or acceptance criteria.
- If the request is too vague to locate in code, ask one focused question before analysing.

## Steps
1. **Find the entry points**: the routes, screens, commands, API endpoints, jobs or events where the feature starts. Search the codebase; don't assume names.
2. **Trace the flow**: follow each entry point through the code it calls (UI → state/hooks → services → data access → storage or external APIs).
3. **Classify each file/component**:
   - **Modify**: existing code that must change.
   - **Create**: new files/components the feature needs.
   - **Read-only dependency**: code the feature relies on but shouldn't change.
4. **Find the ripple effects**: other callers of anything being modified, shared types/interfaces, config, schemas/migrations, and feature flags.
5. **Check the tests**: existing tests covering the affected code, and gaps where none exist.

## Output
- **Affected files/components** — a table with path, classification (modify / create / read-only), and a one-line reason.
- **Dependencies & ripple effects** — what else could break, and why.
- **Data & contract changes** — schema, API, event or type changes, if any.
- **Test coverage** — existing tests to update, and gaps to fill.
- **Risks & unknowns** — anything unverified, stated plainly as an assumption.

Base every entry on code you actually read; cite paths. Do not propose tasks or refactors here; that comes next, starting with `assess-refactoring`.
