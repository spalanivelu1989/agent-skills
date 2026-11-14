# Agent skills

These are the skills I use with Claude Code: diagrams, demo videos, podcasts, research papers and the house writing style. A skill is a folder with a `SKILL.md` file in it. The agent first reads only each skill's name and its one-line description, and opens the full instructions only once it decides the skill fits the task. So installing many skills costs almost nothing until one of them is used.

## Install

Copy or link any skill folder into `~/.claude/skills/` to make it available in every project, or into `.claude/skills/` inside a repo to make it available only there:

```bash
git clone https://github.com/spalanivelu1989/agent-skills.git
ln -s "$PWD/agent-skills/archflow" ~/.claude/skills/archflow
```

Claude Code finds the skill on its next start. You can call it by name (`/archflow`) or just describe the task and let the agent pick it.

## The skills

### Diagrams and visuals

| Skill | What it does |
|---|---|
| [archflow](archflow/) | Turns a `system-architecture.md` into a Mermaid diagram, four PlantUML diagrams with PNGs, and an animated, interactive demo of one request flowing through the system. |
| [archify](archify/) | Builds validated architecture, sequence, data-flow, state, ERD, class, tree, timeline and waterfall diagrams as explorable standalone HTML, with light and dark themes and image, SVG or WebM export. |
| [archify-review](archify-review/) | Reviews Archify issues, PRs or code in terms of value, cost and impact, for triage and maintenance decisions. |
| [component-arch-diagram](component-arch-diagram/) | Draws a clean component architecture diagram (SVG, PNG, editable PPTX) with layer bands and hand-routed, labelled links that never cross a box. |
| [tech-stack-diagram](tech-stack-diagram/) | Draws a "layer cake" tech-stack diagram: each layer with its purpose and the technology chosen for each capability. Outputs SVG, PNG and a PowerPoint slide. |
| [dataviz](dataviz/) | Design rules for any chart, dashboard or stat tile: how to pick the chart type, a colour formula with a validator, and consistent light and dark styling. |

### Demos, video and audio

| Skill | What it does |
|---|---|
| [demo-script](demo-script/) | Turns rough walkthrough steps into a polished, timed `script.md` with on-screen actions and narration, checked against the app's code or the live app. |
| [demo-video](demo-video/) | Records a narrated, captioned MP4 walkthrough of a running web app or a slide deck, using Playwright and a local Kokoro voice-over, with every screen action timed to the words that describe it. |
| [demo-podcast](demo-podcast/) | Produces a two-host podcast episode (MP3 with chapters) from documents, decks or notes, voiced locally with Chatterbox and Kokoro and checked with Whisper. |
| [video-transcript](video-transcript/) | Gets a timestamped transcript of a YouTube or other online video. It tries a transcript service first, then existing captions, and finally downloads the audio and transcribes it locally with Whisper. |

### Writing and documents

| Skill | What it does |
|---|---|
| [explainer-voice](explainer-voice/) | The house writing voice for prose: a science-magazine explainer style that carries one running example and states plainly what is known and what isn't. |
| [html-format](html-format/) | Produces a standalone HTML document in the house design system: teal accent, JetBrains Mono, sidebar navigation, search, sidenotes and a light/paper/dark toggle. |
| [research-paper](research-paper/) | Writes a print-ready A4 PDF research paper or white paper, with cited and evidence-graded claims, rendered with headless Chrome and checked page by page. |
| [explain-handover](explain-handover/) | Explains a document you were handed with no background (spreadsheet, Word file, deck, PDF or code), including hidden sheets, comments and formulas, as a styled HTML page. |

### Feature planning and code

| Skill | What it does |
|---|---|
| [analyze-feature-impact](analyze-feature-impact/) | Maps the files, components and dependencies a planned feature will touch, before tasks are written. Its output feeds assess-refactoring. |
| [assess-refactoring](assess-refactoring/) | Finds refactoring opportunities in the code a feature will touch, using SOLID principles, so they can be done before the feature work. |
| [push](push/) | Commits every pending change and pushes to `main`, screening out secrets and junk files first. Manual invocation only (`/push`). |

### Tools and knowledge bases

| Skill | What it does |
|---|---|
| [abap-wiki](abap-wiki/) | Answers questions from the team's ABAP knowledge vault (standards, decisions, specs, WRICEF objects, runbooks), syncing the latest version from GitHub first and citing pages. |
| [langfuse](langfuse/) | Works with Langfuse (tracing, datasets, experiments, evaluations) and looks up its documentation. |
| [herdr](herdr/) | Controls Herdr, a terminal multiplexer for coding agents: panes, tabs, workspaces and other agents. Used only when Herdr is asked for by name. |

Skills with their own `README.md` explain setup and requirements there. For the rest, everything is in `SKILL.md`.
