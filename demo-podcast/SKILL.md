---
name: demo-podcast
description: Produce a narrated, multi-host podcast episode (MP3 with chapter markers) from project knowledge — documents, slide decks, guides, verified facts, meeting notes — voiced locally with open-source TTS — by default a hybrid of Chatterbox (expressive, human-sounding) and Kokoro (fast, clean), each host in a different voice. Writes the two-host conversation script, fixes pronunciation before rendering, renders and times the audio, checks it with Whisper speech-to-text, encodes a loudness-normalised MP3 and can play it. Use whenever someone asks for a podcast, an audio episode, an audio overview, a "two people talking about X" conversation, a listenable briefing, or to "turn this deck / guide / research into a podcast", for any project or topic. Not for screen-recorded demo videos (use demo-video) or for writing a video script on its own (use demo-script).
---

# Demo podcast

You turn what a project knows into a **conversation two (or more) hosts have out loud**, rendered
locally, each host in their own voice. The default is the **hybrid** engine: the listener's stand-in
on Chatterbox with the saved `@heart_expressive` voice (warm, energetic, human), the specialist on
Kokoro `am_fenrir` (lively and clean). Users have rejected flat voices ("dull and robotic"); this
pair is the one a user chose by ear after hearing seven options. The episode is reproducible from
two files:
- `podcast.json`: title, hosts and voices, speed, pauses, pronunciation rules;
- `podcast-script.md`: chapters (`## `), turns (`NAME: line`) and pauses (`[pause N]`).

`tools/podcast.py` does everything else: `init`, `estimate`, `phonemes`, `render`, `retake`, `check`,
`encode`, `play`. `examples/infor-summit-v2/` is the finished 30.4-minute, 12-chapter hybrid episode
(energetic discovery style); `examples/infor-summit/` is an earlier, calmer all-Kokoro version.

| Engine (`"engine"`) | Sound | 30-min render (Apple Silicon) |
|---|---|---|
| `hybrid` (default) | Chatterbox host sounds human and excited; Kokoro host clean | ~10 min per 10 min of Chatterbox speech (≈45 min for a 30-min episode where she has ~30 % of the words) |
| `kokoro` (`init --kokoro`) | Clean, a little flat | ~4 min |
| `chatterbox` | Both hosts expressive | ~2–2.5 h |

## Workflow

### 1. Brief
Get these, in one message, unless the request already answers them:
- **Audience and use:** internal enablement, or shared with clients? Client-facing raises the bar on facts (step 2).
- **Length:** e.g. 10, 20 or 30 minutes.
- **Hosts:** how many, and their roles. The default pair works well: a **listener's stand-in** who asks
  what the audience would ask, and a **specialist** who answers plainly. Hosts are fictional names.
- **Voices:** default hybrid pair: MAYA = Chatterbox `@heart_expressive`, SAM = Kokoro `am_fenrir`.
  If the user wants to choose, or dislikes a voice, render a **sampler** (step 5b) rather than
  describing voices. If time matters more than expressiveness, offer `init --kokoro`.
- **Sources:** which documents, decks, guides or verified fact lists are the source of truth.

### 2. Gather the facts
Read every source in full. Build the episode from **verified** facts only:
- If the project already has a fact-check (a verification appendix, a public-sources table), use it.
  Otherwise, check each number, name and capability against its source, and for a client-facing
  episode against public sources.
- Keep internal-only material (training decks, partner pricing, unverified figures) out of a client
  episode. Attribute vendor claims ("Infor positions them as the only…"). Label illustrations.
- Note statuses that change (availability, counts, prices) and say them with a date.

### 3. Write the script
Follow `references/writing.md`. In short:
- **Budget words, not minutes:** about **145 words per minute** of episode with `hybrid`, **130** with
  `kokoro` (`podcast.py estimate` checks it). A 30-minute hybrid episode is about 4,300–4,400 words.
- **Chapters of about 3 minutes**, each a `## ` heading; a welcome with the AI-voice disclosure; a wrap-up
  that summarises and gives the listener one question or next step.
- **Turns of one to four sentences**, alternating; `estimate` prints each host's share of the words.
- **Energy:** write a discovery conversation, not a lecture: reactions, repeat-backs, the stand-in
  pushing back, `(excited)` / `(calm)` tags, the odd `[overlap]`. See `references/writing.md`.
- **No one- or two-word lines for a Chatterbox host** ("Been there.", "And?", "Ninety-five!"):
  Chatterbox repeats or invents words on them. Give each at least three or four words.
- **Write for the ear:** numbers in words ("ninety-eight percent", "twenty twenty-six"), acronyms
  hyphenated when they are spelled out ("R-P-A", "C-I-O"), no tables, no URLs, no parentheses.

```bash
python3 ~/.claude/skills/demo-podcast/tools/podcast.py init <dir>      # templates
# write <dir>/podcast-script.md and <dir>/podcast.json
python3 ~/.claude/skills/demo-podcast/tools/podcast.py estimate <dir>
```

### 4. Fix pronunciation before rendering
```bash
python3 ~/.claude/skills/demo-podcast/tools/podcast.py phonemes <dir>
```
Kokoro **guesses words outside its lexicon**, marked ❓: sometimes well ("observability"), often badly for
brand and product names ("Infor" came out as "within 4"), and it reads some acronyms as words ("OS" →
"oss", "IT" → "it"). Add a rule to `podcast.json` for every ❓ name (ordinary ❓ words can instead be
confirmed by the transcript check),
following `references/voices-and-pronunciation.md`, and re-run until it prints "Ready to render".
Doing this before the render saves a full re-render.

