# Demo video

A Claude Code skill that produces a **narrated, captioned demo video (MP4)** of any running web app.

Playwright drives the screen recordings. A natural open-source voice (Kokoro) runs locally for the voice-over, so nothing is sent to a service. The video gets captions plus title and closing cards. Each screen action waits for the phrase in the narration that describes it, which keeps picture and voice in sync. You can start from a finished script (for example one from [`demo-script`](../demo-script/)), a brief or meeting transcripts.

Two files in your project make the video reproducible: `scenes.json` (story, voice-over, captions, cue phrases) and `scenes.py` (what happens on screen at each cue).

## Install

```bash
cp -r demo-video ~/.claude/skills/
```

Requirements: Python Playwright with Chromium, `ffmpeg`, and `uv` with Python 3.10–3.12 for the voice. Claude asks before installing anything missing.

## Use

With the app running, ask Claude Code, for example:

```text
Record this script as a demo video: docs/quickstart-demo-script.md — app at http://localhost:5173
Turn these meeting notes into a 6-minute demo video of the tool
```

Claude sets up a video folder, explores the app, writes the scenes, records and builds the video, then checks the result. The video is read-only by default: Claude asks before any step that writes data, such as an upload or a run. Pass credentials as environment variables; they never go in a file.

## Commands

```bash
python3 ~/.claude/skills/demo-video/engine/init.py docs/demo-video   # vendor the engine into a project
bash docs/demo-video/tools/setup_tts.sh    # once per machine: local voice + Whisper
python3 docs/demo-video/tools/voice.py     # narration + cue times
python3 docs/demo-video/tools/record.py    # screen recordings (or name scenes)
python3 docs/demo-video/tools/build.py     # MP4 + script.md
python3 docs/demo-video/tools/check.py     # transcript diff, late cues, contact sheets, leaks
```

After a caption change, run `build.py` only. After a voice-over or screen-action change, re-record the affected scenes, then run `build.py`. Change the voice with `VOICE=bf_emma` or `VOICE_SPEED=0.95`.

## Files

| Path | What it is |
|---|---|
| `SKILL.md` | Full workflow and rules (read-only, privacy, verify before claiming) |
| `engine/` | Recording, voice, build and check tools, copied into each project by `init.py` |
| `templates/` | Starting `scenes.json`, `scenes.py` and project `README.md` |
| `references/` | Storytelling, scene authoring (cues, masking, pronunciation) and troubleshooting |
| `examples/` | A 10-scene, 6:20 video and a 2:28 how-to built from a user's script |
