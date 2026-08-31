# Component catalog

Every component in the design system, with copy-pasteable markup. All styling
already exists in `assets/template.html` — never add new CSS for these; just use
the class names.

## Contents

- [Design tokens](#design-tokens) — the colour and layout variables
- [Typography](#typography) — the two font families, the type scale, the measure
- [Page furniture](#page-furniture) — eyebrow, title, lede, meta-strip, footer
- [Sidebar and sections](#sidebar-and-sections) — nav, section shells, tags, chips
- [Callouts](#callouts) — win / why / warn
- [Steps and lists](#steps-and-lists) — step headers, ordered steps
- [Code](#code) — blocks, inline, copy button, and syntax highlighting
- [Tables](#tables)
- [Cards](#cards)
- [Choice boxes](#choice-boxes) — two-option comparison
- [Q&A blocks](#qa-blocks)
- [Flow diagram](#flow-diagram) — pipeline / handoff visual
- [Figures](#figures) — screenshots with captions
- [Sidenotes](#sidenotes) — margin notes beside the prose
- [What the page does on its own](#what-the-page-does-on-its-own) — generated
  sidebar, reading time, progress rail

---

## Design tokens

Every colour in the document resolves through these variables. Light mode is the
base; dark mode is Catppuccin Frappé; paper is a warm third theme. Using a raw
hex anywhere in the body means one of the three themes will break, so always
reach for a token.

| Token                         | Light                 | Dark (Frappé)                | Use for                                 |
| ----------------------------- | --------------------- | ---------------------------- | --------------------------------------- |
| `--bg`                        | `#f6f8f8`             | `#303446` Base               | page background                         |
| `--card`                      | `#ffffff`             | `#414559` Surface 0          | section shells, sidebar, buttons        |
| `--ink`                       | `#1c2529`             | `#c6d0f5` Text               | body text                               |
| `--muted`                     | `#56676d`             | `#a5adce` Subtext 0          | secondary text, labels, captions        |
| `--accent`                    | `#0e6e68` teal        | `#81c8be` Teal               | links, active tab, emphasis             |
| `--accent-soft`               | `#e2efed`             | `#51576d` Surface 1          | tag and hover backgrounds               |
| `--win-bg` / `--win-border`   | `#e8f3ea` / `#2e7d4f` | `#292c3c` / `#a6d189` Green  | outcome callouts                        |
| `--warn-bg` / `--warn-border` | `#faf3e0` / `#9a6a00` | `#292c3c` / `#e5c890` Yellow | caution callouts                        |
| `--why-bg`                    | `#edf2f4`             | `#292c3c` Mantle             | rationale callouts, cards, flow boxes   |
| `--border`                    | `#d8e0e0`             | `#51576d` Surface 1          | all hairlines                           |
| `--code-bg` / `--code-ink`    | `#eef2f2` / `#17332f` | `#292c3c` / `#99d1db` Sky    | code, chips, Q&A shells                 |
| `--tok-*` (nine)              | Catppuccin Latte      | Catppuccin Frappé            | syntax highlighting — see [Code](#code) |

### The three themes

The toggle cycles **light → paper → dark**, and the button always names the mode
you are about to switch _to_. Paper is warm, low-glare and meant for long
reading sessions: `--bg: #ece3d2`, `--card: #faf5ea`, `--ink: #332e26`, with the
greys warmed rather than replaced so every component stays tuned for contrast.
No OS setting asks for paper, so it is only ever reached through the toggle.

The palette is declared four times on purpose: once on bare `:root` (light),
once under `@media (prefers-color-scheme: dark)` so the OS preference works with
JS disabled, and once each under `:root[data-theme="dark"]`,
`:root[data-theme="light"]` and `:root[data-theme="paper"]` so the manual toggle
can override the OS in _every_ direction. Dropping the explicit `light` block
silently breaks "force light on a dark-mode machine".

### Layout tokens

| Token                             | Value                        | Controls                                          |
| --------------------------------- | ---------------------------- | ------------------------------------------------- |
| `--measure`                       | `43.5rem`                    | reference value only — nothing is capped by it     |
| `--card-pad`                      | `2.75rem`                    | horizontal padding inside `section.phase`          |
| `--sidenote-w` / `--sidenote-gap` | `0` → `14rem` / `1.75rem`    | the margin gutter; opens at 1440px, and only in documents that contain a sidenote |

No rule reads `--measure` for layout — it is kept on `:root` so a single
prose-heavy document can opt into a narrow column locally (see **Width** in
`SKILL.md`). If you ever do reach for it, keep it in `rem`, not `ch`: a custom
property in `ch` resolves against each element's own font size, so different
elements would compute different widths and stop lining up with each other.

The section's own width comes from `.content { flex: 1 }` against the 256px
sidebar, and `--card-pad` sets the padding inside it. Those two are the whole
horizontal layout.

## Typography

- **`"IBM Plex Mono", monospace`** (400/600/700 + italics) — the document itself:
  body copy, headings, callout labels, chips, buttons, table headers. Body is set
  at 17px / 1.65. IBM Plex Mono tops out at 700, so the handful of `800` rules in
  the CSS resolve to 700 — that is intentional, do not "fix" them.
- **`"Noto Sans Elbasan", sans-serif`** — the sidebar only: its heading label, the
  tab links, and the circled `.num` counters. A proportional face here separates
  navigation from content at a glance. It ships **regular weight only**, so the
  `600`/`700` rules inside `nav.sidebar` are synthesised by the browser. Because
  `.label` also matches the shared mono rule, `nav.sidebar .label` restates the
  family explicitly — inheriting from `nav.sidebar` alone would not win.
- **`ui-monospace, "SF Mono", "Cascadia Code", Menlo, Consolas, monospace`** — code.
  Kept distinct from the body font so code blocks still read as code.

Scale: `h1` 2.1rem · `h2` 1.45rem · `h3` 1.08rem · `h4` 0.98rem · body 17px ·
`.lede` 1.12rem · small UI 0.85rem · labels/tags 0.72rem uppercase with wide
tracking. `h1`/`h2` use `text-wrap: balance` and slight negative letter-spacing.

One `h1` per document, in `<main>` above the layout. `h2` is the section title
inside each `section.phase`. `h3`/`h4` subdivide within a section.

Nothing is width-capped. The page fills the window and every element — prose,
tables, `.flow`, `.cards`, `.choice`, code blocks and figures — runs the full
width of its section, so a paragraph and the table beneath it share an edge.
`--measure` is retained on `:root` as a reference value; no layout rule reads
it. See **Width** in `SKILL.md` for the two capping strategies that were tried
and why both were removed.

## Page furniture

```html
<p class="eyebrow">OPTIONAL KICKER</p>
<h1>Document title</h1>
<p class="lede">One or two sentences: what this is and who it is for.</p>

<div class="meta-strip">
  <span><strong>Audience</strong> — technical &amp; non-technical</span>
  <span><strong>Time</strong> — ~1 working day</span>
  <span
    ><strong>Repo</strong> — <a href="https://example.com">org/repo</a></span
  >
</div>
```

The meta-strip is a horizontal rule-bounded band of 2–5 framing facts. Each
`<span>` is `<strong>Label</strong> — value`. It wraps on narrow screens.

Footer sits at the end of `.content`, inside the layout:

```html
<footer>
  <p>
    <strong>Reusing this document:</strong> what a future reader should know.
  </p>
  <p>Related: <a href="...">link</a> · <a href="...">link</a>.</p>
</footer>
```

## Sidebar and sections

Navigation mode is set once, on the `<html>` element at the top of the file
(`<html lang="en" data-nav="tabbed">`), not here.

```html
<div class="layout">
  <nav class="sidebar" aria-label="Sections">
    <div class="sidebar-head">
      <span class="label">The journey</span>
      <button
        class="sidebar-toggle"
        id="sidebarToggle"
        type="button"
        aria-expanded="true"
        aria-label="Minimize sidebar"
        title="Minimize sidebar"
      >
        «
      </button>
    </div>
    <!-- No links here. They are generated at load. -->
  </nav>
  <div class="content">
    <section class="phase" id="phase1">…</section>
    <div class="pager">
      <button id="pagerPrev" type="button"></button>
      <button id="pagerNext" type="button"></button>
    </div>
    <footer>…</footer>
  </div>
</div>
```

**Do not hand-write the `a.tab` links.** They are generated at load from every
`section.phase` that has an `id`, in document order, using its `<h2>` as the
label. The section ids are the single source of truth, which is what makes an
href pointing at nothing impossible to write. A section without an `id` is
skipped rather than becoming a dead link.

Two attributes on `section.phase` steer the generated tab:

| Attribute        | Use it when                                                                 |
| ---------------- | --------------------------------------------------------------------------- |
| `data-nav-label` | the `h2` is too long for the sidebar — keep labels under about 60 characters |
| `data-nav-num`   | the counter should not simply be the section's position                     |

`data-nav-num` renumbers everything after it too, so `data-nav-num="0"` on a
"read this first" preface leaves the first real step at 1 rather than pushing it
to 2.

- The label text also becomes the `title` tooltip and the pager button text.
- The collapse button and its `id="sidebarToggle"` are required by the script.
  Its state persists in `localStorage`.
- Below 900px the sidebar becomes a horizontal scrolling tab strip automatically.
- With JavaScript off there are no links to show, so the sidebar hides itself
  (`html:not(.js) nav.sidebar`) and the document reads as a plain scrolling page.

Section shell:

```html
<section class="phase" id="phase1">
  <span class="phase-tag">Phase 1 · Foundation</span>
  <h2>Create the GitHub repository</h2>
  <div class="phase-meta">
    <span class="chip">Who — <strong>one technical person</strong></span>
    <span class="chip">Time — <strong>15 minutes</strong></span>
  </div>
  <p>Body copy.</p>
</section>
```

`.phase-tag` is the small uppercase pill above the heading — use it to name the
part/phase. `.phase-meta` holds `.chip`s: 2–4 at-a-glance facts scoped to this
section (who, how long, what you need first). `<strong>` inside a chip renders in
the accent colour.

A `Read — N min` chip is appended to every section automatically, so write only
the chips that you know and the page cannot work out: who it is for, what they
need first, who owns it. The estimate counts prose at 200 words per minute and
ignores `<pre>` blocks — code is scanned rather than read, and counting it would
inflate every technical section past the point where the number means anything.
Writing your own `Read — …` chip suppresses the estimate; `data-readtime="off"`
on `<html>` suppresses it document-wide.

## Callouts

Three flavours, distinguished by meaning rather than decoration. Each carries a
`<span class="label">` that names the callout in its own words — the label is not
boilerplate like "Note", it should say what the reader is about to get.

```html
<div class="win">
  <span class="label">What you have now</span>
  <p>The concrete outcome the reader just achieved.</p>
</div>

<div class="why">
  <span class="label">Why this matters</span>
  <p>Rationale, background, or a pointer to related reading.</p>
</div>

<div class="warn">
  <span class="label">Don't skip this</span>
  <p>A trap, prerequisite, or irreversible action.</p>
</div>
```

- `.win` — green left border. Milestones, outcomes, "you're done with X".
- `.why` — accent left border. Reasoning, context, cross-references. This is the
  workhorse; it carries the explanatory voice that makes the document teach
  rather than merely instruct.
- `.warn` — amber left border. Cautions and prerequisites.

Callouts may contain lists; the last child's bottom margin is already collapsed.

## Steps and lists

Numbered work inside a section uses `.step-h`, which draws a dashed rule above
and a filled accent circle:

```html
<div class="step-h"><span class="n">1</span>Create the repository</div>
<p>What to do.</p>

<div class="step-h"><span class="n">2</span>Add the constitution file</div>
```

For a compact ordered list with breathing room between items:

```html
<ol class="steps">
  <li><strong>Lead-in phrase</strong> — the explanation that follows.</li>
  <li><strong>Next item</strong> — and so on.</li>
</ol>
```

Prefer `.step-h` when each step needs paragraphs, code, or callouts under it, and
`ol.steps` when each step is one self-contained sentence or two.

## Code

```html
<pre>
git clone https://github.com/org/repo.git
cd repo</pre>

<p>Set the key in <code>.env</code>, then run <code>npm start</code>.</p>
```

Blocks scroll horizontally rather than wrapping. Inline `<code>` inside `p`, `li`
and `td` gets a bordered chip treatment automatically.

### Copy button

Every `<pre>` gets one, automatically. A script at the bottom of the template
wraps each block in `div.codewrap` and appends `button.copy-btn` — **do not write
that markup yourself**. A block already sitting inside a `.codewrap` is skipped,
so hand-wrapping one is the way to end up with no button at all. Write a plain
`<pre>` and the button appears.

The button sits in the top-right corner of the block, fades in on hover (it is
always visible on touch devices, which never hover), and flips to `Copied` for a
moment after a successful copy. It is hidden when printing, and with JavaScript
disabled neither the wrapper nor the button exists at all.

What gets copied is the block's text, not its highlighted markup, with the
newline after the opening tag and any trailing whitespace trimmed — so the
clipboard matches what is on screen. That means the block should contain only
what you want pasted: keep prompts (`$`, `>`) and command output in a separate
block from the commands themselves, or the reader pastes them too.

### Syntax highlighting

Add a `language-*` class and the block is coloured by the highlighter at the
bottom of the template — a self-contained tokenizer, no library and no network
request:

```html
<pre class="language-python">
def total(rows):
    # sum the amounts
    return sum(r["amount"] for r in rows)</pre>
```

The class goes on the `<pre>`, or on a `<code>` inside it if you prefer the
CommonMark shape (`<pre><code class="language-ts">`). It works on inline `<code>`
too, though a whole highlighted phrase mid-sentence is usually noisier than plain
`<code>`.

Recognised names, with the obvious aliases (`js`, `ts`, `py`, `sh`, `yml`, `c`,
`cs`, `rb`, `rs`, `kt`, `htm`, `jsx`, `tsx`, `scss`, …):

`python` · `javascript` · `typescript` · `java` · `kotlin` · `go` · `rust` ·
`cpp` · `csharp` · `php` · `ruby` · `swift` · `sql` · `bash` · `json` · `yaml` ·
`html` / `xml` · `css` · `abap`

**Leave the class off when the block is not source code.** Terminal output, file
trees, log excerpts and ASCII diagrams stay monochrome, which is exactly right —
colouring them invents meaning that isn't there. `language-text` (or `console`,
`log`, `diff`) is the explicit way to say "code font, no colour".

An unknown language name is ignored rather than guessed at, so the block simply
renders plain. To add a language, add one `def()` entry in the highlighter; to
switch highlighting off entirely, delete that whole IIFE and every block falls
back to plain `<pre>`.

Tokens are painted through nine variables — `--tok-plain`, `--tok-com`,
`--tok-str`, `--tok-kw`, `--tok-num`, `--tok-fn`, `--tok-typ`, `--tok-op`,
`--tok-var` — Catppuccin Latte in light mode and Frappé in dark, so a block
recolours with the theme toggle like everything else. They sit alongside the
other tokens in every theme block, and the same "change one, change all" rule
applies.

`.skill-invoke` is a variant of inline code for things the reader types to invoke
an agent or command — it renders in the accent colour on the soft accent
background, so slash-commands stand out from ordinary file paths:

```html
<p>Type <code class="skill-invoke">/abap-wiki</code> to query the vault.</p>
```

## Tables

Always wrap so narrow screens scroll the table instead of the page:

```html
<div class="tablewrap">
  <table>
    <thead>
      <tr>
        <th>Setting</th>
        <th>Value</th>
        <th>Why</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Visibility</td>
        <td>Private</td>
        <td>Contains internal knowledge.</td>
      </tr>
    </tbody>
  </table>
</div>
```

The first column renders semibold and non-wrapping (it wraps again below 640px),
so put the short key there and the prose in later columns.

## Cards

A responsive grid that reflows from multi-column to single column on its own.
Use for 2–6 sibling concepts of roughly equal weight.

```html
<div class="cards">
  <div class="card">
    <span class="card-title">Standards</span>
    Conventions the team agreed to follow.
  </div>
  <div class="card">
    <span class="card-title">Decisions</span>
    What was chosen, when, and why.
  </div>
</div>
```

## Choice boxes

A deliberate two-option comparison. `.a` gets an accent top rule (the
recommended path), `.b` gets an amber one (the alternative or the trade-off).

```html
<div class="choice">
  <div class="choice-box a">
    <span class="ct">Option A — GitHub-hosted</span>
    Everything stays in one repository. Simple to back up.
  </div>
  <div class="choice-box b">
    <span class="ct">Option B — SharePoint</span>
    Familiar to the business, but no version history for edits.
  </div>
</div>
```

## Q&A blocks

For anticipated questions, FAQ sections, and "under the hood" appendices. The
`Q — ` prefix is generated by CSS, so write only the question text.

```html
<div class="qa">
  <p class="q">Why Markdown instead of a database?</p>
  <p>Because plain text survives tool changes and diffs cleanly in git.</p>
</div>
```

## Flow diagram

A CSS-only pipeline visual — no images, no libraries — for showing a handoff
between actors or stages. Columns are `.flow-col`; add `.flow-main` to the column
that deserves extra width. Arrows are `.flow-arrow` with `.a1` (`→`, one-way) or
`.a2` (`⇄`, two-way); both rotate to vertical arrows below 760px, and the whole
row stacks.

```html
<div class="flow">
  <div class="flow-col">
    <div class="flow-role">Contributor</div>
    <div class="flow-box">
      <strong>OneDrive Inbox</strong>
      <span>A teammate drops in any document.</span>
    </div>
  </div>
  <div class="flow-arrow a1"><span class="lbl">triggers</span></div>
  <div class="flow-col flow-main">
    <div class="flow-role">Automation</div>
    <div class="flow-box">
      <strong>Claude</strong>
      <ol>
        <li>Reads the document.</li>
        <li>Extracts durable knowledge.</li>
        <li>Updates the right pages.</li>
      </ol>
    </div>
  </div>
  <div class="flow-arrow a2"><span class="lbl">reads &amp; writes</span></div>
  <div class="flow-col">
    <div class="flow-role">Reader</div>
    <div class="flow-box">
      <strong>Obsidian</strong>
      <span>Humans browse the linked vault.</span>
    </div>
  </div>
</div>
```

`.flow-role` is the uppercase actor label above each column. Inside `.flow-box`,
`<strong>` is the accent-coloured box title, `<span>` is muted supporting text,
and `<ol>` renders as a compact muted step list.

## Figures

```html
<figure class="shot">
  <img src="images/screenshot.png" alt="Describe what the screenshot shows" />
  <figcaption>What the reader should notice in this screenshot.</figcaption>
</figure>
```

Images stretch to the content width with a border, rounded corners and a soft
shadow. Always write a real `alt` — the caption and the alt text serve different
readers and should not be identical.

## Sidenotes

```html
<aside class="sidenote">
  <span class="label">Aside</span>
  Provenance, a caveat, a pointer — something the reader can take or leave.
</aside>
<p>The paragraph the note sits beside.</p>
```

Place the `<aside>` immediately **before** the paragraph it belongs to; it floats
into the margin starting at that paragraph's first line. The `.label` is
optional and, like every other label in the system, should say something.

Above 1440px, in a document that contains at least one sidenote, the note sits
in a 14rem gutter that `section.phase` reserves in its right padding, so it
never pushes the prose around or interrupts the line of the argument. Below that
width — or in a document with no sidenotes, where the `:root:has(.sidenote)`
guard never opens the gutter — the same markup renders as an ordinary tinted
block in the flow of the section. No author decision, no second component.

Within a document that uses sidenotes the gutter is reserved in every section,
whether or not that section holds a note — the prose column then starts and ends
at the same place throughout, instead of shifting whenever a note appears. A
document with no sidenotes at all opens no gutter, so a table-dense page does
not pay 14rem of right padding for a feature it never uses.

**Count them first.** The gutter is a document-level switch, not a per-section
one: the first `aside.sidenote` anywhere makes every section reserve the 14rem,
so one aside costs the entire page about 224px of usable width. With fewer than
about three, or in a document dense with tables and code that want the room,
use a `.why` callout and let the sections run full width.

**What belongs in a sidenote:** the aside you would otherwise put in parentheses
and then delete for breaking the sentence. **What does not:** anything the reader
must not miss. A sidenote is skippable by construction — a prerequisite, a trap
or an irreversible action belongs in a `.warn` callout, where it is not.

## What the page does on its own

Three things are handled by the template's script, so they are not markup you
write — but they do change how you write.

**The sidebar is generated** from the section ids. See
[Sidebar and sections](#sidebar-and-sections).

**Reading time** is measured per section and appended to `.phase-meta`. The
consequence for writing: a section that estimates at 12 minutes is telling you it
should probably be two sections.

**A progress rail** sits at the top of the viewport in `--accent`. In scroll mode
it tracks scroll depth; in tabbed mode it tracks position through the section
sequence, because there only one section is on screen and scroll depth would say
nothing about progress through the document. It is hidden in print.
