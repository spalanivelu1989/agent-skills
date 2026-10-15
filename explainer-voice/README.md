# Explainer voice

A Claude Code skill that gives Claude one house writing voice for anything it writes in prose: answers, explanations, docs, READMEs, reports and emails. The style is a long-form science-magazine explainer. It opens on a concrete moment and unfolds the idea by progressive disclosure: the problem, why the obvious fix fails, the insight, the mechanism, then the open question. One running example is carried from start to finish, and every abstraction gets a mental image.

The voice scales with the reply. A one-line status update just gets plain words with the point first; a long explanation gets the full arc. It never touches code or commit messages, and when another skill fixes the format (a demo script, slides, a podcast), that skill's rules win.

## Install

```bash
cp -r explainer-voice ~/.claude/skills/
```

To make it the default for every reply, add this to `~/.claude/CLAUDE.md`:

```markdown
# Writing voice
- **explainer-voice** (`~/.claude/skills/explainer-voice/SKILL.md`): the house style for all prose output.
Whenever a reply or document contains more than a few sentences of prose, invoke the Skill tool with `skill: "explainer-voice"` first (once per session is enough) and write in that voice, scaled to the reply's length.
```

## Use

Once it's in `CLAUDE.md`, there is nothing to do. To use it on demand instead, ask for it, for example:

```text
Explain how our retry logic works, in the explainer voice.
```

## Files

| Path | What it is |
|---|---|
| `SKILL.md` | The arc, sentence-level craft, scaling rules and a pre-send checklist |
| `references/examples.md` | Before-and-after rewrites: a short answer, a long doc, a status reply, a closing paragraph |
