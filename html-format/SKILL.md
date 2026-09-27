---
name: html-format
description: Produces a standalone, self-contained HTML document in the house design system — teal accent, IBM Plex Mono typography with a proportional sidebar, a full-width layout with margin sidenotes, generated sidebar navigation, card sections, callouts, per-section reading time, a reading-progress rail, and a light/paper/dark toggle. Use this whenever the deliverable is an HTML page rather than Markdown: guides, walkthroughs, runbooks, proposals, explainers, onboarding docs, reports, FAQs, or specs. Trigger it when someone asks for a document "as HTML", "as a web page", "in the same style/format as index.html", "in our house style", "matching the other pages", or asks to convert an existing Markdown/text document into a styled HTML page. Also use it when adding a new companion page to a documentation set that already uses this system, so the new page matches the rest.
---

# House HTML document format

This skill produces one file: a self-contained HTML document built from
`assets/template.html` — a teal-accented, card-based reading experience with a
sidebar, semantic callouts, margin sidenotes, and a light/paper/dark toggle that
respects the OS but can be overridden. When someone asks for a page "like
index.html" they mean an existing page in their own documentation set; open it
and match it (see step 1).

The layout fills the window. Nothing is width-capped: prose, tables, cards,
flow diagrams, figures and code blocks all run the full width of their section,
so a paragraph and the table under it share an edge. In documents that use
sidenotes, a gutter opens on the right to hold them. A progress rail is added by
the template's own script.

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

Fill in `<title>` and `<meta name="description">` straight away — the
description is the one sentence shown under the link when the page is shared.

If the document is joining an existing set of pages, open a sibling page first
and match its conventions (storage keys, footer style, relative link paths).
Link siblings with relative paths (`setup.html`): the template opens only
off-site links in a new tab, so a reader walking through the set stays in one
tab.

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
In tabbed mode, Ctrl-F still finds text in hidden sections — they carry
`hidden="until-found"`, and a match switches to that tab — so choosing tabbed no
longer costs a reference reader their search (in browsers without support, find
sees only the open section).
That is why the CSS keys off a `.js-tabbed` class the head script adds rather
than off `data-nav` directly — leave that arrangement alone.

If the document has no sections at all — a single short note — delete the whole
`.layout` wrapper and put the content directly in `<main>` after the lede. The
card styling of `section.phase` still works standalone.

### 4. Write the content

Section titles are `h2` inside `section.phase`; the document has exactly one
`h1`, above the layout. **Give every section an `id`** — that is the only thing
the navigation needs. The sidebar links are generated at load from the sections
themselves, so there is no list of hrefs to keep in sync and no way to point a
tab at an id that does not exist. Put `data-nav-label` on a section when its
`h2` is too long for the sidebar, and `data-nav-num` when the counter should not
be the section's position (`0` on a "read this first" preface renumbers what
follows, so step 1 stays 1).

`.phase-meta` chips carry facts the reader cannot get by looking at the section:
who it is for, what they need in hand first, who owns it, what order things run
in. **Never write `Time — …`, `Writes — …` or `Read — …` chips.** A duration is a
guess about someone else's machine, an output path is already in the command
directly below the chip, and both go stale the moment the content changes — a
wrong number at the top of a section costs more trust than the chip ever bought.
A section with nothing else to say should carry no `.phase-meta` at all.

The automatic reading-time estimate is off unless `<html>` carries
`data-readtime="on"`. Leave it off for anything instructional; turn it on only
for a long prose document that is genuinely read start to finish.

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
| Who a section is for, or what it needs first | `.phase-meta` with `.chip` |
| Source code in a known language              | `pre.language-*`           |
| Terminal output, a file tree, a log excerpt  | plain `pre`                |
| An aside the reader can safely skip          | `aside.sidenote` (see cost) |
| A long block worth collapsing by default     | `details.disclose`         |
| Output the reader must paste back to you     | `.capture`                 |

Code blocks are syntax-highlighted when you tag them with a language:
`<pre class="language-python">`, `language-typescript`, `language-bash`,
`language-sql`, `language-abap` and a dozen more (see the catalog for the list
and the aliases). The highlighter is built into the template — no library, no
network call — so this is a one-attribute decision, not a dependency.

Tag the language whenever the block really is source code; a Python function
that reads as plain grey text is a missed chance to make it scannable. Leave the
class off when the block is _not_ code — command output, directory listings, log
lines, ASCII diagrams. Colouring those invents structure that isn't in them, and
a monochrome block is the visual cue that the reader is looking at output rather
than something to type.

