# Analysis guide

How to turn an extract into understanding. Work through it before writing a word of the page.

## Where the meaning hides, by format

Read the extract's capitalised flags with these in mind. Each one has carried the real story in
some file.

| Format | Look hard at | Why it matters |
|---|---|---|
| Spreadsheet | Cell comments | Often the only guidance: definitions, examples, author doubts ("to be clarified"). |
| | Hidden columns, rows and sheets | Scoring weights, lookup tables, old versions, workings the author didn't want filled in. |
| | Formulas and `-> computed:` values | The logic that turns answers into a result (a score, a status), and what the result is right now. |
| | Drop-down lists | The allowed answers define the question. A missing option ("Unsure") is a design choice worth noting. |
| | Colour rules | Which answers the author considered good, bad or alarming. |
| | Pre-filled vs `-Select-`/blank | Tells you how far the previous person got. |
| | Defined names, external links, `#REF!` | Dependencies on other files; broken references. |
| Word | Comments and tracked changes | Disagreements and decisions in progress. Deleted text shows what was rejected. |
| | Hidden text, headers and footers | Drafting notes, classification marks, version and owner. |
| | Form fields and content controls | The document is a form: its options define the answers. |
| | `[Insert ...]`, highlights, empty table cells | An unfinished template. |
| PowerPoint | Speaker notes | Often the real argument; slides are just headlines. |
| | Hidden slides | Dropped options, backup data, things not to be shown. |
| | Section names | The deck's intended structure. |
| | Pictures with no alt text | Content you can't read: say so rather than guess. |
| PDF | Annotations, form fields, bookmarks | Reviewer remarks; the form's answers; the author's own outline. |
| | Image-only pages | Unread content: OCR it or report the gap. |
| Markdown / text | Front matter, HTML comments, links | Owner and status; hidden remarks; what it depends on. |
| Code | Imports, public classes and methods, constants | What it depends on, what it offers, hard-coded values and secrets. |
| | TODO/FIXME, commented-out blocks | Known debt and abandoned approaches. |
| | I/O: HTTP, SQL, files, env/config | What it touches in the outside world, including personal data. |
| Any | Metadata dates and authors | A creation date years before the subject proves a reused template. A different author from the sender is a lead. |

## Stated vs inferred

Keep two columns as you read. **Stated**: in a cell, paragraph, slide, comment, formula,
option list or metadata, and citable by locator. **Inferred**: your reading of what it means,
why it exists, who it's for, or what's missing. On the page, stated material is presented
plainly. Inferred material goes in a `.why` callout labelled *Interpretation* or in the
right-hand column of the overview's stated/interpretation table, or is worded with a hedge
("probably", "suggests"). Never upgrade an inference to a fact because it is likely.

## Per-unit notes

For each UNITS entry, write down:

- **Name and position** as the file shows them, and its primary purpose in one sentence.
- **Type of information**: free text, scored questions, a checklist, a data table, a narrative,
  code, a register.
- **Its parts**: each question or field, what it really asks (drawing on any comment or note),
  the allowed answers, and any term that needs defining.
- **Practical meaning**: what someone must do or know to answer it, and why the document wants
  it (a law, a policy, a decision it feeds).
- **Current state**: what's filled in (quote it), what's blank, and what's a default that may
  not have been chosen deliberately.
- **Links**: which other units it feeds, repeats, depends on, or contradicts.
- **Running example**: how the example plays out here, if it adds understanding.

## Cross-checks that find real problems

- The same fact answered in two places: do they agree?
- A status or conclusion ("mitigated", "approved", "low risk", "done") with no evidence behind
  it elsewhere.
- An answer that doesn't fit its question ("N/A" to a "how will you..." question).
- A computed result that depends on defaults, or that can't express uncertainty.
- Names that don't match each other: the file name vs the organisation in the text, the author
  vs the owner.
- Numbering gaps or duplicates, references to sections, appendices or links that don't exist,
  `#REF!`.
- Placeholders and LOOSE ENDS: who is meant to resolve them?
- Typos that change meaning or look official.
- Things outdated by date: laws, versions, "being developed" a long time ago.

## What's missing

Ask what a competent reviewer of *this kind* of document would expect: a sign-off, an owner, a
date, a version, a decision record, a risk rating, a data flow, test coverage, error handling.
List what's absent, and say plainly that you're judging against general practice, not against
anything the file states.

## Choosing the running example

Choose one small, concrete, realistic case that fits what's already filled in, if anything is.
The best is a **minimal pair**: two versions one detail apart that the document handles very
differently (a plain staff directory vs the same directory with live GPS tracking). Introduce it
in the overview, use it in the units where it clarifies, and close on it. Label it as
hypothetical. Never present it as what the real project is.
