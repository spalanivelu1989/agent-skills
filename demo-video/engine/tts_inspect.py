"""Inspection helpers that run in the TTS environment (used by check.py).

    echo '{"transcribe": ["a.wav", ...]}'          | python tts_inspect.py   → {"a.wav": "text", ...}
    echo '{"phonemes": ["SAP", "L2C"], "lang": "a"}' | python tts_inspect.py → {"SAP": "sˈæp", ...}
"""
import json
import sys
import warnings

warnings.filterwarnings("ignore")


def load16k(path):
    """Audio as 16 kHz mono float32. Whisper's own loader shells out to ffmpeg, which may be
    missing (mlx-whisper then fails with FileNotFoundError: 'ffmpeg'); WAVs need no ffmpeg."""
    import numpy as np
    import soundfile as sf
    a, rate = sf.read(path, dtype="float32", always_2d=True)
    a = a.mean(axis=1)
    if rate != 16000:
        n = int(len(a) * 16000 / rate)
        a = np.interp(np.linspace(0, len(a) - 1, n), np.arange(len(a)), a).astype("float32")
    return a


def transcribe(files, prompt):
    """Whisper small: mlx-whisper on Apple Silicon, faster-whisper (CPU) everywhere else."""
    try:
        import mlx_whisper
    except ImportError:
        from faster_whisper import WhisperModel
        model = WhisperModel("small", device="cpu", compute_type="int8")
        return {f: "".join(seg.text for seg in model.transcribe(load16k(f), language="en", initial_prompt=prompt)[0]).strip()
                for f in files}
    return {f: mlx_whisper.transcribe(load16k(f), path_or_hf_repo="mlx-community/whisper-small-mlx",
                                      language="en", initial_prompt=prompt)["text"].strip()
            for f in files}


def main():
    job = json.load(sys.stdin)
    out = {}
    if job.get("transcribe"):
        out.update(transcribe(job["transcribe"], job.get("prompt")))
    if job.get("phonemes"):
        from misaki import en
        g = en.G2P(trf=False, british=job.get("lang") == "b", fallback=None)
        for w in job["phonemes"]:
            out[w] = g(w)[0]
    json.dump(out, sys.stdout)


if __name__ == "__main__":
    main()