### 5. Render and time
```bash
bash ~/.claude/skills/demo-podcast/tools/setup_chatterbox.sh          # once per machine, for hybrid
python3 ~/.claude/skills/demo-podcast/tools/podcast.py render <dir>    # run in the background
```
Run it in the background and watch its progress lines (`n/N  MAYA (…)`) with a monitor; tell the user
the expected time up front. Hybrid caches every turn in `<dir>/cache`: after a script edit, `render`
again re-renders only the changed turns and re-assembles in seconds. Read the `TOTAL` line. If it
misses the target, add or cut lines (or change Kokoro `"speed"`, 0.9–1.1), then render again.

### 5b. Voice sampler (when the user wants to choose, or dislikes a voice)
Render the same 15–20 seconds (two lines from the disliked host around one reply from the other) in
five to seven candidate voices, each introduced by the other host ("Option one."), into one MP3,
and open it. Include Chatterbox options (its built-in voice, `@heart_expressive`) as well as Kokoro
ones; measure each candidate's pitch variety and transcript (see "Energy" in
`references/voices-and-pronunciation.md`). Let the user pick by number. Don't keep tuning a voice
the user has said they dislike: a flat Kokoro voice stays flat underneath even when boosted.

If the user says a host sounds dull or flat, measure that host's pitch variety and lift it with a
voice blend and `"pitch_expand"` (see "Energy" in `references/voices-and-pronunciation.md`) rather
than swapping to a lower-quality voice. Give them a short before/after clip as well as the episode.

### 6. Check (and retake)
```bash
python3 ~/.claude/skills/demo-podcast/tools/podcast.py retake <dir>   # hybrid: per-turn check + retakes
python3 ~/.claude/skills/demo-podcast/tools/podcast.py check <dir> --clips
```
`retake` transcribes every Chatterbox turn on its own, renders failing turns again with new seeds
(up to three), keeps the best take and re-assembles. In the Infor episode 14 of 132 turns needed it
(a repeated phrase, an added "Well,", "Emmy candidates"); 10 were fixed by a new seed, and the
remaining four were one- or two-word lines that needed a few more words in the script.
Whisper transcribes the whole episode and compares it with the script; number formats, spelling and
compound-word differences are filtered out. `--clips` re-transcribes each suspect turn on its own. A
turn that comes back right on its own was a Whisper slip, not an audio fault. You cannot hear the
audio: say so, and ask the user to listen once.

### 7. Encode, play, deliver
```bash
python3 ~/.claude/skills/demo-podcast/tools/podcast.py encode <dir>    # MP3, -16 LUFS, chapters
python3 ~/.claude/skills/demo-podcast/tools/podcast.py play <dir>      # QuickTime, if asked
```
Tell the user:
- the MP3 path and length, and a chapter table (time · title);
- the hosts, their voices and roles, and that the voices are disclosed as AI-generated;
- what was verified and how (facts and their sources, pronunciation, transcript check);
- caveats the content carries (statuses to re-check before sharing);
- the files: the MP3, `podcast-script.md` (editable), `podcast.json`, `build/`.

## Rules
- **Disclose AI voices** in the welcome (Chatterbox also adds Resemble's inaudible Perth watermark
  marking its audio as AI-generated; say so when you deliver). Hosts are fictional; never imitate a real person's voice or
  name a real person as a host.
- **No impersonation:** hosts talk *about* a company ("Infor says…"), not *as* it ("At Infor, we…"),
  unless the user speaks for that company and asks for it.
- **Honest content:** sourced numbers exactly as published; attribute claims; label illustrations
  and estimates; date anything that changes.
- **Reference voices:** only the saved `voices/` clips, Kokoro-made clips, or Chatterbox's built-in
  voice. Never clone a real person's voice from a recording.
- **Pronunciation before render;** the transcript check after. Never claim it sounds right without
  the check, and never claim to have listened.
- **Don't publish or upload** the episode anywhere without asking.

## Files
- `tools/podcast.py`: the command line (system `python3` + `ffmpeg`).
- `tools/_kokoro_worker.py`: render, phonemes and transcribe, run inside the Kokoro environment
  (voice blends `af_bella:0.6+af_kore:0.4` and `pitch_expand`).
- `tools/_hybrid.py`: per-host engines, per-turn cache, assembly with natural gaps and `[overlap]`.
- `tools/_chatterbox_worker.py`: the all-Chatterbox engine.
- `tools/setup_tts.sh`: one-time setup of Kokoro + Whisper at `~/.cache/demo-video-tts` (shared with demo-video).
- `tools/setup_chatterbox.sh`: one-time setup of Chatterbox at `~/.cache/demo-podcast-chatterbox`.
- `voices/heart_expressive.wav`: the saved reference clip for the default Chatterbox host (`"reference": "@heart_expressive"`).
- `templates/`: `podcast.json` (hybrid preset), `podcast.kokoro.json` (`init --kokoro`) and `podcast-script.md`.
- `references/writing.md`: structure, host roles, turn writing, writing for the ear, fact handling.
- `references/voices-and-pronunciation.md`: voices, pacing data, rules and verified phonetic spellings.
- `references/troubleshooting.md`: known failures and fixes.
- `examples/infor-summit-v2/`: the finished hybrid episode the user approved (config + script).
- `examples/infor-summit/`: the earlier all-Kokoro episode (config + script).
