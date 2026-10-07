# HTML format

A Claude Code skill that produces a **standalone, self-contained HTML document** in the house design system.

The design uses a teal accent and IBM Plex Mono type, with a full-width layout and margin sidenotes. Every page gets a generated sidebar, a built-in search box, card sections and callouts. It also shows reading time per section and a reading-progress rail, and has a light / paper / dark toggle. The page is a single file with no build step, and it opens directly in a browser.

Use it for guides, walkthroughs, runbooks, proposals, explainers, onboarding docs, reports, FAQs and specs. Use it also to convert a Markdown document to HTML, or to add a page that matches an existing set.

## Install

```bash
cp -r html-format ~/.claude/skills/
```

Requirements: Python 3, standard library only, for the checker.

## Use

Ask Claude Code, for example:

```text
Write the onboarding guide as an HTML page in our house style
Convert docs/runbook.md to HTML, matching index.html
```

Claude copies `assets/template.html` and fills it with your content, using the existing components rather than new CSS. It chooses **tabbed** navigation for step-by-step journeys and **scroll** navigation for references, proposals and FAQs. It then runs the checker before handing the page over.

To lint a finished page yourself:

```bash
python3 ~/.claude/skills/html-format/scripts/check.py page.html
```

The checker exits with status 1 if it reports any ERROR. WARN lines are judgement calls.

## Files

| Path | What it is |
|---|---|
| `SKILL.md` | Full workflow, navigation modes, writing rules, Markdown conversion, palette |
| `assets/template.html` | The template: all CSS, theme toggle, search and navigation scripts |
| `references/components.md` | Catalogue of every component, with copy-paste markup |
| `scripts/check.py` | Linter for finished pages |