Every `<pre>` also gets a copy button, added by a script in the template — you
write a plain block and the button appears on hover. The consequence for writing:
a block is now something a reader will paste whole, so keep commands and their
output in separate blocks rather than pasting a `$` prompt and a wall of output
into someone's terminal.

Sidenotes go in the margin gutter, immediately before the paragraph they belong
to. Reach for one when you would otherwise write a parenthesis and then delete
it for breaking the sentence — provenance, a caveat, a pointer. The test is
whether a reader who skips it still gets everything they need: a sidenote is
skippable by construction, so a prerequisite or an irreversible action belongs
in a `.warn` callout instead, where it is not.

**Sidenotes are all-or-nothing, so count them before you use one.** The gutter
opens per _document_, not per section: one `aside.sidenote` anywhere makes every
section reserve 14rem of right padding, whether or not it holds a note. That is
deliberate — it stops the prose column shifting each time a note appears — but it
means a single aside costs the whole document about 224px of width. Below roughly
three sidenotes, or in a document dense with tables, code blocks and flow
diagrams that want the room, put the aside in a `.why` callout instead and let
every section run full width. The empty right margin this otherwise produces
reads as a layout bug, and it is the most common reason a finished page looks
like it is ignoring the window.

Callout labels should say something. `<span class="label">What you have now</span>`
earns its place; `<span class="label">Note</span>` does not.

Every section `h2` and every `h3` gets a `#` link on hover, and an `h3` without
an `id` is given one from its text. That makes each subsection linkable — so
write `h3`s that make sense out of context, and give one an explicit `id` when
other pages will link to it (a generated id changes when the heading text
does).

### 5. Verify before you hand it over

Run the checker first. It catches most of what follows without a browser:
scaffold text left in, sections without ids, `Time —` chips, empty chip rows,
a lone sidenote, unknown `language-*` names, hand-written `.codewrap` or
`a.tab` markup, duplicate capture keys or a missing `data-capture-store`,
`style=` attributes and extra `<style>` blocks, external scripts, and theme
blocks that have drifted apart.

```bash
python3 ~/.claude/skills/html-format/scripts/check.py <destination>.html
```

Fix every `ERROR` (the exit status is 1 while any remain). `WARN` lines are
judgement calls — a sidenote count, a tabbed document with only three sections —
so read each and either fix it or be able to say why not.

Then open the file for what only a browser shows:

```bash
open <destination>.html   # macOS
```

- Press the theme button three times: light → paper → dark → light. Every
  surface should change at each step. Anything that stays stubbornly white or
  black is a hardcoded colour that should be a token.
- In dark mode, open print preview. The page should come out dark ink on white
  — the print block resets the palette to light.
- Check the sidebar lists every section, in order, with the labels you expect.
- In tabbed mode, click through every sidebar tab and use the pager to the last
  section. Watch the progress rail at the top of the window advance as you go.
- If the document uses sidenotes, widen the window past 1440px and confirm each
  one sits in the right margin beside its paragraph; narrow it again and confirm
  the same note folds into the section as a tinted block. A document with no
  sidenotes should show no right-hand gutter at any width — if it does, the
  `:has()` guard on the gutter has been dropped.
- Count the sidenotes. If there are only one or two, look at the page above
  1440px and decide whether the gutter is earning its keep: every section is
  paying for it, including the table-heavy ones. One stray note left over from
  the template scaffold is the usual culprit — convert it to a `.why` callout and
  the whole document reclaims the width.
- Narrow the window below 900px. The sidebar should become a horizontal tab
  strip, not overflow the page.
- Hover a code block and press its copy button. It should say `Copied` and the
  clipboard should hold the block's text with no highlighting artefacts. A block
  with no button was wrapped in `.codewrap` by hand — the script skips those, so
  delete the hand-written wrapper and let it do the work.
- If the document uses `.capture` blocks, type into one, press Save, reload the
  page and confirm the text came back.
- The single Google Fonts `<link>` (two families) is the only external
  dependency, and the font stacks degrade to the system monospace and sans if it
  fails to load.

Then tell the user the path and, in a sentence, which navigation mode you chose
and why.

## What makes documents in this system good

The visual system is only half of it. The reference document earns its clarity
from a few habits worth copying:

