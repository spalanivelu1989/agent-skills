# Generic prompt — layered component architecture diagram

Paste this into a session in any project (fill in the two bracketed parts). If the
`layered-arch-diagram` skill is installed, the session will pick it up; the prompt
also works on its own.

---

Create a high-level, component-level architecture diagram for this application,
saved as `docs/component-architecture.svg` and `docs/component-architecture.png`
(PNG at 2× scale), plus the source spec it is drawn from.

**Research first.** Read the `[docs]` folder to understand the components,
technologies, data flows and integrations, then check the codebase to confirm them
and to catch anything the docs miss — in particular authentication, guardrails,
observability/tracing, evaluation/scoring (for each engine separately), memory
stores, background jobs and local model servers.

**What to show.** Components only — no classes, files or functions. Cover the
frontend, backend/API, application services, AI/agent components, RAG and
knowledge-graph components, databases and storage, LLMs and external services,
authentication and observability. Each box gets a short bold title and a
two-line subtitle (technology · port, or what it does).

**Layout — this matters most.**
- Numbered horizontal layer bands, top to bottom, each titled at its top-left:
  `[1 Presentation · 2 API & cross-cutting · 3 AI agents · 4 Application services ·
  5 Data & memory · 6 Evaluation]`. Model serving and external services go in
  titled groups in a column on the right.
- Put each component in the layer that matches what it is (a model server is model
  serving, not data; evaluation is its own layer).
- Boxes on a regular grid, aligned in columns across the bands; the user → UI →
  API path is one straight vertical line.
- Do **not** use auto-layout (PlantUML, Graphviz, Mermaid) — place every box and
  route every link by hand, then draw it as SVG.

**Links.**
- Directional arrows; every segment horizontal or vertical, with rounded corners.
- No line may pass through a box; route through the gaps between columns and between
  bands. Aim for zero line crossings.
- Keep it uncluttered: draw a fan-out as one bus with drops; when one component
  talks to most of a layer, end one arrow on that layer's edge; when several agents
  share a runtime, connect shared dependencies to the runtime once.
- Label each link with 1–3 words (protocol, action or payload), beside the line,
  never on a box.

**Style.** White background; soft layer bands; each layer's boxes in their own pale
tint; data stores green (cylinders for databases, a folder for file stores);
external/cloud services as dark rounded boxes; a small legend explaining arrows,
"arrow to a layer", the colour conventions, and any security caveat (e.g. auth).

**Verify.** Check programmatically that no link crosses a box and no label sits on
a box or another label, then open the PNG and look at it. Fix and re-render until
it reads cleanly at a glance. Report what each layer holds and which links you
collapsed.
