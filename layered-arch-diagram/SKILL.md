---
name: layered-arch-diagram
description: Draw a clean, high-level component architecture diagram (SVG + large PNG) of a codebase — numbered horizontal layer bands, side columns for model serving / external services, hand-routed right-angle links with no line through any box. Use when the user asks for a component / high-level / layered architecture diagram, or complains that an auto-laid-out (PlantUML, Graphviz, Mermaid) diagram looks cluttered, tangled, or like a "wired mesh".
---

# Layered architecture diagram

Produces the kind of diagram a technical manager or architect reads at a glance:
numbered horizontal **layer bands** (Presentation → API → Agents → Services →
Data → Evaluation …), a **side column** for model serving and external services,
and **right-angle links** that run through the gaps between boxes. You place every
box and route every link yourself; `scripts/render.py` draws the spec and checks it.

Why not PlantUML/Graphviz/Mermaid: auto-layout decides where lines go, and once a
diagram has ~15+ components with fan-out (an API calling six things, an LLM called
from five places) it weaves lines across boxes and each other. Tweaking direction
hints and hidden edges only moves the tangle. Hand-placing on a grid and routing in
the gaps is what gives the clean result — and it is quick once the plan is right.

## Files

- `scripts/render.py spec.json out.svg` — draws the SVG and prints a report:
  diagonal segments, links running through a box, labels on boxes or on each other,
  and crossings. `--strict` exits 1 on any problem.
- `scripts/export_png.js in.svg out.png [scale]` — crisp PNG via headless Chrome
  (`NODE_PATH="$(npm root -g)" node …`; needs `puppeteer`). Default scale 2.
  Without puppeteer: `rsvg-convert -z 2 in.svg -o out.png`, or `cairosvg`.
- `examples/process-flow.spec.json` — a business-process example (stages, roles, decisions, exceptions).
- `examples/component-architecture.spec.json` — a complete real example (22 boxes,
  32 links, 6 bands, 2 side groups, a bus, layer-level arrows). Read it before
  writing a new spec; copy its coordinates as the starting grid.
- `prompt.md` — the generic prompt, for pasting into another session or project.

## Workflow

### 1. Inventory the components (from the docs, then the code)

Read the project's docs folder first (architecture notes, READMEs, runbooks), then
confirm against the code: entry points, services, stores, external calls, and
the cross-cutting pieces (auth, guardrails, observability, evaluation). For each
component note: a 1-3 word **title**, a two-line **subtitle** (technology · port,
or what it does), and its **kind** (ui, api, agent, svc, data, model, eval, ops, ext).

Stay at component level — no classes, files or functions. Things that are easy to
miss and worth a separate look in the code: evaluation / scoring (per engine —
RAG, agents, graph…), memory stores, auth, tracing/observability, background jobs,
local model servers.

### 2. Assign layers — and get the layer of each box right

Typical bands, top to bottom: 1 Presentation · 2 API & cross-cutting · 3 Agents /
orchestration · 4 Application services · 5 Data & memory · 6 Evaluation. Side column
(right): Model serving · External services.

Put a box in the layer that matches **what it is**, not where it happens to fit:
a model server (Ollama, vLLM) stores nothing, so it is *Model serving*, not *Data*;
evaluation/scoring is its own layer, not a service. When unsure, ask the user —
this is the one decision worth a question.

### 3. Draw the connection list, then collapse it

List every real connection (A → B, 1-3 word label: protocol, action or payload).
Then reduce clutter **without making anything false**:

- **Bus**: one source fanning out to a row (API → three agents) = one trunk down,
  one horizontal bar, short drops, a junction dot. One label.
- **Arrow to a layer**: when one box talks to most of a band (API → services;
  evaluation → Langfuse), end the arrow on the band's edge instead of on each box.
  Say so in the legend: "an arrow to a layer = used by several of its parts".
- **Shared box**: agents that share a runtime connect through it, so memory / LLM /
  web links leave the runtime once, not each agent.
- Never merge two edges whose sources really differ in a way the reader needs
  (e.g. RAG → LLM for answers vs Eval → LLM for judging).

### 4. Lay out the grid

Proven geometry (see the example spec): canvas ~1830 wide; boxes 200×78; four main
columns at centres x = 330 / 610 / 890 / 1170 (280 pitch → 80 px gaps for lanes);
bands x 20–1340, 130 tall (250 for a band with two rows), 20 px apart; band title
at the band's top-left; side column centred ~x 1590 in groups 330 wide; title
at the top; legend box under the last band.

Placement rules:
- The main path (user → UI → API) is one straight vertical line.
- Put a box **directly under** what calls it whenever possible (straight vertical link).
- Leave one column **empty** in a band when a long vertical link has to pass through it.
- Put side-column boxes at the height of the band that talks to them most, so
  those links are short horizontals.

