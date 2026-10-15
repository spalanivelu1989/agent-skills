"""Expressive render with Chatterbox (Resemble AI, MIT). Runs in ~/.cache/demo-podcast-chatterbox.

podcast.py calls it with a JSON job on stdin:
    {"config": "/abs/podcast.json", "chapters": [1, 2] | null, "out": "/abs/build/podcast.wav"}

Each host speaks in the voice of its reference clip (hosts.NAME.reference, made from a Kokoro voice
by podcast.py when hosts.NAME.kokoro_voice is set). Delivery per turn comes from the script tag:
`NAME (excited): …`, `NAME (calm): …`, or plain `NAME: …`, mapped through config "emotions".
Chatterbox adds Resemble's imperceptible Perth watermark, which marks the audio as AI-generated.
"""
import json
import re
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

DEFAULT_EMOTIONS = {
    "neutral": {"exaggeration": 0.6, "cfg_weight": 0.4},
    "excited": {"exaggeration": 0.85, "cfg_weight": 0.3},
    "calm": {"exaggeration": 0.4, "cfg_weight": 0.5},
}
DEFAULT_GAPS = {"default": 0.35, "after_question": 0.2, "overlap": -0.3, "chapter": 0.8}


def apply_rules(text, rules):
    for pat, rep in rules:
        text = re.sub(pat, rep, text)
    return text


def parse(path):
    chapter = 0
    for line in Path(path).read_text().splitlines():
        s = line.strip()
        if s.startswith("## "):
            chapter += 1
            yield ("segment", chapter, s[3:].strip())
        elif s == "[overlap]":
            yield ("overlap", chapter)
        elif re.fullmatch(r"\[pause ([\d.]+)\]", s):
            yield ("pause", chapter, float(re.fullmatch(r"\[pause ([\d.]+)\]", s).group(1)))
        else:
            m = re.match(r"^([A-Z][A-Z0-9_]*)(?: \((\w+)\))?: (.+)$", s)
            if m:
                yield ("turn", chapter, m.group(1), (m.group(2) or "neutral").lower(), m.group(3))


def split_long(text, limit=260):
    """Chatterbox drifts on long inputs; render long turns sentence group by sentence group."""
    if len(text) <= limit:
        return [text]
    parts, cur = [], ""
    for sent in re.split(r"(?<=[.!?])\s+", text):
        if cur and len(cur) + len(sent) > limit:
            parts.append(cur)
            cur = sent
        else:
            cur = f"{cur} {sent}".strip()
    return parts + ([cur] if cur else [])


def trim(a, sr, thresh=0.01):
    import numpy as np
    idx = np.where(np.abs(a) > thresh)[0]
    if not len(idx):
        return a
    pad = int(0.03 * sr)
    return a[max(0, idx[0] - pad): min(len(a), idx[-1] + pad)]


def level(a, target_rms=0.08):
    import numpy as np
    r = float(np.sqrt(np.mean(a ** 2))) or 1e-6
    return np.clip(a * (target_rms / r), -0.98, 0.98)


def main():
    import numpy as np
    import soundfile as sf
    import torch
    from chatterbox.tts import ChatterboxTTS

    job = json.load(sys.stdin)
    cfg_path = Path(job["config"])
    cfg = json.loads(cfg_path.read_text())
    base = cfg_path.parent
    hosts = cfg["hosts"]
    emotions = {**DEFAULT_EMOTIONS, **cfg.get("emotions", {})}
    gaps = {**DEFAULT_GAPS, **cfg.get("gaps", {})}
    rules = cfg.get("rules_chatterbox", [])
    only = set(job.get("chapters") or [])
    seed = int(cfg.get("seed", 7))
    device = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")
    model = ChatterboxTTS.from_pretrained(device=device)
    sr = model.sr

    placed, chapters, turns = [], [], []        # placed: (start_sec, audio)
    t, prev_end, overlap_next, prev_text, first = 0.6, 0.6, False, "", True
    for item in parse(base / cfg.get("script", "podcast-script.md")):
        ch = item[1]
        if only and ch not in only:
            continue
        if item[0] == "segment":
            chapters.append((t, item[2]))
        elif item[0] == "overlap":
            overlap_next = True
        elif item[0] == "pause":
            t += item[2]
            prev_end = t
        else:
            _, _, who, emo, text = item
            if who not in hosts:
                raise SystemExit(f"Speaker {who} is not in podcast.json hosts")
            h = hosts[who]
            e = {**emotions.get("neutral"), **emotions.get(emo, {}), **h.get("emotions", {}).get(emo, {})}
            ref = str((base / h["reference"]).resolve())
            pieces = []
            for k, chunk in enumerate(split_long(apply_rules(text, rules))):
                torch.manual_seed(seed + len(turns) * 10 + k)
                w = model.generate(chunk, audio_prompt_path=ref, exaggeration=float(e["exaggeration"]),
                                   cfg_weight=float(e["cfg_weight"]), temperature=float(e.get("temperature", 0.8)))
                pieces += [trim(w.squeeze(0).cpu().numpy(), sr), np.zeros(int(0.12 * sr), dtype=np.float32)]
            a = level(np.concatenate(pieces[:-1]), float(h.get("rms", 0.08)))
            if first:
                start = t
            elif overlap_next:
                start = max(prev_end + gaps["overlap"], prev_end - 0.6 * len(a) / sr)
            else:
                start = prev_end + (gaps["after_question"] if prev_text.rstrip().endswith("?") else gaps["default"])
            start = max(start, t if not overlap_next else start)
            placed.append((start, a))
            dur = len(a) / sr
            turns.append({"who": who, "emotion": emo, "start": round(start, 2), "dur": round(dur, 2), "text": text})
            prev_end = start + dur
            t = prev_end
            overlap_next, prev_text, first = False, text, False
            print(f"{t / 60:5.1f} min  {who} ({emo}): {text[:60]}", flush=True)
    total = t + 1.0
    mix = np.zeros(int(total * sr) + 1, dtype=np.float32)
    for start, a in placed:
        i = int(start * sr)
        mix[i:i + len(a)] += a[: len(mix) - i]
    mix = np.clip(mix, -0.99, 0.99)
    out = Path(job["out"])
    out.parent.mkdir(parents=True, exist_ok=True)
    sf.write(out, mix, sr)
    stem = out.with_suffix("")
    Path(f"{stem}.chapters.txt" if out.stem != "podcast" else out.parent / "chapters.txt").write_text(
        "".join(f"{int(s // 60):02d}:{int(s % 60):02d}  {n}\n" for s, n in chapters))
    Path(f"{stem}.turns.json" if out.stem != "podcast" else out.parent / "turns.json").write_text(json.dumps(turns, indent=1))
    print(f"TOTAL {total / 60:.2f} min", flush=True)


if __name__ == "__main__":
    main()
