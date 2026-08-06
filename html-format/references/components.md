# Component catalog

Every component in the design system, with copy-pasteable markup. All styling
already exists in `assets/template.html` — never add new CSS for these; just use
the class names.

## Contents

- [Design tokens](#design-tokens) — the colour variables and what each means
- [Typography](#typography) — the two font families and the type scale
- [Page furniture](#page-furniture) — eyebrow, title, lede, meta-strip, footer
- [Sidebar and sections](#sidebar-and-sections) — nav, section shells, tags, chips
- [Callouts](#callouts) — win / why / warn
- [Steps and lists](#steps-and-lists) — step headers, ordered steps
- [Code](#code) — blocks and inline
- [Tables](#tables)
- [Cards](#cards)
- [Choice boxes](#choice-boxes) — two-option comparison
- [Q&A blocks](#qa-blocks)
- [Flow diagram](#flow-diagram) — pipeline / handoff visual
- [Figures](#figures) — screenshots with captions

---

## Design tokens

Every colour in the document resolves through these variables. Light mode is the
base; dark mode is Catppuccin Frappé. Using a raw hex anywhere in the body means
one of the two themes will break, so always reach for a token.

| Token                         | Light                 | Dark (Frappé)                | Use for                               |
| ----------------------------- | --------------------- | ---------------------------- | ------------------------------------- |
| `--bg`                        | `#f6f8f8`             | `#303446` Base               | page background                       |
| `--card`                      | `#ffffff`             | `#414559` Surface 0          | section shells, sidebar, buttons      |
| `--ink`                       | `#1c2529`             | `#c6d0f5` Text               | body text                             |
| `--muted`                     | `#56676d`             | `#a5adce` Subtext 0          | secondary text, labels, captions      |
| `--accent`                    | `#0e6e68` teal        | `#81c8be` Teal               | links, active tab, emphasis           |
| `--accent-soft`               | `#e2efed`             | `#51576d` Surface 1          | tag and hover backgrounds             |
| `--win-bg` / `--win-border`   | `#e8f3ea` / `#2e7d4f` | `#292c3c` / `#a6d189` Green  | outcome callouts                      |
| `--warn-bg` / `--warn-border` | `#faf3e0` / `#9a6a00` | `#292c3c` / `#e5c890` Yellow | caution callouts                      |
| `--why-bg`                    | `#edf2f4`             | `#292c3c` Mantle             | rationale callouts, cards, flow boxes |
| `--border`                    | `#d8e0e0`             | `#51576d` Surface 1          | all hairlines                         |
| `--code-bg` / `--code-ink`    | `#eef2f2` / `#17332f` | `#292c3c` / `#99d1db` Sky    | code, chips, Q&A shells               |

Dark mode is declared three times on purpose: once under
`@media (prefers-color-scheme: dark)` so the OS preference works with JS
disabled, and once each under `:root[data-theme="dark"]` and
`:root[data-theme="light"]` so the manual toggle can override the OS in _both_
directions. Dropping the explicit `light` block silently breaks "force light on a
dark-mode machine".

## Typography

- **`"IBM Plex Mono", monospace`** (400/600/700 + italics) — everything: body copy,
  headings, sidebar, labels, chips, buttons, table headers. Body is set at
  17px / 1.65. IBM Plex Mono tops out at 700, so the handful of `800` rules in the
  CSS resolve to 700 — that is intentional, do not "fix" them.
- **`ui-monospace, "SF Mono", "Cascadia Code", Menlo, Consolas, monospace`** — code.
  Kept distinct from the body font so code blocks still read as code.

Scale: `h1` 2.1rem · `h2` 1.45rem · `h3` 1.08rem · `h4` 0.98rem · body 17px ·
`.lede` 1.12rem · small UI 0.85rem · labels/tags 0.72rem uppercase with wide
tracking. `h1`/`h2` use `text-wrap: balance` and slight negative letter-spacing.

One `h1` per document, in `<main>` above the layout. `h2` is the section title
inside each `section.phase`. `h3`/`h4` subdivide within a section.

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
    <a class="tab" href="#phase1"
      ><span class="num">1</span>Create the repository</a
    >
    <a class="tab" href="#phase2"
      ><span class="num">2</span>Design the structure</a
    >
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

- Every `a.tab` `href` must match a `section.phase` `id`, in the same order.
- `.num` is the circled counter. Start at `0` when there is an orientation
  section that precedes step 1, exactly like a "read this first" preface.
- Sidebar labels should be short; the full text becomes the `title` tooltip and
  the pager button text, so keep them under about 60 characters.
- The collapse button and its `id="sidebarToggle"` are required by the script.
  Its state persists in `localStorage`.
- Below 900px the sidebar becomes a horizontal scrolling tab strip automatically.

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
