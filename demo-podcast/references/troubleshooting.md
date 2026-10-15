# Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| A brand name is missing from the transcript, or heard as other words ("Infor" → "within 4") | Kokoro guesses words outside its lexicon, and names often go wrong | Run `phonemes` **before** rendering; add a `[Word](/ipa/)` rule. |
| "OS" sounds like "oss", "IT" like "it" | Short capitals that are also words are read as words | Rules `O-S`, `I-T`. |
| `check` shows words that were never said ("it does include" → "Infor says that it includes") | A Whisper vocabulary prompt makes Whisper insert prompt words | `check` uses no prompt. Re-test suspect turns with `--clips`; a clean clip means the audio is fine. |
| `check` lists "twenty five percent → 25", "organisation → organization", "cloud suite → cloudsuite" | Whisper writes numbers as digits, uses US spelling and joins compounds | Filtered automatically; any left are cosmetic. |
| A name is "heard" differently every time ("in for", "infer", "info") even after the fix | Whisper doesn't know the name either | Confirm the phonemes, then ask the user to listen; the voice reads it the same way every time. |
| The episode is a minute or two short or long | Word budget off, or speed | Change `"speed"` (0.95 ≈ +3 %) or add/cut a few turns; `estimate` before re-rendering. |
| `Speaker X is not in podcast.json hosts` | A `NAME:` in the script doesn't match a host key | Use the same uppercase key in both files. |
| `Kokoro environment not found` | First use on this machine | `bash tools/setup_tts.sh` (about 1.5 GB; shared with demo-video). |
| A render in the foreground times out | 30 minutes of audio takes about 4 minutes | Run `render` in the background and wait for it to finish. |
| The user says a voice is "dull" or "robotic" | Narrow pitch range (Kokoro female voices ≈ 2.6–2.9 st) | Hybrid engine with a Chatterbox host; if they still dislike it, a voice sampler (SKILL step 5b), not more tuning. |
| A Chatterbox turn repeats a phrase, adds "Well," or garbles a word | Sampling slip, mostly on very short lines | `podcast.py retake <dir>`; if three seeds fail, add a few words to the line and `render` again (only that turn re-renders). |
| `retake` still lists "fourth → forth", digits, or a brand name | Whisper, not the audio | Leave it; ask the user to listen to that turn. |
| `Chatterbox environment not found` | First use of hybrid/chatterbox | `bash tools/setup_chatterbox.sh` (Python 3.11; pins `setuptools<81` for the Perth watermarker). |
| `reference @name not found` | Typo, or a voice not saved in the skill | List `voices/`; or set `"kokoro_voice"` and a project `"reference"` path to make one. |
| Hybrid `render` takes ~40 min | Chatterbox is ~4.5× real time | Run in the background with a progress monitor; edits later re-render only changed turns. |
