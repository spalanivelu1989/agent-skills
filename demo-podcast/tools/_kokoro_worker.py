"""Worker that runs inside the Kokoro TTS environment (~/.cache/demo-video-tts/bin/python).

podcast.py calls it with a JSON job on stdin. Three modes:
    {"mode": "render", "config": "/abs/podcast.json"}            -> build/podcast.wav, chapters.txt, turns.json
    {"mode": "phonemes", "words": ["Infor", ...], "lang": "a"}   -> {"Infor": "❓", ...}
    {"mode": "transcribe", "files": ["/abs/a.wav"], "prompt": null} -> {"/abs/a.wav": "text"}
"""
import json
import re
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

RATE = 24000
SPAN = re.compile(r"(\[[^\]]+\]\(/[^)]+/\))")   # a misaki [word](/ipa/) span


def apply_rules(text, rules):
    """Apply [pattern, replacement] rules in order, never inside a [word](/ipa/) span."""
    for pat, rep in rules:
        parts = SPAN.split(text)
        text = "".join(p if SPAN.fullmatch(p) else re.sub(pat, rep, p) for p in parts)
    return text


def parse_script(path):
    """Yield ("segment", title) | ("pause", seconds) | ("turn", speaker, text) from podcast-script.md."""
    for line in Path(path).read_text().splitlines():
        s = line.strip()
        if s.startswith("## "):
            yield ("segment", s[3:].strip())
            continue
        m = re.fullmatch(r"\[pause ([\d.]+)\]", s)
        if m:
            yield ("pause", float(m.group(1)))
            continue
        m = re.match(r"^([A-Z][A-Z0-9_]*)(?: \((\w+)\))?: (.+)$", s)
        if m:
            yield ("turn", m.group(1), m.group(3), (m.group(2) or "neutral").lower())


def load_voice(pipe, spec):
    """'af_bella' or a weighted blend 'af_bella:0.6+af_kore:0.4' (weights are normalised)."""
    if "+" not in spec and ":" not in spec:
        return spec
    parts = [(n.split(":")[0], float(n.split(":")[1]) if ":" in n else 1.0) for n in spec.split("+")]
    total = sum(w for _, w in parts)
    return sum(pipe.load_voice(n) * (w / total) for n, w in parts)


def expand_pitch(a, k):
    """Widen intonation around the clip's median pitch by factor k (Praat PSOLA). 1.2-1.4 sounds natural."""
    import numpy as np
    import parselmouth
    from parselmouth.praat import call
    snd = parselmouth.Sound(a.astype(np.float64), RATE)
    f0 = snd.to_pitch(pitch_floor=75, pitch_ceiling=500).selected_array["frequency"]
    f0 = f0[f0 > 0]
    if len(f0) < 10:
        return a
    med = float(np.median(f0))
    m = call(snd, "To Manipulation", 0.01, 75, 500)
    pt = call(m, "Extract pitch tier")
    call(pt, "Formula", f"{med}*(self/{med})^{k}")
    call([pt, m], "Replace pitch tier")
    return call(m, "Get resynthesis (overlap-add)").values[0].astype(np.float32)


def render(cfg_path):
    import numpy as np
    import soundfile as sf
    from kokoro import KPipeline

    cfg_path = Path(cfg_path)
    cfg = json.loads(cfg_path.read_text())
    base = cfg_path.parent
    out = base / cfg.get("out_dir", "build")
    out.mkdir(parents=True, exist_ok=True)
    hosts = cfg["hosts"]
    speed = float(cfg.get("speed", 1.0))
    turn_pause = float(cfg.get("turn_pause", 0.45))
    rules = cfg.get("rules", [])
    pipes, voices = {}, {}

    def pipe_for(voice):
        lang = voice[0]                      # a = American English, b = British English
        if lang not in pipes:
            pipes[lang] = KPipeline(lang_code=lang, repo_id="hexgrad/Kokoro-82M")
        return pipes[lang]

    def sil(s):
        return np.zeros(int(RATE * s), dtype=np.float32)

    audio, t, chapters, turns = [sil(0.6)], 0.6, [], []
    for item in parse_script(base / cfg.get("script", "podcast-script.md")):
        if item[0] == "segment":
            chapters.append((t, item[1]))
        elif item[0] == "pause":
            audio.append(sil(item[1]))
            t += item[1]
        else:
            _, who, text, emo = item
            if who not in hosts:
                raise SystemExit(f"Speaker {who} is not in podcast.json hosts")
            spec = hosts[who]["voice"]
            pipe = pipe_for(spec)
            if spec not in voices:
                voices[spec] = load_voice(pipe, spec)
            spd = speed * float(hosts[who].get("speed", 1.0)) * {"excited": 1.06, "calm": 0.95}.get(emo, 1.0)
            chunks = [a.numpy() if hasattr(a, "numpy") else np.asarray(a)
                      for _, _, a in pipe(apply_rules(text, rules), voice=voices[spec], speed=spd)]
            a = np.concatenate(chunks) if chunks else sil(0.2)
            k = float(hosts[who].get("pitch_expand", 1.0))
            if k != 1.0 and len(a) > RATE // 2:
                a = expand_pitch(a, k)
            turns.append({"who": who, "start": round(t, 2), "dur": round(len(a) / RATE, 2), "text": text})
            audio += [a, sil(turn_pause)]
            t += len(a) / RATE + turn_pause
            print(f"{t / 60:5.1f} min  {who}: {text[:60]}", flush=True)
    audio.append(sil(1.0))
    t += 1.0
    sf.write(out / "podcast.wav", np.concatenate(audio), RATE)
    (out / "chapters.txt").write_text("".join(f"{int(s // 60):02d}:{int(s % 60):02d}  {n}\n" for s, n in chapters))
    (out / "turns.json").write_text(json.dumps(turns, indent=1))
    print(f"TOTAL {t / 60:.2f} min", flush=True)


def phonemes(words, lang):
    from misaki import en
    g = en.G2P(trf=False, british=lang == "b", fallback=None)
    return {w: g(w)[0] for w in words}


def transcribe(files, prompt, model):
    import mlx_whisper
    out = {}
    for f in files:
        r = mlx_whisper.transcribe(f, path_or_hf_repo=model, language="en", initial_prompt=prompt)
        out[f] = r["text"].strip()
    return out


def main():
    job = json.load(sys.stdin)
    if job["mode"] == "ref":
        import numpy as np, soundfile as sf
        from kokoro import KPipeline
        p = KPipeline(lang_code=job["voice"][0], repo_id="hexgrad/Kokoro-82M")
        a = np.concatenate([x.numpy() for _, _, x in p(job["text"], voice=job["voice"], speed=1.0)])
        Path(job["out"]).parent.mkdir(parents=True, exist_ok=True)
        sf.write(job["out"], a, RATE)
        print(json.dumps({"out": job["out"], "sec": round(len(a) / RATE, 1)}))
    elif job["mode"] == "render":
        render(job["config"])
    elif job["mode"] == "phonemes":
        json.dump(phonemes(job["words"], job.get("lang", "a")), sys.stdout)
    elif job["mode"] == "transcribe":
        json.dump(transcribe(job["files"], job.get("prompt"),
                             job.get("model", "mlx-community/whisper-small-mlx")), sys.stdout)


if __name__ == "__main__":
    main()
