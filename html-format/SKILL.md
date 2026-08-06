---
name: html-format
description: Produces a standalone, self-contained HTML document in the house design system — teal accent, IBM Plex Mono typography with a proportional sidebar, sidebar navigation, card sections, callouts, light/dark toggle. Use this whenever the deliverable is an HTML page rather than Markdown: guides, walkthroughs, runbooks, proposals, explainers, onboarding docs, reports, FAQs, or specs. Trigger it when someone asks for a document "as HTML", "as a web page", "in the same style/format as index.html", "in our house style", "matching the other pages", or asks to convert an existing Markdown/text document into a styled HTML page. Also use it when adding a new companion page to a documentation set that already uses this system, so the new page matches the rest.
---

# House HTML document format

This skill produces one file: a self-contained HTML document that looks and
behaves like the reference implementation at `index.html` — a teal-accented,
card-based reading experience with a sidebar, semantic callouts, and a light/dark
toggle that respects the OS but can be overridden.

The whole design system already exists as CSS in `assets/template.html`. Your job
is to structure the content well and reach for the right components — not to
invent styling. **Do not write new CSS.** If you find yourself adding a `<style>`
rule or a `style=` attribute, you are almost certainly reaching for a component
that already exists under a different name; check
`references/components.md` first.

## Workflow

### 1. Copy the template

```bash
cp ~/.claude/skills/html-format/assets/template.html <destination>.html
```

Then edit it in place. Starting from the template rather than writing HTML from
scratch is what guarantees the theme tokens, the toggle script, the responsive
breakpoints and the print styles all stay intact — they are easy to reproduce
almost-correctly and hard to reproduce exactly.

If the document is joining an existing set of pages, open a sibling page first
and match its conventions (storage keys, footer style, relative link paths).

### 2. Read the component catalog

Read `references/components.md`. It lists every available class with
copy-pasteable markup and says what each is _for_. Skimming it before writing
content is what stops a document from degenerating into undifferentiated
paragraphs — the components exist to carry meaning, and if you don't know they're
there you won't use them.

### 3. Choose the navigation mode

The `data-nav` attribute on the `<html>` element picks one of two behaviours.
Both use the same sidebar markup, so this is a one-word decision, not a
restructure. Edit that one attribute — never find-and-replace the value across
the file.

**`data-nav="tabbed"`** — one section visible at a time. The sidebar acts as a
step tracker and a prev/next pager appears at the bottom. Choose this when the
document is a **journey**: sequential phases, a setup walkthrough, a course, a
process with an order. Hiding the other sections is the point — it keeps a long
document from looking intimidating and gives the reader a sense of progress.
Roughly: 4 or more sections that are meant to be done in order.

**`data-nav="scroll"`** — everything visible, sidebar is a table of contents that
highlights the section under the reader. Choose this when the document is a
**reference or an argument**: a proposal read top to bottom, an explainer, an
FAQ, a spec, a report. Readers of these want to scroll, skim and Ctrl-F, and
hiding sections actively hurts them. Also correct for anything under about 4
sections, where a pager would be more ceremony than the content deserves.

In scroll mode, delete the `.pager` div (it is hidden by CSS anyway, but leaving
dead markup in the file invites confusion later).

Both modes degrade gracefully: with JavaScript disabled every section is visible
and the pager disappears, so a tabbed document still reads as an ordinary page.
That is why the CSS keys off a `.js-tabbed` class the head script adds rather
than off `data-nav` directly — leave that arrangement alone.

If the document has no sections at all — a single short note — delete the whole
`.layout` wrapper and put the content directly in `<main>` after the lede. The
card styling of `section.phase` still works standalone.

### 4. Write the content

Section titles are `h2` inside `section.phase`; the document has exactly one
`h1`, above the layout. Give every section an `id`, and make the sidebar `a.tab`
hrefs match those ids in the same order — the script derives everything from that
correspondence, including the pager labels.

Reach for the components that match what you're actually saying:

| You are writing…                             | Use                        |
| -------------------------------------------- | -------------------------- |
| The outcome of a completed step              | `.win` callout             |
| Reasoning, context, a cross-reference        | `.why` callout             |
| A prerequisite, trap, or irreversible action | `.warn` callout            |
| Numbered steps with substance under each     | `.step-h` with `.n`        |
| Numbered steps of one or two sentences       | `ol.steps`                 |
| 2–6 sibling concepts of equal weight         | `.cards`                   |
| Two options being weighed against each other | `.choice` with `.a`/`.b`   |
| An anticipated question                      | `.qa` with `.q`            |
| A handoff between actors or stages           | `.flow`                    |
| Structured comparison across attributes      | `.tablewrap` + `table`     |
| At-a-glance facts about a section            | `.phase-meta` with `.chip` |

Callout labels should say something. `<span class="label">What you have now</span>`
earns its place; `<span class="label">Note</span>` does not.

### 5. Verify before you hand it over

Open the file and check it actually works — these are the failures that recur:

```bash
open <destination>.html   # macOS
```

- Toggle to dark mode and back. Every surface should change. Anything that stays
  stubbornly white or black is a hardcoded colour that should be a token.
- In tabbed mode, click through every sidebar tab and use the pager to the last
  section. A tab whose `href` doesn't match a section id silently falls back to
  showing section 0.
- Narrow the window below 900px. The sidebar should become a horizontal tab
  strip, not overflow the page.
- Confirm the file is self-contained: no local CSS or JS files, no build step.
  The single Google Fonts `<link>` (two families) is the only external
  dependency, and the font stacks degrade to the system monospace and sans if it
  fails to load.

Then tell the user the path and, in a sentence, which navigation mode you chose
and why.

## What makes documents in this system good

The visual system is only half of it. The reference document earns its clarity
from a few habits worth copying:

**State who each section is for and how long it takes.** The `.chip` row under a
heading answers "is this for me, right now?" before the reader invests in the
prose.

**Explain the why, not just the what.** The `.why` callout exists because
instructions that don't justify themselves get skipped or cargo-culted. When a
step is non-obvious, say what would go wrong without it.

**Write for the least technical person who will plausibly open the file.** The
reference guide is explicitly aimed at "technical and non-technical" readers, and
that constraint drives its plain-language phrasing, its expansion of jargon on
first use, and its preference for a `.flow` diagram over a paragraph describing
data movement.

**End sections with what the reader now has.** A `.win` callout closing a phase
turns a wall of instructions into a checkpoint.

**Let the tokens do the work.** Teal is the only accent; green, amber and the
muted greys are semantic, not decorative. A document that introduces a fourth
colour to be interesting stops being part of the set.

## Adapting the palette

If a document belongs to a different project and needs its own identity, change
only the `--accent` / `--accent-soft` pair in all three token blocks (`:root`,
`@media (prefers-color-scheme: dark)`, and `:root[data-theme="dark"]` /
`[data-theme="light"]`). Everything else — greys, callout colours, borders — is
tuned for contrast in both themes and should stay put. Pick a dark-mode accent
that is noticeably lighter than the light-mode one; the reference uses
`#0e6e68` against white and Catppuccin Frappé Teal `#81c8be` against `#303446`.

Changing tokens in only one of the three blocks is the most common way this
breaks: the OS-preference block and the manual-toggle block must agree, or the
document will look correct until someone presses the button.

## Files

- `assets/template.html` — the skeleton to copy. Full design system, theme
  toggle, both navigation modes, print styles.
- `references/components.md` — every component with markup and guidance on when
  to use it. Read this before writing content.
