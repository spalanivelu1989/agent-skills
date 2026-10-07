---
name: demo-video
description: Produce a narrated, captioned demo or walkthrough video (MP4) of any running web app — screen recordings driven by Playwright, a natural open-source voice-over (Kokoro, local), captions, title and closing cards, with every screen action timed to the words that describe it. Starts from a finished script (e.g. a script.md with on-screen actions and narration), a brief, or meeting transcripts. Use whenever someone asks for a demo video, product or feature walkthrough, screen recording with voice-over, a video of an app's results, "record this script", or "turn this meeting / brief into a demo video" — even if they only say "record the app" or "make a video of the tool". Not for writing or refining a script on its own; that is a separate script-writing task.
---

# Demo video

You turn a running web app into a **narrated video**, 6–8 minutes by default, or whatever length the user's own script or brief sets (a 2–3 minute how-to is common). The video is reproducible from two files in the project:
- `scenes.json`: the story, voice-over, captions and cue phrases;
- `scenes.py`: what happens on screen at each cue.

The engine is in `engine/` and gets vendored into the project. Picture and voice stay in sync because the narration is generated first and every screen action waits for its cue phrase.

## Workflow

### 0. Brief (only if given transcripts, notes or a brief)
Read every source in full and synthesise it, following `references/storytelling.md`:
- the audience;
- the one thing they must believe;
- the order the requester wants;
- corrections made in the meeting;
- numbers to be quoted;
- open questions to answer in the story;
- estimates to avoid stating as facts.

Show the user the synthesis and a proposed storyline before building. If they gave no brief, ask what the video is for and who will watch it, unless the request already says so.

### 0b. Starting from the user's own script
When the user hands over a step-by-step script (e.g. a doc you refined together), it is the brief:
keep its wording and order, and map it to scenes.
- **Every scene runs in a fresh browser.** Steps that share page state (attach a file → fill the
  form → run → open the log) must be **one** app scene with many cues; split only where the next
  scene can rebuild its state before `mark()` (e.g. by reopening a saved record).
- Intro and closing lines become `"card"` scenes.
- Check every label the script names against the live app or the code; tell the user what differs.

### 1. Set up
```bash
python3 ~/.claude/skills/demo-video/engine/init.py <project>/docs/demo-video   # or wherever the user wants it
bash <dir>/tools/setup_tts.sh        # once per machine; skip if ~/.cache/demo-video-tts exists
```
Requirements:
- Python Playwright with Chromium in the user's normal Python (`python3 -c "import playwright"`);
- `ffmpeg`;
- `uv` and Python 3.10–3.12 for the voice.

Before installing anything missing, ask. If the project already has a video folder, create a new
one beside it rather than re-running `init.py` over someone else's video. Get the app's URL and sign-in from the user. Put credentials in env vars or `login()`, never in `scenes.json`
or any file; pass them on the command line each run (`DEMO_USERNAME='…' DEMO_PASSWORD='…' python3 …`,
single-quoted so a `$` in a password survives the shell).

### 2. Explore the app
Fill in `BASE_URL` and `login()` in `scenes.py`, then:
```bash
python3 <dir>/tools/explore.py /path/one /path/two --tabs
```
- Read the `pass1/*.txt` text dumps for the facts and exact numbers.
- Look at the stills to plan shots.
- Pick the richest single item for the end-to-end scene, plus two contrasting examples.

Check that sign-in really worked: `explore.py` warns when a password field is still on screen, and
the stills should show the app, not the login page.

Two cautions:
- Claude in Chrome is not needed; Playwright headless is more reliable here.
- Note anything sensitive on screen, such as model names, keys, personal names or internal hosts, for `"mask"`.

### 3. Write `scenes.json`
Scenes have one of two kinds:
- `"card"`: rendered from `cards`;
- `"app"`: recorded, and needs a function in `scenes.py`.

For each app scene, write:
- `caption`: under 90 characters;
- `screen`: a stage direction;
- `vo`: the voice-over, at about 150 wpm;
- `cues`: phrases from `vo`, in order, one per screen change.

Every number must match the screen. Also set:
- `output` and `title`;
- `pronounce` and `mask` as needed.

Then render the narration and read the lengths:
```bash
python3 <dir>/tools/voice.py
```

### 4. Write `scenes.py`
One function per app scene, named after its id: setup → `mark()` → `at("cue")` → action. Follow `references/scene-authoring.md`:
- find elements by visible text with `point`, `reveal` and `hover_text`, using `min_x` for side panels;
- do slow navigation before `mark()`;
- **never click anything that writes data** (save, submit, accept, delete). Hover it instead.

