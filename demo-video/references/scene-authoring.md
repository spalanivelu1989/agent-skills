# Writing scenes that stay in step with the voice

## How the timing works
1. `voice.py` splits each scene's `vo` at its `cues`, speaks every part separately, and records when each cue starts. Parts are cached in `clips/_voice/`.
2. `record.py` opens a fresh browser per scene and runs your function. `mark()` says the content is on screen; the voice starts 0.6 s later. `at("cue")` waits until 0.35 s before that cue is spoken, so the screen lands as the words do.
3. The recording runs until the voice ends plus 1.2 s. `build.py` trims everything before `mark()` and lays the audio under it at 1×.

If an action takes longer than the gap to the next cue, `record.py` prints `… late for '<cue>'` and `check.py` reports it. The fixes:
- do the slow part (navigation, opening a modal) **before** `mark()` or earlier in the scene;
- remove steps;
- move the cue later in the sentence.

## Choosing cues
- Use a cue for every moment the screen must change: a new card pointed at, a panel scrolled to, a row opened.
- Make each cue a phrase that appears **once** in that scene's `vo`, in order. Its first words are enough, e.g. `"Hover the score"`.
- Busy scenes need 6–11 cues; simple ones need 2–3.
- Between cues, keep the screen alive with small `point` moves rather than long holds.

## Helpers (`from demo import *`)

| Helper | Use |
|---|---|
| `settle(pg, s=1)` | After `goto` or any navigation: waits for the network to go quiet, then `s` seconds. |
| `point(pg, "Text", min_x=0, max_x=None, dx=0, dy=0)` | Glides the visible cursor to the smallest element whose text **starts with** "Text" (case-insensitive). |
| `reveal(pg, "Text", min_x=…, offset=140)` | Smooth-scrolls that element to near the top of *whatever pane scrolls it*. Use it for side panels and inspectors. |
| `hover_text(pg, "51.3")` | A real hover, which opens tooltips. |
| `click(pg, locator, pause=0.6, look=0.25)` | Scrolls into view, glides, then clicks. **Navigation only.** Raise `look` (≈1.0) to rest on a button the narration names before pressing it. |
| `to(pg, locator)` | Glides onto a locator (ids, roles, inputs with no text for `point`). |
| `type_into(pg, locator, text, delay=35)` | Clicks a field and types visibly. Only fields that aren't saved on their own. |
| `wait_enabled(pg, locator, timeout=40)` | Waits for a button to enable, e.g. Run after an upload is processed. |
| `tab(pg, "Label")` | Clicks an ARIA tab. |
| `wheel(pg, x, y, dy, seconds)` | Smooth wheel scroll under the pointer. Use it when there's no good text anchor. |
| `glide(pg, x, y)` | Raw cursor move. Last resort; pixel positions break when the layout changes. |
| `still(pg, "name")` | Full-resolution PNG to `captures/` for slides. |

Tips for these helpers:
- **Same text in two places, e.g. a table and a detail panel:** restrict by position with `min_x` or `max_x`. For example, `min_x=W*0.7` targets a right-hand inspector.
- **Labels styled in capitals:** case doesn't matter, because matching is on `textContent`.
- **A missing element:** prints a warning and the scene carries on. Read the warnings.

## Recipes

**Sign-in scene.** `record.py` reuses the signed-in session, so start the scene logged out and
hide the username like the password:
```python
def s02_signin(pg, mark, at):
    pg.context.clear_cookies()
    pg.goto(f"{BASE_URL}/login")
    settle(pg, 1)
    pg.add_style_tag(content="#username{-webkit-text-security:disc}")   # a real address on screen
    mark()
    at("Enter the username")
    type_into(pg, pg.locator("#username"), os.environ["DEMO_USERNAME"], delay=30)
    type_into(pg, pg.locator("#password"), os.environ["DEMO_PASSWORD"], delay=60)
    at("then click Sign in")
    click(pg, pg.locator('button:has-text("Sign in")'), 0.2)
    pg.wait_for_url("**/home")
```
Headless Chromium has **no address bar and no file picker** on screen: put the URL in the
caption, and say the file name in the voice-over.

