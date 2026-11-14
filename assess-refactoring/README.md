# assess-refactoring

Finds refactoring opportunities in the code a feature will touch, using SOLID principles. Each one becomes a standalone task to finish before feature work starts.

## Usage

Run it after `analyze-feature-impact`, in the same session:

```
/analyze-feature-impact Add CSV export to the orders page
/assess-refactoring
```

It can also run on its own (`/assess-refactoring for adding CSV export`). It then identifies the affected files itself first.

## Output

For each opportunity:

- **Problem**: what's wrong, and which SOLID principle it breaks
- **Proposed refactor**: the fix
- **Scope**: small, medium or large

Refactors are listed before feature tasks, in a recommended order, and never folded into feature sub-tasks. If it finds nothing, it says so.

## Related

- `analyze-feature-impact`: supplies the list of affected files.
