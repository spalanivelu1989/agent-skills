# Component architecture diagram

A Claude Code skill that draws a clean **component architecture diagram** — "how are the parts wired together?" — as SVG, a large PNG and an editable PowerPoint slide.

The diagram has numbered horizontal layer bands (Presentation → API → Agents → Services → Data → Evaluation), a side column for model serving and external services, and hand-routed right-angle links labelled with protocol or payload. Links never pass through a box. Use it when an auto-laid-out PlantUML, Graphviz or Mermaid diagram has turned into a tangle. It draws business-process flows in the same style too.

For a "what is it built with?" layer-cake diagram with no wiring, use [`tech-stack-diagram`](../tech-stack-diagram/) instead.

## Install

```bash
cp -r component-arch-diagram ~/.claude/skills/
```

Requirements: Python 3. Optional: `puppeteer` (Node) for PNG export, or `rsvg-convert` / `cairosvg` instead; `python-pptx` for the PowerPoint slide.

## Use

Ask Claude Code, for example:

```text
Draw a component architecture diagram of this codebase
Turn this returns process into a process-flow diagram in the same style
```

Claude reads your docs and code, lists the components and connections, places every box on a grid, routes each link, then renders and checks the result. It fixes anything the checker reports and looks at the PNG before handing it over.

## Run the scripts yourself

```bash
S=~/.claude/skills/component-arch-diagram/scripts
python3 $S/relax.py docs/arch.layout.json docs/arch.spec.json      # widen the compact grid
python3 $S/render.py docs/arch.spec.json docs/arch.svg              # draw + report problems (--strict)
NODE_PATH="$(npm root -g)" node $S/export_png.js docs/arch.svg docs/arch.png 2
python3 $S/spec_to_pptx.py docs/arch.spec.json docs/arch.pptx       # editable slide
```

Edit the compact `*.layout.json` file. The relaxed spec, SVG, PNG and PPTX are all generated from it.

## Files

| Path | What it is |
|---|---|
| `SKILL.md` | Full workflow, layout grid, routing rules and spec format |
| `prompt.md` | Generic prompt to paste into another session or project |
| `scripts/` | `render.py`, `relax.py`, `export_png.js`, `spec_to_pptx.py`, `stack.py` |
| `examples/` | A 22-box component architecture spec and a business-process flow spec |
