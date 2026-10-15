#!/usr/bin/env python3
"""demo-podcast command line. Runs with the system python3 (stdlib + ffmpeg); the speech work
runs in the Kokoro environment through _kokoro_worker.py.

    podcast.py init <dir> [--kokoro]      copy podcast.json + podcast-script.md templates into <dir>
                                          (default: hybrid preset; --kokoro: fast all-Kokoro preset)
    podcast.py estimate <dir> [--speed S] words, turns and estimated length
    podcast.py phonemes <dir>             list words Kokoro would drop (❓) or read as a word
    podcast.py render <dir> [--chapters 1,2]  render build/podcast.wav, or build/pilot.wav for chosen chapters
                                          (slow: run it in the background)
    podcast.py check <dir> [--clips]      Whisper transcript vs script; --clips re-checks suspect turns alone
    podcast.py retake <dir> [--turns 3,7] [--attempts 3]
                                          hybrid engine: check each Chatterbox turn on its own, render
                                          failing turns again with new seeds, keep the best take, re-assemble
    podcast.py encode <dir>               loudness-normalised MP3 with chapter markers
    podcast.py play <dir>                 open the MP3 in QuickTime Player and play it (macOS)

The Kokoro environment is $KOKORO_PYTHON or ~/.cache/demo-video-tts/bin/python (set up once with
tools/setup_tts.sh, shared with the demo-video skill). The Chatterbox environment (engines
"chatterbox" and "hybrid") is $CHATTERBOX_PYTHON or ~/.cache/demo-podcast-chatterbox/bin/python
(tools/setup_chatterbox.sh).

Engines (podcast.json "engine"):
    kokoro      every host on Kokoro: fast (about 4 min for 30 min of audio)
    hybrid      each host on its own engine ("engine": "kokoro" | "chatterbox" per host); turns are
                cached in <dir>/cache, so a script edit re-renders only the changed turns
    chatterbox  every host on Chatterbox (slow: about 4.5x real time)
"""
import difflib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
KOKORO_PY = Path(os.environ.get("KOKORO_PYTHON", Path.home() / ".cache" / "demo-video-tts" / "bin" / "python"))
CHATTERBOX_PY = Path(os.environ.get("CHATTERBOX_PYTHON", Path.home() / ".cache" / "demo-podcast-chatterbox" / "bin" / "python"))
REF_TEXT = ("Welcome back to the show. Today we're digging into how manufacturers are putting AI to work inside "
            "their everyday systems, from the shop floor to the finance team. It's a big topic, and honestly, "
            "a really exciting one.")
WORKER = HERE / "_kokoro_worker.py"
HYBRID = HERE / "_hybrid.py"
SPAN = re.compile(r"\[([^\]]+)\]\(/[^)]+/\)")

# Measured: af_heart + am_michael, 3,734 words, 155 turns, 0.45 s turn pauses:
# 28.6 min at speed 1.0 and 29.5 min at 0.95, i.e. about 137 spoken words a minute at 1.0.
WPM_AT_1 = 137.0


def load(d):
    d = Path(d).resolve()
    cfg = json.loads((d / "podcast.json").read_text())
    return d, cfg


def worker(job, capture=True):
    if not KOKORO_PY.exists():
        sys.exit(f"Kokoro environment not found at {KOKORO_PY}. Run: bash {HERE / 'setup_tts.sh'}")
    r = subprocess.run([str(KOKORO_PY), str(WORKER)], input=json.dumps(job), text=True,
                       capture_output=capture)
    if r.returncode:
        sys.exit((r.stderr or "")[-2000:] or f"worker failed ({r.returncode})")
    return json.loads(r.stdout) if capture else None


def parse_script(path):
    for line in Path(path).read_text().splitlines():
        s = line.strip()
        if s.startswith("## "):
            yield ("segment", s[3:].strip())
        elif re.fullmatch(r"\[pause ([\d.]+)\]", s):
            yield ("pause", float(re.fullmatch(r"\[pause ([\d.]+)\]", s).group(1)))
        else:
            m = re.match(r"^([A-Z][A-Z0-9_]*)(?: \((\w+)\))?: (.+)$", s)
            if m:
                yield ("turn", m.group(1), m.group(3))


