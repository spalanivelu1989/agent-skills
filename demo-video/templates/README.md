# Demo video

<!-- One paragraph: what the video shows, for whom, what stays live in the meeting. -->

| File | What it is |
|---|---|
| `demo-video.mp4` | The narrated, captioned video (gitignored; rebuild with the commands below). |
| `script.md` | Timed narration, one section per scene. Generated; edit `scenes.json` instead. |
| `scenes.json` | The story: scenes, captions, voice-over, cue phrases, cards, pronunciation, masks. |
| `scenes.py` | One function per app scene: what happens on screen at each cue. |
| `captures/` | Full-resolution stills of key moments, for slides. |
| `tools/` | The demo-video engine (from the `demo-video` skill; refresh with its `init.py`). |

## Regenerating

```bash
bash tools/setup_tts.sh          # once per machine: local Kokoro voice + Whisper
python3 tools/voice.py           # narration + cue times (cached)
python3 tools/record.py          # screen recordings timed to the narration; or name scenes
python3 tools/build.py           # MP4 + script.md
python3 tools/check.py           # transcript diff, late cues, contact sheets, leaks
```

- **Caption or card change:** run `build.py` only.
- **Voice-over, cues or voice change:** re-record the affected scenes, then build.

## The voice

Kokoro-82M (open source, Apache 2.0) runs locally; nothing is sent to a service.

- **Other voices:** `VOICE=bf_emma` / `am_michael` / `bm_george`.
- **Pace:** `VOICE_SPEED=0.95`.
- **macOS voice:** `TTS=say VOICE=Daniel`.
- **Silent cut:** `VOICE=`.

After changing any of these, re-record, then build.

## Things to know

<!-- Data written or not, what was masked and why, what is synthetic, what is not in the video. -->
