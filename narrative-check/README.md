# Narrative check

A Claude Code skill that audits writing you already have. It checks two things: whether a section's
paragraphs come in an order that builds (no drifting, looping back, repeating or ending twice), and
whether its sentences are clear (no empty openers, unnamed sources, hidden setup or vague
metaphors). It maps what each paragraph does, names the problems, proposes a reordered outline that
keeps your own sentences, and rewrites only after you agree. When you ask it to add a claim, it
checks the claim first and tells you if it overreaches.

It complements `explainer-voice`: that skill is how Claude writes; this one is how Claude edits.

## Install

```bash
cp -r narrative-check ~/.claude/skills/
```

## Use

```text
/narrative-check the "Ontology" section of src/content/articles/MyArticle.jsx
```

Or just describe the problem: "this section drifts, I don't see a logical order, correct me if I'm
wrong", or "this paragraph is vague and unclear".

## Files

- `SKILL.md`: the workflow, the drift and clarity patterns, and how to apply fixes.
- `references/patterns.md`: worked before-and-after cases.