def apply_rules(text, rules):
    for pat, rep in rules:
        parts = re.split(r"(\[[^\]]+\]\(/[^)]+/\))", text)
        text = "".join(p if SPAN.fullmatch(p) else re.sub(pat, rep, p) for p in parts)
    return text


def turns_of(d, cfg):
    return [i for i in parse_script(d / cfg.get("script", "podcast-script.md")) if i[0] == "turn"]


# ---------------------------------------------------------------- commands
def cmd_init(d, kokoro=False):
    d = Path(d)
    d.mkdir(parents=True, exist_ok=True)
    for f, src in (("podcast.json", "podcast.kokoro.json" if kokoro else "podcast.json"),
                   ("podcast-script.md", "podcast-script.md")):
        if (d / f).exists():
            print(f"kept existing {d / f}")
        else:
            shutil.copy(SKILL / "templates" / src, d / f)
            print(f"created {d / f} from {src}")


def cmd_estimate(d, speed=None):
    d, cfg = load(d)
    items = list(parse_script(d / cfg.get("script", "podcast-script.md")))
    turns = [i for i in items if i[0] == "turn"]
    pauses = sum(i[1] for i in items if i[0] == "pause")
    words = sum(len(i[2].split()) for i in turns)
    sp = float(speed or cfg.get("speed", 1.0))
    wpm = WPM_AT_1 * sp ** 0.6           # Kokoro's speed is not linear: 0.95 measured ~133 wpm
    secs = words / wpm * 60 + len(turns) * float(cfg.get("turn_pause", 0.45)) + pauses + 1.6
    if cfg.get("engine") == "hybrid":
        secs = words / 145 * 60   # measured: 4,398 words, 263 turns, 12 chapters -> 30.4 min, pauses included
    by = {}
    for _, who, text in turns:
        by[who] = by.get(who, 0) + len(text.split())
    print(f"{words} words, {len(turns)} turns, {sum(1 for i in items if i[0] == 'segment')} segments")
    print("words by host: " + ", ".join(f"{k} {v} ({v * 100 // max(words, 1)}%)" for k, v in by.items()))
    budget = 145 if cfg.get("engine") == "hybrid" else 130
    print(f"estimated length at speed {sp}: {secs / 60:.1f} min  (budget ≈ minutes × {budget} words for this engine)")


def cmd_phonemes(d):
    d, cfg = load(d)
    rules = cfg.get("rules", [])
    text = " ".join(apply_rules(t[2], rules) for t in turns_of(d, cfg))
    spans = SPAN.findall(text)
    plain = SPAN.sub(" ", text)
    cands = set(re.findall(r"\b[A-Za-z][A-Za-z0-9'+\-]*[A-Z0-9+][A-Za-z0-9'+\-]*\b", plain))   # inner caps, digits, +
    cands |= set(re.findall(r"\b[A-Z][a-z]+(?:'[a-z]+)?(?![a-z'])", plain))                    # capitalised words, contractions whole
    cands |= set(re.findall(r"\b\w+(?:-\w+)+\b", plain))                                     # hyphenated
    cands |= {w for w in set(re.findall(r"\b[a-z]{9,}\b", plain))}                           # long words
    langs = {h["voice"][0] for h in cfg["hosts"].values() if h.get("voice")} or {"a"}
    if any(h.get("engine") == "chatterbox" for h in cfg["hosts"].values()):
        print("Chatterbox hosts: these phonemes are Kokoro's. Chatterbox reads plain respellings from "
              "\"rules_chatterbox\" (\"In-for\", \"Lang Chain\"); check its turns with `retake`.\n")
    bad = []
    for lang in sorted(langs):
        res = worker({"mode": "phonemes", "words": sorted(cands), "lang": lang})
        for w, ph in sorted(res.items()):
            if "❓" in ph:
                bad.append((lang, w, ph))
        acr = {w: ph for w, ph in res.items() if re.fullmatch(r"[A-Z]{2,5}s?", w)}
        if acr:
            print(f"[{lang}] acronyms (a word-like reading means it is said as a word; add 'X-Y-Z' rule if letters were meant):")
            for w, ph in sorted(acr.items()):
                print(f"   {w:10s} {ph}")
    if spans:
        print(f"{len(set(spans))} words already have phonetic spellings: {', '.join(sorted(set(spans)))}")
    if bad:
        print("\nWORDS NOT IN KOKORO'S LEXICON: it will guess them, sometimes well ('observability'),\n"
              "sometimes badly ('Infor' came out as 'within 4'). Add a rule for every name, then re-run;\n"
              "for an ordinary word you may instead confirm it with `check` after rendering:")
        for lang, w, ph in bad:
            print(f"   [{lang}] {w:24s} {ph}")
        sys.exit(1)
    print("\nNo unknown words. Ready to render.")


