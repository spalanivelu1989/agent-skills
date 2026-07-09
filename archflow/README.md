# ArchFlow

**A Claude Code skill that turns a written architecture doc into a diagram set and an animated, playable request-flow demo.**

Give it a `system-architecture.md` (or `system-diagram.md`) file and it generates three consistent artifacts, each derived from the one before it:

1. A **Mermaid diagram** — renders inline on GitHub
2. Two **PlantUML diagrams** — `.puml` source + rendered `.png` each: an **architecture diagram** (the static component view) and a **UML workflow diagram** (a sequence diagram walking one realistic request through the system, phase by phase)
3. An **animated live demo** — a self-contained `index.html` that plays that same request flowing through every component (▶️ play, ⏸ pause, ⏮ back, ⏭ step, a draggable timeline scrubber, a clickable activity log that jumps to any step, and a click-to-open node inspector)

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

| Requirement                                            | Needed for                      | Notes                                                                                                               |
| ------------------------------------------------------ | ------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Claude Code                                            | Running the skill               | This is a Claude Code skill, invoked via chat                                                                       |
| A `system-architecture.md` or `system-diagram.md` file | Everything                      | See below if you don't have one                                                                                     |
| PlantUML + a JRE                                       | Step 3 (PNG rendering)          | Optional — the skill still produces the `.puml` source and continues without the PNG if this is missing             |
| Node.js + npm                                          | Step 8 (verification checks)    | Optional — used for a syntax check, a data-integrity check, and (if `puppeteer` is available) a visual render check |
| `curl`                                                 | Step 7 (vendoring JS libraries) | Ships with macOS, Linux, and Windows 10+ by default                                                                 |

**You don't need to install any of these yourself first.** The skill checks what's already on your machine and, if something's missing, detects your OS (macOS / Linux / WSL / native Windows) and proposes the exact install command for it — `brew`, `apt`/`dnf`/`pacman`, or `choco`/`winget` — before asking you to confirm. Decline any of it and the skill just degrades gracefully (skips the PNG, or skips that one verification check) rather than failing.

<details>
<summary>Manual install commands, if you'd rather do it yourself first</summary>

**macOS:**

```bash
brew install plantuml node
```

**Linux (Debian/Ubuntu):**

```bash
sudo apt update && sudo apt install -y default-jre graphviz plantuml nodejs npm
```

**Linux (Fedora/RHEL):**

```bash
sudo dnf install -y java-17-openjdk plantuml nodejs npm
```

**Linux (Arch):**

```bash
sudo pacman -S --noconfirm jre-openjdk plantuml nodejs npm
```

**Windows (Chocolatey):**

```powershell
choco install -y plantuml nodejs-lts
```

**Windows (winget — no reliable PlantUML package; install Java + Node, then grab plantuml.jar manually):**

```powershell
winget install -e --id OpenJS.NodeJS.LTS
winget install -e --id EclipseAdoptium.Temurin.17.JRE
```

Then download `plantuml.jar` from https://plantuml.com/download and put a small `plantuml.bat` shim (`java -jar C:\tools\plantuml.jar %*`) on your PATH.

**Windows Subsystem for Linux (WSL):** use the Debian/Ubuntu (apt) commands above — WSL behaves like Linux, not native Windows.

Optional npm packages for the Step 8 checks, any platform:

```bash
npm install -g @babel/core @babel/preset-react puppeteer
```

Note: globally installed npm packages aren't on Node's default `require()` path — the skill's verification commands account for this by running with `NODE_PATH="$(npm root -g)"`.

Puppeteer bundles its own Chromium (~200MB); on minimal Linux (containers, headless servers) it may also need `sudo apt install -y libnss3 libatk-bridge2.0-0 libgtk-3-0 libgbm1`.

</details>

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

1. Check for prerequisites (PlantUML, Node.js, curl) and offer to install anything missing for your OS — you'll be asked to confirm before anything gets installed
2. Read and understand your architecture doc
3. Generate/refresh the Mermaid diagram
4. Translate it into two PlantUML diagrams — architecture + workflow sequence — and render the PNGs
5. Turn the workflow scenario into the animated demo's phases and steps
6. Build the animated demo (TSX component + standalone HTML)
7. Run verification checks before reporting done

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
    ├── system-diagram.puml      (PlantUML architecture diagram — source)
    ├── system-diagram.png       (rendered architecture diagram)
    ├── system-workflow.puml     (PlantUML workflow sequence diagram — source)
    ├── system-workflow.png      (rendered workflow diagram)
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

Live demo workflow

1. Check prerequisites (offer to install anything missing)
2. Read & understand the architecture doc
3. Generate Mermaid diagram
4. Generate two PlantUML diagrams from the Mermaid diagram — architecture (components/connections) + workflow (a sequence diagram of one end-to-end request) — and render both PNGs
5. Design the demo scenario — the workflow diagram's phases and messages become the demo's phases and steps
6. Compute layout
7. Generate TSX
8. Generate standalone HTML (vendored React/Babel, works offline)
9. Verify — syntax check, data-integrity check, optional headless render check
10. Report — then open `demo/index.html`

The artifacts are generated **in sequence, each derived from the previous one** — not independently re-derived from your original doc. This keeps them describing the exact same architecture and the exact same request scenario: same components, same edges, same external-system markings.

```
system-architecture.md  →  system-diagram.md (Mermaid)  →  system-diagram.puml (architecture)  →  system-workflow.puml (workflow sequence)  →  demo/ (animated HTML)
```

For the full step-by-step process (prerequisite checks, layout rules, verification checks, and the hard-won lessons behind two previously-fixed bugs), see [`SKILL.md`](./SKILL.md).

---

## Troubleshooting

| Symptom                                                      | Cause                                                                | Fix                                                                                                                         |
| ------------------------------------------------------------ | -------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| No `system-diagram.png` / `system-workflow.png` was produced | PlantUML isn't installed                                             | Let the skill offer to install it for your OS (see [Prerequisites](#prerequisites)), or proceed without the PNGs            |
| `demo/index.html` shows a blank page                         | Missing/broken `vendor/` files, or opened over a restrictive network | Confirm the three files exist in `demo/vendor/`; the demo is designed to work fully offline once they're present            |
| Diagram looks crowded or components overlap in the PNG       | PlantUML's auto-layout struggled with too many packages/participants | Simplify grouping in `system-diagram.puml` (or drop lightly-touched participants from `system-workflow.puml`) and re-render |
| Demo is missing a component you expected                     | The input doc didn't mention it                                      | ArchFlow only uses what's in your architecture doc — update the doc and re-run                                              |
| Prerequisite install command fails (permissions, sudo)       | Package manager needs elevated rights, or isn't installed itself     | Run the proposed command yourself in a terminal with the right privileges, then re-run the skill                            |

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
