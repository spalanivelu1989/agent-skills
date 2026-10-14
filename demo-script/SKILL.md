---
name: demo-script
description: Write, refine and fact-check the script for a demo or walkthrough video of an app, or of a slide deck or document narrated without an app — turn a user's rough step-by-step walkthrough (or a feature list) into a polished, timed script.md with on-screen actions, voice-over narration and a "Before recording" checklist, every label and claim checked against the app's code or the live app. Use when someone asks to write, refine, correct, proofread, tighten or check a demo script, video script, walkthrough script or narration, or says "here are my steps for a demo video — make it a script". Produces the script only; it does not record video (the script is ready to hand to a video-recording skill or to record by hand).
---

# Demo script

You turn a user's walkthrough into a **script.md** a person can read aloud while recording, or that a
recording tool can follow. The script is right in three ways:
- **Accurate:** every button, tab, field and message is named exactly as the app shows it, and every
  claim about what the app does is true.
- **Readable:** plain, spoken English for the audience, with no typos.
- **Timed:** the times come from the word count, not from guesses.

The worked example in `examples/fitgap/` shows a rough draft, the final script and the change list
from a real project. Read it before your first script.

## Workflow

### 1. Intake
Say you are ready and ask for the walkthrough if they have not given it. Before rewriting, get the
answers you can't infer, all in one message:
- **Audience:** business users, technical staff, or both.
- **Length:** the target duration, e.g. 2–3 minutes.
- **Role:** which account or role will be recorded. Role decides what is on screen: tabs, sidebar
  entries and buttons often differ for Admins.
- **Data:** what will be uploaded or entered, and whether it is real or synthetic.
- **Source:** a running app, or a slide deck or document with no app (see *Scripts without an app*).
- **Voice:** read by a person, or by the demo-video skill's Kokoro voice. This changes the timing (step 3).

Don't ask what the code can tell you.

### 2. Verify against the app
Work through `references/verification.md`. In short:
- Find the UI code, or open the live app read-only, and check **every label the draft names**:
  - buttons, tabs and section headings;
  - field names, placeholder text and status messages;
  - the URL and sign-in flow.
- Check **every claim about behaviour**. For example:
  - "compared against SAP Best Practices": is that always true, or only when a source is available?
  - "files are not stored": is that what the code does?
  - how long does it take?
  - is a button disabled while something runs?
  - what does each role see?
- Note the **preconditions** recording will need: a finished past run to load, a file on the
  Desktop, a field that holds a personal e-mail address.

Report label and behaviour differences as corrections. Never smooth one over silently.

### 3. Write the script
Use `templates/script.md`: a table of **#  |  On screen  |  Narration**, then **Before recording**.
- **On screen:** what to do, with exact labels in **bold**, file names in `code`, and on-screen
  status text in *italics*.
- **Narration:** spoken sentences in quotes. Aim for about 150 words a minute, one idea per sentence,
  and no jargon the audience wouldn't use. A URL is written as it should be said.
- Split a step into a/b rows when the screen action changes mid-narration (attach → processing).
  Add a *Pause* row when the user wants a beat between steps.
- **Before recording:** every precondition, setting and gotcha from step 2, as short labelled
  bullets.
- Fix grammar and wording, but keep the user's order and intent. Add only what a client video needs
  and the draft lacks, such as an intro, a close, or showing the results. Say what you added.

Then run the timing tool, and use its output, not your own estimate:
```bash
python3 ~/.claude/skills/demo-script/tools/timing.py path/to/script.md --write
```
On Windows, use `py` or `python` in place of `python3`.
It counts the narration words, adds time for on-screen actions and pauses, rewrites the
`(m:ss–m:ss)` times, and prints the total.

**When Kokoro will read it** (the demo-video skill), time it with `--wpm 130`. Kokoro's `af_heart`
voice at speed 1.0 is slower than the default 150 wpm. Measured on a 675-word script: 150 wpm
predicted 4:54, the voice rendered at 5:32, and `--wpm 130` predicts 5:36. At `"speed": 1.1` the same
voice rendered at 5:14 (`--wpm 143` predicts 5:07). Write to the target at 130 wpm, or say in the
delivery that the video will need speed 1.1.

### 4. Deliver
- Save the script where the user asks; otherwise use `docs/<topic>-demo-video-script.md`.
- In chat, show the script table, then:
  - **What I changed and why:** label corrections, behaviour corrections, additions, wording.
  - **Questions:** at most 3, only where the answer changes the script. Recommend a default for each.
- Give the length, and whether it is inside the target.

### 5. Edit rounds
The user will ask for many small changes: remove a sentence, reword a phrase, trim a section.
- Apply exactly what was asked. Show only the rows that changed, plus the new total from `timing.py`.
- If an edit breaks something else, point it out and offer the fix rather than applying it unasked:
  - an intro that no longer matches a section;
  - a closing line that refers to a cut step;
  - a claim that is now only true sometimes.
- When the target length is exceeded, say by how much and propose the single cut that fixes it.

### 6. Re-sync after recording (when asked)
Recording changes things: a step gets combined, a field is left empty, a pause is added, the timing
shifts. When the user asks to bring the script in line with the finished video, take the narration
word for word from what was recorded, and the times from the real scene lengths. Then list what
changed.

### Scripts without an app (slide decks, documents)
When the screen is a deck rather than an app, the script is the same table, but:
- **On screen** names the slide number and the element the cursor rests on (*Slide 6: point to
  **Diagnose**, then **Automate***), using the slide's exact wording.
- **Verify claims, not labels:** check every fact, name and number against its source document,
  and for a client-facing video against *public* sources (see `references/verification.md` §6).
- **What the viewer sees:** footers that cite internal material, speaker notes and presenter view
  must not appear. Say in Before recording how the slides will be rendered for the video.
- **Illustrative screens:** a recreated or mock screen is labelled on the slide *and* in the
  narration ("Here's an illustration").
- **Dated statuses:** availability labels (Limited Availability, GA) and "new" claims go in Before
  recording with "re-check before publishing".
- **Whose voice:** ask, or note, whether "we" and "us" mean the vendor or a partner. Avoid
  first-person vendor lines ("At Infor, we…") unless the user speaks for the vendor.
- **Names for the voice:** list the brand and product names the narration uses. Kokoro silently
  drops words outside its lexicon (in one video "Infor" came out as "within 4"), and the video skill
  should check them before recording.

## Rules
- **Accuracy over polish.** A wrong label or a promise the app doesn't keep is worse than an awkward
  sentence. When you can't verify a claim, hedge it ("where available") or ask.
- **Times come from the tool.** Re-run `timing.py` after every edit that touches narration.
- **Privacy.** Don't put credentials in the script. Flag on-screen personal data, such as a username
  or a "Deciding as" e-mail, in Before recording. Mark synthetic data as synthetic.
- **Writes.** If a step changes data (uploads, starts a run, submits), say so in Before recording,
  together with what each take leaves behind.
- **Client-facing claims.** Use only what the client could verify. Material from internal training
  decks or partner notes stays out of the narration, or is clearly marked and approved by the user.
- **The script is a file the user owns.** Don't commit or publish it without asking.

## Files
- `templates/script.md`: the output format.
- `references/verification.md`: what to check, and how to find it in code or the live app.
- `tools/timing.py`: word-count timings; `--write` updates the file, `--wpm` and `--action` tune it.
- `examples/fitgap/`: `draft.md` (the user's rough walkthrough), `script.md` (the final script) and
  `changes.md` (what changed and why, round by round).
