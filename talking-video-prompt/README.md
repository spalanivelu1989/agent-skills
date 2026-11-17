# Talking video prompt

A Claude Code skill that writes ready-to-paste prompts for AI video generators: a presenter looks
at the camera and speaks a short script, with lip sync, timed pauses, gestures tied to specific
words, and a call to action. It's built for 8–15 second teasers that promote a blog post or
feature.

It writes the script from the source (a hook, a one-line answer, a call to action), times it at
about 2.5 words per second plus pauses, ties gestures to props in your starting image, and adds
the lines that keep text steady and stop the model rushing the dialogue.

## Install

```bash
cp -r talking-video-prompt ~/.claude/skills/
```

## Use

```text
/talking-video-prompt for the Semantic Model vs Ontology post, under 10 seconds, using the whiteboard photo
```

Or: "write a video prompt like this one for my other post", then "make it shorter".

## Files

- `SKILL.md`: inputs, script formula, timing table, prompt template, rules and checks.
