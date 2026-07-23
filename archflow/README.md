# ArchFlow

**A Claude Code skill that turns a written architecture doc into a diagram set and an animated, playable request-flow demo.**

Give it a `system-architecture.md` (or `system-diagram.md`) file and it generates three consistent artifacts, each derived from the one before it:

1. A **Mermaid diagram** — renders inline on GitHub
2. Four **PlantUML diagrams** — `.puml` source + rendered `.png` each: an **architecture diagram** (the static component view), a **simplified architecture diagram** (the same architecture collapsed to 8-10 boxes, for READMEs and slides), a **UML workflow diagram** (a sequence diagram walking one realistic request through the system, phase by phase), and a **simplified workflow diagram** (the same request retold with the cast collapsed to those 8-10 boxes)
3. An **animated live demo** — a self-contained `index.html` that plays that same request flowing through every component (▶️ play, ⏸ pause, ⏮ back, ⏭ step, a draggable timeline scrubber, a clickable activity log that jumps to any step, a click-to-open node inspector, draggable node cards — links stay attached and re-route live, so you can pull cards apart when edges overlap, then hit 💾 Save layout to keep that arrangement across reloads (unsaved drags disappear on reload) — and **removable connections**: click any link to inspect it and ✂ remove it, then replay — the request stops at the cut: that step is blocked, the rest of the flow is skipped as never reached, and the run ends with a "1 blocked, 2 never reached" summary instead of pretending it carried on; a ⛓ Links button reconnects everything)

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
- **Stress-testing** a design — cut a connection in the live demo, replay, and see exactly which steps break and which are stranded downstream

---

## Prerequisites

| Requirement                                            | Needed for                      | Notes                                                                                                               |
| ------------------------------------------------------ | ------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Claude Code                                            | Running the skill               | This is a Claude Code skill, invoked via chat                                                                       |
| A `system-architecture.md` or `system-diagram.md` file | Everything                      | Optional — if you don't have one, the skill offers to explore the codebase and generate it first (see below)        |
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
4. Translate it into four PlantUML diagrams — architecture and workflow sequence, each with a simplified companion — and render the PNGs
5. Turn the workflow scenario into the animated demo's phases and steps
6. Build the animated demo (TSX component + standalone HTML)
7. Run verification checks before reporting done

