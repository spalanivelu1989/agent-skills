# Whiteboard diagram

A Claude Code skill that draws a hand-drawn-style whiteboard image explaining a few concepts side
by side: marker headings, boxes, tables, graph nodes, arrows and red margin notes. It's built as
SVG and rendered to a crisp PNG with headless Chrome, so every word is real, correctly spelled text
that matches the article it illustrates.

## Install

```bash
cp -r whiteboard-diagram ~/.claude/skills/
chmod +x ~/.claude/skills/whiteboard-diagram/scripts/render.sh
```

Needs Google Chrome (or Chromium) and handwriting fonts; on macOS, Marker Felt and Noteworthy are
built in.

## Use

```text
/whiteboard-diagram a cover image comparing semantic model, ontology and knowledge graph
```

Or: "recreate this whiteboard photo without the person, using our shop example".

## Files

- `SKILL.md`: workflow, canvas grid, style kit, drawing patterns, rendering and checks.
- `assets/template.html`: an empty three-panel board to start from.
- `examples/semantic-ontology-kg.html`: a finished board.
- `scripts/render.sh`: renders a board to PNG and fails loudly if nothing was written.