**State who each section is for and what it assumes.** The `.chip` row under a
heading answers "is this for me, right now?" before the reader invests in the
prose. Keep it to things only the author knows — not timings or file paths the
section already shows.

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

**No coloured leading edges.** A box with a background — a callout, a card, a
folded sidenote — is identified by its tint and its coloured label. Never give it
a coloured bar down its left side (`border-left`, or an inset shadow standing in
for one): repeated on every box it becomes decoration, and it pulls the eye to
the edge rather than the content. `check.py` fails a page that has one.

## Converting Markdown

When the source is a Markdown or text document, translate its constructs into
the components rather than transcribing them — a converted page that is all
`<p>` and `<ul>` has lost what the system is for.

| Markdown                                        | Becomes                                              |
| ----------------------------------------------- | ---------------------------------------------------- |
| `# Title` and the paragraph under it            | `h1` and `.lede`                                     |
| `## Heading`                                    | a `section.phase` with an `id` and that `h2`         |
| `### Heading`                                   | `h3` inside the section                              |
| `> **Note:**`, `> **Why:**`, background prose   | `.why` with a label that says what it is             |
| `> **Warning:**`, `> **Important:**`, prereqs   | `.warn`                                              |
| "You should now have…", "Done when…"            | `.win` closing the section                           |
| `1.` list whose items carry code or paragraphs  | `.step-h` headers                                    |
| `1.` list of one-liners                         | `ol.steps`                                           |
| `- [ ]` task list                               | `ol.steps`, or `.step-h` if the items have substance |
| ` ```lang ` fence                               | `<pre class="language-lang">`, or plain `<pre>` for output |
| pipe table                                      | `.tablewrap` + `table`, short key in column 1        |
| `**Q:** …` / FAQ headings                       | `.qa` with `.q`                                      |
| "Option A vs option B" subsections              | `.choice`                                            |
| `<details>`                                     | `details.disclose` with `.disclose-body`             |
| Front matter (author, audience, status)         | `.meta-strip`, dropping any duration                 |
| Footnotes                                       | sidenotes if there are three or more, else `.why`    |
| `![alt](src)` with a caption line               | `figure.shot` with a distinct `alt` and `figcaption` |

Escape `<`, `>` and `&` inside code blocks — a fenced `<div>` pasted raw into a
`<pre>` becomes a real element. Keep the Markdown's section order and wording
unless asked to edit; the job is structure, not a rewrite.

## Adapting the palette

If a document belongs to a different project and needs its own identity, change
only the `--accent` / `--accent-soft` pair in **all six** token blocks:
`:root`, `@media (prefers-color-scheme: dark)`, `:root[data-theme="dark"]`,
`:root[data-theme="light"]`, `:root[data-theme="paper"]`, and the `@media print`
block (which repeats the light palette so every theme prints dark-on-white).
`check.py` reports any pair of blocks that should match and does not. Everything else —
greys, callout colours, borders — is tuned for contrast in all three themes and
should stay put. Pick a dark-mode accent that is noticeably lighter than the
light-mode one; the reference uses `#0e6e68` against white, `#0c635d` against
warm paper, and Catppuccin Frappé Teal `#81c8be` against `#303446`.

Changing tokens in only some of the blocks is the most common way this breaks:
the OS-preference block and the manual-toggle blocks must agree, or the document
will look correct until someone presses the button — or prints it.

## Width

Nothing in this system is width-capped. The page fills the window; every element
runs the full width of its section. `--measure` remains defined on `:root` as a
reference value, but no rule reads it for layout.

Two capping strategies have been tried and both were wrong, so do not
reintroduce either:

- **A cap on the container** (`.content`, `.layout`, `main`) crushes wide
  content, because a table cannot be wider than the box it sits in — and it
  strands the sidebar collapse button, which frees ~216px that a capped
  `.content` is not allowed to use.
- **A cap on the prose elements only** leaves paragraphs stranded at 696px
  beside tables running 1400px+, which reads worse than either extreme.

If one document is nearly all prose and genuinely wants a narrow column, add
`max-width: var(--measure); margin-inline: auto;` to `.content` in **that file
only**. Do not put it back in the template — the rest of the set is full-width
and a new page that is not will look out of place.

## Files

- `assets/template.html` — the skeleton to copy. Full design system, theme
  toggle, both navigation modes, print styles.
- `references/components.md` — every component with markup and guidance on when
  to use it. Read this before writing content.
- `scripts/check.py` — lints a finished page (stdlib Python, no install). Run it
  before handing a page over.