**Uploading a file.**
```python
attach = pg.locator('button:has-text("Attach")')
to(pg, attach)
with pg.expect_file_chooser() as fc:
    attach.click()
fc.value.set_files(os.path.expanduser("~/Desktop/example.txt"))
```
Time the processing once beforehand (poll the page text for its status lines); if it outlasts the
narration, start it on an earlier cue and do other things (fill the form) while it runs.

**A button in the page header after scrolling down.** `click()` scrolls it into view, but the
jump is abrupt: `reveal()` the header first, then `to()` the button, `hold(pg, 1)`, `click()`.

**A drawer that should stay readable.** After opening it, give it a second or two (`wheel` inside
it) before the next cue closes it with `pg.keyboard.press("Escape")`.

**Values in input fields.** A pre-filled "your name" box can hold the user's e-mail. `mask` does
not reach input values: `pg.add_style_tag(content="#reviewer{color:transparent!important}")`.

## Shape of a scene
```python
def s05_detail(pg, mark, at):
    open_record(pg, "ORD-1042")          # slow setup BEFORE mark()
    tab(pg, "Details")
    mark()
    still(pg, "s05_top")
    at("The comparison puts")
    reveal(pg, "Comparison", min_x=1400, offset=110)
    at("India: four approval tiers")
    point(pg, "Country As-Is", min_x=1400, dx=40, dy=30)
    at("Every claim is quoted")
    reveal(pg, "Evidence", min_x=1400)
```
Put shared navigation (sign-in, opening a record) in plain functions in `scenes.py`.

## Rules
- **Read-only:** never click save, submit, accept, approve, reject, delete, send or publish. Hover them while the voice says what they do. If a flow can't be shown without writing data, ask the user first.
- **Masking:** `scenes.json` `"mask"` lists JavaScript regex sources stripped from every text node as the page renders. Use it for model names, API keys, emails and internal hostnames, anything the client shouldn't see. `check.py` scans the recorded pages' text for leftovers.
- **Personal names:** no real people's names on screen beyond what the user approved. Roles are fine.
- **The `"card"` kind:** a scene of kind `"card"` is rendered from `scenes.json` `cards`; no function is needed.

## Pronunciation
- Kokoro spells most capitalised acronyms letter by letter by itself, e.g. IRN, GST, ITC, BKP2.
- Some acronyms are real words, so Kokoro says them as words, e.g. SAP becomes "sap". Fix these with `"pronounce": {"kokoro": [["\\bSAP\\b", "S-A-P"]]}`.
- Hyphenated letters such as `S-A-P` and `L-2-C` force letter-by-letter reading.
- Codes like `GAP-IN-RET-01` should become what a person would say: `["GAP-IN-RET-0?(\\d+)", "gap \\1"]`.
- **Check a word before changing the script.** `check.py`'s transcript comes from Whisper, which mishears too ("e-invoicing" → "invicing"). Ask misaki directly; `❓` means Kokoro will drop the word, anything else means it is said, and a Whisper-only difference goes in `check_ignore`:
  ```bash
  KPY=$(python3 -c "import sys;sys.path.insert(0,'tools');import voice;print(voice.KOKORO_PY)")
  echo '{"phonemes":["e invoicing","ivolve","[ivolve](/ˈIvɑlv/)"]}' | "$KPY" tools/tts_inspect.py
  ```
- A URL in the voice-over needs a rule that says it the way a person would: `["example-app\\.acme\\.cloud/demo", "example app dot [acme](/ˈækmi/) dot cloud slash demo"]`.
- `check.py` prints each acronym's phonemes. A word-like reading such as `sˈæp` means a rule is needed.
- **Unknown words are dropped silently.** Kokoro skips words outside its lexicon: company names, product names, compounds like "watchlist". `check.py` lists every one. Give a name a phonetic spelling (`[Solvay](/sˈɑlvA/)`; misaki IPA uses `A` = "ay", `I` = "eye", `O` = "oh") and split a compound into words.
- **Rule order:** rules apply in order, and never inside a `[word](/…/)` span an earlier rule produced. Put a possessive (`Solvay's`) before the base word.

## Caption bar
Every app scene has a 92 px caption bar along the bottom. Keep what the narration is talking about above y ≈ 980. For example, `reveal(pg, "Flags", offset=140)` puts the section near the top of its pane, not at the bottom edge.
