"""Hybrid render: each host on its own engine. podcast.json: "engine": "hybrid", and per host
"engine": "kokoro" (with "voice", optional "pitch_expand", "speed") or "engine": "chatterbox" (with
"reference" and "emotions"). podcast.py drives it; each mode runs in the right environment:

    python _hybrid.py kokoro     <dir> [i,j,..] [seed_offset]   (Kokoro env)     clips -> <dir>/cache
    python _hybrid.py chatterbox <dir> [i,j,..] [seed_offset]   (Chatterbox env) clips -> <dir>/cache
    python _hybrid.py assemble   <dir>                          (either env)     -> build/podcast.wav,
                                                                                  chapters.txt, turns.json

Clips are cached per turn as <index>_<HOST>_<hash of the line>.wav, so after a script edit only the
changed turns are rendered again. Without an index list, only missing clips are rendered; with one,
those turns are rendered again (a seed offset gives a different take).
A host "reference" of "@name" means the skill's voices/name.wav.
"""
import hashlib
import json
import re
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
RATE = 24000
HERE = Path(__file__).resolve().parent
EMO_SPEED = {"excited": 1.06, "calm": 0.95}
DEFAULT_GAPS = {"default": 0.32, "after_question": 0.2, "overlap": -0.25, "chapter": 0.8}
DEFAULT_EMOTIONS = {"neutral": {"exaggeration": 0.75, "cfg_weight": 0.35},
                    "excited": {"exaggeration": 0.9, "cfg_weight": 0.3},
                    "calm": {"exaggeration": 0.55, "cfg_weight": 0.42}}


def load(base):
    return json.loads((base / "podcast.json").read_text())


def parse(base, cfg):
    """[("segment", title) | ("overlap",) | ("pause", s) | ("turn", index, host, emotion, text)]"""
    items, n = [], 0
    for line in (base / cfg.get("script", "podcast-script.md")).read_text().splitlines():
        s = line.strip()
        if s.startswith("## "):
            items.append(("segment", s[3:].strip()))
        elif s == "[overlap]":
            items.append(("overlap",))
        elif re.fullmatch(r"\[pause ([\d.]+)\]", s):
            items.append(("pause", float(s[7:-1])))
        else:
            m = re.match(r"^([A-Z][A-Z0-9_]*)(?: \((\w+)\))?: (.+)$", s)
            if m:
                items.append(("turn", n, m.group(1), (m.group(2) or "neutral").lower(), m.group(3)))
                n += 1
    return items


def clip_path(base, i, who, text):
    return base / "cache" / f"{i:03d}_{who}_{hashlib.md5(text.encode()).hexdigest()[:6]}.wav"


def reference(base, h):
    r = h.get("reference", "")
    return HERE.parent / "voices" / f"{r[1:]}.wav" if r.startswith("@") else base / r


def jobs(base, cfg, engine, only):
    out = []
    for it in parse(base, cfg):
        if it[0] != "turn":
            continue
        _, i, who, emo, text = it
        if who not in cfg["hosts"]:
            raise SystemExit(f"Speaker {who} is not in podcast.json hosts")
        if cfg["hosts"][who].get("engine", "kokoro") != engine:
            continue
        if only is not None and i not in only:
            continue
        if only is None and clip_path(base, i, who, text).exists():
            continue
        out.append(it)
    return out


def run_kokoro(base, cfg, only, offset):
    import numpy as np
    import soundfile as sf
    sys.path.insert(0, str(HERE))
    import _kokoro_worker as W
    from kokoro import KPipeline
    pipes, voices = {}, {}
    todo = jobs(base, cfg, "kokoro", only)
    for n, (_, i, who, emo, text) in enumerate(todo, 1):
        h = cfg["hosts"][who]
        spec = h["voice"]
        if spec[0] not in pipes:
            pipes[spec[0]] = KPipeline(lang_code=spec[0], repo_id="hexgrad/Kokoro-82M")
        pipe = pipes[spec[0]]
        if spec not in voices:
            voices[spec] = W.load_voice(pipe, spec)
        spd = float(cfg.get("speed", 1.0)) * float(h.get("speed", 1.0)) * EMO_SPEED.get(emo, 1.0)
        a = np.concatenate([x.numpy() for _, _, x in pipe(W.apply_rules(text, cfg.get("rules", [])), voice=voices[spec], speed=spd)])
        if float(h.get("pitch_expand", 1.0)) != 1.0:
            a = W.expand_pitch(a, float(h["pitch_expand"]))
        clip_path(base, i, who, text).parent.mkdir(exist_ok=True)
        sf.write(clip_path(base, i, who, text), a, RATE)
    print(f"kokoro: {len(todo)} turns rendered", flush=True)