Review the generated files (see [What gets generated](#what-gets-generated)), then **open `demo/index.html` in your browser** — this is the file you actually want to look at.

---

## Don't have an architecture doc yet?

Just run ArchFlow anyway — if you don't have a doc, the skill offers to generate one first: it explores your codebase following its bundled prompt ([`architecture-doc-prompt.md`](./architecture-doc-prompt.md)), writes `system-architecture.md`, shows you a summary of the components and the end-to-end scenario it picked so you can confirm or correct them, and then continues with the normal pipeline.

Prefer to produce the doc yourself in a separate session (for example, the codebase lives somewhere else)? Paste the prompt below into a Claude Code session opened at the root of that codebase — it asks for exactly the information ArchFlow's steps consume: components, groupings, connection mechanisms, the key-connection callout, and one concrete end-to-end scenario:

```text
Explore this codebase thoroughly and write a `system-architecture.md` at the repository root that captures the system's architecture completely and unambiguously. This document will be the single input for generating architecture diagrams, a UML workflow sequence diagram, and an animated demo of one request flowing through the system — so every component, connection, and scenario step you write will literally become a box, an arrow, or an animation step. Be concrete; leave nothing for a reader to infer.

Ground every claim in code you actually read: entry points, route/handler definitions, service clients and SDK usage, queue/topic declarations, database schemas and connection strings, docker-compose/Kubernetes manifests, CI configs, and environment variables. Never invent a component or connection you cannot point to in the code. If something is genuinely undeterminable from the code (e.g. an auth mechanism configured outside the repo), still include it but mark it `(inferred)`.

Do not include a Mermaid or PlantUML diagram in the document — prose and tables only. (A diagram, if present, would be treated as the source of truth by downstream tooling, so an incomplete one does harm.)

Structure the document exactly like this:

# <System Name> — System Architecture

2-3 sentences: what the system does and who uses it. Give the system a short product-style name — it is used to derive code identifiers, so prefer "OrderHub" over "the order processing and fulfilment platform".

## Components

One `###` subsection per internal component (a deployable or independently-reasonable unit: frontend app, backend/API service, background worker, database, cache, queue broker, gateway, CLI). For each:

- **Name**: 3 words maximum, title case — this becomes a diagram box title and a card label, so "Report Worker", not "the asynchronous report generation worker process".
- **Type**: frontend / backend API service / worker / database / cache / queue / gateway / CLI.
- **Layer**: which of 2-4 named layers it belongs to (e.g. Frontend, Core Services, Data, Integration). Use the same layer names consistently — they become the diagram's groupings.
- **Responsibility**: 1-2 sentences, written to stand alone — this text is shown verbatim as the component's description in an interactive inspector.
- **Tech**: framework/language/runtime, one line.

Aim for 6-14 components. If the codebase has more moving parts than that, fold helpers into the component that owns them (a service's internal modules are one box) and say in the Responsibility line what was folded in. Mark any component that is optional (only runs when configured) as **Optional** and say what enables it.

## External dependencies

Every system this codebase depends on but does not own: third-party APIs, SaaS products, LLM providers, legacy systems, identity providers. For each: name, what it provides, **Required or Optional/fallback**, and one line on what happens when it is unavailable. These render differently from internal components in every diagram, so the internal/external split must be exact — when in doubt, "do we deploy and operate it?" decides.

## Connections

A table with one row per communication edge. This is the section diagrams are drawn from, so precision here matters most:

| From | To | Protocol | Auth | Pattern | What flows |
|------|----|----------|------|---------|------------|

- **Protocol**: REST/JSON, gRPC, GraphQL, WebSocket, AMQP, direct SQL, file share, etc.
- **Auth**: JWT, OAuth2 client-credentials, API key, mTLS, none — per edge, not per system.
- **Pattern**: exactly one of — `request/response` (synchronous call, answer comes back on the same connection), `fire-and-forget` (no reply expected), `queue/pub-sub` (name the queue or topic), `polling` (state explicitly who polls whom and how often — this changes how the flow is animated), `webhook/callback`, `scheduled` (cron — state the schedule).
- **What flows**: 2-5 words naming the payload ("order events", "rendered PDF", "embeddings").

Never write "A integrates with B" — name the mechanism. If two components talk over two different channels for two different purposes, write two rows. If a connection's direction is surprising (the "server" initiates, or replies arrive via a separate callback), spell that out in the What-flows cell.

## The key connection

2-4 sentences on the single most important or most easily misunderstood connection in the architecture — almost always "how does this system actually reach its key external dependency". Write the paragraph a new engineer needs to not get this wrong: is it one connection or two different mechanisms for different purposes, who initiates, what the auth handshake is. This paragraph is repeated across every generated artifact as the one thing a viewer should remember.

## Primary end-to-end scenario

Pick **one** realistic scenario that a real user actually triggers and that touches as many components as possible — this single scenario becomes the workflow sequence diagram and the animated demo, so choose the system's signature flow, not a health check. Write it as a numbered walkthrough of 10-20 steps:

- Start with the user's triggering action, quoted ("user drops an invoice PDF into the upload folder").
- Every step names: the acting component, what it sends/asks/does, the receiving component, over which connection (must match a row in the Connections table), and what comes back if anything.
- Name every intermediate artifact in **bold** the moment it is produced (**Test Plan**, **Invoice Record**, **Signed URL**) and refer to it by that name afterwards.
- Group the steps under 3-6 phase headings written as a story a non-engineer can follow ("Explore the site, then write a plan" — not "Discoverer phase").
- If a step is a synchronous ask-and-answer, write it as one step ("asks the DB for X, gets X back"), not two.
- End with the concrete deliverable returned to the user.

## Side paths and scheduled flows  (only if any exist)

Audit logging, metrics, retry/fallback paths, nightly jobs — each in 1-2 sentences, explicitly flagged as optional or scheduled, so downstream diagrams know they may be dropped from simplified views and are not part of the main request chain.

## Deployment constraints  (only if any exist)

Anything a simplified diagram must not abstract away because it is a real operational fact: components that must share a host or volume, a broker that is the only path between two services, ordering/startup dependencies.

Before you finish, verify the document against this checklist and fix any failure:

1. Every component named in the scenario appears in Components; every hop in the scenario matches a row in Connections; every From/To in Connections appears in Components or External dependencies. No orphans in any direction.
2. Every Connections row has a concrete Pattern — no row says "integrates", "talks to", or "uses".
3. The scenario touches at least ~80% of the internal components; if it can't, say which components are off the main path and why.
4. Someone could draw this system accurately without opening the code. Any sentence that requires the code to disambiguate is not finished.
5. Only what the code does today — no roadmap items, no aspirational features, no marketing language.
```

Then come back and run ArchFlow on the file it produces. (The prompt saves the doc at the repository root — if you keep docs elsewhere, add e.g. "save it to docs/architecture/system-architecture.md" at the end.)

---

## What gets generated

Everything is written next to your input file:

```text
docs/
└── architecture/
    ├── system-architecture.md   (your input)
    ├── system-diagram.md        (Mermaid diagram)
    ├── system-diagram.puml      (PlantUML architecture diagram — source)
    ├── system-diagram.png       (rendered architecture diagram — full detail)
    ├── system-diagram-simple.puml  (simplified architecture diagram — source)
    ├── system-diagram-simple.png   ⭐ the one for a README/slide (8-10 boxes)
    ├── system-workflow.puml     (PlantUML workflow sequence diagram — source)
    ├── system-workflow.png      (rendered workflow diagram — full detail)
    ├── system-workflow-simple.puml (simplified workflow diagram — source)
    ├── system-workflow-simple.png  ⭐ the workflow for a README/slide (same cast as the simplified architecture)
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
4. Generate four PlantUML diagrams from the Mermaid diagram — architecture (components/connections), a simplified 8-10 box version of it, workflow (a sequence diagram of one end-to-end request), and a simplified version of the workflow using the same 8-10 box cast — and render all four PNGs
5. Design the demo scenario — the workflow diagram's phases and messages become the demo's phases and steps
6. Compute layout
7. Generate TSX
8. Generate standalone HTML (vendored React/Babel, works offline)
9. Verify — syntax check, data-integrity check, optional headless render check
10. Report — then open `demo/index.html`

The artifacts are generated **in sequence, each derived from the previous one** — not independently re-derived from your original doc. This keeps them describing the exact same architecture and the exact same request scenario: same components, same edges, same external-system markings.

```
system-architecture.md  →  system-diagram.md (Mermaid)  →  system-diagram.puml (architecture)  →  system-diagram-simple.puml (simplified)  →  system-workflow.puml (workflow sequence)  →  system-workflow-simple.puml (simplified workflow)  →  demo/ (animated HTML, built from the full workflow)
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
├── architecture-doc-prompt.md      (ready-made prompt to generate a system-architecture.md from a codebase)
└── templates/
    ├── DemoFlow.template.tsx       (React demo engine + layout rules)
    ├── DemoFlow.template.css
    └── index.template.html         (standalone HTML shell)
```
