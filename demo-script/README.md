# Demo script

A Claude Code skill that turns a rough step-by-step walkthrough, or a feature list, into a polished, timed **script.md** for a demo or walkthrough video.

The script is a table of **#  |  On screen  |  Narration** followed by a **Before recording** checklist. The skill checks every button, tab and field label, and every claim about what the app does, against the app's code or the live app. It reports any difference as a correction. Times come from a word-count tool, not guesses.

The skill writes the script only; it does not record. Hand the finished script to [`demo-video`](../demo-video/), or record it by hand.

## Install

```bash
cp -r demo-script ~/.claude/skills/
```

Requirements: Python 3 (for the timing tool).

## Use

Paste your walkthrough and ask Claude Code, for example:

```text
Here are my steps for a demo video — make it a script. Business audience, 2–3 minutes.
```

Claude asks for anything it can't infer (audience, target length, the role being recorded, real or synthetic data). It then verifies the labels and claims, writes the script and times it. It shows what it changed and why, plus at most three questions. After that, ask for small edits ("cut the second sentence in step 4"); each round shows only the rows that changed, with the new total length.

To re-time a script yourself after editing the narration:

```bash
python3 ~/.claude/skills/demo-script/tools/timing.py docs/my-demo-script.md --write
```

## Files

| Path | What it is |
|---|---|
| `SKILL.md` | Full workflow and rules |
| `templates/script.md` | The output format |
| `references/verification.md` | What to check, and how to find it in the code or the live app |
| `tools/timing.py` | Word-count timings (`--write`, `--wpm`, `--action`) |
| `examples/fitgap/` | A real rough draft, the final script and the round-by-round change list |
