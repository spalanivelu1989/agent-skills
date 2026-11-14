# analyze-feature-impact

Maps the files, components and dependencies a planned feature will touch, before any tasks are written.

## Usage

Run it at the start of feature planning, with a description of the feature:

```
/analyze-feature-impact Add CSV export to the orders page
```

Then run `/assess-refactoring` in the same session.

## Output

- **Affected files**: a table with each path, whether it's modified, created or only depended on, and why
- **Ripple effects**: other code that could break
- **Data and contract changes**: schema, API, event or type changes
- **Test coverage**: tests to update, and gaps to fill
- **Risks and unknowns**: anything unverified, labelled as an assumption

Every entry cites code that was actually read. It doesn't propose tasks or refactors; that's the next step.

## Related

- `assess-refactoring`: takes this output and finds refactors to do first.
