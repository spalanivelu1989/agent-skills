## ArchFlow – Claude Code Skill for Architecture Visualization & Live Workflow Demos

## What it does

Give ArchFlow any `system-architecture.md` or `system-diagram.md` file describing your application's components, and it automatically generates:

1. **A clean PlantUML architecture diagram**
   - `.puml` source
   - Rendered `.png` image

2. **An animated, playable workflow demo**
   - Simulates a real request flowing through your system
   - Shows interactions across components (Frontend → Backend → External APIs → Database, etc.)
   - Includes:
     - ▶️ Play
     - ⏸ Pause
     - ⏭ Step controls
     - 📋 Live activity log

The output is a self-contained `index.html` that opens directly in a browser—**no build step or server required**.

## Why it's useful

Great for:

- Onboarding new team members
- Explaining system architecture
- Walking stakeholders through request flows
- Understanding how the application actually works without drawing diagrams on a whiteboard

## How to use

### 1. Get the skill

Copy the skill into:

```text
~/.claude/skills/archflow/
```

### 2. Run it in Claude Code

Point the skill at your architecture document:

```text
Using ArchFlow, generate a live demo workflow from docs/architecture/system-diagram.md
```

### 3. Review the generated output

ArchFlow writes everything next to your input file:

```text
docs/
└── architecture/
    ├── system-diagram.md
    ├── system-diagram.puml
    ├── system-diagram.png
    └── demo/
        ├── index.html
        └── ...
```

Simply open `demo/index.html` in your browser to explore the animated workflow.

