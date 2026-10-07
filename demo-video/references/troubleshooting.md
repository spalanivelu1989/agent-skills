# Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Claude in Chrome says "Browser extension is not connected" | The extension isn't running or isn't signed in | Don't wait for it. The engine uses Playwright headless, which is more reliable for fixed 1920×1080 captures and records video natively. |
| Login form submits but the URL never changes | The app redirects from the client after the API call | In `login()`, `pg.wait_for_url(...)` for the post-login URL; don't use `networkidle`. |
| `scrollHeight` of the document is the viewport height and nothing scrolls | The page scrolls inside a container | Use `reveal()` or `wheel()`; they find the scrolling pane. `explore.py` finds the largest scroller itself. |
| Kokoro fails with `Can't find model 'en_core_web_sm'` | spaCy's English model can't auto-install into a `uv` environment, which has no pip | Run `setup_tts.sh`; it installs the wheel directly. |
| Kokoro import error on Python 3.13 or 3.14 | Kokoro supports Python 3.10–3.12 | `setup_tts.sh` picks python3.12, 3.11 or 3.10. On macOS, `brew install python@3.12`. |
| SAP comes out as "sap" | Kokoro reads real words as words | Add a `pronounce` rule: `S-A-P`. |
| `check.py` reports GST → "GSD" | Whisper mishears a soft T. Kokoro's phonemes for GST are `ʤˌiˌɛstˈi`, which is right. | Add `["gst", "gsd"]` to `check_ignore`. Always confirm with the printed phonemes before ignoring. |
| A whole scene drifts: the tooltip appears before the words | It was recorded with fixed holds, or recorded before the voice changed | Re-record that scene. `check.py` lists scenes "recorded without the current voice". |
| `… late for '<cue>'` | Navigation or animation takes longer than the gap between cues | Move slow setup before `mark()`, drop steps, or move the cue later in the sentence. |
| Dead air at the end of scenes | The scene length came from `dur`, not from the voice, i.e. a silent build or an old engine | With a voice, the length is always voice + 1.8 s. Check `VOICE` isn't empty. |
| Frame grabs or `check.py` show black | Something rendered black: a page still loading at `mark()`, a missing card PNG, or an old build that faded between scenes | Settle the page before `mark()`; rebuild with the current `build.py` (straight cuts, no fades). |
| `ffmpeg` has no `drawtext` filter | The Homebrew ffmpeg was built without freetype | Captions and cards are rendered as PNGs with Playwright and overlaid, so drawtext isn't needed. |
| Model name visible, e.g. "model claude-…" | The app shows it even in demo mode | Add the regex to `"mask"`. Also tell the user, because the live app still shows it. |
| zsh: `defining function based on alias` | A shell function name clashes with an alias, e.g. `g` | Do helper work in a Python heredoc instead of shell functions. |
| A grep "hangs" for minutes | An empty `$(…)` file list made grep read stdin | Quote and guard file lists, or use the Grep tool. |
| `check.py` lists **words Kokoro cannot pronounce** (a `❓` in its phonemes) | The word isn't in Kokoro's lexicon: names (Solvay), compounds (watchlist, workstream). They are **silently dropped**, e.g. "Solvay's" became "s". | Names: a phonetic rule, `["\\bSolvay\\b", "[Solvay](/sˈɑlvA/)"]`. Compounds: split them, `["\\bwatchlist\\b", "watch list"]`. Put a possessive's rule (`Solvay's`) before the base word's. |
| A name is "heard" as a common word ("Solvay" → "solve") even after fixing it | Whisper doesn't know the name either | `check.py` already gives Whisper the script's names and acronyms as a vocabulary prompt. If a name still differs, check its phonemes, then listen. |
| Hyphenated compounds slur ("go-live" → "goal-live", "low-risk" → "lurisk") | Kokoro runs the parts together | Rules such as `["\\bgo-live\\b", "go live"]`. |
| `build.py` stops: "recording was not made against the current voice-over" | The voice-over, cues, voice or pronunciation changed after the scene was recorded, so the picture timing is wrong | Re-record those scenes. `build.py --allow-stale` makes a rough cut by squeezing the old picture. |
| `record.py`: "The app is not reachable" | The app or its tunnel is down | Start it and re-run. Nothing was recorded, and the previous clips are untouched. |
| Contact-sheet frames are blank | A `set_content` page can't load `file://` images | Fixed: `check.py` writes the sheet as an HTML file beside the frames. |
| Something important sits behind the caption bar | Captions cover the bottom 92 px of every app scene | Use `reveal(..., offset=…)` to keep key content above y ≈ 980, or shorten the scroll. |
| `explore.py` stills show the login page; `login()` raised nothing | `wait_for_url` matched the login page itself: `r".*/demo.*"` matches `/demo/login?next=/demo` | Wait for a URL only the signed-in app has (`**/demo/home`). `explore.py` now warns when a password field is still visible. |
| A click happens but the viewer never sees the cursor reach the button | The button was scrolled off screen; the glide went to off-screen coordinates | Fixed in `click()` (scrolls into view first). For header buttons, `reveal()` the header, then `to()` + `hold(pg, 1)` before clicking. |
| The user's e-mail address is visible in a form field | `mask` rewrites text nodes, not input values | Hide the field's value with CSS (`color: transparent`, or `-webkit-text-security: disc`). `check.py` flags e-mail addresses in page text and inputs. |
| After a pronunciation fix every scene is "not recorded against the current voice-over" | The voice key covers pronunciation for all scenes | Re-record the read-only scenes. For a scene that writes data, decide with the user: a new take, or `--allow-stale` if its audio did not change (the picture is sped up to fit, so check that clicks still land on their words). Finalise the voice before recording write scenes. |
| The voice runs from one step straight into the next | Cue parts are joined with no gap | `"pauses": {"<cue>": 2.0}` on the scene. |
| A Run button is still disabled when its cue arrives | An upload or preview is still processing | `wait_enabled()` before clicking; start the slow step on an earlier cue. |
