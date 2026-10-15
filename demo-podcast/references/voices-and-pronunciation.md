# Voices, pacing and pronunciation

## Default pair (hybrid engine)
| Host | Engine | Voice | Why |
|---|---|---|---|
| MAYA, listener's stand-in | Chatterbox | `@heart_expressive` (skill `voices/`) | Chosen by a user from a seven-voice sampler; warm, energetic, human |
| SAM, specialist | Kokoro | `am_fenrir` | Liveliest clean Kokoro male (pitch variety 5.4 st); the user liked it as is |

Seven-voice sampler the user heard (same lines; pitch variety of the female host in semitones):
Kokoro af_heart widened 3.5 · af_sarah 4.1 · af_kore 4.2 · af_aoede widened 3.7 · bf_lily 3.6 ·
Chatterbox built-in 5.5 · **Chatterbox with af_heart reference 3.6 (chosen)**. Pitch numbers alone
didn't decide it: the chosen voice wasn't the most varied, it sounded the most natural and warm.
So always let the user listen; use the numbers only to shortlist.

## Chatterbox (Resemble AI, MIT)
- Clones the timbre of a 10–12 s reference clip; Kokoro-made references keep everything synthetic.
- Per-turn delivery from the script tag through host `"emotions"`: higher `exaggeration` = more
  animated, lower `cfg_weight` = faster, looser pacing. Values in `voices/README.md`.
- **Pronunciation:** no IPA. `"rules_chatterbox"` uses plain respellings: `Infor` → `In-for`,
  `LangChain` → `Lang Chain`, `Pfaudler` → `Fowdler`, `Birst` → `Burst`, `GenAI` → `Gen A I`,
  acronyms spaced (`E R P`, `C F O`). Verified in the Infor episode: "And Infor says…" came back right.
- **Failure modes:** on one- or two-word lines it may repeat ("98 percent. Ah, 98 percent."), add a
  filler ("Well, 95"), or garble ("Gox 3"). Longer turns are reliable; turns over 260 characters are
  rendered a few sentences at a time to stop drift. `podcast.py retake` finds and fixes most slips.
- **Speed:** about 4.5× real time on Apple Silicon (MPS). 132 turns / 1,275 words took about 40 min.
- Adds Resemble's inaudible Perth watermark (AI-generated marker).

## Pacing (hybrid, measured)
4,398 script words, 263 turns, 12 chapters, gaps 0.32 s (0.2 s after a question), 0.8 s before a
chapter: **30.4 min**, i.e. about **145 words per minute of episode** including pauses. The same
script all-Kokoro was 31.7 min.

## Voices (Kokoro-82M)
The first letter of a voice is its language and accent: `a` = American English, `b` = British English.
The renderer loads one pipeline per language, so hosts can mix accents.

| Voice | Sound | Notes |
|---|---|---|
| `af_heart` | US female, warm | The best-tested voice; a good listener's stand-in |
| `am_michael` | US male, calm | Clearly distinct from af_heart; a good specialist |
| `af_bella` | US female, brighter | Alternative to af_heart |
| `am_adam` | US male, deeper | Alternative to am_michael |
| `bf_emma` | UK female | Use `lang b` rules (phonemes are checked per language) |
| `bm_george` | UK male | As above |

Pick two voices that differ in gender or accent, so listeners always know who is speaking.
A per-host `"speed"` in `podcast.json` multiplies the global speed if one voice runs fast.

### Energy: when a host sounds dull
"Dull" or "robotic" mostly means a narrow pitch range. Measure it: the standard deviation of a
turn's pitch in semitones around its median (Praat via parselmouth). Lively hosts sit around 4–5.

Measured on the same five lines (Kokoro rates voice quality A to D; lower grades risk artefacts):

| Voice | Pitch variety (st) | Grade |
|---|---|---|
| `am_fenrir` | 5.4 | C+ — the energetic male that worked |
| `af_kore` | 4.2 | C+ |
| `bf_alice` / `bf_lily` | 4.2 / 3.8 | D |
| `af_sarah` | 3.8 | C+ |
| `af_heart` | 2.9 | A |
| `af_bella` | 2.6 | A- |
| `am_michael` | 3.8 | B (calm) |

