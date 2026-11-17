---
name: whiteboard-diagram
description: Draw a clean, hand-drawn-style whiteboard image (PNG) that explains concepts visually, such as a cover image or explainer figure for a blog post, doc or slide. It has a whiteboard on a stand, marker-pen headings, panels separated by hand-drawn dividers, boxes, tables, circles, arrows and red margin notes, all in handwriting fonts. The drawing is built as SVG inside an HTML file and rendered to a high-resolution PNG with headless Chrome, so text stays crisp and every label is exact. Use when someone asks to "make a whiteboard image", "draw this on a whiteboard", "recreate this whiteboard photo without the person", "generate a cover image that explains X, Y and Z", or wants a hand-drawn explainer comparing a few concepts side by side. Not for photorealistic images or editing photos (this draws diagrams; it can't remove a person from a photo, only redraw the board's content), for interactive diagrams on a web page (use inline SVG in the page), or for formal architecture diagrams (use component-arch-diagram or archify).
---

# Whiteboard diagram

A whiteboard photo explains a few ideas at a glance: a heading per idea, a small drawing under
each, and red notes where the teacher wanted you to look. This skill draws that, without a camera
or a person in front of it, as an SVG that renders to a sharp PNG. Because every label is real
text, the words are spelled correctly and match the article it illustrates, which an AI image
generator can't promise.

`assets/template.html` is an empty board (room, stand, board, three panels, fonts, arrow markers).
`examples/semantic-ontology-kg.html` is a finished three-panel board comparing a semantic model,
an ontology and a knowledge graph with a shop example. Read both before drawing your first board
in a session; the example shows every drawing pattern below in use.

## Workflow

1. **Get the content right before drawing anything.** List each panel's heading and what it must
   show. If the board illustrates an article, take the terms, names, IDs and example from the
   article itself, so the image and the text agree (the same relationship verbs, the same record
   IDs, the same definitions). Never invent a fact; extra illustrative records are fine, but say so
   when you report.
2. **Check that the panels really differ.** When the board compares concepts, each panel must show
   what makes that concept different, not just a different set of boxes. Ask: if I covered the
   headings, could a reader still tell the panels apart? A semantic model drawn as boxes joined by
   verbs looks exactly like an ontology. Draw it as database tables joined on key columns plus a
   measure, and the difference shows. Tell the user plainly if a reference image they gave gets this
   wrong.
3. **Copy the template** to the scratchpad (`<scratchpad>/whiteboard/board.html`) and fill each
   panel. Keep one comment banner per panel so later edits are easy to find.
4. **Render** with `scripts/render.sh <board.html> <out.png> [scale]` (default scale 2, giving
   2752 × 1536). See "Rendering" for the raw command.
5. **Look at the PNG** with the Read tool. Check every item in "Before you hand it over". Fix and
   re-render until it's clean; it usually takes two or three passes.
6. **Save it where the user wants it** (for a blog, the project's images folder, with a descriptive
   name). Don't overwrite an existing image or change which image a page uses without asking.
7. **Report:** what each panel shows, what you added that isn't in the source, where the file is,
   and what's still the user's call (for example, whether to make it the cover).

## The canvas

- Size 1376 × 768 (16:9-ish, suits cards and covers). The board's writable area is roughly
  x 90–1290, y 70–630.
- Three panels: dividers at x≈482 and x≈902, so panels start at x 96, 516 and 924, each about
  370 px wide. For two panels, one divider at x≈688. For four, it gets cramped; prefer three.
- Per panel, top to bottom: heading (y 112) with a wavy blue underline (y 126); a small grey
  caption (y 160); the drawing (y 170–580); a short blue takeaway line at y 620 ("the math",
  "the meaning", "the facts").
- Don't add marker pens, erasers or other props to the tray. They add clutter and users ask for
  them to be removed.

## The style kit (CSS classes in the template)

