# Voice-over played on the user's own page

Use this when the user wants the narration on their own page, for example an explainer animation
or a lightbox, rather than in an MP4 (SKILL.md › 0d). Nothing is recorded. You render one audio
track, measure when each key word is spoken, and have the page follow the audio.

This was first built for a personal site's "Happiness → Willpower → Confidence" loop animation:
five sentences, about 32 seconds, a 260 KB `.m4a` file.

## 1. Script
- Write one sentence per step of the animation. If the arrows or labels on screen carry words
  ("fuels", "builds", "boosts"), put those words in the narration, so each label appears as it is spoken.
- If the user wrote the script, offer a language check first (SKILL.md › 0b).
- The captions are the spoken sentences, so people with the sound off get the same message.

## 2. Render
Use speed **0.9** for reflective narration; it is clearer than 1.0. Render the narration **in one
pass**, so each sentence flows on from the last. If each sentence is rendered separately, it starts
from cold, and its first word gets rushed.

```bash
KPY=~/.cache/demo-video-tts/bin/python
echo '{"voice":"af_heart","speed":0.9,"items":[{"text":"[When](/wˈɛn/) you are … [That](/ðˈæt/) positivity …","out":"/abs/full.wav"}]}' \
  | "$KPY" -I ~/.claude/skills/demo-video/engine/kokoro_say.py
```

Before rendering, run the phoneme check on every word and look for the delivery risks listed in
SKILL.md › 5b: unstressed openers, `ᵻ` vowels and compounds.

## 3. Add pauses and measure
Run Whisper with `word_timestamps=True` on a **16 kHz numpy array**, not a file path, because the
path loader needs ffmpeg. Then:
1. Find each sentence boundary: the midpoint between the word ending in "." and the next word.
2. Check the level there is near silence (RMS under about 0.1% of peak) before you cut.
3. Insert about 0.8 s of silence at each boundary, and about 0.6 s at the start.
4. Normalise the peak to about 0.89 and write the WAV with soundfile.
5. **Transcribe the final file again.** Take every timing from that file: the start of each
   sentence, each key word, and the moment each character is named. Earlier timings are out of
   date after any edit.

To replace one sentence with a take the user approved, splice it in at a sentence pause, match
its loudness to the rest, and re-measure. Don't re-voice the whole track (SKILL.md › 5b).

## 4. Encode
```bash
afconvert -f m4af -d aac -b 64000 narration.wav site/audio/narration.m4a   # macOS, no ffmpeg
```
Every browser plays AAC in `.m4a`.

## 5. Drive the page from the audio's clock
Keep the timings in one object, and say where they came from:

```js
// Seconds into the track, from Whisper word timestamps on the final file.
const NARRATION = {
  src: 'audio/narration.m4a',
  lines: [{ at: 0.56, text: '…' }, /* one per sentence: captions */],
  words: [{ word: 9.42, arrive: 9.96 }, /* key word spoken, next thing named */],
};
```

Schedule the events against `audio.currentTime`, not against `setTimeout` from the click. That way
the page waits for a voice that starts late on a slow network:

```js
function clock() { return useAudioClock ? audio.currentTime : (performance.now() - t0) / 1000; }
function tick() { const t = clock(); while (events.length && events[0].t <= t) events.shift().fn();
                  if (events.length) raf = requestAnimationFrame(tick); }
audio.muted = isMuted(); audio.currentTime = 0; useAudioClock = true;
audio.play().catch(() => { useAudioClock = false; t0 = performance.now(); });  // blocked or missing: run silently
tick();
```

- **Timing:** finish drawing each arrow just as its word is spoken (start the draw `DRAW` seconds
  earlier), and show the next element when the voice names it.
- **Loading:** create the `Audio` on the first open, so the file isn't downloaded with the page.
  The open is a click, so autoplay is allowed.
- **Muting:** use `audio.muted`, not pause. The clock keeps running, so muting doesn't change the timing.
- **Mute button:** add one next to replay and close. Store the choice in `localStorage` inside
  `try/catch`, and set `aria-pressed`.
- **Stopping:** pause the audio and cancel the scheduler when the page closes, and before a replay.
- **Reduced motion:** show the finished state, and still play the voice and captions.
- **Captions:** reserve room for two or three lines, so the layout doesn't jump as captions change.

## 6. Verify
- Run headless Chrome (Playwright, `--autoplay-policy=no-user-gesture-required`). Open the page,
  sample the state at each key-word time, and check the audio request returns 200 with no console errors.
- **Hand the listening to the user** with `! afplay <full absolute path>` before you put the file
  on the page. Then ask them to play it on the page once.