Two `podcast.json` host options lift a clean but flat voice without changing who it sounds like:
- **Blend:** `"voice": "af_bella:0.6+af_kore:0.4"` averages the voice styles (weights normalised).
- **Widen intonation:** `"pitch_expand": 1.3` stretches each turn's pitch around its median with
  Praat (needs `praat-parselmouth` in the Kokoro env). 1.2–1.4 sounds natural; more sounds sing-song.

`af_bella:0.6+af_kore:0.4` with `pitch_expand 1.3` and `speed 1.04` took the female host from 2.65 to
4.0 st across a 32-minute episode, against the male host's 5.1, with no extra transcript errors.

Kokoro swallows a leading "And" in very short questions ("And fashion?" → "In fashion?") with any
voice: write "What about fashion?" or "And... box four?".

## Pacing (measured)
af_heart + am_michael, 3,734 words, 155 turns, 0.45 s between turns, 1 s chapter pauses:

| Speed | Length | Spoken words/min |
|---|---|---|
| 1.0 | 28.6 min | ≈ 137 |
| 0.95 | 29.5 min | ≈ 133 |

So budget about **130 words per minute of episode** at 1.0 (pauses included). Kokoro's speed isn't
linear: 0.95 added about 3 %, not 5 %. Stay within 0.9–1.1; outside it the voices sound rushed or slow.
A render of 30 minutes takes about 4 minutes on Apple Silicon.

## Pronunciation rules
`podcast.json` `"rules"` is a list of `[regex, replacement]` pairs, applied in order to each turn
before synthesis, never inside a `[word](/ipa/)` span an earlier rule produced.
- **Unknown names → a phonetic spelling** in misaki IPA: `[Word](/ipa/)`. Misaki uses `A` = "ay",
  `I` = "eye", `O` = "oh", `W` = "ow" (as in "how"), `Y` = "oy".
- **Possessive before base:** put the `Name's` rule above the `Name` rule.
- **Acronyms said as letters:** `X-Y-Z` (hyphens force letter-by-letter).
- **Compounds Kokoro slurs:** split them (`forward-deployed` → `forward deployed`, `pick-path` → `pick path`).
- **Brand spellings:** respell (`Xpress` → `Express`, `CloudSuite` → `Cloud Suite`).
- Always confirm a fix with `podcast.py phonemes`. ❓ means the word is not in Kokoro's lexicon and will be
  guessed: ordinary words often come out fine ("observability" did), names often don't ("Infor" → "within 4").

### Verified examples (US English)
| Word | Rule | Phonemes |
|---|---|---|
| Infor | `[Infor](/ˈɪnfɔɹ/)` | ˈɪnfɔɹ ("IN-for") |
| Infor's | `[Infor's](/ˈɪnfɔɹz/)` | ˈɪnfɔɹz |
| agentic | `[agentic](/Aʤˈɛntɪk/)` | Aʤˈɛntɪk ("ay-JEN-tik") |
| Inline | `In-line` | ˈɪnlˌIn |
| Birst | `[Birst](/bˈɜɹst/)` | bˈɜɹst ("burst") |
| LangChain | `[LangChain](/lˈæŋʧAn/)` | lˈæŋʧAn |
| Pfaudler | `[Pfaudler](/fˈWdləɹ/)` | fˈWdləɹ ("FOWD-ler") |
| OS | `O-S` | ˈOˌɛs (otherwise "oss") |
| IT | `I-T` | ˈItˌi (otherwise "it") |
| GenAI | `Gen-A-I` | — |
| ERP | `E-R-P` | ˌiˌɑɹpˈi |
| Value+ | `Value Plus` | — |
| observability | `[observability](/əbzˌɜɹvəbˈɪləTi/)` | əbzˌɜɹvəbˈɪləTi (guessed correctly without it, too) |

Already fine without rules: Bedrock, Coram, CareFor, ChatGPT, GMM, ION ("eye-on"), PDF, APIs,
micro-vertical, non-conformance, available-to-promise.