| Class | Use |
|---|---|
| `.h` | Panel headings: Marker Felt, blue, 34 px, uppercase, numbered ("1. SEMANTIC MODEL") |
| `.t` | Box and node labels: Noteworthy bold, near-black, 18–22 px |
| `.s` | Small labels and captions: Noteworthy, 13–17 px |
| `.r` | Red margin notes: definitions, rules, recipes, warnings |
| `.b` | Blue labels: edge labels, highlighted columns, takeaways |
| `.box` / `.node` | Rectangles / circles with a dark marker outline |
| `.ink` / `.blue` / `.red` | Lines and connectors in each pen colour |

Arrow markers: `url(#ak)` black, `url(#ab)` blue, `url(#ar)` red. Use colour to mean something:
black for structure, blue for links between real things or keys, red for notes and rules.

## Drawing patterns

- **Hand-drawn lines.** Use gentle cubic curves rather than straight lines for arrows and dividers
  (`M x1 y1 C … x2 y2` with control points a few pixels off the straight path). Keep boxes as true
  rectangles with `rx="4"`; wobbly boxes read as sloppy, not hand-drawn.
- **Concept boxes** (ontology classes, entities): a 48 px-high box with a bold label, an optional
  small grey "Class" label above, and verb-labelled arrows between them (*places*, *lists*,
  *is-a*). Put the verb above or beside the arrow, never on it.
- **Database tables:** a header row with the table name, a rule under it, then one 22 px row per
  column with thin dividers. Colour the key columns blue so readers see which columns join. Lower
  case names (`orders`, `customer_id`) signal "physical table".
- **Joins between tables:** align the two rows that join so the connector is one straight
  horizontal line where possible; otherwise use one smooth S-curve. Mark the ends database-style:
  a short bar at the "one" end, a crow's foot (two short lines fanning onto the table edge) at the
  "many" end. Don't float a key-name label on the line; the blue column names already say it.
- **Graph nodes** (knowledge-graph records): circles of radius 40–46 with an ID in bold and an
  optional second line in small text. Draw edges *before* nodes so nodes sit on top, and end edges
  at the circle's edge with a blue arrow.
- **Red notes:** two or three short lines in `.r`, with an optional red arrow or bracket pointing
  at what they explain. One note per idea.
- **Formula boxes:** a rounded box with the formula in `.t` and the conditions under it in `.r`.

## Text fitting

Handwriting fonts are wider than they look. Budget roughly 0.6 × font-size per character for
`.s`, 0.65 × for bold `.t` and `.b`, and 0.75 × for the `.h` headings. A 17-character heading at
34 px is about 430 px, too wide for a 370 px panel; drop to 30–32 px or shorten it. If a label
must sit on a line, put a board-coloured rectangle (`#fafaf8`) behind it, but prefer moving the
label off the line.

## Rendering

```bash
scripts/render.sh board.html board.png 2
```

which runs:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu \
  --hide-scrollbars --force-device-scale-factor=2 --window-size=1376,768 \
  --screenshot="$PWD/board.png" "file://$PWD/board.html"
```

- Headless Chrome uses the system's handwriting fonts (Marker Felt, Noteworthy, Chalkboard SE on
  macOS). `rsvg-convert` doesn't render the HTML wrapper, so stick with Chrome. On other systems,
  swap the font stack for installed handwriting fonts and say so.
- Scale 2 gives a crisp 2752 × 1536 PNG, around 0.9 MB. For a lighter web cover, render at
  scale 1.
- **Always confirm the render actually ran.** Delete the old PNG first (`rm -f board.png`), or
  check the file's timestamp, before reading it. If the shell is unavailable, reading the old PNG
  will show the *previous* version and make it look as though your edits did nothing.
- If shell commands are blocked, make the edits with the file editor anyway, then give the user the
  exact command to run with a leading `!` so it runs in their session. Don't keep retrying a
  blocked command.

## Before you hand it over

1. Nothing overlaps: no label on a line, no text crossing a box edge or a divider, no arrowhead
   buried inside a box.
2. Every arrow starts and ends where it means to (on the box or circle edge).
3. Headings fit their panel, and each panel's bottom takeaway sits clear of the drawing.
4. Terms, names and IDs match the source text exactly.
5. Covering the headings, a reader could still tell the panels apart.
6. No props on the tray, and no person anywhere.
7. The PNG on disk is the new render (fresh timestamp), saved where the user asked.