def split_long(t, limit=260):
    """Chatterbox drifts on long inputs; render long turns a few sentences at a time."""
    if len(t) <= limit:
        return [t]
    parts, cur = [], ""
    for s in re.split(r"(?<=[.!?])\s+", t):
        if cur and len(cur) + len(s) > limit:
            parts.append(cur)
            cur = s
        else:
            cur = f"{cur} {s}".strip()
    return parts + ([cur] if cur else [])


def run_chatterbox(base, cfg, only, offset):
    import numpy as np
    import soundfile as sf
    import torch
    import librosa
    from chatterbox.tts import ChatterboxTTS
    todo = jobs(base, cfg, "chatterbox", only)
    if not todo:
        print("chatterbox: 0 turns rendered", flush=True)
        return
    dev = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")
    m = ChatterboxTTS.from_pretrained(device=dev)
    rules = cfg.get("rules_chatterbox", [])
    seed = int(cfg.get("seed", 11)) + offset

    def trim(a, th=0.01):
        k = np.where(np.abs(a) > th)[0]
        return a if not len(k) else a[max(0, k[0] - 720): k[-1] + 720]

    for n, (_, i, who, emo, text) in enumerate(todo, 1):
        h = cfg["hosts"][who]
        emos = {**DEFAULT_EMOTIONS, **h.get("emotions", {})}
        e = {**emos["neutral"], **emos.get(emo, {})}
        t = text
        for pat, rep in rules:
            t = re.sub(pat, rep, t)
        pieces = []
        for k, ch in enumerate(split_long(t)):
            torch.manual_seed(seed + i * 10 + k)
            w = m.generate(ch, audio_prompt_path=str(reference(base, h)), exaggeration=float(e["exaggeration"]),
                           cfg_weight=float(e["cfg_weight"]), temperature=float(e.get("temperature", 0.8)))
            pieces += [trim(w.squeeze(0).cpu().numpy()), np.zeros(int(0.12 * m.sr), dtype=np.float32)]
        a = librosa.resample(np.concatenate(pieces[:-1]), orig_sr=m.sr, target_sr=RATE)
        clip_path(base, i, who, text).parent.mkdir(exist_ok=True)
        sf.write(clip_path(base, i, who, text), a, RATE)
        print(f"{n}/{len(todo)}  {who} ({emo}): {text[:60]}", flush=True)
    print(f"chatterbox: {len(todo)} turns rendered", flush=True)


def assemble(base, cfg):
    import numpy as np
    import soundfile as sf
    g = {**DEFAULT_GAPS, **cfg.get("gaps", {})}

    def level(a, r):
        return np.clip(a * r / (float(np.sqrt(np.mean(a ** 2))) + 1e-6), -0.98, 0.98)

    placed, chapters, turns = [], [], []
    t, prev_end, overlap, prev_text, first = 0.6, 0.6, False, "", True
    for it in parse(base, cfg):
        if it[0] == "segment":
            if not first:
                t = prev_end = prev_end + g["chapter"]
            chapters.append((t, it[1]))
        elif it[0] == "overlap":
            overlap = True
        elif it[0] == "pause":
            t = prev_end = prev_end + it[1]
        else:
            _, i, who, emo, text = it
            a, _ = sf.read(clip_path(base, i, who, text), dtype="float32")
            a = level(a, float(cfg["hosts"][who].get("rms", 0.08)))
            dur = len(a) / RATE
            if first:
                start = t
            elif overlap:
                start = max(prev_end + g["overlap"], prev_end - 0.5 * dur)
            else:
                start = max(t, prev_end + (g["after_question"] if prev_text.rstrip().endswith("?") else g["default"]))
            placed.append((start, a))
            turns.append({"i": i, "who": who, "emotion": emo, "start": round(start, 2), "dur": round(dur, 2), "text": text})
            prev_end = t = start + dur
            overlap, prev_text, first = False, text, False
    total = t + 1.0
    mix = np.zeros(int(total * RATE) + 1, dtype=np.float32)
    for s, a in placed:
        k = int(s * RATE)
        mix[k:k + len(a)] += a[: len(mix) - k]
    out = base / cfg.get("out_dir", "build")
    out.mkdir(exist_ok=True)
    sf.write(out / "podcast.wav", np.clip(mix, -0.99, 0.99), RATE)
    (out / "chapters.txt").write_text("".join(f"{int(s // 60):02d}:{int(s % 60):02d}  {n}\n" for s, n in chapters))
    (out / "turns.json").write_text(json.dumps(turns, indent=1))
    print(f"TOTAL {total / 60:.2f} min", flush=True)


def main():
    mode, base = sys.argv[1], Path(sys.argv[2]).resolve()
    only = {int(x) for x in sys.argv[3].split(",")} if len(sys.argv) > 3 and sys.argv[3] else None
    offset = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    cfg = load(base)
    {"kokoro": lambda: run_kokoro(base, cfg, only, offset),
     "chatterbox": lambda: run_chatterbox(base, cfg, only, offset),
     "assemble": lambda: assemble(base, cfg)}[mode]()


if __name__ == "__main__":
    main()