def ensure_refs(d, cfg):
    for name, h in cfg["hosts"].items():
        if cfg.get("engine") == "hybrid" and h.get("engine", "kokoro") != "chatterbox":
            continue
        r = h.get("reference", f"refs/{name.lower()}.wav")
        ref = SKILL / "voices" / f"{r[1:]}.wav" if r.startswith("@") else d / r
        if not ref.exists():
            if r.startswith("@") or not h.get("kokoro_voice"):
                sys.exit(f"host {name}: reference {r} not found; set 'reference' to a WAV, '@name' for "
                         f"voices/name.wav, or 'kokoro_voice' to make one")
            print(worker({"mode": "ref", "voice": h["kokoro_voice"], "text": h.get("reference_text", REF_TEXT),
                          "out": str(ref)}))


def run_hybrid(d, mode, turns=None, offset=0):
    py = CHATTERBOX_PY if mode == "chatterbox" else KOKORO_PY
    if not py.exists():
        sys.exit(f"environment not found at {py}. Run: bash {HERE / ('setup_chatterbox.sh' if mode == 'chatterbox' else 'setup_tts.sh')}")
    args = [str(py), "-I", str(HYBRID), mode, str(d)]
    if turns is not None:
        args += [",".join(map(str, sorted(turns))), str(offset)]
    r = subprocess.run(args, env={**os.environ, "TQDM_DISABLE": "1"})
    if r.returncode:
        sys.exit(f"hybrid {mode} failed ({r.returncode})")


def cmd_render(d, chapters=None):
    d, cfg = load(d)
    if cfg.get("engine") == "hybrid":
        if chapters:
            sys.exit("--chapters is not supported with the hybrid engine (it caches turns instead)")
        ensure_refs(d, cfg)
        run_hybrid(d, "kokoro")
        run_hybrid(d, "chatterbox")
        run_hybrid(d, "assemble")
        return
    if cfg.get("engine", "kokoro") != "chatterbox":
        if chapters:
            sys.exit("--chapters is supported with the chatterbox engine only")
        worker({"mode": "render", "config": str(d / "podcast.json")}, capture=False)
        return
    if not CHATTERBOX_PY.exists():
        sys.exit(f"Chatterbox environment not found at {CHATTERBOX_PY}. Run: bash {HERE / 'setup_chatterbox.sh'}")
    ensure_refs(d, cfg)
    out = d / cfg.get("out_dir", "build") / ("pilot.wav" if chapters else "podcast.wav")
    job = {"config": str(d / "podcast.json"), "chapters": chapters, "out": str(out)}
    r = subprocess.run([str(CHATTERBOX_PY), str(HERE / "_chatterbox_worker.py")], input=json.dumps(job), text=True)
    if r.returncode:
        sys.exit(f"chatterbox render failed ({r.returncode})")


SPELL = [(r"(\w{3,})is(e|ed|es|ing|ation|ations)\b", r"\1iz\2"), (r"\bcatalogue\b", "catalog"),
         (r"\bfavourite\b", "favorite"), (r"\bsceptical\b", "skeptical"), (r"\bcolour", "color"),
         (r"\bbehaviour", "behavior"), (r"\bcentre\b", "center")]
NUMW = set("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen "
           "sixteen seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety "
           "hundred thousand million billion point percent dollars and a".split())


def norm(t):
    t = SPAN.sub(r"\1", t).lower().replace("-", " ")
    for p, r in SPELL:
        t = re.sub(p, r, t)
    return [w for w in re.sub(r"[^a-z0-9' ]", " ", t).split() if w]


def trivial(r, h):
    if "".join(r) == "".join(h):                                  # cloud suite / cloudsuite, pick list
        return True
    if r and set(r) <= NUMW and all(re.fullmatch(r"[\d.,%$]+|percent|dollars|and|a", w) for w in h):
        return True                                               # twenty five percent -> 25
    return False