**When the story needs a write** (upload a file, start a run, stop it), ask first and say exactly
what each take leaves behind (a run in History, model spend, an upload) — then:
- time the slow part once **without** the expensive write (e.g. upload but don't run) and design
  the narration around it: start slow operations early so the voice covers the wait, and fill
  other fields while they process; use `wait_enabled()` before the next click;
- record the read-only scenes first and the write scene **last**, after the voice-over,
  pronunciation and pauses are final — any change to them marks every scene stale, and only a
  new take fixes a write scene (`build.py --allow-stale` speeds the old picture up to fit, so its
  actions land early: fine for a rough cut, not for a click the narration names);
- count takes against what the user approved; ask before going over;
- afterwards, offer to clean up what the takes left (list first, delete only the takes, and only
  when the user asks).

### 5. Record, build, check
```bash
python3 <dir>/tools/record.py            # all app scenes; or name some. Prints late cues.
python3 <dir>/tools/build.py             # MP4 + script.md
python3 <dir>/tools/check.py             # transcript diff, phonemes, late cues, contact sheets, leaks
```
**Look at every contact sheet** in `clips/_check/<scene>.png`. Each frame is 1.5 s after a cue and must show what that cue says.

Then fix and re-run:
- late cues or mismatched frames → edit `scenes.py`, re-record that scene;
- transcript differences → change the wording, or add a `pronounce` rule;
- leaks → add `mask` patterns.

You cannot hear the audio. The transcript diff and phonemes are your ears, so say so to the user and ask them to listen once.

### 6. Deliver
Tell the user:
- the MP4 path and length;
- what was verified, and how;
- the voice used, with an offer of alternatives. Render 20-second samples in 4–5 Kokoro voices (`af_heart`, `af_bella`, `am_michael`, `bf_emma`, `bm_george`) if they want to choose;
- anything not in the video, such as tabs to show live;
- anything they must act on, e.g. "the live app still shows the model name".

Fill in the project `README.md` "Things to know" section. Don't commit, publish or upload without asking.

## Changing things later
| Change | Re-run |
|---|---|
| Caption or card text | `build.py` |
| Voice-over wording, cues, voice, speed, pronunciation | `record.py <scenes>` then `build.py` (the timing follows the voice) |
| Screen actions | `record.py <scene>` then `build.py` |
| Engine upgrade | `init.py <dir>` again (keeps `scenes.*` and README) |

A beat between two steps: `"pauses": {"<cue>": 2.0}` on a scene puts that much silence before
the cue is spoken (use it when the user says the voice "jumps" from one step to the next). It only
changes that scene's voice key.

Scene changes are straight cuts. The build never fades to or from black — not between scenes and
not at the start or end — because users see the dip as a flicker. Don't add one back; `check.py`
reports any black stretch over 0.2 s as a fault.

Voice options:
- `VOICE=bf_emma`, `am_michael` and others;
- `VOICE_SPEED=0.95`;
- `TTS=say VOICE=Daniel` for the macOS voice;
- `VOICE=` for a silent cut.

## Rules
- **Read-only.** The video must not change the app's data. If a flow can only be shown by writing data, stop and ask.
- **Honest content.** Label synthetic data as synthetic. Mark estimates as estimates. Quote numbers exactly as computed. Keep corrections from the brief.
- **Privacy.** Mask model names and secrets. `"mask"` only rewrites text nodes, so hide values in
  input fields with CSS (`-webkit-text-security: disc` for a sign-in username, `color: transparent`
  for a pre-filled "your name" box); `check.py` flags any e-mail address left in page text or inputs
  (approve one with `"allow_emails"`). No real people's names unless approved. Credentials only in env vars or `login()`.
- **Verify before claiming.** Run `check.py` and read the contact sheets before saying the video is in sync.

## Files
- `engine/`: `init.py`, `demo.py` (scene helpers), `voice.py`, `record.py`, `build.py`, `check.py`, `explore.py`, `kokoro_say.py`, `tts_inspect.py`, `setup_tts.sh`.
- `templates/`: starting `scenes.json`, `scenes.py`, `README.md`.
- `references/storytelling.md`: brief → story → voice-over.
- `references/scene-authoring.md`: cues, helpers, pronunciation, masking.
- `references/troubleshooting.md`: known failures and fixes.
- `examples/solvay-fitgap/`: a complete real example, a 10-scene, 6:20 video of a fit-gap analysis tool.
- `examples/fitgap-quickstart/`: a 2:28 how-to built from the user's own script: a sign-in scene (username hidden), one long scene that uploads a file, runs, opens the log, stops and loads a past run (a write flow, approved), a pause before a step, and a field hidden with CSS.
