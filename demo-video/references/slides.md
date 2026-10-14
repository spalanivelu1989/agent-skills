# Videos of a slide deck (no app)

Use this when the "app" is a deck, a PDF or a set of images: a client explainer narrated over slides.
The engine is unchanged; each slide becomes a local page and the cursor follows the narration.

## 1. Render the slides
- **Client-safe version first.** Rebuild or export the deck **without** footers that cite internal
  material (training decks, partner notes, "booth team" remarks) and without speaker notes. A footer
  left in place sits under the 92 px caption bar and shows faintly through it, which looks like a
  glitch. If the deck comes from a generator, add a switch (e.g. `CLIENT=1`) that drops footers,
  rather than editing slides by hand.
- **Exact viewport size.** Convert to PDF, then to PNGs scaled to the viewport, not by DPI:
  ```bash
  python3 <pptx-skill>/scripts/office/soffice.py --headless --convert-to pdf deck.pptx
  pdftoppm -png -f 1 -l 17 -scale-to-x 1920 -scale-to-y 1080 deck.pdf slides/s   # s-01.png …
  ```
  Rendering by DPI instead (`-r 150` gives 2000×1125 for a 13.33 in slide) doesn't match the viewport,
  so the page would have to rescale every slide.
- In zsh, `rm -f s-*.png` fails with "no matches found" when nothing matches; use `rm -f -- s-*.png(N)`
  or skip the clean-up on a fresh folder.

## 2. One page per slide
```python
for i in range(1, N + 1):
    open(f"slides/s{i:02d}.html", "w").write(f"""<!doctype html><html><head><meta charset="utf-8">
<style>html,body{{margin:0;background:#241640;overflow:hidden}}img{{display:block;width:1920px;height:1080px}}</style>
</head><body><img id="slide" src="s-{i:02d}.png" alt="Slide {i}"></body></html>""")
```
Set the page background to the deck's own background colour so a slow image load never flashes white.

## 3. Scene helpers
```python
from pathlib import Path
SLIDES = Path(__file__).resolve().parent / "slides"
BASE_URL = SLIDES.as_uri()
PX = 1920 / 13.333            # pixels per slide inch (16:9 wide layout)

def login(pg):
    pass                      # no sign-in

def open_slide(pg, n):
    pg.goto(f"{BASE_URL}/s{n:02d}.html")
    settle(pg, 0.6)
    glide(pg, 12.6 * PX, 1.2 * PX, steps=2)   # park the cursor on an empty part of the slide

def swap(pg, n):              # change slide inside one scene, at a cue
    pg.evaluate(f"document.getElementById('slide').src = 's-{n:02d}.png'")
    hold(pg, 0.3)

def s06_map(pg, mark, at):
    open_slide(pg, 6); mark(); still(pg, "s06_map")
    at("Diagnose, with Process Mining"); glide(pg, 1.98 * PX, 2.44 * PX, steps=35)
```
- A slide image has no DOM text, so `point()` and `reveal()` can't find anything. Use `glide()` to
  coordinates taken from the deck's layout (inches from the generator, or measured on a render).
- **Park the cursor where the slide is empty**, not in the bottom-right corner: a corner position
  sits inside the caption bar and shows as a stray dot for the whole scene.
- Two slides that belong to one narration paragraph go in one scene with `swap()` at the cue,
  rather than two scenes that each need a fresh page load.

## 4. Generate `scenes.json` from the script
Take each scene's `vo` from the script's narration column **verbatim** (strip the quotes and
`**bold**`), so the script and the video can't drift apart. Keep a table of
`(scene id, script row, slide, caption, [(cue, x_in, y_in, swap_to)])` and generate both
`scenes.json` and `scenes.py` from it. Assert, before writing, that every cue occurs in its voice-over
in order, and that every caption is under 90 characters.

## 5. Content rules for client videos
- Every figure on screen must be publicly verifiable; put the sources on a closing `"card"` scene
  rather than in slide footers.
- A recreated or mock screen keeps its "Illustrative" label on the slide, says so in the narration,
  and is named again on the sources card.
- Re-check statuses that change (availability, counts) on the day the video is published.

## 6. Checking
- Contact-sheet frames are taken 1.5 s after each cue; with short gaps between cues the cursor may
  already be moving to the next point. Judge by whether it reached the right element, not by the
  exact frame.
- `check.py`'s Whisper transcript writes amounts as figures ("$700,000"), so it reports the word
  "dollars" as missing. Confirm with the phonemes, then add it to `check_ignore`.