def cmd_check(d, clips=False):
    d, cfg = load(d)
    wav = d / cfg.get("out_dir", "build") / "podcast.wav"
    rules = cfg.get("rules", [])
    turns = turns_of(d, cfg)
    ref_turns = [norm(apply_rules(t[2], rules)) for t in turns]
    ref = [w for tt in ref_turns for w in tt]
    owner = [i for i, tt in enumerate(ref_turns) for _ in tt]
    print("transcribing (no vocabulary prompt: a prompt makes Whisper insert its words) …", flush=True)
    hyp = norm(worker({"mode": "transcribe", "files": [str(wav)], "prompt": None})[str(wav)])
    sm = difflib.SequenceMatcher(a=ref, b=hyp, autojunk=False)
    real, suspect = [], set()
    for op, a1, a2, b1, b2 in sm.get_opcodes():
        if op == "equal" or trivial(ref[a1:a2], hyp[b1:b2]):
            continue
        real.append((op, a1, a2, b1, b2))
        if a1 < len(owner):
            suspect.add(owner[min(a1, len(owner) - 1)])
    print(f"script {len(ref)} words, heard {len(hyp)} words, match {sm.ratio():.3f}, "
          f"{len(real)} non-trivial differences in {len(suspect)} turns\n")
    for op, a1, a2, b1, b2 in real[:80]:
        print(f"  {op:7s} …{' '.join(ref[max(0, a1 - 4):a1])} [{' '.join(ref[a1:a2])}] → [{' '.join(hyp[b1:b2])}]")
    if clips and suspect:
        import tempfile
        tl = json.loads((d / cfg.get("out_dir", "build") / "turns.json").read_text())
        tmp = Path(tempfile.mkdtemp())
        files = []
        for i in sorted(suspect):
            f = tmp / f"turn_{i:03d}.wav"
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(tl[i]["start"]), "-t",
                            str(tl[i]["dur"] + 0.2), "-i", str(wav), str(f)], check=True)
            files.append(str(f))
        res = worker({"mode": "transcribe", "files": files, "prompt": None})
        print("\nSuspect turns re-transcribed on their own (compare with the script line):")
        for f in files:
            i = int(Path(f).stem.split("_")[1])
            ok = difflib.SequenceMatcher(a=ref_turns[i], b=norm(res[f]), autojunk=False).ratio()
            print(f"\n  turn {i + 1} ({turns[i][1]}), match {ok:.2f}\n    script: {turns[i][2]}\n    heard:  {res[f]}")
    print("\nWhisper also mishears: confirm a word with `phonemes` before changing the script, and ask the user to listen.")


def cmd_retake(d, turns=None, attempts=3):
    """Per-turn check of Chatterbox clips; Chatterbox occasionally repeats a phrase, adds a word
    ("Well, ninety-five") or garbles a one- or two-word line. A new seed usually fixes it."""
    import glob
    d, cfg = load(d)
    if cfg.get("engine") != "hybrid":
        sys.exit("retake works with the hybrid engine (per-turn clips in <dir>/cache)")
    items = [t for t in parse_hybrid(d, cfg)]
    cb = {i: (who, text) for i, who, text in items if cfg["hosts"][who].get("engine") == "chatterbox"}
    idx = sorted(turns) if turns else sorted(cb)
    clip = lambda i: Path(glob.glob(str(d / "cache" / f"{i:03d}_{cb[i][0]}_*.wav"))[0])

    def scores(ids):
        res = worker({"mode": "transcribe", "files": [str(clip(i)) for i in ids], "prompt": None})
        out = {}
        for i in ids:
            r, h = norm(cb[i][1]), norm(res[str(clip(i))])
            sm = difflib.SequenceMatcher(a=r, b=h, autojunk=False)
            bad = [op for op in sm.get_opcodes() if op[0] != "equal" and not trivial(r[op[1]:op[2]], h[op[3]:op[4]])]
            out[i] = (1.0 if not bad else round(sm.ratio(), 2), res[str(clip(i))])
        return out

    print(f"checking {len(idx)} Chatterbox turns on their own …", flush=True)
    best = {}
    for i, (sc, heard) in scores(idx).items():
        keep = clip(i).with_suffix(".take0")
        shutil.copy(clip(i), keep)
        best[i] = (sc, keep, heard)
    for att in range(1, attempts + 1):
        todo = [i for i in idx if best[i][0] < 1.0]
        print(f"attempt {att}: {len(todo)} turns to retake {todo}", flush=True)
        if not todo:
            break
        run_hybrid(d, "chatterbox", todo, att * 1000)
        for i, (sc, heard) in scores(todo).items():
            keep = clip(i).with_suffix(f".take{att}")
            shutil.copy(clip(i), keep)
            if sc > best[i][0]:
                best[i] = (sc, keep, heard)
    for i in idx:
        shutil.copy(best[i][1], clip(i))
    for t in (d / "cache").glob("*.take*"):
        t.unlink()
    left = [i for i in idx if best[i][0] < 1.0]
    for i in left:
        print(f"  turn {i + 1} ({cb[i][0]}) still differs ({best[i][0]}):\n    script: {cb[i][1]}\n    heard:  {best[i][2]}")
    if left:
        print("\nIf a line still fails after three seeds, give it a few more words (\"Been there.\" -> "
              "\"Oh, I have been there.\") and run render again: only the edited turns are re-rendered.\n"
              "Digits, homophones (\"fourth\"/\"forth\") and names Whisper doesn't know are not audio faults.")
    run_hybrid(d, "assemble")


