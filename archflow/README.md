Hey team — built a Claude Code skill called ArchFlow that's been really handy, sharing in case useful for you too.

What it does: Give it any system-architecture.md or system-diagram.md file describing your app's components, and it generates:
1. A clean PlantUML diagram (+ rendered PNG) of the architecture
2. An animated, playable demo — a little movie of one real request flowing through every component (frontend → backend → external APIs → DB, etc.), with play/pause/step controls and a live activity log. Opens as a single index.html, no build step, no server needed.

Genuinely useful for onboarding new folks or walking stakeholders through "how does this thing actually work" without a live whiteboard session.

How to use it:
1. Get the skill: ~/.claude/skills/archflow/ (ask me and I'll send you the folder, or grab it from [wherever you're hosting it])
2. In Claude Code, point it at your architec
▎ "Using ArchFlow, generate a live demo workflow from docs/architecture/system-diagram.md"
3. It writes everything next to your input file — the .puml/.png, plus a demo/ folder with the component + index.html. Just open index.html in a browser.

Takes maybe 5-10 min end to end depending on how complex the architecture is. Let me know if you try it and hit anything weird.
