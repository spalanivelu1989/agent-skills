# Tech-stack diagram

A Claude Code skill that draws a **tech-stack ("layer cake") diagram**. It answers "what is this made of, and what did we choose for each part?" and outputs SVG, a large PNG and an editable PowerPoint slide.

Each tinted horizontal layer has a sentence-case name, a one-line purpose and 2–3 cards. Each card pairs a **capability** with the **technology chosen** for it, e.g. *Embeddings → BGE-M3 via Ollama*. Simple down-arrows join the layers, with no box-to-box wiring. It works for a whole application or for one feature such as an agent, a RAG pipeline, ingestion or evaluation. Use it for proposals, slides, onboarding and platform comparisons.

For "who calls whom" with routed arrows, use [`component-arch-diagram`](../component-arch-diagram/) instead.

## Install

```bash
cp -r tech-stack-diagram ~/.claude/skills/
```

Requirements: Python 3. Optional: `puppeteer` (Node) or `rsvg-convert` for PNG export; `python-pptx` for the PowerPoint slide.

## Use

Ask Claude Code, for example:

```text
Make a tech-stack diagram of this application
Draw the RAG pipeline as a layer-cake diagram for a slide
```

Claude picks 4–7 layers, checks the real technology choices in the docs and code, writes a small JSON spec, then renders it. You don't need to set any coordinates; the script lays the diagram out.

## Run the scripts yourself

```bash
S=~/.claude/skills/tech-stack-diagram/scripts
python3 $S/stack_diagram.py docs/stack.spec.json docs/stack.svg     # draw + fit report (--strict)
NODE_PATH="$(npm root -g)" node $S/export_png.js docs/stack.svg docs/stack.png 2
python3 $S/stack_to_pptx.py docs/stack.spec.json docs/stack.pptx    # editable slide
```

A minimal spec:

```json
{
  "title": "Product — Application stack",
  "layers": [
    {"name": "Experience", "desc": "Where analysts and admins work", "tone": "terracotta",
     "items": [{"title": "Web UI", "sub": "React + Vite"},
               {"title": "Accounts & roles", "sub": "Session cookie · scrypt"}]}
  ]
}
```

## Files

| Path | What it is |
|---|---|
| `SKILL.md` | Full workflow, content rules, colours and spec format |
| `scripts/` | `stack_diagram.py`, `export_png.js`, `stack_to_pptx.py` |
| `examples/` | Eight reference specs: a whole-application stack and seven single-feature stacks |
