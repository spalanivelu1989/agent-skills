# ArchFlow

**A Claude Code skill that turns a written architecture doc into a diagram set and an animated, playable request-flow demo.**

Give it a `system-architecture.md` (or `system-diagram.md`) file and it generates three consistent artifacts, each derived from the one before it:

1. A **Mermaid diagram** — renders inline on GitHub
2. A **PlantUML diagram** — `.puml` source + rendered `.png`
3. An **animated live demo** — a self-contained `index.html` that plays one realistic request flowing through every component (▶️ play, ⏸ pause, ⏭ step, plus a live activity log)

No build step, no server — the demo opens directly in a browser and works offline.

> **➡️ Once ArchFlow finishes, open `demo/index.html` in your browser to see the live demo.** That's the main deliverable — everything else (Mermaid, PlantUML, PNG) is supporting material.

---

## Table of contents

- [Quick start](#quick-start)
- [Why it's useful](#why-its-useful)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Don't have an architecture doc yet?](#dont-have-an-architecture-doc-yet)
- [What gets generated](#what-gets-generated)
- [How it works](#how-it-works)
- [Troubleshooting](#troubleshooting)
- [Repository layout](#repository-layout)

---

## Quick start

```text
# 1. Install (one-time)
cp -r archflow ~/.claude/skills/archflow

# 2. Run it against your architecture doc
Using ArchFlow, generate a live demo workflow from docs/architecture/system-architecture.md

# 3. Open the result — open this file in your browser
open docs/architecture/demo/index.html
```

**Open `demo/index.html` in your browser** to see the animated request flow — that's the file that matters.

No architecture doc yet? See [Don't have an architecture doc yet?](#dont-have-an-architecture-doc-yet).

---

## Why it's useful

- **Onboarding** new team members without a whiteboard session
- **Explaining** system architecture in a way that's actually watchable, not just read
- **Walking stakeholders** through a request end-to-end, component by component
- **Understanding** how an unfamiliar application really works, straight from its own docs

---

## Prerequisites

| Requirement                                            | Needed for                   | Notes                                                                                                                                     |
| ------------------------------------------------------ | ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Claude Code                                            | Running the skill            | This is a Claude Code skill, invoked via chat                                                                                             |
| A `system-architecture.md` or `system-diagram.md` file | Everything                   | See below if you don't have one                                                                                                           |
| PlantUML + a JRE                                       | Step 2 (PNG rendering)       | `brew install plantuml` on macOS. Optional — the skill still produces the `.puml` source and continues without the PNG if this is missing |
| Node.js                                                | Optional verification checks | Only used if `@babel/core` or `puppeteer` are already resolvable in your project; not a hard requirement                                  |

---

## Installation

Copy the skill folder into your Claude Code skills directory:

```bash
cp -r archflow ~/.claude/skills/archflow
```

That's it — no dependencies to install, no build step.

---

## Usage

Point the skill at your architecture document from within Claude Code:

```text
Using ArchFlow, generate a live demo workflow from docs/architecture/system-architecture.md
```

Claude Code will:

1. Read and understand your architecture doc
2. Generate/refresh the Mermaid diagram
3. Translate it into a PlantUML diagram and render the PNG
4. Design a realistic end-to-end request scenario
5. Build the animated demo (TSX component + standalone HTML)
6. Run verification checks before reporting done

Review the generated files (see [What gets generated](#what-gets-generated)), then **open `demo/index.html` in your browser** — this is the file you actually want to look at.

---

## Don't have an architecture doc yet?

ArchFlow works from a doc you already have — it doesn't explore your codebase itself. If you don't have one, ask Claude Code to write it first:

```text
Explore this entire repository (frontend, backend, database/migrations, config, docs, README) and write a system-architecture.md file summarizing:

1. What this project does (one paragraph)
2. Every distinct component/layer: frontend(s), backend/API service(s), databases, background workers, sidecars, gateways/proxies, auth services — for each, its name, tech stack, and entry point (main file)
3. Every external dependency: third-party APIs, SaaS tools, legacy systems, LLM providers — anything the system depends on but doesn't own
4. For every connection between two components (internal-to-internal, or internal-to-external), state:
   - The protocol (REST, GraphQL, gRPC, WebSocket, message queue, direct SQL, etc.)
   - The auth mechanism if any (JWT, OAuth2, API key, Basic Auth)
   - A one-line description of what that connection is for
5. The high-level request flow: trace one representative user action from the UI all the way down to the database and back, naming every hop
6. Any open questions or unclear areas you noticed while exploring

Keep it concise and factual — this file will be used to auto-generate an architecture diagram, so be explicit and complete about every component and connection rather than vague or high-level. Save it to docs/architecture/system-architecture.md (create the folder if needed).
```

Then come back and run ArchFlow on the file it produces.

---

## What gets generated

Everything is written next to your input file:

```text
docs/
└── architecture/
    ├── system-architecture.md   (your input)
    ├── system-diagram.md        (Mermaid diagram)
    ├── system-diagram.puml      (PlantUML source)
    ├── system-diagram.png       (rendered diagram)
    └── demo/
        ├── <Name>DemoFlow.tsx   (React component)
        ├── <Name>DemoFlow.css
        ├── index.html           ⭐ OPEN THIS — the live demo, works standalone, offline
        └── vendor/
            ├── react.production.min.js
            ├── react-dom.production.min.js
            └── babel.min.js
```

`<Name>` is a short identifier derived from your project name (e.g. `Cpi`, `Order`).

---

## How it works

The three artifacts are generated **in sequence, each derived from the previous one** — not independently re-derived from your original doc. This keeps them describing the exact same architecture: same components, same edges, same external-system markings.

```
system-architecture.md  →  system-diagram.md (Mermaid)  →  system-diagram.puml (PlantUML)  →  demo/ (animated HTML)
```

For the full step-by-step process (layout rules, verification checks, and the hard-won lessons behind two previously-fixed bugs), see [`SKILL.md`](./SKILL.md).

---

## Troubleshooting

| Symptom                                                | Cause                                                                | Fix                                                                                                              |
| ------------------------------------------------------ | -------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| No `system-diagram.png` was produced                   | PlantUML isn't installed                                             | `brew install plantuml` (macOS), then re-run — or proceed without the PNG                                        |
| `demo/index.html` shows a blank page                   | Missing/broken `vendor/` files, or opened over a restrictive network | Confirm the three files exist in `demo/vendor/`; the demo is designed to work fully offline once they're present |
| Diagram looks crowded or components overlap in the PNG | PlantUML's auto-layout struggled with too many packages              | Simplify grouping in `system-diagram.puml` and re-render                                                         |
| Demo is missing a component you expected               | The input doc didn't mention it                                      | ArchFlow only uses what's in your architecture doc — update the doc and re-run                                   |

---

## Repository layout

```text
archflow/
├── README.md                       (this file)
├── SKILL.md                        (full skill definition — read this to understand or modify the generation logic)
└── templates/
    ├── DemoFlow.template.tsx       (React demo engine + layout rules)
    ├── DemoFlow.template.css
    └── index.template.html         (standalone HTML shell)
```
