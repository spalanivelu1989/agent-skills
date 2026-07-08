## ArchFlow – Claude Code Skill for Architecture Visualization & Live Workflow Demos

## What it does

Give ArchFlow any `system-architecture.md` or `system-diagram.md` file describing your application's components, and it automatically generates three things — each built from the one before it, so they all describe the same architecture:

1. **A Mermaid diagram** (`system-diagram.md`)

   - Quick and readable
   - Renders inline on GitHub and most markdown viewers

2. **A clean PlantUML architecture diagram** — translated from the Mermaid diagram

   - `.puml` source
   - Rendered `.png` image

3. **An animated, playable workflow demo** — built from the PlantUML's component list
   - Simulates a real request flowing through your system
   - Shows interactions across components (Frontend → Backend → External APIs → Database, etc.)
   - Includes:
     - ▶️ Play
     - ⏸ Pause
     - ⏭ Step controls
     - 📋 Live activity log

The demo is a self-contained `index.html` that opens directly in a browser—**no build step or server required**.

## Why it's useful

Great for:

- Onboarding new team members
- Explaining system architecture
- Walking stakeholders through request flows
- Understanding how the application actually works without drawing diagrams on a whiteboard

## Don't have an architecture doc yet?

ArchFlow needs a `system-architecture.md` (or `system-diagram.md`) to work from — it doesn't explore your codebase itself. If you don't have one, ask Claude Code to write it first:

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

## How to use

### 1. Get the skill

Copy the skill into:

```text
~/.claude/skills/archflow/
```

### 2. Run it in Claude Code

Point the skill at your architecture document:

```text
Using ArchFlow, generate a live demo workflow from docs/architecture/system-architecture.md
```

### 3. Review the generated output

ArchFlow writes everything next to your input file:

```text
docs/
└── architecture/
    ├── system-architecture.md   (your input)
    ├── system-diagram.md        (Mermaid diagram)
    ├── system-diagram.puml
    ├── system-diagram.png
    └── demo/
        ├── index.html
        └── ...
```

Simply open `demo/index.html` in your browser to explore the animated workflow — no build step, no server, works offline.