### 5. Route every link by hand

A link is a list of points; every segment horizontal or vertical (corners are
rounded automatically). Rules that keep it clean:

- Start/end on the **box edge** (or inside the box); the arrowhead goes on the end.
- Run vertical lanes through the **gaps between columns** (e.g. x = 470, 750, 1030)
  and horizontal lanes through the **gaps between bands** (e.g. y = band bottom + 10).
- Several links leaving one side of a box: give each its own exit height
  (e.g. y = 530 and 568). Order exits so the one that turns farthest away leaves
  on the outside; then they never cross.
- Long "back-up" links (evaluation → an external service at the top) go round the
  far right in their own lanes (x = 1765, 1795), nested so they don't cross.
- Two links into one box from the same side: different heights.
- Target 0 crossings; accept 1–2 only if the alternative is a long detour.

Labels: 1-3 words, placed beside the segment (`label_at`, `anchor` start / middle /
end), never on a box. They get a white halo, so a label may sit on a line, but not
on another label.

### 6. Render, check, look, fix

```bash
S=~/.claude/skills/layered-arch-diagram/scripts
python3 $S/render.py docs/<name>.spec.json docs/<name>.svg
NODE_PATH="$(npm root -g)" node $S/export_png.js docs/<name>.svg docs/<name>.png 2
```

Fix every reported problem, then **open the PNG and look** (Read the image). The
checker cannot see everything: a label cramped against a band edge, a group title
under a box, a lane hugging a box. Typical fixes: move a label (anchor "end" to put
it left of a vertical line), give a group 20 px more top padding, move a lane 20 px.
Iterate until it reads cleanly. Keep the spec in the repo next to the SVG — it is
the source; the PNG and SVG are outputs.

### 7. Report

Give the paths (spec, SVG, PNG and its pixel size), what each band holds, which
links were collapsed into buses / layer arrows, and any crossing you accepted and why.

## Process diagrams (same style)

The same renderer draws business-process flows (see `examples/process-flow.spec.json`,
an India customer-returns As-Is process):

- **Bands = process stages** (Request & approval → Authorize & return goods → …), steps
  left to right inside a band; the flow drops to the next band through the gap
  between bands ("carriage return" lane, labelled with the hand-off condition).
- **Box colour = the role that owns the step**: define one `kind` per role and add a
  colour key with `legend.swatches`. Decisions use `"shape": "hex"`.
- **Branches** (e.g. replacement / no credit) run down lanes between columns or at
  the right edge of the bands to the step they rejoin.
- **Exceptions**: a right-hand group with two small boxes (`"h": 52`) per stage, fed
  by one red dashed bus from the band's edge (`"color": "#C0392B", "dashed": true`)
  — "exceptions that can arise in this stage", not a line per step.
- **Systems & records**: a bottom band without links; the step subtitles say which
  system each step uses.

## Spec format (summary — the example is the reference)

```json
{
  "title": "System — Component Architecture",
  "canvas": {"width": 1830, "height": 1160},
  "box": {"w": 200, "h": 78},
  "kinds": {"ops": {"fill": "#FFF8E1", "stroke": "#B8962E"}},
  "bands":  [{"n": "1", "name": "Presentation", "x": 20, "y": 60, "w": 1320, "h": 130}],
  "groups": [{"n": "7", "name": "Model Serving", "x": 1420, "y": 492, "w": 330, "h": 298}],
  "actors": [{"label": "Analyst /\nConsultant", "cx": 330, "cy": 125}],
  "nodes":  [{"id": "API", "title": "Backend API", "sub": "FastAPI · REST + SSE\n:8000",
              "kind": "api", "cx": 890, "cy": 275, "shape": "rect|cyl|folder|cloud", "w": 200}],
  "links":  [{"pts": [[890, 164], [890, 234]], "label": "REST / SSE", "label_at": [900, 204],
              "anchor": "start", "arrow": true, "dashed": false, "name": "optional, for reports"}],
  "junctions": [[890, 375]],
  "labels": [{"text": "run agents", "at": [900, 360]}],
  "legend": {"box": {"x": 20, "y": 1080, "w": 1320}, "lines": ["Arrows = request / data direction"]}
}
```

Kinds built in: ui, api, agent, svc, data, model, eval, ops, ext (dark); add your own
under `kinds`. Shapes: `cyl` for databases, `folder` for file stores, `cloud` (dark
pill) for external services, `hex` for decisions, `rect` for everything else. Links
take an optional `color`; `legend.swatches` (`[{"kind": "cs", "text": "Customer
Service"}]`) draws a colour key above the legend lines. Keep the conventions consistent: data stores
green, external services dark.
