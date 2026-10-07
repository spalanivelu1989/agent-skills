# ArchFlow

A Claude Code skill that turns a written architecture doc into a set of diagrams and an **animated, playable request-flow demo**.

Give it a `system-architecture.md` (or `system-diagram.md`) and it generates, each artifact derived from the one before:

1. A **Mermaid diagram**, which renders inline on GitHub.
2. Four **PlantUML diagrams** (`.puml` + `.png`): the architecture, a simplified 8–10 box version for READMEs and slides, a sequence diagram of one end-to-end request, and a simplified version of that sequence.
3. A **live demo**: a self-contained `demo/index.html` that plays the same request flowing through every component. It has play, pause, step and a timeline scrubber, and you can drag, group and annotate the cards. You can also cut a link and replay to see which steps break. It works offline, with no build step and no server.

If you don't have an architecture doc yet, ArchFlow offers to explore the codebase and write one first.

## Install

```bash
cp -r archflow ~/.claude/skills/
```

Requirements: none to start. Optional: PlantUML + a JRE for the PNGs, Node.js for the verification checks, and `curl` for vendoring the JS libraries. The skill checks what is installed and proposes the install command for your OS before installing anything. If you decline, it skips that part.

## Use

Ask Claude Code, for example:

```text
Using ArchFlow, generate a live demo workflow from docs/architecture/system-architecture.md
```

Then **open `demo/index.html` in your browser**. That's the main deliverable.

Everything is written next to the input file:

```text
docs/architecture/
├── system-diagram.md                   Mermaid
├── system-diagram(.puml|.png)          architecture, full detail
├── system-diagram-simple(.puml|.png)   architecture, 8–10 boxes
├── system-workflow(.puml|.png)         request sequence, full detail
├── system-workflow-simple(.puml|.png)  request sequence, simplified
└── demo/
    ├── <Name>DemoFlow.tsx / .css       React component
    ├── index.html                      ⭐ the live demo
    └── vendor/                         React + Babel, for offline use
```

To write the architecture doc in a separate session instead, paste [`architecture-doc-prompt.md`](./architecture-doc-prompt.md) into Claude Code at the root of that codebase. Then run ArchFlow on the file it produces.

## Troubleshooting

| Symptom | Fix |
|---|---|
| No PNGs produced | PlantUML isn't installed. Let the skill install it, or use the `.puml` source as is |
| `demo/index.html` is blank | Check the three files in `demo/vendor/` exist |
| Crowded PNG | Simplify the grouping in the `.puml` file and re-render |
| A component is missing | ArchFlow uses only what the doc says. Update the doc and re-run |

## Files

| Path | What it is |
|---|---|
| `SKILL.md` | Full step-by-step process, layout rules and verification checks |
| `architecture-doc-prompt.md` | Prompt that generates a `system-architecture.md` from a codebase |
| `templates/` | React demo engine (`DemoFlow.template.tsx` / `.css`) and the standalone HTML shell |
