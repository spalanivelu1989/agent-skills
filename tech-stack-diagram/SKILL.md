---
name: tech-stack-diagram
description: Create a tech-stack diagram (application stack, technology stack or "layer cake"). It shows tinted horizontal layers, each with a sentence-case name, a one-line purpose and 2–3 capability cards (capability → chosen technology), joined by simple down-arrows; there is no box-to-box wiring. Outputs SVG, a large PNG and an editable PowerPoint slide. Use when the user asks for an application stack, tech stack, technology stack, layer-cake, capability map or "what is it built with" diagram, for a whole system or for one feature (an agent, a RAG pipeline, ingestion, evaluation), or wants a manager-friendly or slide-ready overview rather than a wiring diagram. For "who calls whom" component diagrams with routed arrows, use component-arch-diagram instead.
---

# Tech-stack diagram

Answers **"what is this made of, and what did we choose for each part?"** in one
glance. Layers are stages or concerns, read top to bottom. Each card names a
**capability** and the **technology chosen** for it. No coordinates and no
routing: you write a small JSON spec and `scripts/stack_diagram.py` lays it out.

Use it for proposals, slides, onboarding, build-vs-buy and platform comparisons
(the same stack with different cards per platform). If the reader needs to see
data flow, protocols or which component calls which, draw a component
architecture diagram (the `component-arch-diagram` skill) instead. The two
complement each other: show the stack first to set the vocabulary, then the wiring.

## Files

- `scripts/stack_diagram.py spec.json out.svg [--strict]`: lays out and draws the SVG,
  then prints a fit report (text likely to overflow a card, subtitles longer than two
  lines). `--strict` exits 1 on any problem.
- `scripts/export_png.js in.svg out.png [scale]`: crisp PNG via headless Chrome
  (`NODE_PATH="$(npm root -g)" node …`, needs `puppeteer`); scale 2 for docs and slides.
  Without puppeteer: `rsvg-convert -z 2 in.svg -o out.png`.
- `scripts/stack_to_pptx.py spec.json out.pptx`: the same diagram as one editable
  PowerPoint slide, every layer and card a native shape (needs `python-pptx`).
- `examples/*.spec.json`: eight reference specs. One is a whole application
  (`application-stack`). The others cover single features: `rag-tech-stack`,
  `ingestion-stack`, `knowledge-graph-stack`, `evidence-agent-stack`,
  `fitgap-copilot-stack` and `evaluation-observability-stack`. `generic-rag` is a
  product-neutral example with open "A or B" choices. Read two or three
  before writing a new spec, since the wording style matters as much as the structure.

## Workflow

### 1. Decide the scope and the reading order

- **Whole application:** from where people work, down to what everything runs on.
  Typical layers: Experience → API & guardrails → Agents / features → Engines →
  Models → Data & memory → Quality & ops.
- **One feature or pipeline:** layers are the **stages in order**. For ingestion that
  is Sources → Conversion → Structure recovery → Reading images → Chunking & indexing.
  For an agent it is Guardrails → Reasoning → Evidence → Verification → Record & observe.

Use 4–7 layers. More than 7 means two diagrams.

### 2. Inventory from the docs, then confirm in the code

Read the project's docs (architecture notes, READMEs), then check the code for the
real choices: model names and versions, libraries, stores, limits. Cards must
state what is actually used, and an invented or outdated technology is the most
common error. Numbers make cards concrete and are worth finding (`≤ 14 tool calls
per run`, `≤ 1,000 tokens`, `27 hand-checked questions`).

### 3. Write the layers and cards

Content rules (these are what make the format read well):

- **Layer name:** sentence case, 1–3 words, a noun phrase (`Retrieval intelligence`,
  `Gates & scoring`). Not Title Case and not ALL CAPS.
- **Purpose line (`desc`):** one short line that starts with a verb and says what the
  layer *does*: "Turn each file into Markdown", "Prove every quote and compute the
  confidence". Not a list of what it contains.
- **Card = capability → choice.** `title` is the capability in 1–3 words (Embeddings,
  Scope check, Run history). `sub` is the chosen technology or the defining fact
  (`BGE-M3 via Ollama`, `Claude Haiku 4.5 · in or out`). Join facts with ` · `.
- Write an open decision as **"A or B"** (`Qwen 3 or Llama 3`) so it stands out.
- **3 cards per layer** is the default and looks best; 2 is fine. More than
  `per_row` (default 3) wraps to a second row. Prefer splitting the layer instead.
- Keep `sub` to about 32 characters or fewer, on one line. The fit report flags anything longer.
- Don't repeat a technology across many cards. If Langfuse appears everywhere, it
  is one card in the ops layer.
- A hosted or external service can be marked `"style": "dark"`. Use it sparingly:
  colour belongs to the layer, and cards stay neutral.

### 4. Colour and arrows

Each layer gets a `tone`: terracotta, indigo, teal, amber, stone, blue, rose or slate.
When omitted, tones go in that order. The reference diagrams use terracotta (top),
indigo, teal, amber, then stone for the last ops/records layer. Keep stone for the
bottom "quality / ops / records" layer, and slate for an API or guardrails layer.

The renderer draws one arrow between consecutive layers, meaning "feeds / builds on
the next layer". Give a layer an `arrow` label only when the payload matters
(`"arrow": "chunks"`).

### 5. Spec

```json
{
  "title": "Product — Application stack",
  "width": 1400,
  "per_row": 3,
  "layers": [
    {"name": "Experience", "desc": "Where analysts and admins work", "tone": "terracotta",
     "items": [{"title": "Web UI", "sub": "React + Vite · app & demo mode"},
               {"title": "Accounts & roles", "sub": "Session cookie · scrypt"},
               {"title": "Admin dashboard", "sub": "Usage · estimated cost · users"}]},
    {"name": "Models", "desc": "Reason, judge, and embed", "tone": "blue",
     "items": [{"title": "Reasoning LLM", "sub": "Claude Opus 5"},
               {"title": "Embeddings", "sub": "BGE-M3 via Ollama"}]}
  ],
  "legend": {"lines": ["Optional footnote, e.g. 'Cards = capability → chosen technology'"]}
}
```

Optional: `card_h` (default 120), `arrow` per layer, `"style": "dark"` per card,
`legend`. Leave `title` empty when the slide or document already has a heading.

### 6. Render, check, look

```bash
S=~/.claude/skills/tech-stack-diagram/scripts
python3 $S/stack_diagram.py docs/<name>.spec.json docs/<name>.svg
NODE_PATH="$(npm root -g)" node $S/export_png.js docs/<name>.svg docs/<name>.png 2
python3 $S/stack_to_pptx.py docs/<name>.spec.json docs/<name>.pptx      # when it goes in a deck
```

Fix every fit-report problem by shortening the text first, and only then by lowering
`per_row` or widening `width`. Then **open the PNG and look**. The check is an estimate,
and only the image shows a cramped card or an awkward line. Keep the spec next to the
outputs: it is the source, and the SVG, PNG and PPTX are generated from it.

### 7. Report

Give the paths (spec, SVG, PNG and its pixel size, PPTX if made), the layers in order,
and any open "A or B" decisions the diagram shows.

## Variations

- **Platform comparison:** one spec per platform with the same layers and card titles,
  where only the `sub` lines change (`PostgreSQL + pgvector` → `HANA Cloud Vector Engine`).
  Readers compare side by side.
- **Per-feature set:** one whole-application stack plus one stack per major feature,
  all with the same title prefix (`Product — Evidence Agent stack`), as in the examples.
