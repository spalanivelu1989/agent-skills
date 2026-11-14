---
name: assess-refactoring
description: 'Identify refactoring opportunities in the code a feature will touch, using SOLID principles. Use during feature planning to surface refactors that should be done before feature work.'
---

# Assess Refactoring Opportunities
Evaluates the affected code for refactors that a feature naturally creates an opportunity to make.

## When to Use
- During feature planning, after `analyze-feature-impact`.
- Each opportunity found becomes a **standalone task to complete before feature work begins**.

## Inputs
- The affected files/components from `analyze-feature-impact`.
- If that output isn't available, first identify the files/components the feature will touch, and assess only those.

## Lens - SOLID
- **Single Responsibility**: components/modules doing too much that could be split.
- **Open/Closed**: can new behavior be added via extension instead of modifying existing code?
- **Liskov Substitution**: subtypes that break expected behavior.
- **Interface Segregation**: components/hooks depending on props/interfaces they don't use.
- **Dependency Inversion**: high-level modules coupled to low-level details.

## Output
For each opportunity, a standalone task:
- **Problem** — with a reference to the SOLID principle it violates.
- **Proposed refactor**.
- **Scope** — small / medium / large.

List refactors **before** feature tasks with a recommended order: refactors first, then feature implementation. Do **not** fold refactors into feature sub-tasks.

If no opportunities are found, say so explicitly and proceed to feature tasks.