def parse_hybrid(d, cfg):
    n = 0
    for it in parse_script(d / cfg.get("script", "podcast-script.md")):
        if it[0] == "turn":
            yield n, it[1], it[2]
            n += 1


def cmd_encode(d):
    d, cfg = load(d)
    b = d / cfg.get("out_dir", "build")
    wav = b / "podcast.wav"
    total = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                  str(wav)], capture_output=True, text=True, check=True).stdout)
    ch = [l.split("  ", 1) for l in (b / "chapters.txt").read_text().strip().splitlines() if l.strip()]
    secs = [int(a.split(":")[0]) * 60 + int(a.split(":")[1]) for a, _ in ch]
    esc = lambda s: re.sub(r"([=;#\\\n])", r"\\\1", s)
    meta = ";FFMETADATA1\n" + "".join(f"{k}={esc(str(cfg[k]))}\n" for k in ("title", "artist", "album") if cfg.get(k))
    for i, (s, (_, n)) in enumerate(zip(secs, ch)):
        e = secs[i + 1] if i + 1 < len(secs) else int(total)
        meta += f"[CHAPTER]\nTIMEBASE=1/1\nSTART={s}\nEND={e}\ntitle={esc(n)}\n"
    (b / "meta.txt").write_text(meta)
    out = d / cfg.get("output", "podcast.mp3")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(wav), "-i", str(b / "meta.txt"),
                    "-map_metadata", "1", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                    "-c:a", "libmp3lame", "-b:a", str(cfg.get("bitrate", "128k")), str(out)], check=True)
    print(f"{out}  {total / 60:.1f} min, {out.stat().st_size / 1e6:.1f} MB")
    print((b / "chapters.txt").read_text())


def cmd_play(d):
    d, cfg = load(d)
    out = d / cfg.get("output", "podcast.mp3")
    subprocess.run(["open", "-a", "QuickTime Player", str(out)], check=True)
    subprocess.run(["osascript", "-e", 'delay 2', "-e", 'tell application "QuickTime Player" to play front document'])
    print(f"playing {out}")


def main():
    a = sys.argv[1:]
    if len(a) < 2 or a[0] not in {"init", "estimate", "phonemes", "render", "check", "retake", "encode", "play"}:
        sys.exit(__doc__)
    cmd, d = a[0], a[1]
    if cmd == "init":
        cmd_init(d, "--kokoro" in a)
    elif cmd == "estimate":
        cmd_estimate(d, a[a.index("--speed") + 1] if "--speed" in a else None)
    elif cmd == "phonemes":
        cmd_phonemes(d)
    elif cmd == "render":
        ch = [int(x) for x in a[a.index("--chapters") + 1].split(",")] if "--chapters" in a else None
        cmd_render(d, ch)
    elif cmd == "check":
        cmd_check(d, "--clips" in a)
    elif cmd == "retake":
        cmd_retake(d, {int(x) - 1 for x in a[a.index("--turns") + 1].split(",")} if "--turns" in a else None,
                   int(a[a.index("--attempts") + 1]) if "--attempts" in a else 3)
    elif cmd == "encode":
        cmd_encode(d)
    elif cmd == "play":
        cmd_play(d)


if __name__ == "__main__":
    main()
